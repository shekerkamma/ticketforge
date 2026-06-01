import uuid

from arq import create_pool
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db import get_session
from app.models.pipeline_run import PipelineRun
from app.models.ticket import Ticket
from app.models.user import User

router = APIRouter(prefix="/api/v1/teams/{team_id}", tags=["dashboard"])


@router.post("/tickets/{ticket_id}/retry")
async def retry_pipeline(
    team_id: uuid.UUID,
    ticket_id: uuid.UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    # Check admin access
    from app.models.team import TeamMember

    membership_result = await session.execute(
        select(TeamMember).where(
            TeamMember.team_id == team_id,
            TeamMember.user_id == user.id,
        )
    )
    member = membership_result.scalar_one_or_none()
    if not member or member.role not in ("owner", "admin"):
        raise HTTPException(403, detail="Admin access required")

    # Load ticket
    ticket_result = await session.execute(
        select(Ticket).where(Ticket.id == ticket_id)
    )
    ticket = ticket_result.scalar_one_or_none()
    if not ticket:
        raise HTTPException(404, detail="Ticket not found")

    if ticket.status not in ("escalated", "failed"):
        raise HTTPException(
            400,
            detail=(
                f"Cannot retry ticket with status '{ticket.status}'. "
                "Only 'escalated' or 'failed' tickets can be retried."
            ),
        )

    # Create new pipeline run
    pipeline_run = PipelineRun(
        ticket_id=ticket.id,
        status="running",
    )
    session.add(pipeline_run)
    ticket.status = "pending"
    await session.commit()
    await session.refresh(pipeline_run)

    # Enqueue pipeline task
    try:
        from app.worker import WorkerSettings

        redis = await create_pool(WorkerSettings.redis_settings)
        await redis.enqueue_job("run_pipeline", str(ticket.id))
        await redis.close()
    except Exception:
        pass

    return {
        "ticket_id": str(ticket.id),
        "pipeline_run_id": str(pipeline_run.id),
        "status": "running",
    }
