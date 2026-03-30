---
type: spec
domain: tsp
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Square + TSP Coding Standards v1.0
**Work Order:** B-066 Phase 2
**Author:** Condor
**Date:** February 28, 2026
**Audience:** Jeremy (primary), all agents touching Square/TSP code
**Status:** DELIVERED — Jeremy's bible for all TSP/Square work
**SDK Version:** Square Python SDK v44.0.1.20260122
**Pipeline:** Sprint 6 TSP branch at `996562f` (33 files, 3,247 lines)

---

## Preamble

This document is the single source of truth for how Canary integrates with Square APIs and how the TSP (Triple Subscriber Pipeline) code is written. Every decision below was derived from:

- The cloned Square Python SDK v44 source code (`Canary/square/square-python-sdk/`)
- Jeremy's B-065 output (webhook manager, validators, scan notes)
- The Sprint 6 TSP pipeline (committed `996562f`)
- All 10 TSP PRDs (v1.2) + Consolidated Review
- Jeremy's LP Coverage Analysis (14% data coverage finding)
- The existing pre-B-065 Canary Square code

If this document contradicts any other document, this document wins for Square/TSP work. If it contradicts a Jeffe standing directive (like B-063 unpinned SDK), the standing directive wins.

---

## Section 1: The Ring-Fence Rule

### The Boundary

Square code lives inside a ring-fence. Nothing outside the fence touches Square objects, SDK responses, or Square field names directly.

**Inside the ring-fence** (may import from `square` package, may read Square response objects):
```
canary/services/tsp/              # All TSP pipeline code
canary/services/square_*.py       # Square service wrappers
canary/services/parsers/square_*  # Square payload parsers
canary/blueprints/webhooks_tsp.py # Webhook receipt endpoint
```

**Outside the ring-fence** (may NOT import from `square`, may NOT reference Square field names):
```
canary/models/                    # ORM models use CRDM names only
canary/blueprints/ (except webhooks_tsp.py)
canary/services/ (except square_* and tsp/)
canary/chirp/                     # Detection engine
```

### Rules

1. **No Square types in models.** ORM models use CRDM column names (`amount_cents`, `employee_id`), never Square names (`amount_money.amount`, `team_member_id`).

2. **No Square imports in blueprints** (except `webhooks_tsp.py`). Blueprints call service functions that return normalized dicts or ORM objects.

3. **Parsers are the translation boundary.** Every Square field name maps to a CRDM column name inside a parser function. Raw Square names never propagate past the parser return value.

4. **`square_client.py` (root) is legacy.** Tag line 1: `# LEGACY — do not import from TSP pipeline`. Contains OAuth patterns to lift later. Do not delete — do not import.

5. **One `Square()` instantiation per process.** Use a module-level singleton or factory. Do not create `Square()` objects inside request handlers.

---

## Section 2: SDK-First Policy

### The Rule

Use the Square SDK for everything it supports. Manual HTTP calls to Square APIs are prohibited. Manual implementations of SDK-provided utilities are deprecated.

### Specific Mandates

**MUST use SDK:**
- All API reads: `client.payments.list()`, `client.refunds.get()`, etc.
- Webhook subscription management: `client.webhooks.subscriptions.*`
- OAuth token exchange: `client.o_auth.obtain_token()`, `client.o_auth.renew_token()`
- Webhook signature verification: `from square.utils.webhooks_helper import verify_signature`

**MUST switch to SDK (action items):**
- `validators/square.py` manual HMAC → `verify_signature()` from SDK. Algorithm is identical; SDK version has stricter input validation (raises `ValueError` on empty args) and keyword-only params. Estimated effort: 15 minutes. Zero risk — same algorithm.

**MUST NOT use:**
- `from square.client import Client` (deprecated v35-v41 class)
- `from square_legacy.client import Client` (side-by-side migration shim — we have no legacy code to migrate)
- Any manual `requests.post()` / `httpx.post()` to Square API endpoints
- The `connect-python-sdk` package or any code from `square/connect-python-sdk/`

