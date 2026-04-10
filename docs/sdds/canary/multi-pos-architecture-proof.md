# Multi-POS Architecture Proof — Toast and Clover Validation

**Status:** Architecture validation (no implementation)
**Date:** 2026-03-22
**Author:** ALX (COO Agent)
**Reviewed by:** Jeffe (CEO)

---

## Principle

Canary is a horizontal data platform. The loss prevention engine operates on
canonical data models (CRDM) that are POS-agnostic by design. Adding a new
POS system should require adapter code — not architectural changes.

This document validates that claim by mapping Toast (restaurant POS) and Clover
(general retail POS) against every layer of the Canary pipeline. If the
abstraction holds for three structurally different systems, it holds for N.

---

## 1. Abstraction Layer Scorecard

| Layer | Current State | Toast Readiness | Verdict |
|---|---|---|---|
| **Identity Resolution** (`app.external_identities`) | Source-agnostic bridge table. UUID primary keys. `source_code` discriminator. | INSERT `source_code='toast'`, map Toast GUIDs. Zero schema changes. | **READY** |
| **Source Registry** (`app.source_systems`) | Reference table with `code`, `display_name`, `category`. Designed for N sources. | INSERT one row: `('toast', 'Toast', 'pos')`. | **READY** |
| **Merchant Connection** (`app.merchant_sources`) | `(merchant_id, source_code)` unique. Status lifecycle. RaaS namespace. | Store Toast restaurant GUID in `external_merchant_id`. | **READY** |
| **Webhook Entry** (`/webhooks/<source>`) | Route parameterized on `<source>`, gated by `REGISTERED_SOURCES` set. | Add `"toast"` to set. Route is already source-agnostic. | **READY** |
| **Signature Validation** | Square HMAC-SHA256 hardcoded. | Toast uses different webhook signing. Need `SignatureValidator` strategy per source. | **NEEDS NEW CODE** |
| **Event Dispatch** (`webhook_dispatch.py`) | 145+ Square event types. Flat `event_type → EventRoute` lookup. | Toast has different event taxonomy. Dispatch needs `(source_code, event_type)` compound key. | **NEEDS GENERALIZATION** |
| **Parser Suite** (`canary/services/parsers/`) | 6 `square_*` parser files, ~17 parse functions. Pure functions — JSON in, flat dict out. | Same pattern, different field mappings. ~8 `toast_*` modules (fewer event types, richer payloads). | **NEEDS NEW CODE** |
| **CRDM Models** (Transaction, Tender, Order, etc.) | Source-agnostic columns. `card_fingerprint` indexed. | Mostly ready. `card_fingerprint` cannot be reliably populated (see Section 4). Need `source_code` on transactions. | **NEEDS MINOR CHANGES** |
| **Chirp Detection Rules** | Rules reference `card_fingerprint`, `entry_method`, `tender_type`. | C-005 (card velocity) degrades without fingerprint. C-008 (manual entry) works. See Section 4. | **DEGRADED** |
| **OAuth / Onboarding** | Square OAuth authorization-code grant. Merchant-initiated consent. | Toast uses client-credentials (machine-to-machine). No merchant consent flow. Partner agreement required. | **NEEDS NEW CODE** |
| **Initial Sync** (RaaS) | Square List APIs for employees, locations, devices. | Toast has `/partners`, `/restaurants`, `/labor/v1/employees`. Different pagination, 20 req/s rate limit. | **NEEDS NEW CODE** |
| **Evidence Chain** (Sub1 seal + Sub3 Merkle) | Operates on raw event bytes and chain hashes. No parsed content dependency. | Source-agnostic by design — seals and Merkle trees process event hashes, not POS-specific fields. | **READY** |

**Summary:** 5 layers ready, 1 needs generalization, 5 need new code, 1 degraded.

---

## 2. POS Adapter Pattern

Each new POS requires the same five components — a repeatable sprint:

| Component | Responsibility | Square (exists) | Toast (new) |
|---|---|---|---|
| **Auth Adapter** | Connect merchant, manage tokens | OAuth authorization-code grant | Client-credentials + Toast partner agreement |
| **Signature Validator** | Verify inbound webhooks | HMAC-SHA256 with Square signing key | Toast webhook signature mechanism |
| **Event Registry** | Map POS events to CRDM parsers | 145+ `square_*` event routes | `order_updated` + ~6 other event types |
| **Parser Suite** | Transform POS JSON to CRDM flat dicts | 6 `square_*` parser files (~17 functions) | ~8 `toast_*` modules |
| **Sync Adapter** | Initial data pull on merchant connect | Square List APIs | Toast REST APIs (`/partners`, `/restaurants`, `/labor`) |

