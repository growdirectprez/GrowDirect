---
screen: /cases/hawk/:id/evidence
title: Evidence Attach
role: LP
wave: W1
origin: O
cp_equivalent: "None"
---

# Evidence Attach

**URL:** `/cases/hawk/:id/evidence`  
**Primary role:** LP  
**Entry points:** Case detail → "Add Evidence" button

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Case ID + title, breadcrumb back to case | Context: which case this evidence attaches to |
| Left column | Transaction search panel | ~60% width |
| Right column | File upload zone + manual record form | ~40% width |
| Preview panel | Full-width — appears after selecting a transaction for attach | Shows transaction before committing |
| Action bar | Attach selected transaction / Upload file / Save manual record, Cancel | |

## Key Elements

### Transaction Search Panel
Search fields: Ticket number (direct lookup), Cashier name/ID, Date range, Transaction amount range, Store. Results table: ticket #, cashier, store, amount, date — checkboxable. Multiple transactions can be selected for bulk attach. Each selected transaction shows a preview badge (ticket # + amount).

**Empty search state:** "Enter a ticket number, cashier, or date range to find transactions."
**No results:** "No transactions match the search criteria."

### Transaction Preview (appears on selection)
Full ticket detail displayed (same as `/transactions/:id`) — LP reviews the full line-item record before attaching. Confirmation visible: "This record will be sealed upon attachment. It cannot be modified after sealing." Seal confirmation is explicit — LP must read and acknowledge it.

### File Upload Zone
Drag-and-drop or click-to-browse. Accepted: PDF, PNG, JPG, DOCX. Max 10MB per file. Files are stored encrypted in S3 (S3 cold tier) and a SHA-256 hash is computed on upload — the hash seals the file content at the moment of upload. File name, upload timestamp, and uploader identity are stored with the hash.

### Manual Record Form
For evidence that isn't a digital artifact:
- Type: Verbal Statement / Physical Observation / Camera Reference / Third-Party Report
- Description: free text (required, min 50 characters)
- Date/time of observation
- Witness name(s) (optional)

Manual records receive a hash of the text content at save time — the hash seals the statement as of submission.

### Seal Confirmation
After any evidence attach action: system displays confirmation: "Evidence record sealed. Hash: [SHA-256]. This record is now immutable and will appear on the case timeline." LP acknowledges. There is no way to modify or delete an attached evidence record — only the case as a whole can be closed.

## Interaction Flows

1. **Attach transaction by ticket number:** LP enters ticket number → transaction appears in results → clicks transaction → preview panel opens → LP verifies it's the right record → clicks "Attach" → seal confirmation shown → evidence appears on case timeline
2. **Bulk attach from cashier search:** LP searches by cashier + date range → 6 transactions match → LP selects 4 of them (excludes 2 unrelated) → clicks "Attach Selected" → all 4 sealed and added to timeline
3. **Upload camera still:** LP has a screenshot from the camera system → clicks Upload → drag-drops image file → adds description "Camera 3, Checkout Lane 4, 2:47pm — subject reaching into drawer" → saves → file sealed with hash

## UX Callout

The seal-on-attach guarantee is the mechanism that makes Canary's evidence records legally defensible. LP investigators cannot edit evidence after attaching it — this isn't a UX constraint, it's a design invariant. The seal confirmation message ("This record is now immutable") is intentionally prominent because LP investigators need to understand that they're creating a permanent record, not a draft. The hash computed at attachment time means that if someone later claims a record was modified after the fact, the hash mismatch proves it. No CP LP process has anything resembling this — evidence in CP investigations lives in email attachments and printouts.

## Navigation Exits

- `/cases/hawk/:id` — back to case detail after attaching evidence
- `/transactions/:id` — from transaction search results (view before attaching)

## Open Questions

None.
