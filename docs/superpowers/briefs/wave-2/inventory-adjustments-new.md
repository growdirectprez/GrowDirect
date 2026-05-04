---
screen: /inventory/adjustments/new
title: Manual Inventory Adjustment
role: MGR
wave: W2
origin: N
cp_equivalent: "frmimphysicaladjust manual entry — Windows-only, no reason required, no approval workflow"
---

# Manual Inventory Adjustment

**URL:** `/inventory/adjustments/new`  
**Primary role:** MGR  
**Entry points:** Adjustments list → New Adjustment button; item detail → create adjustment action

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "New Manual Adjustment", Submit button | |
| Top section | Store + Item selector | Required first step |
| Main content | Adjustment form | |
| Right rail | Current on-hand + adjustment preview | Live update |
| Action bar | Submit Adjustment, Cancel | |

## Key Elements

### Store + Item Selector
Store dropdown (required) then item search (required — by item # or description with barcode scan support). Selecting both unlocks the adjustment form.

### Adjustment Form
- **Direction:** Increase / Decrease (toggle)
- **Quantity:** Integer input (positive value; direction handles sign). Validated: cannot decrease below zero on-hand.
- **Reason:** Required dropdown. Options:
  - Spoilage / Damage (in-store)
  - Vendor Shortfall (not yet returned)
  - Theft Write-off (confirmed by LP)
  - Data Entry Correction
  - Other (requires note)
- **Notes:** Free text. Required when Reason = Other. Optional (but encouraged) for all reasons.
- **Reference (optional):** Link to a case, alert, or purchase order. Provides audit trail connecting the adjustment to an investigative record.

### On-Hand Preview (Right Rail)
Shows current on-hand at selected store. As MGR enters the quantity and direction, a preview shows: "After this adjustment: [N] → [N ± qty]." Prevents errors like entering 50 when they meant 5.

### Approval Threshold
Adjustments exceeding a configurable value threshold (e.g., >$500) require LP Manager approval before applying. Status = Pending Approval. MGR submits; LP Manager sees the pending adjustment in the adjustments list (flagged) and approves or rejects.

Adjustments within the threshold apply immediately on Submit.

**Empty state:** Not applicable — create form.

## Interaction Flows

1. **Spoilage write-off:** MGR finds 6 units of drought-tolerant grass seed with damaged packaging → adjusts Store 1, item #44721, Decrease 6, Reason = Spoilage/Damage → notes "packaging torn in storage, not saleable" → Submit → on-hand decreases immediately
2. **LP-requested theft write-off:** LP closes case → requests MGR write off 3 confirmed missing units → MGR creates adjustment, Reason = Theft Write-off, Reference = Case #C-0091 → submit → adjustment record links back to case
3. **High-value adjustment pending approval:** MGR discovers $600 discrepancy after receiving → creates adjustment → threshold exceeded → status = Pending Approval → LP Manager reviews and approves

## UX Callout

CP's manual adjustment form has no required reason field and no approval workflow. Any user with adjustment permissions can change inventory by any amount with no documentation. Canary requires a reason, optionally a reference, and routes high-value adjustments through an approval step. The reason dropdown isn't bureaucracy — it's the signal that separates legitimate spoilage from unexplained shrink in the LP filter view. An adjustment entered as "Theft Write-off" with a case reference tells a complete operational story; the same adjustment entered with no reason tells LP nothing useful about what happened.

## Navigation Exits

- `/inventory/adjustments` — after submit or cancel
- `/cases/hawk/:id` — from reference field link

## Open Questions

None.
