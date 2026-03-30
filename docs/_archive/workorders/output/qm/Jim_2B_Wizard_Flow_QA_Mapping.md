---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# 2B — Wizard Flow QA Mapping (Processes 1–4)
**Date:** February 24, 2026
**Author:** Jim (QA Manager)
**Feature:** E0-F6-B/C (Guided Wizard Engine + Core Processes)
**References:** Design Spec v1.0 Sections 3, 10; PRD E0-F6-C; CRDM v1.0

---

## Process 1: Open the Store

**Trigger:** Time of day (AM) — action card on Today's View
**Wizard Steps:** 4
**Target Duration:** <5 minutes
**CRDM Tables:** cash_drawer_shifts

### Happy Path

```
SCENARIO: WZ-P1-HAPPY — Complete "Open the Store" wizard
MODULE: Rooster (Daily Operations)
ROLE: Store Manager
STORY: As a Store Manager opening my store in the morning, I follow the guided
       steps to ensure everything is set up correctly before customers arrive.

STEPS:
  1. Manager taps "Open the Store" action card on Today's View
  2. VERIFY: Wizard launches (full-screen overlay, no page reload)

  STEP 1: Verify Store Ready
  3. Screen shows checklist: lights on, register powered, signage visible
  4. Manager checks each item
  5. VERIFY: Progress indicator shows 1/4

  STEP 2: Open Cash Drawer
  6. Screen prompts: "Count your starting cash"
  7. Manager enters starting cash amount (e.g., $200.00)
  8. VERIFY: Amount field accepts dollars and cents
  9. Manager taps Next

  STEP 3: Confirm Opening
  10. Screen shows summary: "Store #1 opening with $200.00 in drawer"
  11. Manager confirms
  12. VERIFY: cash_drawer_shifts record created (status: OPEN, opening_cash_cents: 20000)

  STEP 4: Done
  13. VERIFY: Confetti + chirp sound + "Store is open!"
  14. VERIFY: Returns to Today's View
  15. VERIFY: "Open the Store" card is removed or marked complete

EXPECTED RESULT: 4 steps, <5 min. Cash drawer shift record created.
```

### Edge Cases

```
SCENARIO: WZ-P1-EDGE — Edge cases for "Open the Store"
MODULE: Rooster
ROLE: Store Manager

EDGE CASES:
  E1. Starting cash = $0.00 — should this be allowed? (Possible: some stores start with empty drawers)
      VERIFY: Warning message but still allows proceed
  E2. Starting cash = negative number — MUST reject
  E3. Manager tries to open store that's already open (shift exists, status = OPEN)
      VERIFY: Message "Store #1 is already open" — no duplicate shift created
  E4. Manager taps Back at step 3 — returns to step 2 with amount preserved
  E5. App crashes mid-wizard — no half-created records in database
  E6. Non-numeric input in cash amount field — VERIFY: input validation, clear error
  E7. Two managers try to open the same store simultaneously
      VERIFY: First one wins, second gets "already open" message
```

---

## Process 2: Count the Drawer

**Trigger:** Shift end or Chirp
**Wizard Steps:** 5
**Target Duration:** <6 minutes
**CRDM Tables:** cash_drawer_shifts, cash_drawer_events

### Happy Path

