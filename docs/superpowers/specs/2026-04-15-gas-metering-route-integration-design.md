# Gas Metering Route Integration — Design Spec

**Date:** 2026-04-15
**Linear:** Pending (follows GRO-117)
**Status:** Design approved, pending implementation plan

---

## Problem

GRO-117 shipped the Goose credit system — wallets, gas schedule, gas meter, L402 middleware. But nothing in the app actually calls it. No endpoint is metered. No merchant wallet gets charged. The billing layer is completely isolated from the routes it's supposed to bill.

We need to wire gas metering into the app so we can see usage patterns with fictitious balances before going live with real payments.

## Design Policy

**Ingestion and detection are always free. Intelligence is paid.**

- Webhooks arrive, TSP processes, Chirp fires alerts — no charge, no gate, ever.
- Merchants pay when they consume intelligence: Owl analysis, Fox case management, receipt proofs.
- Analytics dashboards and charts are free — they're the product experience, not premium intelligence.
- Reading alerts, viewing cases, listing employees — free. These are operational.
- Creating cases, attaching evidence, querying the AI — paid. These consume compute.

**Nothing is public.** Every data endpoint requires JWT authentication. Receipt endpoints (previously public) get `@jwt_required` added. Closed by default, open only with a specific use case.

## Approach

New lightweight decorator `@gas_metered(operation_key)` that charges the merchant's wallet using the JWT session identity. No macaroon/L402 dependency. Soft gate — always passes through, never blocks.

This is metering, not gating. L402 enforcement is Phase 1 (blocked by Strike API credentials). This phase gets usage visibility immediately with zero merchant friction.

## New File

### `canary/services/goose/gas_metered.py` (~40 lines)

Decorator: `@gas_metered(operation_key: str)`

Flow:
1. Get `merchant_id` from JWT context (`g.merchant_id`)
2. If no `merchant_id` (unauthenticated request that somehow passed JWT): skip, pass through
3. Look up wallet via `WalletService.get_wallet(merchant_id)`
4. If no wallet: auto-provision wallet and fund it (see Wallet Provisioning section below)
5. Look up cost via `GasMeter.get_cost(operation_key, tier=None)`
6. If cost is 0 or operation not found: skip charge, pass through
7. Call `WalletService.debit(wallet_id, merchant_id, cost, operation_type=operation_key, reference_id=str(uuid4()), reference_type="http_request")` — this bypasses GasMeter.charge() because charge() blocks on insufficient balance. WalletService.debit() allows negative balances by design.
8. Log: operation_key, cost_sats, balance_after (from the returned WalletTransaction.balance_after_sats), wallet status
9. If wallet status is "depleted" or "warning": log warning, pass through (soft gate)
10. Set `g.gas_cost = cost` and `g.gas_wallet_status = wallet.status` on request context
11. Commit the session
12. Call the wrapped route handler

**Session management:** Uses the same Flask scoped session (`get_session()`), not a separate session. Commits the charge before yielding to the route handler. Same pattern as `@l402_required` in `l402_middleware.py`.

**Why bypass GasMeter.charge():** `GasMeter.charge()` checks `WalletService.check_balance()` and returns `charged=False, insufficient=True` when balance is insufficient. This is correct for hard gating but blocks our soft-gate requirement. The decorator uses `GasMeter.get_cost()` for price lookup, then calls `WalletService.debit()` directly to allow negative balances.

## Route Changes

### owl_api.py — 5 routes

| Route | Method | Existing Auth | Gas Operation |
|-------|--------|---------------|---------------|
| `/owl/one-thing` | POST | `@jwt_required` | `owl.query.basic` (25 sats) |
| `/owl/chat` | POST | `@jwt_required` | `owl.query.basic` (25 sats) |
| `/owl/drill` | POST | `@jwt_required` | `owl.query.deep` (250 sats) |
| `/owl/action` | POST | `@jwt_required` | `owl.query.deep` (250 sats) |
| `/owl/health-check` | POST | `@jwt_required` | `owl.health_check` (500 sats) |

Decorator stack: `@jwt_required` then `@gas_metered(...)`. Note: `owl_api.py` uses `@jwt_required` without parentheses. `fox_wired.py` uses `@jwt_required()` with parentheses. Match whatever each file already uses.

No changes to Owl MCP routes (`/owl/manifest`, `/owl/tools`, `/owl/health`) — those are infrastructure.

### fox_wired.py — 2 routes

| Route | Method | Existing Auth | Gas Operation |
|-------|--------|---------------|---------------|
| `POST /fox/cases` | POST | `@jwt_required`, `@roles_required` | `fox.case.created` (100 sats) |
| `POST /fox/cases/<id>/evidence` | POST | `@jwt_required`, `@roles_required` | `fox.evidence.attached` (50 sats) |

Decorator stack: `@jwt_required` then `@roles_required(...)` then `@gas_metered(...)`.

Read routes (`GET /fox/cases`, `GET /fox/cases/<id>`, `GET /fox/cases/<id>/evidence`) remain free.

