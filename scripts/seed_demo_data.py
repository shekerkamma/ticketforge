#!/usr/bin/env python3
import argparse
import json
import sqlite3
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sqlite_timestamp(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(tzinfo=None).strftime("%Y-%m-%d %H:%M:%S.%f")


def demo_repositories(owner: str) -> list[dict[str, object]]:
    return [
        {
            "id": uuid.uuid4().hex,
            "github_repo_id": 910000001,
            "full_name": f"{owner}/ticketforge",
            "trigger_labels": ["bug", "demo"],
            "is_active": 1,
        },
        {
            "id": uuid.uuid4().hex,
            "github_repo_id": 910000002,
            "full_name": f"{owner}/checkout-service",
            "trigger_labels": ["bug", "payments"],
            "is_active": 0,
        },
    ]


def demo_tickets(repo_ids: list[str]) -> list[dict[str, object]]:
    now = utc_now()
    return [
        {
            "id": uuid.uuid4().hex,
            "repository_id": repo_ids[0],
            "github_issue_number": 184,
            "title": "Webhook signature verification fails on Stripe replay events",
            "body": "Replay events are rejected in production even with a valid secret.",
            "labels": ["bug", "payments"],
            "priority": 1,
            "status": "pr_created",
            "created_at": now - timedelta(hours=5),
        },
        {
            "id": uuid.uuid4().hex,
            "repository_id": repo_ids[0],
            "github_issue_number": 187,
            "title": "Agent retries stall after Docker image warmup timeout",
            "body": "Pipeline pauses for several minutes before a retry starts.",
            "labels": ["bug", "infra"],
            "priority": 2,
            "status": "reviewing",
            "created_at": now - timedelta(hours=11),
        },
        {
            "id": uuid.uuid4().hex,
            "repository_id": repo_ids[0],
            "github_issue_number": 189,
            "title": "OAuth callback drops the team context after first login",
            "body": "New users arrive in the dashboard but cannot connect repositories.",
            "labels": ["bug", "auth"],
            "priority": 1,
            "status": "analyzing",
            "created_at": now - timedelta(days=1, hours=2),
        },
        {
            "id": uuid.uuid4().hex,
            "repository_id": repo_ids[0],
            "github_issue_number": 192,
            "title": "Billing settings page throws 500 when team has no email",
            "body": "Checkout attempts fail for early test users without verified email.",
            "labels": ["bug", "billing"],
            "priority": 2,
            "status": "failed",
            "created_at": now - timedelta(days=2, hours=3),
        },
        {
            "id": uuid.uuid4().hex,
            "repository_id": repo_ids[1],
            "github_issue_number": 73,
            "title": "Refund queue processor misses idempotency key on duplicate jobs",
            "body": "Duplicate refund jobs create second outbound requests to the PSP.",
            "labels": ["bug", "payments"],
            "priority": 1,
            "status": "pr_created",
            "created_at": now - timedelta(days=4, hours=6),
        },
        {
            "id": uuid.uuid4().hex,
            "repository_id": repo_ids[1],
            "github_issue_number": 78,
            "title": "Charge status polling remains in generating after API schema drift",
            "body": "Generated fix is blocked because the upstream schema changed last week.",
            "labels": ["bug", "integrations"],
            "priority": 3,
            "status": "generating",
            "created_at": now - timedelta(days=7, hours=1),
        },
        {
            "id": uuid.uuid4().hex,
            "repository_id": repo_ids[1],
            "github_issue_number": 82,
            "title": "Ledger reconciliation edge case escalates when confidence drops",
            "body": "The issue spans accounting logic and cannot be safely auto-fixed.",
            "labels": ["bug", "accounting"],
            "priority": 2,
            "status": "escalated",
            "created_at": now - timedelta(days=10, hours=4),
        },
        {
            "id": uuid.uuid4().hex,
            "repository_id": repo_ids[0],
            "github_issue_number": 193,
            "title": "Slack escalation digest still pending while incident owner is offline",
            "body": "Waiting for product owner guidance before continuing the fix.",
            "labels": ["bug", "ops"],
            "priority": 4,
            "status": "pending",
            "created_at": now - timedelta(days=14, hours=5),
        },
    ]


def demo_runs(tickets: list[dict[str, object]]) -> list[dict[str, object]]:
    by_issue = {ticket["github_issue_number"]: ticket for ticket in tickets}
    now = utc_now()
    return [
        {
            "id": uuid.uuid4().hex,
            "ticket_id": by_issue[184]["id"],
            "status": "completed",
            "started_at": now - timedelta(hours=5, minutes=40),
            "completed_at": now - timedelta(hours=5, minutes=28),
            "duration_seconds": 732,
            "analysis": {"problem_statement": "Webhook replay events fail signature verification"},
            "review_result": {"verdict": "approved", "confidence": 0.91},
            "pr_number": 214,
            "pr_url": "https://github.com/shekerkamma/ticketforge/pull/214",
            "pr_status": "merged",
            "tokens_used": 184000,
        },
        {
            "id": uuid.uuid4().hex,
            "ticket_id": by_issue[187]["id"],
            "status": "running",
            "started_at": now - timedelta(hours=11, minutes=18),
            "completed_at": None,
            "duration_seconds": None,
            "analysis": {"problem_statement": "Retry orchestration stalls on warm image check"},
            "review_result": None,
            "pr_number": None,
            "pr_url": None,
            "pr_status": None,
            "tokens_used": 91000,
        },
        {
            "id": uuid.uuid4().hex,
            "ticket_id": by_issue[189]["id"],
            "status": "running",
            "started_at": now - timedelta(days=1, hours=2, minutes=14),
            "completed_at": None,
            "duration_seconds": None,
            "analysis": {"problem_statement": "First-time OAuth users have no team context"},
            "review_result": None,
            "pr_number": None,
            "pr_url": None,
            "pr_status": None,
            "tokens_used": 42000,
        },
        {
            "id": uuid.uuid4().hex,
            "ticket_id": by_issue[192]["id"],
            "status": "failed",
            "started_at": now - timedelta(days=2, hours=3, minutes=22),
            "completed_at": now - timedelta(days=2, hours=3, minutes=12),
            "duration_seconds": 601,
            "analysis": {"problem_statement": "Stripe checkout path fails without team email"},
            "review_result": {"verdict": "rejected", "reason": "Regression in auth redirect"},
            "pr_number": None,
            "pr_url": None,
            "pr_status": None,
            "error_message": "Test suite failed in billing checkout regression test",
            "tokens_used": 127000,
        },
        {
            "id": uuid.uuid4().hex,
            "ticket_id": by_issue[73]["id"],
            "status": "completed",
            "started_at": now - timedelta(days=4, hours=6, minutes=45),
            "completed_at": now - timedelta(days=4, hours=6, minutes=29),
            "duration_seconds": 978,
            "analysis": {"problem_statement": "Duplicate refund jobs skip idempotency guard"},
            "review_result": {"verdict": "approved", "confidence": 0.84},
            "pr_number": 88,
            "pr_url": "https://github.com/shekerkamma/checkout-service/pull/88",
            "pr_status": "open",
            "tokens_used": 152000,
        },
        {
            "id": uuid.uuid4().hex,
            "ticket_id": by_issue[78]["id"],
            "status": "running",
            "started_at": now - timedelta(days=7, hours=1, minutes=9),
            "completed_at": None,
            "duration_seconds": None,
            "analysis": {"problem_statement": "Generator blocked by schema drift in upstream API"},
            "review_result": None,
            "pr_number": None,
            "pr_url": None,
            "pr_status": None,
            "tokens_used": 118000,
        },
        {
            "id": uuid.uuid4().hex,
            "ticket_id": by_issue[82]["id"],
            "status": "escalated",
            "started_at": now - timedelta(days=10, hours=4, minutes=40),
            "completed_at": now - timedelta(days=10, hours=4, minutes=19),
            "duration_seconds": 1264,
            "analysis": {"problem_statement": "Reconciliation bug crosses service and accounting boundaries"},
            "review_result": {"verdict": "escalate", "confidence": 0.31},
            "pr_number": None,
            "pr_url": None,
            "pr_status": None,
            "escalation_reason": "Low confidence in financial correctness",
            "escalation_notes": "Need finance owner to validate expected ledger behavior.",
            "tokens_used": 203000,
        },
        {
            "id": uuid.uuid4().hex,
            "ticket_id": by_issue[193]["id"],
            "status": "running",
            "started_at": now - timedelta(days=14, hours=5, minutes=12),
            "completed_at": None,
            "duration_seconds": None,
            "analysis": {"problem_statement": "Waiting on incident owner before resuming fix"},
            "review_result": None,
            "pr_number": None,
            "pr_url": None,
            "pr_status": None,
            "tokens_used": 12000,
        },
    ]


def events_for_run(run: dict[str, object]) -> list[dict[str, object]]:
    started_at = run["started_at"]
    assert isinstance(started_at, datetime)
    status = run["status"]
    issue_events = [
        ("content-researcher", "observation", {"observation": "Parsed issue body and narrowed affected files"}),
        ("code-act", "action", {"action_type": "generated_fix_plan", "files": ["backend/app/api/auth.py"]}),
    ]

    if status == "completed":
        issue_events.extend(
            [
                ("code-reviewer", "decision", {"decision": "approved", "confidence": 0.88}),
                ("pr-creator", "action", {"action_type": "opened_pull_request", "pr_number": run["pr_number"]}),
            ]
        )
    elif status == "escalated":
        issue_events.extend(
            [
                ("code-reviewer", "decision", {"decision": "escalate", "confidence": 0.31}),
                ("escalation-agent", "error", {"error": run["escalation_reason"]}),
            ]
        )
    elif status == "failed":
        issue_events.extend(
            [
                ("code-act", "action", {"action_type": "ran_test_suite"}),
                ("code-reviewer", "error", {"error": run["error_message"] or "Pipeline failed"}),
            ]
        )
    else:
        issue_events.extend(
            [
                ("code-act", "action", {"action_type": "executing_patch"}),
                ("code-reviewer", "observation", {"observation": "Run still in progress"}),
            ]
        )

    rows: list[dict[str, object]] = []
    for index, (agent_name, event_type, payload) in enumerate(issue_events):
        rows.append(
            {
                "id": uuid.uuid4().hex,
                "pipeline_run_id": run["id"],
                "agent_name": agent_name,
                "event_type": event_type,
                "payload": payload,
                "timestamp": started_at + timedelta(minutes=index * 2),
            }
        )
    return rows


def ensure_team(conn: sqlite3.Connection, github_login: str) -> tuple[str, str]:
    user_row = conn.execute(
        "select id from users where github_login = ?",
        (github_login,),
    ).fetchone()
    if user_row is None:
        raise SystemExit(f"User '{github_login}' not found in backend/ticketforge.db. Sign in first.")

    user_id = user_row[0]
    team_row = conn.execute(
        """
        select teams.id, teams.name
        from teams
        join team_members on team_members.team_id = teams.id
        where team_members.user_id = ?
        order by teams.created_at asc
        limit 1
        """,
        (user_id,),
    ).fetchone()

    if team_row is not None:
        return team_row[0], team_row[1]

    team_id = uuid.uuid4().hex
    team_name = f"{github_login}'s Team"
    conn.execute(
        "insert into teams (id, name, owner_id, plan) values (?, ?, ?, ?)",
        (team_id, team_name, user_id, "free"),
    )
    conn.execute(
        "insert into team_members (team_id, user_id, role) values (?, ?, ?)",
        (team_id, user_id, "owner"),
    )
    return team_id, team_name


def delete_existing_demo_rows(conn: sqlite3.Connection, team_id: str) -> None:
    demo_repo_ids = [
        row[0]
        for row in conn.execute(
            """
            select id from repositories
            where team_id = ?
              and config like '%"demo_seed": true%'
            """,
            (team_id,),
        ).fetchall()
    ]
    if not demo_repo_ids:
        return

    ticket_ids: list[str] = []
    run_ids: list[str] = []
    for repo_id in demo_repo_ids:
        ticket_ids.extend(
            [row[0] for row in conn.execute("select id from tickets where repository_id = ?", (repo_id,))]
        )
    for ticket_id in ticket_ids:
        run_ids.extend(
            [row[0] for row in conn.execute("select id from pipeline_runs where ticket_id = ?", (ticket_id,))]
        )
    for run_id in run_ids:
        conn.execute("delete from events where pipeline_run_id = ?", (run_id,))
    for ticket_id in ticket_ids:
        conn.execute("delete from pipeline_runs where ticket_id = ?", (ticket_id,))
        conn.execute("delete from tickets where id = ?", (ticket_id,))
    for repo_id in demo_repo_ids:
        conn.execute("delete from repositories where id = ?", (repo_id,))


def seed_demo_data(db_path: Path, github_login: str) -> None:
    conn = sqlite3.connect(db_path, timeout=30)
    conn.execute("pragma foreign_keys = on")
    try:
        team_id, team_name = ensure_team(conn, github_login)
        delete_existing_demo_rows(conn, team_id)

        repos = demo_repositories(github_login)
        tickets = demo_tickets([repo["id"] for repo in repos])
        runs = demo_runs(tickets)
        events = [event for run in runs for event in events_for_run(run)]
        now = utc_now()

        for repo in repos:
            conn.execute(
                """
                insert into repositories
                (id, team_id, github_repo_id, full_name, webhook_id, trigger_labels, is_active, config, created_at, updated_at)
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    repo["id"],
                    team_id,
                    repo["github_repo_id"],
                    repo["full_name"],
                    None,
                    json.dumps(repo["trigger_labels"]),
                    repo["is_active"],
                    json.dumps({"demo_seed": True}),
                    sqlite_timestamp(now),
                    sqlite_timestamp(now),
                ),
            )

        for ticket in tickets:
            created_at = ticket["created_at"]
            assert isinstance(created_at, datetime)
            conn.execute(
                """
                insert into tickets
                (id, repository_id, github_issue_number, github_issue_url, title, body, labels, priority, status, created_at, updated_at)
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    ticket["id"],
                    ticket["repository_id"],
                    ticket["github_issue_number"],
                    f"https://github.com/{github_login}/issues/{ticket['github_issue_number']}",
                    ticket["title"],
                    ticket["body"],
                    json.dumps(ticket["labels"]),
                    ticket["priority"],
                    ticket["status"],
                    sqlite_timestamp(created_at),
                    sqlite_timestamp(created_at),
                ),
            )

        for run in runs:
            started_at = run["started_at"]
            assert isinstance(started_at, datetime)
            completed_at = run["completed_at"]
            conn.execute(
                """
                insert into pipeline_runs
                (id, ticket_id, status, started_at, completed_at, duration_seconds, analysis, fix_diff, review_result,
                 pr_number, pr_url, pr_status, escalation_reason, escalation_notes, tokens_used, container_id, error_message)
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run["id"],
                    run["ticket_id"],
                    run["status"],
                    sqlite_timestamp(started_at),
                    sqlite_timestamp(completed_at) if isinstance(completed_at, datetime) else None,
                    run["duration_seconds"],
                    json.dumps(run["analysis"]) if run["analysis"] is not None else None,
                    None,
                    json.dumps(run["review_result"]) if run["review_result"] is not None else None,
                    run["pr_number"],
                    run["pr_url"],
                    run["pr_status"],
                    run.get("escalation_reason"),
                    run.get("escalation_notes"),
                    run["tokens_used"],
                    None,
                    run.get("error_message"),
                ),
            )

        for event in events:
            timestamp = event["timestamp"]
            assert isinstance(timestamp, datetime)
            conn.execute(
                """
                insert into events
                (id, pipeline_run_id, agent_name, event_type, payload, timestamp)
                values (?, ?, ?, ?, ?, ?)
                """,
                (
                    event["id"],
                    event["pipeline_run_id"],
                    event["agent_name"],
                    event["event_type"],
                    json.dumps(event["payload"]),
                    sqlite_timestamp(timestamp),
                ),
            )

        conn.commit()
        print(f"Seeded demo data for team '{team_name}' ({team_id})")
        print(f"Repositories: {len(repos)}")
        print(f"Tickets: {len(tickets)}")
        print(f"Pipeline runs: {len(runs)}")
        print(f"Events: {len(events)}")
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed local SQLite demo data for TicketForge.")
    parser.add_argument(
        "--db-path",
        default="backend/ticketforge.db",
        help="Path to the local SQLite database file",
    )
    parser.add_argument(
        "--github-login",
        default="shekerkamma",
        help="GitHub login whose team should receive the demo data",
    )
    args = parser.parse_args()
    seed_demo_data(Path(args.db_path), args.github_login)


if __name__ == "__main__":
    main()
