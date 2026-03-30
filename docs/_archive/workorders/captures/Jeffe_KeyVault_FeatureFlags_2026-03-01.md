---
type: decision
domain: business
status: active
created: 2026-03-01
updated: 2026-03-19
---
# Jeffe Capture: Key Vault + Feature Flags / Config Routing
**Date:** March 1, 2026
**Context:** Follow-up to B-073 (RaaS + Namespace Decisions). Jeffe raised two architectural questions about infrastructure readiness.

---

## Capture 1: Key Vault — Token Storage at Scale

**Jeffe's concern:** How do we store all the tokens we're generating? ~20 keys today, but merchant OAuth tokens multiply fast with RaaS adoption.

### Current State
- Secrets in `.env` files (B-027 flagged — no shared credential management)
- Square OAuth app credentials, OrdinalsBot API key, Strike wallet credentials, ngrok token, Cloudflare token
- No encryption-at-rest, no rotation policy, no audit trail

### Scale Problem
- Every merchant OAuth connection generates access token + refresh token pair
- 100 merchants = 200 tokens. 10,000 merchants = 20,000 tokens.
- RaaS amplifies this: Clover, Toast, Lightspeed integrators each generate API keys
- These are live payment credentials — leak = full merchant data access

### Decision: HashiCorp Vault (self-hosted)
**Approved by Jeffe (Mar 1).**

**Why Vault:**
- Open source, free tier, self-hosted (fits "local first, cloud behind a gate")
- Programmatic API for token storage/retrieval
- Automatic rotation policies
- Audit log (SOX compliance)
- Runs in Docker Compose alongside existing stack
- Transit secrets engine for encryption-as-a-service

**Phase 1 (GrowDirect Lab):** Structured `.env` with encryption-at-rest. Vault not required for single-merchant testing.
**Phase 2 gate:** Vault deployed before first external merchant connects. Non-negotiable.

**Alternatives considered:**
- AWS Secrets Manager: cloud-first, per-secret pricing, violates local-first principle
- Doppler: SaaS, developer-friendly, but merchant credentials on third-party infrastructure
- 1Password Teams: team-friendly but not programmatic enough for automated token rotation

### Routing
| Agent | Action |
|---|---|
| **Jeremy** | Add Vault to Docker Compose stack. Design token storage schema (merchant_id → {access_token, refresh_token, expires_at, last_rotated}). Wire `ElJeffeConfig` to read from Vault instead of `.env` in Phase 2. |
| **Tom** | Vault architecture decision: standalone container or sidecar? Key hierarchy design (root key → merchant keys → service keys). Rotation policy spec. |
| **Syd** | Review Vault deployment for SOX compliance. Audit trail requirements. Confirm merchant token storage satisfies Square ToS (B-049). |
| **SOX** | Vault audit log integration into compliance controls. Access logging. Key rotation verification. |

---

## Capture 2: Feature Flags / Configuration Routing

**Jeffe's concern:** Build switches into the code now so we can toggle L402, chain targets, service tiers without rewiring later. Use domain routing (eljeffe.org = free, eljeffe.io = paid).

### Decision: Three-Tier Service Model
**Approved by Jeffe (Mar 1).**

**Tier 1 — FREE (eljeffe.org)**
- No L402 micropayment gate
- No Bitcoin inscription
- SHA-256 hash receipt stored in GrowDirect Postgres only
- Proof of format, not proof of permanence
- Purpose: developer sandbox, freemium conversion funnel
- "You like the format? Now make it permanent."

**Tier 2 — STANDARD (eljeffe.io)**
- L402 micropayment gate (1 sat per verification)
- Bitcoin inscription via Ordinals
- Full .jeffe namespace resolution
- Heartbeat fee optimization
- RaaS API access
- Purpose: production merchants, POS integrators

**Tier 3 — ENTERPRISE (custom)**
- Everything in Standard
- Dedicated .jeffe namespace (pre-registered)
- Priority heartbeat windows
- Dedicated Avalanche subnet partition
- Custom inscription frequency tiers
- SLA + dedicated support
- Purpose: Walmart-scale merchants, audit firms, insurance companies

### Environment Configuration Spec

```env
# ===== SERVICE TIER =====
ELJEFFE_MODE=paid              # paid | free | sandbox
ELJEFFE_DOMAIN=eljeffe.io     # eljeffe.io (paid) | eljeffe.org (free) | localhost (dev)

# ===== CHAIN ROUTING =====
CHAIN_TARGET=bitcoin            # bitcoin | avalanche | mock
INSCRIPTION_MODE=live           # live | mock | dry-run

# ===== FEATURE GATES =====
L402_ENABLED=true               # true | false (false = free tier)
NAMESPACE_ENABLED=false         # true | false (false = Phase 1)
HEARTBEAT_ENABLED=false         # true | false (false = naive timing)
RAAS_API_ENABLED=false          # true | false (false = Canary-only)

# ===== INSCRIPTION TARGET =====
ORDINALSBOT_ENV=testnet         # testnet | mainnet
STRIKE_ENV=sandbox              # sandbox | production

# ===== VAULT =====
VAULT_ADDR=http://vault:8200   # Vault server address
VAULT_TOKEN=                    # Vault auth token (Phase 2)
```

### Architecture Notes
- **Tom's ChainAdapter pattern already supports this.** `BitcoinAdapter`, `AvalancheAdapter`, `MockAdapter` — adding a `FreeAdapter` (no L402, no inscription, hash-only receipt) is trivial.
- **`ElJeffeConfig` class** reads env vars at startup, exposes feature gates to all services.
- **`FeatureGate` middleware** checks config before hitting any gated endpoint.
- **`ChainDispatcher`** routes to correct adapter based on `CHAIN_TARGET` + `ELJEFFE_MODE`.
- **Domain routing:** nginx/Cloudflare routes `eljeffe.org/*` with `ELJEFFE_MODE=free` headers, `eljeffe.io/*` with `ELJEFFE_MODE=paid`.
- **~100 lines of Python** for Jeremy to wire into Sprint 6. Saves months of refactoring later.

### Routing
| Agent | Action |
|---|---|
| **Jeremy** | Build `ElJeffeConfig` class + `FeatureGate` middleware + `ChainDispatcher` routing. Wire into Sprint 6 pipeline. ~100 lines. This goes in NOW, not later. |
| **Tom** | Review config spec for architectural completeness. Confirm ChainAdapter interface accommodates `FreeAdapter`. Vault integration design. |
| **Worm** | DNS routing: `eljeffe.org` → free tier landing + API. `eljeffe.io` → paid tier. Cloudflare Workers for header injection if needed. |
| **Will** | Three-tier pricing page copy. Free → Standard conversion messaging. Developer sandbox onboarding flow. |
| **PhD** | Manifesto update: three-tier model as economic architecture. Free tier as adoption accelerant. |

---

## Classification
**MAXIMUM CONFIDENTIAL** — Contains infrastructure architecture and pricing strategy.
