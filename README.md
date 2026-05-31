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

### Prerequisites

- Python 3.12+
- Node.js 18+
- pip

### Backend

```bash
cd backend
pip install -e . --break-system-packages
pip install aiosqlite --break-system-packages
cp .env.example .env  # or use the existing .env
uvicorn app.main:app --host 0.0.0.0 --port 8000
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