```
SCENARIO: WZ-P2-HAPPY — Complete "Count the Drawer" wizard
MODULE: Bull (Inventory / Cash)
ROLE: Store Manager or Shift Supervisor
STORY: As a shift closer, I count the cash drawer at the end of my shift
       so that any variance is detected and documented immediately.

STEPS:
  1. Merchant taps "Count the Drawer" card on Today's View (or Chirp triggers it)
  2. VERIFY: Wizard launches — "Count the Drawer"

  STEP 1: Select Drawer
  3. Screen shows list of open drawers at this location
  4. Merchant selects drawer to count
  5. VERIFY: System shows expected cash (from sales + starting cash - refunds)

  STEP 2: Enter Actual Count
  6. Merchant enters actual cash counted (bills + coins breakdown or single total)
  7. VERIFY: Amount field accepts dollars and cents

  STEP 3: Variance Check
  8. System computes variance: actual - expected
  9. VERIFY: If variance > $10 (CASH_VARIANCE_THRESHOLD): yellow warning banner
  10. VERIFY: If variance > $50: red warning banner
  11. VERIFY: If variance = $0 or within tolerance: green confirmation

  STEP 4: Document & Close
  12. If variance exists: prompt for notes explaining variance
  13. Optional photo upload of count sheet
  14. VERIFY: cash_drawer_shifts record updated: status → CLOSED, closed_cash_cents, cash_variance_cents computed
  15. VERIFY: cash_drawer_events record created for the count event

  STEP 5: Done
  16. VERIFY: Completion screen with appropriate messaging:
      - Green: "Perfect count! Drawer balanced."
      - Yellow: "Variance noted. Keep an eye on it."
      - Red: "Significant variance — consider investigating."
  17. VERIFY: Confetti only on green (balanced). No confetti on yellow/red.
  18. VERIFY: If red variance: Chirp C-102 fires for this merchant

EXPECTED RESULT: 5 steps, <6 min. Drawer closed, variance calculated, Chirp fires if threshold exceeded.
```

### Edge Cases

```
SCENARIO: WZ-P2-EDGE — Edge cases for "Count the Drawer"
MODULE: Bull
ROLE: Store Manager

EDGE CASES:
  E1. No open drawers — wizard shows "No open drawers to count" message
  E2. Drawer already counted by another user — "This drawer was closed by Sam at 9:15 PM"
  E3. Actual count = exactly the expected amount — variance = 0, green state
  E4. Actual count entered as negative — MUST reject
  E5. Very large variance (>$500) — does the wizard suggest calling the owner?
  E6. Photo upload fails — wizard allows proceeding without photo (photo is optional)
  E7. cash_variance_cents computation: verify it's (actual - expected), not (expected - actual)
      Short drawer = negative variance. Over drawer = positive.
```

### Evidence Chain Validation

```
For Process 2 with variance:
  1. VERIFY: If photo uploaded, evidence record created in Fox tables (INSERT-only)
  2. VERIFY: Evidence record has file_hash (SHA-256)
  3. VERIFY: case_timeline entry created if variance > threshold
  4. VERIFY: Attempting UPDATE on the evidence record fails ("CHAIN OF CUSTODY VIOLATION")
```

---

## Process 3: Resolve Refund Alert

**Trigger:** Chirp: HIGH_REFUND_FREQUENCY
**Wizard Steps:** 5
**Target Duration:** <7 minutes
**CRDM Tables:** transactions (type=RETURN), refund_links

### Happy Path

```
SCENARIO: WZ-P3-HAPPY — Complete "Resolve Refund Alert" wizard
MODULE: Canary (Chirps → Wizard)
ROLE: Store Manager or Owner
STORY: As a merchant receiving a HIGH_REFUND_FREQUENCY Chirp, I investigate
       the refund pattern and determine whether it's legitimate or suspicious.

STEPS:
  1. Chirp fires: HIGH_REFUND_FREQUENCY — "Employee Alex processed 5 refunds today"
  2. Merchant taps Chirp (hero banner or Chirps tab)
  3. VERIFY: Process 3 wizard launches

  STEP 1: Review the Facts
  4. Screen shows: employee name, refund count, total refund amount, time range
  5. VERIFY: Data matches actual transaction records
  6. Merchant reviews and taps Next

  STEP 2: Examine Individual Refunds
  7. Screen shows list of the specific refunds (date, amount, customer, item)
  8. VERIFY: Line item detail visible (from transaction_line_items)
  9. Merchant can tap each refund to see receipt-level detail

  STEP 3: Assess the Situation
  10. Screen shows assessment options:
      - "All legitimate — busy day with returns"
      - "Some look questionable"
      - "This is suspicious — investigate further"
  11. VERIFY: Owner sees "Flag for Fox investigation" button
  12. VERIFY: Manager does NOT see Fox escalation button
  13. Merchant selects an option

  STEP 4: Take Action
  14. Based on selection:
      - Legitimate: checklist of preventive measures (better return policy signage, etc.)
      - Questionable: schedule conversation with employee + document concern
      - Suspicious: (Owner only) launches Fox case creation flow
  15. Merchant completes the action steps

  STEP 5: Done
  16. VERIFY: Chirp marked as resolved
  17. VERIFY: Completion message appropriate to selection
  18. VERIFY: Confetti + chirp sound (only if resolved positively)

EXPECTED RESULT: 5 steps, <7 min. Refund pattern investigated, action taken.
```

