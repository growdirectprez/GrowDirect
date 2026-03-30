---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Jim QA Report — Sprint 6.5 Gate 5 Cold-Run
**Date:** March 1, 2026
**Sprint:** 6.5 — Happy Path Integration Test
**Triage ID:** B-085
**Owner:** Jim (QA Manager)
**Status:** RUNTIME PARTIAL PASS | 3 BUGS FOUND + FIXED | Steps 5.5–5.7 awaiting Jeffe sandbox sale

---

## Executive Summary

All 9 Sprint 6.5 deliverables are on disk and code-reviewed. Gates 1–4 pass code-level QA. B-078/079/080-P1 security: 12/12 PASS. Runtime testing unblocked after Docker PATH fix and revealed **3 integration bugs** — all fixed in-session:

1. **BUG (JQ-005):** `wsgi_b075.py` never called `db_factory.init_app(app)` — Sub 1/2/3 consumers crashed with NoneType on every message. **FIXED:** Added `db_factory.init_app(app)` to boot block.
2. **BUG (JQ-006):** DB URLs not wired into Flask `app.config` — session factory fell back to wrong password (`canary:canary` instead of `canary:canary_dev_2026`). **FIXED:** Added `app.config["CANARY_*_DB_URL"]` from env vars with correct defaults.
3. **BUG (JQ-008):** OAuth authorize redirect sent `client_id=None` — code used `SQUARE_APP_ID` but `.env` defines `SQUARE_APPLICATION_ID`. **FIXED:** Find-replace in `square_oauth_wired.py` + `startup_validator.py`.

**Runtime results:** Steps 5.1–5.4 + 5.8 PASS. Steps 5.5–5.7 require Jeffe to create a sale on Square sandbox Dashboard.

**Process gap identified:** No preflight validation exists. Config mismatches, stale containers, broken symlinks all surfaced during test. Preflight script needed.

---

## Gate 5 Prerequisite Check

| Prerequisite | Status | Notes |
|---|---|---|
| Docker Engine | **NOT INSTALLED** | `docker` command not found. Hard blocker. |
| PostgreSQL container | BLOCKED | Requires Docker |
| Valkey container | BLOCKED | Requires Docker |
| Python 3 | AVAILABLE | Python 3.9.6 at /usr/bin/python3 |
| Virtual environment | AVAILABLE | `venv/` directory exists |
| Docker Compose configs | ON DISK | 5 variants in `devops/` |

**Action Required:** Install Docker Desktop for Mac, then re-run Gate 5.

---

## Deliverable Inventory — All Present

| Gate | File | Status | Size | Last Modified |
|---|---|---|---|---|
| G1 | `wsgi_b075.py` | ON DISK | 7.4 KB | Mar 1 17:28 |
| G1 | `canary/blueprints/square_oauth_wired.py` | ON DISK | 8.3 KB | Mar 1 19:12 |
| G1 | `templates/auth/login.html` | ON DISK | 9.1 KB | Mar 1 17:32 |
| G1 | `canary/blueprints/views_wired.py` | ON DISK | 50.7 KB | Mar 1 17:39 |
| G2 | `canary/services/tsp/consumers/sub2_parse.py` | ON DISK | 11.6 KB | Mar 1 17:36 |
| G2 | `run_sub2.py` | ON DISK | 1.2 KB | Mar 1 17:36 |
| G3 | `templates/transaction_detail.html` | ON DISK | 9.1 KB | Mar 1 17:38 |
| G3 | `templates/transactions.html` | ON DISK | 2.5 KB | Mar 1 19:13 |
| G4 | `templates/pipeline_trace.html` | ON DISK | 4.6 KB | Mar 1 17:40 |

Supporting files: `run_sub1.py` (1.1 KB), `run_sub3.py` (1.1 KB), `requirements.txt` (1.8 KB) — all present.

---

## Code Review Results

### Gate 1: Login → OAuth → Session — PASS

| Check | Result | Notes |
|---|---|---|
| Blueprint registration (square_oauth_bp, webhooks_tsp_bp) | PASS | wsgi_b075.py lines 156–169, try/except wrapped |
| GET /login route | PASS | Lines 108–122, checks existing session |
| inject_merchant_context() auth check | PASS | Lines 66–91, redirects to /login if unauthenticated |
| OAuth callback → session population | PASS | merchant_id + merchant_name stored in Flask session |
| redirect_uri via CANARY_DOMAIN | PASS | Env var with localhost:5050 default |
| Auto-subscribe webhooks | PASS | Called after token exchange |
| DEMO_MERCHANT_ID eliminated | PASS | All 10 routes use g.merchant_id |
| CSRF state parameter validation | PASS | State checked before token exchange |

**Findings:**

