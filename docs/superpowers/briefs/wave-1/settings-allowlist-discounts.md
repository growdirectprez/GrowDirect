---
screen: /settings/allowlist/discounts
title: Allow-List — Discounts
role: ADM
wave: W1
origin: O
cp_equivalent: "None"
---

# Allow-List — Discounts

**URL:** `/settings/allowlist/discounts`  
**Primary role:** ADM  
**Entry points:** Settings nav → Allow-Lists → Discounts; alert detail → "Update allow-list"

**Inherits layout and pattern from `/settings/allowlist/dead-count`.** See that brief for the full screen pattern. Delta documented here.

## Delta from Dead Count Allow-List

**Context panel:** "Discount allow-list entries pre-approve specific discount patterns that would otherwise trigger Q-DR-01 Discount Cap Detection. Use this to approve manager override reason codes, employee discount programs, or promotional discount codes that are authorized to exceed the standard discount cap."

**Rule fed:** Q-DR-01 Discount Cap Detection.

**Key field difference — entry form:**

| Field | Dead Count | Discounts |
|---|---|---|
| Threshold override | Max dead count events per shift | Max discount percentage (%) — blank = no cap |
| Scope | Cashier + Store | Reason Code + Max % + Store + Cashier + Date Range |

Discount allow-list entries are scoped to reason codes: "Reason Code EMD (Employee Discount) is approved for up to 40% on any item at any store, for employees in the 'Staff' role."

**Additional field — Reason Code:** Matches to Counterpoint discount reason codes configured in `/settings/store/discounts`. Required — the allow-list entry applies only when this specific reason code is used. Without a reason code scope, the allow-list would suppress all discount alerts, eliminating the entire detection rule.

## UX Callout (delta)

Discount allow-lists encode the distinction between "authorized manager override" and "unauthorized discount manipulation." An LP investigator who sees "ADM has pre-approved Employee Discount code at up to 40%" knows immediately that a 35% employee discount is not suspicious. Without this, every employee purchase looks like a discount abuse alert.

## Navigation Exits

- `/settings/allowlist/dead-count` — previous allow-list
- `/settings/allowlist/voids` — next allow-list
- `/rules/:id` (Q-DR-01) — rule this allow-list feeds

## Open Questions

None.
