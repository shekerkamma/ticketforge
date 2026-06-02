---
name: semantic-validation
description: Validate that the business meaning of an analysis matches the metric definitions, event semantics, and stakeholder language. Use when a technically correct query may still be conceptually wrong.
---

# Semantic Validation

## Workflow

1. Compare the claimed finding to the actual metric and event semantics.
2. Check for business-language mismatches such as:
   - signups vs activated users
   - revenue booked vs revenue recognized
   - churned accounts vs churned seats
3. Rewrite the finding if the business meaning was overstated.
