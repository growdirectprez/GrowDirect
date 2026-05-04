---
screen: /items
title: Item Catalog Search
role: LP | MGR | BYR
wave: W2
origin: O
cp_equivalent: "frmitems — no cross-location on-hand in search results, no return rate"
---

# Item Catalog Search

**URL:** `/items`  
**Primary role:** BYR; MGR; LP (investigative lookup)  
**Entry points:** Primary sidebar nav (Inventory section); alert detail → item link; transaction detail → item link

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Items", New Item button (BYR/ADM only) | New Item → /items/new |
| Search bar | Full-width, prominent — item #, description, barcode scan | Search triggers on 3+ characters or Enter |
| Filter bar | Category, Status (active/inactive), Asset Items (toggle — L4 A-module) | Secondary filters |
| Main content | Search results table | Empty until search performed |

## Key Elements

### Search Bar
Searches: item number (prefix match), description (fuzzy match), barcode (exact). Barcode scan support: if the device has a camera, a "Scan Barcode" icon activates camera scan mode. Useful for mobile-web use (BYR scanning items on the floor).

**Empty state (pre-search):** "Search by item number, description, or scan a barcode." — browse mode not supported; this is a search-first surface.
**No results:** "No items found for '[term]'. Check item number or try a broader description."

### Search Results Table
Columns: Item # (linked), Description, Category, On Hand (total across all locations), On Hand by Location (expandable per-row — shows each store's on-hand count), Regular Price, Return Rate (%, 90-day), Last Received Date.

**On Hand by Location expand:** Click a row's on-hand cell → expands inline to show: Store 1: 12, Store 2: 4, Warehouse: 30, etc. This is the cross-location visibility that CP's `frmitems` doesn't provide in the search results — in CP, you open the item record and navigate to the Quantities tab.

**Return Rate column:** Subtle LP signal visible to investigator role. Items with return rates > 2× category average are highlighted. This surfaces items frequently being purchased and returned — a refund fraud signal.

**Asset Items filter (L4):** Toggle showing only items classified as assets (L4 A-module addition). Useful for ADM managing asset-class items separately from retail inventory.

## Interaction Flows

1. **Cross-store on-hand check:** BYR searches for "drought tolerant grass seed" → finds item 44721 → expands on-hand by location → sees Store 1 has 47 units, Store 3 has 2 units → knows a transfer recommendation should be coming
2. **LP item lookup:** LP investigating a return fraud case → searches item # from ticket → sees item has a 22% return rate (3× category average) → notes this in the case as a supporting factor
3. **Create new item:** ADM/BYR clicks New Item → navigates to `/items/new`

## UX Callout

Cross-location on-hand in search results is a structural UX improvement over CP. In CP, a buyer who wants to know how much of an item is at each store must: open `frmitems`, find the item, navigate to the Quantities tab, read per-location rows. In Canary: search → expand the on-hand cell → done. The return rate column visible to LP role extends the item catalog into an investigative surface — an LP investigator doesn't need a separate report to find high-return items; it's a column in the standard search results.

## Navigation Exits

- `/items/:id` — item detail
- `/items/new` — item create (ADM/BYR only)

## Open Questions

None.
