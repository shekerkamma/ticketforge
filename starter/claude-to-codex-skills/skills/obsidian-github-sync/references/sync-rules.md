# Sync Rules

Use this reference when `obsidian-github-sync` is active.

## Safe defaults to track

- `*.md`
- template files
- `_index/` MOCs and indexes
- selected `.obsidian/` config files when they help share the vault structure

## Defaults to ignore

- `.obsidian/workspace.json`
- `.obsidian/workspaces.json`
- `.obsidian/cache/`
- `.obsidian/plugins/*/data.json`
- OS trash or editor swap files

## GitHub storage guidance

- Prefer one repo per vault or one repo per major knowledge domain.
- Use SSH remotes when available.
- Keep commit messages descriptive enough to make note history useful.
- For private notes, prefer private GitHub repos.
- If the vault contains large attachments, separate them intentionally or use Git LFS.
