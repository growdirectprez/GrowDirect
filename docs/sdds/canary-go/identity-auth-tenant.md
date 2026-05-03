---
spec-version: 1.0
target-implementation: Go
stack: PostgreSQL 17 + pgx + Chi HTTP + golang-jwt v5 + GCP Identity Platform
status: handoff-ready
type: service
package: cmd/identity + internal/identity
updated: 2026-05-03
license: Apache-2.0
copyright: "Copyright (c) 2026 GrowDirect LLC"
linear: GRO-763
folds: GRO-639, GRO-688, GRO-689
---

# Identity, Auth & Tenant Model — Canary Go

**Service:** `cmd/identity` (port 8086)
**Library:** `internal/identity`
**Authority:** GRO-763 Phase C; folds GRO-639 (epic), GRO-688 (per-agent scoped keys), GRO-689 (RS256 JWT validation)

The identity service is the single source of truth for every authenticated request that crosses a Canary Go service boundary. Loop 2 left it half-built — the cmd/identity binary scaffolded but the test suite gated under Tier-3 because the file structure compiled without a real auth substrate behind it. This SDD describes the rebuild.

The mission is unflashy and load-bearing: every other module's tenant-isolation guarantee depends on identity getting the boundary right. If the gateway leaks one tenant's data into another tenant's response, no amount of downstream encryption or audit infrastructure recovers from that.

---

## Three authentication paths

| Path | Used by | Mechanism | Source of `tenant_id` |
|---|---|---|---|
| **OAuth 2.0 + OIDC** | Human users (founder, merchant operators, auditors) | Browser flow → IdP → ID token → exchange for session JWT | `tenant_id` claim (signed by IdP) |
| **RS256 JWT (service-to-service)** | Canary Go services calling each other; long-lived tokens for trusted agents | Bearer token; JWKS validation against IdP issuer | `tenant_id` claim |
| **Per-agent scoped API key** | External integrators, MCP agents, dev/test clients | `X-Canary-API-Key: <plaintext>` header; hashed lookup against `app.api_keys` | Column on the key row (NULL for platform-scope) |

OAuth/OIDC is Phase 1 wired against **GCP Identity Platform** (per memory `feedback_no_hand_rolling_outside_core_ip` — federated identity is purchased, not hand-rolled). The substrate is portable to Auth0, AWS Cognito, or Dex by swapping the JWKS endpoint config; nothing GCP-specific bleeds into application code.

The legacy HMAC-SHA256 `internal/auth.SignToken`/`VerifyToken` path used by the existing `cmd/identity/sessions/validate` endpoint stays in place for the duration of the migration (see §Migration). Callers drift from it to RS256 over time.

---

## Database

### `app.api_keys` (new — Phase C.2)

```sql
CREATE TABLE app.api_keys (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid REFERENCES app.tenants(id),            -- NULL = platform-scope key
  agent_name      text NOT NULL,                              -- 'gateway' | 'sub1' | 'alx-dev' | etc.
  key_hash        text NOT NULL UNIQUE,                       -- argon2id; never plaintext
  scopes          text[] NOT NULL DEFAULT '{}',               -- 'webhook:write', 'evidence:read', etc.
  rate_limit_rpm  int NOT NULL DEFAULT 600,                   -- per-key rate limit
  status          text NOT NULL DEFAULT 'active'
                  CHECK (status IN ('active','revoked','expired')),
  expires_at      timestamptz,
  last_used_at    timestamptz,
  attributes      jsonb NOT NULL DEFAULT '{}',
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_api_keys_tenant_status ON app.api_keys(tenant_id, status);
CREATE INDEX idx_api_keys_agent ON app.api_keys(agent_name);
```

