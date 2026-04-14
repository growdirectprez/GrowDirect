# Identity-Square — Square OAuth + CRDM Identity Resolution

> **Type:** External Integration (Type 4)
> **Status:** Operational — upgraded to ops contract 2026-04-13
> **Namespace:** canary
> **Code location:** `Canary/canary/utils/crypto.py`, `Canary/canary/models/app/oauth.py`, `Canary/canary/services/square_oauth.py`, `Canary/canary/blueprints/square_oauth_wired.py`, `Canary/canary/services/identity/external_id_resolver.py`, `Canary/canary/services/parsers/`
> **Linear:** GRO-53, GRO-130, GRO-159, GRO-174, GRO-237, GRO-248, GRO-267, GRO-266, GRO-288, GRO-299, GRO-386
> **Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

---

## Purpose

Identity-Square is the external integration layer that connects Square merchant accounts to Canary. It handles three concerns: (1) Square OAuth flow — consent, token exchange, encrypted storage, auto-refresh, and revocation; (2) CRDM identity resolution — POS-agnostic UUID bridging for every entity from Square; (3) Square parsers — 16 pure-function modules that normalize Square webhook payloads into Canary's internal data model.

This service contains the platform's reference implementation of AES-256-GCM encryption for secrets at rest. All other services that need field-level encryption should follow the pattern in `canary/utils/crypto.py`.

---

## Dependencies

| Dependency | Type | Required | Purpose |
|---|---|---|---|
| Square OAuth API | External API | Yes | Token issuance (`/oauth2/authorize`, `/oauth2/token`), refresh, revocation (`/oauth2/revoke`) |
| Square Merchants API | External API | Yes | Business name + currency fetch during merchant provisioning |
| `growdirect_postgres:5432` (canary DB) | Database | Yes | Token storage, merchant records, identity mappings |
| `growdirect_valkey:6379/0` | Cache/Session | Yes | Flask session, OAuth CSRF state storage (GRO-386), `canary:events` stream |
| `canary.utils.crypto` | Internal module | Yes | AES-256-GCM encrypt/decrypt |
| `canary.middleware.jwt_auth` | Internal module | Yes | JWT validation on protected routes, user provisioning |

---

## Data Flow & PII Map

### What Enters

| Source | Data | Format |
|---|---|---|
| Square OAuth callback | Authorization code, merchant ID, granted scopes | HTTP query params |
| Square `/oauth2/token` response | Access token, refresh token, expiry, scopes | JSON |
| Square Merchants API | Business name, currency | JSON |
| Square webhooks (via TSP Sub1) | Raw event payloads for 16+ entity types | JSON in Valkey stream |

### What's Stored

| Table | Field | Classification | Encryption | Notes |
|---|---|---|---|---|
| `app.square_oauth_tokens` | `access_token_encrypted` | **restricted** | AES-256-GCM | Decrypted only in `SquareOAuthService` |
| `app.square_oauth_tokens` | `refresh_token_encrypted` | **restricted** | AES-256-GCM | Nullable (non-renewable tokens) |
| `app.square_oauth_tokens` | `expires_at` | internal | none | UTC timestamp |
| `app.square_oauth_tokens` | `scopes` | internal | none | Comma-separated scope strings |
| `app.square_oauth_tokens` | `merchant_id` | internal | none | FK to `merchants.id` (Canary UUID) |
| `app.merchant_sources` | `external_merchant_id` | internal | none | Square's merchant ID string |
| `app.merchant_sources` | `metadata_json` | internal | none | Granted scopes, timestamps |
| `app.external_identities` | `external_id` | internal | none | Square entity IDs (not PII) |
| `app.external_identities` | `entity_id` | internal | none | Canary UUID |
| Flask session (Valkey) | `user_id`, `merchant_id`, `roles` | internal | none (Valkey in-memory) | Session data |
| Flask session (Valkey) | `square_oauth_state` | internal | none | CSRF token, 5-min TTL |

### What Exits

| Destination | Data | Purpose |
|---|---|---|
| Square API | Decrypted access token | Authenticated API calls (via `get_token()`) |
| Square `/oauth2/revoke` | Decrypted access token | Token revocation on disconnect |
| TSP Sub 2 | Parsed CRDM dicts | Normalized entity data for `canary_sales` |
| Owl / ALX agents | Merchant/employee/location data | Read-only MCP tools |
| Browser | Session cookie (no PII in cookie itself) | Authentication state |

### PII Classification Key

- **public:** Freely visible (business name, currency)
- **internal:** Visible to authenticated users (merchant ID, scopes, entity mappings)
- **sensitive:** Encrypted at rest, logged on access (none in this service currently)
- **restricted:** Encrypted at rest, audited on access, minimal exposure (OAuth tokens)

