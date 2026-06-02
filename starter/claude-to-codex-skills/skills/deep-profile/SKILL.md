---
name: deep-profile
description: Run a deeper profile of selected tables or files: distributions, nulls, cardinality, date coverage, and suspicious columns. Use when the user wants a serious read on data quality or table readiness.
---

# Deep Profile

## Workflow

1. Select the priority tables or files for profiling.
2. For each, record:
   - row estimate
   - primary or candidate key
   - null rates
   - distinct counts
   - min/max dates
   - suspicious free-text or JSON columns
3. Save the result to `working/runs/<timestamp>_<slug>/deep-profile.md`.
4. Highlight anything that blocks trustworthy analysis.
