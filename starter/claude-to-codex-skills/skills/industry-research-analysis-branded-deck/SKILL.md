---
name: industry-research-analysis-branded-deck
description: Build an industry- and customer-aware research-to-strategy-to-branded-PPTX chain using explicit JSON handoffs, bundled Canva-style template assets, and a PowerPoint-native renderer. Use when the user wants an executive deck for a vertical, domain, industry, named customer/account, buyer segment, workflow family, or use-case landscape and the result must address business executives with both strategic implications and concrete use cases.
---

# Industry Research Analysis Branded Deck

This is the generic chain for `industry research -> customer framing -> strategy -> structured analysis -> branded PowerPoint`.

Use it when the request is about a specific industry, ICP, buyer group, or named customer and the final answer must become a real branded `.pptx`.

## Companion skills

- `content-research`
- `account-intelligence-analyst`
- `ai-strategy-researcher`
- `ai-strategy-brief`
- `ai-strategy-council`
- `analytics-to-comms`
- `chart-storyteller`
- `precall-briefer`
- `presales-deal-prep`
- `stakeholder-comms`
- `vertical-scorer`
- `research-analysis-deck`
- `presentation-content-writer`

## Required contract

This skill assumes the chain artifacts already exist for a slug:

- `research-notes/<slug>/source-notes.json`
- `analytics-comms/<slug>/analysis-pack.json`
- `analytics-comms/<slug>/deck-plan.json`

Optional but recommended executive-framing contracts:

- `analytics-comms/<slug>/strategy-brief.json`
- `analytics-comms/<slug>/executive-angle.json`
- `analytics-comms/<slug>/customer-brief.json`
- `analytics-comms/<slug>/use-case-priorities.json`

If legacy markdown notes also exist, treat them as human-readable companions, not as the primary machine-readable handoff.

## Use the bundled script

- `scripts/render_deck.py --slug <slug>`

That script:

1. validates the contract files
2. uses a custom industry builder if one exists
3. otherwise uses the generic branded deck builder
4. runs PPTX visual QA previews and writes a QA summary
5. can optionally copy the deck to Windows Downloads

## Template system

Before building or reviewing slides, load:

- `references/industry-customer-executive-frame.md`
- `references/presentation-template.md`

Treat the template system as part of this skill, not as a side note.

The concrete references are:

- PowerPoint reference deck: `assets/Prasad_Agentic_AI_Use_Cases_Across_Industries.pptx`
- Visual reference PDF: `assets/slide deck-reference.pdf`
- Repo layout reference: `scripts/build_yc_usecase_deck.py`

For use-case-heavy sections, prefer the Canva-adapted use-case layout from `build_yc_usecase_deck.py` over plain tables.

## Workflow

1. Start with `research-analysis-deck` to create or refresh the chain scaffold.
2. Run `content-research` to build source-backed notes for the industry, customer segment, or account context.
3. If a named customer, account, or buyer segment is in scope, run `account-intelligence-analyst` first and capture the commercial context in `customer-brief.md`.
4. Run `ai-strategy-researcher` when the question is market-, vertical-, customer-, or business-model-heavy.
5. Run `vertical-scorer` when the deck needs explicit lane, segment, or use-case prioritization.
6. Run `ai-strategy-brief` to produce the executive strategic takeaway in plain business language.
7. Run `ai-strategy-council` if the decision needs a pressure-tested strategic verdict rather than a single narrative.
8. Run `analytics-to-comms` and `chart-storyteller` to create the analysis pack.
9. Use `stakeholder-comms`, `precall-briefer`, or `presales-deal-prep` when the deck is meant for customer-facing executives or an account-specific meeting.
10. Fill the optional JSON contracts when the deck is customer-aware or executive-heavy:
   - `customer-brief.json`
   - `strategy-brief.json`
   - `use-case-priorities.json`
   - `executive-angle.json`
10. Expand the deck plan until the story is complete:
   - minimum target is usually `25+` slides for a serious executive deck
   - slide count should follow content density, not an arbitrary fixed number
   - split dense findings across more slides instead of shrinking text
11. Map slide families to content before rendering:
   - hero / divider / summary for story control
   - KPI / chart slides for quantitative proof
   - Canva-style use-case cards for workflow-heavy sections
   - case-study slides for named-customer or named-use-case deep dives
12. Render through this skill only after the deck plan is structurally sound and the slide family choice matches the content.
13. Review the generated QA preview bundle before calling the deck finished.

## Rules

- Do not jump from raw notes straight to slides.
- Do not skip the strategy layer for executive audiences.
- Do not use the weak generic PPTX conversion path as the default.
- Prefer a domain-specific branded builder when one exists.
- If no custom builder exists, use the generic branded deck builder from this skill.
- Use the user's Canva-style reference template as the visual system of record.
- Use the Canva-adapted use-case layout for use-case sections unless the content clearly demands a different slide family.
- Do not fall back to plain use-case tables when the slide should communicate prioritization, realization, or executive action.
- Prefer JSON contracts over ad hoc markdown for customer, strategy, prioritization, and executive-angle handoffs.
- Use real evidence, real strategic recommendations, and explicit slide-type variation.
- Every strong deck should answer all four:
  - `what is happening in the industry or market?`
  - `which customer, buyer, or workflow should we care about?`
  - `what are the highest-value use cases?`
  - `what should a business executive do about them?`

## Output

- Repo deck: `docs/reports/<slug>-branded.pptx`
- QA bundle: `docs/reports/_preview/<slug>/`
- Optional Windows copy if requested

## Reference frame

Use these references before building or reviewing the deck:

- `references/industry-customer-executive-frame.md`
- `references/presentation-template.md`

## Worked example

The current repo includes a healthcare provider operations example:

- slug: `healthcare-provider-ops-ai-usecases`
- custom builder: `scripts/build_healthcare_provider_ops_branded_pptx.py`