---

## API Contract

### OAuth Blueprint (`/oauth/*`)

Registered as `square_oauth_bp` in `canary/blueprints/square_oauth_wired.py`.

| Route | Method | Auth | Purpose |
|---|---|---|---|
| `/oauth/authorize` | GET | None | Redirect to Square consent screen |
| `/oauth/callback` | GET | None (CSRF state via Valkey + session fallback) | Exchange auth code for tokens; provision merchant + user |
| `/oauth/status` | GET | JWT required | Return connection status and token expiry |
| `/oauth/refresh` | POST | JWT + admin role | Force-refresh access token |
| `/oauth/disconnect` | POST | JWT + owner/admin role | Revoke token at Square, delete local record |
| `/oauth/sandbox` | GET | None (sandbox env only) | Dev shortcut: store env tokens directly |
| `/oauth/reset-onboarding` | GET | Session + admin role | Sandbox factory reset |
| `/oauth/merchant-reset` | POST | Session auth | Sandbox tenant-scoped reset |
| `/oauth/factory-reset` | POST | Session auth | Sandbox full factory reset |

**Callback response contract:**
- Success: HTTP 302 to `/welcome` (new user) or `/chirps` (returning user)
- CSRF mismatch: HTTP 302 to `/auth/login-page?error=oauth_csrf_mismatch`
- Square error: HTTP 302 to `/settings?error=<error>`
- Token exchange failure: HTTP 302 to `/auth/login-page?error=token_exchange_failed`

### Identity MCP Blueprint (`/identity/*`)

Registered as `identity_mcp_bp`. Exposes `canary-identity` MCP server (v0.1.0). All tools are DB-read only.

| Tool | Required Params | Returns |
|---|---|---|
| `get_merchant` | `merchant_id` | name, business_name, email, phone, created_at |
| `get_settings` | `merchant_id` | timezone, currency, language, notification_preferences |
| `list_employees` | `merchant_id` | employees[], count |
| `get_employee` | `merchant_id`, `employee_id` | id, name, email, phone, location_id, is_active, risk_score |
| `list_locations` | `merchant_id` | locations[], count |
| `get_location` | `merchant_id`, `location_id` | id, name, address, square_location_id, is_active |

### SquareOAuthService (`canary/services/square_oauth.py`)

| Method | Signature | Returns |
|---|---|---|
| `store_token` | `(merchant_id, access_token, refresh_token=None, expires_at=None)` | `None` (upserts) |
| `get_token` | `(merchant_id)` | `{"access_token": str, "expires_at": datetime, "merchant_id": str}` or `None` |
| `refresh_token_flow` | `(merchant_id)` | Same dict as `get_token`; raises `ValueError` on failure |
| `revoke_token` | `(merchant_id)` | `bool` (always deletes local row regardless of Square API result) |

### External Identity Resolver (`canary/services/identity/external_id_resolver.py`)

Pure service functions, no Flask context. All take a SQLAlchemy `Session` as first argument.

| Function | Purpose |
|---|---|
| `resolve_to_canary(session, merchant_id, source_code, entity_type, external_id)` | Square ID to Canary UUID |
| `resolve_to_external(session, merchant_id, entity_type, entity_id, source_code=None)` | Canary UUID to Square ID(s) |
| `register_external_id(session, merchant_id, entity_type, entity_id, source_code, external_id, is_primary=True)` | Upsert identity mapping (idempotent) |
| `bulk_register(session, merchant_id, source_code, mappings)` | Batch registration for initial sync |

---

## AES-256-GCM Encryption Reference

**This is the platform's reference implementation for secrets at rest.** All other services needing field-level encryption should follow this pattern.

### Implementation (`canary/utils/crypto.py`)

**Algorithm:** AES-256-GCM (Galois/Counter Mode) via `cryptography.hazmat.primitives.ciphers.aead.AESGCM`.

**Key derivation:**
1. Read `CANARY_ENCRYPTION_KEY` from environment (base64url-encoded).
2. `base64.urlsafe_b64decode()` to get raw bytes.
3. Take first 32 bytes for AES-256.
4. If the env var is empty/missing, encryption functions refuse to store plaintext in production (raises `RuntimeError`). In testing mode only, falls back to `UNENCRYPTED:` prefix.

**Encrypt flow:**
1. Generate 12-byte random nonce via `os.urandom(12)`.
2. Encrypt plaintext with `AESGCM.encrypt(nonce, plaintext, aad=None)`.
3. Pack: `nonce (12 bytes) + ciphertext + tag (16 bytes appended by GCM)`.
4. Base64-encode the packed bytes.
5. Prepend `GCM:` prefix.
6. Final stored value: `GCM:<base64(nonce + ciphertext + tag)>`.

