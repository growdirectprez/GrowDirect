---
screen: /vendors/:id
title: Vendor Detail
role: BYR | MGR
wave: W3
origin: O
cp_equivalent: "frmvendors detail — Windows-only, no order history, no performance summary"
---

# Vendor Detail

**URL:** `/vendors/:id`  
**Primary role:** BYR; MGR  
**Entry points:** Vendor list row

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Vendor name, status badge, category | Breadcrumb back to /vendors |
| Top section | Contact info + payment terms | |
| Tab bar | Overview / Items / Orders / Performance | |
| Tab content | Tab-dependent | |

## Tabs

### Overview Tab
Vendor contact information: company name, address, phone, email, account rep name and contact, website. Payment terms (Net 30/60/90 etc.), minimum order amounts, lead time (days from PO to expected receipt), preferred shipping method.

**CP crosswalk:** Canary syncs basic contact info from CP's vendor record. Payment terms and lead time, if managed in CP, sync automatically. Additional fields (account rep email, notes) are Canary-native.

### Items Tab
All items sourced from this vendor. Table: Item #, Description, Department, CP Cost, Last Cost (most recent PO), Last Ordered Date, On Hand (across all stores), GMROI. Sorted by GMROI ascending by default — underperforming items at top.

BYR uses this tab to evaluate which items to continue ordering, discontinue, or renegotiate costs on.

### Orders Tab
All POs with this vendor, paginated. Table: PO #, Order Date, Expected Receipt Date, Received Date, Status, Total ($), On-Time (yes/no), Return Value. Sorted by Order Date descending. Clicking a PO navigates to `/orders/:id`.

**Performance visible from orders:** The on-time delivery % shown in the vendor list is computed from this tab's raw data.

### Performance Tab
Charts and KPIs for this vendor over a selectable period (last 90 days / 6 months / 1 year):
- On-Time Delivery % over time (line chart — is performance improving or declining?)
- Average Lead Time (days): PO placed → first receipt
- Return Rate % over time
- Average Cost vs Market Cost (if market comp data available — TBD)
- Fill Rate: % of ordered units actually received (unfilled line items = availability problem)

**Empty state per tab:** "No [items/orders/performance data] for this vendor."

## Interaction Flows

1. **Vendor renewal review:** BYR opens vendor detail → Performance tab → on-time delivery was 90% a year ago, now 62% → trend is declining → opens Orders tab to find the specific POs that were late → prepares for vendor call
2. **Cost negotiation prep:** BYR opens vendor detail → Items tab → sorts by Last Cost → 12 items where Last Cost increased > 10% vs previous → identifies negotiation targets
3. **AP dispute:** Finance opens vendor detail → Orders tab → finds PO #P-0312 shows Received but vendor claims not paid → navigates to order detail to verify receipt and payment status

## UX Callout

Vendor detail in CP is essentially a contact card. There is no order history on the vendor record, no performance metrics, and no view of which items this vendor supplies. A buyer evaluating a vendor relationship in CP must run separate reports (PO history, item list) and manually correlate the results. Canary puts the complete vendor picture — contact info, items, order history, and performance trends — in one place. The performance tab's declining trend line is the kind of signal that gets missed when performance data lives in a spreadsheet someone updates quarterly rather than computed continuously from operational data.

## Navigation Exits

- `/vendors` — back to vendor list
- `/orders/:id` — from Orders tab
- `/items/:id` — from Items tab
- `/orders/new` — create new PO for this vendor

## Open Questions

None.
