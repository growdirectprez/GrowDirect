---
type: spec
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# B-066 Questions Document — Square SDK + TSP Coding Standards Review
**Work Order:** B-066 Phase 1
**Author:** Condor
**Date:** February 28, 2026
**Status:** DELIVERED — requires Jeffe resolution (marked) or Condor's call (marked)
**Gates:** Jeremy's next TSP session + B-067-B wiring pass

---

## Bucket 1: Ring-Fencing Architecture

### Q1.1: Where does the Square SDK boundary sit?
**Context:** Two layers of Square integration exist today:
- **Pre-B-065 layer** (`square_client.py` at repo root, 1,278 lines): Full-featured client with OAuth flow, payment/order/cash drawer fetching, webhook processing. Uses mixed SDK patterns — detects v35 legacy vs v42+ imports at runtime.
- **TSP layer** (Sprint 6 pipeline): Clean v44 SDK usage via `from square import Square`. `square_webhook_manager.py` uses `client.webhooks.subscriptions.*`. Validators use manual HMAC.

**Question:** Is `square_client.py` the ring-fence boundary (everything Square goes through it), or does TSP maintain its own direct SDK access? The two layers currently don't share code.

**Condor's recommendation:** TSP pipeline owns its own SDK access. `square_client.py` is pre-TSP legacy. The ring-fence boundary should be: **any code that calls `Square()` or reads from a Square API response lives inside `canary/services/tsp/` or `canary/services/square_*.py`**. Nothing in blueprints, models, or other services reaches into Square objects directly.

**Resolution needed:** ☐ Condor's call — codified in Standards Doc Section 1.

---

### Q1.2: Existing parsers — keep, replace, or wrap?
**Context:** Six parser files exist in `canary/services/parsers/`:
- `square_payment_parser.py` (103 lines) — `parse_payment()`, `parse_refund()`
- `square_order_parser.py` (94 lines) — `parse_order_line_items()`, `parse_order_tenders()`
- `square_auxiliary_parsers.py` (150 lines) — cash drawer shifts/events, timecards, inventory, gift cards

These parsers extract Square webhook payloads into normalized dicts. TSP-04 (Sub 2 Parse & Route) specifies its own parsers for Phase 1 event types. The existing parsers pre-date TSP and use different field naming conventions.

**Question:** Does Sub 2 consume the existing parsers, replace them with TSP-04 spec'd parsers, or wrap them?

**Condor's recommendation:** Replace. TSP-04 specifies exact field names aligned to CRDM tables. The existing parsers generate UUIDs locally (`generate_uuid()`) instead of using the TSP ULID assignment from TSP-01. They also lack `merchant_id` partitioning awareness. Build TSP-04 parsers from scratch per PRD. Keep existing parsers as reference only — do not import from them.

**Resolution needed:** ☐ Condor's call — codified in Standards Doc Section 9.

---

### Q1.3: `square_client.py` at root — dead code?
**Context:** `Canary/square_client.py` (1,278 lines) sits at the repo root, outside the `canary/` package. It was the original Square integration before TSP. Contains:
- SDK version detection (v35 vs v42+)
- OAuth authorization URL generation + token exchange
- Payment, order, cash drawer, timecard fetching
- Webhook event processing
- Extensive TODOs from Jeremy

TSP pipeline does not import from it. `square_webhook_manager.py` (B-065) duplicates some of its functionality with v44 SDK patterns.

**Question:** Is this file dead code? Should it be removed, archived, or does it serve a purpose that TSP doesn't cover yet (e.g., the OAuth flow, the polling fetch methods)?

**Condor's recommendation:** Not dead — it contains OAuth flow logic that TSP doesn't replicate yet. But it must not be imported by TSP code. Tag it `# LEGACY — do not import from TSP pipeline` at the top. When Jeremy builds the OAuth blueprint, he should lift the OAuth patterns from here and rewrite using v44 SDK's `client.o_auth.obtain_token()` / `client.o_auth.renew_token()`.

**Resolution needed:** ☐ Condor's call — noted in Standards Doc Section 1.

---

### Q1.4: Manual HMAC vs SDK `verify_signature()` — which wins?
**Context:** Two implementations exist:
1. **TSP validator** (`validators/square.py`, lines 47-72): Manual HMAC-SHA256 using `hmac.new()`, builds `notification_url + raw_body` string, Base64 encodes, `hmac.compare_digest()`.
2. **SDK helper** (`webhooks_helper.py`): Identical algorithm — `hmac.new(key, notification_url + request_body, sha256)`, Base64, `hmac.compare_digest()`.

