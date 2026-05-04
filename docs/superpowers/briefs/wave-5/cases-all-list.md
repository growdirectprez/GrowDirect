---
screen: /cases/all
title: All Cases (Cross-Domain)
role: LP | MGR | ADM
wave: W5
origin: N
cp_equivalent: "None — CP has no case management system"
---

# All Cases (Cross-Domain)

**URL:** `/cases/all`  
**Primary role:** LP; MGR; ADM  
**Entry points:** Primary sidebar nav (Cases section); home dashboard active cases widget

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Cases", New Case button, case type filter tabs | Tabs: All / Hawk (LP) / B2B / Compliance / Vendor / Other |
| Filter bar | Status, Store, Assigned To, Date opened, Priority | |
| Main content | Cases table | |

## Key Elements

### Case Type Tabs
- **Hawk:** LP investigation cases — the W1 `/cases/hawk` list, accessible from here as well
- **B2B:** Account-level anomalies routed from the B2B alert class. Separate from LP fraud cases — B2B anomalies may involve commercial disputes, account misuse, or pricing errors rather than internal theft.
- **Compliance:** Regulatory compliance tracking (e.g., food-handling incidents, employee compliance events). May not apply to all verticals.
- **Vendor:** Vendor-related disputes, delivery issues, quality claims requiring formal tracking.
- **Other:** Catch-all for cases that don't fit standard types.

**Why cross-domain cases in W5:** The Hawk case system (W1) handles LP fraud. By W5, the operator has seen enough platform value to run formal case management across other business domains. A vendor dispute that generates a formal case record, with evidence and notes and a resolution workflow, is handled by the same case infrastructure as an LP investigation — the case type determines the workflow, not the underlying system.

### Cases Table (All Types)
Columns: Case #, Type badge, Subject/Topic, Store, Assigned To, Status, Priority, Opened Date, Days Open, Evidence Count, Last Activity.

**Days Open color-coding:** Same as Hawk case list — < 7 grey, 7-14 yellow, > 14 red.

**Evidence Count:** How many evidence items are attached. A case with 12 pieces of evidence is further along than one with 2; the count gives progress context at the list level.

**Empty state:** "No cases for the selected filters."

## Interaction Flows

1. **LP weekly review:** LP opens All Cases → filters Type = Hawk → same as `/cases/hawk` list — no duplication, same data
2. **Vendor dispute management:** Buyer opens vendor detail → creates a Vendor case for a short-shipment dispute → attaches the PO, receiving record, and vendor communication as evidence → case is tracked until vendor credits or ships the missing units
3. **B2B anomaly review:** ADM opens All Cases → filters Type = B2B → 3 B2B cases from the past 30 days → reviews each: 2 resolved, 1 escalated to legal → opens the escalated case to review evidence

## UX Callout

The Hawk case system is the LP-specific instance of a general case management capability. In W5, the platform extends case management to other domains because the operator has seen that structured investigation workflows — evidence attachment, status tracking, notes, resolution records — are useful beyond LP. A vendor dispute handled as a formal case rather than an email chain has an evidence record, a clear owner, and a resolution date. The B2B alert class routing (from W1's Alert Routing settings) feeds directly into B2B cases in this view. The infrastructure is the same; the workflows and resolution types differ by case type.

## Navigation Exits

- `/cases/hawk` — direct Hawk-filtered view (W1 nav entry remains)
- `/cases/all/:id` — case detail
- `/cases/hawk/analytics` — LP-specific analytics from W1

## Open Questions

None.
