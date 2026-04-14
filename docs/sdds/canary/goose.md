# Goose — Treasury & Payment Layer

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]
**Service Type:** App Service (Canary)
**Implementation Status:** Pre-implementation (design only, zero source code exists)

---

## Purpose

The Goose is Canary's monetization and treasury layer. It gates intelligence endpoints with L402 Lightning payments, converts USD subscriptions to Bitcoin via the Strike API, and pools sats into the GrowDirect treasury. GrowDirect operates on a Bitcoin standard — USD is the interface, BTC is the unit of account.

Every intelligence artifact Canary produces has a price. The Owl's weekly health check, the Vault's accumulated memories, the drill path's transaction data — all gated by L402 macaroon tokens. Merchants pay in USD (they don't need to know it's Lightning underneath). Agents pay in sats directly. The Goose collects, converts, and stacks.

---

## Dependencies

| Dependency | Type | Required For |
|------------|------|-------------|
| PostgreSQL 17 (`canary` DB, `app` schema) | Infrastructure | `goose_payments`, `goose_treasury_moves` tables |
| Valkey 8 (DB 0) | Infrastructure | Macaroon nonce cache, rate limiting state |
| Strike API | External | USD-to-BTC conversion, Lightning invoice creation, balance queries |
| `canary/utils/crypto.py` | Internal | AES-256-GCM encryption for macaroon root keys |
| Identity domain (GRO-267) | Internal | `merchant_id` for macaroon tenant scoping |
| `pymacaroons` or equivalent | Package (not yet installed) | Macaroon minting, verification, caveat extraction |

---

## Data Flow & PII Map

### What Enters

| Source | Data | Format |
|--------|------|--------|
| Identity domain (OAuth callback) | `merchant_id` | UUID from `merchants` table |
| Strike webhook (`invoice.updated`) | Payment confirmation, `payment_hash` | JSON webhook payload |
| Client HTTP request | `Authorization: L402 <macaroon>:<preimage>` or `l402_token` cookie | Header / cookie |
| Admin/agent | Manual macaroon mint request | MCP tool call |

### What's Stored

| Table | Field | PII Classification | Encryption Status |
|-------|-------|-------------------|-------------------|
| `goose_payments` | `merchant_id` | **internal** — FK to merchants, tenant identifier | Plaintext (FK reference) |
| `goose_payments` | `strike_invoice_id` | **sensitive** — links to external payment record | **PLAINTEXT** (no encryption) |
| `goose_payments` | `amount_usd` | **internal** — billing amount | Plaintext |
| `goose_payments` | `amount_sats` | **internal** — BTC denomination | Plaintext |
| `goose_payments` | `conversion_rate` | **internal** — USD/BTC rate at time of payment | Plaintext |
| `goose_payments` | `payment_hash` | **sensitive** — Lightning payment proof, cryptographic preimage hash | **PLAINTEXT** (no encryption) |
| `goose_payments` | `macaroon_hash` | **sensitive** — hash of the access token | **PLAINTEXT** (no encryption) |
| `goose_payments` | `tier` | **internal** — subscription level | Plaintext |
| `goose_payments` | `expires_at` | **internal** — token expiry window | Plaintext |
| `goose_payments` | `state` | **internal** — unpaid/paid/expired | Plaintext |
| `goose_treasury_moves` | `amount_sats` | **internal** — transfer amount | Plaintext |
| `goose_treasury_moves` | `txid` | **sensitive** — Bitcoin on-chain transaction ID, links to cold storage wallet | **PLAINTEXT** (no encryption) |
| `goose_treasury_moves` | `destination` | **restricted** — identifies cold storage wallet endpoint | **PLAINTEXT** (no encryption) |

### Macaroon Caveats (In-Token PII)

Macaroons carry embedded identity and access control data. They are cryptographically signed but not encrypted — anyone holding the token can read the caveats.

| Caveat | PII Classification | Notes |
|--------|-------------------|-------|
| `merchant_id` | **internal** | Tenant identifier, UUID |
| `tier` | **internal** | Feature gating level |
| `expires_at` | **internal** | Subscription window |
| `endpoints` | **internal** | Route restriction list |
| `max_requests` | **internal** | Usage meter |
| `max_rows` | **internal** | Data streaming cap (GRO-307) |

### What Exits

