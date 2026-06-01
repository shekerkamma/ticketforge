---
name: agent-browser
description: Browser automation CLI for websites, forms, login flows, screenshots, scraping, and interactive web testing. Use when the user wants to open a site, click through a flow, fill a form, take browser screenshots, or automate browser actions with the `agent-browser` CLI.
---

# Agent Browser

Use the `agent-browser` CLI as the browser automation runtime.

## Preflight

First verify the CLI exists:

```bash
command -v agent-browser
```

If it is missing, say so directly and stop instead of inventing browser steps.

## Core workflow

1. Open a page:

```bash
agent-browser open <url>
```

2. Snapshot interactive elements:

```bash
agent-browser snapshot -i
```

3. Interact using refs like `@e1`, `@e2`:

```bash
agent-browser click @e1
agent-browser fill @e2 "text"
agent-browser select @e3 "option"
```

4. Re-snapshot after any navigation or DOM-changing action.

## Common commands

```bash
agent-browser open <url>
agent-browser close
agent-browser snapshot -i
agent-browser click @e1
agent-browser fill @e2 "text"
agent-browser type @e2 "text"
agent-browser select @e3 "option"
agent-browser check @e4
agent-browser press Enter
agent-browser wait --load networkidle
agent-browser wait --url "**/dashboard"
agent-browser get text @e1
agent-browser get url
agent-browser get title
agent-browser screenshot
agent-browser screenshot --full
agent-browser pdf output.pdf
```

## Stateful flows

For authenticated or repeated sessions:

```bash
agent-browser state save auth.json
agent-browser state load auth.json
```

For parallel sessions:

```bash
agent-browser --session site1 open <url>
agent-browser --session site2 open <url>
agent-browser session list
```

## Rules

- Re-snapshot after navigation, submissions, or dynamic DOM changes.
- Use the CLI's own state mechanism instead of inventing cookie storage.
- If the task depends on the user's real desktop Chrome profile, say that this skill alone is not enough.
- If the user wants visible debugging, prefer `--headed`.
