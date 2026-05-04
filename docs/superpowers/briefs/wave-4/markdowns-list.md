---
screen: /markdowns
title: Markdown Queue
role: BYR | MGR
wave: W4
origin: N
cp_equivalent: "Price changes via frmitems — no markdown queue, no systematic clearance workflow, no sell-through trigger"
---

# Markdown Queue

**URL:** `/markdowns`  
**Primary role:** BYR; MGR  
**Entry points:** Primary sidebar nav (Merchandising section); distribution recommendations → markdown flag

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Markdowns", New Markdown button | |
| Filter bar | Status (Proposed / Approved / Active / Completed), Category, Store, Urgency | |
| Main content | Markdown queue table | |

## Key Elements

### Markdown Queue Table
Columns: Item #, Description, Category, Store(s), Current Price ($), Proposed Price ($), Markdown % , Current On Hand (units), Days on Hand, Sell-Through Rate (%), Status badge, Proposed By, Urgency.

**Urgency:**
- **High:** Days on Hand > 90 (end-of-season overstock); seasonal item with approaching sell-by date
- **Medium:** Days on Hand 60-90, sell-through rate < 30%
- **Low:** Sell-through rate below category average; no urgency but optimization opportunity

**Sell-Through Rate:** Same metric as Category Performance report — units sold ÷ beginning inventory for the period. Items with < 20% sell-through over 60+ days are typical markdown candidates.

**Proposed By:** Can be BYR (manual), or the Distribution Optimizer agent (automated identification). Agent-proposed markdowns appear with an "Agent" badge and the recommendation rationale (e.g., "Days on hand = 108, sell-through = 12% — at current velocity, this item will not clear before next seasonal cycle").

**Status workflow:** Proposed → Approved → Active → Completed. Approved markdowns are price changes pending MGR execution. Active markdowns have been applied to item prices. Completed markdowns have cleared the overstock (sell-through goal met or time window elapsed).

**Empty state:** "No markdown candidates identified. Items will appear here when sell-through thresholds are crossed."

## Interaction Flows

1. **End-of-season clearance:** BYR opens markdown queue → High urgency filter → 14 items → reviews each → adjusts proposed prices based on competitive context → approves all → MGR applies prices
2. **Agent-proposed markdown review:** BYR opens queue → 3 agent-proposed markdowns → reviews rationale → approves 2, rejects 1 (item has purchase order incoming — inventory will clear through demand before next cycle)
3. **Cascading markdown:** Item doesn't clear on first markdown → BYR applies a deeper markdown → updates proposed price → re-approves → price applied

## UX Callout

In CP, markdowns are executed by opening each item record individually and changing the price. There is no queue of candidates, no sell-through trigger, and no workflow for approval. A buyer managing end-of-season clearance in CP is doing it by memory: which items looked slow last week? Which categories haven't been moving? Canary's markdown queue is generated continuously from the perpetual ledger — items cross the sell-through threshold and appear in the queue automatically. The agent-proposed markdowns close the gap between "the system knows this item is slow" and "the buyer has been notified and can act." Nothing about the markdown decision is automated; the queue is the research phase replaced by computation.

## Navigation Exits

- `/markdowns/new` — manual markdown creation
- `/markdowns/:id` — markdown detail / edit
- `/items/:id` — from item # column

## Open Questions

None.