### SDK Version Management (B-063)

```
# requirements.txt
squareup  # B-063: unpinned per Jeffe standing directive. Current: 44.0.1.20260122

# Jeremy session-open ritual:
# 1. pip show squareup — verify version hasn't changed
# 2. If new version detected: freeze Docker image, evaluate changelog, test before adopting
# 3. If breaking change: pin temporarily, file TRIAGE blocker, notify ALX
```

### Client Instantiation Pattern

```python
# CORRECT (v44)
from square import Square

_client: Square | None = None

def get_square_client() -> Square:
    """Singleton Square client. One per process."""
    global _client
    if _client is None:
        _client = Square(
            token=os.environ["SQUARE_ACCESS_TOKEN"],
            environment=os.environ.get("SQUARE_ENVIRONMENT", "sandbox"),
        )
    return _client

# WRONG — deprecated
from square.client import Client  # DO NOT USE
client = Client(access_token=...)  # DO NOT USE
```

---

## Section 3: Event Type Handling Standard

### Webhook Subscription

The canonical event type list lives in `square_webhook_manager.py`. Phase 1:

```python
DEFAULT_EVENT_TYPES = [
    "payment.created",
    "payment.updated",
    "refund.created",
    "refund.updated",
    "inventory.count.updated",
    "order.created",
    "order.updated",
]
```

### Sub 2 Routing

Sub 2 (TSP-04) routes events by `event_type` field from the webhook payload. Routing pattern:

```python
PARSERS = {
    "payment.created": parse_payment_created,
    "payment.updated": parse_payment_updated,
    "refund.created": parse_refund_created,
    "refund.updated": parse_refund_updated,
    # Phase 2:
    # "order.created": parse_order_created,
    # "inventory.count.updated": parse_inventory_updated,
    # "gift_card_activity.created": parse_gift_card_activity,
}

def route_event(event_type: str, payload: dict) -> dict | None:
    parser = PARSERS.get(event_type)
    if parser is None:
        log.info(f"Unhandled event type: {event_type} — ACK'd, not parsed")
        return None
    return parser(payload)
```

### Adding a New Event Type (template)

1. Add event type string to `DEFAULT_EVENT_TYPES` in `square_webhook_manager.py`
2. Update webhook subscription: `python -m canary.services.square_webhook_manager update <sub_id> <url>`
3. Create parser function in `canary/services/tsp/parsers/` following the naming convention `parse_{event_type_with_underscores}(payload: dict) -> dict`
4. Add routing entry to `PARSERS` dict in Sub 2 consumer
5. Add CRDM table mapping if the event type writes to a new table
6. Add smoke test fixture (see Section 8)

### Unknown Event Policy

Unknown event types are **ACK'd but not parsed**. TSP-01 still hashes and publishes them to Valkey Streams. Sub 1 still seals them in the evidence store. Sub 2 logs a warning and skips parsing. Sub 3 still includes them in Merkle batches.

This means: every webhook Square sends is sealed and inscribed, even if Canary doesn't understand it yet. This is by design — it preserves the evidence chain for future parser additions.

---

## Section 4: Error Handling and Resilience

### SDK Error Handling

The Square SDK raises `ApiError` on non-2xx responses. It has built-in retry logic for 408, 429, and 5xx (exponential backoff, default max 2 retries).

**Standard pattern — catch at the service layer:**

```python
from square.core.api_error import ApiError

def fetch_payments(location_id: str) -> list:
    client = get_square_client()
    try:
        return list(client.payments.list(location_id=location_id))
    except ApiError as e:
        if e.status_code == 401:
            log.error(f"Square auth failed — token expired? status={e.status_code}")
            raise SquareAuthError(merchant_id=..., detail="Token expired or revoked")
        if e.status_code == 404:
            log.warning(f"Square resource not found: {e.body}")
            return []
        log.error(f"Square API error: status={e.status_code} body={e.body}")
        raise
```

**Never catch `ApiError` in blueprints.** Blueprints call service functions that handle SDK errors internally.

