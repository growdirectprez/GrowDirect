# Solex Commerce Mockup — Design Spec

**Status:** Draft
**Date:** 2026-04-23
**Author:** Claude (with GC)
**Supersedes:** `docs/playbook-solex-square-merchant.md` (Phases 3–6 / Level 1) — the playbook framed the work as a seeder profile inside Canary; this spec reframes it as a standalone commerce app.

---

## 1. Overview

Build a full-fidelity e-commerce storefront, architected as a real production commerce site, that mirrors `solexglobal.com` visually and sells its product line. The site runs as a GrowDirect-operated merchant against the Square **sandbox**, producing a realistic transaction stream that Canary observes via its existing Square OAuth integration.

The site is not a live retail business. It is a production-grade Canary fixture: built like a real commerce site, operated as a demo artifact.

### 1.1 Goal

1. Give Canary a continuously available, demoable merchant feed that looks like a real MLM wellness reseller — not a seeded database.
2. Exercise Canary's chirp rules (C-001 high-value, C-002 after-hours, C-003 round-amount, plus refund/inventory-shrink rules from GRO-297) against realistic transaction patterns.
3. Provide a polished, visually-faithful site we can walk prospects through in a sales demo.
4. Build the architecture such that flipping to a real (live-mode) merchant later is a config change, not a rewrite.

### 1.2 Non-goals

- A sellable commerce product. This is a fixture, not a SaaS offering.
- A Solex distributorship. We are not entering an MLM contract with Solex Global.
- Live payments. Square is in sandbox mode throughout.
- Multi-tenant. One site, one merchant.
- Replacing Canary's existing sandbox seeder (`square_sandbox_seeder.py` stays — this supplements it).

### 1.3 Constraints

- **Trademark + copyright exposure.** Site mirrors Solex branding and product imagery. Site MUST be non-public-discoverable (noindex, robots disallow, Cloudflare Access password gate). Imagery stored locally; no hotlinking.
- **Platform conventions.** Follow `CLAUDE.md` standards: Flask 3, Jinja, SQLAlchemy 2.0 `Mapped[]`, Postgres 17, Valkey 8, Tailwind 3 via PostCSS, Alpine 3 via npm, magic-link auth, UUID PKs, `created_at`/`updated_at` on every table, no SQLite, no CDN-served frameworks.
- **No new runtime.** Python-only. No Node-based SSR, no WordPress, no Shopify headless.
- **Shared infra.** Joins the existing `growdirect` Docker network. Shares Postgres, Valkey, Ollama.
- **Canary is zero-coupled.** This app must not import from Canary or be imported by Canary. Canary observes purely via the Square merchant feed.

### 1.4 Not-in-this-spec

- Cut-over plan from sandbox to live Square mode (separate spec when we get there).
- Canary rule tuning against MLM traffic patterns (separate work, post-MVP).

---

## 2. Architecture

### 2.1 Repo layout

Peer to Canary/, Cove/:

```
GrowDirect/
├── Solex/
│   ├── CLAUDE.md                  # app-specific context
│   ├── wsgi.py                    # Gunicorn entry, Guardian-protected
│   ├── solex/
│   │   ├── __init__.py            # app factory, blueprints
│   │   ├── config.py              # Base/Dev/Test/Prod configs
│   │   ├── extensions.py          # db, login_manager, mail, rq
│   │   ├── models/                # SQLAlchemy models
│   │   ├── services/              # business logic + external integrations
│   │   ├── routes/                # blueprints
│   │   ├── templates/             # Jinja
│   │   ├── static/                # Tailwind build + Alpine + images
│   │   └── jobs/                  # RQ job functions
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── conftest.py
│   ├── alembic/
│   ├── devops/
│   │   ├── docker-compose.yml
│   │   └── Dockerfile
│   ├── catalog/                   # curated source-of-truth for seed data
│   │   ├── products.yaml
│   │   └── images/
│   ├── package.json
│   └── requirements.txt
```

### 2.2 Blueprints

