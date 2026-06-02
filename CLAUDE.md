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

## Reports & decks

- YC agent-companies decks are **generated, not hand-built**, from one analysis pack: `analytics-comms/yc-agent-companies-spring-2025/analysis.json`.
- Builders in `scripts/` (run from repo root): `build_yc_deck_v2.py` (analyst deck), `build_yc_usecase_deck.py` (use-case/realization deck, Canva-adapted, org-named — exposes reusable helpers + `USE_CASES`), `build_yc_exec_deck.py` (executive briefing; imports the use-case module as a library).
- QA a deck with `python3 scripts/preview_pptx.py <pptx>` — renders PNGs + contact sheet and flags text overflow.
- Brand palette (matches the user's Canva-Pro template): navy `#0A1628`, teal `#00C9A7`, accent `#009B82`, gold `#FFB800`, font **Calibri**. The template itself lives in the `hyundai-peopletech-deck` repo, not here.
- python-pptx pitfall: never append a second `<a:effectLst>` after `shape.shadow.inherit = False` — two of them under one `spPr` make PowerPoint show the "repair" prompt. Reuse the existing `effectLst`. Validate generated decks by checking no `spPr` has >1 `effectLst`.
- Build artifacts (`docs/reports/_chart_assets/`, `_preview/`, `.tools/`) are gitignored.
