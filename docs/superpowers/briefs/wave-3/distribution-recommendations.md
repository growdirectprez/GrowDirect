---
screen: /distribution
title: Distribution Recommendations
role: BYR | MGR
wave: W3
origin: N
cp_equivalent: "None — CP has no distribution recommendation engine; multi-store rebalancing is entirely manual"
---

# Distribution Recommendations

**URL:** `/distribution`  
**Primary role:** BYR; MGR  
**Entry points:** Primary sidebar nav (Planning section); item detail → Distribution tab

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Distribution Recommendations", refresh button, as-of timestamp | |
| Filter bar | Category, Urgency (High / Medium / Low), Store (source or destination) | |
| Main content | Recommendations queue | |

## Key Elements

### Recommendations Queue
Table: Item #, Description, Category, From Store, To Store, Recommended Qty, Reason, Urgency, Estimated Rebalance Value ($), Action.

**Reason types:**
- **Stockout Prevention:** Destination store is below reorder point; source store has excess. Transfer recommended before stockout occurs.
- **Excess Rebalance:** Source store carrying > target days-on-hand; destination store carrying < target. Transfer normalizes both positions.
- **Sell-Through Support:** Source store has items with poor sell-through; destination store has higher velocity for the same item. Transfer improves sell-through rate at the system level.
- **Overstock Correction:** Source store significantly over target position; no specific destination need, but reducing the overstock reduces carrying cost. May recommend multiple small destination stores.

**Urgency:** High = stockout likely within current lead time if not transferred. Medium = within 2× lead time. Low = rebalancing opportunity, not urgent.

**Estimated Rebalance Value ($):** Cost value of the transfer. Used for OTB impact awareness — large rebalancing transfers consume buying capacity even if they're inter-store movements.

**Action:** "Create Transfer" button → navigates to `/transfers/new` pre-populated with From Store, To Store, Item, and Recommended Qty. BYR or MGR reviews and confirms; the recommendation doesn't auto-create transfers.

### Proximity Weighting
Recommendations factor in store proximity (from geo-coordinates in store settings). A transfer from Store 1 to Store 3 (adjacent) is preferred over a transfer from Store 1 to Store 8 (distant). Distance affects shipping cost and lead time; the recommendation engine weights proximity when multiple destinations could absorb the excess.

**Dismiss action:** Individual recommendations can be dismissed ("Not needed — handling via PO"). Dismissed recommendations reappear if the condition worsens.

**Empty state:** "No rebalancing opportunities identified. All stores are within target inventory positions." (Ideal state — rarely seen in practice.)

## Interaction Flows

1. **Morning rebalance review:** BYR opens distribution recommendations → High urgency filter → 3 stockout-prevention recommendations → creates transfers for each → transfers initiated before next delivery day
2. **Seasonal overstock clearance:** End of spring season → BYR opens distribution → 12 "Excess Rebalance" recommendations for drought-tolerant grass seed (peak season is ending, Store 1 heavily overstocked) → creates transfers to distribute excess across stores with lower positions
3. **Sell-through optimization:** BYR sees Cacti category has poor sell-through at Store 2 but strong at Store 4 → distribution rec flags "Sell-Through Support: Move 8 units of item #8812 from Store 2 to Store 4" → creates transfer

## UX Callout

There is no multi-store rebalancing intelligence in any retail POS platform for this market segment. A buyer managing inventory across 4-6 stores in CP does this manually: they pull inventory reports per store, identify imbalances, and initiate transfers based on memory and intuition. Canary computes the recommendations from the perpetual ledger and surfaces them as actionable queue items. The buyer's judgment is still required — the system recommends, the buyer decides. The recommendation engine replaces the research phase (pulling reports, identifying imbalances) not the decision phase. This is the L4 structural addition that makes multi-store buying genuinely manageable at sub-enterprise scale.

## Navigation Exits

- `/transfers/new` — from Create Transfer action (pre-populated)
- `/items/:id` — from item # column link

## Open Questions

None.