**Decrypt flow:**
1. Check prefix: `GCM:` dispatches to GCM decryption, `UNENCRYPTED:` strips prefix and returns plaintext, anything else (e.g., `gAAAAA...`) dispatches to legacy Fernet decryption.
2. For GCM: base64-decode, split at byte 12 (nonce | ciphertext+tag), decrypt with `AESGCM.decrypt()`.
3. For Fernet legacy: use the same `CANARY_ENCRYPTION_KEY` env var as a Fernet key directly.

**Migration path:** Legacy Fernet-encrypted tokens are transparently decrypted by `decrypt_token()`. On the next `store_token()` call, the value is re-encrypted as AES-256-GCM. Merchants who have not re-authorized since GRO-248 still have Fernet-encrypted tokens; these are decrypted correctly but not proactively migrated.

**Security properties:**
- Authenticated encryption: GCM tag ensures ciphertext integrity and authenticity.
- Unique nonce per encryption: 12-byte random nonce from `os.urandom()` (96-bit, NIST-recommended size).
- No AAD (Additional Authenticated Data): `aad=None` in both encrypt and decrypt. Tokens are not bound to a specific merchant_id or context at the cryptographic level.
- Production guard: `RuntimeError` raised if no key is configured and `CANARY_ENV != testing`.

### What the Pattern Gets Right

1. **Algorithm choice:** AES-256-GCM is current best practice for authenticated encryption.
2. **Random nonce:** 12-byte nonce from `os.urandom()` per encryption call. No nonce reuse risk unless the key is used for more than ~2^32 encryptions (well beyond our volume).
3. **Production guard:** Refuses to store plaintext tokens in production — hard fail, not silent degradation.
4. **Transparent migration:** Legacy Fernet tokens are decrypted and re-encrypted on next write without manual intervention.
5. **Clean prefix scheme:** `GCM:`, `UNENCRYPTED:`, and bare (Fernet legacy) prefixes make the encryption scheme self-describing. Easy to audit column values.
6. **Minimal surface:** The crypto module is 137 lines. Two public functions (`encrypt_token`, `decrypt_token`). No key management complexity exposed to callers.

---

## Operations

### Startup Sequence

1. Flask app initializes. `SquareOAuthService.__init__()` calls `_init_crypto()` which reads `CANARY_ENCRYPTION_KEY` from environment via `_get_gcm_key()`.
2. If key is missing: logs warning, sets `_gcm_key = None`. Subsequent encrypt calls will raise `RuntimeError` in production.
3. OAuth blueprint registers routes under `/oauth/*`.
4. Identity MCP blueprint registers read-only tools under `/identity/*`.
5. Health check: `GET /health` (liveness), `GET /readiness` (DB + Valkey connectivity).

### Health Checks

| Endpoint | Type | What it Checks |
|---|---|---|
| `GET /health` | Liveness | Flask process is running |
| `GET /readiness` | Readiness | PostgreSQL `SELECT 1`, Valkey `PING` |

Neither health check validates that `CANARY_ENCRYPTION_KEY` is configured. A container can pass readiness but fail on first token operation.

### Failure Modes

| Failure | Impact | Detection | Recovery |
|---|---|---|---|
| `CANARY_ENCRYPTION_KEY` missing | All token operations fail with `RuntimeError` | First `store_token()` or token refresh call | Set env var, restart container |
| Square API down | New OAuth connections fail; token refresh fails | HTTP timeout (30s) on `/oauth2/token` | Existing tokens continue working until expiry; merchant re-authorizes when Square recovers |
| Token expired + refresh fails | Merchant's Square data stops flowing | `ValueError` from `refresh_token_flow()` | Merchant re-authorizes via `/oauth/authorize` |
| PostgreSQL down | All token CRUD fails, identity resolution fails | `/readiness` returns 503 | Restore DB connection |
| Valkey down | OAuth CSRF state storage fails; session fallback still works (GRO-386) | `/readiness` returns 503; OAuth may succeed via session cookie fallback | Restore Valkey |
| Fernet key format mismatch | Legacy token decryption fails | `_decrypt_fernet_legacy` raises exception | Verify `CANARY_ENCRYPTION_KEY` is valid Fernet key (for legacy) |

### Monitoring Recommendations

| Metric | Alert Threshold | Source |
|---|---|---|
| Token refresh failures | >2 in 1 hour per merchant | Application logs (`Token refresh failed`) |
| OAuth callback errors | Any CSRF mismatch | Application logs (`CSRF token mismatch`) |
| Encryption key missing | Any occurrence | Application logs (`No encryption key configured`) |
| Token store count | 0 merchants connected after 24h of uptime | `SELECT count(*) FROM app.square_oauth_tokens` |
| Expired tokens not refreshed | Token `expires_at` < now() with no refresh attempt | DB query + log correlation |

