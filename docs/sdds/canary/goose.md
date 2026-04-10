# Goose

## Overview

The Goose is Canary's monetization and treasury layer. It gates intelligence endpoints with L402 Lightning payments, converts USD subscriptions to Bitcoin, and pools sats into the GrowDirect treasury. GrowDirect operates on a Bitcoin standard — USD is the interface, BTC is the unit of account.

Every intelligence artifact Canary produces has a price. The Owl's weekly health check, the Vault's accumulated memories, the drill path's transaction data — all gated by L402 macaroon tokens. Merchants pay in USD (they don't need to know it's Lightning underneath). Agents pay in sats directly. The Goose collects, converts, and stacks.

**Blueprints:**

| Blueprint | Prefix | Purpose |
|---|---|---|
| `goose_api` (`canary/blueprints/goose_api.py`) | `/goose` | Subscription, webhook, payment status, QR page |

**Services:**

| Module | Purpose |
|---|---|
| `canary/services/goose/strike_client.py` | Strike API wrapper — invoice creation, quote generation, status checks |
| `canary/services/goose/macaroon_service.py` | L402 macaroon minting, verification, caveat extraction |
| `canary/services/goose/l402_middleware.py` | Flask decorator — gate any endpoint with `@l402_required` |
| `canary/services/goose/models.py` | GoosePayment model — tracks invoices, macaroons, treasury flow |

**Design principles:**

- GrowDirect operates on a Bitcoin standard. USD enters, sats stay. Conversion happens at the gate, not at withdrawal
- The merchant pays in USD — they see "$29.99/month." Strike converts to sats at market rate. The merchant never touches Bitcoin directly unless they choose to
- L402 macaroons are the subscription tokens. No separate auth system, no API keys, no OAuth dance for paid access. Pay → get a receipt with your permissions encoded in it → use it until it expires
- Macaroon caveats encode the whitelist: merchant_id, tier, expiry, endpoint scope. The receipt IS the access control
- Agent access is native. An MCP consumer pays a sat per call via Lightning. No human in the loop. Agent-to-agent commerce
- Treasury is self-custodied. GrowDirect holds its own keys. Strike is the on-ramp (USD→BTC), not the bank. Sats move to cold storage on a schedule
- INSERT-ONLY on payment records. Payments are immutable evidence of the value exchange

## The Bitcoin Standard

GrowDirect's treasury operates in BTC. This is not a feature — it's the financial architecture:

```
USD in (merchant subscription)
  → Strike converts to sats at market rate
  → 1 sat mints the L402 macaroon (access token)
  → remainder sits in Strike hot wallet (operating balance)
  → weekly batch: Strike → cold storage (Trezor/multisig)
  → cold storage IS the treasury
```

**Why BTC standard:**
- Revenue denominated in an appreciating asset
- No bank dependency for international merchants (8 Square countries)
- Lightning settlement is instant and final — no chargebacks, no payment disputes
- Agent-to-agent micropayments don't work with USD rails (minimum transaction costs)
- Ledger-native: the payment record IS the access control token

**USD conversion is a UX layer, not a financial decision.** The merchant sees dollars because that's what they think in. Under the hood, every dollar becomes sats the moment it arrives.

## L402 Protocol

HTTP 402 Payment Required — the status code that's been reserved since 1997, finally realized by Lightning.

```
Client → GET /vault/summary
Server → 402 Payment Required
         WWW-Authenticate: L402 macaroon="...", invoice="lnbc..."

Client pays the Lightning invoice (Cash App, Strike, any LN wallet)

Client → GET /vault/summary
         Authorization: L402 <macaroon>:<preimage>
Server → 200 OK (content served)
```

For web/PWA access, the macaroon is stored in an HttpOnly cookie after first payment. No re-authentication on every request.

For agent/MCP access, the macaroon is passed in the Authorization header. Agents cache and reuse until expiry.

## Macaroon Caveats (Access Control)

Macaroons replace ACLs, API keys, and OAuth scopes with a single cryptographic token:

| Caveat | Purpose | Example |
|---|---|---|
| `merchant_id` | Tenant scoping | `merchant_id = 940759eb-...` |
| `tier` | Feature gating | `tier = standard` or `tier = premium` |
| `expires_at` | Subscription window | `expires_at = 2026-04-22T00:00:00Z` |
| `endpoints` | Route restriction | `endpoints = /api/*,/owl/*,/vault/*` |
| `max_requests` | Usage metering | `max_requests = 10000` |
| `max_rows` | Data streaming cap | `max_rows = 100000` (ties to GRO-307) |

Caveats can only restrict, never expand. A downstream proxy can add caveats to narrow access without knowing the root key. This is how agent delegation works — an agent can give a sub-agent a restricted token.

## Gated Endpoints

| Endpoint | Gate | Pricing Model |
|---|---|---|
| `/vault/summary` | L402 subscription | Monthly — included in tier |
| `/health-check` | L402 subscription | Monthly — included in tier |
| `/owl/search` (MCP) | L402 per-call | Per query — sat micropayment |
| `/vault/recall` (MCP) | L402 per-call | Per recall — sat micropayment |
| `/api/ej/<txn_uuid>` | L402 per-call | Per receipt — sat micropayment |
| Streaming endpoints (GRO-307) | L402 metered | Per-row or per-KB — caveat-based |

