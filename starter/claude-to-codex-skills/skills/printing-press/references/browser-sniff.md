# Browser Sniff

Load this only when generation requires temporary live-site discovery.

## Principle

Browser capture is a generation-time discovery aid. It is not a runtime transport model for the shipped CLI.

## What browser sniffing is for

- discovering hidden endpoints
- learning request shapes
- capturing persisted GraphQL queries
- understanding auth/header construction
- proving whether replayable HTTP or structured extraction is possible

## Rules

- Prefer replayable HTTP or structured extraction as the final CLI surface.
- If only live page-context execution works, hold or reduce scope instead of pretending the CLI is normal.
- Treat browser discovery as a temporary step and keep the artifacts out of published outputs unless sanitized.