Jeremy's scan notes confirm: "Our TSP manual implementation matches exactly. Switching to SDK helper would be cosmetic, not functional."

**Question:** SDK-first policy says use SDK for everything it supports. But the TSP validator is already passing against 26 real Square webhooks. Switch to SDK helper or keep manual?

**Condor's recommendation:** Switch to SDK helper. The algorithm is identical, but:
- SDK helper raises `ValueError` on empty `signature_key` or `notification_url` — our manual version returns `RuntimeError`. SDK is stricter.
- SDK helper takes keyword-only args (`*, request_body, signature_header, signature_key, notification_url`) — prevents argument ordering bugs.
- When Square changes their signature scheme (unlikely but possible), the SDK helper updates with the package. Our manual version doesn't.
- Cost: ~15 minutes to swap. Risk: zero — algorithm is identical.

**Resolution needed:** ☐ Condor's call — codified in Standards Doc Section 2.

---

## Bucket 2: TSP Structure vs. What Square Actually Sends

### Q2.1: Does TSP-01 correctly model the full Square refund object?
**Context:** TSP-01 receives all webhook events at `POST /webhooks/square`. The `parse_refund()` in the existing payment parser extracts: `id`, `payment_id`, `amount_money`, `reason`, `location_id`, `team_member_id`. But the Square refund object contains additional fields: `order_id`, `processing_fee_money`, `status`, `created_at`, `updated_at`, and `unlinked` (a boolean for unlinked refunds not tied to a payment).

**Question:** Is TSP-01's hash-before-parse invariant sufficient here, or does Sub 2 need a refund parser that captures all fields the CRDM `refund_links` table expects?

**Condor's finding:** TSP-01 is correct — it hashes the raw bytes and passes the full payload to Valkey. Sub 2 (TSP-04) is where field extraction happens. The existing `parse_refund()` is incomplete for CRDM compliance — it misses `order_id`, `processing_fee_money`, and `unlinked`. The TSP-04 Phase 1 parser needs to cover all `refund_links` columns.

**Resolution needed:** ☐ Condor's call — flagged in Standards Doc Section 10 as PRD addendum for TSP-04.

---

### Q2.2: Which event types does Sub 2 handle Phase 1 vs Phase 2?
**Context:** TSP-04 specifies 5 Phase 1 parsers but `square_webhook_manager.py` subscribes to 7 event types: `payment.created`, `payment.updated`, `refund.created`, `refund.updated`, `inventory.count.updated`, `order.created`, `order.updated`.

TSP-04 Phase 1 parsers listed: `payment.created`, `refund.created`, `cash_drawer.shift.*`, `cash_drawer.event.created`, `order.created`.

**Questions:**
1. `.updated` events (payment.updated, refund.updated, order.updated) — Phase 1 or Phase 2?
2. `inventory.count.updated` — Phase 1 or deferred?
3. Cash drawer events are NOT in the webhook subscription list — because B-047 confirmed they're poll-only. How does Sub 2 receive them?

**Condor's finding:**
1. `.updated` events should be Phase 1 — they carry status transitions (e.g., payment COMPLETED → CANCELED) that are critical for void/post-void detection (C-004 Chirp).
2. `inventory.count.updated` — Phase 2. The existing parser is ready but the CRDM table and Chirp rules aren't Phase 1 scope.
3. Cash drawer events require a **polling adapter** per B-047. TSP-02 specifies Valkey Streams ingestion, but there's no polling adapter design. This is a Phase 2 gap.

**Resolution needed:** ☐ Jeffe resolution — confirm `.updated` events are Phase 1 scope. ☐ Condor flags polling adapter gap — PRD addendum required for TSP-02/TSP-04.

---

### Q2.3: Cash Drawer API poll-only (B-047) — does TSP have a polling adapter?
**Context:** B-047 confirmed Square's Cash Drawer Shifts API is poll-only. SDK methods: `client.cash_drawers.shifts.list()`, `client.cash_drawers.shifts.retrieve()`. No webhook events exist for cash drawer opens/closes.

TSP-01 is designed for webhook receipt. TSP-02 publishes to Valkey Streams from webhook ingestion. There is no design for a polling source to feed into the same Valkey Stream.

**Question:** How do cash drawer events enter the TSP pipeline if there's no webhook for them?

