import asyncio
import json
import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db import async_session_factory, get_session
from app.models.event import Event
from app.models.pipeline_run import PipelineRun
from app.models.repository import Repository
from app.models.team import TeamMember
from app.models.ticket import Ticket
from app.models.user import User

router = APIRouter(prefix="/api/v1/teams/{team_id}", tags=["sse"])


@router.get("/events/stream")
async def event_stream(
    team_id: uuid.UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    # Verify membership
    result = await session.execute(
        select(TeamMember).where(TeamMember.team_id == team_id, TeamMember.user_id == user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(403, detail="Not a member of this team")

    async def generate():
        last_event_id = None
        while True:
            try:
                # Poll for new events
                query = (
                    select(Event)
                    .join(PipelineRun, PipelineRun.id == Event.pipeline_run_id)
                    .join(Ticket, Ticket.id == PipelineRun.ticket_id)
                    .join(Repository, Repository.id == Ticket.repository_id)
                    .where(Repository.team_id == team_id)
                    .order_by(Event.timestamp.desc())
                    .limit(10)
                )
                if last_event_id:
                    query = query.where(Event.id > last_event_id)

                async with async_session_factory() as poll_session:
                    result = await poll_session.execute(query)
                    events = list(result.scalars().all())

                for event in reversed(events):
                    data = {
                        "id": str(event.id),
                        "agent_name": event.agent_name,
                        "event_type": event.event_type,
                        "payload": event.payload,
                        "timestamp": event.timestamp.isoformat(),
                    }
                    yield f"data: {json.dumps(data)}\n\n"
                    last_event_id = event.id

                await asyncio.sleep(2)
            except asyncio.CancelledError:
                break
            except Exception:
                yield f"data: {json.dumps({'error': 'stream_error'})}\n\n"
                await asyncio.sleep(5)

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
