---
screen: /cases/hawk/:id
title: Case Detail (Hawk)
role: LP | MGR
wave: W1
origin: O
cp_equivalent: "None"
---

# Case Detail (Hawk)

**URL:** `/cases/hawk/:id`  
**Primary role:** LP; secondary: MGR  
**Entry points:** Case list row; alert detail → escalate; evidence attach

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Case ID, status badge, subject name, store, assigned investigator, open date | Status selector dropdown inline (LP can change status from here) |
| Left column (70%) | Evidence timeline + case notes | Chronological, most recent at bottom |
| Right column (30%) | Subject profile panel | Persistent — follows scroll |
| Action bar | Add Evidence, Add Note, Change Status, Request Review, Export Case Report | Fixed at bottom |

## Key Elements

### Evidence Timeline
Chronological list of all evidence records attached to this case. Each entry shows:
- Timestamp (when attached)
- Evidence type (Transaction / Alert / File Upload / Manual Record)
- Brief descriptor (e.g., "Ticket #99221 — $47.50 discount violation")
- Hash Status: **Sealed (green)** or **Tampered (red)**
- Sealing timestamp (when the hash was computed and the record locked)
- Linked resource icon (click to open the source transaction, alert, or file)

The hash status per evidence item is the legal-defensibility core of this screen. Each evidence record is immutable after sealing. A case that goes to HR or police needs this chain unbroken.

**Empty state (no evidence yet):** "No evidence attached. Click 'Add Evidence' to attach transactions, alerts, or documents to this case."

### Case Notes
Threaded comments — each note shows: actor (name + role badge), timestamp, note text. Notes are immutable after posting (no edit/delete). LP uses notes to document findings, manager uses notes to add their review, HR/legal uses notes as the investigation narrative.

### Subject Profile Panel (Right Rail)
Persistent right column. Shows:
- Subject type (Cashier / Customer)
- Alert count (total, all time)
- Case count (how many cases involve this subject)
- Risk score (if customer)
- Recent alert sparkline (30 days)
- "View full profile" link → `/customers/:id` or cashier profile

### Status Selector
Inline dropdown in header. State machine: Open → Under Review → Pending → Closed. Each transition is audited. Closed state requires a closure reason code (Substantiated / Unsubstantiated / Referred to HR / Referred to Police / Cleared).

## Interaction Flows

1. **Work a case:** LP opens case → reviews evidence timeline → reads prior notes → adds a note documenting today's findings → attaches a new transaction found during investigation → status = Under Review
2. **Request manager review:** LP completes initial investigation → adds summary note → changes status to Pending → status change triggers notification to assigned MGR → MGR opens case → adds approval note → status → Closed
3. **Verify evidence integrity:** Before closing a case, LP reviews hash status on every evidence record → all show "Sealed (green)" → LP can confidently export the case report for HR proceedings

## UX Callout

The evidence timeline with hash status per item is what makes Canary's case management legally defensible. Every evidence record shows: when it was ingested, when it was sealed, and whether the record has been tampered with since sealing. A case that goes to HR or a police report needs this audit chain, and no existing retail LP system provides it. CP teams manage cases in spreadsheets, email, and paper files — with no integrity guarantees on any of the "evidence." Canary's case detail is designed to be printable as a legal document, not just an operational tracking tool.

## Navigation Exits

- `/cases/hawk` — back to case list
- `/cases/hawk/:id/evidence` — evidence attach flow (from Action bar)
- `/transactions/:id` — from evidence timeline links
- `/alerts/:id` — from evidence timeline links
- `/customers/:id` — from subject profile panel link
- `/cases/hawk/patterns` — cross-case patterns for this subject

## Open Questions

None.
