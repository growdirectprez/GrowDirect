---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# 1A — UAT Logistics Plan
**Date:** February 24, 2026
**Author:** Jim (QA Manager & CSM)
**UAT Date:** Monday, March 3, 2026
**Eva Deadline:** Merchant list confirmed by Wednesday, February 26

---

## Merchant Participant Requirements

### Minimum Viable UAT Panel: 3 merchants (target: 5)

Jim needs merchants who represent the three core personas the Companion serves. Each merchant must meet ALL criteria below.

| Slot | Role Profile | Why This Profile | Device Requirement | Session Length |
|------|-------------|-----------------|-------------------|---------------|
| M-1 | **Owner-Operator** (single location, hands-on daily) | Tests Today's View, all wizards, Owl/Fox visibility, scorecard access. Full permission set. | iPhone (iOS Safari) + laptop (Chrome) | 90 min |
| M-2 | **Store Manager / Shift Supervisor** (part-timer, non-owner) | Tests role-gated views — must NOT see Fox workbench, Goose, or Team Performance scorecard. Tests Processes 1-4 from the restricted role. | Android phone (Chrome) | 60 min |
| M-3 | **Multi-Store Owner** (2+ locations) | Tests location switcher, cross-store Chirps, aggregated scorecards. Critical for C-303 (WRONG_LOCATION) Chirp validation. | iPad + iPhone | 90 min |
| M-4 (stretch) | **New Merchant** (just onboarded, <1 week) | Tests first-run experience, onboarding flow, "is this confusing on day 1?" | Any mobile device | 45 min |
| M-5 (stretch) | **Tech-resistant Owner** (>50 years old, prefers pen-and-paper) | The phone test. If this merchant can complete Process 4 without calling Jim, we pass. | Whatever they already carry | 60 min |

### Pre-UAT Requirements (Jeremy Must Deliver by Friday Feb 28)

| # | Requirement | Status | Owner |
|---|------------|--------|-------|
| 1 | App serving on iMac QA box via Docker | 🔄 In progress (Sprint 5 Phase 2) | Jeremy |
| 2 | PostgreSQL 3-database architecture running (canary_app, canary_sales, canary_metrics) | 🔄 In progress | Jeremy |
| 3 | Alembic migrations green on real Postgres | 🔄 In progress | Jeremy |
| 4 | INSERT-only triggers verified (P0-1, P0-2) | Pending Phase 3 | Jeremy |
| 5 | Hash chain verification working (P0-3) | Pending Phase 3 | Jeremy |
| 6 | Today's View rendering (Art v1.1 wireframe implemented) | Not started | Jeremy |
| 7 | At least Process 4 wizard functional (CASH_VARIANCE_THRESHOLD → 6-step flow) | Not started | Jeremy |
| 8 | Test merchant accounts seeded with realistic data | Not started | Jeremy + Jim |
| 9 | Square sandbox connected with test transactions | Not started | Jeremy |
| 10 | Network accessible from merchant devices (local Wi-Fi or tunnel) | Not started | Jeremy |

**Jim's assessment:** Items 1-5 are on Jeremy's critical path this week. Items 6-7 are the UAT-critical features. If items 6-7 are not ready by Friday Feb 28, UAT cannot proceed as planned. Jim will flag to Eva by Thursday if trajectory looks red.

### Test Data Requirements

Each merchant test account needs:
- 30+ transactions (mix of SALE, RETURN, VOID, POST_VOID)
- 2-3 active Chirps (including one CASH_VARIANCE_THRESHOLD)
- 1 resolved Chirp (to show completion state)
- Cash drawer shift data (open + closed, with variance)
- Employee timecards (2-3 employees, overlapping shifts)
- At least 1 Fox case in progress (for Owner role testing)

---

## UAT Schedule — Monday, March 3

| Time | Merchant | Focus | Facilitator | Device |
|------|----------|-------|-------------|--------|
| 9:00-10:30 AM | M-1 (Owner-Operator) | Full Companion walkthrough: Today's View → Process 4 wizard → Scorecard → Fox escalation | Jim | iPhone + laptop |
| 10:30-11:00 AM | Buffer / Jim notes | Document findings, reset test data if needed | Jim | — |
| 11:00 AM-12:00 PM | M-2 (Store Manager) | Role-gated testing: Today's View → Process 1 (Open Store) → Process 2 (Count Drawer) → verify restricted access | Jim | Android |
| 12:00-1:00 PM | Lunch break | — | — | — |
| 1:00-2:30 PM | M-3 (Multi-Store Owner) | Multi-location: location switcher, cross-store Chirps, aggregated views | Jim | iPad + iPhone |
| 2:30-3:15 PM | M-4 (New Merchant, if available) | First-run experience, unguided exploration | Jim observes, does not guide | Any mobile |
| 3:15-4:15 PM | M-5 (Tech-resistant, if available) | The phone test: complete Process 4 unassisted | Jim observes, records time-to-complete | Their phone |
| 4:15-5:00 PM | Jim debrief | Compile findings, draft UAT summary for Eva | Jim | — |

### UAT Success Criteria

| # | Criterion | Pass/Fail |
|---|----------|-----------|
| 1 | Today's View loads in <10 seconds on mobile (first load with cold cache) | |
| 2 | Merchant can identify their #1 action within 90 seconds of opening the app | |
| 3 | Owner can complete Process 4 wizard end-to-end in <8 minutes | |
| 4 | Manager sees ONLY role-appropriate content (no Fox, no Goose, no Team Performance) | |
| 5 | All 6 SVG animal icons identifiable at nav-bar size | |
| 6 | Chirp peek indicator shows when 2+ Chirps active, hidden when 0-1 | |
| 7 | No P1 bugs encountered during any session | |
| 8 | No merchant asks "what do I do now?" more than once per wizard | |
| 9 | Photo evidence capture works on mobile (if implemented) | |
| 10 | Jim's phone test: tech-resistant owner completes Process 4 without help | |

---

## ACTION REQUIRED — Eva

**By Wednesday Feb 26:**
- Jim needs confirmed merchant names, contact info, and availability for March 3
- If Jim cannot confirm 3+ merchants by Wednesday, Eva escalates to ALX → Jeffe for network outreach
- Jim will begin direct outreach to existing merchant contacts today (Feb 24)

**Merchant recruitment channels (priority order):**
1. Jeffe's direct contacts (fastest path — Jeffe knows who's friendly and engaged)
2. Jim's existing CSM relationships (if any merchants are already onboarded to earlier builds)
3. GrowDirect network referrals

---

*Jim — QA Manager & CSM*
*Canary LP | Confidential*
*February 24, 2026*
