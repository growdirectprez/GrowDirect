---
screen: /orders
title: Purchase Order List
role: BYR | MGR
wave: W3
origin: O
cp_equivalent: "frmimpo — Windows-only, no OTB check at list level, no delivery performance column"
---

# Purchase Order List

**URL:** `/orders`  
**Primary role:** BYR; MGR  
**Entry points:** Primary sidebar nav (Purchasing section)

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Purchase Orders", New PO button | New PO → /orders/new |
| Filter bar | Status, Vendor, Store, Date range, Overdue Only toggle | |
| Main content | PO table | |

## Key Elements

### PO Table
Columns: PO #, Vendor, Store (destination), Order Date, Expected Receipt Date, Status badge (Draft / Submitted / Confirmed / Partially Received / Received / Cancelled), Total ($), OTB Status (L4), Overdue indicator.

**Status color-coding:** Draft = grey, Submitted = blue, Confirmed = purple, Partially Received = orange, Received = green, Cancelled = red.

**OTB Status (L4 — Open-to-Buy):** For stores with OTB module enabled, shows whether the PO is Within Budget / Over Budget / Pending Approval. A red "Over Budget" badge on a Submitted PO means it's waiting for budget approval before the vendor is notified. Canary-native — no CP equivalent. See OTB screens at `/otb/*`.

**Overdue filter:** POs where Expected Receipt Date has passed and status is not Received or Cancelled. Surfaces vendor delivery failures before they become stockout events. Same pattern as the overdue transfer filter.

**Partially Received status:** A PO where some lines have been received but not all. Common with large multi-item orders from vendors who ship in multiple drops. Clicking navigates to the PO detail to see which lines are pending.

**Empty state:** "No purchase orders in the selected period."

## Interaction Flows

1. **Morning receiving prep:** MGR filters to Status = Confirmed/Partially Received, Store = own store → sees 2 POs expected today → reviews line items before the delivery truck arrives
2. **Overdue vendor follow-up:** BYR applies Overdue Only toggle → 3 POs from the same vendor, all > 5 days late → opens vendor detail to log notes before calling account rep
3. **OTB budget check:** BYR opens PO list → sees 2 POs flagged "Over Budget" → opens each to review which category drove the overage → adjusts quantities or escalates for approval

## UX Callout

CP's `frmimpo` requires the buyer to open each PO to see its status and content. There is no list-level performance signal — overdue detection requires manually scanning expected receipt dates. The overdue toggle in Canary's PO list surfaces vendor delivery failures proactively, in the same way the overdue transfer toggle surfaces transit shrink. The OTB status column is the L4 addition that brings purchasing discipline to the PO list — a buyer can see at a glance whether the orders they've submitted are within the budget framework they set for the period.

## Navigation Exits

- `/orders/new` — create new PO
- `/orders/:id` — PO detail
- `/otb` — OTB budget management (L4)

## Open Questions

None.
