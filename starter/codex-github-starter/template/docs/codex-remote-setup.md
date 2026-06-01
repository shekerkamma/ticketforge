# Codex Remote Setup

This repo is set up for a GitHub-first Codex workflow.

## Goal

Run the repo in a cloud/container workspace so the machine doing the work is not your laptop.

For this repo, the direct path is GitHub Codespaces or any equivalent devcontainer host.

## 1. Open the repo in a cloud container

This repo includes:

- `.devcontainer/devcontainer.json`

That container installs:

- Python 3.12
- Node 20
- Codex CLI via `scripts/install_codex_cli.sh`

## 2. Start Codex inside the remote workspace

From the repo root:

```bash
codex
```

At that point, Codex is operating against the remote workspace rather than your laptop.

## 3. Use the repo as the source of truth

Keep the working loop simple:

```bash
git pull origin main
git checkout -b feat/short-description
codex
```

When the task is done:

```bash
git status
git add -A
git commit -m "feat: short description"
git push -u origin feat/short-description
```

## 4. Keep one master session

If you open multiple Codex sessions:

- keep one as the master session
- use it for product context and merge decisions
- use side sessions for narrower tasks

## 5. Start with plan-first prompts

Use prompts like:

```text
Read the repo first. Explain the affected files, constraints, and risks. Propose a minimal plan before editing.
```

## 6. Why this solves the laptop problem

With this setup:

- GitHub stores the code and branch history
- the cloud container holds the live workspace
- Codex runs against that remote workspace

Your laptop becomes a client, not the machine that owns the work.