### Configuration

| Environment Variable | Purpose | Required | Current Source |
|---|---|---|---|
| `CANARY_ENCRYPTION_KEY` | AES-256-GCM key (base64url-encoded 32 bytes) | Yes (prod) | `.env` file |
| `SQUARE_APPLICATION_ID` | Square OAuth app client ID | Yes | `.env` file |
| `SQUARE_APPLICATION_SECRET` | Square OAuth app client secret | Yes | `.env` file |
| `SQUARE_ENVIRONMENT` | `sandbox` or `production` | Yes | `.env` file |
| `SQUARE_REDIRECT_URL` | OAuth callback URI override | No | `.env` file (falls back to `CANARY_DOMAIN/oauth/callback`) |
| `SQUARE_ACCESS_TOKEN` | Sandbox access token (sandbox shortcut only) | Sandbox only | `.env` file |
| `SQUARE_MERCHANT_ID` | Sandbox merchant ID (sandbox shortcut only) | Sandbox only | `.env` file |
| `CANARY_DOMAIN` | Base domain for redirect URI construction | Yes (prod) | `.env` file |
| `CANARY_ADMIN_MERCHANTS` | Comma-separated Square merchant IDs for admin elevation | No | `.env` file |
| `DATABASE_URL` | PostgreSQL connection string | Yes | `.env` file |
| `VALKEY_URL` | Valkey connection string | Yes | `.env` file |

**Requested OAuth scopes** (hardcoded in `square_oauth_wired.py`):
`MERCHANT_PROFILE_READ`, `PAYMENTS_READ`, `ORDERS_READ`, `EMPLOYEES_READ`, `TIMECARDS_READ`, `ITEMS_READ`, `INVENTORY_READ`, `GIFTCARDS_READ`, `CUSTOMERS_READ`, `CASH_DRAWER_READ`.

---

## Deployment

### Docker Service

Identity-Square runs inside the `canary-flask` container. No separate deployment unit.

```yaml
# Part of Canary/devops/docker-compose.yml
canary-flask:
  build: ..
  image: canary-flask
  ports:
    - "5001:5001"
  environment:
    - CANARY_ENCRYPTION_KEY=${CANARY_ENCRYPTION_KEY}
    - SQUARE_APPLICATION_ID=${SQUARE_APPLICATION_ID}
    - SQUARE_APPLICATION_SECRET=${SQUARE_APPLICATION_SECRET}
    - SQUARE_ENVIRONMENT=${SQUARE_ENVIRONMENT}
    # ... other env vars
  depends_on:
    - growdirect_postgres
    - growdirect_valkey
```

### AWS Target Architecture

| Component | AWS Service | Notes |
|---|---|---|
| Flask app | ECS/Fargate | Single task definition with canary-flask |
| PostgreSQL | RDS PostgreSQL 17 | `canary` database |
| Valkey | ElastiCache (Valkey-compatible) | DB 0 for sessions + cache |
| `CANARY_ENCRYPTION_KEY` | **AWS Secrets Manager** (target) | Currently in `.env` — P0 finding |
| `SQUARE_APPLICATION_SECRET` | **AWS Secrets Manager** (target) | Currently in `.env` — P0 finding |
| OAuth callback | ALB + Route53 | HTTPS required for production OAuth redirect |

### CI/CD Requirements

- Encryption key must be injected from Secrets Manager at container startup, not baked into image.
- OAuth callback URL must match the Square Developer Dashboard redirect URI exactly.
- Sandbox and production environments must use separate Square application IDs.

---

## Type 4 Additional Sections: External Integration

### Signature Validation

Square OAuth does not use webhook signatures on the OAuth flow itself. CSRF protection is handled via a state token stored in Valkey (GRO-386) with 5-minute TTL and session cookie fallback:

1. `/oauth/authorize` generates a random state token (`secrets.token_urlsafe(32)`), stores it in Valkey as `canary:oauth_state:<token>` with 300-second TTL, and also saves it in the Flask session as fallback.
2. `/oauth/callback` checks Valkey first for the state token, deletes it on match (one-time use). If Valkey lookup fails, falls back to session cookie comparison.
3. On mismatch: redirect to login with `error=oauth_csrf_mismatch`.

Square webhook signature validation (HMAC-SHA256) is handled upstream in TSP Sub 1 and is documented in the TSP SDD.

### Retry and Idempotency

