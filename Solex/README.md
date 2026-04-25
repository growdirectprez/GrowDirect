# Solex

Canary-observable Square sandbox merchant. See
`../docs/superpowers/specs/2026-04-23-solex-commerce-mockup-design.md`.

## Dev quickstart

```bash
cp .env.example .env
# fill in Square sandbox credentials
cd devops && docker compose up -d
docker compose exec web python3 -m solex.cli catalog import
open http://localhost:5003
```

## Runbook

### Daily dev

```bash
cd ~/GrowDirect/Solex
./devops/scripts/dev.sh up     # start web + worker + mailhog
./devops/scripts/dev.sh logs   # tail web logs
./devops/scripts/dev.sh shell  # bash in web container
./devops/scripts/dev.sh test   # run pytest in web container
./devops/scripts/dev.sh down   # stop
```

### Reseed catalog

```bash
docker compose exec web python3 -m solex.cli catalog import
```

### Seed admin user (dev only)

```bash
docker compose exec web python3 -m solex.cli admin create-seed-user \
  --email dev@solex.local --password password
```

### Alembic

```bash
docker compose exec web alembic upgrade head
docker compose exec web alembic revision --autogenerate -m "<message>"
```

### Square sandbox test cards

- `cnon:card-nonce-ok` — successful payment
- `cnon:card-nonce-declined` — declined
- See Square docs for CVV/postal-code failure tokens.

### MailHog (dev email inbox)

Web UI: http://localhost:8027

### Webhook tunneling for local dev

Square sandbox webhooks require a public URL. Use Cloudflare Tunnel:

```bash
cloudflared tunnel --url http://localhost:5003
```

Configure the resulting URL + path `/api/webhooks/square` in the Square developer dashboard.

### Running the sandbox-live integration test

Requires `SQUARE_SANDBOX_*` env vars in `.env`:

```bash
docker compose run --rm -e SOLEX_ENV=testing web pytest -m sandbox_live -v
```

If creds are missing, the test is automatically skipped.

## Theme

Plan 4 ships with a branded Tailwind theme approximating Solex Global's look:

| Token | Hex | Use |
|---|---|---|
| `solex-teal`  | `#1F5961` | Primary accents, CTAs, logo |
| `solex-gold`  | `#B79355` | Eyebrows, badges, highlights |
| `solex-leaf`  | `#5E7A5A` | Secondary accents, hover states |
| `solex-clay`  | `#A35E3E` | Alerts, tertiary labels |
| `solex-cream` | `#F7F4EE` | Page background |
| `solex-sand`  | `#E8E0D1` | Subtle section backgrounds, image placeholders |
| `solex-ink`   | `#1C1C1A` | Headings, body text on light |
| `solex-body`  | `#3F3F3B` | Body copy |
| `solex-muted` | `#8A8A84` | Muted metadata |
| `solex-line`  | `#E5E2DC` | Dividers, borders |

Typography: Cormorant Garamond (display) + Inter (body) via Google Fonts.
Tune the palette in `Solex/tailwind.config.js` after seeing real screenshots
against `solexglobal.com`.

## Catalog

- 25 SKUs live in `catalog/products.yaml` across 4 categories (supplements 10,
  devices 5, therapy 5, pet 5).
- Imagery is Pillow-generated placeholder tiles (`solex/static/catalog/images/`).
  Real Solex product photos swap in post-merge.

### Regenerate placeholder tiles

```
docker compose exec web python3 -m solex.cli catalog generate-placeholders
```

### Drop in real imagery

1. Save each photo as JPG or PNG to `Solex/catalog/images/<sku>.<ext>` using
   the lowercased SKU.
2. Update `image_path` in `products.yaml` if the extension changes.
3. Run `docker compose exec web python3 -m solex.cli catalog import` — the
   importer copies updated images from `catalog/images/` to
   `solex/static/catalog/images/`.

See `docs/catalog-curation.md` for the full playbook.

## Feature surface

Solex is a complete Square-sandbox commerce platform. As of GRO-536 (cycle
2026-04-24, tag `solex-live-square-v1`), the following surfaces are live and
validated against real Square sandbox:

### Customer storefront

- `/`, `/shop`, `/shop/<category>`, `/products/<slug>` — branded 25-SKU catalog
- `/cart` + cart drawer (Alpine.js) — line items, quantity, subtotal
- `/checkout` — Square Web Payments SDK card element, shipping/billing address,
  optional autoship subscription enrollment
