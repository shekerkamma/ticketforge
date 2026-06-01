---
name: precall-briefer
description: Produce a one-page pre-call brief for a sales, success, or deal call using CRM history, recent account activity, and company changes. Use when the user asks for call prep, meeting prep, or a last-minute summary before talking to a prospect or customer.
---

# Precall Briefer

This is a Codex-native chain skill for compressing deal context into a 60-second read.

## Workflow

1. Gather:
   - meeting date and objective
   - prospect or customer participants
   - prior notes, emails, CRM history, or account brief
2. If the account context is thin, use `account-intelligence-analyst` first.
3. Extract:
   - last meaningful interaction
   - what changed since then
   - likely stakeholders and roles
   - active risks, blockers, or competing pressures
4. Produce a brief that optimizes for action during the call, not for archival completeness.

## Output structure

```markdown
# Pre-Call Brief — <Date> — <Company>

## Call Context
- ...

## Last Conversation
- ...

## What Changed Since Last Contact
- ...

## Decision-Maker Map
- ...

## Talk Track Priorities
- ...

## Risks And Blockers
- ...
```

## Rules

- Keep it to roughly one page.
- Every section should help the caller decide what to say, ask, or avoid.
- Flag missing context explicitly instead of smoothing over it.
- Separate confirmed facts from likely inferences.
