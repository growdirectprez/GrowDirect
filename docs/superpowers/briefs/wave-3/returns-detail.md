---
screen: /returns/:id
title: Return Detail
role: MGR | LP
wave: W3
origin: O
cp_equivalent: "None — CP has no return detail record; returns exist only as negative-value transactions"
---

# Return Detail

**URL:** `/returns/:id`  
**Primary role:** MGR; LP  
**Entry points:** Returns list row; alert detail → return evidence link; customer detail → returns tab

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Return ID, status badge, date, store | Breadcrumb back to /returns |
| Top section | Return summary + original transaction link | |
| Main content | Return line items | |
| Evidence panel | Hash seal status + alert linkage | |
| Action bar | Approve Return, Flag for LP, Override (MGR) | Status-dependent |

## Key Elements

### Return Summary
Return date/time, cashier, customer (if loyalty account), return value, reason code (customer-stated), store, processing terminal (station ID).

**Original transaction link:** Every return in Canary is linked to the originating sale transaction. "Return of Transaction #T-0882, sold 2026-04-12." Clicking navigates to `/transactions/:id` for the original sale. LP can verify the original sale before deciding to approve or flag the return.

If no original transaction is linked (return without receipt — return-without-receipt is a higher-risk return pattern): "No original transaction on file. Customer returned without receipt." Status defaults to Pending Review.

### Return Line Items
Table: Item #, Description, Qty Returned, Unit Price, Return Value, Condition (Saleable / Damaged / As-Is). Condition determines how the returned item is handled in inventory: Saleable returns go back to inventory; Damaged returns trigger an inventory adjustment for the damaged quantity.

### Evidence Panel
Hash seal status: the return event is hash-sealed like all transaction events in Canary. "Return record sealed — hash verified." Tampering indicator if the record has been altered.

Alert linkage: if a detection rule fired on this return, the linked alert appears here with its status (Open / Closed / Dismissed). LP can see the alert context without leaving the return record.

### Approve / Flag Actions
- **Approve:** Marks return Approved; inventory adjusted per line conditions; refund method confirmed.
- **Flag for LP:** Opens the LP alert creation flow pre-populated with the return as seed evidence.
- **Override (MGR):** For Pending Review returns — MGR can approve outside normal parameters with a reason logged. Override is audited.

**Empty state:** Not applicable — return exists before this screen.

## Interaction Flows

1. **Legitimate return approval:** MGR opens return → checks original transaction → 4-day-old sale, items in saleable condition → approves → inventory updated → no LP action
2. **LP escalation:** Return without receipt on a $180 item → MGR opens detail → no original transaction → flags for LP → alert created with return as evidence → LP investigator takes over
3. **Evidence attach:** LP has open case → finds return detail matches pattern in case → uses evidence panel to link return to existing case directly from return detail

## UX Callout

CP returns are negative transactions — there is no return record type. An LP investigator seeing a flagged return pattern in Canary has a complete record to work with: the return event (sealed with hash), the original transaction it was tied to, the cashier, the reason code, and the alert that fired. None of this exists in CP as a coherent record — it would need to be assembled manually from transaction reports and phone calls. The return-without-receipt indicator is the highest-signal field on this screen from an LP perspective: a customer who returns without a receipt has no provable purchase, and that's the most common setup for return fraud.

## Navigation Exits

- `/returns` — back to returns list
- `/transactions/:id` — original sale
- `/alerts/list` — from alert linkage
- `/cases/hawk/:id` — from evidence panel case link
- `/customers/:id` — from customer link

## Open Questions

None.
