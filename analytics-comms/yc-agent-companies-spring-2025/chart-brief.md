# Chart Brief

## Use-case density by cluster

- Best chart type: Horizontal bar chart
- Why this fits: The question is ranking and comparison across use-case clusters.
- Narrative takeaway: Workflow automation and customer-facing ops dominate the cohort.
- Encoding guidance: Sort clusters descending by company count and label each bar directly.
- Annotation plan: Call out the top two clusters and note that healthcare is smaller but strategically important.

## Team-size distribution

- Best chart type: Histogram or binned bar chart
- Why this fits: The question is distribution, not ranking.
- Narrative takeaway: The cohort is extremely early, with a strong concentration at 1-2 person teams.
- Encoding guidance: Use bins for 1-2, 3-4, 5-6, 7-8, 9-10 based on sizes [1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 5, 5, 6, 6, 7, 7, 7, 8, 8].
- Annotation plan: Highlight the median team size and the share of teams with 1-2 people.

## Use-case map by business shape

- Best chart type: 2x2 matrix
- Why this fits: The question is strategic positioning, not exact counts.
- Narrative takeaway: The strongest names cluster where workflow ownership and willingness to pay are both high.
- Encoding guidance: Axes: horizontal = horizontal tooling to vertical workflow ownership; vertical = weak to strong willingness to pay.
- Annotation plan: Place healthcare ops high/right, tooling/infra left/high, generic agent apps lower/left.
