import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_team_admin
from app.db import get_session
from app.models.repository import Repository
from app.models.team import Team, TeamMember
from app.models.user import User

router = APIRouter(prefix="/api/v1/teams", tags=["teams"])


class CreateTeamRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)


@router.get("")
async def list_teams(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(Team, TeamMember.role)
        .join(TeamMember, TeamMember.team_id == Team.id)
        .where(TeamMember.user_id == user.id)
    )
    teams: list[dict[str, str | int | None]] = []
    for team, role in result.all():
        count_result = await session.execute(
            select(func.count()).select_from(TeamMember).where(TeamMember.team_id == team.id)
        )
        member_count = count_result.scalar() or 0
        teams.append(
            {
                "id": str(team.id),
                "name": team.name,
                "plan": team.plan,
                "role": role,
                "member_count": member_count,
            }
        )
    return {"teams": teams}


@router.post("", status_code=201)
async def create_team(
    body: CreateTeamRequest,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    team = Team(name=body.name, owner_id=user.id)
    session.add(team)
    await session.flush()

    member = TeamMember(team_id=team.id, user_id=user.id, role="owner")
    session.add(member)
    await session.commit()
    await session.refresh(team)

    return {
        "id": str(team.id),
        "name": team.name,
        "plan": team.plan,
        "owner_id": str(team.owner_id),
    }


@router.get("/{team_id}")
async def get_team(
    team_id: uuid.UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    # Verify membership
    membership_result = await session.execute(
        select(TeamMember).where(TeamMember.team_id == team_id, TeamMember.user_id == user.id)
    )
    if not membership_result.scalar_one_or_none():
        raise HTTPException(403, detail="Not a member of this team")

    team_result = await session.execute(select(Team).where(Team.id == team_id))
    team = team_result.scalar_one_or_none()
    if not team:
        raise HTTPException(404, detail="Team not found")

    # Get members
    result = await session.execute(
        select(User.github_login, User.avatar_url, TeamMember.role)
        .join(TeamMember, TeamMember.user_id == User.id)
        .where(TeamMember.team_id == team_id)
    )
    members = [
        {"github_login": login, "avatar_url": avatar, "role": role}
        for login, avatar, role in result.all()
    ]

    repository_result = await session.execute(
        select(Repository).where(Repository.team_id == team_id)
    )
    repos = [
        {
            "id": str(r.id),
            "full_name": r.full_name,
            "is_active": r.is_active,
            "trigger_labels": r.trigger_labels,
        }
        for r in repository_result.scalars().all()
    ]

    return {
        "id": str(team.id),
        "name": team.name,
        "plan": team.plan,
        "owner_id": str(team.owner_id),
        "members": members,
        "repositories": repos,
    }


class AddMemberRequest(BaseModel):
    github_username: str = Field(min_length=1, max_length=39)
    role: str = Field(default="member", pattern="^(member|admin)$")


class UpdateMemberRequest(BaseModel):
    role: str = Field(pattern="^(member|admin)$")


@router.post("/{team_id}/members", status_code=201)
async def add_member(
    team_id: uuid.UUID,
    body: AddMemberRequest,
    _admin: TeamMember = Depends(require_team_admin),
    session: AsyncSession = Depends(get_session),
):
    # Find user by GitHub username
    result = await session.execute(
        select(User).where(User.github_login == body.github_username)
    )
    target_user = result.scalar_one_or_none()
    if not target_user:
        raise HTTPException(404, detail="User not found. They must sign in first.")

    # Check if already a member
    result = await session.execute(
        select(TeamMember).where(
            TeamMember.team_id == team_id, TeamMember.user_id == target_user.id
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(409, detail="User is already a team member")

    member = TeamMember(team_id=team_id, user_id=target_user.id, role=body.role)
    session.add(member)
    await session.commit()

    return {
        "github_login": target_user.github_login,
        "avatar_url": target_user.avatar_url,
        "role": member.role,
    }


@router.patch("/{team_id}/members/{user_id}")
async def update_member_role(
    team_id: uuid.UUID,
    user_id: uuid.UUID,
    body: UpdateMemberRequest,
    _admin: TeamMember = Depends(require_team_admin),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(TeamMember).where(
            TeamMember.team_id == team_id, TeamMember.user_id == user_id
        )
    )
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(404, detail="Member not found")

    if member.role == "owner":
        raise HTTPException(400, detail="Cannot change owner role")

    member.role = body.role
    await session.commit()

    return {"user_id": str(user_id), "role": member.role}


@router.delete("/{team_id}/members/{user_id}", status_code=204)
async def remove_member(
    team_id: uuid.UUID,
    user_id: uuid.UUID,
    _admin: TeamMember = Depends(require_team_admin),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(TeamMember).where(
            TeamMember.team_id == team_id, TeamMember.user_id == user_id
        )
    )
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(404, detail="Member not found")

    if member.role == "owner":
        raise HTTPException(400, detail="Cannot remove team owner")

    await session.delete(member)
    await session.commit()
