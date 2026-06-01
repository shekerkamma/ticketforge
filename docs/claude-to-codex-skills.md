# Claude To Codex Skills

This repo now includes a staged migration path for adapting global Claude skills into Codex-compatible skills.

## What is already adapted

These skills are staged and ready to install into `~/.codex/skills`:

- `account-intelligence-analyst`
- `anti-slop`
- `agent-browser`
- `architect`
- `architecture-to-everything`
- `ai-strategy-brief`
- `ai-strategy-council`
- `ai-strategy-researcher`
- `analytics-to-comms`
- `carousel-to-deck`
- `crm-hygiene-enforcer`
- `session-handoff`
- `ss`
- `time-skill`
- `time-tokyo`
- `weather-fetcher`
- `weather-fetcher-tokyo`
- `code-review-specialist`
- `content-marketing-team`
- `content-draft-writer`
- `content-outlier-research`
- `content-performance-tracker`
- `content-publish-helper`
- `content-topic-queue`
- `content-weekly-report`
- `contract-reviewer`
- `content-research`
- `competitive-intel-sprint`
- `content-repurpose`
- `difficult-conversation-prep`
- `explainer-graphic`
- `export-results`
- `install-marp`
- `llm-council`
- `log-performance`
- `markdown-preview`
- `marp-deck-builder`
- `marp-exporter`
- `morning-briefing`
- `obsidian-github-sync`
- `obsidian-vault-manager`
- `outreach-architect`
- `printing-press`
- `precall-briefer`
- `presentation`
- `presentation-accessibility`
- `presentation-content-writer`
- `presentation-exporter`
- `presentation-speaker-notes`
- `presentation-theme`
- `proposal-generator`
- `review-draft`
- `research-to-strategy`
- `second-brain-capture`
- `slide-deck-builder`
- `stakeholder-comms`
- `tune-voice`
- `url-dossier`
- `video-to-deck`
- `vertical-scorer`
- `watch`
- `workflow-visualizer`
- `presales-deal-prep`
- `chart-storyteller`
- `graphify`

The staged copies live under:

- `starter/claude-to-codex-skills/skills/`

## Codex chain skills

These skills are not blind copies of the Claude originals. They were rewritten as Codex-native chain skills:

- `agent-browser`
- `account-intelligence-analyst`
- `presentation`
- `architect`
- `architecture-to-everything`
- `content-draft-writer`
- `content-marketing-team`
- `content-outlier-research`
- `content-performance-tracker`
- `content-publish-helper`
- `content-research`
- `content-topic-queue`
- `content-weekly-report`
- `crm-hygiene-enforcer`
- `research-to-strategy`
- `url-dossier`
- `llm-council`
- `obsidian-github-sync`
- `obsidian-vault-manager`
- `outreach-architect`
- `marp-deck-builder`
- `marp-exporter`
- `printing-press`
- `precall-briefer`
- `competitive-intel-sprint`
- `analytics-to-comms`
- `ai-strategy-researcher`
- `ai-strategy-council`
- `presales-deal-prep`
- `proposal-generator`
- `content-repurpose`
- `second-brain-capture`
- `slide-deck-builder`
- `stakeholder-comms`
- `ss`
- `tune-voice`
- `video-to-deck`

The Codex pattern is:

- keep the reusable workflow in one skill
- bundle long supporting knowledge in `references/`
- use companion skills where they exist
- avoid Claude-only routing, slash commands, or `AskUserQuestion` dependencies

The strategy/communications wave follows the same rule:

- keep reusable scoring or memo skills as standalone helpers
- rewrite multi-step orchestrators as chain skills
- prefer markdown-first outputs, with optional richer export only when the environment supports it

The presales/content/chart wave extends that pattern:

- presales uses research + positioning + objection handling as one chain
- content repurposing keeps one source-of-truth note before generating variants
- chart work is treated as a narrative/encoding problem, not just a graphic choice

The second-brain / Obsidian wave follows the same rule:

- `content-research` can now hand off durable notes into a second brain instead of stopping at temporary research files
- `second-brain-capture` turns raw findings into reusable markdown notes with frontmatter and note-type conventions
- `obsidian-vault-manager` bootstraps or normalizes a Git-friendly vault structure
- `obsidian-github-sync` treats GitHub as the storage layer for the vault instead of relying on app-only sync

Recommended chain:

1. `content-research` to ingest URLs, videos, repos, or documents
2. `second-brain-capture` to turn the outputs into durable notes
3. `obsidian-vault-manager` if the notes should live in a proper vault
4. `obsidian-github-sync` if the vault should use GitHub as the source of truth
5. `graphify` if the user wants relationship or concept mapping on top

The browser / desktop-adjacent wave is narrower:

- `agent-browser` is worth keeping as a direct Codex skill because it wraps a real browser CLI
- `ss` is worth keeping as a fast screenshot-ingest workflow
- `open-gstack-browser` and `setup-browser-cookies` are not worth porting directly; they are mostly gstack runtime glue and consent/preamble machinery

The first `Claude Cowork` wave is intentionally selective:

- `anti-slop` as a durable prose-quality filter
- `carousel-to-deck` as a bridge from content assets into presentation work
- `morning-briefing` as a daily enterprise-AI scanning workflow

These are good fits because they transfer cleanly without dragging in the whole old Claude runtime model.

The `Sales Agents` wave follows the same pattern:

- `account-intelligence-analyst` for prospect and company research
- `outreach-architect` for turning that research into contact sequences
- `precall-briefer` for one-page meeting prep
- `crm-hygiene-enforcer` for pipeline and record cleanup against exported data
- `proposal-generator` for turning qualified-opportunity context into a sendable commercial draft

Recommended chain:

