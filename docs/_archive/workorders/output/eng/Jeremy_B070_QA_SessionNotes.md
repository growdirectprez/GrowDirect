---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Jeremy Session Notes — B-070: QA/UAT Gate (Sandbox Testing)

**Date:** March 1, 2026 (executed Feb 28 evening)
**Branch:** `sprint-6-beta` at `c99b3f8`
**Dispatch:** `_ALX/WorkOrders/dispatches/Jeremy_B070_ProductionCutover_SessionPrompt.md`
**Pivot:** Jeffe redirected from production cutover to QA/UAT sandbox testing on iMac.

---

## Session Summary

Originally dispatched for production cutover (sandbox → live). Jeffe redirected: "not ready for production yet — we should be packaging for sandbox testing against QA on the iMac." First clean branching workflow established.

---

## Deliverables

### 1. Git Branching Model Established (FIRST TIME)

```
main                        @ 0bfc9b1   (stable — untouched)
alpha-clean                 @ 72d0082   (Sprint 5 baseline)
sprint-6-tsp                @ c99b3f8   (alpha/dev — where code gets written)
sprint-6-beta               @ c99b3f8   (QA — cut from alpha for iMac testing)
sprint-5-baseline (tag)     @ 72d0082   (tag)
```

**Rule:** Code is written on `sprint-6-tsp`. When clean, cut beta. Beta goes to iMac. Nothing merges to `main` until Jim signs off.

### 2. B-067 Explorer Committed

Previously untracked B-067 files (Jim QA PASSED) committed to `sprint-6-tsp`:
- `canary/blueprints/square_explorer_wired.py` (22 lines)
- `canary/services/square_capability_explorer.py` (415 lines)
- `static/square_explorer.html` (1,260 lines)
- `wsgi_alpha3x.py` (1 line — blueprint registration)

Commit: `d040f24`

### 3. Migration Idempotency Fix

**Problem:** `canary_deploy.sh --full` does teardown → fresh DB → run all migrations. Migration `000` calls `SalesBase.metadata.create_all()` which creates ALL tables/columns from current Python models. Migrations `004`, `005`, `006` then fail with "already exists" errors because:
- `004` adds columns that `000` already created (source_event_id, event_hash, ip_address, user_agent)
- `005` creates `evidence_records` table that `000` already created
- `006` creates `inscription_pool` + `event_inscriptions` tables that `000` already created

**Fix:** Added IF NOT EXISTS guards using `information_schema` lookups:
- `004`: `_column_exists()`, `_constraint_exists()`, `_index_exists()` helpers
- `005`: `_table_exists()` — returns early if table exists
- `006`: `_table_exists()` — returns early if table exists

Commit: `c99b3f8`

### 4. iMac QA Deploy

**Deploy result:**
| Component | Status |
|---|---|
| Branch | `sprint-6-beta` @ `c99b3f8` |
| Services | 7/7 UP (postgres, valkey, pgbouncer, flask, superset, airflow-web, airflow-scheduler) |
| Migrations | ALL GREEN — app (004), sales (006), metrics (000) |
| Tests | 541 pass / 43 fail (pre-existing) / 31 skip |
| Health | `http://192.168.10.117:5002/health` → 200 OK |
| Explorer | `http://192.168.10.117:5002/explorer` → 200 OK |
| Elapsed | 13m 16s |

**Note:** Flask external port is **5002** (not 5001) per `.env.alpha3x` override.

**Note:** The 43 test failures are pre-existing (Jim's backlog — see HANDOFF). Not introduced by this deploy.

**Note:** iMac had dirty working tree (`devops/seeds/level_b_demo.py` modified locally). Stashed before checkout. Stash preserved at `stash@{0}`.

### 5. .gitignore Cleanup

Added `.git-old/` to `.gitignore`, removed tracked `.bak` lock files. Commit: `ecbbb8a`.

---

## Commits (this session)

| Hash | Message |
|---|---|
| `d040f24` | feat(B-067): Square Capability Explorer — 16/16 families, Jim QA PASSED |
| `ecbbb8a` | chore: gitignore .git-old/ debris, remove tracked lock backups |
| `c99b3f8` | fix(migrations): idempotent guards on sales 004/005/006 |

---

## Verified Endpoints (QA iMac)

- `http://192.168.10.117:5002/health` → 200 (`{"service":"canary-flask","status":"healthy","version":"alpha3x"}`)
- `http://192.168.10.117:5002/explorer` → 200

---

## Outstanding / Next

- **Production cutover (B-070 original scope):** DEFERRED — Jeffe will greenlight when ready
- **43 pre-existing test failures:** Jim to classify (legit skip vs. real risk)
- **Demo seed data:** May need re-run (`level_b_demo.py`) if companion demo is needed
- **Port documentation:** Flask is on 5002 externally on iMac QA — update deploy skill references if needed

---

*Session by Jeremy | March 1, 2026*
*B-064 Heartbeat Rule: QA/UAT gate — sandbox validation on iMac*
