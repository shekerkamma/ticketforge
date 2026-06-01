---
name: outreach-architect
description: Design a personalized multi-step B2B outreach sequence using account context, relationship stage, and a clear call to action. Use when the user asks for cold outreach, warm outreach, follow-up sequencing, or tailored email and LinkedIn copy for a specific prospect.
---

# Outreach Architect

This is a Codex-native chain skill for turning account intelligence into a usable outreach plan.

## Inputs

Best inputs:

- an account intelligence brief
- prospect name, role, and company
- relationship type: cold, warm, previous contact, or active deal
- any deal stage, timing, or close-date pressure

## Workflow

1. Read the account context first. If it does not exist yet, ask for the minimum facts or suggest running `account-intelligence-analyst`.
2. Classify the motion:
   - cold outreach
   - warm referral or inbound
   - re-engagement
   - active opportunity follow-up
3. Build a sequence with:
   - one primary email
   - one alternate channel touch if useful
   - follow-up steps with timing
   - no-reply handling
4. Personalize every message to one or two real signals from the account brief.
5. Run the copy through `anti-slop` before finalizing.

## Output structure

```markdown
# Outreach Plan — <Prospect> @ <Company>

## Sequence Strategy
...

## Touch 1
**Channel:** Email
**Timing:** ...
**Goal:** ...
**Copy:** ...

## Touch 2
...

## Touch 3
...

## No-Reply Handling
- ...
```

## Rules

- Keep each message short and single-purpose.
- One CTA per touch.
- Do not use generic openers that could fit any company.
- If the account context is weak, say so and lower the personalization claims.