**Key observation:** Toast is structurally simpler to integrate than Square. Square fires
dozens of granular event types (payment.created, payment.updated, order.created,
refund.created, etc.). Toast fires `order_updated` for nearly everything — one payload
containing the full Order → Check → Selection hierarchy. Fewer parsers, but each parser
does more decomposition work.

---

## 3. Data Model Mapping — Toast to CRDM

### 3.1 Structural Differences

| Concept | Square | Toast | Canary Impact |
|---|---|---|---|
| Order hierarchy | Order → LineItems | Order → Checks → Selections | Parser must flatten checks into order-level aggregates |
| Split checks | Separate orders | Native — multiple checks per order | Transaction model already supports; tender linkage per check |
| Payments | `tenders[]` on Order | `payments[]` on each Check | Parser iterates checks, not order-level tenders |
| Employee on transaction | On tender (`tender.employee_id`) | On order (`order.server.guid`) | Toast is better — direct linkage, no tender chase |
| Void tracking | Limited (status/refund) | `voided` + `voidDate` + `voidBusinessDate` at order/check/selection level | Toast is richer — three-level void granularity |
| Business date | Computed from timestamp + timezone | First-class `businessDate` integer (yyyyMMdd) | Toast is better — restaurant-aware, handles overnight |
| Currency units | Cents (integer) | Dollars (decimal) | Parser must convert dollars → cents |
| Discounts | `discounts[]` on order + per-line | `appliedDiscounts[]` on check + per-selection | Parser must aggregate from check level |

### 3.2 Field Mapping

| Canary CRDM Field | Square Source | Toast Source | Status |
|---|---|---|---|
| `transaction.external_id` | `payment.id` | `order.guid` | Direct map |
| `transaction.card_fingerprint` | `card.fingerprint` | Composite: `last4 + cardType` | **Degraded** (see Section 4) |
| `transaction.entry_method` | `card_details.entry_method` | `payment.cardEntryMode` | Direct map (enum remap) |
| `transaction.employee_id` | `tender.employee_id` | `order.server.guid` | Direct map |
| `transaction.device_id` | `tender.device_id` | `order.device` | Direct map |
| `transaction.location_id` | `payment.location_id` | Header: `Toast-Restaurant-External-ID` | Direct map |
| `transaction.customer_id` | `order.customer_id` | Only on takeout/delivery orders | **Gap** (no dine-in customer) |
| `transaction.business_date` | Computed | `order.businessDate` | Direct map (Toast native) |
| `tender.tender_type` | `tender.type` (CARD/CASH/etc.) | `payment.type` (CREDIT/CASH/etc.) | Enum remap |
| `tender.card_brand` | `card.card_brand` | `payment.cardType` | Direct map |
| `tender.card_last4` | `card.last_4` | `payment.last4Digits` | Direct map |
| `tender.amount_cents` | `tender.amount_money.amount` | `payment.amount` × 100 | Unit conversion |
| `order.discount_amount` | `order.discounts[].amount` | `check.appliedDiscounts[].discountAmount` | Structural — aggregate from checks |
| `order.void_status` | Limited | `voided` + `voidDate` at 3 levels | Toast is richer |
| `order.source` | `order.source` | `order.source` (IN_STORE, ONLINE, KIOSK, etc.) | Direct map (enum remap) |

---

## 4. Card Fingerprint and Customer Identity

### 4.1 The Card Fingerprint Gap

**Square** provides `card.fingerprint` — a cryptographic hash that uniquely identifies
a physical card across all transactions. Same card always produces the same hash. This
powers Canary's C-005 (CARD_VELOCITY) rule and is the foundation of card risk scoring
(GRO-263).

**Toast** provides `cardPaymentId` — described as a "unique non-sensitive card
identifier." However, this field is **unreliable for EMV (chip) and keyed entries** —
availability varies by firmware and payment processor, and is frequently null. Since
chip transactions are the majority of in-store card payments, `cardPaymentId` cannot
be depended on for cross-transaction card tracking.

**Available Toast card fields:**

| Field | Availability | Reliability for Identity |
|---|---|---|
| `cardPaymentId` | Swiped/tokenized only. Null for EMV and keyed. | Unreliable |
| `last4Digits` | Always present on card payments | Low — collision risk across cards |
| `cardType` (brand) | Always present | Discriminator only |
| `cardEntryMode` | Always present | Not an identity field |
| `cardFirst6` (BIN) | Auth flow only, not on Orders API reads | Not available in webhook path |

