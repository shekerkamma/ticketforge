---
name: content-performance-tracker
description: Refresh and summarize performance metrics for published content, then route the result into the performance log so future voice tuning has real data. Use when the user asks to update content metrics, check how posts are doing, or run a recurring performance refresh.
---

# Content Performance Tracker

This is a Codex-native chain skill for closing the loop between publishing and learning.

## Workflow

1. Gather the content items to refresh:
   - one URL
   - a recent published batch
   - a spreadsheet or note export
2. Normalize the available metrics by channel.
3. Summarize:
   - current top performer
   - biggest recent change
   - obvious missing data
4. Append clean entries through `log-performance`.
5. If enough data exists, suggest `tune-voice`.

## Output structure

```markdown
# Performance Refresh — <date>

## Updated Items
- ...

## Top Performer
- ...

## Biggest Delta
- ...

## Missing Or Failed Reads
- ...
```

## Rules

- Trends matter more than false precision.
- If metrics are partial, say exactly what is missing.
- Do not fabricate engagement numbers from weak signals.
- Keep the result structured so it can feed `log-performance`.
