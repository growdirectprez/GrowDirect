---
screen: /transfers/:id
title: Transfer Detail
role: MGR | RCV
wave: W2
origin: O
cp_equivalent: "Transfer Out detail — no partial-fulfillment notation, no receiving-store notification"
---

# Transfer Detail

**URL:** `/transfers/:id`  
**Primary role:** MGR; RCV  
**Entry points:** Transfer list row

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Transfer ID, status badge, From Store → To Store, initiated date | Breadcrumb back to /transfers |
| Top section | Transfer header (origin/destination, dates, status) | |
| Main content | Line items table | |
| Bottom section | Notes section + action log | |
| Action bar | Confirm Shipment, Print Picking List, Add Note | MGR-only actions |

## Key Elements

### Transfer Header
From store, To store, Initiated by (user), Initiated date, Expected receipt date (editable by MGR if date changes), Status badge.

### Line Items Table
Columns: Item #, Description, Qty Requested, Qty to Ship (editable — default = qty requested), Notes per line (for partial fulfillment notation).

**Qty to Ship is editable before shipment confirmation.** If MGR discovers a specific item is not fully available at pack time (e.g., requested 20 but only 17 saleable units on the shelf), they can reduce Qty to Ship to 17 and add a line note: "3 units damaged in storage — not included."

After Confirm Shipment, Qty to Ship is locked. The variance between Qty Requested and Qty to Ship is noted as a "Pre-ship variance" — distinct from a transit variance (items lost between ship and receipt).

### Action Log
Time-ordered record of all actions on this transfer: created by / when, edited by / when (with field changes), confirmed shipment by / when, received by / when (destination store's action). This is the audit trail for the transfer.

### Confirm Shipment Action
Changes status from Initiated → In Transit. Triggers: notification to destination store's MGR/RCV ("Transfer T-1049 from Store 1 has shipped — 3 items, 45 units. Expected [date]."), inventory at source does NOT decrement until receipt is confirmed (perpetual ledger waits for receipt to close the loop).

### Print Picking List
Generates a formatted PDF of the line items (item #, description, qty to ship, storage location if configured). Used by warehouse/stock room staff picking items for the transfer.

**Empty state:** Not applicable — transfer exists before this screen is reached.

## Interaction Flows

1. **Use as picking list:** RCV at source store opens this screen → reviews line items → physically picks each item → adjusts Qty to Ship if any discrepancies → Confirms Shipment
2. **Partial fulfillment:** MGR can only ship 3 of 5 items (2 items backordered) → creates this transfer with 3 items, notes backorder status in transfer notes → confirms shipment of 3 → creates a new transfer for the remaining 2 when stock arrives
3. **Check transfer status:** Destination store MGR opens transfer → sees status = In Transit, expected 2026-05-07 → checks Qty to Ship to know what to prepare receiving dock for

## UX Callout

The editable Qty to Ship before confirmation is the mechanism that prevents the most common CP transfer problem: a quantity entered at initiation that differs from what actually shipped, creating unexplained variances at receipt. CP's Transfer Out form sets the quantity at initiation time with no way to adjust at pack time without creating a new form. Canary allows the adjustment at the source before shipment confirmation, with a clear audit trail of what was changed and why.

## Navigation Exits

- `/transfers` — back to transfer list
- `/transfers/:id/receive` — for destination store MGR/RCV
- `/transfers/:id/variance` — if variance detected at receipt (auto-navigated or from transfer list)

## Open Questions

None.
