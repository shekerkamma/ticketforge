# TicketForge — Project Instructions

## What this repo is (two identities — route your work)

1. **TicketForge product** — multi-agent AI pipeline that turns GitHub issues
   into merged PRs. FastAPI backend, Next.js 14 frontend, SQLite local /
   PostgreSQL prod. Rules below apply here.
2. **Deck & analytics workspace** — `analytics-comms/`, `yc-companies/`,
   `url-dossiers/`, `scripts/build_*.py`, and the staged Codex skill pack in
   `starter/` (see `AGENTS.md` — generated, never hand-edit; re-run
   `python3 scripts/sync_agents_skill_index.py` after changing staged skills).

## Commands — what to run when

Prefer Makefile targets; raw commands only when a target doesn't cover it.

| Task | Command |
| --- | --- |
| First-time setup | `make bootstrap` (or `make backend-install` / `make frontend-install`) |
| Run both dev servers | `make dev` (backend `make backend` → :8000, frontend `make frontend` → :3000) |
| Backend tests | `ENCRYPTION_KEY="test-encryption-key-32-chars!!" DATABASE_URL="sqlite+aiosqlite://" JWT_SECRET="test-secret" python3 -m pytest tests/ -v --tb=short` (run from `backend/`; suites: `test_api`, `test_agents`, `test_pipeline`, `test_services`) |
| Frontend tests | `cd frontend && npm run test` (Vitest) |
| Frontend lint/build | `cd frontend && npm run lint && npm run build` |
| Smoke test | `make smoke-test` |
| Seed demo data | `make demo-data` |
| GitHub integration check | `make github-check` / `make github-bootstrap` |
| Docker (full stack) | `docker compose up` (dev) / `docker-compose.prod.yml` (prod) |

Backend tests fail without those three env vars — they are required, not
optional.

## Auth for local testing

- `GET /api/auth/dev-login` bypasses GitHub OAuth — mints a JWT for the first
  user in the DB.
- Frontend shows a "Dev Login (skip OAuth)" button when `NEXT_PUBLIC_API_URL`
  is not set.
- JWT secret in `.env` is `dev-secret-change-in-production`.
- Test data must be seeded into `ticketforge.db` (SQLite) — `make demo-data`.

## Architecture facts

- **Pipeline agents live in `backend/app/agents/`** (`content_researcher.py`,
  `code_act_agent.py`, `code_reviewer.py`, `pr_creator.py`, `escalation.py`,
  base class in `base.py`). `backend/app/services/` holds service wrappers
  (e.g. `claude_service.py`) — do not conflate the two.
- SQLAlchemy `Uuid` type stores UUIDs as 32-char hex (no dashes) in SQLite.
- CORS allows only `http://localhost:3000`.
- All API routes under `/api/` or `/api/v1/`; auth via `Authorization: Bearer`
  JWT decoded in `app/api/deps.py`; rate limiting 60 req/min via slowapi.
- Backend: routers in `app/api/`, models in `app/models/`, background work in
  `app/tasks/` + `worker.py`.
- Frontend: Next.js app router — pages `src/app/`, utils `src/lib/`; all
  requests go through `apiFetch()` in `src/lib/api.ts` (handles auth).

## Don't do

- Don't modify `.env` files without asking — they contain secrets.
- Don't add `aiosqlite`/`asyncpg` import guards — `db.py` switches
  SQLite/Postgres via URL scheme.
- Don't use `regex=` in FastAPI Query params — deprecated; use `pattern=`.
- Don't hand-edit `AGENTS.md` — regenerate it.

## Reports & decks (pointer)

Deck building is packaged as the `industry-research-analysis-branded-deck`
skill (`starter/claude-to-codex-skills/skills/industry-research-analysis-branded-deck/`)
— brand palette, Canva-adapted layouts, python-pptx pitfalls, and QA live
there. Quick QA: `python3 scripts/preview_pptx.py <pptx>`. Build artifacts
(`docs/reports/_chart_assets/`, `_preview/`, `.tools/`) are gitignored.
