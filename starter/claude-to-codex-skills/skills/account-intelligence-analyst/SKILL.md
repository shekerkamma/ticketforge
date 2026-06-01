---
name: account-intelligence-analyst
description: Build a concise B2B account and prospect intelligence brief from public sources, CRM notes, and company materials. Use when the user asks to research a prospect, build an account profile, prep for first outreach, or identify buying signals and risk flags before engaging.
---

# Account Intelligence Analyst

This is a Codex-native chain skill for turning scattered account context into a usable sales brief.

## When to use it

Use this skill when the user needs:

- a prospect intelligence profile
- account research before outreach
- buying signals and risk flags
- conversation hooks grounded in real company context

## Workflow

1. Gather the minimum useful inputs:
   - prospect name or profile URL
   - company name or domain
   - any CRM notes, prior emails, or deal context if available
2. Use `content-research` or `url-dossier` if the inputs include public URLs or source documents.
3. Extract only decision-relevant facts:
   - title, tenure, influence, likely mandate
   - company priorities, recent launches, funding, hiring, leadership changes
   - existing relationship history or stale-record signals
4. Synthesize into a single brief with:
   - company overview
   - prospect profile
   - buying signals
   - risk flags
   - conversation starters
   - open questions
5. If the user maintains durable research notes, hand the result to `second-brain-capture`.

## Output structure

```markdown
# <Prospect Name> — <Company> Intelligence Brief

## Company Overview
- ...

## Prospect Profile
- ...

## Buying Signals
- ...

## Risk Flags
- ...

## Conversation Starters
- ...

## Open Questions
- ...
```

## Rules

- Timestamp and source any non-obvious factual claims.
- Prioritize signal over completeness; a short accurate brief beats a noisy dossier.
- Separate observed facts from inferences.
- If CRM access is unavailable, say so and proceed with public-source research only.
