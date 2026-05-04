---
screen: /orders/:id/receive
title: PO Receiving
role: RCV | MGR
wave: W3
origin: N
cp_equivalent: "frmimreceiving — Windows-only, no mobile, no partial receipt handling, no damage flag"
---

# PO Receiving

**URL:** `/orders/:id/receive`  
**Primary role:** RCV; MGR  
**Entry points:** PO detail → Confirm Receipt; receiving list → inbound PO action

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Receiving PO #[id] from [Vendor]", expected receipt date | |
| Main content | Receipt line entry table | Mobile-optimized: large tap targets, barcode scan |
| Damage notation section | Per-line damage flags + free text | Below line table |
| Action bar | Confirm Receipt, Save Progress, Flag for Review | |

## Key Elements

### Receipt Line Entry Table
Columns: Item # (scan icon), Description, Vendor SKU, Ordered Qty, Confirmed Qty, Expected Remaining (Confirmed − Previously Received), Received Qty (editable), Variance (auto-computed), Damage Flag (per-line toggle).

**Expected Remaining** is the operative column — if a PO has been partially received, RCV only needs to match the remaining expected qty, not the full original order. This prevents double-counting on multi-delivery POs.

**Variance:** Same auto-computation as transfer receipt — positive (over), negative (short), zero (clean). Color-coded green/orange/blue. Variance = 0 for all lines is the target state.

**Barcode Scan:** RCV taps scan icon → scans item barcode → item row highlights → enters received qty on large numeric keypad. Mobile-first — RCV is at the receiving dock.

### Damage Flag
Per-line toggle. When flagged: damage description field appears. Damaged quantities are counted as received but flagged for inventory adjustment. Same pattern as transfer receipt.

### Confirm Receipt Action
Posts the receipt. Inventory at destination increases by received qty for each line. PO line statuses update (Received / Partially Received). If any variance exists: advisory shown ("3 line items have variances — review before confirming"). RCV can confirm through or return to correct entries.

After confirmation: PO status recalculated. If all lines fully received: PO → Received. If some lines remain: PO → Partially Received.

**Cost capture:** On receipt, the unit cost from the PO line is captured against the inventory record as the latest cost. Perpetual ledger updates with received qty × cost.

### Save Progress
Same pattern as transfer receipt — session preserves entered quantities; RCV can resume if interrupted.

**Empty state:** All Received Qty fields blank at start.

## Interaction Flows

1. **Standard receipt:** RCV scans each item → all quantities match expected remaining → confirms → PO fully received → inventory updated
2. **Partial delivery:** Vendor delivers 3 of 5 PO lines today → RCV enters the 3 received lines → 2 lines left at 0 received → confirms partial → PO status = Partially Received → remaining lines stay open for next delivery
3. **Short shipment:** RCV enters 48 units for item with expected 50 → variance = −2 → notes "vendor shorted 2 units, not included in delivery slip" → confirms → variance logged against PO line; buyer notified

## UX Callout

PO receiving in CP (`frmimreceiving`) requires a PC at the receiving dock — same problem as transfer receipt. Canary's PO receiving form is mobile-first for the same reason: the dock is where the count happens, not the office. The expected-remaining column is the W3 refinement on the W2 transfer receipt pattern — multi-delivery POs are the norm in wholesale purchasing, and Canary tracks each delivery against the running remaining balance automatically. In CP, partial receipts require the buyer to manually track what's been received across multiple receipt events; Canary maintains this state as a first-class feature of the PO record.

## Navigation Exits

- `/orders/:id` — back to PO detail (from Save Progress or after confirm)
- `/receiving` — receiving list (if navigated from there)

## Open Questions

None.
