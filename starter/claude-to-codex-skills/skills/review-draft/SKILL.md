---
name: review-draft
description: Review a draft against an established brand voice or recent writing patterns, score the fit, identify what is off, and provide a corrected version when needed. Use when the user asks whether a draft sounds like them, wants a voice review, or needs cleanup before publishing.
---

# Review Draft

This is the voice-editor layer for generated content.

## Workflow

1. Load the best available voice reference:
   - existing voice profile
   - recent strong examples
   - user-supplied sample posts
2. Review the draft for:
   - banned or overused words
   - generic AI structures
   - weak hooks
   - tone mismatch
   - format mismatch for the channel
3. Return:
   - a blunt score
   - what is off
   - a clean rewrite if the draft needs one
4. If recurring voice patterns show up across multiple reviews, suggest `tune-voice`.

## Output structure

- `Voice Score: X/5`
- short honest assessment
- grouped issues with fixes
- full clean version when needed

## Rules

- Prioritize voice fidelity over superficial polish.
- Do not soften clear problems.
- Preserve the core argument while fixing the delivery.
- Skip the rewrite only if the draft is already strong enough to publish.
