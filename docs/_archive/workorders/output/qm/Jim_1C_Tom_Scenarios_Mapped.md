---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# 1C — Tom's Data Integrity Scenarios Mapped to Jim's Test Format
**Date:** February 24, 2026
**Author:** Jim (QA Manager)
**Source:** Tom's B-001 Session Output — "Notes for Jim" section (P0-3)
**Canonical Terminology:** Per PhD Alignment Brief Section 6

---

Tom specified 7 QA test cases for hash chain and immutability verification. Below, each is mapped to Jim's standard test scenario format.

---

## TOM-QA-001: INSERT Verification (Hash Chain Computation)

```
SCENARIO: Verify hash chain entry_hash is correctly computed on INSERT
MODULE: Canary Core (Audit)
ROLE: System (automated — no user role)
STORY: As the system, when a record is INSERTed into audit_log, the entry_hash
       is automatically computed from canonical record data + previous_hash
       so that the chain of custody is maintained without manual intervention.
PRECONDITIONS:
  - PostgreSQL running with canary_app schema
  - pgcrypto extension installed
  - P0-3 compute_entry_hash trigger active on audit_log
  - Test merchant account exists
STEPS:
  1. INSERT 5 records into canary_app.audit_log for test merchant
  2. For each record, call canary_app.verify_entry_hash('audit_log', record_id)
  3. Verify each returns is_valid = TRUE
  4. Verify each stored_hash matches expected_hash
  5. Verify previous_hash on record #1 is NULL (genesis)
  6. Verify previous_hash on records #2-5 equals entry_hash of prior record
EXPECTED RESULT: All 5 records have valid hashes. Chain links correctly.
EDGE CASES:
  - What if two records INSERT simultaneously for same merchant? (concurrency race)
  - What if canonical field ordering changes between PostgreSQL versions?
SEVERITY: Critical
LINKED STORY: CRDM v1.0 Principle 3 — Immutable Where It Matters
TESTABLE BEFORE UAT: Yes — requires PostgreSQL with P0-3 triggers
```

---

## TOM-QA-002: Chain Walk Verification

```
SCENARIO: Walk hash chain from most recent record back to genesis
MODULE: Canary Core (Audit)
ROLE: System (automated)
STORY: As the system, I can walk the hash chain from any record back to the
       genesis record and verify every link is intact, confirming no tampering
       has occurred.
PRECONDITIONS:
  - 5 records INSERTed per TOM-QA-001
  - verify_hash_chain function deployed
STEPS:
  1. Call canary_app.verify_hash_chain('audit_log', record_5_id, merchant_id)
  2. Verify function returns 5 rows (one per chain position)
  3. Verify ALL rows show is_valid = TRUE
  4. Verify chain_position runs from 1 (most recent) to 5 (genesis)
  5. Verify genesis record (position 5) has previous_hash = NULL
EXPECTED RESULT: 5 rows, all valid, chain intact from tip to genesis.
EDGE CASES:
  - What if a merchant has only 1 record (genesis only)?
  - What if merchant has 1,000+ records (performance)?
SEVERITY: Critical
LINKED STORY: CRDM v1.0 Principle 3; Tom B-001 P0-3
TESTABLE BEFORE UAT: Yes — requires PostgreSQL with P0-3 functions
```

---

## TOM-QA-003: Tamper Detection

```
SCENARIO: Detect record tampering via hash chain verification
MODULE: Canary Core (Audit)
ROLE: System (automated — simulates superuser attack)
STORY: As the security system, if an attacker with superuser access disables
       triggers, modifies a record, and re-enables triggers, the hash chain
       verification detects the tampering and reports the exact broken link.
PRECONDITIONS:
  - 5 records INSERTed per TOM-QA-001
  - All chain links verified valid (TOM-QA-002 passed)
STEPS:
  1. Using superuser connection: ALTER TABLE audit_log DISABLE TRIGGER trg_immutable_audit_log_update
  2. UPDATE audit_log SET details = 'tampered' WHERE id = <record_3_id>
  3. ALTER TABLE audit_log ENABLE TRIGGER trg_immutable_audit_log_update
  4. Call canary_app.verify_hash_chain('audit_log', record_5_id, merchant_id)
  5. Verify function reports is_valid = FALSE at the tampered record (position 3)
  6. Verify error_message contains "HASH MISMATCH"
EXPECTED RESULT: Chain broken at position 3. Records 1-2 (after tamper) still show valid. Record 3 shows mismatch.
EDGE CASES:
  - What if genesis record (first in chain) is tampered?
  - What if attacker also recomputes the hash for record 3? (Answer: records 4-5 still break because their previous_hash references the old hash of 3)
SEVERITY: Critical
LINKED STORY: CRDM v1.0 Principle 3; Tom B-001 P0-3
TESTABLE BEFORE UAT: Yes — requires superuser access for simulation
```

