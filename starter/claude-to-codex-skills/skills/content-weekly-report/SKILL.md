---
name: content-weekly-report
description: Produce a weekly content digest that summarizes what shipped, what is blocked, what performed best, and what should be turned into content next week. Use when the user asks for a weekly content report, Friday digest, or content retrospective.
---

# Content Weekly Report

This is a Codex-native chain skill for converting raw content activity into a decision-oriented weekly digest.

## Workflow

1. Gather the week's source data:
   - published posts, essays, decks, or videos
   - drafts in progress or stuck in review
   - recent outlier research
   - queue candidates for next week
2. If the data lives in spreadsheets, markdown notes, or screenshots, normalize it first.
3. Build the report around four questions:
   - what shipped
   - what worked
   - what is stuck
   - what should happen next week
4. If the environment supports delivery into notes, email, or a vault, save it there after generating the markdown.

## Output structure

```markdown
# Content Week — <date range>

## What Shipped
...

## What Worked
...

## What Is Stuck
...

## Cadence Check
...

## Next Week
...
```

## Rules

- Do not invent wins if nothing shipped.
- Treat this as an operator report, not a morale memo.
- Keep the lead metric simple and defensible.
- If the underlying data is thin, say what is missing.
