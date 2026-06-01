---
name: obsidian-github-sync
description: Use GitHub as durable storage for an Obsidian vault or markdown-based second brain. Use when the user asks to sync Obsidian with GitHub, keep notes in a repo, or treat GitHub as the storage layer for their vault.
---

# Obsidian GitHub Sync

Use Git and GitHub as the storage and sync layer for a vault or second-brain directory.

Read `references/sync-rules.md` before configuring the repo.

## Workflow

1. Identify the vault or notes root.
2. If the target is not already a git repo, initialize it with:

```bash
bash "$CODEX_HOME/skills/obsidian-github-sync/scripts/setup_repo_sync.sh" "<vault-path>" "<optional-remote-url>"
```

3. Verify:
   - current branch
   - remote configuration
   - `.gitignore` safety rules
4. If the user wants a GitHub repo created and `gh` is available, create or connect the remote.
5. Use the sync helper when the user wants a snapshot commit:

```bash
bash "$CODEX_HOME/skills/obsidian-github-sync/scripts/sync_vault.sh" "<vault-path>" "vault snapshot"
```

## Recommended operating model

- one main branch unless the user needs more complex collaboration
- pull before editing on a different machine
- commit after meaningful note changes, not every keystroke
- push frequently enough that GitHub stays the source of truth

## Rules

- Never store secrets, tokens, or transient browser state in the vault repo.
- Keep note storage text-first; use Git LFS only if the user knowingly wants large binaries.
- Ignore Obsidian workspace and plugin-local state by default.
- If a user wants fully automatic sync, explain the tradeoff before wiring a scheduled commit/push flow.
