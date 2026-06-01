import logging
import uuid
from datetime import UTC, datetime

from sqlalchemy import func, select

from app.agents.code_act_agent import CodeActAgent
from app.agents.code_reviewer import CodeReviewerAgent
from app.agents.content_researcher import ContentResearcherAgent
from app.agents.escalation import EscalationHandler
from app.agents.pr_creator import PRCreatorAgent
from app.api.billing import PLAN_LIMITS
from app.db import async_session_factory
from app.models.pipeline_run import PipelineRun
from app.models.repository import Repository
from app.models.team import Team
from app.models.ticket import Ticket
from app.models.user import User
from app.services.claude_service import ClaudeService
from app.services.docker_service import DockerService
from app.services.event_logger import EventLogger
from app.services.github_service import GitHubService

logger = logging.getLogger(__name__)


async def run_pipeline(_ctx: dict, ticket_id: str) -> str:
    logger.info("Pipeline started for ticket %s", ticket_id)

    async with async_session_factory() as session:
        # Load ticket
        ticket_result = await session.execute(
            select(Ticket).where(Ticket.id == uuid.UUID(ticket_id))
        )
        ticket = ticket_result.scalar_one_or_none()
        if not ticket:
            logger.error("Ticket %s not found", ticket_id)
            return f"Ticket {ticket_id} not found"

        # Load repository
        repository_result = await session.execute(
            select(Repository).where(Repository.id == ticket.repository_id)
        )
        repo = repository_result.scalar_one_or_none()
        if not repo:
            logger.error(
                "Repository %s not found for ticket %s",
                ticket.repository_id,
                ticket_id,
            )
            ticket.status = "failed"
            await session.commit()
            return f"Ticket {ticket_id} failed: repository not found"

        # Load team and owner for GitHub token
        team_result = await session.execute(
            select(Team).where(Team.id == repo.team_id)
        )
        team = team_result.scalar_one_or_none()
        if not team:
            logger.error("Team %s not found for repository %s", repo.team_id, repo.id)
            ticket.status = "failed"
            await session.commit()
            return f"Ticket {ticket_id} failed: team not found"

        owner_result = await session.execute(
            select(User).where(User.id == team.owner_id)
        )
        owner = owner_result.scalar_one_or_none()
        github_token = owner.github_access_token if owner else ""

        # Check ticket limit for current billing period
        month_start = datetime.now(UTC).replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )
        usage_result = await session.execute(
            select(func.count())
            .select_from(Ticket)
            .where(
                Ticket.repository_id.in_(
                    select(Repository.id).where(Repository.team_id == team.id)
                ),
                Ticket.created_at >= month_start,
            )
        )
        monthly_count = usage_result.scalar() or 0
        plan_limit = PLAN_LIMITS.get(team.plan, 20)

        if monthly_count > plan_limit:
            ticket.status = "failed"
            await session.commit()
            logger.warning(
                "Ticket %s rejected: team %s at %d/%d monthly limit",
                ticket_id,
                team.id,
                monthly_count,
                plan_limit,
            )
            return (
                f"Ticket {ticket_id} rejected: monthly ticket limit reached "
                f"({monthly_count}/{plan_limit})"
            )

        # Create pipeline run
        pipeline_run = PipelineRun(
            ticket_id=ticket.id,
            status="running",
        )
        session.add(pipeline_run)
        await session.commit()
        await session.refresh(pipeline_run)

        # Update ticket status
        ticket.status = "analyzing"
        await session.commit()

        event_logger = EventLogger(session)
        claude_service = ClaudeService()
        escalation = EscalationHandler(pipeline_run.id, event_logger)
        slack_url = (repo.config or {}).get("slack_webhook_url", "")

        # --- Step 1: Content Analysis ---
        researcher = ContentResearcherAgent(pipeline_run.id, event_logger, claude_service)
        analysis_result = await researcher.run({
            "title": ticket.title,
            "body": ticket.body,
            "labels": ticket.labels,
            "issue_number": ticket.github_issue_number,
        })

        pipeline_run.analysis = (
            analysis_result.output if isinstance(analysis_result.output, dict) else {}
        )
        pipeline_run.tokens_used = analysis_result.tokens_used

        if analysis_result.error and "APIConnectionError" in str(analysis_result.error):
            ticket.status = "pending"
            pipeline_run.status = "failed"
            pipeline_run.escalation_reason = "Claude API unavailable — ticket will be retried"
            pipeline_run.completed_at = datetime.now(UTC)
            await session.commit()
            logger.warning(
                "Claude API down for ticket %s — leaving as pending for retry",
                ticket_id,
            )
            return f"Ticket {ticket_id} queued for retry: Claude API unavailable"

        if not analysis_result.success:
            # Escalate
            ticket.status = "escalated"
            pipeline_run.status = "escalated"
            pipeline_run.escalation_reason = analysis_result.error
            pipeline_run.completed_at = datetime.now(UTC)
            await session.commit()

            await escalation.escalate(
                repo_full_name=repo.full_name,
                issue_number=ticket.github_issue_number,
                github_token=github_token,
                agent_name="content_researcher",
                reason=analysis_result.error or "Low confidence analysis",
                partial_analysis=analysis_result.output,
                slack_webhook_url=slack_url,
            )
            return f"Ticket {ticket_id} escalated: {analysis_result.error}"

        # --- Step 2: Code Generation ---
        ticket.status = "generating"
        await session.commit()

        docker_service = DockerService()
        code_agent = CodeActAgent(pipeline_run.id, event_logger, claude_service, docker_service)
        fix_result = await code_agent.run({
            "analysis": analysis_result.output,
            "repo_url": f"https://github.com/{repo.full_name}.git",
            "branch": "main",
            "github_token": github_token,
        })

        pipeline_run.tokens_used = fix_result.tokens_used

        if not fix_result.success:
            ticket.status = "escalated"
            pipeline_run.status = "escalated"
            pipeline_run.escalation_reason = fix_result.error
            pipeline_run.completed_at = datetime.now(UTC)
            await session.commit()

            await escalation.escalate(
                repo_full_name=repo.full_name,
                issue_number=ticket.github_issue_number,
                github_token=github_token,
                agent_name="code_act_agent",
                reason=fix_result.error or "Failed to generate fix",
                partial_analysis=analysis_result.output,
                slack_webhook_url=slack_url,
            )
            return f"Ticket {ticket_id} escalated: {fix_result.error}"

        # Save the diff
        fix_output = fix_result.output if isinstance(fix_result.output, dict) else {}
        pipeline_run.fix_diff = fix_output.get("diff", "")
        await session.commit()

        # --- Step 3: Code Review ---
        ticket.status = "reviewing"
        await session.commit()

        reviewer = CodeReviewerAgent(pipeline_run.id, event_logger, claude_service)
        review_result = await reviewer.run({
            "diff": pipeline_run.fix_diff,
            "analysis": analysis_result.output,
            "repo_config": repo.config or {},
        })

        pipeline_run.review_result = (
            review_result.output if isinstance(review_result.output, dict) else {}
        )
        pipeline_run.tokens_used = review_result.tokens_used

        if not review_result.success:
            ticket.status = "escalated"
            pipeline_run.status = "escalated"
            pipeline_run.escalation_reason = review_result.error
            pipeline_run.completed_at = datetime.now(UTC)
            await session.commit()

            await escalation.escalate(
                repo_full_name=repo.full_name,
                issue_number=ticket.github_issue_number,
                github_token=github_token,
                agent_name="code_reviewer",
                reason=review_result.error or "Review failed",
                partial_analysis=analysis_result.output,
                slack_webhook_url=slack_url,
            )
            return f"Ticket {ticket_id} escalated: {review_result.error}"

        # --- Step 4: PR Creation ---
        github_service = GitHubService()
        pr_agent = PRCreatorAgent(
            pipeline_run.id, event_logger, docker_service, github_service
        )
        pr_result = await pr_agent.run({
            "repo_full_name": repo.full_name,
            "repo_url": f"https://github.com/{repo.full_name}.git",
            "issue_number": ticket.github_issue_number,
            "diff": pipeline_run.fix_diff,
            "analysis": analysis_result.output if isinstance(analysis_result.output, dict) else {},
            "review": review_result.output if isinstance(review_result.output, dict) else {},
            "github_token": github_token,
        })

        if not pr_result.success:
            # Retry once, then escalate with diff saved
            ticket.status = "escalated"
            pipeline_run.status = "escalated"
            pipeline_run.escalation_reason = pr_result.error
            pipeline_run.completed_at = datetime.now(UTC)
            await session.commit()

            await escalation.escalate(
                repo_full_name=repo.full_name,
                issue_number=ticket.github_issue_number,
                github_token=github_token,
                agent_name="pr_creator",
                reason=pr_result.error or "PR creation failed",
                partial_analysis=analysis_result.output,
                slack_webhook_url=slack_url,
            )
            return f"Ticket {ticket_id} escalated: {pr_result.error}"

        # Success — update pipeline run with PR info
        pr_output = pr_result.output if isinstance(pr_result.output, dict) else {}
        pipeline_run.pr_number = pr_output.get("pr_number")
        pipeline_run.pr_url = pr_output.get("pr_url")
        pipeline_run.pr_status = "open"

        ticket.status = "pr_created"
        pipeline_run.status = "completed"
        pipeline_run.completed_at = datetime.now(UTC)
        if pipeline_run.started_at:
            delta = pipeline_run.completed_at - pipeline_run.started_at
            pipeline_run.duration_seconds = int(delta.total_seconds())
        await session.commit()

        logger.info(
            "Pipeline completed for ticket %s — PR #%s created: %s",
            ticket_id,
            pipeline_run.pr_number,
            pipeline_run.pr_url,
        )
        return f"Pipeline completed for ticket {ticket_id} — PR #{pipeline_run.pr_number}"
