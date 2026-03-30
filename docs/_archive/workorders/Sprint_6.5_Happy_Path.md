---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Sprint 6.5 — Happy Path Integration Test

**Created:** March 1, 2026
**Owner:** Eva (tracking) + ALX (routing)
**Sprint Goal:** First true end-to-end integration test — login, OAuth, sale, webhook, CRDM, pipeline trace.
**Duration:** 5 working days
**Final Gate:** Jim runs the full flow cold, unassisted.

---

## The Flow (10 steps)

| Step | What Happens | Owner | Gate |
|------|-------------|-------|------|
| 1 | User hits `/login` | Jeremy | G1 |
| 2 | Login page → "Connect with Square" | Jeremy | G1 |
| 3 | Square OAuth redirect → callback → token stored | Jeremy | G1 |
| 4 | Session gets real merchant_id from OAuth | Jeremy | G1 |
| 5 | Webhook subscription auto-created for sandbox merchant | Jeremy | G1 |
| 6 | User does a sale on Square sandbox Dashboard/POS | Jim (test) | G2 |
| 7 | Square sends webhook → HMAC verified → stream published | Existing (works) | — |
| 8 | Sub 2 parses webhook → writes Transaction to DB | Jeremy | G2 |
| 9 | User sees transaction, clicks into detail | Jeremy + Art | G3 |
| 10 | User sees pipeline trace — how the event flowed | Jeremy + Tom | G4 |

---

## Gate 1: Login → OAuth → Session (Days 1–2)

**Owner:** Jeremy (build) + Tom (review)
**Triage ID:** B-081

| # | Task | Hours | File(s) |
|---|------|-------|---------|
| 1.1 | Register `square_oauth_bp` + `webhooks_tsp_bp` in `wsgi_b075.py` | 2h | `wsgi_b075.py` |
| 1.2 | Add `GET /login` route → renders `auth/login.html` with "Connect with Square" button | 1h | `wsgi_b075.py`, `templates/auth/login.html` |
| 1.3 | Modify `inject_demo_context()` → check session for OAuth merchant, redirect to `/login` if unauthenticated | 2h | `wsgi_b075.py` |
| 1.4 | Fix OAuth callback → store merchant_id + merchant_name in Flask session | 2h | `canary/blueprints/square_oauth_wired.py` |
| 1.5 | Fix `redirect_uri` → use CANARY_DOMAIN env var (default localhost:5050) | 0.5h | `canary/blueprints/square_oauth_wired.py` |
| 1.6 | Auto-subscribe webhooks on OAuth callback | 2h | `canary/blueprints/square_oauth_wired.py` |
| 1.7 | Replace all `DEMO_MERCHANT_ID` with `g.merchant_id` in views_wired.py | 1h | `canary/blueprints/views_wired.py` |

**Jim validates:** Login → OAuth → dashboard loads with real sandbox merchant name.

---

## Gate 2: Sub 2 — Parse Webhooks into CRDM (Days 2–3)

**Owner:** Jeremy (build) + Tom (review)
**Triage ID:** B-082

| # | Task | Hours | File(s) |
|---|------|-------|---------|
| 2.1 | Create `sub2_parse.py` consumer for `sub2-parse` group | 3h | `canary/services/tsp/consumers/sub2_parse.py` |
| 2.2 | Wire `webhook_router.py` → call existing parsers | 3h | `canary/services/webhook_router.py` |
| 2.3 | Write parsed data to CRDM tables (Transaction, LineItem, Tender) | 4h | `sub2_parse.py` |
| 2.4 | Create `run_sub2.py` launcher | 0.5h | `run_sub2.py` |
| 2.5 | Update ingestion_log status → `parsed` | 1h | `sub2_parse.py` |

**Jim validates:** Do $5.00 sale on Square sandbox. `SELECT * FROM transactions` shows CRDM fields.

---

## Gate 3: Transaction Detail + Click-Through (Days 3–4)

**Owner:** Jeremy (frontend) + Art (review)
**Triage ID:** B-083

| # | Task | Hours | File(s) |
|---|------|-------|---------|
| 3.1 | Create `transaction_detail.html` template | 3h | `templates/transaction_detail.html` |
| 3.2 | Add `GET /transactions/<id>` route | 2h | `canary/blueprints/views_wired.py` |
| 3.3 | Add click-through links on `/transactions` table | 0.5h | `templates/transactions.html` |
| 3.4 | Backend filtering — date, employee, type | 3h | `canary/blueprints/views_wired.py` |
| 3.5 | CRDM field mapping display + raw payload side-by-side | 2h | `templates/transaction_detail.html` |

**Jim validates:** Click transaction → see CRDM fields + raw Square JSON.

---

## Gate 4: Pipeline Trace (Days 4–5)

**Owner:** Jeremy (build) + Tom (review)
**Triage ID:** B-084

| # | Task | Hours | File(s) |
|---|------|-------|---------|
| 4.1 | Create `GET /api/trace/<event_id>` endpoint | 3h | `canary/blueprints/views_wired.py` |
| 4.2 | Create `pipeline_trace.html` template | 3h | `templates/pipeline_trace.html` |
| 4.3 | Link from transaction detail → "View Pipeline Trace" | 0.5h | `templates/transaction_detail.html` |
| 4.4 | Timeline: Received → Sealed → Parsed → Batched with timestamps | 2h | `templates/pipeline_trace.html` |

**Jim validates:** Trace the $5.00 sale through all 4 pipeline steps.

---

## Gate 5: Jim Integration Test (Day 5)

| # | Step | Pass/Fail Criteria |
|---|------|-------------------|
| 5.1 | Start wsgi_b075 + Sub 1 + Sub 2 + Sub 3 | All 4 start clean |
| 5.2 | Hit localhost:5050 → `/login` | Login page renders |
| 5.3 | Click "Connect with Square" → OAuth | Callback succeeds |
| 5.4 | Dashboard loads with real merchant name | Not "Sunrise Coffee" |
| 5.5 | Create $5.00 sale on Square sandbox | Sale completes |
| 5.6 | Refresh `/transactions` | Transaction appears <30s |
| 5.7 | Click transaction row | Detail page with CRDM fields |
| 5.8 | Click "Pipeline Trace" | 4-step flow with timestamps |

---

## Prerequisites

- Jeffe: Sandbox merchant credentials active
- Jeremy: Docker + Valkey running, ngrok/tunnel URL ready
- Jim: Square sandbox dashboard access

## Out of Scope

- Keycloak / JWT (Flask session only)
- Chirp detection (no alerts fire)
- Alert detail page
- Settings save
- Mobile companion
- Production credentials
- CSRF / rate limiting

---

*Classification: Internal — Sprint Planning*