| Destination | Data | Format |
|-------------|------|--------|
| Client browser | `l402_token` HttpOnly cookie | Signed macaroon |
| Client/agent | `402 Payment Required` + Lightning invoice | HTTP response + `WWW-Authenticate` header |
| Strike API | Invoice creation requests, balance queries | HTTPS API calls |
| Cold storage (Trezor/multisig) | Bitcoin withdrawal transactions | On-chain BTC |
| `app.goose_payments` | INSERT-ONLY payment records | SQLAlchemy writes |

---

## API Contract

### Blueprint: `goose_api` (planned, not yet created)

| Route | Method | Auth | Purpose |
|-------|--------|------|---------|
| `/goose/subscribe` | POST | Session (logged-in merchant) | Create Strike invoice for subscription tier |
| `/goose/status/<invoice_id>` | GET | Session | Check payment status |
| `/goose/webhook/strike` | POST | Strike HMAC signature | Handle `invoice.updated` events, mint macaroon |
| `/goose/qr/<invoice_id>` | GET | Public | QR code page for Lightning invoice payment |

### L402 Middleware: `@l402_required` (planned decorator)

Any endpoint decorated with `@l402_required` will:
1. Check for `Authorization: L402` header or `l402_token` cookie
2. Verify macaroon signature and caveats (merchant_id, tier, expiry, endpoints)
3. Return `402 Payment Required` with Lightning invoice if token is missing/invalid/expired
4. Pass through if token is valid

### MCP Tools (canary-goose server, planned)

| Tool | Category | Auth Required | PII Access | Description |
|------|----------|:---:|:---:|-------------|
| `goose_create_invoice` | billing | Admin | merchant_id | Create Strike invoice for subscription |
| `goose_check_payment` | billing | Admin | payment_hash, strike_invoice_id | Check payment status by invoice ID |
| `goose_verify_macaroon` | auth | Admin | merchant_id (from caveats) | Verify and decode an L402 macaroon |
| `goose_treasury_balance` | treasury | Admin | amount_sats, wallet addresses | Current Strike balance + cold storage total |
| `goose_mint_token` | auth | Admin | merchant_id, tier | Manually mint a macaroon (admin/testing) |

---

## The Bitcoin Standard

GrowDirect's treasury operates in BTC. USD is the interface, not the unit of account.

```
USD in (merchant subscription)
  -> Strike converts to sats at market rate
  -> 1 sat mints the L402 macaroon (access token)
  -> remainder sits in Strike hot wallet (operating balance)
  -> weekly batch: Strike -> cold storage (Trezor/multisig)
  -> cold storage IS the treasury
```

Key design decisions:
- Revenue denominated in an appreciating asset
- No bank dependency for international merchants (8 Square countries)
- Lightning settlement is instant and final — no chargebacks, no payment disputes
- Agent-to-agent micropayments don't work with USD rails
- The payment record IS the access control token (macaroon)

---

## L402 Protocol

HTTP 402 Payment Required — the status code reserved since 1997, realized by Lightning.

```
Client -> GET /vault/summary
Server -> 402 Payment Required
         WWW-Authenticate: L402 macaroon="...", invoice="lnbc..."

Client pays the Lightning invoice (Cash App, Strike, any LN wallet)

Client -> GET /vault/summary
         Authorization: L402 <macaroon>:<preimage>
Server -> 200 OK (content served)
```

For web/PWA access, the macaroon is stored in an HttpOnly cookie after first payment. For agent/MCP access, the macaroon is passed in the Authorization header.

### Macaroon Caveats (Access Control)

Macaroons replace ACLs, API keys, and OAuth scopes with a single cryptographic token.

| Caveat | Purpose | Example |
|--------|---------|---------|
| `merchant_id` | Tenant scoping | `merchant_id = 940759eb-...` |
| `tier` | Feature gating | `tier = standard` or `tier = premium` |
| `expires_at` | Subscription window | `expires_at = 2026-04-22T00:00:00Z` |
| `endpoints` | Route restriction | `endpoints = /api/*,/owl/*,/vault/*` |
| `max_requests` | Usage metering | `max_requests = 10000` |
| `max_rows` | Data streaming cap | `max_rows = 100000` (GRO-307) |

Caveats can only restrict, never expand. A downstream proxy can add caveats to narrow access without knowing the root key — this is how agent delegation works.

### Gated Endpoints

| Endpoint | Gate | Pricing Model |
|----------|------|---------------|
| `/vault/summary` | L402 subscription | Monthly — included in tier |
| `/health-check` | L402 subscription | Monthly — included in tier |
| `/owl/search` (MCP) | L402 per-call | Per query — sat micropayment |
| `/vault/recall` (MCP) | L402 per-call | Per recall — sat micropayment |
| `/api/ej/<txn_uuid>` | L402 per-call | Per receipt — sat micropayment |
| Streaming endpoints (GRO-307) | L402 metered | Per-row or per-KB — caveat-based |