| Blueprint | Prefix | Auth | Surface |
|---|---|---|---|
| `storefront` | `/` | public | `/`, `/shop`, `/shop/<category>`, `/products/<slug>`, `/search`, `/cart`, `/checkout`, `/order/<public_token>` |
| `account` | `/account` | customer login | `/account`, `/account/orders`, `/account/subscriptions`, `/account/addresses` |
| `admin` | `/admin` | admin login | `/admin`, `/admin/catalog`, `/admin/orders`, `/admin/refunds`, `/admin/inventory`, `/admin/customers`, `/admin/subscriptions` |
| `lab` | `/admin/lab` | admin login | `/admin/lab`, `/admin/lab/scenarios/<name>`, `/admin/lab/runs/<id>` |
| `api` | `/api` | session or bearer | `/api/cart/*`, `/api/checkout/*`, `/api/webhooks/square` |

### 2.3 Runtime topology

```
[ Cloudflare Access gate ]
            │
            ▼
[ Flask (gunicorn --reload) :5003 ]
   │            │               │
   ▼            ▼               ▼
[ Postgres ] [ Valkey ]    [ Square Sandbox ]
  solex       DB 2          (merchant, catalog optional mirror,
  solex_test  (sessions      payments, refunds, card-on-file)
              + cart         
              + RQ queue)    
            │
            ▼
[ RQ worker (same image, different command) ]
   │
   ▼
[ Scheduled jobs: autoship charging, cart abandonment,
                  catalog sync, scenario execution ]

[ MailHog :1027/8027 ]  ← dev SMTP
```

### 2.4 Environment slots

| Resource | Value |
|---|---|
| Flask port | 5003 |
| Postgres DB | `solex` / `solex_test` |
| Valkey DB index | 2 (Canary=0, Cove+Angel=1) |
| MailHog SMTP / Web | 1027 / 8027 |
| Public hostname (dev) | `localhost:5003` |
| Public hostname (staging) | `solex.growdirect.app` (Cloudflare Access gated) |
| Docker compose `name:` | `solex` |
| Image names | `solex-web`, `solex-worker` |
| Container names | `solex_web`, `solex_worker` |
| Network | `growdirect` (external) |

---

## 3. External dependencies

All third-party integrations, explicit. Stubbed implementations are behind real interfaces; swapping to production is a config change.

| Dependency | Purpose | v1 implementation | Prod implementation |
|---|---|---|---|
| **Square API (sandbox)** | Orders, Payments, Refunds, Cards-on-file, Customers, Catalog (optional mirror) | Square Python SDK pointed at sandbox via `SQUARE_ENVIRONMENT=sandbox` | Same SDK, `SQUARE_ENVIRONMENT=production` + live access token |
| **Square Web Payments SDK** | Client-side card tokenization | Sandbox JS bundle from `sandbox.web.squarecdn.com` | Production JS bundle |
| **Square Webhooks** | Payment state changes, refund completions | Sandbox webhook signing key, endpoint `/api/webhooks/square` | Production webhook signing key, same endpoint |
| **RQ (Redis Queue)** | Background jobs — autoship charging, cart abandonment, scenario execution, catalog sync | RQ on Valkey DB 2 (Valkey is Redis-compatible) | Same |
| **rq-scheduler** | Cron-style scheduling for autoship + cart-abandonment jobs | rq-scheduler on Valkey | Same |
| **Email (SMTP)** | Transactional email | MailHog in dev, interface = `EmailService`. `send(template, to, context)` | Postmark (or AWS SES) in prod, same interface |
| **Tax calculation** | Line-item + shipping tax | `TaxService` with `FlatRateTaxStub` (configurable `TAX_RATE_PCT`, default 0) | `SquareTaxService` using Square's order-level tax, or TaxJar via interface |
| **Shipping rates** | Shipping cost at checkout | `ShippingService` with `FlatRateShippingStub` ($6.95 ground, $14.95 expedited, free > $99) | `EasyPostShippingService` behind same interface |
| **Address validation** | Normalize/verify shipping address | `AddressValidator` with `NoopValidator` (regex-only) | `SmartyStreetsValidator` behind same interface |
| **Fulfillment** | Mark orders shipped, track shipment | `FulfillmentService` with `ManualFulfillmentStub` (admin clicks "mark shipped", generates fake tracking number) | `ShipStationFulfillmentService` behind same interface |
| **Image CDN** | Product imagery | Flask-served from `static/catalog/images/` | CloudFront or Cloudflare Images |
| **Search** | Product full-text search | Postgres `tsvector` + `plainto_tsquery` — no new dep | Same (or Meilisearch behind `SearchService`) |
| **Analytics (site)** | Page views, funnel | `AnalyticsService` with `NoopAnalytics` | Plausible or GA4 |
| **Error tracking** | Exceptions | Stdout + Flask log | Sentry |
| **Feature flags** | Gate experimental flows | Simple env-var-backed `FeatureFlags` class | Same (no new dep) |
| **Auth — admin** | Admin users | Flask-Login + magic link (Canary pattern) | Same |
| **Auth — customer** | Customer accounts | Flask-Login + magic link (primary), password fallback | Same |
| **CSRF** | Form protection | Flask-WTF | Same |
| **Rate limiting** | Checkout + webhook abuse | Flask-Limiter backed by Valkey | Same |