### Idempotency Keys

All mutating Square API calls (create, update) require an idempotency key:

```python
import uuid

response = client.payments.create(
    idempotency_key=str(uuid.uuid4()),
    source_id="...",
    amount_money={"amount": 100, "currency": "USD"},
)
```

For TSP Phase 1, the only mutating call is webhook subscription management. Idempotency keys are already handled in `square_webhook_manager.py`.

### Rate Limits

Square's rate limit is per-application, not per-merchant. The SDK handles 429 retries automatically. Additional rules:

1. **Never parallelize list() calls across multiple locations in the same process.** Sequential only.
2. **For batch operations** (Phase 2 backfill): add 100ms delay between pages.
3. **If rate-limited after SDK retries exhaust:** log, backoff 60 seconds, retry once more, then fail the operation.

### Partial Responses

Square API calls can return partial data (some fields null depending on payment state). Rules:

1. **Never assume a field exists** — always use `.get()` or `getattr()` with defaults.
2. **Null `card_details`** is valid — cash payments have no card data.
3. **Null `team_member_id`** is valid — self-service kiosk transactions have no employee.
4. **Null `order_id`** is valid — quick-charge payments may not create orders.

---

## Section 5: Pagination Standard

### Default Pattern: Stream Items

```python
# CORRECT — stream one item at a time
for payment in client.payments.list(location_id="..."):
    process_single(payment)
```

This is the default for all real-time and on-demand operations. The SDK handles cursor management internally.

### Batch Pattern: Stream Pages

```python
# For batch operations (replay, backfill, reporting)
for page in client.payments.list(location_id="...").iter_pages():
    process_batch(page.items)
    checkpoint(page.cursor)  # Save cursor for resume
```

Use page-level iteration when:
- You need checkpointing for long-running operations
- You're writing to a database in batches
- TSP-09 replay operations

### Rules

1. **Never materialize a full list into memory.** No `all_payments = list(client.payments.list())`. A merchant with 100K payments will OOM the container.
2. **Never ignore pagination.** If you call `.list()` and process only the first result, you missed everything else.
3. **Checkpoint on page boundaries**, not item boundaries. If the process dies mid-page, replay that page.
4. **For TSP polling adapter** (Phase 2, cash drawers + labor): paginate with a time window filter. Never open-ended `list()` without date bounds.

---

## Section 6: Field Naming and Normalization

### The Boundary

Square field names exist only inside parser functions. CRDM column names exist everywhere else. The parser is the translation point.

### Normalization Map (Phase 1)

| Square Field | CRDM Column | Parser | Notes |
|---|---|---|---|
| `amount_money.amount` | `amount_cents` | parse_payment | Integer cents |
| `amount_money.currency` | `currency` | parse_payment | ISO 4217 |
| `team_member_id` | `employee_id` | all parsers | Square renamed from employee_id |
| `card_details.card.fingerprint` | `card_fingerprint` | parse_payment | Network-universal per B-048 |
| `card_details.card.card_brand` | `card_brand` | parse_payment | VISA, MASTERCARD, etc. |
| `card_details.card.last_4` | `card_last4` | parse_payment | Last 4 digits |
| `card_details.entry_method` | `entry_method` | parse_payment | KEYED, SWIPED, EMV, CONTACTLESS |
| `risk_evaluation.risk_level` | `risk_level` | parse_payment | PENDING, NORMAL, MODERATE, HIGH |
| `source_type` | `square_product` | parse_payment | CARD, CASH, WALLET, etc. |
| `refund_money.amount` | `refunded_amount_cents` | parse_payment | Cumulative refund on payment |
| `id` (on refund) | `external_id` | parse_refund | Square's refund ID |
| `payment_id` (on refund) | `original_external_id` | parse_refund | Links refund to payment |
| `opened_cash_money.amount` | `expected_cash_cents` | parse_cash_drawer | Opening balance |
| `closed_cash_money.amount` | `actual_cash_cents` | parse_cash_drawer | Closing balance |
| `state` | `status` | parse_cash_drawer | OPENED → OPEN, CLOSED → CLOSED |

