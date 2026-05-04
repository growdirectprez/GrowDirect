---
screen: /settings/allowlist/dead-count
title: Allow-List — Dead Count
role: ADM
wave: W1
origin: O
cp_equivalent: "None — CP security codes control what operators can do; allow-lists control what Canary won't alert on"
---

# Allow-List — Dead Count

**URL:** `/settings/allowlist/dead-count`  
**Primary role:** ADM  
**Entry points:** Settings nav → Allow-Lists → Dead Count; alert detail → "Update allow-list" link; rule detail allow-list summary

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Allow-List: Dead Count", Add Entry button | |
| Context panel | What "dead count" means + which rule this allow-list feeds | Brief description above table |
| Main content | Allow-list entries table | |

## Key Elements

### Context Panel
Brief, non-technical explanation of this allow-list's purpose: "Dead count occurs when a cashier opens a drawer without processing a transaction (e.g., to make change for a non-customer). This allow-list pre-approves specific cashier/store patterns so Canary does not generate alerts when the pattern is a known business practice."

Rule fed: Q-DC-01 Dead Count Detection.

### Allow-List Entries Table
Columns: Cashier Name / ID, Store, Threshold Override (max dead count events per shift — null = unlimited), Date Range (start–end; blank end = indefinite), Added By, Reason (free text), Active (toggle). 

Rows sortable by store, cashier, expiry date.

**Empty state:** "No allow-list entries. Add entries to pre-approve specific cashier/store patterns that would otherwise generate dead-count alerts."

### Add Entry Form (opens on "Add Entry")
Fields:
- Cashier (search-as-you-type user lookup, or "All cashiers at this store")
- Store
- Threshold override (blank = suppress all alerts for this cashier/store combination)
- Date range (start, optional end — if no end, entry is indefinite and displays a warning: "Indefinite entries should be reviewed periodically")
- Reason (required — minimum 20 characters)

On save: entry activates immediately. If a rule was recently suppressed by an allow-list but LP investigator saw the alert anyway (race condition during entry creation), a brief note appears: "Note: there may be a delay of up to 60 seconds before this entry takes effect."

### Deactivation
Toggle per row. Deactivated entries are greyed but retained (audit trail). They can be reactivated. Deleted entries are soft-deleted — visible in "Show deactivated" toggle.

## Interaction Flows

1. **Pre-approve change-making behavior:** ADM learns that Store 3's front-of-house cashier routinely opens the drawer to make change for non-transaction scenarios (café-adjacent setup) → adds allow-list entry: Cashier = J. Martinez, Store = Store 3, reason = "Front register makes change for café; CP config confirms authorized" → saves → dead-count alerts for this cashier/store suppressed
2. **Investigate a suppressed alert:** LP receives alert that "should have been suppressed" → checks allow-list → finds entry for this cashier has expired (end date = last week) → adds new entry with updated date range
3. **Review indefinite entries:** ADM runs periodic review → filters table to entries with no end date → reviews each one → deactivates entries that are no longer valid

## UX Callout

Counterpoint's security codes control what operators *can do* at the POS — they restrict POS functions. Canary allow-lists control what Canary *won't alert on* — they encode institutional knowledge about legitimate exceptions. These are complementary, not redundant. The allow-list is Canary's memory of "we know about this pattern; it's fine." Without allow-lists, LP teams manually acknowledge the same false-positive alerts every day, degrading investigator trust in the system. The require-a-reason constraint is intentional: allow-list entries should be explainable, not just expedient.

## Navigation Exits

- `/settings/allowlist/discounts` — next allow-list screen
- `/rules/:id` (Q-DC-01) — rule this allow-list feeds
- `/alerts` — filtered to dead-count alerts, to see what this allow-list is suppressing

---

**Pattern note:** The three remaining allow-list screens (`/settings/allowlist/discounts`, `/settings/allowlist/voids`, `/settings/allowlist/comps`) inherit this layout and interaction pattern exactly. Each has a different context panel explanation, a different key field in the entry form, and routes to a different rule. Differences are documented in their individual briefs.

## Open Questions

None.
