---
name: presales-deal-prep
description: Prepare for a prospect or client meeting with research, positioning, contract risk review, and objection handling. Use when the user wants presales prep, meeting prep, pitch prep, or deal prep for a prospect.
---

# Presales Deal Prep

This is a Codex-native chain skill for enterprise deal preparation.

## Companion skills

- `content-research`
- `ai-strategy-brief`
- `contract-reviewer`
- `difficult-conversation-prep`
- `presentation`

## Workflow

1. Capture the prospect, meeting context, and your offering.
2. Build an account brief with `content-research`.
3. Turn that into a vertical-aware positioning memo with `ai-strategy-brief`.
4. If a contract or terms document exists, run `contract-reviewer`.
5. Build objection handling and conversation scripts with `difficult-conversation-prep`.
6. If needed, package the pitch angle into slides through `presentation`.

## Outputs

- `presales/<slug>-account-brief.md`
- `presales/<slug>-positioning-brief.md`
- `presales/<slug>-contract-review.md` when relevant
- `presales/<slug>-meeting-prep.md`
- optional slide outline or deck draft

## Required cheat sheet

Always produce a compact one-page summary with:

- 3 key facts about the prospect
- your positioning angle
- top 3 objections and responses
- recommended opening line

## Rules

- Prefer concrete company signals over generic vertical boilerplate.
- Keep legal review separate from sales positioning.
- If no contract exists, say that explicitly instead of implying it was checked.
