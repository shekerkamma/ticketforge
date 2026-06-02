---
name: define-metric
description: Define a metric rigorously with formula, grain, filters, numerator, denominator, caveats, and validation checks. Use when the user asks what a metric means or before calculating a metric repeatedly.
---

# Define Metric

## Workflow

1. Write a metric spec with:
   - metric name
   - business meaning
   - formula
   - grain
   - inclusion and exclusion rules
   - required tables or fields
   - known caveats
2. Save it to `.knowledge/datasets/<dataset-id>/metrics/<metric>.yaml` when appropriate.
3. Update the metric index.
4. Add one quick validation check the analyst should run before trusting the metric.
