---
screen: /otb
title: Open-to-Buy Dashboard
role: BYR | MGR
wave: W3
origin: N
cp_equivalent: "None — OTB is entirely absent from CP; no CP equivalent"
---

# Open-to-Buy Dashboard

**URL:** `/otb`  
**Primary role:** BYR; MGR  
**Entry points:** Primary sidebar nav (Planning section)

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Open-to-Buy", period selector, store selector | Period = buying season or fiscal month |
| Top section | OTB summary tiles | |
| Main content | Category budget table | |
| Right rail | Pending approvals + recent PO impact | |

## Key Elements

### OTB Summary Tiles
Five tiles for the selected period and store:
- **Total Budget ($):** Configured OTB budget for all categories
- **Committed ($):** Submitted + Confirmed PO amounts (money spent or committed)
- **Available ($):** Budget − Committed (what's left to spend)
- **Pending Approval ($):** Over-budget POs awaiting approval
- **Forecasted Need ($):** Estimated remaining purchasing need based on current sell-through and target end-of-period inventory position (if sell-through data is available)

**Color coding:** Available → green if > 20% of budget remains, yellow 10-20%, red < 10%.

### Category Budget Table
Rows: one per department/category. Columns: Category, Budget, Committed, Available, Committed %, Pending Approval, POs (count), Status.

**Status column per category:**
- **Healthy:** Available > 20% of budget
- **Watch:** Available 10-20%
- **Near Limit:** Available < 10%
- **Over Budget:** Committed > Budget (requires approval for any new POs)
- **Unbudgeted:** No budget configured for this category (any PO in this category bypasses OTB gate)

Clicking a category row opens a drilldown showing all POs contributing to the committed amount for that category in the selected period.

### Pending Approvals (Right Rail)
List of over-budget POs awaiting approval. Each shows: PO #, Vendor, Category, Over-budget amount, Submitted by, Time waiting. Approve / Reject actions inline. Approval releases the PO for vendor transmission; rejection returns it to Draft with a reason.

**BYR vs MGR approval authority:** Configurable. By default, MGR can approve up to a configured dollar amount; larger over-budget requests escalate to BYR or ADM.

**Empty state:** "No active OTB budgets configured for this period. Add budgets in OTB Settings to enable purchasing controls."

## Interaction Flows

1. **Buying season opening:** BYR opens OTB dashboard at start of spring season → all categories show Available = 100% (fresh budgets) → begins submitting POs → Available decreases as POs are committed
2. **Mid-season rebalance:** Tropicals budget is 95% committed with 6 weeks left in the season → BYR reviews sell-through for Tropicals → if strong, requests budget increase in OTB settings → if weak, holds remaining purchasing
3. **Over-budget approval:** BYR submitted a high-value PO that pushed Succulents over budget → appears in Pending Approvals → MGR reviews the category position and business case → approves → PO status updates to Confirmed

## UX Callout

There is no OTB module in CP. Buying discipline in a CP-managed operation is entirely manual: buyers track budget vs. commitment in spreadsheets, and there is no gate on the PO creation form. The OTB dashboard closes this gap by making purchasing discipline a system property rather than a spreadsheet habit. The "Pending Approvals" rail is the mechanism that gives senior management visibility before over-budget commitments become confirmed orders — the same concept as LP's write-off approval threshold, applied to purchasing. This is an L4 structural addition to Canary that has no CP analogue at all.

## Navigation Exits

- `/otb/settings` — configure budgets and approval thresholds
- `/orders` — full PO list
- `/orders/:id` — from pending approval row

## Open Questions

None.
