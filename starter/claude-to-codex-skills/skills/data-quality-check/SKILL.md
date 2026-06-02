---
name: data-quality-check
description: Audit data quality before analysis: nulls, duplicates, freshness, key integrity, date coverage, and implausible values. Use when the user wants validation or when analysis quality is at risk.
---

# Data Quality Check

## Workflow

1. Check for:
   - missing critical fields
   - duplicate primary keys
   - invalid dates or negative counts
   - stale data
   - mismatched join keys
2. Classify findings as:
   - blocker
   - warning
   - note
3. Save a concise report in the current run directory.
4. If blockers exist, stop and explain what is unsafe to conclude.
