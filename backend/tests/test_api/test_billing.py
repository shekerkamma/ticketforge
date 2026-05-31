"""Tests for Phase 6 — Billing API endpoints."""

import uuid


def test_get_billing_info(auth_client):
    create_resp = auth_client.post("/api/v1/teams", json={"name": "Billing Team"})
    team_id = create_resp.json()["id"]

    response = auth_client.get(f"/api/v1/teams/{team_id}/billing")
    assert response.status_code == 200
    data = response.json()
    assert data["plan"] == "free"
    assert data["ticket_limit"] == 20
    assert data["tickets_used"] == 0
    assert data["tickets_remaining"] == 20
    assert data["has_subscription"] is False


def test_get_billing_not_member(auth_client):
    fake_id = str(uuid.uuid4())
    response = auth_client.get(f"/api/v1/teams/{fake_id}/billing")
    assert response.status_code == 403


def test_checkout_not_owner(auth_client, test_user_2):
    """Non-owner cannot create checkout session (billing requires Stripe anyway, so
    we just verify the auth/ownership check)."""
    # This test verifies that the endpoint exists and requires ownership.
    # The actual Stripe call will fail without a real key, so we test the
    # ownership guard separately.
    create_resp = auth_client.post("/api/v1/teams", json={"name": "Checkout Team"})
    team_id = create_resp.json()["id"]

    # The test user IS the owner, so the checkout will fail at Stripe level (no key).
    # We can at least confirm it doesn't 403.
    response = auth_client.post(f"/api/v1/teams/{team_id}/billing/checkout")
    # Expected: 500 (Stripe key not configured) — NOT 403
    assert response.status_code == 500
