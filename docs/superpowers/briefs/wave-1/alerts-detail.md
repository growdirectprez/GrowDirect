---
screen: /alerts/:id
title: Alert Detail + Acknowledge
role: LP | MGR
wave: W1
origin: O
cp_equivalent: "None"
---

# Alert Detail + Acknowledge

**URL:** `/alerts/:id`  
**Primary role:** LP; secondary: MGR  
**Entry points:** Alert list row click; email notification deep-link

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Alert severity badge, rule name, store, timestamp, status badge | Breadcrumb back to /alerts |
| Left column | Transaction card + cashier history panel | ~60% width |
| Right column | Rule context panel + customer card (if present) + allow-list check | ~40% width |
| Action bar | Disposition selector, notes field, Acknowledge, Escalate to Case buttons | Bottom of page; always visible |

## Key Elements

### Transaction Card
Full ticket context: ticket number (linked to `/transactions/:id`), line items (abbreviated — item count, total value), tender type, cashier name, terminal, date/time. The specific transaction detail that triggered the alert — not a generic summary.

### Rule Context Panel
The most important element on this screen. Three sub-fields:
- **What the rule checks:** Human-readable description. E.g., "Fires when a cashier applies discounts exceeding 20% of a transaction total within a single shift."
- **What the threshold is:** E.g., "Threshold: 20% per shift."
- **What the actual value was:** E.g., "Actual: 34.7% — cashier J. Martinez, 3:00pm–3:45pm."

The rule context panel is what makes this alert explainable to a manager. CP investigators currently work from memory of what each rule means.

### Cashier Alert History
Sparkline showing this cashier's alert frequency over the last 30 days, by rule type. Small table: rule name, alert count, last triggered. Answers "is this a one-off or a pattern?" without navigating away from the screen.

### Customer Card (conditional)
Appears only if the transaction was linked to a customer account. Shows: customer name, risk score badge, case count (linked to their cases). Quick investigator context without leaving the alert.

### Allow-List Check Panel (conditional)
Appears if the alert fired on a pattern that is partially covered by an allow-list entry (e.g., alert fired but a similar pattern is allow-listed for a different store). Shows: "Note: Similar pattern is allow-listed at [Store B] for [cashier role]. Consider updating the allow-list if this is a known legitimate pattern." — Not prescriptive; investigator decides.

### Disposition Controls
Disposition code selector: Explained (alert is legitimate but behavior is authorized) / Suspicious (alert warrants investigation but not yet a case) / Escalate (create a case now). Notes field (free text). Submit = Acknowledge button.

## Interaction Flows

1. **Acknowledge as explained:** LP reads rule context → sees the cashier was doing a manager override during a training session → selects "Explained" → adds note "Training session J. Martinez, authorized by MGR Kim" → clicks Acknowledge → alert status → Acknowledged
2. **Escalate to case:** LP reads rule context + cashier history → sees this cashier triggered the same void rule 7 times this month → clicks "Escalate to Case" → modal opens with pre-filled evidence record (this alert + its transaction) → case created at `/cases/hawk/:id`
3. **Update allow-list:** LP sees allow-list check panel showing a related pattern is allow-listed elsewhere → clicks "Update Allow-List" link → navigates to relevant `/settings/allowlist/*` screen → adds entry to suppress future alerts for this known pattern

## UX Callout

The rule context panel (what checked / what threshold / what actual value) is the single most important design element in the entire LP investigator UX. Without it, an LP investigator reads "Discount Cap Alert — Q-DR-01" and has to recall from memory what Q-DR-01 means and what the threshold is. With it, the alert explains itself. Counterpoint's LP process involves printing a Price Exceptions report, cross-referencing it with the Z-tape, and building a narrative manually. Canary's alert detail gives the investigator everything they need to make a disposition decision in under 2 minutes.

## Navigation Exits

- `/alerts` — back to alert list
- `/transactions/:id` — full transaction detail (linked from transaction card)
- `/cases/hawk/:id` — case created on escalation
- `/customers/:id` — customer profile (from customer card)
- `/settings/allowlist/*` — update allow-list from allow-list check panel
- `/rules/:id` — rule detail (linked from rule name in header)

## Open Questions

None.