---

## TOM-QA-004: Genesis Record Validation

```
SCENARIO: First record for a new merchant has NULL previous_hash and valid entry_hash
MODULE: Canary Core (Audit)
ROLE: System (automated)
STORY: As the system, when the first audit_log record for a brand-new merchant
       is created, it establishes the genesis of the hash chain with previous_hash
       = NULL and a correctly computed entry_hash.
PRECONDITIONS:
  - PostgreSQL running with P0-3 triggers active
  - No existing audit_log records for test merchant "NEW_MERCHANT_001"
STEPS:
  1. INSERT 1 record into audit_log for merchant "NEW_MERCHANT_001"
  2. Query the record — verify previous_hash IS NULL
  3. Call verify_entry_hash('audit_log', record_id) — verify is_valid = TRUE
  4. Verify entry_hash = SHA-256(canonical_data || '') (empty string for NULL previous)
EXPECTED RESULT: Genesis record created with NULL previous_hash and valid hash.
EDGE CASES:
  - What if the merchant_id already exists with records from a prior test run?
SEVERITY: Critical
LINKED STORY: CRDM v1.0 Principle 3
TESTABLE BEFORE UAT: Yes
```

---

## TOM-QA-005: Cross-Merchant Isolation

```
SCENARIO: Merchant A's hash chain is independent of Merchant B's records
MODULE: Canary Core (Audit)
ROLE: System (automated)
STORY: As the multi-tenant system, each merchant's hash chain is isolated.
       Records from Merchant B do not affect Merchant A's chain verification.
PRECONDITIONS:
  - Merchant A has 3 records in audit_log
  - Merchant B has 5 records in audit_log
STEPS:
  1. INSERT 3 records for Merchant A, then 5 records for Merchant B (interleaved)
  2. Verify Merchant A's chain: verify_hash_chain('audit_log', A_record_3, merchant_A_id) → 3 rows, all valid
  3. Verify Merchant B's chain: verify_hash_chain('audit_log', B_record_5, merchant_B_id) → 5 rows, all valid
  4. Verify Merchant A's genesis record references only Merchant A records
  5. Verify Merchant B's genesis record references only Merchant B records
  6. DELETE all Merchant B records (via superuser bypass) — verify Merchant A's chain is STILL intact
EXPECTED RESULT: Chains are fully independent. Mutation of one merchant's data has zero impact on another's.
EDGE CASES:
  - What if merchant_id is NULL on a record? (Should not happen — enforce NOT NULL)
  - What if two merchants share an employee_id? (Fine — chains are merchant-scoped)
SEVERITY: Critical
LINKED STORY: CRDM v1.0 Part 2 (Multi-Tenant Architecture)
TESTABLE BEFORE UAT: Yes
```

---

## TOM-QA-006: Trigger Rejection — UPDATE on audit_log

```
SCENARIO: Attempt UPDATE on immutable audit_log table — must fail
MODULE: Canary Core (Audit)
ROLE: System (automated — tests database constraint)
STORY: As the database, any attempt to UPDATE a record in audit_log must be
       rejected with a "CHAIN OF CUSTODY VIOLATION" error, protecting the
       evidentiary record from modification.
PRECONDITIONS:
  - P0-2 immutability triggers active on audit_log
  - At least 1 record exists in audit_log
STEPS:
  1. Attempt: UPDATE canary_app.audit_log SET details = 'modified' WHERE id = <any_record>
  2. Verify the operation is REJECTED
  3. Verify error message contains "CHAIN OF CUSTODY VIOLATION"
  4. Verify error message contains table name "audit_log"
  5. Verify the record is UNCHANGED after the rejected operation
EXPECTED RESULT: UPDATE fails. Error message is clear and actionable. Record untouched.
EDGE CASES:
  - What if someone tries UPDATE ... SET details = details (no-op update)? Still must fail.
  - What if the UPDATE is inside a transaction that also INSERTs? INSERT should still succeed.
SEVERITY: Critical
LINKED STORY: CRDM v1.0 Principle 3; Tom B-001 P0-2
TESTABLE BEFORE UAT: Yes — requires P0-2 triggers deployed
```

