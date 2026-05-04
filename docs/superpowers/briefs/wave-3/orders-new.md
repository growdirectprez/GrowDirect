---
screen: /orders/new
title: Purchase Order Creation
role: BYR | MGR
wave: W3
origin: O
cp_equivalent: "frmimpo new — Windows-only, no OTB check inline, no cost vs. budget display"
---

# Purchase Order Creation

**URL:** `/orders/new`  
**Primary role:** BYR; MGR  
**Entry points:** PO list → New PO button; vendor detail → New PO action; replenishment recommendation → Create PO

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "New Purchase Order", Save Draft / Submit PO buttons | Submit notifies vendor (if integration enabled) or marks Submitted |
| Top section | Vendor + destination store selectors | Required first step |
| Main content | Line items table | |
| Right rail | Summary panel + OTB impact (L4) | |
| Action bar | Add Item, Submit PO, Save Draft, Cancel | |

## Key Elements

### Vendor + Store Selectors
Vendor dropdown (searchable) and destination store dropdown. Both required before adding line items. Selecting vendor populates the vendor's lead time and payment terms in the right rail for reference.

### Line Items Table
Columns: Item # (search with barcode scan), Description (auto-fills), Department, Vendor SKU (vendor's item code — synced from vendor item records), Order Qty (editable), Unit Cost (from vendor's last cost; editable — negotiated price can override), Line Total ($), On Hand at Destination (live).

**On Hand at Destination:** Same pattern as Transfer Initiation — shows current on-hand at the destination store as each item is added. Prevents ordering items already overstocked. If on-hand > reorder point for an item, an inline advisory appears: "On Hand: 42 — above reorder point. Confirm this order is intentional."

**Vendor SKU:** When submitting a PO to a vendor, the vendor's item code is what appears on the order. Canary maps CP item # → vendor SKU automatically from the vendor item record.

### OTB Impact Panel (L4 — Right Rail)
If the destination store has an active OTB budget for the period, the right rail shows:
- **Category Budgets:** For each category with items on this PO: Budget Remaining vs This PO's spend in that category.
- **Overall Status:** Within Budget (green) / Over Budget (red) / No OTB configured (grey).

As items are added, the OTB impact updates in real time. If a line item pushes a category over budget, an inline warning appears on that line: "Adding this item puts Tropicals $240 over the current OTB budget."

**Over-budget POs:** If submitted over budget, status = Submitted but flagged for OTB approval. The vendor is not notified until approval is granted. See `/otb/approvals`.

### Submit vs Save Draft
**Save Draft:** PO exists in Canary; vendor not notified; status = Draft.
**Submit PO:** Status → Submitted. If vendor integration is configured, PO is transmitted. If not, status = Submitted and the buyer handles vendor communication externally. OTB approval gate fires if applicable.

**Empty state:** Not applicable — create form.

## Interaction Flows

1. **Routine replenishment:** BYR opens item detail → Replenishment tab shows item #8812 is below reorder point at Store 3 → clicks Create PO → lands on orders/new pre-populated with vendor + item → adjusts qty → submits
2. **Bulk seasonal order:** BYR adds 20 drought-tolerant items from a single vendor → OTB panel shows Tropicals is $1,200 over budget for the period → removes 3 highest-cost items to bring within budget → submits
3. **Draft for review:** MGR creates a PO for a large order → saves draft → sends link to BYR for review → BYR adjusts costs based on negotiated pricing → BYR submits

## UX Callout

The OTB impact panel is the L4 addition that converts PO creation from a purchasing event into a planning event. In CP, a buyer can submit any PO for any amount at any time with no budget check. The OTB panel shows the buyer the budget consequence of each line they add, in real time, before they submit. This is the behavioral difference between a buying process that has discipline and one that doesn't: the discipline is embedded in the workflow, not enforced by a separate approval step after the fact. The on-hand-at-destination field prevents the common error of restocking an already-overstocked item — the same design principle as the transfer initiation's on-hand-at-source field.

## Navigation Exits

- `/orders` — after submit or cancel
- `/orders/:id` — on submit (navigates to new PO detail)
- `/otb` — from OTB panel budget link

## Open Questions

None.