| Operation | Retry | Idempotency |
|---|---|---|
| Token exchange (`/oauth2/token`) | No retry — redirect to error on failure | Not needed (one-time auth code) |
| Token refresh (`/oauth2/token` refresh grant) | No automatic retry; next `get_token()` call triggers a new refresh attempt | Safe to retry — Square issues new tokens |
| Token revocation (`/oauth2/revoke`) | No retry — best-effort call | Idempotent at Square |
| `store_token()` | No retry at service level | Idempotent — upserts by `merchant_id` |
| `register_external_id()` | No retry at service level | Idempotent — upserts by `(merchant, entity, source)` |
| `bulk_register()` | No retry at service level | Idempotent — skips existing mappings |

### Degradation When Square Is Down

| Square API State | Impact on Canary | Behavior |
|---|---|---|
| OAuth endpoints down | New merchant connections fail | User sees error redirect; existing merchants unaffected |
| Merchants API down | Merchant provisioning degrades | Falls back to `business_name="New Merchant"`, `currency="USD"` |
| Token refresh endpoint down | Expired tokens cannot refresh | `get_token()` raises `ValueError`; downstream API calls fail until Square recovers and merchant re-authorizes |
| All Square APIs down | No new data flows; existing data remains accessible | Canary UI continues working with cached data; webhook delivery from Square stops |

---

## Data Model

All tables in the `app` schema. All models use SQLAlchemy 2.0 `Mapped[]` syntax.

### SquareOAuthToken (`app.square_oauth_tokens`)

One row per merchant. Tokens encrypted at rest with AES-256-GCM.

| Column | Type | Encryption | Notes |
|---|---|---|---|
| `id` | `String(36)` PK | none | UUID, `generate_uuid()` default |
| `merchant_id` | `String` (TenantMixin) | none | FK to `merchants.id` (Canary UUID) |
| `access_token_encrypted` | `Text` NOT NULL | AES-256-GCM | Stored as `GCM:<base64(...)>` |
| `refresh_token_encrypted` | `Text` nullable | AES-256-GCM | Null if non-renewable |
| `token_type` | `String(20)` | none | Default `bearer` |
| `expires_at` | `DateTime` nullable | none | UTC timestamp |
| `scopes` | `Text` | none | Comma-separated |
| `created_at` / `updated_at` | `DateTime` (AuditMixin) | none | Automatic timestamps |

Index: `idx_square_oauth_tokens_merchant_id` on `merchant_id`.

### ExternalIdentity (`app.external_identities`)

Junction table: Canary UUID to source system ID. One row per `(merchant, entity, source)`.

| Column | Type | Notes |
|---|---|---|
| `id` | `String` PK | UUID |
| `merchant_id` | `String` (TenantMixin) | FK to `merchants.id` |
| `entity_type` | `String` | CHECK: `employee\|location\|device\|product\|customer` |
| `entity_id` | `String` | Canary UUID for this entity |
| `source_code` | `String` | FK to `source_systems.code` |
| `external_id` | `String` | Square's native ID |
| `is_primary` | `Boolean` | True = this source is authoritative |

Constraints: Two UNIQUE constraints prevent duplicate forward/reverse mappings. Two composite indexes optimize resolution queries.

### MerchantSource (`app.merchant_sources`)

Registry of authorized data sources per merchant. See dependency graph for full column list.

### SourceSystem (`app.source_systems`)

Reference table for POS identifiers. PK is `code` string (e.g., `square`, `clover`).

---

## Security & Compliance

### OAuth Token Encryption (Reference Pattern)

See the "AES-256-GCM Encryption Reference" section above for full implementation details. Key points:

- Access and refresh tokens are **always** encrypted before storage.
- Decryption happens only inside `SquareOAuthService.get_token()`, `refresh_token_flow()`, and `revoke_token()`.
- The `_encrypt()` / `_decrypt()` methods on `SquareOAuthService` delegate to `canary.utils.crypto` functions.
- Legacy Fernet tokens are transparently migrated to GCM on next write.

### CSRF Protection (GRO-386)

OAuth state token stored in Valkey with 5-minute TTL and one-time use semantics. Session cookie fallback for environments where Valkey is temporarily unavailable.

### PCI Compliance

Parsers follow strict PCI-safe extraction:
- `parse_card`: Extracts fingerprint, brand, last4, card_type. Does NOT extract cardholder name or billing address.
- `parse_payment`: Extracts CVV/AVS status as metadata. No raw card numbers transit Canary (Square tokenizes upstream).
- Full card data never enters Canary's network boundary.

### Privacy Enforcement

- `parse_customer`: Stores only `square_customer_id` and timestamps. No name, email, phone, or address extracted.
- `parse_loyalty_account`: Phone number hashed with SHA-256 before storage (`phone_hash`). Raw phone discarded.
- `parse_team_member`: Minimal PII; `square_employee_id` is the relational key. Email extracted as display decoration only.

