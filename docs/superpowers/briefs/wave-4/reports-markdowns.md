---
screen: /reports/markdowns
title: Markdown Report
role: BYR | MGR
wave: W4
origin: N
cp_equivalent: "None — CP has no markdown tracking; price changes are overwrite events with no history"
---

# Markdown Report

**URL:** `/reports/markdowns`  
**Primary role:** BYR; MGR  
**Entry points:** Primary sidebar nav (Reports section → Merchandising); markdown queue → view completed

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Markdown Report", date range selector, store selector | |
| Filter bar | Category, Status (Active / Completed / All), Urgency | |
| Main content | Markdown performance table | |

## Key Elements

### Markdown Performance Table
Columns: Item #, Description, Category, Store, Original Price, Markdown Price, Markdown %, Markdown Date, Units Sold Before Markdown, Units Sold Since Markdown, Sell-Through Before (%), Sell-Through Since (%), Remaining On Hand, Status (Active / Cleared / Partially Cleared).

**Sell-Through Before vs After:** The core markdown effectiveness metric. If sell-through was 8% before the markdown and is 35% after — the markdown worked. If sell-through is 10% before and 11% after — the markdown didn't move the needle; a deeper markdown or different action is needed.

**Status values:**
- **Active:** Markdown is currently applied; item still has unsold inventory
- **Cleared:** Item sold through to zero (or near-zero) on-hand
- **Partially Cleared:** On-hand reduced but not zero; sell-through has improved but clearance incomplete

**Remaining On Hand:** Current inventory. For BYR: how much is still left to clear? If sell-through improvement stalled at 40% with 60 units remaining, a second markdown may be warranted.

**Empty state:** "No markdown history for the selected period."

## Interaction Flows

1. **End-of-season clearance review:** BYR opens markdown report → all Active markdowns → sorted by Sell-Through Since ascending → 3 items under 25% sell-through despite markdown → these items need deeper markdowns or redistribution
2. **Success analysis:** BYR reviews Cleared markdowns → identifies 4 items that cleared within 2 weeks of markdown → these items respond well to price reductions — notes for future planning
3. **Partial clearance action:** BYR sees item with 45 units remaining and stalled sell-through → creates distribution recommendation to move excess to higher-velocity stores → or creates a second markdown

## UX Callout

The before/after sell-through comparison is the analytical element that converts a markdown from a tactical decision into a measured intervention. In CP, a price change happens and the effect is unknowable from the system — you'd have to compare sales reports before and after, manually attribute the change to the price reduction, and do the arithmetic in Excel. Canary tracks each markdown as an event with a start date, so the before-and-after is automatically computed. The markdown lifecycle closes: queue → approve → apply → measure → iterate. Each stage is supported by system data rather than manual effort.

## Navigation Exits

- `/markdowns` — back to markdown queue
- `/items/:id` — from item # column

## Open Questions

None.
