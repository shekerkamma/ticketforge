"""Tests for Phase 5 — Dashboard API endpoints (retry pipeline)."""

import asyncio
import uuid

from tests.conftest import TEST_USER_ID, TestSessionLocal
from app.models.repository import Repository
from app.models.ticket import Ticket


def _seed_ticket(auth_client, status="escalated"):
    """Create a team and seed a ticket with given status."""
    create_resp = auth_client.post("/api/v1/teams", json={"name": "Dashboard Team"})
    team_id = uuid.UUID(create_resp.json()["id"])

    repo_id = uuid.uuid4()
    ticket_id = uuid.uuid4()

    async def _seed():
        async with TestSessionLocal() as session:
            repo = Repository(
                id=repo_id,
                team_id=team_id,
                github_repo_id=11111,
                full_name="org/dash-repo",
            )
            session.add(repo)
            await session.flush()

            ticket = Ticket(
                id=ticket_id,
                repository_id=repo_id,
                github_issue_number=42,
                github_issue_url="https://github.com/org/dash-repo/issues/42",
                title="Test bug",
                status=status,
            )
            session.add(ticket)
            await session.commit()

    asyncio.get_event_loop().run_until_complete(_seed())
    return str(team_id), str(ticket_id)


def test_retry_escalated_ticket(auth_client):
    team_id, ticket_id = _seed_ticket(auth_client, status="escalated")

    response = auth_client.post(f"/api/v1/teams/{team_id}/tickets/{ticket_id}/retry")
    assert response.status_code == 200
    data = response.json()
    assert data["ticket_id"] == ticket_id
    assert data["status"] == "running"
    assert "pipeline_run_id" in data


def test_retry_failed_ticket(auth_client):
    team_id, ticket_id = _seed_ticket(auth_client, status="failed")

    response = auth_client.post(f"/api/v1/teams/{team_id}/tickets/{ticket_id}/retry")
    assert response.status_code == 200


def test_retry_pending_ticket_rejected(auth_client):
    team_id, ticket_id = _seed_ticket(auth_client, status="pending")

    response = auth_client.post(f"/api/v1/teams/{team_id}/tickets/{ticket_id}/retry")
    assert response.status_code == 400
    assert "Cannot retry" in response.json()["message"]


def test_retry_nonexistent_ticket(auth_client):
    create_resp = auth_client.post("/api/v1/teams", json={"name": "Retry Team"})
    team_id = create_resp.json()["id"]
    fake_ticket = str(uuid.uuid4())

    response = auth_client.post(f"/api/v1/teams/{team_id}/tickets/{fake_ticket}/retry")
    assert response.status_code == 404