**Condor's recommendation:** Build a `polling_adapter` module that runs on a schedule (Airflow DAG or `apscheduler`), calls `client.cash_drawers.shifts.list()`, and publishes results to the same `canary:events` Valkey Stream with a synthetic event wrapper. This way Sub 1/2/3 don't need to know whether data came from a webhook or a poll.

**Resolution needed:** ☐ Condor flags — PRD addendum required for TSP-02 (polling adapter design).

---

### Q2.4: Which PRDs need addenda before Jeremy builds Phase 2?
**Findings from this review:**

| PRD | Addendum Needed | Topic |
|---|---|---|
| TSP-02 | YES | Polling adapter design for cash drawer + labor APIs |
| TSP-04 | YES | `.updated` event parser templates + refund field completeness |
| TSP-04 | YES | Cash drawer parser routing (poll-sourced vs webhook-sourced) |
| TSP-05 | NO | Phase 1 mock inscription is correct. OrdinalsBot integration is Sprint 7. |
| TSP-06 | YES | Detection rules for `.updated` events (void/post-void transitions) |
| TSP-07 | NO | Sprint 7+ scope — no addenda needed now. |

**Resolution needed:** ☐ ALX routes addenda back to Condor follow-up.

---

## Bucket 3: Speed-to-Market Risks

### Q3.1: OAuth token scope — which permissions are active?
**Context:** B-032 RESOLVED — merchant account created, Canary authorized as marketplace app. But the OAuth scopes granted during authorization determine what APIs Jeremy can call.

**Question:** Which scopes are currently active on the GrowDirect Lab merchant? Do Phase 2 expansion scopes (inventory, loyalty, labor) require re-authorization?

**Condor's finding:** The `square_client.py` OAuth flow generates authorization URLs but doesn't specify explicit scopes — it uses the default set. The SDK's `client.o_auth.obtain_token()` returns `access_token`, `refresh_token`, `merchant_id`, and `expires_at` — but NOT a scope list. Scope verification requires checking the Square Developer Dashboard or calling `client.merchants.get("me")` and testing specific API endpoints.

**Resolution needed:** ☐ Jeffe resolution — check Square Developer Dashboard for active scopes. ☐ Jeremy: add scope verification to smoke test (call each Phase 1 API, confirm 200 not 403).

---

### Q3.2: Old `Client` vs new `Square` class — any legacy patterns in our code?
**Context:** Square SDK v44 uses `from square import Square` / `client = Square(token=...)`. The deprecated pattern is `from square.client import Client` / `client = Client(access_token=...)`. The OAuth example in `connect-api-examples` still uses the old `Client` class.

**Finding:** Two files use legacy patterns:
1. `square_client.py` (root, line ~30): Runtime detection of `Client` vs `Square` — tries both.
2. `connect-api-examples/connect-examples/oauth/python/oauth-flow.py`: Uses `from square.client import Client`.

TSP pipeline code is clean — all v44 `from square import Square`.

**Risk:** If anyone copies the OAuth example verbatim, they'll import the deprecated class. The old `Client` class may be removed in a future SDK version.

**Resolution needed:** ☐ Condor's call — codified in Standards Doc Section 2 (SDK-First Policy).

---

### Q3.3: `connect-python-sdk` deprecated — any imports from it?
**Context:** The `connect-python-sdk` repo is cloned to `square/connect-python-sdk/` for reference. It was the pre-v42 SDK. The current SDK is `square-python-sdk`.

**Finding:** Zero imports from `connect-python-sdk` anywhere in Canary code. Confirmed via scan. The repo is reference-only.

**Resolution needed:** None — no action required.

---

### Q3.4: SDK unpinned (`squareup`) — what happens when Square ships 45.x mid-sprint?
**Context:** B-063 standing directive: `requirements.txt` has `squareup` (unpinned). Jeffe directive: always take latest, never pin.

**Risk:** If Square releases v45 with breaking changes (renamed methods, changed response shapes, modified pagination behavior), the next `pip install` in Docker will pull the new version silently. No tests would catch this until runtime.

**Finding:** The SDK is Fern-generated. Breaking changes are unlikely within a major version but the SDK has no SemVer contract — versions are date-stamped (`44.0.1.20260122`). The next release could rename `client.payments.list()` to something else.