### Role-Based Access

| Route | Required Auth |
|---|---|
| `/oauth/status` | JWT |
| `/oauth/refresh` | JWT + `admin` role |
| `/oauth/disconnect` | JWT + `owner` or `admin` role |
| Identity MCP tools | Read-only, no destructive operations |
| Sandbox routes | `SQUARE_ENVIRONMENT == sandbox` + session admin |

---

## Error Handling

### OAuth Callback: Hard vs Soft Failures

**Hard failures (redirect to error page):**
- CSRF state mismatch
- Square returns `error` parameter
- Missing `code` in callback
- Token exchange returns non-200

**Soft failures (log and continue):**
- `_provision_merchant()`: Falls back to `business_name="New Merchant"`, `currency="USD"` on Square API failure.
- `_register_square_source()`: Catch-all, logs warning.
- `_store_granted_scopes()`: Catch-all, logs warning.
- `_run_onboarding_pipeline()`: Catch-all, logs warning.
- `_trigger_first_health_check()`: Catch-all, logs warning.

### SquareOAuthService Error Handling

- `get_token()`: Returns `None` if no token record exists. Auto-refreshes if expired.
- `refresh_token_flow()`: Raises `ValueError` on missing refresh token or Square rejection.
- `revoke_token()`: Always deletes local token row regardless of Square API success.
- Encryption init: Logs warning if key absent; does not raise until first encrypt call in production.

### Parser Error Handling

All 16 parsers follow a consistent defensive pattern:
- `.get("key", {})` with empty-dict defaults for nested objects.
- ISO 8601 parsing with try/except; falls back to `None` or `datetime.now(UTC)`.
- Missing required fields log a warning but return partial dicts to avoid dropping events.
- Exception: `parse_timecard` returns `None` on missing required fields; TSP Sub 2 must check.

---

## Code Review Findings

### F1: Encryption Key in `.env` File — P0

**Description:** `CANARY_ENCRYPTION_KEY` is loaded from `.env` via `os.getenv()`. The `.env` file is not encrypted, is mounted into the container, and could be committed to version control or exposed in container inspection. Same applies to `SQUARE_APPLICATION_SECRET`.

**Recommended fix:** Move all secrets (`CANARY_ENCRYPTION_KEY`, `SQUARE_APPLICATION_SECRET`, `SQUARE_ACCESS_TOKEN`) to AWS Secrets Manager. Use `boto3` to retrieve at container startup. The crypto module's `_get_gcm_key()` should support reading from Secrets Manager as a primary source with env var fallback for local dev.

**Linear:** Needs GRO issue.

### F2: No Audit Logging for Token Access — P1

**Description:** `get_token()` logs `Stored OAuth token for merchant=...` on writes but does not log token reads or decryptions. There is no audit trail showing which service or request accessed a merchant's decrypted token. `revoke_token()` logs the deletion but not who initiated it.

**Recommended fix:** Add structured audit log entries for: (a) every `get_token()` call (log merchant_id, caller identity, timestamp — never the token value), (b) every `refresh_token_flow()` call, (c) every `revoke_token()` call including the initiating user/role. Consider a dedicated `audit_log` table or structured log format for SIEM integration.

**Linear:** Needs GRO issue.

### F3: No Key Rotation Procedure — P2

**Description:** There is no documented or implemented procedure for rotating `CANARY_ENCRYPTION_KEY`. If the key is compromised, all tokens must be re-encrypted with a new key. The current code supports exactly one key — no dual-key or key-versioning mechanism exists.

**Recommended fix:** (a) Document a manual rotation procedure: decrypt all tokens with old key, re-encrypt with new key, swap env var. (b) Implement a key-versioning scheme: store a key version identifier alongside the ciphertext prefix (e.g., `GCMv2:`). (c) Support a `CANARY_ENCRYPTION_KEY_PREVIOUS` env var for dual-key decrypt during rotation window.

**Linear:** Needs GRO issue.

### F4: No AAD (Additional Authenticated Data) in GCM Encryption — P2

**Description:** The GCM encryption passes `aad=None` to `AESGCM.encrypt()`. This means the ciphertext is not bound to a specific merchant_id or context. If an attacker with database write access swapped the `access_token_encrypted` value between two merchant rows, the decryption would succeed without error.

**Recommended fix:** Pass the `merchant_id` as AAD to bind each ciphertext to its owner row. This requires updating both `encrypt_token()` and `decrypt_token()` to accept an `aad` parameter, and re-encrypting all existing tokens with AAD on migration.

**Linear:** Needs GRO issue.

### F5: No Rate Limiting on OAuth Endpoints — P1

