---
name: tracking-gaps
description: Identify missing instrumentation, broken event coverage, or schema gaps that block confident analysis. Use when the data cannot support the business question cleanly.
---

# Tracking Gaps

## Workflow

1. List the questions the current data cannot answer reliably.
2. Map each gap to:
   - missing field
   - missing event
   - inconsistent grain
   - no durable key
3. Prioritize the gaps by business impact.
4. End with a concrete instrumentation backlog.
