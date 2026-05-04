---
screen: /inventory/adjustments
title: Inventory Adjustments
role: MGR | LP
wave: W2
origin: O
cp_equivalent: "frmimphysicaladjust — Windows-only, no source attribution, no LP linkage"
---

# Inventory Adjustments

**URL:** `/inventory/adjustments`  
**Primary role:** MGR; LP  
**Entry points:** Primary sidebar nav (Inventory section); post-count auto-link; variance review → adjustment created

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Inventory Adjustments", New Adjustment button | New Adjustment → /inventory/adjustments/new |
| Filter bar | Source, Store, Date range, Item search, Direction (Increase / Decrease) | |
| Main content | Adjustments table | |

## Key Elements

### Adjustments Table
Columns: Adjustment ID, Date, Store, Item #, Description, Qty Change (+/-), Value ($), Source, Approved By, Reference.

**Source values:**
- **Physical Count:** Auto-generated from count post. Reference = Count ID.
- **Receiving:** Auto-generated from damage notation at transfer receipt. Reference = Transfer ID.
- **Transfer Variance:** Auto-generated from variance disposition (Damage / Carrier Loss). Reference = Transfer ID + variance line.
- **Manual:** Created via New Adjustment. Reference = optional note.
- **Return Processing:** Auto-generated when a return is processed against inventory.

**Direction filter:** Increases (positive qty) vs Decreases (negative qty). Decreases are the loss-relevant category — LP can filter to shrink-only quickly.

**Value ($) column:** Qty change × average cost at time of adjustment. Gives dollar impact at a glance.

**LP context:** LP can filter Source = Manual, Direction = Decrease, sort by Value descending to surface unexplained shrink events. Manual adjustments with no reference and no approval chain are the highest-risk category.

### Source Attribution
Every adjustment has a source. Auto-generated adjustments (Physical Count, Receiving, Transfer Variance) have a system-assigned reference that links back to the originating event. Manual adjustments require a reason (entered in New Adjustment form).

**Empty state:** "No adjustments in the selected period."

## Interaction Flows

1. **LP shrink review:** LP filters Source = Manual, Direction = Decrease, last 30 days → sees 4 manual decreases with no case reference → investigates each: 2 are legitimate spoilage notations by MGR, 2 are unexplained → opens alert for the 2 unexplained
2. **MGR reviews count aftermath:** After posting a count, MGR opens adjustments → filters Reference = Count #C-0047 → sees all 6 adjustments applied → confirms each matches the variance table they reviewed at post
3. **Transfer damage audit:** LP opens adjustments → filters Source = Receiving, last 60 days → identifies Store 3 has 12 receiving-damage adjustments vs 2 for Store 1 → pattern warrants investigation

## UX Callout

CP's inventory adjustment screen (`frmimphysicaladjust`) has no source field. An adjustment is an adjustment — there is no way to tell from the record whether it came from a count, a transfer, a return, or a manager covering up a theft. Canary's source attribution is the difference between an audit trail and a black box. Every adjustment has a paper trail back to its originating event. Manual adjustments are clearly labeled as manual — they stand out in the LP filter view. The four auto-generated sources cover 90% of legitimate adjustment events; a manual adjustment for something outside those categories should prompt scrutiny.

## Navigation Exits

- `/inventory/adjustments/new` — create manual adjustment
- `/inventory/count/:id/post` — from Physical Count source reference
- `/transfers/:id/variance` — from Transfer Variance source reference

## Open Questions

None.
