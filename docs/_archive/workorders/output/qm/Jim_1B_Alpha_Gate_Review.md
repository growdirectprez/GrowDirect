---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# 1B — Alpha Gate Checklist Review
**Date:** February 24, 2026
**Author:** Jim (QA Manager)
**Reference:** `Canary_IP/Markdown/QA/Alpha_v0.1.0_QA_Handoff.md`

---

## Alpha Gate Checklist — Status Assessment

The checklist from Eva's QA Handoff defines 15 sign-off items (final section). Jim's assessment of each against current Sprint 5 status:

| # | Gate Item | Achievable by UAT (Mar 3)? | Status | Dependency | Jim's Notes |
|---|----------|---------------------------|--------|------------|-------------|
| 1 | Full unit test suite passes (414+ pass, 0 Sprint-related failures) | ✅ YES | Current: 541 pass / 0 fail / 0 errors / 216 skipped. **Exceeds gate.** | None — already green | The 216 skipped are Docker tests (B-024 resolved). Acceptable for alpha gate. |
| 2 | All 22 QA scenarios pass (or failures documented as known issues) | ⚠️ PARTIAL | Scenarios 1-6, 8-10, 12 are testable via unit tests. Scenarios 7 (Fox), 11 (Square OAuth sandbox), 13-14 (E2E/browser) require running app. | Jeremy Phase 2-4 complete | Cannot fully validate until app serves on iMac. Jim will run automated scenarios the moment Jeremy delivers a working stack. |
| 3 | Sprint 2 Chirp rules verified (49/49 tests green) | ✅ YES | All 49 passing in current dev loop. | None | Green. |
| 4 | Sprint 2 parse helpers verified (23/23 tests green) | ✅ YES | All 23 passing. | None | Green. |
| 5 | Sprint 2 ingestion layer verified (13/13 tests green) | ✅ YES | All 13 passing. | None | Green. |
| 6 | Sprint 3 Chirp rules verified (53/53 tests green) | ✅ YES | All 53 passing in current dev loop. | None | Green. |
| 7 | Sprint 3 parse helpers verified (24/24 tests green) | ✅ YES | All 24 passing. | None | Green. |
| 8 | Sprint 3 ingestion layer verified (13/13 tests green) | ✅ YES | All 13 passing. | None | Green. |
| 9 | PII protection: loyalty phone numbers SHA-256 hashed | ✅ YES | Covered by `test_parse_helpers_sprint3.py` — `parse_loyalty_account()` hashes phone, raw phone never stored. | None | Green. Verified in test fixtures. |
| 10 | No P1 bugs remain open | ⚠️ UNKNOWN | Cannot assess until app is running on real Postgres. Unit tests are clean but P1 bugs may surface during integration testing. | Jeremy Phase 2-4 | Jim will triage immediately upon first full-stack run. |
| 11 | All P2 bugs have tickets with owners | ⚠️ UNKNOWN | Same — need integration run to identify P2 bugs. | Jeremy Phase 2-4 | Jim owns triage. |
| 12 | Docker build + test pass is reproducible on iMac | 🔴 NOT YET | Sprint 5 Phase 2 is in progress. Jeremy is migrating to real PostgreSQL + Docker on iMac. | Jeremy Phase 2 (critical path) | **This is the #1 blocker for Jim's full sign-off.** Jim cannot validate reproducibility until Jeremy delivers a green Docker stack. |
| 13 | Eva has reviewed Jim's QA report | ⏳ PENDING | Jim is producing the QA report now (this session). Eva reviews after Jim delivers. | This session's output | On track. |
| 14 | Database has 31 tables (test_data_integrity confirms) | ⚠️ NEEDS UPDATE | Current `test_data_integrity.py` checks 31 tables. Sprint 5 may add tables from Alembic migrations. Tom's B-001 doesn't add new tables — adds triggers + columns. CRDM-G1 added `previous_chain_hash` column but no new table. | Verify after Phase 2 | Table count should remain 31 for alpha. Verify post-migration. |
| 15 | 22 immutability triggers active (test_data_integrity confirms) | ⚠️ NEEDS UPDATE | Tom's B-001 specifies 12 new triggers on financial tables (P0-1: 6 tables × 2 triggers) + 8 new triggers on evidence tables (P0-2: 4 tables × 2 triggers) = 20 new triggers. Previous count was 22. **New expected total: 42 triggers.** `test_data_integrity` needs updating. | Jeremy Phase 3 (trigger deployment) | Jim flags: the test file's expected trigger count is stale. Jeremy must update `test_data_integrity.py` to expect 42 (or whatever the final count is post-P0-1/P0-2). |

---

## Summary

| Category | Count |
|----------|-------|
| ✅ Achievable now (green) | 8 items (#1, 3-9) |
| ⚠️ Achievable by UAT but dependent on Jeremy | 5 items (#2, 10, 11, 14, 15) |
| 🔴 Not yet achievable — critical path | 1 item (#12: Docker reproducibility) |
| ⏳ In progress (this session) | 1 item (#13: Eva review) |

## Flags for Eva

1. **Item #12 is the hard gate.** Jim cannot sign off on alpha until Docker build + test is reproducible on iMac. Jeremy owns this — Sprint 5 Phase 2.
2. **Item #15 trigger count is stale.** Tom's B-001 adds 20 triggers. `test_data_integrity.py` expected count needs updating from 22 to the actual post-migration total. Jeremy should fix this during Phase 3.
3. **Items #10 and #11 (P1/P2 bug triage)** — Jim will run triage the moment a full stack is available. If bugs surface that block UAT, Jim escalates immediately.

## Jim's Recommendation

The gate is **achievable by March 3** IF Jeremy's Sprint 5 Phase 2-4 lands by Friday Feb 28. The unit test foundation is solid (541 passing). The risk is integration — moving from SQLite to real PostgreSQL may surface issues that don't exist in unit tests. Jim will run the full Rooster (all 3 modes) the moment the stack is available and report results within 4 hours.

---

*Jim — QA Manager*
*Canary LP | Confidential*
*February 24, 2026*
