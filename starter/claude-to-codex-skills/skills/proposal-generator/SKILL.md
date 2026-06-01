---
name: proposal-generator
description: Generate a tailored B2B proposal, quote, or statement of work from deal context, discovery notes, and pricing inputs. Use when the user asks for a proposal, quote, SOW, commercial document, or deal-ready summary for a qualified opportunity.
---

# Proposal Generator

This is a Codex-native chain skill for going from deal context to a sendable proposal draft.

## Inputs

Gather as many of these as exist:

- prospect and company name
- deal stage and target timeline
- discovery notes or call transcripts
- pricing or rate-card inputs
- requested scope, deliverables, or commercial constraints

## Workflow

1. Read the deal context and extract:
   - desired outcomes
   - pain points in the prospect's own language
   - scope and assumptions
   - pricing constraints or discount approvals
2. Structure the draft in this order:
   - executive summary
   - current situation and challenge
   - proposed solution
   - scope of work
   - investment
   - commercial terms
   - next steps
3. Keep the narrative specific to the deal; do not produce brochure copy.
4. If terms need extra scrutiny, route the draft through `contract-reviewer`.
5. If the user needs a slide version, route the core proposal story into `presentation`.

## Output structure

```markdown
# Proposal — <Company>

## Executive Summary
...

## Situation And Challenge
...

## Proposed Solution
...

## Scope Of Work
...

## Investment
...

## Terms
...

## Next Steps
...
```

## Rules

- Document assumptions clearly.
- Keep scope boundaries explicit to prevent scope creep.
- Separate base scope from optional add-ons.
- If the environment cannot export PDF or branded documents, say so and produce the clean source draft.
