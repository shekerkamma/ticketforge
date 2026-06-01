---
name: morning-briefing
description: Produce a daily enterprise-AI briefing focused on Sheker's priorities: automotive AI, Azure, AWS Bedrock, Google Vertex AI, Anthropic, and agentic frameworks. Use when the user asks for a morning briefing, daily scan, or what matters today.
---

# Morning Briefing

Generate a focused daily signal brief, not a generic news dump.

## Priorities

Bias the scan toward:

- Anthropic and Claude updates
- Azure OpenAI, Power Platform, Copilot Studio
- AWS Bedrock and Bedrock Agents
- Google Vertex AI and ADK
- automotive AI and SAP + AI work
- agentic framework releases with real enterprise relevance

Ignore low-signal items like consumer AI apps, generic funding news, or hype with no enterprise angle.

## Workflow

1. Gather at least 6 targeted searches and collect at least 8 raw findings.
2. Score each finding for:
   - relevance to active work
   - buzz
   - timeliness
   - POC applicability
   - client impact
   - accessibility today
3. Discard weak items.
4. Build the briefing:
   - top signals
   - quick hits
   - one concrete recommendation for today

## Output structure

```markdown
# Morning Briefing — <date>

## Top 3 Signals

### 1. <title>
**Score:** <n>/22 | **Urgency:** <red/yellow/green>
**What happened:** ...
**POC / client angle:** ...
**Action:** ...

## Quick Hits
- ...

## Recommendation
...
```

## Rules

- Be opinionated.
- Frame every item through enterprise POC delivery, not abstract interest.
- If a Claude / Anthropic developer product update is materially relevant, it belongs near the top.
- If only 2 items matter, return 2. Do not pad to 3.
