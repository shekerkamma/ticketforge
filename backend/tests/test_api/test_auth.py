import asyncio
from urllib.parse import parse_qs, urlparse

from sqlalchemy import select

import app.api.auth as auth_api
from app.config import settings
from app.models.team import Team, TeamMember
from app.models.user import User
from tests.conftest import TestSessionLocal


def test_dev_login_bootstraps_local_user_and_team(client, monkeypatch):
    monkeypatch.setattr(auth_api, "async_session_factory", TestSessionLocal)

    response = client.get("/api/auth/dev-login", follow_redirects=False)

    assert response.status_code in (302, 307)
    location = response.headers["location"]
    parsed = urlparse(location)
    token = parse_qs(parsed.query).get("token")
    assert parsed.path == "/auth/callback"
    assert token and token[0]

    async def verify_state():
        async with TestSessionLocal() as session:
            users = (await session.execute(select(User))).scalars().all()
            teams = (await session.execute(select(Team))).scalars().all()
            memberships = (await session.execute(select(TeamMember))).scalars().all()
            return users, teams, memberships

    users, teams, memberships = asyncio.run(verify_state())

    assert len(users) == 1
    assert users[0].github_login == settings.local_dev_github_login
    assert len(teams) == 1
    assert teams[0].name == settings.local_dev_team_name
    assert len(memberships) == 1
    assert memberships[0].role == "owner"
    assert memberships[0].user_id == users[0].id
    assert memberships[0].team_id == teams[0].id
