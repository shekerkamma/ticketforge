# CLAUDE.md / AGENTS.md Audit — ticketforge — 2026-07-12

Auditor: `/claude-md-auditor` (first live run). Verdict: **both files had
drifted from the repo — 4 contradictions/dead instructions, 4 gaps, 1
altitude problem.** Status: **rewrite APPLIED 2026-07-12 (user-approved)** —
CLAUDE.md rewritten, AGENTS.md regenerated via its script after fixing the
snap path inside `scripts/sync_agents_skill_index.py`. Verified: `make dev`
dry-runs, backend pytest collects 42 tests with the documented env vars,
vitest executes. Correction to finding 4: the generator's count of 103 was
right (one staged dir has no SKILL.md); the raw `ls` count of 104 was the
imprecise number.

## Step 0 — Guardrails

- No contract-pinned prose: no test references CLAUDE.md/AGENTS.md.
- Mirror set: CLAUDE.md (53L, hand-written) and AGENTS.md (144L, **generated**
  by `scripts/sync_agents_skill_index.py`). Not mirrors — AGENTS.md fixes go
  through the generator, never by hand-editing.

## Contradictions & dead instructions

1. **CLAUDE.md L32** — "No test framework configured yet for frontend
   (Jest/Vitest TBD)". Reality: `frontend/package.json` has `"test": "vitest run"`.
2. **CLAUDE.md L35** — "pipeline agents … defined in `backend/app/services/`".
   Reality: they live in `backend/app/agents/` (`code_act_agent.py`,
   `code_reviewer.py`, `content_researcher.py`, `pr_creator.py`,
   `escalation.py`); `services/` holds `claude_service.py`.
3. **AGENTS.md L8** — install target `~/snap/codex/34/skills`. Snap revision
   34 no longer exists (current: 64/66). Should be `~/snap/codex/current/skills`.
4. **AGENTS.md L9** — "staged skill count: 103". Actual: **104**. The
   generator hasn't been re-run since the last skill was added (its own Notes
   section says to re-run it).

## Gaps (rules followed in practice, never written)

5. **How to run backend tests.** `backend/tests/` has 5 suites + conftest,
   but CLAUDE.md never mentions pytest. Tribal rule recovered from session
   history (permission grants):
   `ENCRYPTION_KEY="test-encryption-key-32-chars!!" DATABASE_URL="sqlite+aiosqlite://" JWT_SECRET="test-secret" python3 -m pytest tests/test_api/ -v --tb=short`
   — the required env vars exist nowhere on the page.
6. **Makefile ignored.** 10+ targets (`bootstrap`, `dev`, `smoke-test`,
   `github-check`, `demo-data`, …) duplicate/supersede the raw commands
   CLAUDE.md gives; a cheaper model should be told which entry point wins.
7. **Docker unmentioned.** `docker-compose.yml` + `docker-compose.prod.yml`
   exist; CLAUDE.md describes only bare-process dev.
8. **Dual repo identity unstated.** This repo is (a) the TicketForge product
   and (b) a deck/analytics workspace (`analytics-comms/`, `yc-companies/`,
   `url-dossiers/`, `scripts/build_*.py`, the 104-skill `starter/` pack).
   Neither file routes "which kind of work uses which rules".

## Bloat / wrong altitude

9. **CLAUDE.md L42–53 (Reports & decks)** is skill-shaped content — builder
   scripts, palette, python-pptx pitfalls — now packaged into the
   `industry-research-analysis-branded-deck` skill (commits `b682982`,
   `54e91bc`). Keep a 3-line pointer; move the rest into the skill.

## Recommended rewrite shape (on approval)

What the repo is (both identities) → commands table (Makefile-first, test
env vars verbatim) → architecture facts (corrected agent paths) → don'ts →
3-line deck pointer. AGENTS.md: fix via
`python3 scripts/sync_agents_skill_index.py` after correcting the install
target, never by hand.

Cadence: re-audit after the next skill-pack sync or major backend refactor.
