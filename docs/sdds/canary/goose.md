# Goose — Credit System & L402 Gate

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]
**Architecture:** [[docs/sdds/canary/architecture|Canary Architecture SDD]]
**Service Type:** App Service (Canary blueprint)
**Implementation Status:** Phase 0 complete (GRO-117, 2026-04-15)
**Linear:** [GRO-117](https://linear.app/growdirect/issue/GRO-117)

---

## Purpose

Goose is Canary's monetization layer. It manages prepaid sat-denominated merchant wallets, meters per-operation gas charges, and gates intelligence endpoints with L402 macaroon tokens. GrowDirect operates on a Bitcoin standard — USD is the interface, BTC is the unit of account.

The design shifted during implementation from a subscription model (pay monthly, get access) to a prepaid credit model (treasury funds a wallet, gas meter charges per operation). This gives finer-grained billing — a TSP ingestion costs 1 sat, an Owl deep query costs 250 sats, and gold list alerts are free.

L402 Lightning payment is the planned external funding channel. Phase 0 builds the credit system and gas meter; Strike integration is wired but requires API credentials to activate.

---

## What Shipped (Phase 0)

- 5 database tables (`app` schema)
- 8 services
- 11 API routes (blueprint: `goose_api` on `/goose` prefix)
- 58 tests (10 test files)
- 1 Alembic migration (`goose_a00001`)
- 6 config vars
- `pymacaroons>=0.13.0` dependency

---

## Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| PostgreSQL 17 (`canary` DB, `app` schema) | Infrastructure | Active |
| Valkey 8 (DB 0) | Infrastructure | Active |
| Strike API | External | **Not wired — needs API credentials** |
| `canary/utils/crypto.py` | Internal | Active (AES-256-GCM for bolt11, payment_hash, preimage) |
| Identity domain (GRO-267) | Internal | Active (`merchant_id` FK) |
| `pymacaroons>=0.13.0` | Package | Installed |

---

## Data Model (app schema, 5 tables)

### merchant_wallets

One wallet per merchant. Custodial sat balance with status derived from thresholds.

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID PK | |
| `merchant_id` | VARCHAR(36), unique | FK to merchants |
| `balance_sats` | BIGINT | Current balance |
| `lifetime_funded_sats` | BIGINT | Total credits ever received |
| `lifetime_spent_sats` | BIGINT | Total debits ever charged |
| `status` | VARCHAR(20) | `active` / `warning` / `depleted` / `suspended` |
| `funded_by` | VARCHAR(20) | `treasury` / `self` / `mixed` (one-way transitions) |
| `warning_threshold_sats` | BIGINT | Default 20,000 |
| `hard_floor_sats` | BIGINT | Default 0 |
| `created_at`, `updated_at` | TIMESTAMP | |
| `created_by`, `modified_by` | VARCHAR | Audit |

Status is derived from balance: `active` (> warning_threshold), `warning` (> hard_floor), `depleted` (<= hard_floor). `suspended` requires a scheduled job (not yet implemented).

### wallet_transactions

INSERT-ONLY financial ledger. Immutability enforced via SQLAlchemy `before_update` and `before_delete` event listeners + CHECK constraint.

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID PK | |
| `wallet_id` | UUID FK | References merchant_wallets |
| `merchant_id` | VARCHAR(36) | Denormalized for fast per-merchant queries |
| `tx_type` | VARCHAR(10) | `credit` / `debit` |
| `source` | VARCHAR(50) | `treasury_fund` / `strike_payment` / `promo_credit` / `refund_credit` / `gas_fee` |
| `operation_type` | VARCHAR(100) | Gas schedule operation_key (debits only) |
| `amount_sats` | BIGINT | Always positive (CHECK constraint) |
| `balance_after_sats` | BIGINT | Wallet balance after this transaction |
| `reference_id` | VARCHAR(255) | E.g., chirp alert ID, TSP transaction ID |
| `reference_type` | VARCHAR(100) | E.g., `chirp_alert`, `tsp_transaction`, `fox_case` |
| `strike_invoice_id` | VARCHAR(255) | For `strike_payment` credits only |
| `note` | TEXT | Free-form audit text |
| `created_at`, `updated_at` | TIMESTAMP | Set once at insert — immutable |

### gas_schedule

Per-operation pricing. 11 operations seeded. Tier-specific overrides via JSONB.

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID PK | |
| `operation_key` | VARCHAR(100), unique | E.g., `tsp.transaction.ingested`, `owl.query.deep` |
| `category` | VARCHAR(50) | `transaction` / `detection` / `compute` |
| `description` | TEXT | Human-readable |
| `cost_sats` | BIGINT | Base cost (0 = free) |
| `is_active` | BOOLEAN | Default true |
| `tier_overrides` | JSONB | Optional `{tier_name: cost_sats}` |
| `created_at`, `updated_at` | TIMESTAMP | |

**Seeded operations:**

| Operation Key | Category | Cost (sats) |
|---------------|----------|-------------|
| `tsp.transaction.ingested` | transaction | 1 |
| `tsp.transaction.batch` | transaction | 10 |
| `chirp.alert.fired` | detection | 5 |
| `chirp.gold_list.fired` | detection | 0 (free) |
| `fox.case.created` | compute | 100 |
| `fox.evidence.attached` | compute | 50 |
| `owl.query.basic` | compute | 25 |
| `owl.query.deep` | compute | 250 |
| `owl.health_check` | compute | 500 |
| `vault.recall` | compute | 10 |
| `receipt.proof` | compute | 50 |

### macaroon_tokens

L402 bearer token metadata. Raw macaroon bytes never stored — only SHA-256 hash.

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID PK | |
| `merchant_id` | VARCHAR FK | Indexed with status |
| `macaroon_hash` | VARCHAR(255) | SHA-256 hex digest |
| `caveats` | JSONB | Snapshot at mint: merchant_id, tier, expires_at, endpoints |
| `status` | VARCHAR(20) | `active` / `revoked` / `expired` / `replaced` |
| `minted_at` | TIMESTAMP | |
| `expires_at` | TIMESTAMP | |
| `revoked_at` | TIMESTAMP | Null if not revoked |
| `replaced_by` | UUID FK (self) | Token rotation chain |
| `created_at`, `updated_at` | TIMESTAMP | |

### strike_invoices

Lightning invoice records. Sensitive fields encrypted at rest.

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID PK | |
| `merchant_id` | VARCHAR FK | |
| `wallet_id` | UUID FK | References merchant_wallets |
| `strike_invoice_id` | VARCHAR(255), unique | Strike-issued ID, webhook idempotency key |
| `amount_usd` | NUMERIC(12,2) | |
| `amount_sats` | BIGINT | |
| `conversion_rate` | NUMERIC(18,8) | BTC/USD at creation time |
| `bolt11_enc` | TEXT | **Encrypted** (AES-256-GCM) |
| `payment_hash_enc` | VARCHAR(255) | **Encrypted** |
| `preimage_enc` | VARCHAR(255) | **Encrypted**, populated only on settlement |
| `state` | VARCHAR(20) | `pending` / `paid` / `expired` / `canceled` |
| `paid_at` | TIMESTAMP | Null until settled |
| `expires_at`, `created_at`, `updated_at` | TIMESTAMP | |

---

## Data Flow & PII Map

### What Enters

| Source | Data | Format |
|--------|------|--------|
| Identity domain (OAuth callback) | `merchant_id` | UUID from `merchants` table |
| Strike webhook (`invoice.updated`) | Payment confirmation | JSON webhook payload |
| Client HTTP request | `Authorization: L402 <macaroon>:<preimage>` or `l402_token` cookie | Header / cookie |
| Admin routes | Fund, revoke, gas schedule updates | JSON via JWT-authenticated requests |

### PII Classification

| Table | Field | Classification | Encryption |
|-------|-------|---------------|------------|
| `strike_invoices` | `bolt11_enc` | **sensitive** | AES-256-GCM |
| `strike_invoices` | `payment_hash_enc` | **sensitive** | AES-256-GCM |
| `strike_invoices` | `preimage_enc` | **sensitive** | AES-256-GCM |
| `strike_invoices` | `strike_invoice_id` | **sensitive** | Plaintext (idempotency key, needed for webhook lookup) |
| `macaroon_tokens` | `macaroon_hash` | internal | Plaintext (hash, not the token) |
| All tables | `merchant_id` | internal | Plaintext (FK reference) |
| `wallet_transactions` | `amount_sats`, `balance_after_sats` | internal | Plaintext |

### What Exits

| Destination | Data | Format |
|-------------|------|--------|
| Client browser | `l402_token` HttpOnly cookie | Signed macaroon |
| Client/agent | `402 Payment Required` + cost info | JSON response |
| Strike API | Invoice creation, balance queries | HTTPS API calls |
| `app.*` tables | INSERT-ONLY records | SQLAlchemy writes |

---

## Services (8)

### WalletService (`canary/services/goose/wallet_service.py`)

Manages merchant sat balances with FOR UPDATE row locking (TOCTOU prevention).

| Method | Purpose |
|--------|---------|
| `get_wallet(merchant_id)` | Fetch wallet or None |
| `check_balance(wallet_id, required_sats)` | Balance check |
| `credit(wallet_id, merchant_id, amount_sats, source, ...)` | Add sats, update status/funded_by |
| `debit(wallet_id, merchant_id, amount_sats, operation_type, ...)` | Charge sats, allows negative balance (grace) |

### GasMeter (`canary/services/goose/gas_meter.py`)

Per-operation billing. Looks up cost from gas_schedule, charges wallet.

| Method | Purpose |
|--------|---------|
| `get_cost(operation_key, tier)` | Returns cost in sats (0 if inactive/missing/free) |
| `charge(merchant_id, operation_key, reference_id, reference_type, tier)` | Lookup + balance check + debit. Returns `ChargeResult` |

Free operations (cost=0) skip debit entirely. Tier overrides take precedence over base cost.

### MacaroonService (`canary/services/goose/macaroon_service.py`)

L402 token lifecycle. Raises `ValueError` if `GOOSE_MACAROON_ROOT_KEY` is empty.

| Method | Purpose |
|--------|---------|
| `mint(merchant_id, tier, ttl_days, endpoints)` | Create macaroon with first-party caveats, store hash in DB |
| `verify(macaroon_bytes)` | HMAC signature + expiry + revocation check. Returns `VerifyResult` |
| `revoke(token_id)` | Set status=revoked, populate revoked_at |

### StrikeClient (`canary/services/goose/strike_client.py`)

Strike API wrapper. All methods raise `StrikeClientError` on non-2xx.

| Method | Purpose |
|--------|---------|
| `create_invoice(amount_usd, description)` | POST /invoices |
| `get_invoice(invoice_id)` | GET /invoices/{id} |
| `get_quote(amount_usd)` | POST /rates/tick (USD->BTC rate) |
| `get_balance()` | GET /balances |
| `verify_webhook(body, signature)` | HMAC-SHA256 timing-safe verification |

### GooseOnboardingService (`canary/services/goose/onboarding.py`)

Provisions wallet + macaroon at OAuth. Idempotent — returns existing wallet if found.

| Method | Purpose |
|--------|---------|
| `provision_merchant(merchant_id, tier)` | Create wallet -> mint macaroon -> fund via treasury. Returns `ProvisionResult` |

Default initial funding: 100,000 sats (via `GOOSE_INITIAL_FUNDING_SATS`).

### TreasuryService (`canary/services/goose/treasury.py`)

Admin-facing funding and reporting.

| Method | Purpose |
|--------|---------|
| `fund_merchant(merchant_id, amount_sats, note)` | Credit wallet from treasury. Warns if total > 10M sats |
| `get_treasury_summary()` | Aggregate stats: total_funded, total_self_funded, merchant count, reserve floor |

### seed.py (`canary/services/goose/seed.py`)

`seed_gas_schedule(session)` — idempotent seeder for 11 gas operations.

### l402_middleware.py (`canary/services/goose/l402_middleware.py`)

`@l402_required(operation_key)` decorator.

Flow: extract token (cookie or header) -> verify macaroon -> charge gas -> set `g.l402_merchant_id` and `g.l402_tier` -> pass through.

On failure: returns 402 with `{error, reason, cost_sats}`.

---

## API Contract

### Blueprint: `goose_api` (prefix: `/goose`)

| Route | Method | Auth | Purpose |
|-------|--------|------|---------|
| `/goose/health` | GET | None | Service health + Strike config status |
| `/goose/wallet` | GET | JWT | Wallet details + last 20 transactions |
| `/goose/wallet/topup` | POST | JWT (10/min) | Create Strike invoice for wallet credit |
| `/goose/wallet/topup/<invoice_id>` | GET | JWT | Check invoice status |
| `/goose/gas-schedule` | GET | JWT | List active gas operations and costs |
| `/goose/webhook/strike` | POST | HMAC (100/min) | Handle Strike invoice.updated events |
| `/goose/admin/fund` | POST | JWT + admin | Fund merchant wallet from treasury |
| `/goose/admin/gas-schedule` | PUT | JWT + admin | Update operation costs |
| `/goose/admin/treasury` | GET | JWT + admin | Treasury summary stats |
| `/goose/admin/wallets` | GET | JWT + admin | List all merchant wallets |
| `/goose/admin/revoke/<macaroon_id>` | POST | JWT + admin | Revoke a macaroon token |

CSRF exempt. Onboarding gate passthrough configured.

---

## L402 Protocol — Current State and Gaps

### What Works

- Macaroon minting with first-party caveats (merchant_id, tier, expires_at, endpoints)
- Macaroon HMAC verification + expiry check + revocation check
- `@l402_required` decorator extracts token, verifies, charges gas
- Admin revocation via `/goose/admin/revoke/<id>`
- Macaroon provisioned automatically at merchant onboarding

### What Does Not Work Yet

| Gap | Impact | Blocked By |
|-----|--------|------------|
| **No endpoint uses `@l402_required` for hard gating** | 9 endpoints now use `@gas_metered` for soft-gate metering (Owl: 5, Fox: 2, Receipt: 2). L402 hard gating with `@l402_required` remains deferred to Phase 1 (requires Strike credentials). | Strike API credentials for L402 402 responses |
| **402 response has no Lightning invoice** | Middleware returns `{error, reason, cost_sats}` — not `WWW-Authenticate: L402 macaroon="...", invoice="lnbc..."` per L402 spec | Strike API credentials |
| **Strike webhook not testable** | Handler code exists, HMAC verification exists, but no real webhooks arrive | Strike API credentials |
| **Top-up flow incomplete** | Route exists, creates Strike invoice, stores encrypted bolt11 — but no real invoice is generated | Strike API credentials |
| **No macaroon renewal** | Onboarding mints one token. When it expires, no self-service re-mint. Admin can revoke but not re-issue via API. | Needs renewal endpoint or auto-renewal on topup |
| **`receipt_tsp.py` ungated** | Explicit comment: "Sprint 7+ wraps this with L402 Lightning payment verification" | Goose Phase 0 completion (done), but gating decision pending |

### Cross-SDD L402 References (need updating)

| SDD | Reference | Issue |
|-----|-----------|-------|
| `external-identities.md` (line 402) | References `goose_payments` table | Table doesn't exist — now `wallet_transactions` + `strike_invoices` |
| `platform-overview.md` (line 42) | Describes Goose as "Phase 2" | Phase 0 is now complete |
| `architecture.md` (line 414) | Link only — accurate | No change needed |

---

## The Bitcoin Standard

GrowDirect's treasury operates in BTC. USD is the interface, not the unit of account.

```
USD in (merchant self-service top-up via Strike)
  -> Strike converts to sats at market rate
  -> sats credited to merchant_wallets.balance_sats
  -> gas meter charges per operation (1-500 sats each)
  -> gold list alerts are free (0 sats)

Treasury funding (admin):
  -> TreasuryService.fund_merchant credits wallet from GrowDirect reserves
  -> initial onboarding grant: 100,000 sats (~$10)
  -> tracked as source="treasury_fund" in wallet_transactions
```

Key design decisions:
- Revenue denominated in an appreciating asset
- No bank dependency for international merchants (8 Square countries)
- Per-operation pricing aligns cost with value delivered
- Gold list (top detection rules) are free — the hook
- Agent-to-agent micropayments don't work with USD rails

---

## Macaroon Caveats (Access Control)

First-party caveats. Caveats can only restrict, never expand.

| Caveat | Purpose | Example |
|--------|---------|---------|
| `merchant_id` | Tenant scoping | `merchant_id = 940759eb-...` |
| `tier` | Feature gating | `tier = free` |
| `expires_at` | Token lifetime | `expires_at = 2026-05-15T00:00:00Z` |
| `endpoints` | Route restriction | `endpoints = /api/*,/owl/*` |

Macaroons are signed (HMAC) but not encrypted. Anyone holding the token can read caveats. Accepted risk for Phase 0/1.

---

## Treasury Wallet Architecture

```
Strike Hot Wallet (operating)
  +-- Receives: merchant top-up payments (Lightning)
  +-- Not yet active (needs Strike API credentials)

Merchant Wallets (app.merchant_wallets)
  +-- Prepaid credit balance in sats
  +-- Funded by: treasury grants or self-service top-up
  +-- Debited by: gas meter per operation

Emergency Reserve
  +-- Configurable floor: GOOSE_EMERGENCY_RESERVE_USD (default $500)
  +-- TreasuryService logs warning if total funding exceeds 10M sats
```

---

## Interconnections

| Domain | Relationship |
|--------|-------------|
| **Identity (GRO-267)** | `merchant_id` FK on all Goose tables. Onboarding provisions wallet at OAuth. |
| **Vault** | `vault.recall` gas operation (10 sats). Endpoint gating deferred. |
| **Owl** | `owl.query.basic` (25), `owl.query.deep` (250), `owl.health_check` (500). Endpoint gating deferred. |
| **Chirp** | `chirp.alert.fired` (5 sats), `chirp.gold_list.fired` (0 sats — free). Alert delivery is free; analysis is paid. |
| **Fox** | `fox.case.created` (100), `fox.evidence.attached` (50). |
| **TSP** | `tsp.transaction.ingested` (1), `tsp.transaction.batch` (10). |
| **Receipt/TSP** | `receipt.proof` (50 sats). L402 gating deferred to Sprint 7+. |
| **RaaS** | RaaS namespace maps to merchant_id. Lapsed wallet doesn't delete namespace — gated endpoints return 402. |

---

## Operations

### Startup Sequence

1. Validate `GOOSE_MACAROON_ROOT_KEY` is set (MacaroonService raises ValueError if empty)
2. Register `goose_api` blueprint on `/goose` prefix
3. Gas schedule seeded on first boot (idempotent)
4. Strike client initialized (degrades gracefully if no API key)

### Health Check

`GET /goose/health` returns `{status: "healthy", service: "goose", strike_configured: bool}`

### Failure Modes

| Failure | Impact | Behavior |
|---------|--------|----------|
| Strike API down / not configured | Cannot create invoices or top up | Top-up returns error; existing wallets and macaroons continue to work |
| Macaroon root key missing | Cannot mint or verify tokens | MacaroonService refuses to initialize (ValueError) |
| Database unavailable | Cannot record transactions | 500 error; no silent failures |
| Wallet depleted | Merchant can't use gated endpoints | Gas meter returns `insufficient=True`; `@l402_required` returns 402 |
| Expired macaroon | Token rejected | `@l402_required` returns 402 |
| Invalid macaroon signature | Tampered or wrong root key | Verify returns `valid=False` |

### Configuration

| Variable | Purpose | Default |
|----------|---------|---------|
| `STRIKE_API_KEY` | Strike API authentication | `""` (empty) |
| `STRIKE_API_URL` | Strike API base URL | `https://api.strike.me/v1` |
| `GOOSE_MACAROON_ROOT_KEY` | Root key for macaroon crypto | `""` (**must be set**) |
| `GOOSE_WEBHOOK_SECRET` | HMAC secret for Strike webhooks | `""` (empty) |
| `GOOSE_INITIAL_FUNDING_SATS` | Initial onboarding credit | `100000` |
| `GOOSE_EMERGENCY_RESERVE_USD` | Treasury reserve floor | `500` |

---

## Deployment

Goose runs inside the Canary Flask container — no separate service. Blueprint registered on `/goose` prefix.

### AWS Target

| Component | AWS Service | Notes |
|-----------|------------|-------|
| Application | ECS/Fargate (Canary task) | Blueprint within Canary container |
| Database | RDS PostgreSQL 17 | 5 tables in `app` schema |
| Secrets | AWS Secrets Manager | `STRIKE_API_KEY`, `GOOSE_MACAROON_ROOT_KEY`, `GOOSE_WEBHOOK_SECRET` |
| Cache | ElastiCache (Valkey) | Session + rate limiting |

### CI/CD

- `pymacaroons>=0.13.0` in requirements
- Migration `goose_a00001` is idempotent (IF NOT EXISTS)
- Strike webhook URL registered post-deploy: `https://<domain>/goose/webhook/strike`

---

## Code Review Findings

### Resolved (Phase 0)

| # | Finding | Resolution |
|---|---------|------------|
| C1 | TOCTOU on wallet mutations | FOR UPDATE row locking on credit/debit |
| C2 | Empty macaroon root key accepted | ValueError on empty key in MacaroonService.__init__ |
| C3 | INSERT-ONLY not enforced | SQLAlchemy event listeners + CHECK constraint |
| P0-1 | No implementation | 5 models, 8 services, 11 routes, 58 tests |
| P0-2 | No database tables | Migration `goose_a00001` |
| P0-3 | No secrets management | Config vars defined, AWS Secrets Manager for prod |
| P0-5 | No webhook HMAC validation | StrikeClient.verify_webhook with timing-safe compare |
| P0-6 | Sensitive fields plaintext | bolt11, payment_hash, preimage encrypted via AES-256-GCM |
| P1-2 | No rate limiting | 10/min on topup, 100/min on webhook |
| P1-5 | No webhook idempotency | strike_invoice_id dedup check, skip if already paid |
| P2-5 | No macaroon revocation | Revocation via hash lookup + admin endpoint |

### Open

| # | Priority | Finding | Notes |
|---|----------|---------|-------|
| P0-4 | P0 | Macaroon root key rotation undefined | Rotation invalidates all tokens. Need dual-key verification + batch re-mint strategy. |
| P1-1 | P1 | No structured audit logging | wallet_transactions provides financial audit, but no structured log events for macaroon mint/reject, webhook processing. |
| P1-3 | P1 | No data retention policy | INSERT-ONLY tables grow indefinitely. Need 7-year retention + anonymization plan. |
| P1-4 | P1 | Macaroon caveats readable by token holder | Accepted risk for Phase 0/1. Consider encrypted payloads for Phase 2+. |
| P1-6 | P1 | Error response leak prevention | Not yet audited — payment error responses may expose internal details. |
| P2-1 | P2 | No key rotation runbook | Strike API key, webhook secret, macaroon root key — no documented procedures. |
| P2-2 | P2 | No monitoring dashboards | No metrics for invoice volume, gas charges, treasury balance. |
| P2-3 | P2 | No cold storage automation | Manual treasury management only. |
| P2-4 | P2 | receipt_tsp.py L402 gating deferred | Serves event verification proofs without payment (Sprint 7+). |
| L402-1 | **P1** | **No endpoint uses `@l402_required` (hard gate)** | 9 routes use `@gas_metered` (soft gate). L402 hard gating deferred to Phase 1 (Strike credentials). |
| L402-2 | **P1** | **402 response missing Lightning invoice** | Returns JSON `{error, reason, cost_sats}` — not `WWW-Authenticate: L402` header with invoice. Blocked by Strike credentials. |
| L402-3 | **P1** | **No macaroon renewal flow** | Token expires, no self-service re-mint. Admin revoke exists but no re-issue. |
| L402-4 | **P2** | **Cross-SDD references stale** | `external-identities.md` references `goose_payments` (doesn't exist). `platform-overview.md` lists Goose as Phase 2. |

---

## Phase Roadmap

| Phase | What | Status |
|-------|------|--------|
| Phase 0 | Credit system, gas meter, L402 middleware, macaroon lifecycle, Strike client | **Complete** (GRO-117) |
| Phase 0.5 | Gas metering on 9 intelligence routes (Owl, Fox, receipt) via `@gas_metered` soft gate | **Complete** |
| Phase 1 | Strike API credentials, live Lightning invoices, production L402 responses | Planned |
| Phase 2 | MCP per-call micropayments, agent-to-agent commerce | Planned |
| Phase 3 | BTCPay Server self-hosted (remove Strike dependency) | Future |
| Phase 4 | Treasury automation — threshold-based cold storage sweeps | Future |
| Phase 5 | LNURL-Auth — passwordless merchant login via Lightning wallet | Future |

---

## Production Readiness Checklist

- [x] Models created with UUID PKs, `Mapped[]` syntax, `created_at`/`updated_at`
- [x] INSERT-ONLY enforcement on wallet_transactions (event listeners + CHECK)
- [x] FOR UPDATE concurrency control on wallet mutations
- [x] PII encrypted at rest — bolt11, payment_hash, preimage (AES-256-GCM)
- [x] Webhook HMAC verification (timing-safe)
- [x] Webhook idempotency (strike_invoice_id dedup)
- [x] Rate limiting on public endpoints (topup: 10/min, webhook: 100/min)
- [x] Macaroon revocation mechanism (hash lookup + admin endpoint)
- [x] Health check endpoint (`/goose/health`)
- [x] Migration idempotent (IF NOT EXISTS)
- [x] 58 tests passing (models, services, middleware, E2E)
- [ ] At least one endpoint decorated with `@l402_required` (L402-1)
- [ ] 402 response includes Lightning invoice per L402 spec (L402-2)
- [ ] Macaroon renewal flow (L402-3)
- [ ] Secrets in AWS Secrets Manager (P0-4, production deploy)
- [ ] Root key rotation procedure documented (P0-4)
- [ ] Structured audit logging (P1-1)
- [ ] Data retention policy (P1-3)
- [ ] Error response audit (P1-6)
- [ ] Cross-SDD references updated (L402-4)