1. `account-intelligence-analyst`
2. `outreach-architect` or `precall-briefer`, depending on whether the next motion is outreach or a live meeting
3. `proposal-generator` once the opportunity is qualified
4. `crm-hygiene-enforcer` on a weekly cadence to keep the underlying system trustworthy

The `Claude Cowork` content pipeline wave is now covered too:

- `content-outlier-research` for pattern mining across current high-performing content
- `content-topic-queue` for turning those patterns into a ranked backlog
- `content-marketing-team` as the parent orchestrator
- `content-draft-writer` for converting one topic into a review-ready draft
- `content-publish-helper` for the human-gated publishing handoff
- `content-performance-tracker` for refreshing metrics and routing them into the log
- `content-weekly-report` for the Friday operator digest
- `slide-deck-builder` for enterprise-style visual deck generation from topics, memos, or research packs

Recommended chain:

1. `content-outlier-research`
2. `content-topic-queue`
3. `content-marketing-team` to decide whether to research, queue, draft, publish, track, or report next
4. `content-draft-writer`
5. `review-draft` and `anti-slop` for voice and cleanup
6. `content-publish-helper`
7. `content-performance-tracker` -> `log-performance`
8. `tune-voice` once enough entries exist
9. `content-weekly-report` at the end of the week
10. `slide-deck-builder` when the same material needs presentation form

The slide / Marp / preview wave is now covered too:

- `slide-deck-builder` remains the general visual-deck path
- `marp-deck-builder` is the markdown-slide path when the user wants `.marp.md`
- `marp-exporter` lints and renders Marp decks with vendored helpers and bundled themes
- `install-marp` handles environment setup for real Marp exports
- `markdown-preview` gives a quick local HTML preview for ordinary markdown and `.marp.md`
- `video-to-deck` chains `watch` + research + deck generation for video-driven presentation workflows

Recommended chain:

1. `video-to-deck` if the source material is a video
2. `slide-deck-builder` for general presentation work
3. `stakeholder-comms` when the same findings need different audience framing
4. `export-results` when the output needs to become email, Slack, brief, or slides
5. `marp-deck-builder` when the user wants markdown-native slide source
6. `marp-exporter` for lint + HTML/PDF output
7. `markdown-preview` for quick local review of markdown or deck source

The `printing-press` migration is intentionally lean:

- keep a Codex wrapper around the real `printing-press` binary
- preserve only the high-value references: setup checks, spec inputs, browser sniffing, secret protection, and shipcheck
- do not copy the full Claude-only orchestration prompt 1:1

For diagrams, the existing installed pack is already the recommended layer:

- `workflow-visualizer`
- `explainer-graphic`
- `graphify`
- `architecture-to-everything`

## What still needs redesign

These categories are not safe to copy 1:1 and should be rewritten before installation:

- `autoplan`
- `gstack/*`
- skills that depend on `AskUserQuestion`
- skills that depend on `~/.claude/skills/gstack/*`
- skills that hard-code `~/.claude` session state or slash commands as part of the workflow

Still not ported from the strategy side:

- Slack/Notion/browser-posting style wrappers that assume external integrations are already installed
- the old Obsidian plugin wrapper under `gstack/obsidian-command-center`, which is still too Claude/gstack-specific to copy 1:1
- the old `printing-press-polish` follow-on workflow, which should be rebuilt separately if needed

## Tracked External Corpora

The main external Claude corpus currently tracked is:

- Windows path: `D:\AppliedAICourse\Claude Cowork`
- WSL path: `/mnt/d/AppliedAICourse/Claude Cowork`

This corpus currently contains:

- `22` real `SKILL.md` files
- `11` under `ClaudeOS/skills`
- `5` under `Sales Agents`
- `6` `.skill` wrappers

The highest-value clusters there are:

- `ClaudeOS/skills/*`
- `Sales Agents/*`
- standalone skills such as `anti-slop`, `carousel-to-deck`, `llm-council`, `log-performance`, `review-draft`, and `tune-voice`

## Inventory your Claude skills

Run:

```bash
python3 scripts/migrate_claude_skills.py inventory
```

To include an additional workspace-specific Claude corpus, such as a Claude Cowork or ClaudeOS folder:

```bash
python3 scripts/migrate_claude_skills.py inventory \
  --source-root "/mnt/d/AppliedAICourse/Claude Cowork"
```

You can also set extra roots through:

```bash
CLAUDE_SKILL_SOURCE_ROOTS="/mnt/d/AppliedAICourse/Claude Cowork"
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

If the skill lives in an additional source root, use the displayed namespaced path:

```bash
python3 scripts/migrate_claude_skills.py stage \
  --source-root "/mnt/d/AppliedAICourse/Claude Cowork" \
  --skills "Claude Cowork::ClaudeOS/skills/morning-briefing"
```

The migrator will refuse `rewrite` skills instead of copying them blindly.

For the chain-oriented skills listed above, the repo-managed templates take precedence over the original Claude wrappers.

## Video and URL skills

Two additions are especially useful for link-heavy workflows:

- `watch`: adapted from the open-source `bradautomates/claude-video` project, with the Python scripts vendored into the staged skill and patched for Codex home-path behavior
- `url-dossier`: a Codex-native "analyze this link" chain skill that routes video URLs to `watch`, GitHub URLs to `gh` plus file inspection, and generic URLs to web access or `curl`

`watch` still depends on local binaries:

- `ffmpeg`
- `ffprobe`
- `yt-dlp`

The vendored `setup.py` preflight checks these and uses:

```bash
python3 "$WATCH_SKILL_DIR/scripts/setup.py" --check
```

Its config now resolves to:

```text
~/.config/watch/.env
```

instead of the Snap-local home path.

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
