---
screen: /customers/:id → Risk tab
title: Customer Risk Score
role: LP
wave: W1
origin: O
cp_equivalent: "None"
---

# Customer Risk Score (Tab on Customer Detail)

**URL:** `/customers/:id` → Risk tab  
**Primary role:** LP  
**Entry points:** Customer detail → Risk tab; customer lookup (risk badge click)

**Note:** This tab renders within `/customers/:id`. The parent route's header (customer name, loyalty number, status badge, overall risk score) remains visible above the tab bar.

## Layout

| Zone | Content | Notes |
|---|---|---|
| Tab content top | Risk score gauge + overall score + trend | Full-width |
| Left section | Contributing factors breakdown | ~55% width |
| Right section | Score history sparkline + manual override section | ~45% width |
| Bottom section | Top contributing transactions | Full-width table |

## Key Elements

### Risk Score Gauge
Visual gauge (0–100 arc). Current score displayed prominently. Color zones: 0–30 = grey (None), 31–60 = yellow (Medium), 61–80 = orange (High), 81–100 = red (Critical). Trend arrow: ↑ (increasing), ↓ (decreasing), → (stable) based on 30-day movement.

### Contributing Factors Breakdown
Horizontal bar chart — one bar per factor:
- Return Rate Weight (0–100 score component)
- Discount Pattern Weight
- Case Involvement Weight
- Transaction Velocity Weight

Each bar shows the factor's contribution to the overall score and the raw metric: "Return Rate: 24% over last 90 days (industry avg: 8%)". Clicking a factor bar highlights its contributing transactions in the bottom table.

The decomposition (why is this score 73?) is the core value. An LP investigator cannot act on a number without being able to explain it to a manager.

### Score History Sparkline
30/60/90-day toggle. Shows score trend over time. Useful for: confirming a customer is de-escalating after a prior investigation, detecting an escalating pattern that hasn't yet triggered an alert.

### Manual Override Section
LP can override the system score with a documented reason:
- Override score (0–100 manual entry)
- Reason (required: "Known VIP customer — high return rate is preference-driven, confirmed legitimate")
- Expiry date (required — override automatically expires and system score resumes)

Manual overrides are audited (actor + timestamp + reason + expiry). Override indicator appears on the gauge when active.

### Top Contributing Transactions Table
The 5 transactions contributing most to the current score. Columns: date, type (Sale/Return), amount, store, factor (which score component this transaction affects). Rows link to `/transactions/:id`.

**Empty state:** "No transactions on file. Risk score is 0 (None)."

## Interaction Flows

1. **Explain risk score to manager:** LP investigating a flagged customer → opens Risk tab → sees score 67 (High) → reads contributing factors: Return Rate 40% (weight: 55%), Case Involvement 1 case (weight: 30%) → notes the top 3 contributing transactions → goes to manager meeting with specific transaction evidence
2. **Override VIP customer:** MGR identifies a high-value customer being flagged inappropriately (frequent returns due to bulk purchasing patterns) → LP reviews and agrees → adds manual override with reason and 90-day expiry → score shows as overridden on customer card
3. **Monitor de-escalation:** LP checks a customer who was High-risk 60 days ago → sparkline shows score trending down from 72 to 31 → LP notes the customer's behavior has normalized → case was appropriately closed

## UX Callout

The score decomposition is more valuable than the score itself. An LP investigator who sees "Risk Score: 73" without explanation cannot act on it — they can't explain to a manager why the customer is being flagged, and they can't determine whether to investigate further or apply an override. The contributing factors breakdown makes the score actionable: it gives LP the specific language to present findings, and it gives managers the data to challenge or confirm the LP assessment. No CP equivalent exists because CP has no risk scoring model at all.

## Navigation Exits

- `/customers/:id` — parent tab bar (Overview, Context tabs)
- `/transactions/:id` — from contributing transactions table

## Open Questions

None.