---

## 4. Component inventory

Each component lists: **purpose**, **interface**, **v1 implementation**, **dependencies**, **stub notes**.

### 4.1 `services/square_client.py`

- **Purpose:** All Square API calls go through here. Single place to swap sandbox/production.
- **Interface:** `create_order`, `create_payment`, `create_refund`, `create_customer`, `save_card_on_file`, `charge_saved_card`, `retrieve_payment`, `verify_webhook_signature`.
- **v1:** Square Python SDK, sandbox. Wraps retry (tenacity) on 5xx, idempotency keys generated per call.
- **Deps:** `squareup` PyPI package, config.
- **Stub:** None. This is real v1.

### 4.2 `services/cart.py`

- **Purpose:** Cart lifecycle. Session-backed for guests, DB-persisted for logged-in customers. Add/remove/update lines, apply promotions (stubbed), compute totals.
- **Interface:** `Cart.load(request)`, `cart.add(product, qty)`, `cart.remove(line_id)`, `cart.update_qty(line_id, qty)`, `cart.apply_promo(code)`, `cart.totals()`.
- **v1:** Guest carts in Valkey DB 2 keyed by signed session cookie. Customer carts in `carts` table.
- **Stub:** `apply_promo` returns "not implemented" — promotion engine is stubbed.

### 4.3 `services/checkout.py`

- **Purpose:** Orchestrates the complete order-placement flow. The critical path.
- **Interface:** `place_order(cart, customer_info, address, payment_token, *, autoship_source=None, scenario_tag=None, placed_at=None)` → `Order`.
- **v1:** Full implementation. Called by storefront checkout AND by scenario runner (they use the same path).
- **Steps:**
  1. Validate cart against current inventory.
  2. Compute totals via `TaxService` + `ShippingService`.
  3. `square_client.create_order` with line items + taxes + shipping.
  4. `square_client.create_payment` with token → Square charges (sandbox).
  5. Persist `Order` + `OrderItem`s in a single DB transaction.
  6. `InventoryService.decrement_for_order` (same transaction).
  7. Enqueue confirmation email + analytics event.
  8. Return Order.
- **Errors:** any step failure rolls back DB, returns typed exception, nothing persisted. Square-side partial state handled by webhook reconciliation (§4.10).

### 4.4 `services/inventory.py`

- **Purpose:** Stock levels per SKU. All moves logged as immutable adjustments.
- **Interface:** `on_hand(product)`, `decrement(product, qty, reason, **ctx)`, `increment(product, qty, reason, **ctx)`, `adjust_to(product, target, reason, **ctx)`, `decrement_for_order(order)`, `increment_for_refund(refund)`.
- **v1:** Full implementation. Row-level locking on `inventories` during moves. `InventoryAdjustment` append-only.
- **Shrink events:** scenario runner calls `adjust_to` with `reason='shrink'` — produces the "disappearing inventory" Canary needs for GRO-297 shrink rules.
- **Stub:** Reorder automation is stubbed — low-stock triggers email to admin only, no PO generation.

### 4.5 `services/subscriptions.py`

- **Purpose:** Autoship — real subscription engine. Customer saves card, selects product + cadence, the system charges on schedule.
- **Interface:** `Subscription.create(customer, product, qty, cadence_days, starting_at)`, `.pause()`, `.resume()`, `.cancel()`, `charge_due_subscriptions()` (runs on a schedule).
- **v1:** Full architecture. Card-on-file via Square `save_card_on_file`. `Subscription` model with `next_charge_at`. rq-scheduler cron job calls `charge_due_subscriptions()` every 15 min, which finds due subs and runs each through `checkout.place_order(..., autoship_source=subscription_id)`.
- **Stub:** Customer-facing self-service subscription management UI (`/account/subscriptions`) is wired for view + cancel only. Pause/resume/skip-next are stubbed behind feature flag `SOLEX_FLAG_SUB_SELFSERVE=false`.