### Rules

1. **Square's `id` fields become `external_id` or `square_{type}_id` in CRDM.** Canary uses ULIDs as primary keys. Square IDs are reference only.
2. **Money is always integer cents.** Never store as float. Never divide by 100 until display layer.
3. **Timestamps are ISO 8601 strings from Square.** Parse to `datetime` in the parser. Store as `TIMESTAMP WITH TIME ZONE` in PostgreSQL.
4. **`team_member_id` → `employee_id` everywhere in Canary.** Square renamed this field across SDK versions. Canary standardizes on `employee_id`.
5. **`merchant_id` comes from the webhook payload root**, not from nested objects. Extracted by `validators/square.py:extract_merchant_id()`.

---

## Section 7: OAuth Scope and Permission Standard

### Phase 1 Scopes (Active)

| Scope | Required For |
|---|---|
| `PAYMENTS_READ` | Payments + Refunds |
| `MERCHANT_PROFILE_READ` | Merchants + Locations |
| `WEBHOOKS_READ` | Webhook subscription management |
| `WEBHOOKS_WRITE` | Webhook subscription creation/update |

### Phase 2 Expansion Scopes

| Scope | Required For | Notes |
|---|---|---|
| `ORDERS_READ` | Orders | |
| `ITEMS_READ` | Catalog | |
| `INVENTORY_READ` | Inventory | |
| `CUSTOMERS_READ` | Customers | |
| `CASH_DRAWER_READ` | Cash Drawers | B-047: poll-only |
| `TIMECARDS_READ` | Labor / Timecards | B-047: poll-only |
| `EMPLOYEES_READ` | Team Members | |
| `GIFTCARDS_READ` | Gift Cards | |

### Expansion Process

1. Add required scope to the OAuth authorization URL
2. Merchant re-authorizes (one-time consent screen)
3. New access token includes expanded scopes
4. Store updated token via `SquareOAuthService.store_token()`
5. Verify: call the new API endpoint, confirm 200 (not 403)

### Graceful Degradation

If a Phase 2 API call returns 403 (insufficient scope):
1. Log the scope gap: `log.warning(f"Missing scope for {api_family} — merchant needs re-authorization")`
2. Return empty result to caller (not an error)
3. Dashboard shows "Authorization needed" badge instead of data
4. Do NOT retry — 403 is not transient

### Scope Verification Smoke Test

After OAuth flow completes, run:
```python
def verify_scopes(client: Square, expected_families: list[str]) -> dict:
    """Call one read method per family. Returns {family: True/False}."""
    results = {}
    checks = {
        "payments": lambda: next(iter(client.payments.list()), None),
        "merchants": lambda: client.merchants.get(merchant_id="me"),
        "locations": lambda: client.locations.list(),
    }
    for family, check_fn in checks.items():
        if family not in expected_families:
            continue
        try:
            check_fn()
            results[family] = True
        except ApiError as e:
            results[family] = (e.status_code != 403)
    return results
```

---

## Section 8: Test Data Standard

### Smoke Test Definition

A **Sprint 6 smoke test** is: one event of each Phase 1 type passes through the complete TSP pipeline end-to-end.

| # | Event Type | Entry | Sub 1 | Sub 2 | Sub 3 | Receipt | Pass Criteria |
|---|---|---|---|---|---|---|---|
| 1 | `payment.created` | TSP-01 200 OK | evidence_records row, event_hash matches | transactions row (Phase 2) | Merkle leaf + mock inscription | receipt_tsp returns sealed record | All rows present, hashes match |
| 2 | `refund.created` | TSP-01 200 OK | evidence_records row, chain_hash links | refund_links row (Phase 2) | Merkle leaf + mock inscription | receipt_tsp returns sealed record | All rows present, chain valid |
| 3 | Batch flush | N/A | N/A | N/A | 100 events or 10 min timeout triggers Merkle build | inscription_pool row with merkle_root | Tree is deterministic, root matches |
| 4 | Chain verify | N/A | Full chain walk | N/A | N/A | N/A | `verify_chain()` returns True for all records |

