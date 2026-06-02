---
name: ai-analyst
description: Codex-native analytics entrypoint for business questions, metrics, trends, forecasting, and stakeholder-ready analysis. Use when the user asks a quantitative question or wants data explored, validated, and turned into findings or a deck.
---

# AI Analyst

This is the Codex-native entrypoint for analytics work. Use it when a request is
fundamentally about data, metrics, trends, comparisons, forecasting, or business
opportunity sizing.

Read these references first:
- `references/workspace-layout.md`
- `references/analysis-levels.md`

Companion skills:
- `ask-question` for first-pass routing
- `setup` and `connect-data` for onboarding
- `run-analysis` for a full pipeline
- `analytics-to-comms`, `chart-storyteller`, and `research-analysis-deck` for
  packaging findings

## Workflow

1. Treat the user question as a business decision question, not just a query request.
2. Confirm or infer the active dataset, source files, or data connection.
3. Route to the lightest sufficient path:
   - direct metric answer
   - exploratory analysis
   - validated investigation
   - full deck-producing pipeline
4. Keep a durable run trail under the workspace when the analysis is non-trivial.
5. End with findings, caveats, and specific next actions.

## Rules

- Prefer `ask-question` as the first analytical step for ambiguous requests.
- Use `run-analysis` when the user wants a multi-step investigation, charts, or a deck.
- Use `research-analysis-deck` when the work needs explicit JSON handoffs into a
  presentation workflow.
- Never present a number without its timeframe, grain, and caveats.
