---
name: crm-hygiene-enforcer
description: Audit CRM exports or pipeline snapshots for stale deals, missing fields, duplicates, stage mismatches, and reporting risk. Use when the user asks to clean CRM data, audit pipeline quality, review imports, or produce a prioritized data hygiene queue.
---

# CRM Hygiene Enforcer

This is a Codex-native chain skill for turning messy CRM exports into an action queue.

## When to use it

Use this skill for:

- weekly CRM hygiene reviews
- post-import audits
- forecast cleanup
- duplicate and stale-deal detection

## Inputs

Typical inputs:

- CSV exports from CRM
- spreadsheets
- snapshots of account, contact, and opportunity tables
- funnel rules or stage definitions

## Workflow

1. Confirm the scope:
   - contacts
   - accounts
   - opportunities
   - activities
2. Identify the rules that matter:
   - stale thresholds
   - required fields
   - valid stage transitions
   - duplicate tolerance
3. Audit the data for:
   - stale records
   - missing owners or critical fields
   - impossible close dates or amounts
   - stage mismatches
   - likely duplicates
4. Separate:
   - safe auto-fix suggestions
   - items requiring human review
5. Produce a ranked hygiene report with explicit owners and recommended actions.

## Output structure

```markdown
# CRM Hygiene Audit — <date>

## Summary
- ...

## Critical Issues
- ...

## Stale Deals
- ...

## Missing Data
- ...

## Duplicate Candidates
- ...

## Manual Action Queue
- ...
```

## Rules

- Be conservative about auto-corrections; prefer recommendations over silent edits.
- Explain the rule behind each flagged issue.
- Treat the output as an operations queue, not a generic report.
- If the user only provides narrative descriptions instead of data exports, offer the audit logic and required columns.
