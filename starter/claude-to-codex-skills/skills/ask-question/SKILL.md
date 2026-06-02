---
name: ask-question
description: Mandatory analytics entrypoint for a data question, metric request, trend readout, breakdown, or chart request. Use to classify the question, load the active data context, and route to the right analytical path.
---

# Ask Question

Read `../ai-analyst/references/workspace-layout.md` and
`../ai-analyst/references/analysis-levels.md` first.

## Workflow

1. Load the active workspace and dataset context if it exists.
2. Parse the user question into:
   - metric or outcome
   - entities or segments
   - time range
   - required output
3. Classify the request as `L1` through `L5`.
4. Route to the lightest sufficient next skill:
   - `define-metric`
   - `explore-data`
   - `compare-datasets`
   - `forecast`
   - `size-opportunity`
   - `run-analysis`
5. Write a short question brief before doing expensive work.

## Question brief

Save the brief under `working/runs/<timestamp>_<slug>/question-brief.md` with:
- the user question
- normalized analytical question
- chosen level
- metrics involved
- candidate dimensions
- known caveats
- recommended next skill

## Rules

- For `L1-L2`, proceed directly once the brief is clear.
- For `L3+`, explain the plan briefly before continuing.
- If the workspace does not exist yet, route to `setup` or `connect-data`.
- If the question is presentation-oriented, route to `run-analysis`.
