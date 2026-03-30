---
name: canary-verify
description: |
  Verification before completion. Use before claiming work is complete, fixed,
  or passing — before committing or creating PRs. Evidence before assertions.
  Replaces superpowers:verification-before-completion.
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---

# Canary Verify — Verification Before Completion

> "We don't want to add to the stress. We want to ease it."
> — Jeffe, Feb 26, 2026

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Announce at start:** "I'm using canary-verify to confirm this work is complete."

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the command in this session, you cannot claim it passes.

---

## The Gate — Five Steps

```
1. IDENTIFY: What command proves this claim?
2. RUN: Execute the full command (fresh, not cached)
3. READ: Full output. Check exit code. Count failures.
4. VERIFY: Does output confirm the claim?
   - NO -> State actual status with evidence
   - YES -> State claim WITH evidence
5. ONLY THEN: Make the claim
```

Skip any step = lying, not verifying.

---

## Canary Verification Checklist

### Code Quality
```bash
# Unit tests
python3 -m pytest tests/unit/ -v
# Expected: All pass, 0 failures

# Smoke tests
python3 -m pytest tests/smoke/ -v --timeout=30
# Expected: All pass, no regressions

# Integration tests (if plan requires)
python3 -m pytest tests/integration/ -m postgres -v
```

### App Health
```bash
# Health endpoint responds
curl -s http://localhost:5001/health | python3 -m json.tool
# Expected: 200 OK, all services healthy

# No Python errors in logs
docker compose -f docker-compose.dev.yml logs --tail=50 canary-app | grep -i error
# Expected: No unexpected errors
```

### Data Integrity (if touching canary_sales)
```bash
# INSERT-only triggers intact
docker exec canary-db psql -U canary -d canary -c "
  SELECT tgname FROM pg_trigger WHERE tgname LIKE 'enforce_%';
"
# Expected: All immutability triggers present

# No orphaned rows
docker exec canary-db psql -U canary -d canary -c "
  SELECT count(*) FROM app.alerts
  WHERE merchant_id NOT IN (SELECT id FROM app.merchants);
"
# Expected: 0
```

### Guardian Manifest (if protected files modified)
```bash
cat .guardian-manifest
# Expected: SHA256 hashes updated for modified files
```

### Pipeline Completeness (if touching a service or data route)

**This is the verification that catches lazy pipes. Do not skip it.**

```bash
# 1. Data goes IN — prove the write
python3 -m pytest tests/integration/test_<service>_write.py -v
# Show: row inserted, returned ID, correct schema

# 2. Data comes OUT — prove the read
python3 -m pytest tests/integration/test_<service>_read.py -v
# Show: row retrieved, fields match what was written

# 3. Row counts — prove nothing was lost or duplicated
docker exec canary-db psql -U canary -d canary -c "
  SELECT schemaname, relname, n_live_tup
  FROM pg_stat_user_tables
  WHERE relname = '<table>';
"
# Show: count before, action, count after, delta = expected

# 4. Route responds — prove the API contract
curl -s http://localhost:5001/<route> | python3 -m json.tool
# Show: 200 OK, payload matches SDD

# 5. End-to-end — prove the full pipe
# Input -> service -> model -> database -> query -> response
# If any link in this chain is stubbed, hardcoded, or TODO'd — NOT DONE.
```

**"Tests pass" is not enough. Show the data. Count the rows. Verify the content.**

### Pipeline Architecture (if touching any pipeline node)

```
-> Does this feature maintain merchant-first isolation?
-> Does this feature connect to the gLog where it should?
-> Does this feature respect the Canonical UUID Principle?
```

### Broader QA (if shipping or branch is complete)

Run `canary-qa` in diff-aware mode for a full surface sweep. canary-verify
proves individual claims; canary-qa proves the branch works end-to-end
across all affected routes, services, and data flows.

### Linear Issue
```
-> GRO issue status updated?
-> Acceptance criteria checked off?
-> If blocked on anything, is TRIAGE.md updated?
```

---

## North Star Check

Before declaring done, two questions:

> 1. Does this feature reduce the merchant's cognitive load?
> If it requires recovery steps, explanation, or back-and-forth — it fails.

> 2. Does this feature advance the tLog-to-gLog evolution?
> If it creates mutable state where immutable state would serve better — question it.

---

## Red Flags — STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before running verification ("Done!", "Perfect!")
- About to commit without running tests
- Relying on a previous test run (not this session)
- "Just this once"
- ANY wording implying success without evidence

---

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| "Tests pass" | Test output: 0 failures | Previous run, "should pass" |
| "Build works" | Health endpoint: 200 OK | "No errors in code" |
| "Bug fixed" | Failing test now passes | "Changed the code" |
| "No regressions" | Full smoke suite green | "Only changed one file" |
| "Data integrity preserved" | Trigger check + orphan check | "Didn't touch sales schema" |
| "Route works" | curl showing correct JSON payload | "Route exists and returns 200" |
| "Pipeline complete" | End-to-end: input -> DB -> query -> response | "Each piece works individually" |

---

*Canary Verify v1.0 — Verification Before Completion*
*Replaces: superpowers:verification-before-completion*