---

## Treasury Wallet Architecture

```
Strike Hot Wallet (operating)
  +-- Receives: all subscription + micropayment sats
  +-- Holds: 1-2 weeks operating balance
  +-- Withdraws: weekly batch to cold storage

Cold Storage (treasury)
  +-- Trezor hardware wallet (primary)
  +-- 2-of-3 multisig (Jeffe + ALX + escrow)
  +-- Holds: long-term BTC treasury

Emergency Reserve
  +-- Strike balance floor: always keep $500 equivalent
      for refund processing and operational costs
```

Self-custodied. GrowDirect holds its own keys. Strike is a payment processor, not a custodian.

---

## Data Model (app schema)

| Table | Purpose | Key Columns | Mutability |
|-------|---------|-------------|------------|
| `goose_payments` | Tracks every payment event | `id` (UUID PK), `merchant_id` (FK), `strike_invoice_id`, `amount_usd`, `amount_sats`, `conversion_rate`, `state` (unpaid/paid/expired), `payment_hash`, `macaroon_hash`, `tier`, `expires_at`, `created_at` | **INSERT-ONLY** |
| `goose_treasury_moves` | Tracks sats movement to cold storage | `id` (UUID PK), `amount_sats`, `source` (strike), `destination` (cold_storage), `txid` (Bitcoin txid), `status`, `created_at` | **INSERT-ONLY** |

Payment records are immutable. State transitions create new records, never UPDATE existing ones. This is the financial audit trail.

---

## Interconnections

| Domain | Relationship |
|--------|-------------|
| **Identity (GRO-267)** | Merchant identity -> macaroon `merchant_id` caveat. External identities are POS-agnostic; Goose is payment-agnostic |
| **Vault (GRO-305)** | Vault summary is the first gated endpoint. The weekly intelligence report is the product the merchant pays for |
| **Owl** | Owl search and health check are gated. Per-query micropayments for MCP consumers |
| **MCP Memory Bus (GRO-172)** | Every MCP endpoint is monetized by the Goose. The memory bus is the distribution channel; the Goose is the toll booth |
| **Streaming (GRO-307)** | Large data streams are metered via macaroon `max_rows` caveat |
| **RaaS** | The RaaS namespace (`raas:{merchant_id}`) IS the billing identity. Macaroon `merchant_id` caveat maps to the RaaS namespace. When a subscription lapses, the namespace stays but gated endpoints return 402. Re-subscribe = re-mint macaroon = instant access restoration |
| **Chirp** | Alert delivery is free (the hook). Analysis and context is the paid product |
| **Receipt/TSP** | `receipt_tsp.py` is designed for L402 gating (Sprint 7+, per-receipt micropayment). Currently ungated pending Strike API approval |

---

## Operations

### Startup Sequence

No Goose-specific startup exists yet. When implemented:

1. Validate `STRIKE_API_KEY` is configured (fail-fast if missing)
2. Validate `GOOSE_MACAROON_ROOT_KEY` is configured (fail-fast if missing)
3. Register `goose_api` blueprint on `/goose` prefix
4. Initialize Strike client with API key
5. Verify Strike API connectivity (GET account info)
6. Register `@l402_required` middleware in Flask app

### Health Checks

| Check | Method | Expected |
|-------|--------|----------|
| Goose service alive | `GET /goose/health` | `200 {"status": "healthy"}` |
| Strike API reachable | Strike API GET call | 200 response within 5s |
| Macaroon root key loaded | Startup validation | Key present in config |
| Database writable | INSERT test row to `goose_payments` | Row created |

### Failure Modes

| Failure | Impact | Behavior |
|---------|--------|----------|
| Strike API down | Cannot create invoices, cannot check payment status | Return 503 on subscription endpoints; existing macaroons continue to work (offline verification) |
| Macaroon root key missing | Cannot mint or verify any tokens | App refuses to start (fail-fast) |
| Database unavailable | Cannot record payments | Return 503; do NOT mint macaroons without recording the payment first |
| Expired macaroon presented | Client loses access | Return 402 with new invoice; client re-pays to get fresh token |
| Invalid macaroon signature | Tampered or wrong root key | Return 401 Unauthorized; log the attempt |
| Strike webhook fails | Payment confirmed but macaroon not minted | Retry via webhook redelivery; payment recorded but access delayed |

