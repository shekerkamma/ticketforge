from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse
from jose import JWTError, jwt
from sqlalchemy import select

from app.config import normalize_origin, settings
from app.db import async_session_factory
from app.models.team import Team, TeamMember
from app.models.user import User

router = APIRouter(prefix="/api/auth", tags=["auth"])

GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"


def create_jwt(user_id: str, github_login: str) -> str:
    payload = {
        "user_id": user_id,
        "github_login": github_login,
        "exp": datetime.now(timezone.utc) + timedelta(hours=settings.jwt_expiry_hours),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def create_oauth_state(return_to: str) -> str:
    payload = {
        "return_to": return_to,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=10),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def resolve_return_to_origin(return_to: str | None) -> str:
    if return_to is None:
        return settings.app_url

    normalized = normalize_origin(return_to)
    if normalized is None or not settings.is_allowed_app_origin(normalized):
        raise HTTPException(400, detail="Invalid return_to origin")

    return normalized


def resolve_post_auth_origin(state: str | None) -> str:
    if state is None:
        return settings.app_url

    try:
        payload = jwt.decode(state, settings.jwt_secret, algorithms=["HS256"])
    except JWTError as exc:
        raise HTTPException(400, detail="Invalid OAuth state") from exc

    return_to = payload.get("return_to")
    if not isinstance(return_to, str):
        raise HTTPException(400, detail="Invalid OAuth state")

    return resolve_return_to_origin(return_to)


async def ensure_local_dev_user(session) -> User:
    result = await session.execute(select(User).limit(1))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            github_id=settings.local_dev_github_id,
            github_login=settings.local_dev_github_login,
            github_access_token="local-dev-token",
            email=settings.local_dev_email,
        )
        session.add(user)
        await session.flush()

    membership_result = await session.execute(
        select(TeamMember).where(TeamMember.user_id == user.id).limit(1)
    )
    membership = membership_result.scalar_one_or_none()

    if membership is None:
        team = Team(name=settings.local_dev_team_name, owner_id=user.id)
        session.add(team)
        await session.flush()
        session.add(TeamMember(team_id=team.id, user_id=user.id, role="owner"))

    await session.commit()
    await session.refresh(user)
    return user


@router.get("/github")
async def github_login(return_to: str | None = Query(default=None)):
    redirect_origin = resolve_return_to_origin(return_to)
    params = {
        "client_id": settings.github_client_id,
        "redirect_uri": f"{settings.api_url}/api/auth/github/callback",
        "scope": "repo read:user",
        "state": create_oauth_state(redirect_origin),
    }
    return RedirectResponse(url=f"{GITHUB_AUTHORIZE_URL}?{urlencode(params)}")


@router.get("/github/callback")
async def github_callback(
    code: str = Query(...),
    state: str | None = Query(default=None),
):
    redirect_origin = resolve_post_auth_origin(state)

    async with httpx.AsyncClient() as client:
        # Exchange code for access token
        token_response = await client.post(
            GITHUB_TOKEN_URL,
            json={
                "client_id": settings.github_client_id,
                "client_secret": settings.github_client_secret,
                "code": code,
            },
            headers={"Accept": "application/json"},
        )
        token_data = token_response.json()

        if "access_token" not in token_data:
            raise HTTPException(400, detail="Invalid code")

        access_token = token_data["access_token"]

        # Fetch user info
        user_response = await client.get(
            GITHUB_USER_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_data = user_response.json()

    # Create or update user
    async with async_session_factory() as session:
        result = await session.execute(
            select(User).where(User.github_id == user_data["id"])
        )
        user = result.scalar_one_or_none()

        if user:
            user.github_login = user_data["login"]
            user.github_access_token = access_token
            user.avatar_url = user_data.get("avatar_url")
            user.email = user_data.get("email")
        else:
            user = User(
                github_id=user_data["id"],
                github_login=user_data["login"],
                github_access_token=access_token,
                avatar_url=user_data.get("avatar_url"),
                email=user_data.get("email"),
            )
            session.add(user)

        await session.commit()
        await session.refresh(user)

        token = create_jwt(str(user.id), user.github_login)

    return RedirectResponse(url=f"{redirect_origin}/auth/callback?token={token}")


@router.get("/dev-login")
async def dev_login(return_to: str | None = Query(default=None)):
    """Local dev only — bypass GitHub OAuth with a minimal local user/team bootstrap."""
    redirect_origin = resolve_return_to_origin(return_to)
    async with async_session_factory() as session:
        user = await ensure_local_dev_user(session)

    token = create_jwt(str(user.id), user.github_login)
    return RedirectResponse(url=f"{redirect_origin}/auth/callback?token={token}")


@router.post("/refresh")
async def refresh_token():
    # Placeholder — will be wired up with auth dependency in TASK-010
    raise HTTPException(501, detail="Not implemented yet")