### Sandbox Events

Square's sandbox generates test events via:
1. `square_webhook_manager.py test <subscription_id> [event_type]` — sends a test webhook
2. Manual API calls in sandbox (create a payment, then refund it)
3. Square Developer Dashboard → Webhooks → Send Test Event

### Replay Protocol

For repeatable testing:
1. Capture raw webhook payloads to JSON fixtures: `tests/fixtures/square_webhooks/`
2. Name fixtures: `{event_type}_{variant}.json` (e.g., `payment.created_card.json`, `refund.created_partial.json`)
3. Replay through TSP-01 endpoint using `curl` or `httpx`
4. HMAC header must be recomputed for replay (use the SDK helper with the fixture body)

### Test Fixture Directory Structure

```
tests/
  fixtures/
    square_webhooks/
      payment.created_card.json
      payment.created_cash.json
      payment.updated_completed.json
      payment.updated_canceled.json
      refund.created_full.json
      refund.created_partial.json
```

### What We Do NOT Test in Sprint 6

- Unit tests for TSP pipeline (per B-067 dispatch: "pure reads, sandbox only, no unit tests")
- End-to-end with real Bitcoin inscriptions (Sprint 7 — OrdinalsBot)
- Multi-merchant scenarios (one merchant only until first test cycle validates)
- Production credentials (next gate after smoke test passes)

---

## Section 9: The Academic Exercise Results

### What Square Provides vs What We've Built

This section maps SDK capabilities to existing Canary code and renders a verdict: **Adopt** (use SDK as-is), **Wrap** (thin wrapper around SDK), or **Ignore** (not relevant to LP).

| Capability | Square SDK | Canary Code | Verdict | Notes |
|---|---|---|---|---|
| **Webhook signature verification** | `verify_signature()` in `webhooks_helper.py` | `validators/square.py` manual HMAC | **ADOPT** | Switch to SDK helper. Identical algorithm, stricter validation. |
| **Webhook subscription management** | `client.webhooks.subscriptions.*` (7 methods) | `square_webhook_manager.py` | **ADOPT** | Already using SDK. Clean v44 implementation. |
| **Payment list/get** | `client.payments.list()`, `.get()` | `square_client.py` (legacy, mixed SDK versions) | **WRAP** | Build new service function using v44. Normalize to CRDM in parser. |
| **Refund list/get** | `client.refunds.list()`, `.get()` | `square_payment_parser.parse_refund()` | **WRAP** | Parser exists but incomplete (missing `order_id`, `processing_fee_money`). Rebuild per TSP-04. |
| **Order search/get** | `client.orders.search()`, `.get()`, `.batch_get()` | `square_order_parser.py` | **WRAP** | Parser exists. Phase 2 — rebuild per TSP-04 spec. |
| **Cash drawer list/retrieve** | `client.cash_drawers.shifts.list()`, `.retrieve()` | `square_auxiliary_parsers.parse_cash_drawer_shift()` | **WRAP** | Parser exists. Needs polling adapter (B-047). Phase 2. |
| **Labor timecard search/get** | `client.labor.search_timecards()`, `.retrieve_timecard()` | `square_auxiliary_parsers.parse_timecard()` | **WRAP** | Parser exists. Poll-only (B-047). Phase 2. |
| **Inventory counts/changes** | `client.inventory.batch_get_counts()`, `.batch_get_changes()` | `square_auxiliary_parsers.parse_inventory_adjustment()` | **WRAP** | Parser exists. Phase 2. |
| **Gift card activities** | `client.gift_cards.activities.list()` | `square_auxiliary_parsers.parse_gift_card_activity()` | **WRAP** | Parser exists. Phase 2. |
| **Customer list/search** | `client.customers.list()`, `.search()` | None | **WRAP** | Phase 2. Reference data for card fingerprint correlation. |
| **Catalog list/search** | `client.catalog.list()`, `.search()` | None | **WRAP** | Phase 2. Reference data for line item names/prices. |
| **OAuth token exchange** | `client.o_auth.obtain_token()`, `.renew_token()` | `square_oauth.py` (stub), `square_client.py` (legacy) | **WRAP** | `square_oauth.py` has Fernet encryption layer. Needs SDK wiring (TODO in code). |
| **Merchant profile** | `client.merchants.get("me")` | None | **ADOPT** | Phase 1 infra. Direct SDK call. |
| **Location list** | `client.locations.list()` | None | **ADOPT** | Phase 1 infra. Direct SDK call. |
| **Auto pagination** | `SyncPager` / `AsyncPager` | Manual cursor in `square_client.py` | **ADOPT** | SDK pagination replaces all manual cursor logic. |
| **Auto retry** | 408/429/5xx exponential backoff | None | **ADOPT** | SDK handles. No custom retry needed. |
| **Async client** | `AsyncSquare` | None | **IGNORE** | Not needed Sprint 6. Canary uses sync Flask. Evaluate for Phase 3 scale. |
| **File uploads** | `client.invoices.create_invoice_attachment()` | None | **IGNORE** | Not LP-relevant. |
| **Dispute evidence** | `client.disputes.evidence.*` | None | **IGNORE** | Phase 3. |
| **Loyalty programs** | `client.loyalty.*` | None | **IGNORE** | Phase 3. |
| **Subscriptions** | `client.subscriptions.*` | None | **IGNORE** | Not planned. No LP signal. |