**Subscription tiers** gate the web UI. **Per-call micropayments** gate the MCP/agent endpoints. Both use the same L402 middleware — the macaroon just has different caveats.

## Treasury Wallet Architecture

```
Strike Hot Wallet (operating)
  ├── Receives: all subscription + micropayment sats
  ├── Holds: 1-2 weeks operating balance
  └── Withdraws: weekly batch to cold storage

Cold Storage (treasury)
  ├── Trezor hardware wallet (primary)
  ├── 2-of-3 multisig (Jeffe + ALX + escrow)
  └── Holds: long-term BTC treasury

Emergency Reserve
  └── Strike balance floor: always keep $500 equivalent
      for refund processing and operational costs
```

**Self-custodied.** GrowDirect holds its own keys. Strike is a payment processor, not a custodian. Sats move to cold storage as fast as operationally practical.

## Interconnections

| Domain | Relationship |
|---|---|
| **Identity (GRO-267)** | Merchant identity → macaroon `merchant_id` caveat. External identities are POS-agnostic; Goose is payment-agnostic |
| **Vault (GRO-305)** | Vault summary is the first gated endpoint. The weekly intelligence report is the product the merchant pays for |
| **Owl** | Owl search and health check are gated. Per-query micropayments for MCP consumers |
| **MCP Memory Bus (GRO-172)** | Every MCP endpoint exposed by GRO-172 is monetized by the Goose. The memory bus is the distribution channel; the Goose is the toll booth |
| **Streaming (GRO-307)** | Large data streams are metered via macaroon `max_rows` caveat. Agent pays for bandwidth + LLM inference costs |
| **RaaS** | The RaaS namespace (`raas:{merchant_id}`) IS the billing identity. The `.jeffe` name inscribed on L1 is the permanent customer record. Macaroon `merchant_id` caveat maps to the RaaS namespace. Namespace resolution is free (the hook). Namespace-scoped intelligence is gated (the product). When a merchant's subscription lapses, their RaaS namespace stays (data is never deleted) but gated endpoints return 402. Re-subscribe = re-mint macaroon = instant access restoration. The `.jeffe` inscription provides cryptographic proof that this merchant existed and paid — immutable billing history on L1 |
| **Chirp** | Alert delivery is free (the hook). Analysis and context (Follow Up → Vault) is the paid product |

## Data Model (app schema)

| Table | Purpose | Key Columns |
|---|---|---|
| `goose_payments` | Tracks every payment event (INSERT-ONLY) | `id` (UUID PK), `merchant_id` (FK merchants.id), `strike_invoice_id`, `amount_usd`, `amount_sats`, `conversion_rate`, `state` (unpaid/paid/expired), `payment_hash`, `macaroon_hash`, `tier`, `expires_at`, `created_at` |
| `goose_treasury_moves` | Tracks sats movement from Strike → cold storage | `id` (UUID PK), `amount_sats`, `source` (strike), `destination` (cold_storage), `txid` (Bitcoin txid), `status`, `created_at` |

**INSERT-ONLY.** Payment records are immutable. State transitions create new records, never UPDATE existing ones. This is the financial audit trail.

## MCP Tools (canary-goose server)

| Tool | Category | Purpose |
|---|---|---|
| `goose_create_invoice` | billing | Create Strike invoice for subscription |
| `goose_check_payment` | billing | Check payment status by invoice ID |
| `goose_verify_macaroon` | auth | Verify and decode an L402 macaroon |
| `goose_treasury_balance` | treasury | Current Strike balance + cold storage total |
| `goose_mint_token` | auth | Manually mint a macaroon (admin/testing) |

## Inbound Contracts

- Identity domain provides `merchant_id` during OAuth callback → Goose creates initial trial macaroon
- Any HTTP request with `Authorization: L402` header or `l402_token` cookie → Goose middleware verifies
- Strike webhook `invoice.updated` → Goose mints macaroon and sets cookie

## Outbound Contracts

- Sets `l402_token` HttpOnly cookie on payment confirmation
- Returns `402 Payment Required` with Lightning invoice for unauthenticated requests
- Writes GoosePayment records to `app.goose_payments`
- Calls Strike API for invoice creation, quote generation, and balance queries

## Phase Roadmap

| Phase | What | Status |
|---|---|---|
| Phase 0 | Strike closed-circle test — gate one endpoint, pay from Cash App | Blueprint ready |
| Phase 1 | Production L402 on all gated endpoints, subscription tiers | Planned |
| Phase 2 | MCP per-call micropayments, agent-to-agent commerce | Planned |
| Phase 3 | BTCPay Server self-hosted (remove Strike dependency) | Future |
| Phase 4 | Treasury automation — scheduled cold storage withdrawals | Future |
| Phase 5 | LNURL-Auth — passwordless merchant login via Lightning wallet | Future |
