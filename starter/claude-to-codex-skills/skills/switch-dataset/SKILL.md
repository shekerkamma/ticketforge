---
name: switch-dataset
description: Change the active dataset in the analytics workspace and confirm what schema and metric context is now in scope. Use when the user wants to work on another dataset.
---

# Switch Dataset

## Workflow

1. Confirm the target dataset exists.
2. Update `.knowledge/active.yaml`.
3. Show the active dataset summary:
   - name
   - source type
   - top tables
   - key metrics if known
4. Suggest the next likely analytical step.