**Hashing:** [argon2id](https://datatracker.ietf.org/doc/html/rfc9106) — Go binding `golang.org/x/crypto/argon2`. Per RFC 9106 recommended parameters: `time=1, memory=64MB, threads=4, hashLen=32`. Salt is per-key (16-byte crypto/rand), stored alongside the hash in a self-describing string `argon2id$<saltB64>$<hashB64>`. Verification computes the hash of the plaintext key against the stored salt; constant-time compare.

**Key plaintext format:** 32 random bytes, base32-encoded, prefixed with `cy_` for visual identification: e.g., `cy_QH4LP3RXY...`. Plaintext is returned **once** at create-time; never stored in plaintext, never re-displayable.

**Replacement of `CANARY_MCP_API_KEY`:** the legacy static-string env var stays as a temporary fallback for cmd/sub2 and any other client that depends on it, gated behind `CANARY_MCP_API_KEY_LEGACY=true`. Defaults to false in the next release; removal is a Wave B follow-up.

### Schema location

Lands at the end of `deploy/schema/01_app_foundation.sql` (alongside other app.* tables). Seed at least one platform-scope dev key + one tenant-scope dev key in `99_seed.sql`.

---

## JWT validation (RS256)

`internal/identity/jwt.go` — public-key JWT validation against an IdP JWKS endpoint.

**Configuration:**

| Env var | Default | Purpose |
|---|---|---|
| `IDENTITY_JWKS_URL` | `https://identitytoolkit.googleapis.com/v1/projects/<project>/jwks` | JWKS source |
| `IDENTITY_JWT_ISSUER` | `https://securetoken.google.com/<project>` | Expected `iss` claim |
| `IDENTITY_JWT_AUDIENCE` | `<project>` | Expected `aud` claim |
| `IDENTITY_JWKS_CACHE_TTL_SECONDS` | `300` | JWKS key cache TTL |

**Flow:**

1. Fetch JWKS once at first use; cache by `kid`. TTL refresh per env var.
2. On `Authorization: Bearer <token>` validate:
   - parse `kid` from header
   - look up matching public key in cache; refetch JWKS if missing
   - verify signature (RS256)
   - check `iss`, `aud`, `exp`, `nbf`, `iat`
3. Extract `sub` (user id) and `tenant_id` (custom claim) — both required.
4. Inject into request context via `tenant.InjectAuthContext(ctx, claims)`.

The legacy `internal/auth.VerifyToken` (HS256, single secret) stays in place for `/sessions/validate` until the human-user OAuth flow lands. RS256 path is layered on top, not replacing.

**Reference implementation:** [github.com/golang-jwt/jwt/v5](https://github.com/golang-jwt/jwt) — already in go.mod for HS256; same library handles RS256 via `jwt.SigningMethodRS256`.

---

## API key middleware

`internal/identity/apikey.go` — chi middleware reading `X-Canary-API-Key`.

**Flow:**

1. Read `X-Canary-API-Key` header. Empty → next handler (lets routes layer multiple auth options).
2. Compute argon2id verify against `app.api_keys.key_hash`. (We can short-circuit by indexing on a non-secret prefix — the first 8 bytes of base32 — but the simple path is "fetch all active keys, verify each" which is fine until ~10⁴ keys per tenant. The lookup is keyed by `tenant_id` once the request body's tenant is known; for unauthenticated routes the only candidate set is platform-scope keys.)
3. On match: verify `status='active'`, `expires_at` is NULL or future. Update `last_used_at` (single UPDATE, no read).
4. Inject context: `tenant_id`, `agent_name`, `scopes[]`. The handler can check scopes via `identity.RequireScope(ctx, "webhook:write")`.
5. Rate limit per-key via Memorystore counter — increment-then-test against `rate_limit_rpm` × 60s rolling window. Backoff: 429 with `Retry-After` header.

**Why both JWT and API key:** human flow uses JWT (rotated quickly, revoked via session log-out). Service-to-service and external integrators use API keys (stable, scoped, rotation is explicit). Routes pick which middleware they want, or accept either via a chi.Router group.

---

## Tenant boundary enforcement

`internal/tenant/middleware.go` — already exists. Phase C extends it:

```go
type Claims struct {
    TenantID   uuid.UUID
    AgentName  string    // for API key auth
    UserID     uuid.UUID // for JWT auth (zero on API key paths)
    Scopes     []string  // API key scopes (nil on JWT paths)
    AuthMethod string    // "jwt" | "apikey" | "legacy_hmac"
}

func InjectAuthContext(ctx context.Context, c Claims) context.Context
func ClaimsFromContext(ctx context.Context) (Claims, bool)
func RequireTenant(next http.Handler) http.Handler
```

**Cross-tenant defense:** every handler that accepts a `tenant_id` in the request body MUST validate that the body's `tenant_id` matches `Claims.TenantID`. The dispatch's "build full surface" posture means we can't just trust the body — a malicious or compromised caller could substitute a different tenant id and read data they shouldn't.

A package-level helper enforces this:

```go
func tenant.AssertBodyTenantMatches(ctx context.Context, bodyTenantID uuid.UUID) error
```

Returns `ErrTenantMismatch` (which the handler maps to 403) if mismatched. The request log records the attempted-vs-claimed mismatch for security audit.

**Lint check (deferred to Wave B):** `internal/tenant/lint/main.go` — `go vet`-style tool that grep's all `pool.Query`/`pool.QueryRow` call-sites and flags any that don't include `tenant_id` in the WHERE clause. Not blocking; advisory.

---

## Endpoints (cmd/identity rebuild)

| Method | Path | Auth | Purpose |
|---|---|---|---|
| GET | `/health` | none | Liveness check; returns build info, JWKS cache hit count, DB ping |
| POST | `/sessions/validate` | none (legacy) | Existing HS256 validate — kept for migration |
| POST | `/v1/identity/keys` | admin scope | Create new API key; returns plaintext once |
| GET | `/v1/identity/keys` | admin scope | List keys for caller's tenant |
| POST | `/v1/identity/keys/{id}/revoke` | admin scope | Mark revoked |
| GET | `/v1/identity/whoami` | any auth | Return decoded JWT/API-key context for caller debugging |

**Stub endpoints kept:** `/merchants/*`, `/oauth/*`, `/sessions` (existing 501 stubs — wired for callers, real implementations land in later loops).

**Test coverage (5-10 integration tests):**

- `TestHealthEndpoint` — DB + Valkey ping; returns 200 (Tier-3 lift acceptance signal)
- `TestCreateAPIKey_AdminAuthorized` — POST returns plaintext; row in `app.api_keys` with hashed value
- `TestCreateAPIKey_NoAuth` — returns 401
- `TestListAPIKeys_TenantScoped` — only returns caller's tenant keys
- `TestRevokeAPIKey_Idempotent` — second revoke is no-op
- `TestWhoami_JWT` — returns decoded JWT context
- `TestWhoami_APIKey` — returns decoded API key context
- `TestSessionValidate_ExistingHS256Still Works` — backward-compat regression guard

DB-touching tests stay under `//go:build integration` per existing convention. Pure handler-level tests (request shape, error envelope) move to `cmd/identity/handlers_test.go` without a build tag.

---

## Cyber-liability prereq mapping

Per memory `feedback_insurance_prereq_compliance` — the cyber-liability questionnaire maps 1:1 to GRO-686 through GRO-699. This dispatch closes:

- **GRO-688** — Replace static `CANARY_MCP_API_KEY` with per-agent scoped keys → `app.api_keys` + `internal/identity/apikey.go`
- **GRO-689** — Spec production JWT validation (RS256 against IdP JWKS) → `internal/identity/jwt.go`

Both folded with closure comments referencing this dispatch's commit SHAs.

---

## Migration

The existing HS256 `internal/auth` path stays operational. Two caller cohorts move:

1. **Service-to-service callers** (cmd/sub2, cmd/gateway internal calls) — switch from `CANARY_MCP_API_KEY` env var to a real `app.api_keys` row. Each cmd binary gets its own key on first deploy. No code change at the consumer side; the gateway's middleware swap from "static-string compare" to "argon2id verify against table" is the only mechanical diff.

2. **Human users** (founder dashboard, future merchant UI) — adopt OAuth/OIDC against GCP Identity Platform when the merchant UI lands. Until then the existing magic-link / session-cookie flow on the legacy Canary Python prototype is the human path.

External merchant API consumers (CATz partners, MCP agents) get tenant-scoped API keys via `POST /v1/identity/keys`. The plaintext is shown once at create-time; rotated by creating a new key and revoking the old.

---

## Cross-references

- [`CanaryGo/internal/auth/`](../../../CanaryGo/internal/auth) — existing HS256 path (kept)
- [`CanaryGo/internal/tenant/`](../../../CanaryGo/internal/tenant) — request-context tenant carrier
- [`docs/sdds/go-handoff/identity.md`](../go-handoff/identity.md) — earlier identity spec; absorbed into this doc
- [`docs/superpowers/plans/2026-05-03-oq-resolution-pack.md`](../../superpowers/plans/2026-05-03-oq-resolution-pack.md) — §A.1 standing meta-rule §1 (open-source standards) drove OAuth + RS256 + argon2id choices
- [`Brain/wiki/cards/loop2-build-report.md`](../../../Brain/wiki/cards/loop2-build-report.md) — Tier-3 cmd/identity backlog from Loop 2
- Memory `feedback_no_hand_rolling_outside_core_ip` — drove GCP Identity Platform / Auth0 / Cognito choice over hand-rolling federated identity
- Memory `feedback_insurance_prereq_compliance` — cyber-liability prereq tracking
- RFC 9106 — argon2id parameter recommendations
- RFC 7519 — JSON Web Token spec
- RFC 7517 — JSON Web Key Set spec
