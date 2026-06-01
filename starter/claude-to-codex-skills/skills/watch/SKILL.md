---
name: watch
description: Watch a video from YouTube, Vimeo, TikTok, X, or a local file by extracting frames and transcript evidence. Use when the user asks to analyze a video, summarize a YouTube link, inspect a screen recording, or answer questions about what happens in a video.
---

# Watch

This is a Codex-adapted version of the open-source `watch` skill. It vendors the working Python scripts from the original project and removes the Claude-only setup flow.

## Skill directory

Use:

```bash
WATCH_SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/watch"
```

In this environment, `CODEX_HOME` should already point to the active Codex skill home.

## Workflow

1. Run silent preflight:

```bash
python3 "$WATCH_SKILL_DIR/scripts/setup.py" --check
```

2. If preflight fails, run:

```bash
python3 "$WATCH_SKILL_DIR/scripts/setup.py"
```

3. If Whisper API keys are still missing after setup, continue with `--no-whisper` unless the user explicitly wants full fallback transcription.
4. Run the watcher:

```bash
python3 "$WATCH_SKILL_DIR/scripts/watch.py" "<video-url-or-path>"
```

5. Read every frame path the report prints.
6. Use the transcript and frames together to answer the user.

## Good use cases

- summarize a YouTube video
- inspect a screen recording or bug repro video
- analyze the opening hook of a creator video
- answer timestamp-specific questions about a video

## Focus mode

When the user asks about a specific moment or range, pass `--start` and `--end` to get denser frame coverage:

```bash
python3 "$WATCH_SKILL_DIR/scripts/watch.py" "<video-url-or-path>" --start 2:15 --end 2:45
```

## Constraints

- Best results are on videos under about 10 minutes unless you focus on a specific section.
- Token cost is dominated by frames; use focus ranges for long videos.
- Native captions are preferred. Whisper fallback requires a key in the watch config.
- `agent-browser` is not required for this skill.

## Provenance

Based on the MIT-licensed `bradautomates/claude-video` project, adapted for Codex use.