### Edge Cases

```
SCENARIO: WZ-P3-EDGE — Edge cases for "Resolve Refund Alert"
MODULE: Canary
ROLE: Store Manager / Owner

EDGE CASES:
  E1. Employee has exactly 3 refunds (at threshold boundary) — does Chirp fire?
      Per CRDM: C-001 HIGH_REFUND_FREQUENCY fires at >3 per day. 3 = no fire. 4 = fires.
  E2. All refunds are for the same customer — different pattern than multiple customers
  E3. Refunds span multiple locations (for multi-store owner)
  E4. refund_links missing employee_id or location_id (CRDM-G2 gap — not yet fixed)
      VERIFY: Wizard handles missing data gracefully — shows "Unknown employee" not crash
  E5. Merchant selects "Suspicious" but is a Manager (no Fox access)
      VERIFY: Wizard suggests "Ask your owner to review" — does not expose Fox
  E6. The employee who processed the refunds is the merchant themselves
```

---

## Process 4: Resolve Cash Drawer Shortage

**Trigger:** Chirp: CASH_VARIANCE_THRESHOLD (C-102)
**Wizard Steps:** 6
**Target Duration:** <8 minutes
**CRDM Tables:** cash_drawer_shifts, employee_timecards

### Happy Path

(Covered in detail by TV-S2-001 in the Day-in-the-Life scripts. Summary here for completeness.)

```
SCENARIO: WZ-P4-HAPPY — Complete "Resolve Cash Drawer Shortage" wizard
MODULE: Canary (Chirps → Wizard)
ROLE: Any (with progressive disclosure based on role)
STORY: As a merchant receiving a CASH_VARIANCE_THRESHOLD Chirp, I investigate
       and resolve the cash shortage through a guided 6-step process.

STEPS:
  Step 1: Confirm the fact — "Was the drawer actually short $X?" Yes/No + photo
  Step 2: Who touched it last? — Pre-filled closer list from employee_timecards
  Step 3: Common causes — 4 illustrated cards (refund missed / math error / theft / other)
          OWNER ONLY: "Flag for Fox investigation" button visible
  Step 4: Fix it now — Step-by-step checklist with check-off animation
  Step 5: Learn & prevent — Tip + "Add to team playbook" toggle
  Step 6: Done — Confetti + chirp sound + "Great job — shrink prevented"

EXPECTED RESULT: 6 steps, <8 min. Shortage investigated, evidence captured, Chirp resolved.
```

### Edge Cases

```
SCENARIO: WZ-P4-EDGE — Edge cases for "Resolve Cash Drawer Shortage"
MODULE: Canary
ROLE: Various

EDGE CASES:
  E1. Variance = exactly $10.00 (at threshold) — does Chirp fire?
      Per CRDM: C-102 fires when |variance| > $10. $10 exactly = no fire. $10.01 = fires.
  E2. Drawer is OVER (positive variance, not short) — wizard title should say "surplus" not "shortage"
  E3. "No" at step 1 (drawer was not actually short) — wizard should short-circuit to Done
      with message "False alarm — glad to hear it!"
  E4. Photo upload at step 1: file > 10MB — VERIFY: size limit with clear error message
  E5. Photo upload: unsupported format (.heic on older Android) — VERIFY: format validation
  E6. Step 2 "Who touched it last?" — no timecards for any employees today
      VERIFY: Shows "No timecard data available" — allows proceed with manual entry
  E7. Owner selects "Theft (I suspect…)" at step 3 → taps "Flag for Fox investigation"
      VERIFY: Fox case created with evidence from steps 1-2 pre-populated
      VERIFY: case_evidence record has SHA-256 file_hash for photo
      VERIFY: case_timeline entry: "Case created from Process 4 wizard"
  E8. Step 4 checklist: merchant unchecks an item after checking it — allowed or locked?
  E9. Wizard timeout: merchant walks away for 30 minutes mid-wizard
      VERIFY: Session doesn't expire, progress preserved
  E10. Same Chirp resolved while merchant is mid-wizard (another user resolved it)
       VERIFY: Graceful message on completion attempt: "This was already resolved by Sam"
```

