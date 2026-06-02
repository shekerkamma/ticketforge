---
name: setup
description: Set up or repair an AI Analyst workspace with user profile, business context, data pointers, and output preferences. Use when the user wants to onboard, configure, or reset the analytics environment.
---

# Setup

Read `../ai-analyst/references/workspace-layout.md` first.

## Workflow

1. Create the workspace layout if it does not exist.
2. Capture:
   - role and technical level
   - domain and team context
   - preferred output style
   - default metrics or KPIs
3. Write:
   - `.knowledge/user/profile.md`
   - `.knowledge/user/business-context.md`
   - `.knowledge/setup-state.yaml`
4. If no data is connected, route to `connect-data`.
5. End with suggested first analytical questions.

## Rules

- Ask only the minimum questions needed to make the environment usable.
- Keep secrets out of repo-tracked files.
- If the user already has a workspace, update it instead of recreating it.
