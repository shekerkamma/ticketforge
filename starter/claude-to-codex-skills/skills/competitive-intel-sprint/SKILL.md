---
name: competitive-intel-sprint
description: Build a structured competitive intelligence package from a competitor name, video, site, or source bundle. Use when the user wants competitive analysis, a threat assessment, or an executive brief on what a competitor is doing.
---

# Competitive Intel Sprint

This is a Codex-native chain skill for competitive analysis.

## Companion skills

- `watch`
- `content-research`
- `ai-strategy-researcher`
- `vertical-scorer`
- `ai-strategy-brief`
- `presentation`

## Workflow

1. Capture the competitor name, source material, and the comparison lens.
2. If there is a demo or presentation video, run `watch`.
3. Build structured source notes with `content-research`.
4. Add broader market context with `ai-strategy-researcher`.
5. Score the opportunity or threat with `vertical-scorer`.
6. Turn the result into an executive brief with `ai-strategy-brief`.
7. If requested, package the findings into slides through `presentation`.

## Outputs

- `competitive-intel/<slug>-research.md`
- `competitive-intel/<slug>-market-context.md`
- `competitive-intel/<slug>-scorecard.md`
- `competitive-intel/<slug>-brief.md`
- optional deck outline or slide files

## Deliverable requirements

Always include:

- threat level
- 3 actionable takeaways
- win/loss matrix
- recommended next move

## Rules

- Distinguish between observed product facts, inferred GTM strategy, and speculation.
- Quote exact claims when they come from videos or marketing material.
- Treat absence of evidence as uncertainty, not a negative signal.