### Monitoring

| Metric | Alert Threshold | Notes |
|--------|----------------|-------|
| `goose.invoices.created` | None (informational) | Track subscription volume |
| `goose.invoices.paid` | < 1 per day after launch | Indicates payment flow broken |
| `goose.macaroons.minted` | Should track with invoices.paid | Divergence = mint failure |
| `goose.macaroons.rejected` | > 10/hour | Potential token stuffing attack |
| `goose.strike.api_errors` | > 5 in 10 minutes | Strike API degradation |
| `goose.treasury.balance_usd` | < $500 | Emergency reserve breach |
| `goose.treasury.moves` | None (informational) | Track cold storage transfers |

### Configuration (Planned Env Vars)

| Variable | Purpose | Current Status |
|----------|---------|---------------|
| `STRIKE_API_KEY` | Strike API authentication | **Not configured** |
| `STRIKE_API_URL` | Strike API base URL (sandbox vs production) | **Not configured** |
| `GOOSE_MACAROON_ROOT_KEY` | Root key for macaroon minting/verification | **Not configured** |
| `GOOSE_WEBHOOK_SECRET` | HMAC secret for Strike webhook signature validation | **Not configured** |
| `GOOSE_SUBSCRIPTION_PRICE_USD` | Default subscription price (e.g., 29.99) | **Not configured** |
| `GOOSE_COLD_STORAGE_ADDRESS` | Bitcoin address for treasury withdrawals | **Not configured** |
| `GOOSE_EMERGENCY_RESERVE_USD` | Minimum Strike balance floor (default $500) | **Not configured** |

---

## Deployment

### Docker Service Definition

Goose runs inside the existing Canary Flask container — no separate service. It registers as a blueprint (`goose_api`) on the `/goose` prefix.

```yaml
# No separate Docker service — Goose is a Canary blueprint
# Added to canary-web via blueprint registration in canary/__init__.py
```

### AWS Target

| Component | AWS Service | Notes |
|-----------|------------|-------|
| Application | ECS/Fargate (Canary task) | Blueprint within Canary container |
| Database | RDS PostgreSQL 17 | `goose_payments`, `goose_treasury_moves` in `app` schema |
| Secrets | AWS Secrets Manager | `STRIKE_API_KEY`, `GOOSE_MACAROON_ROOT_KEY`, `GOOSE_WEBHOOK_SECRET`, `GOOSE_COLD_STORAGE_ADDRESS` |
| Cache | ElastiCache (Valkey) | Macaroon nonce cache, rate limiting |

### CI/CD Requirements

- Strike API key must be available in CI for integration tests (sandbox key)
- Macaroon root key must be generated and stored in Secrets Manager before first deploy
- Strike webhook URL must be registered after deploy (callback URL = `https://<domain>/goose/webhook/strike`)

---

## Inbound Contracts

| Source | Data | Trigger |
|--------|------|---------|
| Identity domain | `merchant_id` during OAuth callback | Goose creates initial trial macaroon |
| Any HTTP request | `Authorization: L402` header or `l402_token` cookie | Goose middleware verifies |
| Strike webhook | `invoice.updated` event | Goose mints macaroon and sets cookie |

## Outbound Contracts

| Destination | Data | Trigger |
|-------------|------|---------|
| Client browser | `l402_token` HttpOnly cookie | Payment confirmation |
| Client/agent | `402 Payment Required` + Lightning invoice | Unauthenticated request to gated endpoint |
| `app.goose_payments` | INSERT-ONLY payment record | Every payment event |
| Strike API | Invoice creation, quote generation, balance queries | Subscription flow, treasury management |

---

## Phase Roadmap

| Phase | What | Status |
|-------|------|--------|
| Phase 0 | Strike closed-circle test — gate one endpoint, pay from Cash App | Blueprint ready (design) |
| Phase 1 | Production L402 on all gated endpoints, subscription tiers | Planned |
| Phase 2 | MCP per-call micropayments, agent-to-agent commerce | Planned |
| Phase 3 | BTCPay Server self-hosted (remove Strike dependency) | Future |
| Phase 4 | Treasury automation — scheduled cold storage withdrawals | Future |
| Phase 5 | LNURL-Auth — passwordless merchant login via Lightning wallet | Future |

---

## Code Review Findings

### Summary

