# Connection Guide

## Local files
- Store file paths relative to the workspace when possible.
- Capture file format, row estimate, and date coverage.

## DuckDB
- Record the `.duckdb` file path.
- Note the logical schema or key tables if known.

## Postgres / BigQuery / Snowflake
- Record host, database, schema, and role metadata only.
- Reference env vars for secrets.
- Avoid writing passwords, tokens, or private keys into manifests.
