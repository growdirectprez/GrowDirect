---
screen: /transactions/:id
title: Transaction Detail
role: LP | MGR
wave: W2
origin: O
cp_equivalent: "Ticket History detail — no hash, no rule overlay, no case link"
---

# Transaction Detail

**URL:** `/transactions/:id`  
**Primary role:** LP; MGR  
**Entry points:** Transaction list row; chirp detail; alert detail

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Ticket #, store, terminal, cashier, date/time, status | Breadcrumb back to /transactions |
| Top panel | Hash seal status — full-width prominent banner | Same as /chirps/:id — green verified / red tampered |
| Left column (65%) | Line items table + tender section + totals | Complete ticket record |
| Right column (35%) | Rules evaluated panel + customer card | Investigation context |
| Action bar | Link to Case, View Audit Proof, View Customer, Export PDF, View Cashier Profile | Bottom |

## Key Elements

### Hash Seal Status (Top Panel)
Identical to `/chirps/:id`. Green: "Transaction record verified — not modified since ingestion." Red: "ALERT: Record does not match original hash." Red state is an LP event requiring immediate case creation.

### Line Items Table
Every line item: Item #, Description, Quantity, Unit Price, Discount Amount, Discount Reason Code, Extended Price. Subtotal row. Discount Total row (sum of all discount amounts). Tax row. Total row.

Complete, not summarized. This is a legal-quality transaction record — every field that CP would show on a ticket is here, plus the discount breakdown per line item (which CP's ticket history doesn't decompose per-line).

### Tender Section
Every tender line: Tender Type, Amount, Change Given. Multi-tender transactions show all tender lines. Total tender row = total paid.

### Rules Evaluated Panel
Same as `/chirps/:id` — list of every detection rule that evaluated this transaction, with outcome (Pass / Fire / Dry-run). Fires link to `/alerts/:id`. This panel answers "why did this transaction generate an alert?" and "why didn't it trigger a rule I expected?"

### Customer Card (conditional)
Appears if transaction is customer-linked. Name, loyalty number, risk score badge (linked to customer detail). MGR can navigate to customer account from here to handle a return or loyalty question.

## Interaction Flows

1. **Full transaction investigation:** LP opening transaction from an alert → reads all line items → identifies the specific discount line that triggered the rule → checks discount reason code → cross-references with allow-list (if rule fired unexpectedly on an allow-listed pattern) → decides to link to case or acknowledge
2. **End-of-day check:** MGR reviews a specific high-value transaction flagged by a colleague → verifies line items add up, tender is correct, no anomalous discounts → satisfied, no action needed
3. **Attach to case:** LP views transaction → confirms it's relevant to an open investigation → clicks "Link to Case" → evidence sealing flow begins → transaction attached to case timeline

## UX Callout

The discount breakdown per line item (not just a total discount) is the investigative improvement over CP's ticket history. CP shows total discount on the ticket but not which line item received which discount at which reason code. Canary's per-line discount column means LP can see "Item #4721 received a $23 discount at reason code MO (Manager Override)" without running a separate Price Exceptions report. Combined with the hash seal and rules evaluated panel, the transaction detail becomes an active investigative tool rather than a passive receipt viewer.

## Navigation Exits

- `/transactions` — back to transaction list
- `/transactions/:id/proof` — audit proof certificate (from Action bar)
- `/cases/hawk/:id` — case linked from evidence attach action
- `/customers/:id` — from customer card
- `/alerts/:id` — from rules evaluated panel

## Open Questions

None.
