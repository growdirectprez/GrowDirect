---
screen: /transfers/:id/variance
title: Transfer Variance Review
role: LP | MGR
wave: W2
origin: O
cp_equivalent: "None — variance resolution is entirely manual in CP"
---

# Transfer Variance Review

**URL:** `/transfers/:id/variance`  
**Primary role:** LP; MGR  
**Entry points:** Transfer list (Variance-Flagged row); LP alert → link; transfer receipt → auto-redirected when variance exceeds threshold

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Variance Review: Transfer #[id] — From [Store] → To [Store]", variance amount ($) | |
| Pattern alert (conditional) | "Note: This transfer route has had [N] variance events in the past 60 days" | Appears if repeat variance pattern detected |
| Main content | Variance table | Per-line breakdown |
| Case link section | Link to existing case or create new case | Below variance table |
| Action bar | Set Disposition per line, Request Approval, Approve Write-Off | |

## Key Elements

### Variance Table
Columns: Item #, Description, Shipped Qty, Received Qty, Variance Qty, Variance Value ($), Disposition selector (Damage / Carrier Loss / Internal Shrink / Receiving Error).

Disposition is set per line. Each disposition has different downstream behavior:
- **Damage:** MGR writes off; inventory adjustment created; no LP case needed unless pattern
- **Carrier Loss:** Insurance claim workflow; ADM documents; no immediate LP case
- **Internal Shrink:** LP case creation strongly recommended; system flags for investigation
- **Receiving Error:** Qty correction initiated; inventory adjustment created; no LP case

### Pattern Alert (conditional)
Appears when this transfer route (Store A → Store B) has had variance events > 1 in 60 days. "This is the 3rd variance event on this route in 60 days. Consider opening a cross-case investigation." Links to `/cases/hawk/patterns` pre-filtered to this route.

### Case Link Section
"Link this variance to an existing case" (search) or "Create new case with this variance as seed evidence." If creating: variance record becomes the first evidence item on the new case, pre-sealed.

### Write-Off Approval
For Damage and Carrier Loss dispositions within MGR authorization limit: MGR can approve the write-off directly. For amounts exceeding the authorization limit (configurable): "Approval required from LP Manager." Status: Pending Approval.

**Empty state:** Not applicable — variance exists before reaching this screen.

## Interaction Flows

1. **Routine damage write-off:** LP reviews variance → 2-unit variance on fragile pots → disposition = Damage → MGR approves write-off within authorization limit → inventory adjusted → no LP case
2. **Internal shrink investigation:** LP sees 12-unit variance → pattern alert shows 3rd variance this route → disposition = Internal Shrink for 10 units → LP creates case with variance as seed evidence → case routed to same investigator handling the route
3. **Receiving error correction:** RCV discovers they entered 18 instead of 20 in the receipt form → variance = −2 → disposition = Receiving Error → system creates a corrective inventory adjustment → no LP case; error documented

## UX Callout

In CP, a variance discovered at transfer receipt is a paper note on the receiving dock, a phone call to the store manager, and maybe an email to LP — all manual, all delayed, all undocumented. Canary's variance review screen is the automatic response to the receipt event. LP doesn't need to be told; the alert and this screen exist the moment the RCV clicks Confirm Receipt with a variance. The pattern alert (repeat variance on this route) is the cross-transfer intelligence that no individual alert surface can provide — it's only visible by aggregating multiple transfer records, which Canary does automatically.

## Navigation Exits

- `/transfers` — back to transfer list
- `/cases/hawk/:id` — case created from this variance
- `/cases/hawk/patterns` — from pattern alert link

## Open Questions

None.
