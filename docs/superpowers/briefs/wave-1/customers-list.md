---
screen: /customers
title: Customer Lookup (Investigator)
role: LP
wave: W1
origin: O
cp_equivalent: "frmcustomers — full form but no risk score, no case context"
---

# Customer Lookup (Investigator)

**URL:** `/customers`  
**Primary role:** LP  
**Entry points:** Primary sidebar nav (Customers section); alert detail → customer name link; case detail → subject search

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Customers", search bar | Search is prominent — this screen is primarily a search entry point |
| Filter bar | Risk band (High / Medium / Low / None), Case Status (has open cases / no cases), Store affinity | Secondary filter controls |
| Main content | Search results table | Empty until search is performed |

## Key Elements

### Search Bar
Prominent, centered, full-width. Searches: customer name (partial match), email, phone number, loyalty number. Minimum 3 characters to trigger search. Results appear instantly as user types.

**Empty state (pre-search):** "Search by name, email, phone, or loyalty number to find a customer." — not a table of all customers. This screen is a search surface, not a browse surface.
**No results:** "No customers match '[search term]'. Try a partial name or check spelling."

### Search Results Table
Columns: Name, Loyalty #, Risk Score badge (0–100, color-coded: 0–30 = grey/None, 31–60 = yellow/Medium, 61–80 = orange/High, 81–100 = red/Critical), Case Count (integer, linked to their cases), Last Transaction (date), Primary Store. Rows link to `/customers/:id`.

Risk score and case count are in the search results — not buried in the detail. The investigator's first question is "does this customer have a risk signal?" before opening a full profile.

### Risk Band Filter
Allows LP to browse customers by risk level without a specific person in mind. Use case: LP reviewing the high-risk customer list at the start of a shift to see if any high-risk customers transacted recently.

## Interaction Flows

1. **Find customer from alert:** LP investigating an alert linked to customer "Sarah T." → searches "Sarah T" → sees 1 result with Risk Score = 73 (High) and Case Count = 2 → clicks through to customer detail
2. **Browse high-risk customers:** LP applies Risk Band = High filter → sees all customers with risk score > 60 → sorts by Last Transaction → identifies a high-risk customer who transacted yesterday → opens their profile to review
3. **Verify customer innocence:** LP investigating a void → transaction was customer-linked → searches customer → sees Risk Score = 4 (None), Case Count = 0 → notes in alert: "Customer cleared, no LP history"

## UX Callout

The investigator view of a customer is fundamentally different from the operator view. CP's `frmcustomers` shows addresses, credit terms, and account status — useful for the MGR handling a return, not useful for an LP investigator. Canary's customer lookup surfaces risk score and case history in the search results, before the investigator opens a record. The design decision to make this a search-first screen (not a full customer list) reflects how LP investigators actually work: they have a specific person in mind, find them fast, and confirm their risk context.

## Navigation Exits

- `/customers/:id` — customer detail for any result row

## Open Questions

None.
