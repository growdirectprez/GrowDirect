---
screen: /items/new
title: Item Create
role: ADM | BYR
wave: W2
origin: N
cp_equivalent: "frmitems new record — Windows-only"
---

# Item Create

**URL:** `/items/new`  
**Primary role:** ADM; BYR  
**Entry points:** Item catalog search → New Item button; vendor detail → "New item for this vendor"

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "New Item", Save Draft / Save & Activate buttons | Two save modes — draft doesn't make item active in POS |
| Main content | Multi-section form — Basics + Pricing + Inventory Defaults + Identifiers | Single scroll or tabbed; recommended: single scroll for create flow |
| Action bar | Save Draft, Save & Activate, Cancel | Bottom; fixed |

## Key Elements

### Basics Section
Required: Item #, Description, Category (searchable dropdown), Vendor (searchable dropdown → `/vendors/:id`), Unit of Measure, Status (Draft / Active).
Optional: Subcategory, Alternate description, Item notes.

Item # can be auto-generated (sequential from last used # in category) or manually entered. Auto-generate is the default — most operators don't hand-craft item numbers.

### Pricing Section
Regular price (required). Location price overrides (optional — set different regular prices per store). Sales tax code (mapped to tax authorities in `/settings/tax`).

### Inventory Defaults Section
Min (reorder point), Max, Reorder quantity. Applied as defaults across all locations when item is activated. Location-specific values can be overridden on `/items/:id` Replenishment tab after creation.

### Identifiers Section
Primary barcode (UPC/EAN — required if barcode scanning is used). Additional barcodes (+ Add Barcode — repeating field). Alternative item # (vendor's part number, for receiving matching).

### Save & Activate vs Save Draft
- **Save Draft:** Item saved but not visible in POS or search results. ADM completes setup before activating. Draft items appear in item search with "Draft" badge.
- **Save & Activate:** Item immediately active — visible in POS, available for transactions, included in reports.

**Empty state:** Not applicable — this is a create form.

## Interaction Flows

1. **Create standard retail item:** BYR fills in basics + pricing + primary barcode → Save & Activate → item immediately searchable and available in POS reports
2. **Create draft for future season:** BYR creates next season's inventory items in draft state before they arrive → items exist in catalog for PO creation but are not visible to POS cashiers → ADM activates when stock arrives
3. **Batch import alternative (note):** For bulk item creation (> 20 items), the file import on the item list may be faster. This screen handles single-item creation. Both paths lead to the same active item state.

## UX Callout

Item creation in CP requires navigating to `frmitems`, selecting New, and filling in a complex multi-tab form that includes fields irrelevant to most operators (Bills of Material, serial number tracking, complex pricing profiles). Canary's create form shows only the fields that matter for a standard retail item, with the multi-tab complexity deferred to the item detail page after creation. The Save Draft / Save & Activate distinction solves a real operational problem: buyers often need to create items in advance of stock arrival (for PO creation purposes) without making them available at the register.

## Navigation Exits

- `/items/:id` — redirects here after save (new item's detail page)
- `/items` — cancel returns here

## Open Questions

None.