| ID | Severity | Description | File:Line | Recommendation |
|---|---|---|---|---|
| JQ-001 | MEDIUM | `Transaction.id.startswith(txn_id)` — UUID prefix match is semantically risky | views_wired.py:497 | Use exact UUID match or document prefix behavior |
| JQ-002 | LOW | Token DB storage commit not wrapped in try/except | square_oauth_wired.py:83 | Add try/except; continue to session on failure |
| JQ-003 | LOW | Generic exception logging lacks type info | views_wired.py:570 | Log exception class name for debugging |

---

### Gate 2: Sub 2 Parse Consumer — PASS

| Check | Result | Notes |
|---|---|---|
| Consumer pattern matches Sub 1/Sub 3 | PASS | XREADGROUP → process → XACK, identical structure |
| 7 event type families routed | PASS | payment, refund, order, inventory, labor, gift_card, cash_drawer |
| CRDM table writes | PASS | Transaction, LineItem, Tender + auxiliary tables |
| ingestion_log status → 'parsed' | PASS | Status update + processed_at timestamp |
| Duplicate detection | PASS | Unique constraint handled gracefully |
| Dead letter routing | PASS | Malformed/unprocessable messages routed out |
| Error ceiling (10 consecutive) | PASS | Matches Sub 1/Sub 3 pattern |
| Launcher (run_sub2.py) | PASS | Identical structure to run_sub1.py / run_sub3.py |

**Findings:**

| ID | Severity | Description | File:Line | Recommendation |
|---|---|---|---|---|
| JQ-004 | LOW | Consumer name collision risk in multi-worker (hostname-only) | sub2_parse.py:31 | Add PID or ULID suffix. Sprint 6.6 item. Inherited from Sub 1. |

---

### Gate 3: Transaction Detail + Click-Through — PASS

| Check | Result | Notes |
|---|---|---|
| 4-panel layout | PASS | Payment, Card/Security, Context, Pipeline |
| CRDM field mapping display | PASS | All 24 fields rendered |
| Raw JSON payload display | PASS | Conditional, scrollable, tojson filter |
| Click-through from transactions table | PASS | Row onclick + yellow TXN ID link |
| Filter chips with active state | PASS | Jinja conditional class application |
| Items column bracket notation | PASS | `txn['items']` not `txn.items` |
| Link to Pipeline Trace | PASS | Button to `/api/trace/{{ txn.full_id }}` |

**Findings:** None.

---

### Gate 4: Pipeline Trace — PASS

| Check | Result | Notes |
|---|---|---|
| 4-step vertical timeline | PASS | Received → Sealed → Parsed → Batched |
| Status indicators (3 states) | PASS | complete (yellow), pending (gray), unknown (red) |
| Timestamps per step | PASS | Rendered in step footer |
| Connector lines between steps | PASS | Color matches step status |
| Graceful pending/unknown display | PASS | No hard failures |
| Legend | PASS | All 4 steps documented |

**Findings:** None.

---

## B-078/079/080-P1 Security Carry-Forward — ALL PASS

| ID | Check | Result | Evidence |
|---|---|---|---|
| B-078.1 | HMAC: Base64 + compare_digest | PASS | square.py:40–71, webhooks_wired.py:28–35 |
| B-078.2 | JWT: PyJWT 2.x + JWKS cache | PASS | jwt_auth.py:1–109, thread-safe 5min TTL |
| B-078.3 | No missing imports | PASS | All blueprint files compile clean |
| B-079.1 | `__init__.py` delegates to registry | PASS | Single import, `__all__` exports |
| B-079.2 | registry.py single source | PASS | 12 blueprints, safe registration |
| B-079.3 | Consumers wired to wsgi_b075 | PASS | webhooks_tsp on wsgi_b075.py:164 |
| B-080.1 | No SQL injection | PASS | All queries parameterized (%s) |
| B-080.2 | No hardcoded secrets | PASS | Dev defaults marked; prod validation enforced |
| B-080.3 | Config.validate() at startup | PASS | wsgi_b075.py:179–183 |
| B-080.4 | TenantMixin applied | PASS | All tenant-scoped models inherit |
| B-080.5 | Open redirect protection | PASS | All redirects use Flask url_for() |
| B-080.6 | No sensitive data logged | PASS | No tokens/passwords in log output |

---

## Gate 5 Cold-Run Status

| Step | Description | Status |
|---|---|---|
| 5.1 | Start wsgi_b075 + Sub 1 + Sub 2 + Sub 3 | **PASS** — all 4 services running after JQ-005/006 fixes |
| 5.2 | Hit localhost:5050 → /login | **PASS** — 302 redirect to /login?reason=login_required |
| 5.3 | Click "Connect with Square" → OAuth | **PASS** — /oauth/sandbox → 302 → /dashboard |
| 5.4 | Dashboard with real merchant name | **PASS** — "Square Merchant" / "Sunrise Coffee — Torrance" |
| 5.5 | Create $5.00 sale on Square sandbox | **WAITING** — Jeffe needs to create sale in Square sandbox Dashboard |
| 5.6 | Refresh /transactions → transaction appears | **WAITING** — depends on 5.5 |
| 5.7 | Click transaction → detail page | **SCAFFOLDING PASS** — route works, falls back to list for demo data. Needs real DB data from 5.5 |
| 5.8 | Pipeline Trace → 4-step flow | **PASS** — 4-step timeline renders with status indicators, graceful degradation for unknown events |

