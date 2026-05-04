---
screen: /inventory/count
title: Physical Count List
role: MGR | CNT
wave: W2
origin: O
cp_equivalent: "frmimphysicalcount — Windows-only, no mobile entry, no real-time progress"
---

# Physical Count List

**URL:** `/inventory/count`  
**Primary role:** MGR; CNT (Counter)  
**Entry points:** Primary sidebar nav (Inventory section)

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Physical Counts", New Count button | New Count → /inventory/count/new |
| Filter bar | Status, Store, Date range | |
| Main content | Count table | |

## Key Elements

### Count Table
Columns: Count ID, Store, Count Type (Full / Department / Spot), Initiated Date, Scheduled Date, Status badge (Draft / In Progress / Completed / Posted), Item Count (total items in scope), Progress (% of lines entered — live during In Progress), Variance ($) (populated after post), Actions.

**Status color-coding:** Draft = grey, In Progress = blue, Completed = green (awaiting post), Posted = teal (finalized), Variance-Flagged = red (if variance > threshold after post).

**Progress column:** Visible only for In Progress counts. Updates in real-time as counter entries are submitted. "47 / 120 lines" shows exact line progress; the percentage gives scan speed feedback.

**Variance ($) column:** Populated after posting. Negative = short (loss); positive = over. Clicking variance amount on a Posted row navigates to the count's adjustment summary.

### New Count Button
Navigates to `/inventory/count/new`. Visible to MGR only.

### Count Type Definitions
- **Full Count:** All active items at one store; typically done once or twice yearly; longest run time
- **Department Count:** All items in a single department (e.g., Tropicals, Hardscape); monthly cadence in most stores
- **Spot Count:** Selected items only; LP-initiated (e.g., after a shrink alert fires on a specific SKU)

**Empty state:** "No physical counts in the selected period. Click 'New Count' to schedule a count."

## Interaction Flows

1. **Morning count check:** MGR opens count list → filters to Status = In Progress → sees count is 75% complete → opens count to monitor entry progress
2. **Post a completed count:** MGR sees a Completed count → clicks to open → navigates to `/inventory/count/:id/post` to review and post variances
3. **LP spot count audit:** LP notices high return rate on item #7734 → initiates Spot Count for that SKU via New Count → result shows 3 units missing vs perpetual ledger

## UX Callout

CP's physical count module (`frmimphysicalcount`) requires a PC terminal at the counting location — counters write tally sheets by hand, then a manager keys them into CP. Canary's count list is the management view of a mobile-first counting process: counters use their phones at the shelf, and the progress column reflects their work in real time. A manager watching 47/120 lines complete knows exactly how far the team has gotten without walking the floor.

## Navigation Exits

- `/inventory/count/new` — initiate new count
- `/inventory/count/:id` — count entry/detail
- `/inventory/count/:id/post` — post a completed count

## Open Questions

None.
