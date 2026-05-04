---
screen: /customers/:id → Context tab
title: Customer Cross-Module Context
role: LP
wave: W1
origin: O
cp_equivalent: "None"
---

# Customer Cross-Module Context (Tab on Customer Detail)

**URL:** `/customers/:id` → Context tab  
**Primary role:** LP  
**Entry points:** Customer detail → Context tab

**Note:** Tab renders within `/customers/:id`. Parent header remains visible.

## Layout

| Zone | Content | Notes |
|---|---|---|
| Tab content top | Summary panel — three KPI tiles | Full-width |
| Left section | Cases as subject list | ~50% width |
| Right section | Cashier co-occurrence table | ~50% width |
| Bottom section | Evidence appearances (which cases contain this customer's transactions as evidence) | Full-width |

## Key Elements

### Summary Panel (Three KPI Tiles)
1. **Cases as Subject:** N — count of cases where this customer is the named investigation subject. Links to case list filtered to this customer.
2. **Transactions as Evidence:** M — count of this customer's transactions that have been attached to any case as evidence (across all cases, not just theirs). Indicates how frequently this customer's transactions are being investigated.
3. **Stores Transacted At:** K — distinct store count. LP signal: a customer active at many stores has wider exposure.

### Cases as Subject List
All cases where this customer is a named subject. Columns: Case ID, case type, status badge, opened date, assigned investigator. Rows link to `/cases/hawk/:id`.

**Empty state:** "This customer has not been the subject of any investigation." — affirmatively useful for the innocence-check scenario.

### Cashier Co-Occurrence Table
LP-specific collusion detection surface. Columns: Cashier Name, Transaction Count (how many transactions involve this customer AND this cashier), Alert Overlap (how many alerts from those transactions involve this cashier), Alert Rate (alerts / transactions — unusually high = signal). Sorted by Transaction Count descending.

The co-occurrence signal: if customer X has transacted with cashier Y 47 times and 12 of those transactions triggered alerts, that's a meaningful pattern. If the same customer has transacted with 30 different cashiers and the alert rate is uniform, the pattern suggests the customer, not the cashier.

**Empty state:** "No cashier co-occurrence data available for this customer."

### Evidence Appearances
A table showing cases (beyond this customer's own cases) that contain this customer's transactions as attached evidence. E.g., "Your transaction #99221 was attached to Case CW-0041 (Cashier J. Martinez — Discount Fraud)." Shows LP the full network of how this customer's activity has been used in investigations.

## Interaction Flows

1. **Innocence check:** LP investigating an alert linked to customer B → opens Context tab → Cases as Subject: 0, Transactions as Evidence: 0 → LP notes in alert disposition: "Customer cleared — no LP history"
2. **Identify collusion:** LP opens Context tab → cashier co-occurrence shows this customer's transactions with Cashier J. Martinez have a 34% alert rate vs 3% with all other cashiers → LP notes this as a collusion signal → opens `/cases/hawk/patterns` to see the full subject graph
3. **Track multi-case customer:** MGR notices a customer who is the subject of 3 open cases across 2 stores → opens Context tab → confirms cases are independent (not cross-related) → escalates to LP manager for coordinated investigation

## UX Callout

Cashier co-occurrence — this customer appears disproportionately with this specific cashier AND those transactions have high alert rates — is a collusion detection signal that no existing retail LP system surfaces automatically. In CP shops, this pattern would be discovered only if an LP investigator happened to be reviewing alerts from both the customer and the cashier simultaneously and manually noticed the overlap. Canary surfaces it in a single table view, ranked by statistical significance. The innocence-check use case (Cases as Subject = 0) is equally important and equally invisible in CP — LP investigators currently have no fast way to confirm a customer has never been investigated.

## Navigation Exits

- `/customers/:id` — parent tab bar
- `/cases/hawk/:id` — from cases as subject list
- `/cases/hawk/patterns` — to see full subject graph including this customer

## Open Questions

None.
