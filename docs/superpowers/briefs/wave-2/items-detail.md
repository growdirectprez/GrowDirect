---
screen: /items/:id
title: Item Detail
role: LP | MGR | BYR
wave: W2
origin: O+L4
cp_equivalent: "frmitems — no performance KPIs, no cross-location committed view, no alert overlay"
---

# Item Detail

**URL:** `/items/:id`  
**Primary role:** BYR (primary); MGR; LP  
**Entry points:** Item catalog search result

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Item # + Description, Status badge (Active/Inactive), Edit button (ADM/BYR) | Breadcrumb back to /items |
| Top section | Item card (attributes) + Performance KPI row | Full-width |
| Tab bar | Overview · Pricing · Inventory by Location · Sales History · Replenishment · Alerts | Role-filtered tabs |
| Active tab content | Tab-specific content | Primary working area |

## Key Elements

### Item Card
Item image (placeholder if none), Item #, Description, Category, Subcategory, Vendor (linked to `/vendors/:id`), Unit of Measure, Status, Barcodes (list). All visible in the card — no tab navigation needed for basic attributes.

### Performance KPI Row
Four tiles, always visible:
- **Sell-Through Rate** (% of received inventory sold in the period)
- **Return Rate** (% of units returned, 90-day)
- **GMROI** (gross margin return on inventory investment — key buyer metric)
- **Discount Rate** (% of transactions on this item that included a discount)

KPI row is role-aware: LP sees Return Rate and Discount Rate prominently; BYR sees GMROI and Sell-Through prominently. Same values, different visual emphasis.

### Inventory by Location Tab
Table: Location (store name), On Hand, Committed (reserved by open orders/layaways), Available (on hand − committed), Min (reorder point), Max. The committed/available distinction (CP shows only on-hand; buyers make decisions without knowing how much is reserved) is the critical addition.

### Pricing Tab
Unified price intelligence surface (CP displacement target #1):
- Regular price with effective date
- All active special prices (date range, applicable stores, amount/%)
- All active promotions affecting this item (linked to `/promotions`)
- All active contract prices (customer-specific — listed if any exist)
- Price simulator: input: qty × customer × date × store → output: final price with precedence explanation

### Sales History Tab
Units/week chart (90 days). Transaction list (last 50 transactions involving this item). Filterable by store, date.

### Replenishment Tab (L4 — O.2.1 gap)
Parameters per location: Reorder Point (ROP), Economic Order Quantity (EOQ), Safety Stock, Weeks of Supply (WOS) target. Edit inline. These values feed the Suggested Orders algorithm.

### Alerts Tab (LP role only)
All LP alerts that reference this item in their evidence. Read-only. Allows LP to see at a glance whether an item has been involved in prior alerts — useful for high-return items.

**Empty states:** All tabs show "No data available" when their data set is empty.

## Interaction Flows

1. **Buyer inventory check:** BYR opens item → switches to Inventory by Location tab → sees committed vs available per store → identifies Store 3 has 40 on-hand but only 8 available (32 committed to open orders) → adjusts replenishment plan
2. **Investigate high-return item:** LP opens item from transaction evidence → sees Return Rate = 18% (alerts tab shows 4 prior alerts) → opens Alerts tab → reviews prior alert patterns → adds to case notes
3. **Price check before season:** BYR opens item → goes to Pricing tab → uses price simulator → confirms seasonal promotion is applying correctly to the expected customer + store combo

## UX Callout

Committed inventory (on-hand minus reserved by orders = truly available) is a buyer decision-quality improvement with no CP equivalent. CP shows raw on-hand from `frmitems` quantities tab. A buyer making a replenishment decision needs to know what's actually available to sell — not what's physically in the store. If 32 of 40 units are committed to layaways and special orders, the effective stock is 8, not 40. Canary surfaces this distinction on the default inventory tab. The Pricing tab's unified price simulator replaces 7 separate CP forms that buyers currently navigate to understand what a customer will actually pay.

## Navigation Exits

- `/items` — back to item search
- `/items/:id/edit` — item edit (ADM/BYR)
- `/vendors/:id` — vendor linked from item card
- `/orders/suggested` — if replenishment params indicate reorder needed
- `/promotions` — promotion linked from Pricing tab
- `/alerts/:id` — from Alerts tab

## Open Questions

None.
