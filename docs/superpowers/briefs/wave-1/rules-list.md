---
screen: /rules
title: Detection Rules List
role: LP | ADM
wave: W1
origin: O
cp_equivalent: "None — Counterpoint has no alert rule system"
---

# Detection Rules List

**URL:** `/rules`  
**Primary role:** LP; secondary: ADM  
**Entry points:** Primary sidebar nav (Surveillance section); alert detail → rule name link

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Detection Rules", rule count (enabled/total) | "14 of 24 rules enabled" format |
| Filter bar | Rule family (11 families), Status (enabled/disabled), Search by name | Filters apply instantly |
| Main content | Table of all detection rules | One row per rule |

## Key Elements

### Rules Table
Columns: Rule Name (e.g., "Q-DC-01 Drawer Cash Variance"), Rule Family (11 families: Drawer, Discount, Void, Comp, Return, Item, Customer, Transfer, Labor, Receiving, B2B), Description (one-line), Enabled/Disabled toggle (inline — state change is audited), Alert Count (30 days — number of alerts this rule generated), Last Fired (relative timestamp), Allow-List dependency indicator (icon if this rule has associated allow-list entries).

Rows are sorted by Alert Count descending by default — hottest rules first. LP investigators want to know which rules are active vs silent.

**Empty state (search):** "No rules match '[search term]'."

**Zero alert count:** Rules with 0 alerts in 30 days show a "Silent" badge (grey). Not a problem — may indicate good operational practice or a store that hasn't yet triggered that pattern. LP should investigate if a rule was expected to be firing.

### Enable/Disable Toggle
Inline toggle — click to change state. Confirmation required: "Disable this rule? This will stop generating alerts for [rule name]. Reason required." Reason is logged to `/admin/audit`. Enabled state is green; disabled is grey.

### Alert Count Column
Links to `/alerts?rule=[rule_id]` — one click from the rules list to see every alert this rule has generated, pre-filtered.

## Interaction Flows

1. **Audit active rules:** LP opens rules list → scans enabled/disabled states → confirms rules appropriate for their tenant's operations are enabled → flags any rule that should be enabled but isn't
2. **Identify high-volume rules:** LP sorts by Alert Count → identifies Q-DR-01 generated 143 alerts this month → investigates whether the threshold is too tight or the behavior is genuinely anomalous → adjusts allow-list or escalates to ADM to adjust thresholds
3. **Disable for training period:** LP is onboarding new cashiers this week → selects Q-VO-01 Void Detection → clicks disable → enters reason "New cashier training week, 2026-05-05 through 2026-05-09" → rule disabled → monitoring resumes automatically on end date (if end-date support exists) or re-enabled manually

## UX Callout

Alert count per rule — shown inline, sorted by default — is the key design decision that makes this screen operationally useful rather than administrative. LP investigators need to see which rules are "hot" before they start working alerts. In CP, there are no rules and no alert system; LP teams rely entirely on manual Crystal Reports review and institutional knowledge about what to look for. Canary's rule list makes the entire detection logic surface visible and auditable, with alert volume as the primary organizing signal.

## Navigation Exits

- `/rules/:id` — rule detail for any row
- `/alerts` (filtered) — alert count column links to filtered alert list
- `/settings/allowlist/*` — from allow-list dependency indicator

## Open Questions

None.
