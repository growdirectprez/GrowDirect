---
screen: /cases/all/:id
title: Case Detail (Cross-Domain)
role: LP | MGR | ADM
wave: W5
origin: N
cp_equivalent: "None — CP has no case management system"
---

# Case Detail (Cross-Domain)

**URL:** `/cases/all/:id`  
**Primary role:** LP; MGR; ADM  
**Entry points:** All-cases list row; exception detail → Create Case; LP pattern view

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Case #, type badge, status badge, priority | Breadcrumb back to /cases/all |
| Top section | Case summary (subject, type, date, assigned) | |
| Tab bar | Timeline / Evidence / Notes / Related | |
| Tab content | Tab-dependent | |
| Action bar | Advance Status, Reassign, Close Case, Archive | |

## Key Elements

### Case Summary
Case type, subject (employee, customer, vendor, or topic), opening event (exception, alert, manual creation), assigned investigator, store scope, priority, opened date.

**For Hawk cases:** Identical to `/cases/hawk/:id`. This is the same record — the cross-domain view is a superset that includes Hawk cases, not a separate record type.

**For B2B, Vendor, Compliance, Other:** The subject line is a topic or party rather than a specific individual (e.g., "Vendor: Greenfield Wholesale — PO #P-0309 short-shipment dispute" or "B2B: Account #BA-0044 unauthorized price level usage").

### Timeline Tab (CANONICAL — same as Hawk case detail)
Time-ordered feed of all case events: case opened, evidence attached (each with hash seal status), status changes, notes added, assigned changed. The audit trail for the case lifecycle.

**Cross-domain evidence types vary:** LP cases attach transactions, alerts, and reports. Vendor cases attach POs, receiving records, and email correspondence (file upload). B2B cases attach transaction records and account history. The attach mechanism is the same; the evidence types differ by case domain.

### Evidence Tab
Gallery of all attached evidence items. Filter by type. Each item: source, attach timestamp, sealed status (hash verified / not sealed), attached by.

**Seal-on-attach applies to all case types.** A vendor dispute document uploaded as evidence is hash-sealed at attach time. Whether it's a receipt of short-shipment or an email from the vendor, the evidentiary record is cryptographically anchored from the moment of attachment.

### Notes Tab
Threaded investigation/case notes. Immutable after 15 minutes. Same pattern as exception detail notes.

### Related Tab
Links to related cases (manually linked or system-detected — e.g., B2B case and a Hawk case involving the same store during the same period). Cross-domain connections surface here: an LP case that may have a vendor-quality contributing factor can be linked to a Vendor case investigating that vendor's return rate.

**Empty state per tab:** "No [timeline events/evidence/notes/related cases] yet."

## Interaction Flows

1. **Vendor credit resolution:** BYR opens vendor case for short-shipment dispute → attaches PO, receiving record, and vendor email acknowledgment → advances status from "Investigating" → "Vendor Credit Received" → closes case with resolution note: "$240 vendor credit applied to account"
2. **B2B escalation:** ADM opens B2B case for unauthorized price level usage → reviews evidence (transaction records showing Retail account using Wholesale pricing for 3 months) → escalates to legal → links to LP case #C-0041 investigating same period at same store → related cases tab updated
3. **LP-vendor convergence:** LP has open Hawk case for internal shrink → opens related cases → system has linked it to a Vendor case for the same SKUs showing high return rate from the same vendor → LP and BYR coordinate: vendor quality problem is masking as internal theft in the detection rules → updates LP case notes with this context

## UX Callout

The cross-domain case detail is architecturally the same as the Hawk case detail — it had to be, because the evidentiary model is non-negotiable regardless of domain. What changes is the interpretation: the same hash-sealed evidence record, the same note threads, the same timeline structure apply whether LP is investigating a cashier or a buyer is documenting a vendor dispute. The Related tab is the W5 addition that makes the cross-domain architecture valuable: real-world loss events rarely stay cleanly in a single domain. Vendor quality problems create LP signals. B2B account abuse creates both commercial and LP risks. The Related tab is where these connections become visible and traceable, without requiring LP and BYR to share a spreadsheet.

## Navigation Exits

- `/cases/all` — back to all-cases list
- `/cases/hawk/:id` — for Hawk-type cases (same record, domain-specific nav)
- `/exceptions/:id` — from originating exception

## Open Questions

None.
