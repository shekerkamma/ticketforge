# Planning Methodology

Use this when the `architect` skill is active.

## Phase 0: Scope and personas

- Define the brief, constraints, examples, and success criteria.
- Pick 3-5 personas with distinct concerns.
- Good persona mix:
  - End-user advocate
  - Technical architect
  - Domain specialist
  - Growth or business strategist
  - Ops or delivery engineer

## Phase 1: Independent plans

Each persona should cover:

1. What needs to be built
2. How it should be structured
3. Proposed waves or phases
4. Dependencies
5. Risks and unknowns
6. What they would push back on

## Phase 2: Debate summary

The moderator should extract:

- Agreements
- Conflicts
- Gaps
- Resolutions with reasoning
- Open questions

## Phase 3: Revised plans

Each persona revises their plan using the debate summary.

## Phase 4: Synthesis

The master plan should include:

1. Executive summary
2. Wave structure table
3. Detailed waves and task specs
4. Dependency graph
5. Files changed summary
6. Open questions

## BUILD_STATUS.yaml

Recommended fields:

```yaml
project: example-project
master_plan: ./EXAMPLE_MASTER_PLAN.md
current_wave: 0
total_waves: 4
tasks:
  - id: W0.1
    wave: 0
    description: Example task
    status: not_started
    depends_on: []
    output_files: []
```

## Practical rules

- Never run parallel builders against the same output file.
- Prefer explicit task IDs and dependencies over vague checklists.
- Keep the tracker current if work continues across sessions.
