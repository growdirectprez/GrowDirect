---
screen: /transactions
title: Transaction List
role: LP | MGR
wave: W2
origin: O
cp_equivalent: "frmpstickethistory — no hash status, no case-link, no discount filter"
---

# Transaction List

**URL:** `/transactions`  
**Primary role:** LP; MGR  
**Entry points:** Primary sidebar nav (Surveillance section); chirp feed → "View in transactions"; alert detail → transaction link

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Transactions", Export button | Export applies current filters |
| Filter bar | Store, Date range, Transaction type, Cashier, Terminal, Amount range, Has-discount flag | Multi-select where applicable; Has-discount is a single toggle |
| Main content | Paginated transaction table | Primary working surface; 50 rows per page default |

## Key Elements

### Transaction Table
Columns: Ticket #, Type badge (SALE / RETURN / VOID / LAYAWAY — color-coded), Store, Terminal, Cashier, Customer (name if linked, blank if anonymous), Item Count, Subtotal, Discount Total, Tax, Total, Tender Type (primary tender), Timestamp.

Sortable by: Ticket #, Timestamp, Total (amount), Cashier. Default sort: most recent first.

Rows link to `/transactions/:id`. Hash seal status is NOT shown in the list — that's a detail-level feature. The list is for finding and filtering; the detail is for investigation.

**Empty state:** "No transactions match the current filters." For stores not yet sending data: "No transactions received from [Store] — data ingestion may not be configured."

### Has-Discount Filter
Single-click toggle. When enabled: table shows only transactions where discount_total > 0. The single most useful LP filter after date range — in CP, this requires running a Price Exceptions report as a separate step. Here it's one toggle.

### Amount Range Filter
Min and max dollar inputs. Useful for: "show me all transactions between $200–$500 this week" (looking for high-value anomalies) or "show me all transactions under $1 this month" (looking for test/void artifacts).

### Export
Exports the full filtered result set as CSV. Includes all columns. Used by LP for offline analysis, by MGR for reporting to accounting.

## Interaction Flows

1. **End-of-day audit:** MGR filters to Store = their store, Date = today, Type = all → reviews all transactions → sorts by Total descending → spot-checks top 10 high-value transactions
2. **Cashier investigation:** LP investigating a specific cashier → filters to Cashier = J. Martinez, Date range = last 30 days, Has-discount = ON → sees all discounted transactions → exports for offline analysis → identifies a pattern
3. **Find specific ticket:** LP has ticket number from an alert → types ticket # into search (if search is available on this screen) or navigates to `/transactions/:id` directly

## UX Callout

The "has-discount" toggle is the design decision that most directly improves LP's daily workflow compared to CP. In CP, pulling all discounted transactions for a cashier requires: running Price Exceptions report, filtering by cashier, printing/exporting, cross-referencing with ticket history. In Canary: filter bar → toggle Has-discount → filter Cashier → done. One filter, not a three-step report pipeline. The hash-seal column is deliberately excluded from this list view — it's investigative-depth information that belongs in the detail, not a filter criterion.

## Navigation Exits

- `/transactions/:id` — transaction detail for any row
- `/transactions/:id/proof` — via detail view
- `/cases/hawk` — if LP opens a case from pattern discovered in this list

## Open Questions

None.
