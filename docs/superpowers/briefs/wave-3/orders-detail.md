---
screen: /orders/:id
title: Purchase Order Detail
role: BYR | MGR | RCV
wave: W3
origin: O
cp_equivalent: "frmimpo detail — no receiving progress, no action log, no partial receipt tracking"
---

# Purchase Order Detail

**URL:** `/orders/:id`  
**Primary role:** BYR; MGR; RCV  
**Entry points:** PO list row

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | PO #, status badge, vendor name, destination store | Breadcrumb back to /orders |
| Top section | PO header (vendor, store, dates, terms, OTB status) | |
| Main content | Line items table | |
| Bottom section | Notes + action log | |
| Action bar | Confirm Receipt, Edit PO (Draft only), Cancel PO, Print PO | Role-filtered |

## Key Elements

### PO Header
Vendor, destination store, Order Date, Expected Receipt Date, Submitted Date, Confirmed Date (when vendor acknowledged — if integration enabled), Total ($), Payment Terms, Lead Time, OTB status badge (L4).

### Line Items Table
Columns: Item #, Description, Vendor SKU, Order Qty, Confirmed Qty (vendor's confirmed quantity — may differ from ordered if vendor has partial availability), Received Qty (from receipts), Remaining Qty (Confirmed − Received), Unit Cost, Line Total, Status (Open / Partially Received / Received / Cancelled).

**Remaining Qty column:** Key field for the receiving dock. "What is still expected to arrive on this PO?" answers directly from this column. For partially received POs, the remaining qty drives dock prep.

**Received Qty:** Updates automatically as receipts are posted. Each receipt event is linked to specific PO lines — receiving 10 units of item #7734 against PO #P-0048 shows 10 in the Received Qty for that line.

### Action Log
Immutable time-ordered record: created by/when, submitted, vendor confirmed, first receipt, partial receipt events, fully received, any edits made before submission. Same audit trail model as transfer detail.

### Confirm Receipt Action
Opens the receiving workflow at `/orders/:id/receive` (or routes to `/receiving/new` pre-populated with this PO). Available to RCV and MGR for the destination store.

### Edit PO
Only available in Draft status. After submission, the PO is locked. Changes require cancellation and re-creation, or a change order (future enhancement — not in scope for W3).

### Cancel PO
Marks the PO as Cancelled. If partially received, cancellation applies only to unrecieved lines. Reason required. Logged in action log.

**Empty state:** Not applicable — PO exists before this screen.

## Interaction Flows

1. **Receiving dock prep:** RCV opens PO detail → reviews Remaining Qty column → 5 items still expected → 2 items fully received on the last delivery → prepares dock for the remaining 3
2. **Vendor quantity discrepancy:** Vendor confirms they can only ship 80 of 100 ordered units → BYR updates Confirmed Qty to 80 → Remaining Qty recalculates → notes entered in action log
3. **BYR PO audit:** BYR reviews submitted POs → opens PO #P-0048 → checks Received Qty vs Confirmed Qty → all items received → marks reviewed in notes

## UX Callout

The Remaining Qty column answers the question every receiving manager asks before a delivery: "What am I supposed to get today?" In CP, this requires opening the PO, mentally subtracting the received quantities from the ordered quantities, and doing that for each line. Canary computes it. The action log applies the same evidentiary model as the transfer detail — every change to the PO is stamped, and the receiving dock always knows the authoritative expected delivery.

## Navigation Exits

- `/orders` — back to PO list
- `/orders/:id/receive` — start receiving
- `/vendors/:id` — vendor detail from header

## Open Questions

None.
