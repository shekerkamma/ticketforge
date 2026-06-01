---
name: printing-press
description: Generate or improve a CLI for an API using the external `printing-press` binary. Use when the user wants a ship-ready CLI generated from an API name, spec file, HAR capture, or API docs URL.
---

# Printing Press

This is the Codex-native wrapper for the external `printing-press` binary.

Read `references/setup-checks.md` first.

## What this skill is for

Use it when the user wants to:

- generate a CLI from an API name
- generate from an OpenAPI or YAML spec
- generate from a HAR capture
- generate from a docs URL or product URL
- run the binary in its `codex` mode when supported

## Preflight

First verify the binary exists:

```bash
command -v printing-press
```

If it is missing, stop and show the install command from `references/setup-checks.md`.

## Main entry patterns

```bash
printing-press "<api>"
printing-press "<api>" codex
printing-press --spec ./openapi.yaml
printing-press --har ./capture.har --name MyAPI
printing-press https://postman.com/explore
```

## Workflow

1. Confirm the input shape:
   - API name
   - local spec file
   - HAR capture
   - URL
2. Read `references/spec-inputs.md` if the format or source is ambiguous.
3. Run the `printing-press` binary with the narrowest correct input form.
4. If the run needs temporary browser-based discovery, read `references/browser-sniff.md`.
5. Before any archive, publish, or share step, read `references/secret-protection.md`.
6. Before calling the result ship-ready, read `references/shipcheck.md`.

## Rules

- This skill wraps the binary; it does not replace it.
- Do not claim the CLI is shippable without both structural checks and behavioral testing.
- Browser sniffing is temporary discovery only, not permission to ship a resident browser runtime.
- If the user asks for second-pass cleanup and there is no dedicated polish skill installed yet, say that explicitly instead of pretending the old Claude-only polish workflow exists.
