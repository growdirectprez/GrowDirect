---
screen: /transfers/new
title: Transfer Initiation
role: MGR
wave: W2
origin: N
cp_equivalent: "frmimtransferout — Windows-only, no inline on-hand at source"
---

# Transfer Initiation

**URL:** `/transfers/new`  
**Primary role:** MGR  
**Entry points:** Transfer list → New Transfer button

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "New Transfer", Save Draft / Confirm Transfer buttons | Confirm transitions status to Initiated |
| Top section | Store selector (From → To) | Required first step |
| Main content | Item lines table | Add items after selecting stores |
| Right rail | Summary panel (total units, estimated cost) + Notes field | Persistent |
| Action bar | Add Item, Confirm Transfer, Save Draft, Cancel | Bottom |

## Key Elements

### Store Selector (From → To)
Dropdown selectors for source store and destination store. Both required before adding items. Store selector shows on-hand total per store in the dropdown (e.g., "Store 1 — 247 active items") — quick context for which stores have inventory.

### Item Lines Table
Columns: Item # (search-as-you-type with barcode scan support), Description (auto-fills), On Hand at Source (live — pulled from perpetual ledger at the moment of selection), Transfer Qty (editable — validated: cannot exceed on-hand at source), Notes per line (optional).

**On Hand at Source field:** This is the key UX improvement over CP's Transfer Out form. CP requires the user to know the on-hand quantity before entering — there's no lookup during the form entry. Canary shows on-hand at source on every line as you add items. "You have 40 on hand at Store 1 — enter transfer quantity."

**Validation:** Transfer Qty > On Hand at Source triggers an inline error: "Transfer quantity cannot exceed on-hand. Adjust quantity or select a different source store."

### Summary Panel
Running total: line count, total units being transferred, estimated cost (units × average cost at source). Not an authorization amount — informational.

### Notes Field
Optional notes for the transfer: reason (e.g., "Cover stockout at Store 3 — drought-tolerant grass seed"), expected delivery method, ETA.

**Empty state:** Not applicable — create form.

## Interaction Flows

1. **Balance inventory between stores:** MGR selects From = Store 1, To = Store 3 → searches "drought tolerant" → adds item 44721 → sees on-hand at Store 1 is 47 → enters Transfer Qty = 20 → adds notes → Confirm → status = Initiated → Store 3 notified
2. **Emergency stockout cover:** MGR selects same day same stores → adds single item with qty 5 → confirms immediately (no draft) → Store 3 receives notification to expect transfer
3. **Partial fulfillment:** MGR adds 3 items → realizes on-hand for item 3 is lower than expected → reduces qty or removes the line → confirms with 2 of 3 originally planned items

## UX Callout

The on-hand-at-source field on every line item is the primary UX improvement over CP's Transfer Out form. CP requires the user to look up on-hand separately (in `frmitems` or an inventory report), write it down, and then key it into the Transfer Out form. Canary fetches it live during form entry. The difference in error rate and time-per-transfer is material — getting wrong quantities into a transfer is a common CP operational problem that creates variance records downstream.

## Navigation Exits

- `/transfers` — after confirm (redirects to new transfer's detail)
- `/transfers` — cancel

## Open Questions

None.