**Composite card identity approach:** `last4Digits + cardType` provides a low-confidence
card identifier. Two different Visa cards ending in 4242 would collide. This is
materially worse than Square's cryptographic fingerprint but is the best Toast exposes.

### 4.2 Impact on Chirp Detection Rules

| Rule | Square Behavior | Toast Behavior |
|---|---|---|
| **C-005 CARD_VELOCITY** (same card 5+ times/hour) | Exact match on `card_fingerprint`. High confidence. | Composite match on `last4 + brand`. Collision risk. **Degraded.** |
| **C-008 MANUAL_ENTRY_SPIKE** (5+ keyed-in cards/shift) | `entry_method = KEYED` | `cardEntryMode = KEYED`. **Works.** |
| **C-010 PARTIAL_AUTHORIZATION** | `approved_amount < requested_amount` | Same fields available. **Works.** |
| **Card risk scoring** (GRO-263) | Fingerprint-based aggregation | Cannot implement at same confidence. **Degraded.** |
| **Refund-to-different-card** (future) | Fingerprint comparison | Cannot implement. **Blocked.** |

### 4.3 Source-Aware Confidence Tiers

The Chirp rule engine should become **source-aware** — same rule, different confidence
levels depending on what the POS provides:

| Tier | Criteria | Card Identity Method | Confidence |
|---|---|---|---|
| **Tier 1** | Cryptographic fingerprint available | `card.fingerprint` (Square) | High |
| **Tier 2** | Composite key only | `last4 + brand` (Toast) | Medium |
| **Tier 3** | Cash / no card data | N/A | N/A — rule skipped |

Alert metadata should carry a `detection_confidence` field so downstream consumers
(Fox cases, dashboard, EJ spine) can weight alerts appropriately.

### 4.4 Customer Identity Gap

**Square** provides a Customer API. Customer IDs appear on transactions. Canary stores
these in `app.customers` (privacy-first, no PII, aggregate metrics only).

**Toast** has no Customer API. Customer data (name, phone, email) only appears on
takeout and delivery orders. Dine-in orders — the bulk of restaurant volume — carry
no customer identity. The only person identifier on a dine-in order is `server`
(employee) and an optional freeform `tabName`.

**Impact:** Customer-level LP patterns (repeat customer fraud, customer-employee
collusion) cannot be detected on Toast dine-in transactions. This is a data
availability limitation of the POS, not an architectural gap in Canary.

**Mitigation:** For Toast merchants, customer identity could be enriched through:
- Loyalty program integration (Toast supports outbound loyalty hooks)
- Card composite identity as a customer proxy (same card = same customer, with
  collision caveats from Section 4.1)
- House account linkage (`payment.type = HOUSE_ACCOUNT`)

---

## 5. Toast API Characteristics

### 5.1 Authentication

Toast uses **OAuth 2.0 client-credentials grant** (machine-to-machine). No merchant-
facing consent flow. Access is managed through Toast's partner program.

| Aspect | Square | Toast |
|---|---|---|
| Grant type | Authorization-code (merchant consent) | Client-credentials (partner agreement) |
| Token endpoint | `/oauth2/token` | `/authentication/v1/authentication/login` |
| Restaurant scoping | `merchant_id` in token | `Toast-Restaurant-External-ID` header |
| Multi-location | Per-merchant token | JWT with partner GUID or management set |
| Onboarding | Merchant installs app, grants scopes | Toast approves partner, assigns restaurants |

### 5.2 Webhooks

Toast webhooks deliver full object payloads. The primary LP-relevant webhook is
`order_updated`, which fires on every order lifecycle event (create, payment, void,
refund, discount, status change). The full Order object is included in the payload.

**Idempotency:** Each event has a GUID. Deduplicate on event GUID.
**Fallback:** Every webhook has a corresponding polling API. Toast recommends
periodic polling as backup.

### 5.3 Rate Limits

| Scope | Limit |
|---|---|
| Default (most APIs) | 20 req/s AND 10,000 req/15 min |
| Orders `/ordersBulk` | 5 req/client/location/second |
| Menus `/menus` | 1 req/s/location |
| Historical queries | Max 1-month range, 5-10s spacing |

Rate limits are tighter than Square. Webhook-first architecture is mandatory — aligns
with how Canary already operates via TSP.

### 5.4 Partner Program

Toast's partner program requires: application review, compliance vetting, signed partner
agreement, sandbox development, and a one-hour certification call. Historically involves
revenue sharing (reported at 30%). This is a fundamentally different go-to-market than
Square's self-service developer platform.

---

## 6. What Toast Does Better Than Square

