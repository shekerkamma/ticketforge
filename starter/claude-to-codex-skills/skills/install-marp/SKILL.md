---
name: install-marp
description: Check for Node/npm and install or verify Marp CLI so markdown slide decks can be rendered to HTML, PDF, or PPTX. Use when the user asks to install Marp, set up markdown slide generation, or enable Marp exports.
---

# Install Marp

Use this skill when the user explicitly wants Marp available in the environment.

## Workflow

1. Check prerequisites:

```bash
which npm
npm --version
```

2. Check whether Marp is already available:

```bash
npx @marp-team/marp-cli --version
```

3. If missing, install it:

```bash
npm install -g @marp-team/marp-cli
```

4. Verify:

```bash
marp --version
```

## Rules

- Do not install Marp unless the user wants it or the workflow genuinely depends on it.
- Prefer user-scoped installs over root installs.
- If npm is missing, say that Node.js/npm must be installed first.
- Always verify the installed version after setup.