### 4.6 `services/refunds.py`

- **Purpose:** Issue refunds via Square, mark orders refunded, restore inventory.
- **Interface:** `issue_refund(order, amount_cents, reason, *, scenario_tag=None)`, `issue_full_refund(order, reason)`.
- **v1:** Full implementation. Calls `square_client.create_refund`, creates `Refund`, sets `Order.status = refunded|partially_refunded`, calls `InventoryService.increment_for_refund`, enqueues customer email.
- **Returns flow:** stubbed. Customer-initiated return request form exists (`/account/orders/<id>/return`) but creates a `ReturnRequest` that an admin manually approves → triggers refund. No RMA labels, no shipping-back logistics.

### 4.7 `services/catalog.py`

- **Purpose:** Browse, search, and manage product catalog.
- **Interface:** `list_products(category=None, search=None, page=1)`, `get_product(slug)`, `import_from_yaml(path)`, `sync_to_square()`, `build_search_index()`.
- **v1:** Full browse + search (Postgres `tsvector`). `import_from_yaml` is the primary seeder.
- **Stub:** `sync_to_square` — mirrors our catalog to Square's Catalog API. Not required for checkout (we pass inline line items), but useful for Canary rules that inspect catalog attributes. Implemented but behind feature flag `SYNC_CATALOG_TO_SQUARE=false` in v1.

### 4.8 `services/email.py` — `EmailService`

- **Purpose:** Transactional email abstraction.
- **Interface:** `send(template_name, to, **context)`. Templates: `order_confirmation`, `shipping_notification`, `refund_confirmation`, `subscription_charged`, `subscription_failed`, `magic_link`, `cart_abandonment`, `admin_low_stock`.
- **v1:** SMTP to MailHog in dev, real Postmark-compatible SMTP in staging. All 8 templates real.
- **Stub:** None — full templates in v1.

### 4.9 `services/scenarios/` — scenario runner

- **Purpose:** Admin-triggered batches of orders through the real checkout path. Each scenario produces a cohort of realistic transactions with declared characteristics.
- **Interface:** every scenario subclasses `Scenario`:
  ```python
  class Scenario:
      name: str
      description: str
      params_schema: ParamsModel  # pydantic
      def run(self, params: ParamsModel) -> ScenarioRun: ...
      def expected_chirps(self, params: ParamsModel) -> list[ExpectedChirp]: ...
  ```
- **Registered scenarios (v1):**
  | Name | Purpose | Canary rule coverage |
  |---|---|---|
  | `normal_retail_day` | 20–40 small-basket purchases spread across business hours | baseline, no chirps expected |
  | `after_hours_burst` | 5–15 orders between 22:00–02:00 local | C-002 AFTER_HOURS |
  | `round_amount_cluster` | 6–10 orders all ending in $0.00 | C-003 ROUND_AMOUNT |
  | `high_value_sale` | 1–3 orders ≥ $500 | C-001 HIGH_VALUE |
  | `autoship_cohort` | 15–30 repeat orders tagged autoship, same customers recurring | repeat-transaction pattern, Square card-on-file signal |
  | `bulk_reseller_order` | 1–2 orders with 10–30 line items each | volume anomaly; MLM reseller-to-reseller flavor |
  | `refund_wave` | Issues refunds against a cohort of prior orders | refund-pattern rule coverage |
  | `shrink_event` | Adjusts inventory down on 5–10 SKUs with `reason='shrink'` — no offsetting orders | GRO-297 shrink rule |
  | `cart_abandonment_cohort` | Creates and abandons carts at various funnel stages | funnel analytics, no chirps |
- **v1:** All 9 scenarios implemented. UI at `/admin/lab` lists them with per-scenario param forms. `Run` button enqueues an RQ job; run detail page shows progress + created orders + (eventually) which Canary chirps fired.
- **Execution model:** sync for ≤5 orders, RQ job for larger batches. Orders tagged `scenario_tag='<name>-<run_id>'` for traceability.
- **Stub:** "Which chirps actually fired" is stubbed — requires Canary read-side integration which we explicitly zero-couple. v1 shows `expected_chirps` from the scenario declaration; confirming they fired is a manual check in Canary's UI. Post-MVP: an optional read-only Canary API call to verify.

### 4.10 `services/webhooks.py`