Toast's data model has several advantages for loss prevention:

1. **Split check awareness.** Check-level model exposes voids, discounts, and payments
   per-check within a single order. Square merges at the order level.

2. **Three-level void tracking.** `voided` + `voidDate` + `voidBusinessDate` at order,
   check, AND selection levels. Square's void data is more limited.

3. **Employee on order.** `server.guid` directly on the order object. Square puts
   `employee_id` on tenders — requires chasing through payment objects.

4. **Business date as first-class field.** `businessDate` integer handles overnight
   restaurants correctly. Square requires computation from timestamp + timezone.

5. **Cash management API.** Dedicated API for cash drawer events — useful for cash-
   based fraud detection beyond what Square exposes.

6. **Security integration cookbook.** Toast publishes documentation for building LP
   integrations, recommending monitoring of discounts, voids, and refunds with
   timestamp correlation to video. LP is a validated use case on their platform.

---

## 7. Implementation Scope Estimate

Adding Toast as a second POS requires one sprint focused on the adapter layer:

| Work Item | Complexity | Dependencies |
|---|---|---|
| Toast auth adapter (client-credentials) | Medium | Toast partner agreement signed |
| Webhook signature validator | Low | Toast webhook docs |
| Event registry (~8 Toast event types) | Low | Generalize `webhook_dispatch.py` |
| Toast parser suite (~8 modules) | Medium | CRDM field mapping (Section 3) |
| Toast sync adapter (employees, locations, devices) | Medium | Toast REST API rate limits |
| Generalize dispatch to `(source_code, event_type)` | Low | One-time refactor |
| Add `source_code` to transactions table | Low | Alembic migration (sales chain) |
| Chirp confidence tiers | Medium | Source-aware rule evaluation |
| Composite card identity for Toast | Low | Parser-level logic |
| Currency normalization (dollars → cents) | Low | Parser-level logic |

**Not required:** No changes to External Identities, source_systems, merchant_sources,
CRDM models (beyond `source_code` column), Owl search, Fox cases, EJ spine, or
dashboard. The abstraction layer holds.

---

## 8. Clover as Third POS — Pattern Validation

To confirm the adapter pattern scales to N POS systems, Clover was evaluated against
the same framework. If the abstraction holds for three structurally different POS
systems (Square, Toast, Clover), it holds for any.

### 8.1 Clover API Profile

| Dimension | Clover |
|---|---|
| Owner | Fiserv (banking conglomerate) |
| Market | General retail + QSR |
| Auth | OAuth 2.0 with expiring tokens (v2 flow, mandatory) |
| Webhooks | **Notification-only** — payload contains object ID + event type, not full object. Requires callback to fetch data. |
| Rate limits | 16 req/s per token, 50 req/s per app, 5 concurrent per token |
| Query window | 90-day hard limit on payments/orders endpoints |
| Revenue share | 70/30 developer/Clover on subscription revenue |
| Approval | Functional review + video demo + legal/privacy review |

### 8.2 Adapter Layer Fit

| Component | Clover Specifics | Pattern Holds? |
|---|---|---|
| **Auth Adapter** | OAuth 2.0 authorization-code (like Square, unlike Toast). Expiring tokens with refresh. | Yes — closest to Square's flow |
| **Signature Validator** | `X-Clover-Auth` header verification | Yes — new validator, same strategy |
| **Event Registry** | P (payments), O (orders), C (customers), E (employees), CA (cash adjustments) | Yes — fewer event types than Square |
| **Parser Suite** | Notification-only webhooks require fetch-then-parse. Two-step: receive ID → GET full object → parse. | Yes — parser input is the same (JSON), but ingestion adds a fetch step |
| **Sync Adapter** | `/v3/merchants/{mId}/employees`, `/devices`, `/orders`. Max 3 `?expand=` fields per call. 90-day query window. | Yes — pagination differs, but same pattern |

### 8.3 Card Fingerprint — Clover

**Clover does not provide a card fingerprint.** The `cardTransaction` sub-object
(requires `?expand=cardTransaction`) exposes:

| Field | Availability | Identity Value |
|---|---|---|
| `first6` (BIN) | Card-present payments | Discriminator — narrows issuer |
| `last4` | Always on card payments | Low — collision risk |
| `cardType` (brand) | Always | Discriminator only |
| `entryType` | Always (SWIPED, EMV_CONTACT, EMV_CONTACTLESS, KEYED) | Not identity — LP signal |
| `vaultedCard.token` | Only when merchant explicitly saves card | Merchant-scoped, not universal |
| `cardholderName` | Sometimes present | PII — cannot use as key |

