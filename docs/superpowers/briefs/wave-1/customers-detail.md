---
screen: /customers/:id
title: Customer Detail (Base Profile)
role: LP | MGR
wave: W1
origin: O
cp_equivalent: "frmcustomers — A/R + Ticket History tabs, no analytics overlay"
---

# Customer Detail

**URL:** `/customers/:id`  
**Primary role:** LP (investigator view); MGR (operator view)  
**Entry points:** Customer lookup; alert detail; case detail subject link

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Customer name, loyalty number, status badge (Active/Inactive), risk score badge | Persistent across all tabs |
| Tab bar | Overview · Risk · Context · Commercial (W3) · AR (W3) · Loyalty (W4) | Tabs render based on role and wave phase |
| Tab content | Active tab's content | Full-width below tab bar |
| Action bar | Open Case, Link to Case, Export Customer Report | Available to LP role |

## Key Elements

### Overview Tab (default)
**KPI Row:** Lifetime Spend ($), Average Transaction ($), Return Rate (%), Loyalty Balance (points). Four tiles — immediate context without scrolling.

**Transaction History Table:** Most recent 25 transactions (paginated). Columns: date, store, cashier, type (Sale/Return/Void), amount, loyalty points earned. Rows link to `/transactions/:id`. Filterable by store, date range, transaction type.

**Contact Information:** Name, email, phone, primary address. Read-only in LP view. MGR view has edit capability (not scoped here — edit functionality is a Wave 3+ feature per CP crosswalk).

### Risk Tab
See `/customers/:id` → Risk — dedicated brief.

### Context Tab
See `/customers/:id` → Context — dedicated brief.

### Commercial Tab (Wave 3)
See `/customers/:id` → Commercial — covered in Wave 3 brief group.

### AR Tab (Wave 3)
See `/customers/:id` → AR — covered in Wave 3 brief group.

### Loyalty Tab (Wave 4)
See `/customers/:id` → Loyalty — covered in Wave 4 brief group.

**Empty state (new customer, no transactions):** "No transaction history on file."
**Empty state (no loyalty enrollment):** Loyalty tab shows "Customer is not enrolled in any loyalty program. [Enroll]"

## Interaction Flows

1. **Full customer investigative review:** LP arrives from an alert → Overview tab loaded → reviews KPI row (high return rate = suspicious) → reviews recent transaction history → clicks to Risk tab → reviews contributing factors → clicks to Context tab → sees case involvement → opens case from action bar
2. **Manager handles return:** MGR navigates to customer from transaction lookup → Overview tab → confirms loyalty balance → verifies address for refund check → returns to POS with confidence
3. **Open case from context:** LP reviews Context tab → sees this customer has been in evidence on 2 prior cases → uses "Open Case" action to create a new investigation with this customer as the subject

## UX Callout

Canary surfaces investigator-relevant analytics (return rate, store affinity, risk indicators) that CP buries across multiple tabs with no cross-tab summary. The KPI row — lifetime spend, avg ticket, return rate, loyalty balance — answers the four questions an LP investigator or store manager asks before engaging with a customer record. CP requires navigating to separate tabs for each piece. The role-based tab visibility (Risk and Context tabs only for LP; Commercial and AR tabs for MGR) keeps each persona's view clean — the investigator doesn't see AR terms; the MGR doesn't see the risk score decomposition.

## Navigation Exits

- `/customers` — back to customer lookup
- `/customers/:id/risk` — Risk tab
- `/customers/:id/context` — Context tab
- `/transactions/:id` — from transaction history table
- `/cases/hawk/:id` — from "Open Case" or "Link to Case" action

## Open Questions

None.