### Evidence Chain Validation (Process 4)

```
SCENARIO: WZ-P4-EVIDENCE — Verify evidence flows from wizard to Fox
MODULE: Canary → Fox
ROLE: Owner (has Fox access)

STEPS:
  1. Complete Process 4 wizard with photo upload and Fox escalation
  2. Navigate to Fox tab
  3. VERIFY: New case exists, created from this wizard
  4. VERIFY: case_evidence contains the photo from wizard step 1
  5. VERIFY: Evidence record has file_hash (SHA-256)
  6. VERIFY: Evidence record has chain_hash (hash chain linked)
  7. VERIFY: case_timeline shows: "Case created from Guided Wizard — Process 4"
  8. VERIFY: case_timeline shows: "Evidence added: [photo filename]"
  9. Attempt to UPDATE the case_evidence record via direct SQL
  10. VERIFY: "CHAIN OF CUSTODY VIOLATION" — rejected
  11. Attempt to DELETE the case_evidence record
  12. VERIFY: "CHAIN OF CUSTODY VIOLATION" — rejected

EXPECTED RESULT: Full evidence chain from wizard to Fox. Immutable.
```

---

## Completion UX Matrix (All 4 Processes)

| Process | Confetti? | Chirp Sound? | Completion Message | Chirp Resolved? |
|---------|-----------|-------------|-------------------|-----------------|
| P1: Open Store | Yes | Yes | "Store is open!" | N/A (not Chirp-triggered) |
| P2: Count Drawer (balanced) | Yes | Yes | "Perfect count! Drawer balanced." | N/A or resolves if Chirp-triggered |
| P2: Count Drawer (variance) | No | No | "Variance noted. Keep an eye on it." | Chirp stays active if severe |
| P3: Resolve Refund (legitimate) | Yes | Yes | "All clear — refund pattern explained." | Yes |
| P3: Resolve Refund (suspicious) | No | No | "Flagged for investigation." | Yes (escalated to Fox) |
| P4: Resolve Shortage (resolved) | Yes | Yes | "Great job — shrink prevented." | Yes |
| P4: Resolve Shortage (false alarm) | Yes | Yes | "False alarm — glad to hear it!" | Yes |
| P4: Resolve Shortage (escalated) | No | No | "Case opened — Fox is on it." | Yes (escalated to Fox) |

---

## Cross-Process QA Checklist

| Check | P1 | P2 | P3 | P4 |
|-------|----|----|----|----|
| HTMX step swap (no page reload) | ☐ | ☐ | ☐ | ☐ |
| Progress indicator shows current/total | ☐ | ☐ | ☐ | ☐ |
| Back button works at every step | ☐ | ☐ | ☐ | ☐ |
| Wizard takes full screen (mobile) | ☐ | ☐ | ☐ | ☐ |
| Touch targets ≥ 44px | ☐ | ☐ | ☐ | ☐ |
| Complete in target time | ☐ <5m | ☐ <6m | ☐ <7m | ☐ <8m |
| Completion screen (confetti where appropriate) | ☐ | ☐ | ☐ | ☐ |
| Returns to Today's View after completion | ☐ | ☐ | ☐ | ☐ |
| Role gating (progressive disclosure) | N/A | N/A | ☐ | ☐ |
| Evidence chain (photo → Fox) | N/A | ☐ | ☐ | ☐ |
| Chirp resolved on completion | N/A | ☐ | ☐ | ☐ |
| No data created on wizard abandon | ☐ | ☐ | ☐ | ☐ |

---

*Jim — QA Manager*
*Canary LP | Confidential*
*February 24, 2026*
