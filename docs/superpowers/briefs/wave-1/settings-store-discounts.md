---
screen: /settings/store/discounts
title: Store Config — Discount Cap
role: ADM
wave: W1
origin: O
cp_equivalent: "frmpscontrol"
---

# Store Config — Discount Cap

**URL:** `/settings/store/discounts`  
**Primary role:** ADM  
**Entry points:** Settings nav → Store Config → Discount Cap

**Inherits layout and pattern from `/settings/store/drawer`.** See that brief for the full screen pattern. Delta documented here.

## Delta from Drawer Threshold

**Context panel:** "This cap sets the maximum discount percentage (as a % of transaction subtotal) before Canary generates a Q-DR-01 Discount Cap Detection alert. Stores with routine manager discounts or employee purchase programs may need a higher cap."

**Rule fed:** Q-DR-01 Discount Cap Detection.

**Config field:** Max discount percentage (%) per store — not a dollar amount. Stored as a decimal (e.g., 20.0 = 20%). Per-store, per reason code overrides are configured in `/settings/allowlist/discounts` — this screen sets the global cap that applies when no allow-list entry matches.

**Interaction note:** This threshold interacts with the Discount Allow-List. The allow-list can authorize a specific reason code to exceed this cap. The cap is the fallback: if no allow-list entry matches the reason code + cashier + store combination, this threshold applies.

## Navigation Exits

- `/settings/store/drawer` — previous store config LP threshold screen
- `/settings/store/void-reasons` — next

## Open Questions

None.