### Summary Counts

| Verdict | Count | Action |
|---|---|---|
| **ADOPT** | 7 | Use SDK directly — no wrapper needed |
| **WRAP** | 10 | Thin wrapper: SDK call → parser → CRDM dict |
| **IGNORE** | 4 | Not relevant to current or planned LP scope |

---

## Section 10: PRD Addenda Required

These are flags only. Each routes back to Condor for a follow-up session. ALX handles routing.

| PRD | Addendum | One-Line Description |
|---|---|---|
| **TSP-02** | Polling adapter | Design pattern for non-webhook data sources (cash drawer, labor) to feed into `canary:events` Valkey Stream |
| **TSP-04** | `.updated` event parsers | Phase 1 needs `payment.updated` and `refund.updated` parsers for void/post-void/status transition detection |
| **TSP-04** | Refund field completeness | `parse_refund()` missing `order_id`, `processing_fee_money`, `unlinked` fields required by CRDM `refund_links` |
| **TSP-04** | Poll-source vs webhook-source routing | Sub 2 needs to handle events from both webhook ingestion and polling adapter without breaking the fan-out model |
| **TSP-06** | Transition detection rules | `.updated` events carry state transitions (COMPLETED → CANCELED). Detection engine needs rules for void/post-void patterns. |

---

## Quick Reference Card

```
# Client
from square import Square
client = Square(token=os.environ["SQUARE_ACCESS_TOKEN"], environment="sandbox")

# Read payments
for payment in client.payments.list(location_id="..."):
    process(payment)

# Verify webhook
from square.utils.webhooks_helper import verify_signature
is_valid = verify_signature(
    request_body=raw_body_string,
    signature_header=headers["x-square-hmacsha256-signature"],
    signature_key=os.environ["SQUARE_WEBHOOK_SIGNATURE_KEY"],
    notification_url=os.environ["SQUARE_NOTIFICATION_URL"],
)

# Handle errors
from square.core.api_error import ApiError
try:
    result = client.payments.get(payment_id="...")
except ApiError as e:
    log.error(f"Square API error: {e.status_code} {e.body}")

# Manage webhook subscriptions
# python -m canary.services.square_webhook_manager list
# python -m canary.services.square_webhook_manager create <ngrok_url>
# python -m canary.services.square_webhook_manager test <sub_id> refund.created
```

---

*Condor | B-066 Phase 2 | February 28, 2026*
*This is Jeremy's bible. When in doubt, check here first.*