- **Purpose:** Receive Square webhooks for payment/refund state reconciliation.
- **Interface:** `handle(event)`, plus route `/api/webhooks/square`.
- **v1:** Signature verification, event dispatch (`payment.updated`, `refund.updated`, `order.updated`). Idempotent via `SquareWebhookEvent` dedup table.
- **Why:** Handles the case where a Square payment transitions state out-of-band (e.g., disputed, reconciled). Without this, our order state drifts from Square.
- **Orphan-payment recovery:** If a webhook arrives for a `square_payment_id` we have no local `Order` for (e.g., DB write failed after Square charged), the handler issues an automatic refund via `refunds.issue_refund_by_payment_id` and logs to `admin_low_stock`-style admin alert. We do not synthesize local orders from webhook data — we reverse the payment and surface it.

### 4.11 `services/catalog_import.py`

- **Purpose:** Load `catalog/products.yaml` + `catalog/images/` into DB.
- **Interface:** CLI: `python3 -m solex.cli catalog import`.
- **v1:** Full. Idempotent (upsert by SKU). Manages image copy from `catalog/images/` to `static/catalog/images/`.
- **Source:** hand-curated YAML. ~25 SKUs covering Solex's categories (AO Scan devices, supplements, PEMF mats, red-light, bundles, pet). Prices and names reflect real Solex product line.

### 4.12 `services/auth.py`

- **Purpose:** Magic-link + password auth for both admin and customer users, mirroring Canary's pattern.
- **Interface:** `request_magic_link(email, audience)`, `consume_magic_link(token)`, `authenticate_password(email, password)`.
- **v1:** Full. Separate `AdminUser` and `Customer` tables, separate Flask-Login user loaders per blueprint.

### 4.13 `services/tax.py`, `services/shipping.py`, `services/addresses.py`, `services/fulfillment.py`

- Thin strategy-pattern services behind stub implementations (see §3 table). Each is a ~30-line interface + ~50-line stub. Real providers swap in without touching callers.

### 4.14 `services/analytics.py`

- **Purpose:** Page views, add-to-cart, checkout-started, purchase events.
- **v1:** `NoopAnalytics`. Interface and call sites are real; events are dropped.

### 4.15 `services/abandonment.py`

- **Purpose:** Find carts inactive ≥ 2h with items, send recovery email; 24h later, a final nudge.
- **v1:** Real. rq-scheduler cron every 30 min calls `run_abandonment_sweep()`.

### 4.16 `services/feature_flags.py`

- **Purpose:** Env-driven flags to gate experimental behavior.
- **v1:** Simple class reading `SOLEX_FLAG_*` env vars. No provider dep.

---

## 5. Data model

UUID PKs, `Mapped[]` syntax, `created_at` + `updated_at` everywhere, soft-delete via `deleted_at` where relevant.

### 5.1 Catalog

```
Category(id, name, slug, sort, parent_id?, deleted_at?)
Product(id, sku, slug, name, description, short_description, price_cents, compare_at_cents?,
        image_path, gallery_paths[], category_id, active, weight_grams, dimensions_json,
        square_catalog_object_id?, search_tsv, deleted_at?)
ProductTag(id, product_id, tag)            # for search/filter keywords
```

### 5.2 Inventory

```
Inventory(id, product_id [unique], on_hand, reorder_at?, updated_at)
InventoryAdjustment(id, product_id, delta, reason, order_id?, refund_id?,
                    scenario_tag?, admin_user_id?, note?)
      reason ∈ {sale, refund, restock, shrink, correction, initial}
```

### 5.3 Customers + auth

```
AdminUser(id, email, password_hash?, last_login_at?, active, deleted_at?)
Customer(id, email, password_hash?, first_name?, last_name?, phone?,
         square_customer_id?, default_address_id?, deleted_at?)
MagicLinkToken(id, audience, user_id, token_hash, expires_at, consumed_at?)
Address(id, customer_id, label, first_name, last_name, line1, line2?, city,
        region, postal_code, country, phone?, deleted_at?)
```

### 5.4 Cart

```
Cart(id, customer_id?, session_key?, currency, applied_promo_code?,
     last_activity_at, recovered_at?, abandonment_emailed_at?)
CartLine(id, cart_id, product_id, qty, price_snapshot_cents)
```

Guest carts may exist as Valkey-only (no DB row); on customer sign-in, Valkey cart migrates to `Cart`. **Merge semantics:** if the signing-in customer already has a persisted `Cart`, line quantities are summed by `product_id` (no dedup by price snapshot), and the most-recent `last_activity_at` wins. Applied promo code, if any, is preserved from the persisted cart.