---

## TOM-QA-007: Trigger Rejection — DELETE on case_evidence

```
SCENARIO: Attempt DELETE on immutable case_evidence table — must fail
MODULE: Fox (Evidence)
ROLE: System (automated — tests database constraint)
STORY: As the database, any attempt to DELETE a record from case_evidence must
       be rejected with a "CHAIN OF CUSTODY VIOLATION" error, protecting the
       Fox investigation evidence from destruction.
PRECONDITIONS:
  - P0-2 immutability triggers active on case_evidence
  - At least 1 evidence record exists in case_evidence
STEPS:
  1. Attempt: DELETE FROM canary_app.case_evidence WHERE id = <any_record>
  2. Verify the operation is REJECTED
  3. Verify error message contains "CHAIN OF CUSTODY VIOLATION"
  4. Verify error message contains table name "case_evidence"
  5. Verify the record STILL EXISTS after the rejected operation
  6. Verify the record's chain_hash is unchanged
EXPECTED RESULT: DELETE fails. Evidence preserved. Chain of custody maintained.
EDGE CASES:
  - What if someone tries DELETE with CASCADE from parent case table?
  - What if someone tries TRUNCATE TABLE? (Answer: TRUNCATE bypasses row triggers — need separate protection)
SEVERITY: Critical
LINKED STORY: CRDM v1.0 Principle 3; Tom B-001 P0-2; Fox Module Spec
TESTABLE BEFORE UAT: Yes — requires P0-2 triggers deployed
```

---

## Additional Scenarios Jim Adds (From Tom's "Handoff to Jim" Section)

### TOM-QA-008: Compensating INSERT Pattern

```
SCENARIO: Data correction via compensating INSERT (not UPDATE)
MODULE: Canary Core (Sales)
ROLE: System (automated)
STORY: When a data correction is needed (e.g., wrong amount ingested), the system
       creates a new compensating INSERT with a correction_flag and reference to
       the original record, rather than modifying the original.
PRECONDITIONS:
  - P0-1 immutability triggers active on canary_sales.transactions
  - Original transaction record exists with incorrect amount
STEPS:
  1. Attempt UPDATE on original transaction — verify REJECTED ("IMMUTABILITY VIOLATION")
  2. INSERT new compensating record with: correction_flag = TRUE, original_transaction_id = <original_id>, corrected fields
  3. Verify new record INSERTed successfully
  4. Verify original record is UNCHANGED
  5. Verify both records exist — original + correction
EXPECTED RESULT: Original preserved. Correction appended. Full audit trail maintained.
EDGE CASES:
  - What if correction record itself needs correction? (Chain of corrections)
  - What if original_transaction_id references a non-existent record?
SEVERITY: High
LINKED STORY: CRDM v1.0 Principle 3; Tom B-001 P0-1 Note #4
TESTABLE BEFORE UAT: Yes — requires P0-1 triggers
```

---

## Testability Summary

| Scenario | Requires Running App? | Requires PostgreSQL? | Requires Triggers? | Testable Before UAT? |
|----------|----------------------|---------------------|-------------------|---------------------|
| TOM-QA-001 | No | Yes | Yes (P0-3) | Yes, after Phase 3 |
| TOM-QA-002 | No | Yes | Yes (P0-3) | Yes, after Phase 3 |
| TOM-QA-003 | No | Yes (superuser) | Yes (P0-2, P0-3) | Yes, after Phase 3 |
| TOM-QA-004 | No | Yes | Yes (P0-3) | Yes, after Phase 3 |
| TOM-QA-005 | No | Yes | Yes (P0-3) | Yes, after Phase 3 |
| TOM-QA-006 | No | Yes | Yes (P0-2) | Yes, after Phase 3 |
| TOM-QA-007 | No | Yes | Yes (P0-2) | Yes, after Phase 3 |
| TOM-QA-008 | No | Yes | Yes (P0-1) | Yes, after Phase 3 |

**All 8 scenarios are testable via direct SQL against PostgreSQL.** None require the web application to be running. Jim can validate these as soon as Jeremy completes Sprint 5 Phase 3 (trigger deployment).

---

*Jim — QA Manager*
*Canary LP | Confidential*
*February 24, 2026*
