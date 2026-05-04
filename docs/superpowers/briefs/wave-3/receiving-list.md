---
screen: /receiving
title: Receiving Queue
role: RCV | MGR
wave: W3
origin: N
cp_equivalent: "None — CP has no dedicated receiving queue; receiving is accessed by opening POs individually"
---

# Receiving Queue

**URL:** `/receiving`  
**Primary role:** RCV; MGR  
**Entry points:** Primary sidebar nav (Purchasing section → Receiving)

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Receiving Queue", store selector | Defaults to current user's store |
| Filter bar | Status (Expected Today / In Transit / Overdue), Vendor | |
| Main content | Inbound queue table | |

## Key Elements

### Inbound Queue Table
Columns: PO #, Vendor, Expected Date, Items (line count), Remaining Units, Status (Expected / Overdue / Partially Received / Received), Action.

**Expected Today filter:** Default view on open. Shows only POs with Expected Date = today (and any overdue POs not yet received). This is the morning dock checklist — RCV opens the receiving queue to see what's arriving today.

**Remaining Units:** Total units still expected across all open lines on this PO. Helps RCV plan dock space and labor for incoming deliveries.

**Overdue rows:** POs where Expected Date has passed and status is not Received. Orange tint + "Overdue" badge. Same pattern as transfer overdue.

**Action column:** "Start Receiving" button → navigates to `/orders/:id/receive`. Only appears for Expected / Overdue / Partially Received rows.

### No Active Inbound State
If there are no POs expected today and no overdue POs: "Nothing expected today. Check the full PO list for upcoming deliveries." Link to `/orders`.

**Empty state (no POs at all):** "No active inbound POs for [Store]. Purchase orders will appear here when submitted."

## Interaction Flows

1. **Morning dock setup:** RCV opens receiving queue → Expected Today shows 2 POs → reviews Remaining Units to gauge volume → prepares dock accordingly → as trucks arrive, clicks Start Receiving for each
2. **Overdue follow-up:** MGR opens receiving queue → 1 overdue PO from 3 days ago → clicks through to PO detail → calls vendor account rep → logs note in PO action log
3. **Afternoon partial:** RCV receives first drop of a large PO → clicks Start Receiving → enters partial quantities → confirms → queue shows PO now in Partially Received status → reappears in queue for next delivery

## UX Callout

CP has no receiving queue. A receiving clerk uses CP by opening the PO module, searching for the relevant PO, and opening it from a list of all purchase orders. If three deliveries are expected today, the clerk needs to know the PO numbers in advance or search by vendor name — neither is a reliable workflow for a busy dock. Canary's receiving queue is today-scoped by default: the answer to "what's arriving today?" is a single screen open, not a search query across all historical POs. The overdue indicator serves the same function as the overdue transfer toggle — surfacing vendor delivery failures before they become stockout events.

## Navigation Exits

- `/orders/:id/receive` — start receiving a specific PO
- `/orders/:id` — PO detail
- `/orders` — full PO list

## Open Questions

None.
