# TicketForge

**From GitHub Issue to merged PR via multi-agent AI pipeline.**

Label a bug, get a PR. TicketForge uses a multi-agent AI pipeline to analyze GitHub issues, generate fixes in sandboxed containers, run code review, and open pull requests — automatically.

## How it works

1. **Label an issue** — Add your trigger label (e.g. `bug`) to any GitHub issue
2. **AI analyzes** — Content Researcher agent extracts problem scope and affected files
3. **Code generated** — CodeAct agent writes and tests a fix in a sandboxed container
4. **PR created** — After code review passes, a PR appears on your repo. You just merge.

## Architecture

```
Frontend (Next.js 14)  →  Backend (FastAPI)  →  AI Pipeline
     ↓                         ↓                    ↓
  Dashboard              PostgreSQL/SQLite      Claude API
  Tickets list           GitHub OAuth           Docker Sandbox
  Analytics              Stripe Billing         Code Review Agent
  Settings               Webhook handlers       PR Creation
```

## Quick start (local dev)

Codex-specific repo workflow: [docs/codex-workflow.md](/home/shekerk/ticketforge/docs/codex-workflow.md)
Codex remote/cloud workflow: [docs/codex-remote-setup.md](/home/shekerk/ticketforge/docs/codex-remote-setup.md)
GitHub OAuth setup: [docs/github-oauth-setup.md](/home/shekerk/ticketforge/docs/github-oauth-setup.md)
Production deployment setup: [docs/DEPLOYMENT.md](/home/shekerk/ticketforge/docs/DEPLOYMENT.md)
Production checklist: [docs/production-checklist.md](/home/shekerk/ticketforge/docs/production-checklist.md)
Reusable Codex/GitHub starter: [starter/codex-github-starter/README.md](/home/shekerk/ticketforge/starter/codex-github-starter/README.md)

### Prerequisites

- Python 3.12+
- Node.js 18+
- `npm`

### One-command setup

```bash
make bootstrap
```

This installs backend dependencies, backend dev tools, and frontend dependencies.
In a Codespace or devcontainer workflow, it also installs the Codex CLI.

### One-command run

```bash
make dev
```

Local URLs:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`

### Smoke test

```bash
make smoke-test
```

### GitHub foundation check

```bash
make github-check
```

This checks the GitHub-first setup this repo expects: git repo, origin remote, git identity, `gh`, `codex`, SSH keys, and remote container support.

### GitHub repo bootstrap

```bash
make github-bootstrap
```

This uses `gh` to apply the default label set used by the Codex workflow. It requires `gh auth login`.

### Local GitHub identity

Local dev login uses the public GitHub identity `shekerkamma` by default via `backend/.env`:

```bash
LOCAL_DEV_GITHUB_LOGIN=shekerkamma
LOCAL_DEV_EMAIL=shekerkamma@users.noreply.github.com
```

This is only for `/api/auth/dev-login`. Real GitHub OAuth still requires your own `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET`.

### Backend

```bash
cd backend
python3 -m pip install -e .[dev] --break-system-packages
cp .env.example .env  # or use the existing .env
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Test it

1. Open http://localhost:3000
2. Click **"Dev Login (skip OAuth)"** to bypass GitHub auth
3. Explore: Dashboard, Tickets, Analytics, Settings

On a fresh database, `Dev Login` now bootstraps a local user and owner team automatically.

API docs: http://localhost:8000/docs

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/auth/github` | GitHub OAuth login |
| GET | `/api/auth/dev-login` | Dev login (local only) |
| GET | `/api/v1/teams` | List teams |
| POST | `/api/v1/teams` | Create team |
| GET | `/api/v1/teams/{id}` | Team detail |
| POST | `/api/v1/teams/{id}/members` | Add member |
| GET | `/api/v1/teams/{id}/repos` | List repositories |
| POST | `/api/v1/teams/{id}/repos` | Connect repository |
| GET | `/api/v1/teams/{id}/tickets` | List tickets |
| GET | `/api/v1/teams/{id}/tickets/{id}` | Ticket detail |
| POST | `/api/v1/teams/{id}/tickets/{id}/retry` | Retry failed pipeline |
| GET | `/api/v1/teams/{id}/analytics` | Analytics dashboard |
| GET | `/api/v1/teams/{id}/analytics/export` | Export CSV |
| GET | `/api/v1/teams/{id}/billing` | Billing info |
| POST | `/api/v1/teams/{id}/billing/checkout` | Stripe checkout |
| GET | `/api/v1/teams/{id}/events/stream` | SSE event stream |
| POST | `/api/webhooks/github` | GitHub webhook |
| POST | `/api/webhooks/stripe` | Stripe webhook |

## Tech stack

- **Frontend:** Next.js 14, TypeScript, Tailwind CSS
- **Backend:** FastAPI, SQLAlchemy (async), Pydantic
- **Database:** PostgreSQL (prod) / SQLite (local dev)
- **AI:** Claude API (Anthropic)
- **Payments:** Stripe
- **Auth:** GitHub OAuth + JWT
- **Sandbox:** Docker with `--network=none` isolation

## Project structure

```
backend/
  app/
    api/          # Route handlers
    models/       # SQLAlchemy models
    services/     # Business logic (Claude, Docker, encryption)
    config.py     # Pydantic settings
    db.py         # Database engine
    main.py       # FastAPI app
frontend/
  src/
    app/          # Next.js pages (dashboard, tickets, analytics, settings)
    lib/          # API client, auth helpers, SSE
docs/
  prd.md          # Product requirements
  product-roadmap.md  # 62/62 tasks complete
  gtm.md          # Go-to-market playbook
```

## License

MIT
