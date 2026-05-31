"""Tests for Phase 4 — Teams API endpoints."""

import uuid


def test_create_team(auth_client):
    response = auth_client.post("/api/v1/teams", json={"name": "My Team"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "My Team"
    assert data["plan"] == "free"
    assert "id" in data


def test_create_team_empty_name_rejected(auth_client):
    response = auth_client.post("/api/v1/teams", json={"name": ""})
    assert response.status_code == 422


def test_list_teams(auth_client):
    # Create a team first
    auth_client.post("/api/v1/teams", json={"name": "Team A"})

    response = auth_client.get("/api/v1/teams")
    assert response.status_code == 200
    teams = response.json()["teams"]
    assert len(teams) >= 1
    assert teams[0]["name"] == "Team A"
    assert teams[0]["role"] == "owner"
    assert teams[0]["member_count"] == 1


def test_get_team_detail(auth_client):
    create_resp = auth_client.post("/api/v1/teams", json={"name": "Detail Team"})
    team_id = create_resp.json()["id"]

    response = auth_client.get(f"/api/v1/teams/{team_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Detail Team"
    assert len(data["members"]) == 1
    assert data["members"][0]["github_login"] == "testuser"
    assert data["members"][0]["role"] == "owner"
    assert data["repositories"] == []


def test_get_team_not_member(auth_client):
    fake_id = str(uuid.uuid4())
    response = auth_client.get(f"/api/v1/teams/{fake_id}")
    assert response.status_code == 403


def test_add_member(auth_client, test_user_2):
    create_resp = auth_client.post("/api/v1/teams", json={"name": "Member Team"})
    team_id = create_resp.json()["id"]

    response = auth_client.post(
        f"/api/v1/teams/{team_id}/members",
        json={"github_username": "testuser2", "role": "member"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["github_login"] == "testuser2"
    assert data["role"] == "member"


def test_add_member_not_found(auth_client):
    create_resp = auth_client.post("/api/v1/teams", json={"name": "No Member Team"})
    team_id = create_resp.json()["id"]

    response = auth_client.post(
        f"/api/v1/teams/{team_id}/members",
        json={"github_username": "nonexistent_user"},
    )
    assert response.status_code == 404


def test_add_member_duplicate(auth_client, test_user_2):
    create_resp = auth_client.post("/api/v1/teams", json={"name": "Dup Team"})
    team_id = create_resp.json()["id"]

    auth_client.post(
        f"/api/v1/teams/{team_id}/members",
        json={"github_username": "testuser2"},
    )
    response = auth_client.post(
        f"/api/v1/teams/{team_id}/members",
        json={"github_username": "testuser2"},
    )
    assert response.status_code == 409


def test_remove_member(auth_client, test_user_2):
    create_resp = auth_client.post("/api/v1/teams", json={"name": "Remove Team"})
    team_id = create_resp.json()["id"]

    from tests.conftest import TEST_USER_2_ID

    auth_client.post(
        f"/api/v1/teams/{team_id}/members",
        json={"github_username": "testuser2"},
    )

    response = auth_client.delete(f"/api/v1/teams/{team_id}/members/{TEST_USER_2_ID}")
    assert response.status_code == 204


def test_cannot_remove_owner(auth_client):
    create_resp = auth_client.post("/api/v1/teams", json={"name": "Owner Team"})
    team_id = create_resp.json()["id"]

    from tests.conftest import TEST_USER_ID

    response = auth_client.delete(f"/api/v1/teams/{team_id}/members/{TEST_USER_ID}")
    assert response.status_code == 400
    assert "owner" in response.json()["message"].lower()


def test_update_member_role(auth_client, test_user_2):
    create_resp = auth_client.post("/api/v1/teams", json={"name": "Role Team"})
    team_id = create_resp.json()["id"]

    from tests.conftest import TEST_USER_2_ID

    auth_client.post(
        f"/api/v1/teams/{team_id}/members",
        json={"github_username": "testuser2"},
    )

    response = auth_client.patch(
        f"/api/v1/teams/{team_id}/members/{TEST_USER_2_ID}",
        json={"role": "admin"},
    )
    assert response.status_code == 200
    assert response.json()["role"] == "admin"
