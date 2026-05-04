---
screen: /customers/:id — AR Tab
title: Customer Accounts Receivable
role: MGR | ADM
wave: W3
origin: O
cp_equivalent: "AR customer screen in CP — no aging visualization, no LP context for outstanding balances"
---

# Customer Accounts Receivable

**URL:** `/customers/:id` (AR tab)  
**Primary role:** MGR; ADM  
**Entry points:** Customer detail → AR tab

## Layout

This tab renders within `/customers/:id`. The parent header (customer name, ID, risk score badge, KPI row, tab bar) persists. This brief covers the AR tab content only.

| Zone | Content | Notes |
|---|---|---|
| Tab content | AR summary KPIs | |
| Section 1 | Open balance + aging | |
| Section 2 | AR transaction history | |
| Action bar | Record Payment, Apply Credit, Generate Statement | |

## Key Elements

### AR Summary KPIs
- **Total Open Balance ($):** Current AR balance
- **Current (0-30 days) ($)**
- **Past Due 31-60 days ($)**
- **Past Due 61-90 days ($)**
- **Past Due 90+ days ($)**
- **Credit Limit ($):** Configured in customer profile
- **Available Credit ($):** Credit Limit − Open Balance

**Aging color-coding:** Current = green, 31-60 = yellow, 61-90 = orange, 90+ = red. AR aging visualization at a glance without needing to parse numbers.

### AR Transaction History
Table: Date, Invoice #, Description (sale or return), Charges ($), Credits ($), Running Balance ($), Days Outstanding.

Standard AR ledger view. Sorted by date descending. Filtering by status (Open / Paid / Disputed) reduces to the subset of interest.

### LP Context on AR
Outstanding balances and AR history have LP relevance: a customer with a large AR balance who is also a return fraud suspect may be using the AR account to obscure the return/refund cycle. The risk score badge in the parent header (always visible) keeps the LP signal in view even when MGR is looking at AR.

### Record Payment
MGR records a customer payment against open invoices. Payment amount, payment method, applied invoices. This reduces the open balance and generates a credit in the AR transaction history. Payments are logged with the user and timestamp.

### Apply Credit
MGR applies an existing credit (from a return or price adjustment) against the AR balance. Reduces open balance.

### Generate Statement
Generates a printable or emailable AR statement for the customer. Standard format: aging summary + transaction history. Used for collection conversations or B2B account reviews.

**Empty state:** "No AR balance or history for this customer. AR activity will appear here when charge sales or credits are posted."

## Interaction Flows

1. **Payment collection call:** MGR opens AR tab → customer has $420 outstanding, 45 days past due → generates statement → calls customer → records $420 payment → balance clears
2. **Credit limit check:** Salesperson asks MGR whether customer can charge another purchase → MGR opens AR tab → Available Credit = $40 (nearly at limit) → declines new charge or escalates for approval
3. **LP-AR cross-check:** LP investigating return fraud suspect → opens AR tab → customer has $0 outstanding balance despite 8 recent charge sales → all charges paid immediately with credits → LP notes: customer is using returns to systematically zero-out their AR

## UX Callout

AR in CP is a separate module with its own customer screen. The integration between the customer's LP risk profile and their AR history doesn't exist — they're separate records in separate modules. Canary keeps the AR tab in the same customer record as the risk profile and commercial data. The three-way view (commercial value + AR health + LP risk) is available in a single session without navigating between modules. For a business owner who is also the manager and the AR collector and sometimes the LP investigator, this is the operational reality: everything about a customer should be in one place.

## Navigation Exits

- `/customers/:id` — back to customer overview

## Open Questions

None.
