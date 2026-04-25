---
date: 2026-04-24
type: wiki
tags: [solex, square, integration, factory-cycle, gro-536]
sources: [Solex/solex/services/square_client.py, Solex/solex/services/checkout.py, Solex/solex/services/webhooks.py, Solex/solex/routes/api.py, Solex/solex/routes/lab.py, docs/dispatches/dispatch-solex-2026-04-24.md, docs/superpowers/specs/2026-04-23-solex-commerce-mockup-design.md]
last-compiled: 2026-04-24
needs-review: 2026-05-08
method-role: Writer
method-stage: close
---


**Wiki:** [[Brain/Home|Home]]

# Solex — Square Integration Notes

## Summary

Solex's Square sandbox commerce pipeline shipped under GRO-536 in factory cycle 2026-04-24. The pipeline is a complete checkout → payment → webhook reconciliation loop, observable through Canary's existing OAuth integration without any Canary code change. This note captures what shipped, what surprised us, and the patterns we'd reach for again.

## What shipped vs. what the dispatch claimed

The original dispatch (`docs/dispatches/dispatch-solex-2026-04-24.md`) overestimated remaining work because it was authored without grepping the current code. Of 8 planned tasks, 6 were already done in `fix/solex-live-debug-pass`. The cycle compressed from a planned 3–5 sessions of build to a single ship-and-document session.

| Dispatch task | Dispatch state | Reality at preflight |
|---|---|---|
| 1. `square_client.py` SDK wrap with retry + idempotency | not built | ✅ shipped — 367 lines, Tenacity retry, HMAC-SHA256 verify, idempotency key gen |
| 2. `checkout.place_order()` real implementation | stub | ✅ shipped — Square-first / DB-after, inventory in same tx |
| 3. Web Payments SDK on `/checkout` | not wired | ✅ shipped — sandbox CDN script, `card.tokenize()` → `/checkout/submit` → `place_order` |
| 4. `/api/webhooks/square` route | not built | ✅ shipped — signature verify, `IntegrityError`-based dedup, payment/refund/order dispatch |
| 5. `SquareWebhookEvent` model + migration | not built | ✅ shipped — model + table both in `alembic/versions/0001_initial.py` |
| 6. Inventory decrement on order | not built | ✅ shipped — `inventory.decrement_for_order()` w/ `with_for_update()` lock, called in `place_order` tx |
| 7. Admin lab MVP — single scenario | not built | ✅ shipped expanded — all 9 scenarios runnable (decision: accept) |
| 8. Sandbox-live e2e | not built | ✅ shipped — 3 sandbox-live tests, all green against real Square |

The 6 false-negatives in the dispatch are why **the founder's standing rule "don't assume things are broken — verify current state" matters**. A 30-minute audit before Stage 2 Research saved the cycle from blueprinting work that already existed.

## Component map

The pipeline has four layers. Each is a single Flask service or route with one job.