### 5.5 Order

```
Order(id, public_token [short unguessable], customer_id?, customer_email, customer_name,
      shipping_address_json, billing_address_json,
      subtotal_cents, tax_cents, shipping_cents, total_cents, currency,
      status, square_order_id, square_payment_id?,
      autoship, autoship_subscription_id?, scenario_tag?,
      placed_at, fulfilled_at?, tracking_number?)
      status ∈ {pending, paid, shipped, delivered, refunded, partially_refunded, cancelled, failed}
OrderItem(id, order_id, product_id, sku_snapshot, name_snapshot, image_path_snapshot,
          price_snapshot_cents, qty, line_total_cents)
OrderNote(id, order_id, admin_user_id?, body, internal)
```

`public_token` is used in order-confirmation URLs to let guests access their order without login.

### 5.6 Subscriptions

```
Subscription(id, customer_id, product_id, qty, cadence_days,
             square_card_id, next_charge_at, status, paused_until?,
             last_charged_at?, created_at, cancelled_at?)
      status ∈ {active, paused, cancelled, past_due}
SubscriptionCharge(id, subscription_id, order_id?, attempted_at, succeeded, failure_reason?)
```

### 5.7 Refunds + returns

```
Refund(id, order_id, square_refund_id?, amount_cents, reason,
       admin_user_id?, scenario_tag?, created_at)
ReturnRequest(id, order_id, customer_id, reason, status,
              approved_by_admin_user_id?, created_at, resolved_at?)
      status ∈ {pending, approved, denied, completed}
```

### 5.8 Ops / observability

```
SquareWebhookEvent(id, square_event_id [unique], event_type, payload_json,
                   received_at, processed_at?, error?)
ScenarioRun(id, scenario_name, params_json, admin_user_id,
            started_at, completed_at?, status, summary_json)
      status ∈ {pending, running, succeeded, failed, partial}
EmailLog(id, template, to, sent_at, provider_message_id?, error?)
```

### 5.9 Migrations

Single Alembic head. Initial migration creates all tables. No backwards-compat shims — greenfield app.

---

## 6. Data flows

### 6.1 Guest checkout (happy path)

```
[browser]                       [flask]                         [square]
  add-to-cart (HTMX) ─────────▶ /cart/add
                                  session cart in Valkey
  /checkout  ────────────────▶ renders Jinja with Web Payments SDK
  card form tokenized ─────────────────────────────────▶ sandbox.web.squarecdn
  token returned ◀─────────────────────────────────────
  POST /checkout/submit ─────▶ checkout.place_order()
                                  tax.compute() [stub: flat %]
                                  shipping.compute() [stub: flat]
                                  square_client.create_order ────────▶
                                                       ◀── order_id
                                  square_client.create_payment ──────▶
                                                       ◀── payment succeeded
                                  DB tx: Order + OrderItems + Inventory decrements
                                  RQ: enqueue confirmation email
                                  302 /order/<public_token>
                                                                       (later)
                                                                       webhook payment.updated ──▶
                                                                       /api/webhooks/square
                                                                         reconcile state
[canary]                                                        ◀── same event to Canary's endpoint
                                (zero coupling; Canary observes via its own Square OAuth)
```

### 6.2 Autoship charge

```
rq-scheduler tick (every 15 min)
  → charge_due_subscriptions()
    → for each Subscription where next_charge_at ≤ now, status=active:
        square_client.charge_saved_card(square_card_id, amount)
        on success: checkout.place_order(..., autoship_source=sub.id)
                    sub.next_charge_at = now + cadence_days
                    sub.last_charged_at = now
        on failure: sub.status = past_due; enqueue subscription_failed email
```

### 6.3 Scenario run

```
admin clicks "Run: after_hours_burst" with {count: 12}
  → POST /admin/lab/scenarios/after_hours_burst/run
    → ScenarioRun row created, status=pending
    → if count ≤ 5: sync execution; else enqueue RQ job
  → scenario.run():
      for i in range(count):
          synthesize {customer, cart, placed_at in 22:00–02:00 window}
          checkout.place_order(..., scenario_tag=f"after_hours_burst-{run_id}",
                                placed_at=synthetic_time)
      ScenarioRun.summary_json += {orders_created, failures}
      status = succeeded | partial | failed
  → admin lab UI polls /admin/lab/runs/<id> for live summary
```