- `/checkout/submit` (POST) — consumes Square payment token, calls
  `services.checkout.place_order()`, persists `Order` + `OrderItem`s,
  decrements inventory under row-level lock, sends order confirmation email,
  redirects to `/order/<public_token>`
- `/account/login` (magic-link or password) → `/account/orders`,
  `/account/subscriptions`, `/account/addresses`, `/account/profile`
- 9 placeholder static pages: `/about`, `/events`, `/university`, `/blog`,
  `/resources`, `/privacy`, `/refunds`, `/shipping`, `/terms`

### Square integration (services layer)

- `services/square_client.py` — wraps `squareup==44.0.1.20260122`. Tenacity
  retry on transient 5xx, idempotency keys, HMAC-SHA256 webhook signature
  verify. Exception taxonomy: `SquareTransient`, `SquareDeclined`,
  `SquareError`. Methods: `create_order`, `create_payment`, `create_refund`,
  `create_customer`, `save_card_on_file`, `verify_webhook_signature`.
- `services/checkout.py:62` — `place_order()` orchestrator. Square calls
  before DB writes; one DB transaction for `Order` + `OrderItem`s + inventory
  decrements; orphan-payment refund path exists for "Square charged but DB
  failed" recovery.
- `services/inventory.py:32` — `decrement_for_order()` writes
  `InventoryAdjustment` rows with `with_for_update()` lock.
- `services/subscriptions.py` — autoship lifecycle, card-on-file, RQ-scheduled
  renewal jobs.
- `services/refunds.py`, `services/returns.py` — refund issuance + return
  request workflow (admin UX in C4).
- `services/scenarios/` — 9 cart-synthesis scenarios for testing observability:
  `after_hours_burst`, `autoship_cohort`, `bulk_reseller_order`,
  `cart_abandonment_cohort`, `high_value_sale`, `normal_retail_day`,
  `refund_wave`, `round_amount_cluster`, `shrink_event`.

### Webhooks

- `POST /api/webhooks/square` — signature verify (BadSignature → 401),
  dedup via `square_event_id` unique constraint, dispatch by type:
  - `payment.updated` — informational if local order exists; orphan-payment
    auto-refund if not
  - `refund.updated` — refund lifecycle touchpoint
  - `order.updated` — recorded but not dispatched (C2 admin UX surface)
- `square_webhook_events` table is append-only audit trail. All received
  events recorded regardless of dispatcher routing.

### Admin

- `/admin/login` (Flask-Login + magic-link), `/admin/` dashboard with
  Orders/Products/Subscriptions/Returns counts
- `/admin/catalog`, `/admin/inventory`, `/admin/orders`, `/admin/customers`,
  `/admin/returns`, `/admin/subscriptions` — CRUD surfaces
- `/admin/lab` — scenario runner for all 9 registered scenarios. Sync
  execution for low-count runs, RQ-async for higher counts. `ScenarioRun`
  rows persisted with full params + summary JSON. Run-detail at
  `/admin/lab/runs/<run_id>`.

## Test suite

- **Unit (59):** `tests/unit/test_services_*` + `tests/unit/test_routes_*` —
  pure-Python with mocked dependencies
- **Integration (182, non-sandbox):** `tests/integration/` — Postgres-backed
  integration tests
- **Smoke (23):** `tests/smoke/test_visual_smoke.py` — every branded route
  renders 200
- **Sandbox-live (3, opt-in):** `tests/integration/test_*sandbox*.py` —
  marked `@pytest.mark.sandbox_live`, auto-skipped without `SQUARE_SANDBOX_*`
  env vars. Cycle-closing run on 2026-04-24:
  - `test_checkout_sandbox::test_places_order_against_real_sandbox` — PASSED
  - `test_scenario_sandbox::test_high_value_scenario_against_sandbox` — PASSED
  - `test_subscriptions_sandbox::test_autoship_cycle_against_real_sandbox` — PASSED

Run the full non-sandbox suite:

```bash
docker compose -f devops/docker-compose.yml exec -T web pytest -m "not sandbox_live" -q
```

Run the sandbox-live suite (creds required in `.env`):

```bash
docker compose -f devops/docker-compose.yml exec -T web pytest -m sandbox_live -v
```

## Background

See `Brain/wiki/solex-square-integration-notes.md` for the integration
playbook — Square SDK version pinning, webhook signature flow, idempotency
strategy, RQ + Valkey scoping, and the cycle-2026-04-24 audit story
(6 of 8 dispatch tasks were already done).
