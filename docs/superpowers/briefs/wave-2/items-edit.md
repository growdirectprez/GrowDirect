---
screen: /items/:id/edit
title: Item Edit
role: ADM | BYR
wave: W2
origin: N
cp_equivalent: "frmitems — same form, Windows-only"
---

# Item Edit

**URL:** `/items/:id/edit`  
**Primary role:** ADM; BYR  
**Entry points:** Item detail → Edit button (top-right)

## Layout

**Inherits layout from `/items/new`.** Same form sections (Basics, Pricing, Inventory Defaults, Identifiers). Pre-populated with existing values.

**Key difference from create:** No "Save Draft" mode — item is already active (or in an existing state). Save is immediate. A "Deactivate" action (separate from Save) is available for active items.

## Key Elements

### Edit Form (pre-populated)
Same fields as `/items/new`. All sections visible and editable by ADM/BYR role. MGR role can view the edit form in read-only mode (no save) — this prevents unintended edits by store managers who only have view authority on catalog data.

### Price Edit (on Pricing section)
Editing the regular price here applies to all locations (global price change). Location-specific overrides are managed from the item detail Pricing tab after saving, not from this form.

Price change is audited: old price, new price, changed by, timestamp — visible on the Price History report (`/reports/price-history`).

### Deactivate Action
Available below the Save button. Deactivating an item: removes it from POS search, stops new transactions from using it, preserves historical data. Requires confirmation: "Deactivate this item? It will no longer be available for new transactions." Items with open orders or committed inventory cannot be deactivated until those are resolved — system shows a blocking warning.

### Barcode Management
Identifiers section allows adding/removing barcodes. Removing a barcode that appears on existing inventory labels is flagged: "This barcode appears on recent receiving records. Removing it may affect future barcode scans."

**Empty state:** Not applicable — pre-populated form.

## Interaction Flows

1. **Update vendor:** BYR switches the vendor on an item (new supplier found) → changes Vendor dropdown → saves → item's vendor linked updates, future POs default to new vendor
2. **Correct description:** ADM fixes a typo in an item description → edits Description field → saves → corrected description appears in search results and transaction displays
3. **Deactivate discontinued item:** BYR selects Deactivate → confirms → item no longer available at register → historical transactions referencing it remain intact

## UX Callout

Same functionality as CP's `frmitems` edit mode, delivered web-native. The distinction is operational context: in CP, editing an item requires a PC at the office; in Canary, a buyer on the floor with a tablet can edit item details on the spot after identifying an error during a receiving session. Price change auditing (visible in `/reports/price-history`) is automatic — no separate "price change log" form needed.

## Navigation Exits

- `/items/:id` — returns here after save
- `/items` — cancel returns to item search

## Open Questions

None.
