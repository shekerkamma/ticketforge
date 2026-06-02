---
name: connect-data
description: Connect CSV, DuckDB, Postgres, BigQuery, or Snowflake data into the AI Analyst workspace and create a durable dataset manifest plus schema notes. Use when the user wants to add, list, or switch data sources.
---

# Connect Data

Read `../ai-analyst/references/workspace-layout.md` first.

Use the example manifests in `references/connection-templates/` as starting points.

## Workflow

1. Identify the connection type:
   - local files
   - DuckDB
   - Postgres
   - BigQuery
   - Snowflake
2. Gather only non-secret connection metadata.
3. Write or update:
   - `.knowledge/datasets/<dataset-id>/manifest.yaml`
   - `.knowledge/datasets/<dataset-id>/schema.md`
   - `.knowledge/active.yaml` when switching or activating
4. Record how credentials are supplied, but never inline secrets.
5. Produce a short readiness summary: tables, files, time range, and obvious risks.

## Rules

- Prefer environment variables for credentials.
- If the user only has CSVs or Parquet files, still create a dataset manifest.
- If the schema is large, summarize top-priority tables first.
