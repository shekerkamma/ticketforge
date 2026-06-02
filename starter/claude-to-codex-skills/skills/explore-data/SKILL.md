---
name: explore-data
description: Explore the active dataset to understand tables, fields, date coverage, grain, and obvious analytical starting points. Use before deeper analysis when the data shape is not yet clear.
---

# Explore Data

## Workflow

1. Inventory the available files or tables.
2. Summarize:
   - likely fact tables
   - likely dimensions
   - event timestamps
   - join keys
   - grain and freshness
3. Create a compact exploration note in the current run directory.
4. Surface obvious blockers such as missing dates, no user keys, or sparse metrics.
5. Recommend the next skill:
   - `deep-profile`
   - `define-metric`
   - `data-quality-check`
   - `run-analysis`
