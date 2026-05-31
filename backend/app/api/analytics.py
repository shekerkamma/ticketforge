import csv
import io
import json
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db import get_session
from app.models.pipeline_run import PipelineRun
from app.models.repository import Repository
from app.models.team import TeamMember
from app.models.ticket import Ticket
from app.models.user import User

router = APIRouter(prefix="/api/v1/teams/{team_id}", tags=["analytics"])

PERIOD_DAYS = {"7d": 7, "30d": 30, "90d": 90}


@router.get("/analytics")
async def get_analytics(
    team_id: uuid.UUID,
    period: str = Query(default="30d", pattern="^(7d|30d|90d)$"),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    # Verify membership
    result = await session.execute(
        select(TeamMember).where(TeamMember.team_id == team_id, TeamMember.user_id == user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(403, detail="Not a member of this team")

    days = PERIOD_DAYS.get(period, 30)
    since = datetime.now(timezone.utc) - timedelta(days=days)

    # Get repo IDs for this team
    repo_result = await session.execute(
        select(Repository.id).where(Repository.team_id == team_id)
    )
    repo_ids = [r for (r,) in repo_result.all()]

    if not repo_ids:
        return {
            "period": period,
            "tickets_processed": 0,
            "prs_created": 0,
            "prs_merged": 0,
            "escalations": 0,
            "acceptance_rate": 0.0,
            "avg_fix_time_seconds": 0,
            "tokens_used": 0,
            "estimated_hours_saved": 0.0,
        }

    # Tickets processed
    tickets_result = await session.execute(
        select(func.count())
        .select_from(Ticket)
        .where(Ticket.repository_id.in_(repo_ids), Ticket.created_at >= since)
    )
    tickets_processed = tickets_result.scalar() or 0

    # Pipeline runs in period
    runs_result = await session.execute(
        select(PipelineRun)
        .join(Ticket, Ticket.id == PipelineRun.ticket_id)
        .where(Ticket.repository_id.in_(repo_ids), PipelineRun.started_at >= since)
    )
    runs = list(runs_result.scalars().all())

    prs_created = sum(1 for r in runs if r.pr_number is not None)
    prs_merged = sum(1 for r in runs if r.pr_status == "merged")
    escalations = sum(1 for r in runs if r.status == "escalated")
    tokens_used = sum(r.tokens_used or 0 for r in runs)

    # Acceptance rate
    completed_runs = [r for r in runs if r.status == "completed"]
    acceptance_rate = (prs_merged / len(completed_runs) * 100) if completed_runs else 0.0

    # Average fix time
    durations = [r.duration_seconds for r in runs if r.duration_seconds]
    avg_fix_time = int(sum(durations) / len(durations)) if durations else 0

    # Estimated hours saved (accepted PRs * 2 hours)
    estimated_hours_saved = prs_merged * 2.0

    return {
        "period": period,
        "tickets_processed": tickets_processed,
        "prs_created": prs_created,
        "prs_merged": prs_merged,
        "escalations": escalations,
        "acceptance_rate": round(acceptance_rate, 1),
        "avg_fix_time_seconds": avg_fix_time,
        "tokens_used": tokens_used,
        "estimated_hours_saved": estimated_hours_saved,
    }


@router.get("/analytics/export")
async def export_analytics(
    team_id: uuid.UUID,
    period: str = Query(default="30d", pattern="^(7d|30d|90d)$"),
    format: str = Query(default="csv", pattern="^(csv|json)$"),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    # Verify membership
    result = await session.execute(
        select(TeamMember).where(TeamMember.team_id == team_id, TeamMember.user_id == user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(403, detail="Not a member of this team")

    days = PERIOD_DAYS.get(period, 30)
    since = datetime.now(timezone.utc) - timedelta(days=days)

    repo_result = await session.execute(
        select(Repository.id, Repository.full_name).where(Repository.team_id == team_id)
    )
    repos = {r_id: name for r_id, name in repo_result.all()}

    if not repos:
        if format == "json":
            return {"tickets": []}
        return StreamingResponse(
            io.StringIO("No data"),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=analytics.csv"},
        )

    # Get ticket-level data with latest pipeline run
    tickets_result = await session.execute(
        select(Ticket)
        .where(Ticket.repository_id.in_(repos.keys()), Ticket.created_at >= since)
        .order_by(Ticket.created_at.desc())
    )
    tickets = list(tickets_result.scalars().all())

    rows = []
    for ticket in tickets:
        run_result = await session.execute(
            select(PipelineRun)
            .where(PipelineRun.ticket_id == ticket.id)
            .order_by(PipelineRun.started_at.desc())
            .limit(1)
        )
        run = run_result.scalar_one_or_none()

        rows.append({
            "issue_number": ticket.github_issue_number,
            "repo": repos.get(ticket.repository_id, "unknown"),
            "title": ticket.title,
            "status": ticket.status,
            "priority": ticket.priority,
            "created_at": ticket.created_at.isoformat(),
            "fix_time_seconds": run.duration_seconds if run else None,
            "pr_number": run.pr_number if run else None,
            "pr_status": run.pr_status if run else None,
            "tokens_used": run.tokens_used if run else 0,
        })

    if format == "json":
        return {"tickets": rows}

    # CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=rows[0].keys() if rows else [])
    writer.writeheader()
    writer.writerows(rows)

    return StreamingResponse(
        io.StringIO(output.getvalue()),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=ticketforge-analytics-{period}.csv"
        },
    )
