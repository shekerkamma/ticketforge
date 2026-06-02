# AGENTS.md

## Skills

### Available skills

- `watch`: Watch a video from YouTube, Vimeo, TikTok, X, or a local file by extracting frames and transcript evidence. Use when the user asks to analyze a video, summarize a YouTube link, inspect a screen recording, or answer questions about what happens in a video. Skill file: `/home/shekerk/snap/codex/34/skills/watch/SKILL.md`

### How to use

- If the user explicitly says `watch` or asks to analyze a video URL, use the `watch` skill.
- Read only the minimum needed from the skill file, then follow its workflow.
- Prefer the vendored scripts already referenced by the skill instead of rewriting the workflow manually.