### 6.4 Refund

```
admin clicks "Refund" on order detail
  → POST /admin/orders/<id>/refund {amount, reason}
    → refunds.issue_refund()
      square_client.create_refund ──▶
                                   ◀── refund_id
      Refund row created
      Order.status = refunded | partially_refunded
      inventory.increment_for_refund
      email.send(refund_confirmation)
      (webhook refund.updated arrives later, marks Refund.square_refund_id settled)
```

### 6.5 Catalog import (one-shot)

```
developer runs: python3 -m solex.cli catalog import
  → reads catalog/products.yaml
  → for each product: upsert by sku
  → copy catalog/images/<sku>.jpg → static/catalog/images/<sku>.jpg
  → rebuild search_tsv on all products
  → report {inserted, updated, skipped}
```

---

## 7. UI / visual fidelity

### 7.1 Reference

`solexglobal.com` + `shop.solexnation.com`. Homepage, shop page, product detail, cart, checkout, account.

### 7.2 Approach

- Tailwind theme derived from Solex's actual palette (earthy greens, warm neutrals, frequency/biofield brand cues), extracted by eye from the reference site.
- Typography: match serif display + sans body pairing used on solexglobal.com (likely Montserrat + a display serif; confirm at implementation).
- Hero section: large lifestyle imagery + value prop (matches reference home).
- Shop page: grid of product cards, category filter (simple nav, not faceted).
- Product detail: gallery + description + quantity selector + autoship option + add-to-cart.
- Cart: slide-over drawer (Alpine) + full cart page.
- Checkout: single-page form, Square SDK card element.
- Account: order history, subscriptions list, saved addresses.

Visual fidelity is a pass *after* functional MVP lands. Layouts use placeholder imagery initially.

### 7.3 Header / nav

Matches reference: logo, primary nav (Shop, About, Blog, Events, Resources, University), cart icon + count. "Events" and "University" link to placeholder static pages (no CMS).

### 7.4 Footer

Matches reference: four-column layout, policy links (terms, privacy, refunds, shipping) — all placeholder static pages.

---

## 8. Security + compliance

- **Cloudflare Access password gate** on `solex.growdirect.app`. Not publicly discoverable.
- `<meta name="robots" content="noindex,nofollow">` on every page.
- `robots.txt: Disallow: /` at the root.
- **CSRF** on all POST forms (Flask-WTF).
- **Rate limiting** on `/checkout/submit`, `/api/webhooks/square`, `/auth/*` (Flask-Limiter on Valkey).
- **Webhook signature verification** mandatory; bad signature → 401.
- **PII handling:** customer email, name, address stored. No card data ever touches our servers — Square Web Payments SDK tokenizes client-side. Card-on-file is a Square token reference.
- **Legal banner** on admin-internal pages ("Sandbox environment — not a live business. Imagery and product info are used under fair-use research context for internal Canary testing only.").

---

## 9. Error handling

| Failure | Detection | Response |
|---|---|---|
| Square API 5xx | try/except in `square_client` with tenacity retry (3x, exp backoff) | If still failing: raise `SquareUnavailable`, caller rolls back, user sees "try again shortly" |
| Square API 4xx (bad card, decline) | HTTP status in response | Return typed `PaymentDeclined(reason)`, no Order persisted, user sees reason |
| Webhook signature bad | verify_signature fails | 401, no side effect, log |
| Webhook duplicate event | `SquareWebhookEvent.square_event_id` unique | 200 OK, no-op |
| DB constraint violation in order write | SQLAlchemy IntegrityError | Rollback transaction, return 500, log; Square payment may have succeeded — webhook reconciliation catches this |
| Inventory oversell race | row-level lock; if post-decrement `on_hand < 0` | v1: allow (sandbox, no goods). Log warning. Post-MVP: reject pre-payment |
| Scenario run failure mid-batch | exception in `place_order` loop | Continue loop, log per-item failure to `ScenarioRun.summary_json.failures[]`, final status = `partial` |
| Autoship charge declined | Square returns declined | `Subscription.status = past_due`, email customer, retry next tick up to 3 times, then cancel |
| Email send failure | EmailService exception | Log to `EmailLog.error`, enqueue retry (RQ retry policy: 3 tries) |

Nothing silent. Everything logged. Sandbox-era tolerances (oversell) documented and deferred to the live-mode cut-over spec (§1.4).

