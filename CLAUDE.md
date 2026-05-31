# TicketForge — Project Instructions

## What this is
TicketForge: multi-agent AI pipeline that turns GitHub issues into merged PRs. FastAPI backend, Next.js 14 frontend, SQLite for local dev, PostgreSQL for prod.

## Local dev setup
```bash
# Backend
cd backend && pip install -e . --break-system-packages && uvicorn app.main:app --port 8000

# Frontend
cd frontend && npm install && npm run dev
```

## Auth for local testing
- Use `GET /api/auth/dev-login` to bypass GitHub OAuth — mints a JWT for the first user in the DB
- Frontend shows a "Dev Login (skip OAuth)" button when `NEXT_PUBLIC_API_URL` is not set
- JWT secret in `.env` is `dev-secret-change-in-production`
- Test data must be seeded into `ticketforge.db` (SQLite) — see seed script pattern in session handoff

## Key architecture decisions
- SQLAlchemy `Uuid` type stores UUIDs as 32-char hex (no dashes) in SQLite
- CORS allows only `http://localhost:3000` (frontend origin)
- All API routes under `/api/` or `/api/v1/`
- Auth via JWT in `Authorization: Bearer` header, decoded in `app/api/deps.py`
- Rate limiting: 60 req/min via slowapi

## Code conventions
- Backend: FastAPI routers in `app/api/`, models in `app/models/`, services in `app/services/`
- Frontend: Next.js app router, pages in `src/app/`, shared utils in `src/lib/`
- API client: `src/lib/api.ts` — all requests go through `apiFetch()` which handles auth
- No test framework configured yet for frontend (Jest/Vitest TBD)

## Agents
TicketForge's AI pipeline agents (Content Researcher, CodeAct, Code Reviewer) are defined in `backend/app/services/` as Python services.

## Don't do
- Don't modify `.env` files without asking — they contain secrets
- Don't add `aiosqlite` or `asyncpg` import guards — the db.py module handles SQLite/Postgres switching via URL scheme
- Don't use `regex=` in FastAPI Query params — deprecated, use `pattern=` instead
