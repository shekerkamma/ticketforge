import asyncio
from urllib.parse import parse_qs, urlparse

from jose import jwt
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


def test_github_login_signs_allowed_preview_origin(client, monkeypatch):
    preview_origin = "https://ticketforge-git-main-shekerkamma-projects.vercel.app"
    monkeypatch.setattr(settings, "app_url", "https://ticketforge.example.com")
    monkeypatch.setattr(settings, "app_urls", "")
    monkeypatch.setattr(settings, "app_url_regex", r"^https://ticketforge.*\.vercel\.app$")

    response = client.get(
        "/api/auth/github",
        params={"return_to": preview_origin},
        follow_redirects=False,
    )

    assert response.status_code in (302, 307)
    parsed = urlparse(response.headers["location"])
    params = parse_qs(parsed.query)
    payload = jwt.decode(params["state"][0], settings.jwt_secret, algorithms=["HS256"])

    assert parsed.netloc == "github.com"
    assert payload["return_to"] == preview_origin
    assert params["redirect_uri"][0] == f"{settings.api_url}/api/auth/github/callback"


def test_resolve_post_auth_origin_uses_signed_state(monkeypatch):
    preview_origin = "https://ticketforge-preview.vercel.app"
    monkeypatch.setattr(settings, "app_url", "https://ticketforge.example.com")
    monkeypatch.setattr(settings, "app_urls", "")
    monkeypatch.setattr(settings, "app_url_regex", r"^https://.*\.vercel\.app$")

    state = auth_api.create_oauth_state(preview_origin)

    assert auth_api.resolve_post_auth_origin(state) == preview_origin


def test_dev_login_redirects_to_allowed_preview_origin(client, monkeypatch):
    preview_origin = "https://ticketforge-preview.vercel.app"
    monkeypatch.setattr(auth_api, "async_session_factory", TestSessionLocal)
    monkeypatch.setattr(settings, "app_url", "https://ticketforge.example.com")
    monkeypatch.setattr(settings, "app_urls", "")
    monkeypatch.setattr(settings, "app_url_regex", r"^https://.*\.vercel\.app$")

    response = client.get(
        "/api/auth/dev-login",
        params={"return_to": preview_origin},
        follow_redirects=False,
    )

    assert response.status_code in (302, 307)
    location = response.headers["location"]
    parsed = urlparse(location)
    token = parse_qs(parsed.query).get("token")

    assert parsed.scheme == "https"
    assert parsed.netloc == "ticketforge-preview.vercel.app"
    assert parsed.path == "/auth/callback"
    assert token and token[0]


def test_dev_login_rejects_untrusted_return_origin(client, monkeypatch):
    monkeypatch.setattr(auth_api, "async_session_factory", TestSessionLocal)
    monkeypatch.setattr(settings, "app_url", "https://ticketforge.example.com")
    monkeypatch.setattr(settings, "app_urls", "")
    monkeypatch.setattr(settings, "app_url_regex", "")

    response = client.get(
        "/api/auth/dev-login",
        params={"return_to": "https://evil.example.com"},
        follow_redirects=False,
    )

    assert response.status_code == 400
    assert response.json() == {
        "error": "bad_request",
        "message": "Invalid return_to origin",
    }