---

## 10. Testing

### 10.1 Unit tests

- Models: constraint checks, computed columns, `Mapped[]` shapes.
- Cart: add/remove/update, total computation, promo stub.
- Inventory: decrement/increment/adjust, row-level locking under concurrent access (using `SELECT FOR UPDATE`).
- Checkout: mocked Square client, verifies the full orchestration sequence.
- Refunds: mocked Square client.
- Subscriptions: `charge_due_subscriptions` scheduling + state transitions.
- Scenarios: each of the 9 scenario classes — param validation, order count, timestamp distribution, tag application.
- Tax/shipping stubs: flat-rate math.
- Email templates: render without error for all contexts.
- Webhook signature verification + event dispatch.
- Auth: magic link flow, password fallback, user-loader isolation between admin and customer audiences.

### 10.2 Integration tests

- Full checkout flow against **Square sandbox** (real API, test DB). Requires `SQUARE_SANDBOX_ACCESS_TOKEN` in test env.
- Refund flow against sandbox.
- Card-on-file save + charge against sandbox.
- Webhook endpoint receives a real sandbox webhook payload (captured fixture), dispatches correctly.
- Scenario runner end-to-end for each scenario: sandbox orders created, tags applied, summary correct.

### 10.3 Smoke tests

- `docker compose up` → check `/` renders, `/shop` lists seeded products, `/admin/login` shows form, webhook endpoint responds 401 on bad signature.

### 10.4 Test DB

Separate `solex_test`. Fixtures: `seed_catalog`, `seed_admin_user`, `seed_customer`, `seed_order`, `seed_subscription`.

### 10.5 CI

`pytest -m "not sandbox_live"` runs in CI by default (no Square API calls). Sandbox-live suite runs on-demand (requires secrets).

---

## 11. Deployment + operations

### 11.1 Dev

```
cd ~/GrowDirect/devops && docker compose up -d         # shared infra
cd ~/GrowDirect/Solex/devops && docker compose up -d   # solex web + worker
```

Flask served at `localhost:5003` with `--reload`. Worker runs `rq worker solex-default` and `rq-scheduler` in a second container.

### 11.2 Staging

`solex.growdirect.app` via Cloudflare tunnel to the same gunicorn, behind Cloudflare Access. Managed under the existing GrowDirect production infra plan (EC2 t3.micro).

### 11.3 Runbook essentials

- **Catalog reimport:** `docker compose exec web python3 -m solex.cli catalog import`
- **Scenario from CLI:** `docker compose exec web python3 -m solex.cli scenarios run after_hours_burst --count 10`
- **Reset sandbox merchant data:** documented but destructive (Square sandbox data is shared — per the `Square sandbox is shared` memory, we do NOT delete other apps' sandbox data).
- **Worker health:** `docker compose ps worker`; RQ queue depth in `/admin`.

---

## 12. Open questions

1. **Cloudflare Access audience.** Public password gate, or SSO-restricted to GrowDirect team emails only? (Default: team SSO; password gate only if SSO is fussy.)
2. **Whose email from-address?** `orders@solex.growdirect.app`? Or a made-up reseller identity? Decide at implementation.
3. **Post-MVP: Canary read-side integration for scenario verification.** Opt-in, read-only, through a documented Canary API endpoint. Not blocking.
4. **Catalog image licensing.** Fair-use-for-research argument relies on non-public access. If we later flip to public (even for marketing demos), imagery strategy needs revisiting.
5. **Distributor pricing.** Solex's real model has distributor vs. retail prices. v1 ignores this (single price per SKU). If we want `bulk_reseller_order` scenarios to reflect realistic wholesale discount, add `Product.wholesale_price_cents` + a `customer_role` flag post-MVP.

---

## 13. Related

- `docs/playbook-solex-square-merchant.md` — original playbook. Superseded for Phases 3–6.
- `Canary/canary/services/square_sandbox_seeder.py` — existing Canary seeder, remains in use for Canary's farmers-market demo merchant. Unaffected by this work.
- GRO-297 — inventory adjustments + shrink rule testing. This app's `shrink_event` scenario is the direct integration point.
- GRO-144 (Ops Dashboard), GRO-129 (Owl search) — will be demoed on this merchant post-MVP.
- `Brain/wiki/canary-platform-overview` — Canary context.
- CLAUDE.md — platform standards this spec follows.
