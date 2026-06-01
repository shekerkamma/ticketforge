# Claude To Codex Skills

This repo now includes a staged migration path for adapting global Claude skills into Codex-compatible skills.

## What is already adapted

These skills are staged and ready to install into `~/.codex/skills`:

- `session-handoff`
- `time-skill`
- `time-tokyo`
- `weather-fetcher`
- `weather-fetcher-tokyo`
- `code-review-specialist`
- `contract-reviewer`
- `difficult-conversation-prep`
- `workflow-visualizer`
- `graphify`

The staged copies live under:

- `starter/claude-to-codex-skills/skills/`

## What still needs redesign

These categories are not safe to copy 1:1 and should be rewritten before installation:

- `autoplan`
- `gstack/*`
- skills that depend on `AskUserQuestion`
- skills that depend on `~/.claude/skills/gstack/*`
- skills that hard-code `~/.claude` session state or slash commands as part of the workflow

## Inventory your Claude skills

Run:

```bash
python3 scripts/migrate_claude_skills.py inventory
```

Output columns:

- `classification`
- `skill`
- `path`
- `reasons`

Classifications mean:

- `direct_port`: mostly portable as-is
- `light_edit`: portable after small path or tool wording fixes
- `rewrite`: should be redesigned for Codex instead of copied

## Refresh the staged starter set

Run:

```bash
python3 scripts/migrate_claude_skills.py stage
```

That rewrites the repo-managed staged skills from the current adaptation templates.

## Adapt additional Claude skills on demand

If a Claude skill inventories as `direct_port` or `light_edit`, you can stage it by name:

```bash
python3 scripts/migrate_claude_skills.py stage --skills affiliate-workflow,graphify
```

If the skill name is ambiguous, use the Claude relative path instead:

```bash
python3 scripts/migrate_claude_skills.py stage --skills ai-analyst/analysis-design-spec
```

The migrator will refuse `rewrite` skills instead of copying them blindly.

## Install the staged skills into Codex

To install every staged skill:

```bash
./starter/claude-to-codex-skills/install.sh
```

To install only selected skills:

```bash
./starter/claude-to-codex-skills/install.sh session-handoff time-skill
```

By default this installs into:

```text
$CODEX_HOME/skills
```

If `CODEX_HOME` is unset, it falls back to:

```text
~/.codex/skills
```

If you use a different Codex home:

```bash
CODEX_HOME=/path/to/codex-home ./starter/claude-to-codex-skills/install.sh
```

## Practical migration rule

- Move repo-wide behavior into `AGENTS.md` or `.codex/prompts/`.
- Port plain instruction skills directly.
- Rewrite Claude-only orchestration skills instead of copying them.
- Move deterministic shell logic into scripts when the same steps repeat.