**Mitigation:** B-063 directive stands (Jeffe's call). But:
1. Pin in `requirements.txt` comment: `squareup  # B-063: unpinned per Jeffe. Current: 44.0.1.20260122`
2. Jeremy's session-open ritual includes `pip show squareup` — verify version hasn't changed.
3. If a new version drops mid-sprint, Jeremy freezes Docker image and evaluates before upgrading.

**Resolution needed:** ☐ Condor's call — codified in Standards Doc Section 2.

---

## Bucket 4: Coding Standards Gaps

### Q4.1: Error handling pattern for Square API calls
**Context:** The SDK has built-in retry logic (408, 429, 5xx with exponential backoff, max 2 retries). It raises `ApiError` on non-success responses with `status_code` and `body`.

**Question:** Does Jeremy catch `ApiError` at the SDK call site, or let it propagate to the blueprint error handler?

**Condor's recommendation:** Catch at the service layer, never at the blueprint. Pattern:
```python
try:
    response = client.payments.list(...)
except ApiError as e:
    if e.status_code == 429:
        log.warning("Square rate limit hit")
        raise RetryableError(...)
    raise SquareApiError(status=e.status_code, detail=e.body)
```

**Resolution needed:** ☐ Condor's call — codified in Standards Doc Section 4.

---

### Q4.2: Paginator handling in new SDK
**Context:** SDK v44 returns `SyncPager` objects for list endpoints. Two consumption patterns:
```python
# Pattern A: Iterate items
for payment in client.payments.list():
    process(payment)

# Pattern B: Iterate pages
for page in client.payments.list().iter_pages():
    process_batch(page)
```

**Question:** Which pattern does Jeremy use? Does he materialize full lists or stream?

**Condor's recommendation:** Stream (Pattern A) for real-time processing. Never materialize full lists into memory — a merchant with 100K payments would OOM. For batch operations (replay, backfill), use Pattern B with explicit page-level checkpointing.

**Resolution needed:** ☐ Condor's call — codified in Standards Doc Section 5.

---

### Q4.3: Field naming — Square names vs Canary normalized names
**Context:** Square uses `amount_money.amount` (cents as integer), `card_details.card.fingerprint`, `team_member_id`. CRDM uses `amount_cents`, `card_fingerprint`, `employee_id`. The normalization happens in parsers.

**Question:** Where is the normalization boundary? Sub 2 parsers? A shared mapping layer?

**Condor's recommendation:** Sub 2 parsers own the boundary. Each parser maps Square field names to CRDM column names. No shared mapping layer — parsers are the single translation point. Raw Square field names never appear outside of parser functions.

**Resolution needed:** ☐ Condor's call — codified in Standards Doc Section 6.

---

### Q4.4: Test data strategy — sandbox vs real event types
**Context:** B-065 processed 26 real Square webhooks from the sandbox. TSP uses Valkey Streams in DB 4 for event routing.

**Question:** What's the smoke test definition? Which events must pass end-to-end before declaring a Sprint 6 milestone?

**Condor's recommendation:** Sprint 6 smoke test = one of each Phase 1 event type passes through the complete pipeline:
1. `payment.created` → TSP-01 receipt → TSP-03 evidence seal → TSP-05 mock inscription → TSP-07 receipt lookup
2. `refund.created` → same path
3. Merkle batch flushes (100 events or 10 min timeout)
4. Chain hash verification passes for all sealed records

**Resolution needed:** ☐ Condor's call — codified in Standards Doc Section 8.

---

## Summary

| Bucket | Questions | Jeffe Resolution | Condor's Call | PRD Addenda |
|---|---|---|---|---|
| 1. Ring-Fencing | 4 | 0 | 4 | 0 |
| 2. TSP vs Square | 4 | 1 | 3 | 3 |
| 3. Speed-to-Market | 4 | 1 | 3 | 0 |
| 4. Standards Gaps | 4 | 0 | 4 | 0 |
| **TOTAL** | **16** | **2** | **14** | **3** |

**Jeffe action items:**
1. Q2.2: Confirm `.updated` events are Phase 1 scope (void/post-void detection)
2. Q3.1: Check Square Developer Dashboard for active OAuth scopes

**PRD addenda required (routes back to Condor):**
1. TSP-02: Polling adapter design for cash drawer + labor APIs
2. TSP-04: `.updated` event parser templates + refund field completeness + poll-source routing
3. TSP-06: Detection rules for `.updated` transition events

---

*Condor | B-066 Phase 1 | February 28, 2026*
*Gates: Jeremy next TSP session*
