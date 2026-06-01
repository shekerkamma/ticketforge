import uuid
from datetime import UTC, datetime

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.config import settings
from app.db import get_session
from app.models.repository import Repository
from app.models.team import Team, TeamMember
from app.models.ticket import Ticket
from app.models.user import User

router = APIRouter(tags=["billing"])

stripe.api_key = settings.stripe_secret_key

PLAN_LIMITS = {
    "free": 20,
    "team": 500,
    "enterprise": 10_000,
}


@router.post("/api/v1/teams/{team_id}/billing/checkout")
async def create_checkout_session(
    team_id: uuid.UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    # Only team owner can upgrade
    result = await session.execute(
        select(TeamMember).where(
            TeamMember.team_id == team_id,
            TeamMember.user_id == user.id,
            TeamMember.role == "owner",
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(403, detail="Only team owners can manage billing")

    team_result = await session.execute(select(Team).where(Team.id == team_id))
    team = team_result.scalar_one_or_none()
    if not team:
        raise HTTPException(404, detail="Team not found")

    if team.plan != "free":
        raise HTTPException(400, detail="Team already has an active subscription")

    # Create or reuse Stripe customer
    if not team.stripe_customer_id:
        if not user.email:
            raise HTTPException(400, detail="User email is required for billing")
        customer = stripe.Customer.create(
            email=user.email,
            metadata={"team_id": str(team_id), "github_login": user.github_login},
        )
        team.stripe_customer_id = customer.id
        await session.commit()

    checkout = stripe.checkout.Session.create(
        customer=team.stripe_customer_id,
        line_items=[{"price": settings.stripe_price_id_team, "quantity": 1}],
        mode="subscription",
        success_url=f"{settings.app_url}/dashboard/settings?billing=success",
        cancel_url=f"{settings.app_url}/dashboard/settings?billing=cancelled",
        metadata={"team_id": str(team_id)},
    )

    return {"checkout_url": checkout.url}


@router.post("/api/webhooks/stripe")
async def stripe_webhook(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
    except (ValueError, stripe.SignatureVerificationError):
        raise HTTPException(400, detail="Invalid webhook signature")

    if event["type"] == "checkout.session.completed":
        session_data = event["data"]["object"]
        team_id = session_data.get("metadata", {}).get("team_id")
        subscription_id = session_data.get("subscription")

        if team_id and subscription_id:
            result = await session.execute(
                select(Team).where(Team.id == uuid.UUID(team_id))
            )
            team = result.scalar_one_or_none()
            if team:
                team.plan = "team"
                team.stripe_subscription_id = subscription_id
                await session.commit()

    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        subscription_id = subscription["id"]

        result = await session.execute(
            select(Team).where(Team.stripe_subscription_id == subscription_id)
        )
        team = result.scalar_one_or_none()
        if team:
            team.plan = "free"
            team.stripe_subscription_id = None
            await session.commit()

    return {"received": True}


@router.get("/api/v1/teams/{team_id}/billing")
async def get_billing_info(
    team_id: uuid.UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(TeamMember).where(
            TeamMember.team_id == team_id, TeamMember.user_id == user.id
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(403, detail="Not a member of this team")

    team_result = await session.execute(select(Team).where(Team.id == team_id))
    team = team_result.scalar_one_or_none()
    if not team:
        raise HTTPException(404, detail="Team not found")

    # Get current month usage
    month_start = datetime.now(UTC).replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )
    repo_result = await session.execute(
        select(Repository.id).where(Repository.team_id == team_id)
    )
    repo_ids = [r for (r,) in repo_result.all()]

    monthly_usage = 0
    if repo_ids:
        usage_result = await session.execute(
            select(func.count())
            .select_from(Ticket)
            .where(
                Ticket.repository_id.in_(repo_ids),
                Ticket.created_at >= month_start,
            )
        )
        monthly_usage = usage_result.scalar() or 0

    limit = PLAN_LIMITS.get(team.plan, 20)

    return {
        "plan": team.plan,
        "ticket_limit": limit,
        "tickets_used": monthly_usage,
        "tickets_remaining": max(0, limit - monthly_usage),
        "has_subscription": team.stripe_subscription_id is not None,
    }