**The entire Goose service is unimplemented.** The SDD describes a complete design with blueprints, services, models, and middleware, but the codebase contains zero Goose-specific source code. No blueprint file (`goose_api.py`), no service modules (`strike_client.py`, `macaroon_service.py`, `l402_middleware.py`), no model file (`goose_payments`), no database migration, no env vars, and no tests exist. The only code reference to L402/Goose is a comment in `receipt_tsp.py` noting that L402 gating is deferred to Sprint 7+.

### P0 — Blocks Production

| # | Finding | Description | Recommended Fix |
|---|---------|-------------|-----------------|
| P0-1 | **No implementation exists** | The SDD describes `canary/blueprints/goose_api.py`, `canary/services/goose/strike_client.py`, `canary/services/goose/macaroon_service.py`, `canary/services/goose/l402_middleware.py`, and `canary/services/goose/models.py` — none of these files exist in the codebase. Zero lines of Goose code have been written. | Implement Phase 0 (gate one endpoint with Strike sandbox). Create the service directory, models, Strike client, macaroon service, L402 middleware, and blueprint. Follow the Microservice Delivery Pattern from Canary CLAUDE.md. |
| P0-2 | **No database tables** | `goose_payments` and `goose_treasury_moves` tables are designed but no Alembic migration exists. | Create Alembic migration for both tables in `app` schema using `Mapped[]` syntax, UUID PKs, INSERT-ONLY constraint enforcement. |
| P0-3 | **No secrets management for payment keys** | `STRIKE_API_KEY`, `GOOSE_MACAROON_ROOT_KEY`, `GOOSE_WEBHOOK_SECRET` are not in `.env`, not in AWS Secrets Manager, not referenced anywhere in config. These are high-value cryptographic secrets controlling real money and access tokens. | Add to `.env.example` with placeholder values. Implement AWS Secrets Manager retrieval for production. Macaroon root key compromise = full token forgery. |
| P0-4 | **Macaroon root key storage undefined** | The macaroon root key is the most sensitive secret in the system — it can forge any access token for any merchant. No storage, rotation, or access control plan exists. | Store in AWS Secrets Manager with restricted IAM policy. Document rotation procedure. Root key rotation invalidates all outstanding macaroons — requires re-mint strategy. |
| P0-5 | **No Strike webhook signature validation** | The SDD specifies a Strike webhook handler but no HMAC signature validation exists (because no code exists). Without webhook authentication, an attacker can forge payment confirmations and mint unauthorized macaroons. | Implement HMAC-SHA256 signature verification on `/goose/webhook/strike` using `GOOSE_WEBHOOK_SECRET`. Reject unsigned or mis-signed payloads. |
| P0-6 | **Payment-sensitive fields stored plaintext** | The data model stores `strike_invoice_id`, `payment_hash`, `macaroon_hash`, `txid`, and `destination` (cold storage address) as plaintext strings. `payment_hash` is a cryptographic proof of payment. `txid` links to on-chain Bitcoin transactions. `destination` reveals the cold storage wallet address. | Encrypt `strike_invoice_id`, `payment_hash`, `txid`, and `destination` at rest using AES-256-GCM via `canary/utils/crypto.py`. `macaroon_hash` can remain plaintext (it's a hash, not the token itself). |

### P1 — Before GA

| # | Finding | Description | Recommended Fix |
|---|---------|-------------|-----------------|
| P1-1 | **No audit logging for payment operations** | No audit trail for invoice creation, payment confirmation, macaroon minting, treasury moves, or macaroon verification failures. Financial operations require immutable audit logs for compliance. | Add structured audit log entries for all Goose operations: invoice_created, payment_confirmed, macaroon_minted, macaroon_rejected, treasury_move_initiated, treasury_move_confirmed. |
| P1-2 | **No rate limiting on webhook or payment endpoints** | `/goose/webhook/strike` and `/goose/subscribe` have no rate limiting. Webhook endpoint is a DDoS target. Subscribe endpoint could be used for invoice spam. | Flask-Limiter on `/goose/webhook/strike` (100/minute), `/goose/subscribe` (10/minute per merchant). |
| P1-3 | **No data retention policy for payment records** | `goose_payments` is INSERT-ONLY with no retention policy. Financial records accumulate indefinitely. Some jurisdictions require retention (7 years for tax), others require deletion (GDPR). | Define retention policy: financial records retained 7 years (tax compliance), then anonymized (merchant_id removed, amounts aggregated). Treasury moves retained permanently (on-chain records are permanent anyway). |
| P1-4 | **Macaroon caveats readable by token holder** | Macaroons are signed but not encrypted. Anyone holding the token can read `merchant_id`, `tier`, `endpoints`, etc. While these are classified as "internal" not "sensitive," token theft exposes tenant identity and access scope. | Document this as an accepted risk for Phase 1. For Phase 2+, consider encrypting the macaroon payload (third-party caveats with an encryption service) or using opaque token IDs that resolve server-side. |
| P1-5 | **No idempotency on Strike webhook handler** | If Strike redelivers a webhook (network retry), a naive handler would mint duplicate macaroons or create duplicate payment records. | Use `strike_invoice_id` as idempotency key. Check `goose_payments` for existing record before INSERT. Return 200 OK on duplicate webhook to acknowledge receipt without re-processing. |
| P1-6 | **No error responses leak prevention** | No implementation exists to validate, but the design should mandate that error responses on payment endpoints never leak internal details (Strike API errors, database errors, key configuration issues). | All Goose error responses must return generic messages. Log full errors server-side. Never expose Strike API responses to clients. |

### P2 — Post-Launch

| # | Finding | Description | Recommended Fix |
|---|---------|-------------|-----------------|
| P2-1 | **No key rotation procedure** | Macaroon root key rotation invalidates all outstanding tokens. No documented procedure for rotating Strike API key, webhook secret, or macaroon root key. | Document rotation runbook: (1) generate new root key, (2) deploy with dual-key verification (old + new), (3) re-mint all active macaroons in batch, (4) remove old key after TTL. |
| P2-2 | **No monitoring dashboards** | No Grafana/CloudWatch dashboards for payment volume, conversion rates, treasury balance, macaroon mint/reject rates. | Build treasury dashboard: invoice volume, payment success rate, BTC balance, cold storage transfer history, macaroon rejection rate. |
| P2-3 | **No cold storage automation** | Weekly batch transfers to cold storage are manual. No automated threshold-based sweeps. | Phase 4 automation: when Strike balance exceeds $X, auto-initiate transfer to cold storage address. Requires 2-of-3 multisig approval flow. |
| P2-4 | **`receipt_tsp.py` L402 gating deferred** | `receipt_tsp.py` has comments noting L402 gating is deferred to Sprint 7+ pending Strike API spend approval. This endpoint serves event verification proofs without payment. | Implement L402 gating on receipt endpoint once Goose Phase 0 is complete. Per-receipt micropayment model. |
| P2-5 | **No macaroon revocation mechanism** | If a merchant's macaroon is compromised, there is no way to revoke it before expiry. | Implement revocation list in Valkey (SET of revoked macaroon hashes). Check on every `@l402_required` verification. TTL matches max macaroon lifetime. |

---

## Production Readiness Checklist

- [ ] PII encrypted at rest — `strike_invoice_id`, `payment_hash`, `txid`, `destination` need AES-256-GCM (P0-6)
- [ ] Secrets in AWS Secrets Manager — `STRIKE_API_KEY`, `GOOSE_MACAROON_ROOT_KEY`, `GOOSE_WEBHOOK_SECRET`, `GOOSE_COLD_STORAGE_ADDRESS` (P0-3, P0-4)
- [ ] Health check endpoint responds — `/goose/health` returning service + Strike API status (not yet implemented)
- [ ] Audit logging for sensitive operations — invoice creation, payment confirmation, macaroon mint/reject, treasury moves (P1-1)
- [ ] Data retention policy implemented — 7-year financial record retention, then anonymization (P1-3)
- [ ] Rate limiting on public endpoints — webhook and subscribe endpoints (P1-2)
- [ ] Error responses don't leak internals — generic error messages on all payment endpoints (P1-6)
- [ ] Webhook signature validation — HMAC-SHA256 on Strike webhook payloads (P0-5)
- [ ] Idempotency on webhook handler — `strike_invoice_id` dedup check (P1-5)
- [ ] Macaroon root key rotation procedure documented (P2-1)
- [ ] Database migration created and tested — `goose_payments`, `goose_treasury_moves` (P0-2)
- [ ] Blueprint created and registered — `goose_api.py` on `/goose` prefix (P0-1)
- [ ] L402 middleware implemented and tested — `@l402_required` decorator (P0-1)
- [ ] Strike client with error handling — circuit breaker, retry, timeout (P0-1)
- [ ] Macaroon service with caveat validation — mint, verify, extract (P0-1)
- [ ] Integration tests proving end-to-end payment flow — invoice -> payment -> macaroon -> gated access (P0-1)
