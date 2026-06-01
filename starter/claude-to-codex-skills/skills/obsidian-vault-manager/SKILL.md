---
name: obsidian-vault-manager
description: Set up or maintain an Obsidian vault for repo-backed notes, templates, MOCs, and second-brain workflows. Use when the user asks to create an Obsidian vault, organize vault folders, add templates, or make a note system Obsidian-friendly.
---

# Obsidian Vault Manager

Create or normalize a Git-friendly Obsidian vault.

Read `references/vault-layout.md` before changing the vault structure.

## Workflow

1. Detect the target vault path.
   - Prefer an explicit path.
   - Otherwise detect an existing `.obsidian/` directory.
   - If none exists, choose a repo-local folder such as `vault/`.
2. If the vault does not exist, bootstrap it with:

```bash
bash "$CODEX_HOME/skills/obsidian-vault-manager/scripts/bootstrap_vault.sh" "<vault-path>"
```

3. Ensure the core layout exists:
   - `_index/`
   - `_templates/`
   - `daily/`
   - `projects/`
   - `research/`
   - `sources/`
   - `evergreen/`
   - `attachments/`
   - `archive/`
4. Ensure starter files exist:
   - `README.md`
   - `_index/Second Brain MOC.md`
   - `_templates/source-note.md`
   - `_templates/evergreen-note.md`
   - `_templates/meeting-note.md`
5. Normalize `.gitignore` so local-only Obsidian state stays out of git.
6. If the user wants GitHub-backed storage, continue with `obsidian-github-sync`.

## Rules

- Keep the vault plain markdown first; Obsidian is a reader, not the storage format.
- Do not commit transient Obsidian workspace files unless the user explicitly wants them tracked.
- Prefer a small, predictable folder structure over plugin-heavy conventions.
- Preserve existing vault content; add structure without flattening the user's notes.
