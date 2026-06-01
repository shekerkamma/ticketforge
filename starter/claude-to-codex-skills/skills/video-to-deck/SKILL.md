---
name: video-to-deck
description: Turn a video URL or local video file into a research-backed presentation package. Use when the user wants to convert a video into slides, a deck outline, a Marp deck, or a richer explainer package instead of just a transcript.
---

# Video To Deck

This is a Codex-native chain skill for going from video to presentation artifacts.

## Workflow

1. Run `watch` on the video to extract transcript, frames, and structure.
2. Use `content-research` or `url-dossier` to enrich the topic with supporting sources.
3. If the concept benefits from a visual analogy, use `explainer-graphic`.
4. Build the slide artifact:
   - `slide-deck-builder` for HTML or presentation-source output
   - `marp-deck-builder` if the user wants markdown slides
5. If the user needs rendered Marp outputs, finish with `marp-exporter`.

## Output options

- transcript summary
- research note
- explainer graphic
- slide outline
- `.marp.md` deck
- rendered HTML or PDF deck

## Rules

- Stop if the video extraction failed; do not fake the downstream deck.
- Keep the deck anchored to what the video actually argues or demonstrates.
- Separate source-backed facts from your own synthesis.
- If the user wants a narrow section only, scope the deck to that segment instead of summarizing the full video.