**Composite key:** `first6 + last4 + cardType` — better than Toast's `last4 + brand`
because Clover exposes the BIN on card-present reads. Still probabilistic, but the
collision space is smaller (1M × 10K × ~5 brands = ~50B combinations vs. Toast's
10K × ~5 = ~50K).

### 8.4 Customer Identity — Clover

Clover has a Customer API (`/v3/merchants/{mId}/customers`), but customer linkage to
orders is **manual and merchant-dependent**. Most card-present dine-in and retail
transactions have no customer record. Clover does not auto-link customers via card
identity the way Square does.

### 8.5 Clover-Specific Architectural Considerations

Two things about Clover are structurally different from both Square and Toast:

**1. Notification-only webhooks.** Square and Toast send the full object in the webhook
payload. Clover sends only the object ID. The TSP consumer must make a follow-up API
call to fetch the full object before parsing. This means:
- Higher API call volume (every webhook triggers a GET)
- Rate limit pressure (16 req/s per token)
- Need for a fetch queue with backoff between the webhook receiver and the parser

This does not break the architecture — it adds a **fetch step** between webhook receipt
and parser dispatch. The Sub2 consumer would branch: if `source_code == 'clover'`,
fetch the object first; otherwise, parse inline.

**2. Separate order and payment entities.** Square and Toast nest payments inside
orders. Clover keeps them as separate API resources linked by reference. A complete
transaction picture requires joining order + payment + `?expand=cardTransaction,employee,device`.
This is a parser concern, not an architectural one.

### 8.6 Three-POS Comparison — Card Identity

| Capability | Square | Toast | Clover |
|---|---|---|---|
| Card fingerprint | Native `card.fingerprint` — cryptographic, deterministic | `cardPaymentId` — unreliable for EMV | None |
| BIN (first 6) | Available | Auth flow only, not on Orders API | Available via `?expand=cardTransaction` |
| Last 4 | Available | Available | Available |
| Card brand | Available | Available | Available |
| Entry method | Available | Available | Available |
| Composite key quality | Not needed (fingerprint) | `last4 + brand` (~50K space) | `first6 + last4 + brand` (~50B space) |
| Confidence tier | **Tier 1** (high) | **Tier 2** (medium) | **Tier 2** (medium-high) |

**Observation:** Clover actually provides a better composite card identity than Toast
because it exposes the BIN. The confidence tier system proposed in Section 4.3 handles
this naturally — same framework, different confidence level per source.

### 8.7 Verdict

The adapter pattern holds for Clover. The same five components (auth adapter, signature
validator, event registry, parser suite, sync adapter) apply. The two Clover-specific
wrinkles (notification-only webhooks, separate order/payment entities) are handled at
the parser and consumer level — no changes to identity resolution, CRDM models, Chirp
rules, or the evidence chain.

**The one-time generalizations identified for Toast** (dispatch compound key, `source_code`
column, confidence tiers) **also serve Clover with zero additional work.** This confirms
the generalization is POS-agnostic, not Toast-specific.

---

## 9. Conclusion

**The horizontal platform thesis is validated.** Three structurally different POS
systems — Square (self-service OAuth, full object webhooks, native card fingerprint),
Toast (client-credentials, full object webhooks, no fingerprint), and Clover
(expiring OAuth, notification-only webhooks, no fingerprint) — all map to the same
adapter pattern without architectural changes.

The one-time generalizations (dispatch compound key, `source_code` column, confidence
tiers) serve all three. The identity layer, CRDM models, Chirp rules, evidence chain,
Owl search, Fox cases, and EJ spine are source-agnostic by design and require no
changes.

**The honest gap is card fingerprint.** Square is the only major POS that provides a
cryptographic card identifier. Toast and Clover both require composite keys built from
`last4 + brand` (Toast) or `first6 + last4 + brand` (Clover). Card velocity detection
(C-005) and card risk scoring (GRO-263) degrade from exact-match to probabilistic-match
on non-Square POS systems. This is a data quality limitation of the POS ecosystem, not
an architectural failure. The mitigation — source-aware confidence tiers in Chirp —
keeps the detection framework honest about what each source can provide.

**The commercial gap is onboarding.** Each POS has a different partner model: Square
self-serves via OAuth, Toast requires a signed partner agreement and certification
call, Clover requires a functional review with video demo. This changes the go-to-market
motion per POS but does not affect the technical architecture.

Each new POS is a sprint — auth adapter, signature validator, event registry, parser
suite, sync adapter. The same five components, the same pattern, different field
mappings. The framework is ready.

---

*Canary | GrowDirect Inc. | Confidential*
