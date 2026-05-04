---
screen: /cases/hawk/patterns
title: Cross-Case Pattern View
role: LP
wave: W1
origin: O
cp_equivalent: "None"
---

# Cross-Case Pattern View

**URL:** `/cases/hawk/patterns`  
**Primary role:** LP  
**Entry points:** Case detail → "View subject patterns"; Investigations nav → Patterns tab

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Patterns", time range selector, minimum case count threshold slider | Threshold: show subjects with ≥ N cases (default: 2) |
| Top section | Subject graph — network visualization | Visual anchor for pattern detection |
| Left column | Subject table | ~50% width |
| Right column | Temporal heatmap | ~50% width |

## Key Elements

### Subject Graph
Force-directed node graph. Nodes: subjects (cashiers, customers, terminals). Node size proportional to case count. Edges: open cases linking two or more subjects (e.g., a cashier and a customer who appear in the same cases). Edge thickness proportional to case count linking them.

Color: Cashier nodes = blue, Customer nodes = orange, Terminal nodes = grey. Red border on any node with > 3 open cases.

Clicking a node opens a details panel: subject name, type, case list (linked). Clicking an edge opens a details panel: which cases connect these two subjects.

**Empty state:** "No subjects appear in more than [threshold] cases. Lower the minimum case count to see more subjects, or check back as cases accumulate."

The graph is not intended for daily use — it surfaces when LP has an active pattern worth visualizing. It becomes valuable at ~20+ cases.

### Subject Table
Columns: Subject Name, Type (Cashier / Customer / Terminal), Case Count, Total Amount (sum of evidence amounts across their cases), Stores (which stores their cases span), Last Case Opened. Sorted by Case Count descending.

**"Coordinated Scheme" flag action:** LP selects 2+ related subjects → clicks "Flag as Coordinated Scheme" → creates a linking record that associates the cases and labels the pattern as coordinated. This flag is visible on each involved case's detail page.

### Temporal Heatmap
Calendar heatmap (week × hour-of-day grid, 30-day window). Cell color intensity = alert density for that hour/weekday combination. Reveals: "Most alerts fire on Friday afternoons between 3–6pm." Operational pattern for staffing LP coverage.

## Interaction Flows

1. **Identify repeat subject:** LP opens patterns → sorts subject table by Case Count → sees Cashier J. Martinez in 4 open cases → threshold node is large and red in the graph → LP clicks Martinez node → case list opens → reviews all 4 cases to determine if they're coordinated
2. **Detect collusion:** LP notices in the graph that Cashier A and Customer B are connected by 3 cases → both were present in the same transactions → LP flags as coordinated scheme → adds note to each involved case
3. **Optimize LP coverage:** LP checks temporal heatmap → sees Friday 4–5pm is the highest-alert hour → recommends to MGR that LP coverage shift starts Thursday evening and covers Friday afternoon

## UX Callout

The needle-in-a-haystack problem in LP is that individual alerts don't reveal coordinated behavior — only the aggregate pattern does. Counterpoint operators discover multi-case patterns only by manually reviewing paper Z-tapes across multiple days and building a narrative from memory. Canary's pattern view does the cross-case aggregation automatically and surfaces it visually. A cashier with 4 cases in 60 days across 2 stores is invisible at the individual alert level; this screen makes it the first thing LP sees.

## Navigation Exits

- `/cases/hawk/:id` — any case from subject node detail panel or table row
- `/cases/hawk/analytics` — back to analytics overview

## Open Questions

None.
