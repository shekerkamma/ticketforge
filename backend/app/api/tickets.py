import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db import get_session
from app.models.event import Event
from app.models.pipeline_run import PipelineRun
from app.models.repository import Repository
from app.models.team import TeamMember
from app.models.ticket import Ticket
from app.models.user import User

router = APIRouter(prefix="/api/v1/teams/{team_id}/tickets", tags=["tickets"])


async def _require_member(team_id: uuid.UUID, user: User, session: AsyncSession):
    membership_result = await session.execute(
        select(TeamMember).where(TeamMember.team_id == team_id, TeamMember.user_id == user.id)
    )
    if not membership_result.scalar_one_or_none():
        raise HTTPException(403, detail="Not a member of this team")


@router.get("")
async def list_tickets(
    team_id: uuid.UUID,
    status: str | None = None,
    repo_id: uuid.UUID | None = None,
    cursor: str | None = None,
    limit: int = Query(default=50, le=100),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    await _require_member(team_id, user, session)

    # Get repos for this team
    repo_query = select(Repository.id).where(Repository.team_id == team_id)
    if repo_id:
        repo_query = repo_query.where(Repository.id == repo_id)
    repo_result = await session.execute(repo_query)
    repo_ids = [r for (r,) in repo_result.all()]

    if not repo_ids:
        return {"tickets": [], "next_cursor": None}

    query = (
        select(Ticket, Repository.full_name)
        .join(Repository, Repository.id == Ticket.repository_id)
        .where(Ticket.repository_id.in_(repo_ids))
        .order_by(Ticket.created_at.desc())
    )

    if status:
        query = query.where(Ticket.status == status)

    if cursor:
        query = query.where(Ticket.id < uuid.UUID(cursor))

    query = query.limit(limit + 1)
    result = await session.execute(query)
    rows = result.all()

    has_more = len(rows) > limit
    rows = rows[:limit]

    tickets = []
    for ticket, repo_name in rows:
        # Get latest pipeline run
        run_result = await session.execute(
            select(PipelineRun)
            .where(PipelineRun.ticket_id == ticket.id)
            .order_by(PipelineRun.started_at.desc())
            .limit(1)
        )
        latest_run = run_result.scalar_one_or_none()

        tickets.append({
            "id": str(ticket.id),
            "repo_full_name": repo_name,
            "issue_number": ticket.github_issue_number,
            "title": ticket.title,
            "status": ticket.status,
            "created_at": ticket.created_at.isoformat(),
            "latest_run": {
                "id": str(latest_run.id),
                "status": latest_run.status,
                "pr_url": latest_run.pr_url,
                "duration_seconds": latest_run.duration_seconds,
            } if latest_run else None,
        })

    next_cursor = str(tickets[-1]["id"]) if has_more and tickets else None
    return {"tickets": tickets, "next_cursor": next_cursor}


@router.get("/{ticket_id}")
async def get_ticket(
    team_id: uuid.UUID,
    ticket_id: uuid.UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    await _require_member(team_id, user, session)

    ticket_result = await session.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = ticket_result.scalar_one_or_none()
    if not ticket:
        raise HTTPException(404, detail="Ticket not found")

    # Get pipeline runs
    run_result = await session.execute(
        select(PipelineRun)
        .where(PipelineRun.ticket_id == ticket_id)
        .order_by(PipelineRun.started_at.desc())
    )
    runs = [
        {
            "id": str(run.id),
            "status": run.status,
            "started_at": run.started_at.isoformat() if run.started_at else None,
            "duration_seconds": run.duration_seconds,
            "pr_url": run.pr_url,
            "pr_number": run.pr_number,
            "escalation_reason": run.escalation_reason,
        }
        for run in run_result.scalars().all()
    ]

    return {
        "ticket": {
            "id": str(ticket.id),
            "issue_number": ticket.github_issue_number,
            "github_issue_url": ticket.github_issue_url,
            "title": ticket.title,
            "body": ticket.body,
            "labels": ticket.labels,
            "status": ticket.status,
            "created_at": ticket.created_at.isoformat(),
        },
        "pipeline_runs": runs,
    }


@router.get("/{ticket_id}/runs/{run_id}/events")
async def get_run_events(
    team_id: uuid.UUID,
    ticket_id: uuid.UUID,
    run_id: uuid.UUID,
    cursor: str | None = None,
    limit: int = Query(default=50, le=100),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    await _require_member(team_id, user, session)

    query = (
        select(Event)
        .where(Event.pipeline_run_id == run_id)
        .order_by(Event.timestamp)
    )

    if cursor:
        query = query.where(Event.id > uuid.UUID(cursor))

    query = query.limit(limit + 1)
    result = await session.execute(query)
    events_list = list(result.scalars().all())

    has_more = len(events_list) > limit
    events_list = events_list[:limit]

    events = [
        {
            "id": str(e.id),
            "agent_name": e.agent_name,
            "event_type": e.event_type,
            "payload": e.payload,
            "timestamp": e.timestamp.isoformat(),
        }
        for e in events_list
    ]

    next_cursor = events[-1]["id"] if has_more and events else None
    return {"events": events, "next_cursor": next_cursor}
