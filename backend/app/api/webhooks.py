import hashlib
import hmac
import logging

from fastapi import APIRouter, Header, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy import select

from app.config import settings
from app.db import async_session_factory
from app.models.pipeline_run import PipelineRun
from app.models.repository import Repository
from app.models.ticket import Ticket

router = APIRouter(tags=["webhooks"])

limiter = Limiter(key_func=get_remote_address)
logger = logging.getLogger(__name__)


def verify_signature(payload: bytes, signature: str | None, secret: str) -> bool:
    if not signature:
        return False
    expected = "sha256=" + hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


@router.post("/api/webhooks/github")
@limiter.limit("100/minute")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str | None = Header(None),
    x_github_event: str | None = Header(None),
):
    payload = await request.body()

    if not verify_signature(payload, x_hub_signature_256, settings.github_webhook_secret):
        raise HTTPException(401, detail="Invalid signature")

    if x_github_event not in ("issues", "pull_request"):
        return {"received": True, "action": "ignored", "reason": "unhandled event type"}

    data = await request.json()
    action = data.get("action")

    # Handle PR closed events (merged or rejected)
    if x_github_event == "pull_request" and action == "closed":
        pr = data.get("pull_request", {})
        pr_number = pr.get("number")
        merged = pr.get("merged", False)

        async with async_session_factory() as session:
            pipeline_run_result = await session.execute(
                select(PipelineRun).where(PipelineRun.pr_number == pr_number)
            )
            pipeline_run = pipeline_run_result.scalar_one_or_none()
            if pipeline_run:
                pipeline_run.pr_status = "merged" if merged else "rejected"
                await session.commit()
                logger.info(
                    "PR #%d %s for pipeline run %s",
                    pr_number,
                    "merged" if merged else "rejected",
                    pipeline_run.id,
                )

        return {"received": True, "action": "pr_status_updated"}

    if action not in ("opened", "labeled"):
        return {"received": True, "action": "ignored", "reason": f"unhandled action: {action}"}

    issue = data.get("issue", {})
    repo_data = data.get("repository", {})
    github_repo_id = repo_data.get("id")
    issue_labels = [label["name"] for label in issue.get("labels", [])]

    async with async_session_factory() as session:
        # Find the repository
        repository_result = await session.execute(
            select(Repository).where(
                Repository.github_repo_id == github_repo_id,
                Repository.is_active.is_(True),
            )
        )
        repo = repository_result.scalar_one_or_none()

        if not repo:
            return {"received": True, "action": "ignored", "reason": "repo not registered"}

        # Check trigger labels
        trigger_labels = repo.trigger_labels or ["bug"]
        if not any(label in trigger_labels for label in issue_labels):
            return {"received": True, "action": "ignored", "reason": "no matching trigger label"}

        # Idempotent: check if ticket already exists
        existing = await session.execute(
            select(Ticket).where(
                Ticket.repository_id == repo.id,
                Ticket.github_issue_number == issue["number"],
            )
        )
        if existing.scalar_one_or_none():
            return {"received": True, "action": "ignored", "reason": "ticket already exists"}

        # Determine priority from labels
        priority_map = {"critical": 0, "high": 1, "medium": 2, "low": 4}
        priority = 3  # default (unlabeled)
        for label in issue_labels:
            if label.lower() in priority_map:
                priority = min(priority, priority_map[label.lower()])

        # Create ticket
        ticket = Ticket(
            repository_id=repo.id,
            github_issue_number=issue["number"],
            github_issue_url=issue.get("html_url", ""),
            title=issue.get("title", ""),
            body=issue.get("body"),
            labels=issue_labels,
            priority=priority,
            status="pending",
        )
        session.add(ticket)
        await session.commit()
        await session.refresh(ticket)

        logger.info(
            "Ticket created: %s for %s#%d",
            ticket.id,
            repo.full_name,
            issue["number"],
        )

        # Enqueue pipeline run (will be wired to ARQ in TASK-018)
        # For now, import is deferred to avoid circular dependency
        try:
            from arq import create_pool
            from app.worker import WorkerSettings

            redis = await create_pool(WorkerSettings.redis_settings)
            await redis.enqueue_job("run_pipeline", str(ticket.id))
            await redis.close()
        except Exception as e:
            logger.warning("Failed to enqueue pipeline job: %s", e)

    return {"received": True, "action": "ticket_created", "ticket_id": str(ticket.id)}
