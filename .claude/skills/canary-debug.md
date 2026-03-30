---
name: canary-debug
description: |
  Systematic debugging for Canary. Use when encountering any bug, test failure,
  or unexpected behavior — before proposing fixes. Four-phase root cause
  investigation with Canary-specific debugging surfaces. Replaces
  superpowers:systematic-debugging.
allowed-tools:
  - Read
  - Bash
  - Edit
  - Write
  - Grep
  - Glob
---

# Canary Debug — Systematic Debugging

> "The problem was never the people. The problem was the log."

## Overview

Random fixes waste time and create new bugs. Find root cause first. Always.

**Core principle:** ALWAYS find root cause before attempting fixes.

**Announce at start:** "I'm using canary-debug for root cause investigation."

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

---

## Phase 1: Root Cause Investigation

1. **Read error messages carefully** — full stack traces, line numbers, error codes
2. **Reproduce consistently** — if not reproducible, gather more data
3. **Check recent changes** — `git log --oneline -10`, `git diff HEAD~3 --stat`
4. **Check Canary debugging surfaces in order:**

**A. Health & Stack:**
```bash
curl -s http://localhost:5001/health
docker compose -f docker-compose.dev.yml ps
docker exec canary-db psql -U canary -d canary -c "SELECT 1;"
docker exec canary-valkey valkey-cli ping
```

**B. TSP Pipeline (Triple Subscriber Pipeline):**
- Sub 1: Raw seal (legal witness)
- Sub 2: Business logic parse
- Sub 3: Bitcoin anchor

**C. Database Integrity:**
```bash
# Orphaned rows
docker exec canary-db psql -U canary -d canary -c "
  SELECT count(*) FROM app.alerts
  WHERE merchant_id NOT IN (SELECT id FROM app.merchants);"

# INSERT-only triggers
docker exec canary-db psql -U canary -d canary -c "
  SELECT tgname, tgrelid::regclass FROM pg_trigger WHERE tgname LIKE 'enforce_%';"
```

5. **Trace data flow — the six-node pipeline:**
```
Node 1: Square webhook -> TSP ingestion
Node 2: Sub 1 -> raw seal, legal witness
Node 3: Sub 2 -> parse, route, CRDM tables
Node 4: Detection rules -> Chirp alerts
Node 5: Fox case -> investigation, evidence chain
Node 6: Sub 3 -> Bitcoin ordinal, gLog
```

Where in this chain does data go wrong? Trace backward from the symptom.

**Common pipeline breaks:**
- Data arrives at Node 1 but not Node 3 -> subscriber issue
- Data at Node 3 but detection doesn't fire -> rule config or threshold
- Detection fires but dashboard doesn't show it -> route/query issue

---

## Phase 2: Pattern Analysis

1. Find working examples in the codebase
2. Compare working vs broken
3. Check memory: `memory_recall("similar issue")`
4. Read the SDD for intended behavior

## Phase 3: Hypothesis and Testing

1. Form one hypothesis with reasoning
2. Test minimally — one change, one variable
3. Verify — did it work? Yes -> Phase 4. No -> new hypothesis.
4. Don't stack fixes. One at a time.

## Phase 4: Implementation

1. Write failing test reproducing the bug (use canary-tdd)
2. Implement single fix addressing root cause
3. Verify: test passes, smoke tests pass, no regressions

## The 3-Fix Rule

```
Fix 1 fails -> Return to Phase 1 with new information
Fix 2 fails -> Return to Phase 1, question your assumptions
Fix 3 fails -> STOP. This is an architecture problem. Escalate.
```

---

## Common Canary Bug Patterns

| Symptom | Likely Root Cause | Check First |
|---------|-------------------|-------------|
| Alert not firing | Rule disabled or threshold wrong | `app.merchant_rule_configs` |
| Webhook 401 | HMAC signature mismatch | Square webhook secret in `.env` |
| Dashboard shows stale data | Valkey cache not invalidated | Cache TTL |
| Missing transactions | TSP subscriber failed silently | TSP logs |
| FK violation on INSERT | Using `merchant_id` (Square) not `id` (UUID) | Model FKs |
| Template render error | Jinja2 context missing variable | Blueprint route handler |
| Docker service won't start | Port conflict or env var missing | `docker compose logs` |

---

*Canary Debug v1.0 — Systematic Debugging*
*Replaces: superpowers:systematic-debugging*
