# Codex Workflow for TicketForge

This guide adapts the GitHub workflow from Hannah Stulberg and Sidwyn Koh's "GitHub is the New Google Drive" framing to a Codex-based setup for this repo.

## 1. Treat GitHub as the source of truth

For TicketForge, the repository is the system of record for:

- product requirements in `docs/`
- backend and frontend code
- branch-based changes
- PR review and merge decisions

Do not treat a local laptop state as canonical. The repo is canonical.

## 2. Run Codex against the repo, not against loose files

Open Codex in the repository root:

```bash
cd /path/to/ticketforge
codex
```

Work from the repo root so the agent can inspect both `backend/` and `frontend/` together.

## 3. Use one master session

If you run multiple Codex sessions in parallel, keep one session as the master session.

Use the master session to:

- hold product context
- decide task boundaries
- assign branch names
- resolve conflicting approaches before merge

Use side sessions for scoped tasks such as:

- backend API changes
- frontend UI work
- test repair
- docs updates

## 4. Start with planning before edits

Use a plan-first prompt before asking Codex to change code.

Example:

```text
Read the repo first. Explain the affected files, constraints, and risks. Propose a minimal implementation plan. Do not edit code until the plan is explicit.
```

This is the easiest way to avoid vague edits across `backend/`, `frontend/`, and `docs/`.

## 5. Follow the daily GitHub rhythm

This repo should follow the same pull -> branch -> edit -> test -> commit -> push -> PR flow described in the article.

### Recommended loop

```bash
git pull origin main
git checkout -b feat/short-description
codex
```

After Codex finishes:

```bash
git status
git add .
git commit -m "feat: short description"
git push -u origin feat/short-description
```

Then open a PR in GitHub.

## 6. Install and run the repo locally

The current repo README uses direct local installs.

### Backend

```bash
cd backend
python3 -m pip install -e . --break-system-packages
python3 -m pip install aiosqlite --break-system-packages
cp .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Full stack with containers

```bash
docker compose up --build
```

## 7. Prompts that fit this repo

### Bug fix

```text
Read the relevant backend and frontend files first. Identify the failing behavior, propose the smallest fix, add or update tests, and summarize the risk before editing.
```

### Feature work

```text
Inspect the existing patterns in this repo. Match the current architecture. Keep the implementation minimal, verify with tests where available, and list any follow-up work separately.
```

### Review mode

```text
Review this branch like a strict code reviewer. Prioritize bugs, regressions, missing tests, and operational risks. Findings first.
```

## 8. Practical constraints in this environment

- `codex` is installed (`codex-cli 0.114.0`)
- `git` is installed
- `gh` is installed (`gh 2.45.0`)
- `node` and `npm` are installed (`node v18.20.8`)

That means Codex can work on the repo immediately, and both GitHub CLI workflows and frontend local setup are available without extra installation.
