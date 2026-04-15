# Canary Account Management + Credit System Design

**Date:** 2026-04-15
**Status:** Design — no implementation exists
**Linear:** TBD (needs GRO issue)
**Scope:** Canary-internal (not a platform service)

---

## Purpose

Build a credit-based account management system for Canary, denominated in
satoshis, backed by Lightning via the Strike API, with tunable gas fees per
operation type. Every metered operation in Canary has a sat cost. GrowDirect
treasury pre-funds merchant wallets at onboarding to bootstrap adoption.

This design implements the account/billing layer described in the Goose SDD
(`docs/sdds/canary/goose.md`) Phase 0 — specifically the L402 gating, macaroon
tokens, Strike integration, and treasury wallet. It does NOT implement merchant
commerce wallets, BTCPay integration, or the 0.1% arbitrage micro-fee (all
future phases).

---

## Architecture Decisions

These are settled by this design session. Don't revisit without a reason.

1. **Canary-internal, not platform service.** Only Canary needs credit-based
   billing now. Cove is HOA assessments, Angel is a Cove module. Build in
   Canary with clean interfaces; extract later if needed.

2. **Custodial credit wallets.** GrowDirect holds the keys. This is Wallet 1
   territory (GrowDirect's own sats allocated to merchants). Not merchant
   commerce funds (Wallet 2, future). No money transmitter issue — promotional
   credit from GrowDirect's own treasury.

3. **Strike API end-to-end.** Invoice creation, payment confirmation, treasury
   management all through Strike. Customers pay from any Lightning wallet (Cash
   App, Strike, Phoenix, etc.) — it's all Lightning invoices on the wire.

4. **Macaroon at onboarding.** Minted when merchant completes Square OAuth and
   gets their internal UUID. Not at first payment. GrowDirect is the first
   payer.

5. **Tunable gas schedule.** Every metered operation has a sat cost in a
   `gas_schedule` table. Costs are adjustable without code changes. Initial
   values are placeholders — tuned from real usage data.

6. **Three meter categories.** Transactions processed, detection events, and
   compute operations. All draw from one shared sat balance per merchant. Single
   pool, not separate budgets per meter.

7. **Soft degradation on credit exhaustion.** Gold list alerts always visible
   (the hook). Premium features gate progressively. 402 with Strike invoice QR
   to refill.

---

## Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| PostgreSQL 17 (`canary` DB, `app` schema) | Infrastructure | Exists |
| Valkey 8 (DB 0) | Infrastructure | Exists |
| Strike API | External | **Not configured** — needs `STRIKE_API_KEY` |
| `canary/utils/crypto.py` (AES-256-GCM) | Internal | Exists |
| Identity domain — Square OAuth + merchant UUID | Internal | Exists |
| `pymacaroons` | Package | **Not installed** |
| Existing `Organization` model | Internal | Exists (has `billing_status`, `subscription_tier`) |
| Existing `square_oauth_wired.py` (OAuth callback) | Internal | Exists |

---

## Onboarding Flow

```
Merchant clicks "Connect with Square"
  → Square OAuth callback fires (existing flow)
  → Canary assigns internal merchant UUID (existing)
  → NEW: Goose creates merchant_wallet row (balance = 0)
  → NEW: Goose mints macaroon scoped to merchant UUID
         caveats: merchant_id, tier=free, expires_at
  → NEW: Goose funds wallet from GrowDirect Strike treasury
         (pre-configured initial_funding_sats from gas_schedule)
  → Macaroon set as l402_token HttpOnly cookie
  → Merchant lands on dashboard with credits loaded
```

The merchant never sees sats, Lightning, or crypto terminology. They see
"credits remaining" in their account. The underlying denomination is sats.

---

## Data Model (app schema)

**FK note:** All `merchant_id` FKs reference `app.merchants.id` (the internal
UUID). `Organization` is the billing root above merchants — the wallet is
merchant-scoped because metering happens at the merchant level (per-location
data). The `Organization` relationship is accessed through the existing
`merchants.organization_id` FK.

### New Tables

#### `merchant_wallets`

Custodial credit wallet per merchant. One wallet per merchant. Balance in sats.

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID PK | `uuid.uuid4` |
| `merchant_id` | UUID FK → merchants | Unique, one wallet per merchant |
| `balance_sats` | BIGINT | Current credit balance. Can go negative (grace). |
| `lifetime_funded_sats` | BIGINT | Total sats ever credited (treasury + self-funded) |
| `lifetime_spent_sats` | BIGINT | Total sats ever consumed |
| `warning_threshold_sats` | BIGINT | Default 20000. Alert merchant when balance drops below this absolute sat amount. |
| `hard_floor_sats` | BIGINT | Default 0. Below this, premium features gate. |
| `status` | VARCHAR(30) | `active`, `warning`, `depleted`, `suspended` |
| `funded_by` | VARCHAR(30) | `treasury`, `self`, `mixed` — who funded this wallet |
| `created_at` | TIMESTAMPTZ | |
| `updated_at` | TIMESTAMPTZ | |

#### `wallet_transactions`

Immutable ledger. Every credit and debit. INSERT-ONLY.

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID PK | |
| `wallet_id` | UUID FK → merchant_wallets | |
| `merchant_id` | UUID FK → merchants | Denormalized for query speed |
| `tx_type` | VARCHAR(30) | `credit`, `debit` |
| `source` | VARCHAR(50) | Credits: `treasury_fund`, `strike_payment`, `manual_credit`, `promo`. Debits: `gas_fee` |
| `operation_type` | VARCHAR(50) | Null for credits. For debits: matches `gas_schedule.operation_key` |
| `amount_sats` | BIGINT | Always positive. Direction determined by `tx_type`. |
| `balance_after_sats` | BIGINT | Running balance after this transaction |
| `reference_id` | UUID | FK to the triggering record (alert, transaction, case, invoice) |
| `reference_type` | VARCHAR(50) | `chirp_alert`, `tsp_transaction`, `fox_case`, `owl_query`, `strike_invoice` |
| `strike_invoice_id` | VARCHAR(255) | Null unless this is a Strike payment credit |
| `note` | TEXT | Optional human-readable note |
| `created_at` | TIMESTAMPTZ | |
| `updated_at` | TIMESTAMPTZ | Set once at insert, never modified. Present for platform compliance. |

**Indexes:** `wallet_id + created_at` (transaction history), `merchant_id + created_at` (merchant-scoped queries), `reference_id + reference_type` (reverse lookups).

#### `gas_schedule`

Tunable pricing table. Each operation type has a sat cost.

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID PK | |
| `operation_key` | VARCHAR(100) | Unique. e.g., `tsp.transaction.processed`, `chirp.alert.fired`, `fox.case.created` |
| `category` | VARCHAR(30) | `transaction`, `detection`, `compute` |
| `description` | TEXT | Human-readable description of what this operation is |
| `cost_sats` | BIGINT | Current cost in sats. 0 = free. |
| `is_active` | BOOLEAN | Can disable metering on specific operations |
| `tier_overrides` | JSONB | Optional per-tier pricing. `{"starter": 1, "pro": 0, "enterprise": 0}` |
| `created_at` | TIMESTAMPTZ | |
| `updated_at` | TIMESTAMPTZ | |

**Initial gas schedule (placeholder values — tune from real data):**

| operation_key | category | cost_sats | notes |
|---------------|----------|-----------|-------|
| `tsp.transaction.ingested` | transaction | 1 | Per transaction through TSP pipeline |
| `tsp.transaction.batch` | transaction | 10 | Per webhook batch processed |
| `chirp.alert.fired` | detection | 5 | Per Chirp rule hit surfaced as alert |
| `chirp.gold_list.fired` | detection | 0 | Gold list alerts are FREE (the hook) |
| `fox.case.created` | compute | 100 | Fox case creation |
| `fox.evidence.attached` | compute | 50 | Evidence attachment to case |
| `owl.query.basic` | compute | 25 | Owl basic search |
| `owl.query.deep` | compute | 250 | Owl deep analysis |
| `owl.health_check` | compute | 500 | Weekly health check report |
| `vault.recall` | compute | 10 | Memory recall from vault |
| `receipt.proof` | compute | 50 | TSP receipt verification proof |


**Note:** Initial treasury funding amount per merchant is configured via
`GOOSE_INITIAL_FUNDING_SATS` env var (default 100,000 sats), not in the gas
schedule. The gas schedule is for per-operation pricing only.

#### `macaroon_tokens`

Track minted macaroons. Not the token itself — the metadata.

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID PK | |
| `merchant_id` | UUID FK → merchants | |
| `macaroon_hash` | VARCHAR(255) | SHA-256 of the macaroon bytes (for lookup, not the secret) |
| `caveats` | JSONB | Snapshot of caveats at mint time |
| `status` | VARCHAR(30) | `active`, `exhausted`, `expired`, `revoked` |
| `minted_at` | TIMESTAMPTZ | |
| `expires_at` | TIMESTAMPTZ | From the `expires_at` caveat |
| `revoked_at` | TIMESTAMPTZ | Null unless revoked |
| `replaced_by` | UUID FK → macaroon_tokens | Points to the replacement token |
| `created_at` | TIMESTAMPTZ | |
| `updated_at` | TIMESTAMPTZ | Updated on status transitions (revoked, expired). |

#### `strike_invoices`

Track Strike Lightning invoices for credit refills.

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID PK | |
| `merchant_id` | UUID FK → merchants | |
| `wallet_id` | UUID FK → merchant_wallets | |
| `strike_invoice_id` | VARCHAR(255) | Strike's invoice identifier |
| `amount_usd` | NUMERIC(12,2) | USD amount requested |
| `amount_sats` | BIGINT | Sat equivalent at invoice creation |
| `conversion_rate` | NUMERIC(18,8) | USD/BTC rate at invoice time |
| `bolt11` | TEXT | Lightning invoice string (for QR). Encrypted at rest (AES-256-GCM). |
| `payment_hash` | VARCHAR(255) | Lightning payment hash. Populated on invoice creation. Encrypted at rest. |
| `preimage` | VARCHAR(255) | Lightning preimage (proof of payment). Populated on settlement. Encrypted at rest. |
| `state` | VARCHAR(30) | `pending`, `paid`, `expired`, `canceled` |
| `paid_at` | TIMESTAMPTZ | |
| `expires_at` | TIMESTAMPTZ | |
| `created_at` | TIMESTAMPTZ | |
| `updated_at` | TIMESTAMPTZ | Updated on state transitions. |

**Idempotency:** `strike_invoice_id` is the dedup key. On webhook redelivery,
check for existing record before processing. Return 200 on duplicate to
acknowledge without re-minting credits.

---

## Credit Lifecycle

### Phase 1: Treasury Funding (Onboarding)

```
GrowDirect Strike Wallet
  → Mint macaroon for merchant (caveats: merchant_id, tier, expires_at, endpoints)
  → INSERT merchant_wallet (balance = 0)
  → INSERT wallet_transaction (credit, source=treasury_fund, amount=100000 sats)
  → UPDATE merchant_wallet (balance = 100000)
  → Merchant starts using Canary
```

### Phase 2: Credit Consumption (Normal Usage)

```
TSP processes transaction for merchant
  → Look up gas_schedule for 'tsp.transaction.ingested' → 1 sat
  → Check merchant_wallet.balance_sats >= 1
  → INSERT wallet_transaction (debit, operation=tsp.transaction.ingested, amount=1)
  → UPDATE merchant_wallet (balance -= 1)
  → If balance < warning_threshold → set status = 'warning', notify merchant

Chirp fires gold list alert
  → Look up gas_schedule for 'chirp.gold_list.fired' → 0 sats
  → No debit. Alert surfaces for free. Always.

Merchant opens Fox case
  → Look up gas_schedule for 'fox.case.created' → 100 sats
  → Check balance >= 100
  → If yes: debit, proceed
  → If no: return 402 with Strike invoice QR
```

### Phase 3: Self-Funded Refill

```
Merchant sees "credits low" warning
  → Clicks "Add Credits" in dashboard
  → Canary calls Strike API: create Lightning invoice (e.g., $10 = ~10,000 sats)
  → Dashboard shows QR code (BOLT11 string)
  → Merchant scans with Cash App / Strike / any Lightning wallet
  → Strike webhook fires: invoice.paid
  → INSERT wallet_transaction (credit, source=strike_payment, amount=10000)
  → UPDATE merchant_wallet (balance += 10000)
  → Mint fresh macaroon with updated limits
  → Set l402_token cookie
```

---

## Soft Degradation

When credits run low, features degrade progressively — never a hard wall on
the alerts that sell the product.

| Wallet Status | Trigger | What's Gated | What's Free |
|---------------|---------|-------------|-------------|
| `active` | balance > warning_threshold | Nothing | Everything |
| `warning` | balance < warning_threshold_sats | Nothing (yet) — merchant sees banner | Everything + warning banner |
| `depleted` | balance <= hard_floor_sats | Fox, Owl, Vault, receipt proofs | Dashboard, alerts, gold list hits, basic views |
| `suspended` | balance < 0 for > 7 days | Everything except dashboard login | Dashboard read-only, "Add Credits" prompt |

Gold list alerts (C-502 POST_VOID, C-301 OFF_CLOCK, etc.) are **always free
and always visible.** They are the hook. A merchant who sees "Your cashier
voided $200 after the customer left" will pay to unlock Fox.

---

## L402 Middleware

### `@l402_required` Decorator

Applied to gated endpoints. Checks macaroon token before allowing access.

```python
# Pseudocode — actual implementation in canary/services/goose/l402_middleware.py

@l402_required
def owl_deep_analysis(merchant_id):
    # This only executes if:
    # 1. Valid macaroon present (cookie or Authorization header)
    # 2. Macaroon caveats satisfied (merchant_id, tier, not expired)
    # 3. Merchant wallet has sufficient balance for this operation
    # If any check fails → 402 with Strike invoice
    pass
```

### Verification Flow

```
Request arrives at gated endpoint
  → Check for l402_token cookie or Authorization: L402 <macaroon>:<preimage> header
  → If missing: 402 + create Strike invoice + return invoice in WWW-Authenticate
  → If Authorization header: verify preimage against payment_hash in strike_invoices
  → Verify macaroon HMAC chain against root key
  → Extract caveats: merchant_id, tier, expires_at
  → Check expires_at > now()
  → Check merchant_wallet.balance_sats >= gas_schedule cost for this operation
  → If all pass: debit wallet, set l402_token cookie (for subsequent requests), proceed
  → If expired or exhausted: 402 + new Strike invoice
```

**Cookie vs Header:** First request after payment uses `Authorization: L402
<macaroon>:<preimage>` (proves payment). Server verifies preimage, then sets
`l402_token` HttpOnly cookie for subsequent requests. Cookie-based requests
skip preimage verification — the cookie proves the server already validated
the payment.

### Macaroon Caveats

| Caveat | Purpose | Set At |
|--------|---------|--------|
| `merchant_id` | Tenant scoping | Mint time |
| `tier` | Feature gating (future tier differentiation) | Mint time |
| `expires_at` | Token expiry window | Mint time (default 30 days) |
| `endpoints` | Route restriction list | Mint time (default: all) |

**Note:** Usage metering (max_requests, max_sats) is tracked in the
`merchant_wallets` table, not in macaroon caveats. This allows real-time
balance updates without re-minting the token on every operation. The macaroon
authenticates the merchant; the wallet table authorizes the spend.

---

## Strike Integration

### Services

#### `StrikeClient` (`canary/services/goose/strike_client.py`)

Wraps Strike API. Handles:
- Invoice creation (amount in USD, receives sats equivalent)
- Invoice status polling
- Webhook signature verification (HMAC-SHA256)
- Account balance queries
- Currency conversion quotes

#### `TreasuryService` (`canary/services/goose/treasury.py`)

Manages GrowDirect's treasury operations:
- Fund merchant wallet from treasury
- Track treasury outflows (merchant funding) and inflows (merchant payments)
- Balance floor enforcement ($500 emergency reserve per Goose SDD)

### Env Vars (new)

| Variable | Purpose |
|----------|---------|
| `STRIKE_API_KEY` | Strike API authentication |
| `STRIKE_API_URL` | `https://api.strike.me/v1` (prod) or sandbox |
| `GOOSE_MACAROON_ROOT_KEY` | Root key for macaroon minting/verification |
| `GOOSE_WEBHOOK_SECRET` | HMAC secret for Strike webhook validation |
| `GOOSE_INITIAL_FUNDING_SATS` | Default treasury funding per merchant (100000) |
| `GOOSE_EMERGENCY_RESERVE_USD` | Minimum Strike balance floor (500) |

---

## API Contract

### Blueprint: `goose_api` — prefix `/goose`

| Route | Method | Auth | Purpose |
|-------|--------|------|---------|
| `/goose/wallet` | GET | Session | Merchant's wallet balance + recent transactions |
| `/goose/wallet/topup` | POST | Session | Create Strike invoice for credit refill |
| `/goose/wallet/topup/<invoice_id>` | GET | Session | Check payment status + QR page |
| `/goose/webhook/strike` | POST | Strike HMAC | Handle `invoice.updated` events |
| `/goose/gas-schedule` | GET | Session | Current gas prices (transparency) |
| `/goose/health` | GET | None | Service health + Strike API reachability |

### Admin / MCP Tools

| Route | Method | Auth | Purpose |
|-------|--------|------|---------|
| `/goose/admin/fund` | POST | Session + `@role_required('admin')` | Manually fund a merchant wallet from treasury |
| `/goose/admin/gas-schedule` | PUT | Session + `@role_required('admin')` | Update gas schedule pricing |
| `/goose/admin/treasury` | GET | Session + `@role_required('admin')` | Treasury balance + outflow summary |
| `/goose/admin/wallets` | GET | Session + `@role_required('admin')` | All merchant wallets overview |
| `/goose/admin/revoke/<macaroon_id>` | POST | Session + `@role_required('admin')` | Revoke a macaroon |

---

## Integration Points

### Square OAuth Callback (modify existing)

`canary/blueprints/square_oauth_wired.py` — after merchant UUID assignment,
call `GooseOnboardingService.provision_merchant(merchant_id)` which:
1. Creates `merchant_wallet` row
2. Mints macaroon
3. Funds wallet from treasury
4. Sets `l402_token` cookie

### TSP Pipeline (modify existing)

After Sub4 (Chirp detection) processes a transaction, emit a gas debit:
- `tsp.transaction.ingested` — 1 sat per transaction
- `chirp.alert.fired` — 5 sats per non-gold-list alert
- `chirp.gold_list.fired` — 0 sats (always free)

### Fox Case Management (modify existing)

On case creation: check wallet balance, debit `fox.case.created` (100 sats).
If insufficient: return 402 with refill prompt.

### Owl Analytics (modify existing)

On query: check wallet balance, debit `owl.query.basic` or `owl.query.deep`.
If insufficient: return 402.

---

## File Layout

```
Canary/canary/
├── services/goose/
│   ├── __init__.py
│   ├── strike_client.py      — Strike API wrapper
│   ├── macaroon_service.py   — Mint, verify, revoke macaroons
│   ├── l402_middleware.py     — @l402_required decorator
│   ├── wallet_service.py     — Credit/debit operations, balance checks
│   ├── treasury.py           — Treasury funding, balance management
│   ├── gas_meter.py          — Gas schedule lookup, debit orchestration
│   └── onboarding.py         — Merchant wallet provisioning at OAuth
├── blueprints/
│   └── goose_api.py          — /goose routes
├── models/app/
│   ├── merchant_wallet.py    — MerchantWallet model
│   ├── wallet_transaction.py — WalletTransaction model (INSERT-ONLY)
│   ├── gas_schedule.py       — GasSchedule model
│   ├── macaroon_token.py     — MacaroonToken model
│   └── strike_invoice.py     — StrikeInvoice model
└── migrations/
    └── versions/
        └── xxxx_goose_account_credit_system.py  — Alembic migration
```

---

## What's NOT in Scope

| Item | Why Not | When |
|------|---------|------|
| Merchant commerce wallets (Wallet 2) | Non-custodial, needs BTCPay, different legal | Goose Phase 1+ |
| BTCPay Server integration | Heavy infra, not needed for credit system | Goose Phase 1+ |
| 0.1% arbitrage micro-fee | Needs merchant commerce flow | Goose Phase 2+ |
| Cold storage automation | No treasury volume yet | Goose Phase 4 |
| LNURL-Auth (Lightning login) | Nice-to-have, not blocking | Goose Phase 5 |
| Separate meter pools per category | Complexity without data to justify it | Revisit after usage data |
| Platform-level billing service | Only Canary needs this now | Extract when Cove/Angel need it |

---

## Interconnections with Existing Goose SDD

This design implements a subset of `docs/sdds/canary/goose.md`:

| Goose SDD Component | This Design | Status |
|---------------------|-------------|--------|
| `goose_payments` table | Replaced by `wallet_transactions` + `strike_invoices` (more granular) | New design |
| `goose_treasury_moves` table | Handled by `wallet_transactions` with `source=treasury_fund` | Simplified |
| L402 middleware (`@l402_required`) | Included | Design ready |
| Macaroon minting + verification | Included | Design ready |
| Strike API integration | Included | Design ready |
| Treasury wallet architecture | Included (Wallet 1 only) | Design ready |
| Gated endpoints | Included | Design ready |
| MCP tools (`goose_*`) | Replaced by admin API routes | Simplified for Phase 0 |

The Goose SDD remains the canonical reference for the full vision (Phases 0-5).
This spec is the Phase 0 implementation plan.

---

## Security Considerations

- **Macaroon root key** is the most sensitive secret. Compromise = full token
  forgery. Store in env var for dev, AWS Secrets Manager for prod. Document
  rotation procedure.
- **Strike webhook HMAC** — verify signature on every webhook. Reject unsigned
  payloads. Forged webhooks = unauthorized credit minting.
- **wallet_transactions is INSERT-ONLY.** No UPDATEs, no DELETEs. This is the
  financial audit trail.
- **Encrypt at rest:** `strike_invoice_id`, `bolt11` in `strike_invoices` table
  via `canary/utils/crypto.py` (AES-256-GCM). Wallet balances are internal
  accounting, not PII — plaintext OK.
- **Rate limiting:** `/goose/wallet/topup` — 10/minute per merchant.
  `/goose/webhook/strike` — 100/minute global. Use existing Flask-Limiter.