---

## Runtime Bugs Found and Fixed

| ID | Severity | Description | Root Cause | Fix Applied |
|---|---|---|---|---|
| JQ-005 | **CRITICAL** | Sub 1/2 consumers crash on every message: `'NoneType' object has no attribute 'rollback'` | `wsgi_b075.py` never called `db_factory.init_app(app)`. DB session factory singleton created empty at module import. Consumers got None sessions. | Added `db_factory.init_app(app)` to wsgi_b075.py boot block (line 184) |
| JQ-006 | **HIGH** | Sub 1 auth failure: `FATAL: password authentication failed for user "canary"` | DB URLs not in Flask `app.config`. Session factory fell back to hardcoded default `canary:canary` instead of `canary:canary_dev_2026` from docker-compose. | Added `app.config["CANARY_*_DB_URL"]` from env vars with correct defaults (lines 50–57) |
| JQ-008 | **HIGH** | OAuth blank page — `client_id=None` in authorize redirect | `square_oauth_wired.py` used `SQUARE_APP_ID` but `.env` defines `SQUARE_APPLICATION_ID`. Same for SECRET. `startup_validator.py` had same mismatch. | Find-replace in `square_oauth_wired.py` + `startup_validator.py`: `SQUARE_APP_ID` → `SQUARE_APPLICATION_ID`, `SQUARE_APP_SECRET` → `SQUARE_APPLICATION_SECRET` |

**Environment issues also resolved:**
- Docker symlinks broken by macOS App Translocation → fixed by user (re-pointed to /Applications/Docker.app/)
- Stale containers running old code on :5001 → stopped (only Postgres + Valkey remain)
- `.env` file configured for old stack (sqlite/:5001) → env vars passed directly for Sprint 6.5

---

## Process Gap: Preflight Validation Missing

**Root cause of repeated config issues:** No automated check validates the environment before testing. Every session discovers mismatches manually.

**Preflight checklist (spec for Jeremy to build):**
1. Docker daemon running
2. Required containers healthy (Postgres, Valkey)
3. No stale app containers (canary_flask on wrong code)
4. Port 5050 available (or identify what's on it)
5. DB connectivity test (connect to all 3 databases with credentials)
6. DB schema tables exist (evidence_records, transactions, etc.)
7. Valkey stream client connects (DB 4)
8. Required env vars present and non-empty
9. `pip show squareup` confirms v44+ (standing directive B-063)
10. No process listening on conflicting ports

**Recommendation:** `make preflight` target. Runs before `make run`. Fails loud if anything is wrong.

---

## QA Verdict

**Code-Level QA: APPROVED**
- Gates 1–4: All pass code review
- B-078/079/080-P1: 12/12 security items validated

**Runtime QA: PARTIAL PASS**
- Steps 5.1–5.4 + 5.8: PASS (after JQ-005/006 fixes)
- Steps 5.5–5.7: WAITING on Jeffe sandbox sale
- 2 critical/high bugs found and fixed in-session

**Jim's recommendation:** Jeffe creates a $5.00 sale on Square sandbox Dashboard. If the webhook fires and transaction appears on /transactions, steps 5.6–5.7 will complete the gate. The infrastructure and code are now clean.

---

## Findings Summary

| ID | Gate | Severity | Description | Owner | Sprint |
|---|---|---|---|---|---|
| JQ-001 | G1 | MEDIUM | UUID startsWith() prefix match | Jeremy | 6.5 |
| JQ-002 | G1 | LOW | Token DB commit needs try/except | Jeremy | 6.6 |
| JQ-003 | G1 | LOW | Exception logging lacks type info | Jeremy | 6.6 |
| JQ-004 | G2 | LOW | Consumer name collision risk | Jeremy | 6.6 |
| JQ-005 | G5 | **CRITICAL** | DB factory never initialized — consumers crash | **FIXED** | 6.5 |
| JQ-006 | G5 | **HIGH** | DB password mismatch — config not in app.config | **FIXED** | 6.5 |
| JQ-007 | Process | **HIGH** | No preflight validation script exists | Jeremy | 6.5 |
| JQ-008 | G1 | **HIGH** | OAuth env var name mismatch — `SQUARE_APP_ID` vs `SQUARE_APPLICATION_ID` | **FIXED** | 6.5 |

---

*QA Manager: Jim*
*Classification: Internal — QA Report*