### receipt_tsp.py — 2 routes

| Route | Method | Existing Auth | Gas Operation |
|-------|--------|---------------|---------------|
| `/receipt/by-hash/<hash>` | GET | **None (currently public)** | `receipt.proof` (50 sats) |
| `/receipt/by-event/<id>` | GET | **None (currently public)** | `receipt.proof` (50 sats) |

Changes:
1. Add `@jwt_required` (these were public, now closed)
2. Add `@gas_metered("receipt.proof")`

`/receipt/health` stays public (health check).

**Merchant scoping:** Adding `@jwt_required` means `g.merchant_id` is available. The `_build_receipt()` query currently looks up by `event_hash` or `event_id` without filtering by merchant. Add a `merchant_id` filter to the query so merchants can only look up their own receipts. Cross-merchant lookups return 404.

## Wallet Provisioning

Merchants who onboarded before Goose don't have wallets. The decorator auto-provisions on first metered request.

**Do NOT use `GooseOnboardingService.provision_merchant()`** — that method also mints a macaroon token as a side effect, creating orphaned macaroon records we don't need. Instead, the decorator provisions directly:

1. Create wallet via `WalletService` (or direct model insert): `MerchantWallet(merchant_id=merchant_id, balance_sats=0, status="active")`
2. Fund via `TreasuryService.fund_merchant(merchant_id, initial_funding_sats)` where `initial_funding_sats` comes from `GOOSE_INITIAL_FUNDING_SATS` (default 100k)
3. Commit

This is idempotent — check for existing wallet before creating. Merchant never notices, no friction. No macaroon minted.

## Soft Gate Behavior

| Scenario | Behavior |
|----------|----------|
| Wallet has sufficient balance | Charge, pass through |
| Wallet at 0 or negative | Charge (goes more negative), log warning, pass through |
| No wallet exists | Auto-provision (100k sats), charge, pass through |
| No merchant_id in context | Skip metering, pass through |
| Gas operation not in schedule | Skip metering (GasMeter returns 0 cost), pass through |
| DB error on charge | Log error, pass through (never block on billing failure) |

## What Does NOT Change

- No changes to TSP pipeline, Chirp detection, or webhook processing
- No changes to alert endpoints (read/investigate/dismiss/escalate)
- No changes to analytics or chart endpoints
- No changes to employee, location, or merchant profile endpoints
- No changes to MCP blueprint routes
- No changes to auth, health, or ops console routes
- No L402/macaroon dependency — purely JWT + gas meter
- Gas schedule stays as-is (11 operations, same costs)

## Observability

After this ships, the admin dashboard (`/goose/admin/wallets`, `/goose/admin/treasury`) shows:

- Per-merchant wallet balance (draining from 100k toward 0 and negative)
- Transaction history (every metered request is a `wallet_transaction` row)
- Which operations merchants use most (group by `operation_type`)
- Which merchants burn through credits fastest
- Treasury summary (total funded vs total spent)

No new dashboards or UI needed — the existing Goose admin routes already expose this data.

## Tests

Unit tests for `@gas_metered` decorator:

1. Metered request with existing wallet — charges correct amount, verify wallet_transaction row created
2. Metered request with no wallet — auto-provisions (wallet + treasury fund, no macaroon), then charges
3. Metered request with depleted wallet — debits into negative balance, passes through, logs warning
4. Metered request with no JWT context (`g.merchant_id` missing) — skips, passes through
5. Metered request with unknown operation_key — skips (0 cost from `get_cost()`), passes through
6. DB error during charge — logs error, passes through (never blocks on billing failure)
7. Verify `g.gas_cost` and `g.gas_wallet_status` set on request context after charge
8. Auto-provision does NOT mint a macaroon — verify no `MacaroonToken` rows created

Integration tests:

9. Full flow: JWT auth -> hit Owl endpoint -> verify wallet_transaction created with correct operation_key and cost_sats
10. Receipt endpoint: returns 401 without JWT (previously public)
11. Receipt endpoint: with JWT, can only look up own merchant's receipts (merchant scoping)

## Files Changed

| File | Change |
|------|--------|
| `canary/services/goose/gas_metered.py` | **New** — decorator implementation |
| `canary/blueprints/owl_api.py` | Add `@gas_metered` to 5 routes |
| `canary/blueprints/fox_wired.py` | Add `@gas_metered` to 2 routes |
| `canary/blueprints/receipt_tsp.py` | Add `@jwt_required` + `@gas_metered` to 2 routes, add merchant_id scoping to `_build_receipt()` query |
| `tests/unit/test_gas_metered.py` | **New** — 8 unit tests |
| `tests/integration/test_gas_metered_routes.py` | **New** — 3 integration tests |

## Future (Not This Spec)

- L402 enforcement (hard gate with 402 + Lightning invoice) — Phase 1, needs Strike credentials
- Background charging in TSP/Chirp pipelines — separate design decision
- MCP tool call metering — separate gas operations needed
- Usage dashboard UI — currently admin API only