**Description:** The `/oauth/authorize`, `/oauth/callback`, and `/oauth/sandbox` routes have no rate limiting. An attacker could abuse the authorize endpoint to generate excessive Square redirect requests, or attempt callback brute-forcing against the CSRF state.

**Recommended fix:** Apply Flask-Limiter decorators: `10/minute` on `/oauth/authorize`, `20/minute` on `/oauth/callback`, `5/minute` on `/oauth/sandbox`. The existing `limiter` extension is already initialized in `canary/extensions.py`.

**Linear:** Needs GRO issue.

### F6: Health Check Does Not Validate Encryption Key — P1

**Description:** The `/readiness` endpoint checks PostgreSQL and Valkey connectivity but does not verify that `CANARY_ENCRYPTION_KEY` is configured and valid. A container can pass readiness checks but fail on the first token operation.

**Recommended fix:** Add an encryption key check to the readiness endpoint. Test that `_get_gcm_key()` returns a non-None 32-byte key. Do not expose the key value in the health response.

**Linear:** Needs GRO issue.

### F7: Degraded Merchant Provisioning Allows Bad FK — P1

**Description:** If `_provision_merchant()` returns `None`, the callback falls back to using the raw Square merchant ID string as `data_merchant_id`. This string cannot satisfy FK constraints referencing `merchants.id` (UUID). `store_token()` will fail with an FK violation or silently write a bad merchant_id.

**Recommended fix:** Treat `internal_id is None` as a hard failure — redirect to error page instead of continuing with a string merchant ID that will break downstream FK relationships.

**Linear:** Needs GRO issue.

### F8: SDD Config Section Lists Wrong Env Var Name — P0 (documentation)

**Description:** The previous SDD version listed `TOKEN_ENCRYPTION_KEY` as the environment variable for encryption. The actual code uses `CANARY_ENCRYPTION_KEY` (verified in `canary/utils/crypto.py` line 29). This documentation mismatch could cause misconfiguration.

**Status:** Fixed in this SDD revision.

### F9: No Data Retention Policy for Tokens — P1

**Description:** There is no automated cleanup of `square_oauth_tokens` rows for disconnected merchants or expired sessions. Revoked tokens are deleted immediately, but merchants who simply stop using Canary accumulate stale token rows indefinitely.

**Recommended fix:** Implement a retention policy: (a) tokens for disconnected merchants (status `disconnected` in `merchant_sources`) should be deleted after 30 days, (b) tokens that have not been refreshed in 90 days should trigger a notification, (c) add a `last_accessed_at` column to track usage.

**Linear:** Needs GRO issue.

### F10: Fernet Legacy Tokens Not Proactively Migrated — P2

**Description:** Legacy Fernet-encrypted tokens are only re-encrypted as GCM when a merchant re-authorizes (triggering `store_token()`). Merchants who have not re-authorized since GRO-248 still have Fernet tokens. If the Fernet library is eventually removed from dependencies, these tokens become unreadable.

**Recommended fix:** Write a one-time migration script that reads all non-`GCM:` prefixed tokens, decrypts with Fernet, re-encrypts with GCM, and updates in place. Run before removing Fernet dependency.

**Linear:** Needs GRO issue.

---

## Production Readiness Checklist

- [x] OAuth tokens encrypted at rest (AES-256-GCM, GRO-248)
- [x] CSRF protection on OAuth flow (Valkey + session fallback, GRO-386)
- [x] PCI-safe parser extraction (no cardholder data stored)
- [x] Customer PII excluded from parsers (no name/email/phone)
- [x] Loyalty phone numbers hashed (SHA-256)
- [x] Production guard prevents plaintext token storage
- [x] Legacy Fernet tokens transparently decrypted
- [x] Health check endpoint responds (`/health`, `/readiness`)
- [x] Role-based access on sensitive routes
- [x] Idempotent identity resolution (upsert pattern)
- [ ] **Secrets in AWS Secrets Manager** (currently `.env` — F1, P0)
- [ ] **Audit logging for token access** (no audit trail — F2, P1)
- [ ] **Rate limiting on OAuth endpoints** (none — F5, P1)
- [ ] **Health check validates encryption key** (not checked — F6, P1)
- [ ] **Hard fail on merchant provisioning failure** (degrades to bad FK — F7, P1)
- [ ] **Data retention policy for tokens** (no cleanup — F9, P1)
- [ ] **Key rotation procedure documented** (no procedure — F3, P2)
- [ ] **AAD binding in GCM encryption** (not implemented — F4, P2)
- [ ] **Proactive Fernet migration** (passive only — F10, P2)

---

## Square Parsers Reference

16 pure-function parser modules normalize Square webhook payloads into Canary CRDM dicts. All parsers: no database access, no Flask context, no side effects. Input: raw payload dict. Output: CRDM dict with UUID `id` field.

