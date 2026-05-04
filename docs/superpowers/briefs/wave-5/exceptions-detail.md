---
screen: /exceptions/:id
title: Exception Detail
role: LP | MGR
wave: W5
origin: N
cp_equivalent: "None — CP has no exception record type"
---

# Exception Detail

**URL:** `/exceptions/:id`  
**Primary role:** LP; MGR  
**Entry points:** Exception queue row

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Exception ID, type, status badge, priority | Breadcrumb back to /exceptions |
| Top section | Exception summary + triggering alert | |
| Main content | Evidence panel + investigation notes | |
| Right rail | Subject profile (cashier/customer) + history | |
| Action bar | Advance Status, Escalate, Create Case, Dismiss | |

## Key Elements

### Exception Summary
Date/time, store, transaction ID, cashier, exception type, amount ($), rule that triggered the underlying alert, rule context (what was checked, threshold, actual value — same Rule Context Panel as the Alert Detail brief). Direct link to the triggering transaction in `/transactions/:id`.

**Hash seal status:** Exception is anchored to a hash-sealed transaction. "Underlying transaction: hash verified." If the transaction has been tampered with, the exception detail shows the tamper indicator — this is evidence integrity, LP-critical.

### Evidence Panel
Linked evidence items: the triggering alert, the transaction(s), any additional evidence attached during investigation (manual records, file uploads, linked prior cases). Same evidence attach workflow as the Hawk case evidence screen — seal-on-attach applies. LP can add evidence directly from the exception detail; it becomes part of the exception's evidentiary record whether or not a formal case is opened.

### Investigation Notes
Threaded text notes added by LP investigators. Each note: author, timestamp, content. Notes are immutable (cannot be edited after 15 minutes; a correction must be a new note). The note thread is the investigation diary — what LP looked at, what they concluded, what action they took.

### Subject Profile (Right Rail)
**If cashier-pattern exception:** Cashier name, shift info, recent alert history (last 90 days), cashier risk score, open cases as subject.

**If customer-pattern exception:** Customer name, risk score, case history, return history, loyalty tier (if enrolled).

**History panel:** Other exceptions involving the same subject in the last 90 days. Pattern context: is this an isolated event or part of a series?

### Action Bar
- **Advance Status:** New → In Review → Resolved (requires resolution type: Case Opened / No Action Required / Referred / Monitoring)
- **Escalate:** Status → Escalated. Routes to a different LP user or ADM. Adds escalation note.
- **Create Case:** Creates a new Hawk case with this exception as seed evidence. Pre-populates the case with the exception's evidence and subject.
- **Dismiss:** Closes the exception without action. Reason required (false positive / legitimate transaction / duplicate).

**Empty state:** Not applicable — exception exists before reaching this screen.

## Interaction Flows

1. **Standard investigation:** LP opens exception → reviews Rule Context Panel → checks cashier history (right rail) → this is the 4th similar exception from this cashier in 30 days → clicks Create Case → exception evidence and cashier ID pre-populate the new case → LP adds investigative notes
2. **Dismissal — false positive:** LP reviews exception → Over-Discount type → opens transaction → customer has a Wholesale price level → discount is legitimate → adds note: "Customer #C-4821 is a Wholesale account at 25% level — exception is expected behavior" → Dismisses with reason: Legitimate Transaction → flags LP substrate config to add this customer to the discount allow-list
3. **Escalation:** Exception implicates the Store 2 manager → LP doesn't have authority to investigate a manager → escalates to ADM LP team with notes → status = Escalated → ADM takes over

## UX Callout

The exception detail is where LP investigation work actually happens. The alert tells LP what to look at; the exception is where LP looks at it, documents what they found, and decides what to do. The evidence panel with seal-on-attach means that any additional evidence LP gathers during the investigation becomes part of the cryptographically-anchored record — the evidentiary model extends from the original transaction through every document, note, and linked record LP adds during the investigation. This is the difference between a paper-based LP program (notes in a spiral notebook, copies of printed reports stapled together) and an evidentiary-grade digital program. When HR or legal needs the record, it's already complete, organized, and tamper-proof.

## Navigation Exits

- `/exceptions` — back to exception queue
- `/transactions/:id` — from exception summary
- `/cases/hawk/:id` — after Create Case action
- `/alerts/:id` — from triggering alert link

## Open Questions

None.
