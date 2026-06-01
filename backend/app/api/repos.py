import uuid
from typing import cast

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.config import settings
from app.db import get_session
from app.models.repository import Repository
from app.models.team import TeamMember
from app.models.user import User
from app.services.github_service import GitHubService

router = APIRouter(prefix="/api/v1/teams/{team_id}/repos", tags=["repositories"])


class ConnectRepoRequest(BaseModel):
    github_repo_full_name: str = Field(pattern=r"^[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+$")
    trigger_labels: list[str] | None = None

    @field_validator("trigger_labels")
    @classmethod
    def validate_labels(cls, v: list[str] | None) -> list[str] | None:
        if v is not None:
            return [label.strip()[:50] for label in v if label.strip()][:20]
        return v


class UpdateRepoRequest(BaseModel):
    trigger_labels: list[str] | None = None
    is_active: bool | None = None
    config: dict | None = None

    @field_validator("trigger_labels")
    @classmethod
    def validate_labels(cls, v: list[str] | None) -> list[str] | None:
        if v is not None:
            return [label.strip()[:50] for label in v if label.strip()][:20]
        return v


async def _require_admin(team_id: uuid.UUID, user: User, session: AsyncSession):
    result = await session.execute(
        select(TeamMember).where(TeamMember.team_id == team_id, TeamMember.user_id == user.id)
    )
    member = result.scalar_one_or_none()
    if not member or member.role not in ("owner", "admin"):
        raise HTTPException(403, detail="Admin access required")


async def _require_member(team_id: uuid.UUID, user: User, session: AsyncSession):
    result = await session.execute(
        select(TeamMember).where(TeamMember.team_id == team_id, TeamMember.user_id == user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(403, detail="Not a member of this team")


@router.get("")
async def list_repos(
    team_id: uuid.UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    await _require_member(team_id, user, session)
    result = await session.execute(
        select(Repository).where(Repository.team_id == team_id)
    )
    repos = [
        {
            "id": str(r.id),
            "full_name": r.full_name,
            "is_active": r.is_active,
            "trigger_labels": r.trigger_labels,
        }
        for r in result.scalars().all()
    ]
    return {"repositories": repos}


@router.post("", status_code=201)
async def connect_repo(
    team_id: uuid.UUID,
    body: ConnectRepoRequest,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    await _require_admin(team_id, user, session)

    github = GitHubService()
    try:
        webhook_url = f"{settings.api_url}/api/webhooks/github"
        webhook_id = await github.register_webhook(
            repo=body.github_repo_full_name,
            url=webhook_url,
            secret=settings.github_webhook_secret,
            token=user.github_access_token,
        )
    except Exception as e:
        raise HTTPException(400, detail=f"Webhook registration failed: {e}")
    finally:
        await github.close()

    # Get repo ID from GitHub API
    try:
        import httpx

        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"https://api.github.com/repos/{body.github_repo_full_name}",
                headers={"Authorization": f"Bearer {user.github_access_token}"},
            )
            resp.raise_for_status()
            github_repo_id = resp.json()["id"]
    except Exception:
        github_repo_id = hash(body.github_repo_full_name) & 0x7FFFFFFF

    repo = Repository(
        team_id=team_id,
        github_repo_id=github_repo_id,
        full_name=body.github_repo_full_name,
        webhook_id=webhook_id,
        trigger_labels=body.trigger_labels or ["bug"],
    )
    session.add(repo)
    await session.commit()
    await session.refresh(repo)

    return {
        "id": str(repo.id),
        "full_name": repo.full_name,
        "webhook_id": repo.webhook_id,
        "trigger_labels": repo.trigger_labels,
    }


@router.patch("/{repo_id}")
async def update_repo(
    team_id: uuid.UUID,
    repo_id: uuid.UUID,
    body: UpdateRepoRequest,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    await _require_admin(team_id, user, session)

    result = await session.execute(
        select(Repository).where(Repository.id == repo_id, Repository.team_id == team_id)
    )
    repo = result.scalar_one_or_none()
    if not repo:
        raise HTTPException(404, detail="Repository not found")

    if body.trigger_labels is not None:
        repo.trigger_labels = cast(dict, body.trigger_labels)
    if body.is_active is not None:
        repo.is_active = body.is_active
    if body.config is not None:
        repo.config = cast(dict, body.config)

    await session.commit()
    await session.refresh(repo)

    return {
        "id": str(repo.id),
        "full_name": repo.full_name,
        "trigger_labels": repo.trigger_labels,
        "is_active": repo.is_active,
        "config": repo.config,
    }


@router.delete("/{repo_id}", status_code=204)
async def delete_repo(
    team_id: uuid.UUID,
    repo_id: uuid.UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    await _require_admin(team_id, user, session)

    result = await session.execute(
        select(Repository).where(Repository.id == repo_id, Repository.team_id == team_id)
    )
    repo = result.scalar_one_or_none()
    if not repo:
        raise HTTPException(404, detail="Repository not found")

    # Remove webhook from GitHub
    if repo.webhook_id:
        try:
            import httpx

            async with httpx.AsyncClient() as client:
                await client.delete(
                    f"https://api.github.com/repos/{repo.full_name}/hooks/{repo.webhook_id}",
                    headers={"Authorization": f"Bearer {user.github_access_token}"},
                )
        except Exception:
            pass

    await session.delete(repo)
    await session.commit()
