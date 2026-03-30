---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# 1D — B-007 Untested Routes: Prioritization
**Date:** February 24, 2026
**Author:** Jim (QA Manager)
**Blocker:** B-007 — 20 routes without tests
**Source:** Jeremy's Sprint 5 Work Order, Phase 3; ORPHAN_REPORT.md

---

## Classification: Must-Have-Before-UAT vs. Can-Wait

Jim's logic: any route a merchant touches during UAT must have test coverage. Backend/infrastructure routes can wait.

### MUST HAVE BEFORE UAT (10 routes)

These routes are on the merchant's critical path or directly support the Guided Companion experience.

| # | Route | File | Why Must-Have | UAT Impact |
|---|-------|------|--------------|------------|
| 1 | `GET /today` | companion_wired.py | **This IS Today's View.** The first screen every merchant sees. No test = no confidence in the #1 feature. | 🔴 Blocks all UAT sessions |
| 2 | `GET /wizard/<int:chirp_id>` | companion_wired.py | Wizard launcher — every Chirp tap goes here. Core interaction pattern for E0-F6. | 🔴 Blocks Process 1-4 testing |
| 3 | `POST /wizard/<int:chirp_id>/step/<int:step_num>` | companion_wired.py | Wizard step progression — the "Next" button in every wizard. Without this, wizards don't advance. | 🔴 Blocks wizard completion |
| 4 | `POST /process/<int:process_id>/complete` | companion_wired.py | Process completion endpoint — records wizard completion, triggers confetti UX. | 🔴 Blocks wizard sign-off |
| 5 | `GET /scorecard/<period>` | companion_wired.py | Scorecard display — Owner end-of-day review. Part of Scenario Set 3. | 🟡 Blocks Owner UAT session |
| 6 | `POST /<alert_id>/escalate` | alerts_wired.py | Chirp escalation to Fox — Owner at wizard step 3 "Flag for Fox investigation." | 🟡 Blocks Fox escalation test |
| 7 | `POST /alerts/<int:alert_id>/resolve` | app.py | Chirp resolution — marks a Chirp as resolved after wizard completion. | 🟡 Blocks Chirp lifecycle test |
| 8 | `GET /cases/<int:case_id>/evidence/<int:evidence_id>` | fox_wired.py | Evidence retrieval — Fox case management, view uploaded evidence. | 🟡 Blocks Fox evidence review |
| 9 | `POST /cases/<int:case_id>/actions` | fox_wired.py | Fox case action — add notes, change status, assign to user. | 🟡 Blocks Fox case management |
| 10 | `GET /cases/<int:case_id>/evidence/verify` | fox_wired.py | Evidence chain verification — validates hash chain integrity for a case. | 🟡 Blocks Fox evidence trust |

### CAN WAIT UNTIL POST-ALPHA (10 routes)

These routes are infrastructure, settings, or duplicates that merchants won't directly exercise during UAT.

| # | Route | File | Why Can Wait | Risk of Waiting |
|---|-------|------|-------------|-----------------|
| 11 | `POST /sweep` | chirp_wired.py | Chirp sweep (batch re-evaluation) — automated backend process, not merchant-triggered. | Low — sweep runs on schedule, not on merchant action |
| 12 | `GET /userinfo` | auth.py | User info endpoint — returns logged-in user metadata. Used internally by frontend. | Low — covered indirectly by auth flow tests |
| 13 | `GET /readiness` | health.py | Readiness probe — Kubernetes/Docker health check. Not merchant-facing. | Low — covered by Quick Crow health tests |
| 14 | `GET /<location_id>/stats` | locations_wired.py | Per-location stats — Owner multi-store view. Not in MVP Process 1-4 scope. | Medium — needed for multi-store UAT (M-3), but stats are informational |
| 15 | `GET /<int:id>` | merchants.py | Get merchant by ID — admin/API use only. Not merchant-facing UI. | Low — admin route |
| 16 | `PUT /<int:id>` | merchants.py | Update merchant — admin/API use only. | Low — admin route, restricted access |
| 17 | `GET /billing` | settings.py | Billing page — Farm settings. Not in MVP wizard scope. | Low — settings page, not core workflow |
| 18 | `GET /receipt/<payment_id>` | app.py | Receipt retrieval — secondary feature, not in wizard flow. | Low — convenience feature |
| 19 | `GET /receipt/<payment_id>` | wsgi.py | **Duplicate** of #18 — same route registered in both app.py and wsgi.py. Jeremy should consolidate. | Low — duplicate, clean up in Sprint 6 |
| 20 | `POST /alerts/<int:alert_id>/resolve` | wsgi.py | **Duplicate** of #7 — same route in wsgi.py. Another consolidation candidate. | Low — duplicate |

---

## Summary

| Category | Count | Routes |
|----------|-------|--------|
| 🔴 Must-Have Before UAT | 5 | `/today`, `/wizard/...`, `/wizard/.../step/...`, `/process/.../complete`, `/scorecard/...` |
| 🟡 Must-Have Before UAT | 5 | `/escalate`, `/resolve`, Fox evidence routes (3) |
| ✅ Can Wait Post-Alpha | 10 | Infrastructure, admin, settings, duplicates |

## Recommendation to Jeremy

**Priority 1 (this week):** Write test stubs for the 5 companion_wired.py routes (#1-5). These are the Companion's spine — every UAT scenario depends on them.

**Priority 2 (before Friday):** Write test stubs for alert escalation (#6), alert resolution (#7), and Fox evidence routes (#8-10). These support the Owner's full workflow including Fox investigation.

**Priority 3 (post-alpha):** Clean up the 10 remaining routes. Note the 2 duplicates (#19, #20) — these should be consolidated during Sprint 6 refactoring, not just tested separately.

## B-007 Status Change Request

Once Jeremy writes stubs for the 10 must-have routes, Jim recommends:
- Change B-007 from 🟡 HIGH to 🟠 MEDIUM (remaining 10 routes are low-risk)
- Track the 10 post-alpha routes as tech debt in Sprint 6 backlog

---

*Jim — QA Manager*
*Canary LP | Confidential*
*February 24, 2026*
