---
name: log-performance
description: Record structured performance data for published content so future review and voice-tuning decisions are based on actual outcomes. Use when the user shares engagement metrics, wants to log a post's performance, or needs a consistent performance history for later analysis.
---

# Log Performance

This skill is the structured data-entry layer for content performance.

## Workflow

1. Capture the minimum useful fields:
   - content title or identifier
   - platform
   - publish date
   - primary metric and value
2. Capture optional but useful context:
   - format
   - hook style
   - topic
   - secondary metrics
   - notes
3. Append the entry in a consistent markdown structure.
4. If the user has enough entries for pattern analysis, recommend `tune-voice`.

## Output structure

Use a stable append-only format:

```markdown
---
**<DATE> | <PLATFORM> | <FORMAT>**

**Content:** ...
**Hook style:** ...
**Topic:** ...

**Metrics:**
- ...

**Hit expectations:** ...
**Notes:** ...
---
```

## Rules

- Consistency matters more than verbosity.
- If a field is unknown, use `—` instead of inventing it.
- Treat failed content as equally important data.