**`Solex/solex/services/square_client.py` — Square SDK wrapper.** 367 lines. Wraps `squareup==44.0.1.20260122`. Public surface: `create_order`, `create_payment`, `create_refund`, `create_customer`, `save_card_on_file`, `verify_webhook_signature`. Tenacity retries 5xx three times with exponential backoff. Exception taxonomy: `SquareTransient` (retried), `SquareDeclined` (4xx caller's fault, not retried), `SquareError` (everything else). Idempotency keys are UUIDv4 generated per call; survives retries via Tenacity.

**`Solex/solex/services/checkout.py:62` — `place_order()` orchestrator.** The critical invariant: Square API calls happen **before** any DB write. If Square fails, nothing persists locally. If the DB fails after Square succeeded, the webhook orphan-recovery path issues a refund. Sequence:

1. Compute subtotal, shipping quote, tax.
2. `square.create_order()` → Square order ID.
3. `square.create_payment(source_id=payment_token, amount, order_id)` → Square payment ID.
4. Insert `Order` row (`status='paid'`, holds both Square IDs).
5. Insert `OrderItem` rows.
6. `inventory.decrement_for_order(order)` writes `InventoryAdjustment` rows under a row-level lock.
7. `session.commit()`.
8. Email send wrapped in `try/except` so an SMTP outage doesn't crash checkout.

**`Solex/solex/routes/api.py:44` — `/api/webhooks/square` endpoint.** Reads body + `X-Square-HmacSha256-Signature` header + URL, hands them to `WebhooksService.handle()`. `BadSignature` → 401. `KeyError` on missing `event_id` → 400. Success → 204 (Square's preferred response).

**`Solex/solex/services/webhooks.py` — webhook dispatcher.** Verifies signature first. Dedups via `INSERT … ON UNIQUE square_event_id`; an `IntegrityError` short-circuits to a no-op (idempotent under replay). Dispatches by `type`:

- `payment.updated` → if a local order exists, no-op (informational); if not, **orphan-payment refund** via `RefundsService.issue_refund_by_payment_id()`.
- `refund.updated` → looks up `Refund` by `square_refund_id` and (Plan 1: touchpoint only).
- `order.updated` → no-op for Plan 1; Plan 2 admin UI will use it.

## Square SDK notes

- **Pin:** `squareup==44.0.1.20260122`. Versioning is calendar-based (Square ships breaking changes monthly), so the date in the version is the API rev. Worth re-pinning on each minor.
- **Sandbox auth:** `SquareClient` reads `SQUARE_SANDBOX_ACCESS_TOKEN` (Bearer), `SQUARE_SANDBOX_APPLICATION_ID`, `SQUARE_SANDBOX_LOCATION_ID`. The Web Payments SDK on the frontend reads only the application ID + location ID; the access token never leaves the server.
- **Test cards (sandbox-only):** `cnon:card-nonce-ok` (success), `cnon:card-nonce-declined` (decline), CVV/postal failure variants per Square docs. Auto-skip in `test_*sandbox*.py` if `SQUARE_SANDBOX_*` env vars missing.
- **Idempotency:** every `create_order` / `create_payment` / `create_refund` request includes a `idempotency_key` UUIDv4. Retries on transient 5xx use the same key (Tenacity replays the same call object), so Square dedupes server-side.
- **Webhook signature:** HMAC-SHA256 over `notification_url + body`, base64-encoded, compared in constant time against `X-Square-HmacSha256-Signature`. Keyed by `SQUARE_SANDBOX_WEBHOOK_SIGNATURE_KEY`. Rotation: change the key in the dashboard, deploy the new value, re-subscribe; Solex doesn't currently support a grace-period dual-key fallback.

## Webhook event types subscribed

The webhook dispatcher is wired for three event types out of Square's full catalog:

- `payment.updated` — primary signal that a charge completed (or refunded).
- `refund.updated` — refund lifecycle.
- `order.updated` — Square-side order changes (currently no-op, future admin UX surface).

Other event types Square sends are accepted (200 OK) and recorded in `square_webhook_events` but not dispatched to a handler. This is intentional: it preserves the audit trail without forcing handler logic for events the platform doesn't yet act on.

## Idempotency under replay

The `square_event_id` unique constraint on `square_webhook_events` is the dedup primitive. An `INSERT` that conflicts raises `IntegrityError`, the service rolls back the transaction, fetches the existing row, and returns it without re-running the dispatcher. Result: posting the same event ten times has the same effect as posting it once. The pattern is also used at the order layer via Square's idempotency key, so even if the webhook reconciliation logic re-fires `create_payment`, Square returns the same payment object.

## Admin lab — scope decision

The dispatch spec scoped the admin lab to a single scenario (`high_value_sale`). Reality on the branch: `Solex/solex/routes/lab.py` already supports all 9 registered scenarios (`after_hours_burst`, `autoship_cohort`, `bulk_reseller_order`, `cart_abandonment_cohort`, `high_value_sale`, `normal_retail_day`, `refund_wave`, `round_amount_cluster`, `shrink_event`). Each scenario synthesizes a cart, calls `place_order()` with `scenario_tag='<scenario>-<run_id>'`, and persists a `ScenarioRun` row.

**Decision (Stage 9, founder-delegated):** accept all 9. The implementation works, PR #8 confirmed `shrink_event` and the sandbox-live suite confirmed `high_value_sale`, and gating to one of nine adds work without value. The C2 cycle (next) reframes from "build full scenario runner" to "productionize the existing runner UX" — status indicators, run history filters, scenario detail views.

## Local dev — webhook tunneling

Square sandbox webhooks need a public URL. We use `cloudflared` ad-hoc per session:

```
cloudflared tunnel --url http://localhost:5003
```

Configure the resulting `https://*.trycloudflare.com/api/webhooks/square` in the Square dev dashboard's webhook subscription. The tunnel survives a Mac sleep but not a `cloudflared` process restart; if webhook deliveries stop, the URL needs re-registering. We don't currently run a persistent named tunnel — the ad-hoc pattern has been good enough through the cycle.

## RQ + Valkey scoping

Solex's RQ queue runs on Valkey DB 2 (Canary uses DB 0, Cove uses DB 1). Job naming convention: `solex.<jobname>`. The scenario runner enqueues to `solex.scenario_runner` when a synthesized cart count exceeds a threshold; smaller counts run synchronously in the request thread.

The `docker-compose.yml` rq worker command resolves `VALKEY_URL` at container runtime via shell-expanded env (Plan 4 fix; see PR #8 commit `b3016cd`) so Valkey's password isn't hardcoded in the compose file.

## Test surface

- **Unit (59 tests):** `tests/unit/test_services_*` — pure-Python coverage of `square_client`, `checkout`, `webhooks`, `inventory`, `refunds`, `subscriptions`, `returns`, `tax`, `shipping`, plus route-level rendering tests. All mock-based; no DB or network.
- **Integration (182 tests, non-sandbox-live):** `tests/integration/test_*` — Postgres-backed. Cover catalog import, scenario runs, webhook endpoint behavior, checkout submit, subscriptions at checkout, route handlers under DB conditions.
- **Smoke (23 tests):** `tests/smoke/test_visual_smoke.py` — every branded route renders.
- **Sandbox-live (3 tests, marked `@pytest.mark.sandbox_live`):** auto-skipped without `SQUARE_SANDBOX_*` env vars. Run via `docker compose -f devops/docker-compose.yml exec -T web pytest -m sandbox_live -v`. Cycle-closing run on 2026-04-24:
  - `test_checkout_sandbox.py::test_places_order_against_real_sandbox` — PASSED
  - `test_scenario_sandbox.py::test_high_value_scenario_against_sandbox` — PASSED
  - `test_subscriptions_sandbox.py::test_autoship_cycle_against_real_sandbox` — PASSED
  - 3 passed in 9.52s.

## Subscriptions, refunds, returns — built but parked-for-UX

These were marked deferred to C3/C4 in the dispatch. The plumbing actually exists:

- `Solex/solex/services/subscriptions.py` (159 lines) — autoship lifecycle, card-on-file via Square's customer + card storage, RQ-scheduler-backed renewal job.
- `Solex/solex/services/refunds.py` (46 lines) — manual refund issuance + the orphan-payment-recovery callsite from webhooks.
- `Solex/solex/services/returns.py` (51 lines) — return request workflow.
- `Subscription`, `Refund`, `Return` models all present.

The C3/C4 cycles re-purpose to "surface in admin/customer UX" rather than "build from scratch." The pipeline is complete; the views aren't.

## Patterns worth reusing

1. **Service-first orchestration in routes.** Routes like `api.py:44` are 20 lines of "parse request → call service → translate exception to HTTP status." All branch logic lives in service classes. Easy to test in isolation, easy to reason about in production.

2. **Square calls before DB writes.** The `place_order()` invariant — never persist a local order until Square has confirmed the charge — eliminates a class of "we charged the customer but lost the order" bugs. The trade-off is the orphan-payment refund path needs to exist; the trade-off is worth it.

3. **`IntegrityError` as a dedup primitive.** The webhook handler doesn't check-then-insert. It just inserts and catches the conflict. One round trip, no race window.

4. **Auto-skipping integration tests when creds are missing.** `pytest.mark.sandbox_live` plus a fixture that checks env vars and skips gracefully. CI runs the suite green even without Square access; developers with creds get the deeper validation. No two-tier test config.

## Risks parked

- **Cloudflare named tunnel.** Ad-hoc `trycloudflare.com` URL is fine for development but means the Square dashboard webhook subscription URL changes every time `cloudflared` restarts. A persistent named tunnel is on the C5 cycle.
- **Webhook signature key rotation.** No grace-period dual-key fallback. If we rotate the key in the dashboard before deploying the new value, webhooks 401 until the deploy lands. Operationally OK in sandbox; needs a plan for live mode.
- **Live mode flip.** Sandbox creds → production creds is a separate spec entirely (spec §1.4). No code change should be required, but the runbook around it is.

## Related

- [[Brain/projects/Canary|Canary MOC]] — Solex exists to feed Canary's merchant-feed observation
- [[docs/superpowers/specs/2026-04-23-solex-commerce-mockup-design|Solex commerce mockup spec]] — section 4 (the spec authority)
- [[docs/dispatches/dispatch-solex-2026-04-24|Original GRO-536 dispatch]] — superseded by the audit-corrected scope; kept as historical artifact

## Sources

- `Solex/solex/services/square_client.py` (cycle-current)
- `Solex/solex/services/checkout.py:62`
- `Solex/solex/services/webhooks.py`
- `Solex/solex/services/inventory.py`
- `Solex/solex/routes/api.py:44`
- `Solex/solex/routes/lab.py`
- `Solex/alembic/versions/0001_initial.py` — `square_webhook_events` table
- `Solex/tests/integration/test_checkout_sandbox.py`
- `Solex/tests/integration/test_scenario_sandbox.py`
- `Solex/tests/integration/test_subscriptions_sandbox.py`
- Linear: GRO-536 (description + audit comment)
- PR #8: https://github.com/growdirectprez/GrowDirect/pull/8
