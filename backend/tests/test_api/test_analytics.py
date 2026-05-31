"""Tests for Phase 5 — Analytics API endpoints."""

import uuid

from tests.conftest import TEST_USER_ID, TestSessionLocal
from app.models.repository import Repository
from app.models.team import Team, TeamMember


def _seed_team_with_repo(auth_client):
    """Helper: create team via API, then seed a repo directly in DB."""
    import asyncio

    create_resp = auth_client.post("/api/v1/teams", json={"name": "Analytics Team"})
    team_id = uuid.UUID(create_resp.json()["id"])

    repo_id = uuid.uuid4()

    async def _seed():
        async with TestSessionLocal() as session:
            repo = Repository(
                id=repo_id,
                team_id=team_id,
                github_repo_id=99999,
                full_name="org/analytics-repo",
                trigger_labels=["bug"],
            )
            session.add(repo)
            await session.commit()

    asyncio.get_event_loop().run_until_complete(_seed())
    return team_id, repo_id


def test_get_analytics_empty(auth_client):
    create_resp = auth_client.post("/api/v1/teams", json={"name": "Empty Analytics"})
    team_id = create_resp.json()["id"]

    response = auth_client.get(f"/api/v1/teams/{team_id}/analytics")
    assert response.status_code == 200
    data = response.json()
    assert data["tickets_processed"] == 0
    assert data["prs_created"] == 0
    assert data["period"] == "30d"


def test_get_analytics_with_period(auth_client):
    create_resp = auth_client.post("/api/v1/teams", json={"name": "Period Team"})
    team_id = create_resp.json()["id"]

    response = auth_client.get(f"/api/v1/teams/{team_id}/analytics?period=7d")
    assert response.status_code == 200
    assert response.json()["period"] == "7d"


def test_get_analytics_not_member(auth_client):
    fake_id = str(uuid.uuid4())
    response = auth_client.get(f"/api/v1/teams/{fake_id}/analytics")
    assert response.status_code == 403


def test_export_analytics_json_empty(auth_client):
    create_resp = auth_client.post("/api/v1/teams", json={"name": "Export JSON Team"})
    team_id = create_resp.json()["id"]

    response = auth_client.get(
        f"/api/v1/teams/{team_id}/analytics/export?format=json"
    )
    assert response.status_code == 200
    assert response.json()["tickets"] == []


def test_export_analytics_csv_empty(auth_client):
    create_resp = auth_client.post("/api/v1/teams", json={"name": "Export CSV Team"})
    team_id = create_resp.json()["id"]

    response = auth_client.get(
        f"/api/v1/teams/{team_id}/analytics/export?format=csv"
    )
    assert response.status_code == 200
    assert "text/csv" in response.headers.get("content-type", "")