| Parser Module | Function(s) | Event Types | Target Model(s) |
|---|---|---|---|
| `square_payment_parser` | `parse_payment`, `parse_refund` | `payment.*`, `refund.*` | `Transaction`, `RefundLink` |
| `square_order_parser` | `parse_order` + 8 child parsers | `order.*` | `Transaction` + 8 child models |
| `square_customer_parser` | `parse_customer` | `customer.*` | `Customer` |
| `square_location_parser` | `parse_location` | `location.*` | `Location` |
| `square_device_parser` | `parse_device` | `device.*` | `Device` |
| `square_card_parser` | `parse_card` | `card.*` | `CardProfile` |
| `square_team_member_parser` | `parse_team_member` | `team_member.*` | `Employee` |
| `square_invoice_parser` | `parse_invoice` | `invoice.*` | `Invoice` |
| `square_loyalty_parser` | `parse_loyalty_account`, `parse_loyalty_event` | `loyalty.*` | `LoyaltyAccount`, `LoyaltyEvent` |
| `square_gift_card_parser` | `parse_gift_card` | `gift_card.*` | `GiftCard` |
| `square_subscription_parser` | `parse_subscription` | `subscription.*` | `Subscription` |
| `square_dispute_parser` | `parse_dispute` | `dispute.*` | `Dispute` |
| `square_payout_parser` | `parse_payout` | `payout.*` | `Payout` |
| `square_bank_account_parser` | `parse_bank_account` | `bank_account.*` | `BankAccount` |
| `square_terminal_parser` | `parse_terminal_checkout`, `parse_terminal_refund` | `terminal.*` | `TerminalCheckout`, `TerminalRefund` |
| `square_auxiliary_parsers` | 5 functions | `cash_drawer.*`, `labor.*`, `inventory.*`, `gift_card_activity.*` | Various |

---

## Known Issues & Reconciliation

### Degraded merchant provisioning path

If `_provision_merchant()` returns `None`, the callback uses the raw Square merchant ID string as `data_merchant_id`. This breaks FK constraints. See F7. Treat as a hard failure.

### Sandbox shortcut bypasses scope collection

`/oauth/sandbox` passes `SQUARE_SCOPES.split()` to `_store_granted_scopes` rather than scopes from the actual token. Acceptable for development; scope-gated features need real OAuth flow.

### `parse_order.employee_id` always `None`

Order events lack `team_member_id` at the order level. TSP Sub 2's `_build_models()` backfills from tenders. Unattributed transactions (no assignable employee) remain `employee_id=None` — treated as unattributed, not manager overrides. See GRO-299.

### `parse_timecard` returns `None` on missing fields

Unlike other parsers that return partial dicts, `parse_timecard` returns `None` on missing required fields. TSP Sub 2 must check for `None` before model instantiation.

### `resolve_category_name` depends on catalog presence

Square does not always include catalog data in webhook payloads. Category names are best-effort decoration; downstream services must not depend on them.

---

## Testing

### Unit Tests

One test file per parser module in `Canary/tests/unit/`. 16 parser test files + `test_external_identities.py` for the identity model and resolver.

All parser tests use fully-populated payloads (no null shortcuts — platform standard). Critical assertions per parser:
1. Output `id` is a valid UUID string.
2. `merchant_id` propagated from top-level payload.
3. Square entity ID extracted correctly from `data.object.<type>` (webhook format).
4. Monetary amounts extracted from `*_money.amount` sub-objects.
5. PII fields absent from output dict.

### Integration Tests

Identity resolver integration tests (requires `canary_test` DB):
- `register_external_id` is idempotent.
- `resolve_to_canary` returns correct UUID.
- `resolve_to_external` returns list with correct shape.
- `bulk_register` skips existing, returns correct count.

### Running

```bash
# Parser unit tests (no DB required)
python3 -m pytest tests/unit/ -k "parser" -v

# External identity tests
python3 -m pytest tests/unit/test_external_identities.py -v

# Full unit suite
python3 -m pytest tests/unit/ -v

# Integration tests (requires canary_test DB)
python3 -m pytest tests/integration/ -m postgres -v
```

---

## Downstream Consumers

| Service | What it Consumes |
|---|---|
| TSP (all subsystems) | `SquareOAuthService.get_token()` for authenticated Square API calls |
| TSP Sub 2 | All 16 parser modules for event normalization |
| Chirp | Customer aggregates from `parse_customer`; employee risk from `app.employees` |
| Owl | Merchant/employee/location data via Identity MCP tools |
| Fox | Dispute records from `parse_dispute` |
| OnboardingCoordinator | Called from OAuth callback |
| Health check runner | Called from OAuth callback |
