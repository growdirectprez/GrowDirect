# Identity

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]
**Architecture:** [[docs/sdds/canary/architecture|Canary Architecture SDD]]
**Service Type:** Type 1 — App Service (Canary)
**Last Code Review:** 2026-04-13

## Purpose

The Identity domain owns merchant registration, user authentication, RBAC, Square OAuth token management, and tenant context injection. It is the security perimeter and tenant boundary for every other domain in Canary LP. No data flows into the system until Identity establishes a merchant via Square OAuth.

**Core principle:** Organization is business identity; Merchant is POS connection. One organization owns 1..N merchants (multi-location chains). Each merchant maps to exactly one Square OAuth token. All tenant-scoped tables inherit `merchant_id` via `TenantMixin`.

**Authentication model:** Square OAuth is the only way in. No login forms, no stubs, no Keycloak in production today. The OAuth callback creates a Flask session (Valkey-backed). JWT middleware supports two modes: `development` (Bearer token matching `CANARY_DEV_JWT_SECRET` grants admin role) and `production` (rejects all — Keycloak RS256 not yet implemented). API key bypass (`X-API-Key` header matching `CANARY_MCP_API_KEY`) enables agent-to-agent calls.

## Dependencies

| Dependency | Type | Required | Notes |
|------------|------|----------|-------|
| PostgreSQL (`canary` DB, `app` schema) | Database | Yes | All identity tables |
| Valkey (DB 0) | Cache/Sessions | Yes | Server-side sessions, rate limiter state, OAuth CSRF state |
| Square OAuth2 API | External API | Yes | Token exchange, refresh, revocation |
| Square Merchants API | External API | Yes | Business name, currency, country during provisioning |
| RaaS Onboarding Coordinator | Internal Service | No | Webhook registration + initial sync (best-effort) |
| Flask-Session | Library | Yes | Valkey-backed server-side sessions |
| Flask-Limiter | Library | Yes | Rate limiting (2000/day, 500/hr default) |
| Flask-Talisman | Library | Yes | Security headers (CSP, HSTS) |
| Flask-WTF (CSRFProtect) | Library | Yes | CSRF protection on forms |
| `cryptography` (AESGCM) | Library | Yes (prod) | AES-256-GCM token encryption |

## Data Flow & PII Map

### What enters

| Source | Data | Format |
|--------|------|--------|
| Square OAuth callback | Authorization code, merchant_id, access_token, refresh_token | HTTPS redirect + JSON token response |
| Square Merchants API | Business name, currency, country | JSON API response |
| User browser | Email (pre-OAuth capture), session cookie | Form POST, HTTP cookie |
| MCP agents | `X-API-Key` header, `merchant_id` in params | HTTP headers + JSON |

### What's stored

| Table | Field | PII Classification | Encryption | Notes |
|-------|-------|-------------------|------------|-------|
| `app.users` | `email` | **sensitive** | Plaintext | User login email — needs encryption |
| `app.users` | `username` | internal | Plaintext | Derived from email |
| `app.users` | `display_name` | internal | Plaintext | Merchant name or email |
| `app.users` | `last_login_at` | internal | Plaintext | Login timestamp |
| `app.organizations` | `billing_email` | **sensitive** | Plaintext | Billing contact — needs encryption |
| `app.organizations` | `org_name` | internal | Plaintext | Business name |
| `app.merchants` | `merchant_name` | internal | Plaintext | From Square API |
| `app.merchant_settings` | `notif_phone` | **sensitive** | Plaintext | SMS phone number — needs encryption |
| `app.square_oauth_tokens` | `access_token_encrypted` | **restricted** | AES-256-GCM | Encrypted at rest (GRO-248) |
| `app.square_oauth_tokens` | `refresh_token_encrypted` | **restricted** | AES-256-GCM | Encrypted at rest (GRO-248) |
| `app.interest_signup` | `email` | **sensitive** | Plaintext | Beta interest list — needs encryption |
| `app.employees` | `email` | **sensitive** | Plaintext | Synced from Square — needs encryption |
| `app.employees` | `phone` | **sensitive** | Plaintext | Synced from Square — needs encryption |
| `app.employees` | `name` | internal | Plaintext | Masked when `show_employee_names=false` |
| `app.audit_log` | `ip_address` | **sensitive** | Plaintext | Client IP — needs hashing |
| Valkey | Session data (user_id, roles, merchant_id) | internal | Plaintext in Valkey | No TLS or AUTH configured |
| Valkey | OAuth CSRF state tokens | internal | Plaintext in Valkey | 5-min TTL, one-time use |

### What exits

| Destination | Data | Notes |
|-------------|------|-------|
| Square OAuth2 API | client_id, client_secret, access_token, refresh_token | Token exchange, refresh, revocation |
| Flask `g` context | user_id, roles, merchant_id, merchant_ids, organization_id, display_name | Consumed by all downstream domains |
| Browser session cookie | Session ID only (data is server-side in Valkey) | HttpOnly, SameSite=Lax |
| MCP tool responses | Merchant profile, employee list, location list | Read-only, tenant-scoped |

## API Contract

### Auth Blueprint (`/auth`)

| Path | Method | Auth | Rate Limit | Description |
|------|--------|------|------------|-------------|
| `/auth/login-page` | GET | Public | Default | Landing page with "Connect with Square" button |
| `/auth/join` | GET | Public | Default | Alias for login-page |
| `/auth/start-connect` | POST | Public (CSRF exempt) | Default | Capture pre-OAuth email into session |
| `/auth/session-logout` | POST | Session | Default | Clear Flask session, redirect to `/auth/join` |
| `/auth/clear-session` | POST | Public (CSRF exempt) | Default | Emergency session reset |
| `/auth/join-interest` | POST | Public (CSRF exempt) | Default | Capture email for beta interest list |
| `/auth/session-login` | POST | Public (CSRF exempt) | Default | Deprecated redirect to login-page |

### OAuth Blueprint (`/oauth`)

| Path | Method | Auth | Rate Limit | Description |
|------|--------|------|------------|-------------|
| `/oauth/authorize` | GET | Public | Default | Redirect to Square OAuth consent screen with CSRF state |
| `/oauth/callback` | GET | Public | Default | Exchange auth code for tokens, provision merchant, run onboarding |
| `/oauth/status` | GET | JWT | Default | Check token connection status and expiry |
| `/oauth/refresh` | POST | JWT + admin | Default | Force-refresh access token via Square API |
| `/oauth/disconnect` | POST | JWT + owner/admin | Default | Revoke token and disconnect source |
| `/oauth/sandbox` | GET | Public (sandbox only) | Default | Dev shortcut: store sandbox tokens directly |
| `/oauth/reset-onboarding` | GET | Session (sandbox only) | Default | Factory reset: truncate transactional data |
| `/oauth/merchant-reset` | POST | Session (sandbox only) | Default | Tenant-scoped reset |
| `/oauth/factory-reset` | POST | Session (sandbox only) | Default | Full factory reset + Valkey flush |

### Merchant REST (`/api/merchants`)

| Path | Method | Auth | Description |
|------|--------|------|-------------|
| `/api/merchants/profile` | GET | JWT | Get merchant profile |
| `/api/merchants/profile` | PUT | JWT | Update merchant profile |
| `/api/merchants/settings` | GET | JWT | Get merchant settings |
| `/api/merchants/settings` | PUT | JWT | Update merchant settings |

### Employee REST (`/api/employees`)

| Path | Method | Auth | Description |
|------|--------|------|-------------|
| `/api/employees/` | GET | JWT | List employees (filterable) |
| `/api/employees/<id>` | GET | JWT | Get single employee |
| `/api/employees/<id>/transactions` | GET | JWT | Employee transaction history |
| `/api/employees/<id>/alerts` | GET | JWT | Employee alert history |
| `/api/employees/<id>/risk` | GET | JWT | Employee risk score |

### Location REST (`/api/locations`)

| Path | Method | Auth | Description |
|------|--------|------|-------------|
| `/api/locations/` | GET | JWT | List locations |
| `/api/locations/<id>` | GET | JWT | Get single location |
| `/api/locations/<id>` | PUT | JWT | Update location |
| `/api/locations/<id>/stats` | GET | JWT | Location statistics |

### Identity MCP (`/identity`)

| Tool | Auth Required | PII Access | Rate Limit | Description |
|------|:---:|:---:|:---:|-------------|
| `get_merchant` | API Key | merchant_name | Default | Get merchant profile |
| `get_settings` | API Key | notification prefs | Default | Get merchant settings |
| `list_employees` | API Key | name, email, phone | Default | List employees for merchant |
| `get_employee` | API Key | name, email, phone, risk_score | Default | Get single employee detail |
| `list_locations` | API Key | address | Default | List locations for merchant |
| `get_location` | API Key | address | Default | Get single location detail |

Standard MCP endpoints: `/identity/manifest`, `/identity/tools`, `/identity/tools/<name>`, `/identity/health`. All read-only; writes stay in REST blueprints.

## Data Model

All Identity tables live in the `app` schema within the single `canary` database. Models use SQLAlchemy 2.0 `Mapped[]` syntax with `AppBase`.

### organizations
Root business entity. One org owns 1..N merchants.

| Column | Type | Notes |
|--------|------|-------|
| id | String(36) PK | uuid4 |
| org_name | String(255) | Business name |
| billing_email | String(255) | Nullable |
| subscription_tier | String(20) | starter / professional / enterprise |
| billing_provider | String(20) | square / manual / none |
| billing_external_id | String(255) | Square subscription ID |
| billing_status | String(20) | trialing / active / past_due / canceled / comped |
| is_active | Boolean | Default true |

Mixins: AuditMixin, SoftDeleteMixin (GSLM: db_status, effective dating). Access: CRUD. FKs: parent of merchants.

### merchants
POS connection entity. One merchant = one Square account = one OAuth token.

| Column | Type | Notes |
|--------|------|-------|
| id | String(36) PK | Internal UUID (used in all data tables) |
| organization_id | String(36) FK | -> organizations.id |
| source_merchant_id | String(36) UNIQUE | Square merchant ID (external) |
| merchant_name | String(255) | From Square Merchants API |
| currency | String(3) | Default USD |
| is_active | Boolean | Default true |

Mixins: None (standalone with manual timestamps). Access: CRUD. FKs: every tenant-scoped table references merchant_id.

### merchant_settings
Per-merchant configuration. One row per merchant. Drives fiscal calendar for all period metrics and dashboard rendering.

Key columns: timezone, language, date_format, calendar_type (nrf_454 | calendar_month), fiscal_year_start_month, fiscal_week_start_day, fiscal_pattern (4,5,4 etc.), notification prefs (email/sms/in_app, quiet hours, severity threshold, daily limit, phone), theme, show_employee_names. Mixins: None (manual timestamps). Access: CRUD. FK: merchant_id UNIQUE.

### users
User account created on Square OAuth login. Multi-tenant via user_roles.

| Column | Type | PII | Notes |
|--------|------|-----|-------|
| id | String(36) PK | No | uuid4 |
| merchant_id | String(36) FK | No | Primary tenant (via TenantMixin) |
| username | String(100) | No | Derived from email prefix |
| email | String(255) | **sensitive** | Login email — plaintext |
| display_name | String(255) | internal | Merchant name or email |
| is_active | Boolean | No | Default true |
| last_login_at | datetime | No | Login timestamp |

Mixins: TenantMixin, AuditMixin, SoftDeleteMixin. Constraints: UNIQUE(merchant_id, email). Access: CRUD.

### roles
Global RBAC definitions. Not tenant-scoped. Six roles: admin, owner, manager, operator, member, viewer.

Key columns: role_name (UNIQUE), description. Mixins: AuditMixin. Access: read-mostly (seeded via reference_data.py).

### user_roles
Tenant-scoped role assignments. A user can hold different roles across merchants.

Key columns: user_id FK -> users.id, role_id FK -> roles.id, merchant_id. Mixins: TenantMixin, AuditMixin. Access: CRUD.

### square_oauth_tokens
Encrypted OAuth credentials. One per merchant. AES-256-GCM encryption at rest.

| Column | Type | PII | Notes |
|--------|------|-----|-------|
| id | String(36) PK | No | uuid4 |
| merchant_id | String(36) FK | No | Via TenantMixin |
| access_token_encrypted | Text | **restricted** | AES-256-GCM encrypted |
| refresh_token_encrypted | Text | **restricted** | AES-256-GCM encrypted (nullable) |
| token_type | String(20) | No | Default "bearer" |
| expires_at | datetime | No | UTC expiration |
| scopes | Text | No | Comma-separated granted scopes |

Mixins: TenantMixin, AuditMixin. Access: CRUD (managed by SquareOAuthService).

### Additional tables (Identity-adjacent)

- **employees**: Staff records synced from Square. PII: name, email, phone (all plaintext).
- **locations**: Physical store locations synced from Square. Address is internal.
- **location_hierarchy**: Parent-child location relationships.
- **customers**: Customer profiles synced from Square. PII: name, email (plaintext).
- **products**: Catalog items synced from Square. No PII.
- **source_systems**: Registry of external data sources. No PII.
- **merchant_sources**: Junction between merchants and source systems. Tracks connection status and granted scopes.
- **interest_signup**: Beta interest list. PII: email (plaintext).

## Workflows

### Merchant Onboarding (Square OAuth)

This is the primary entry point for all merchants. No data flows until OAuth completes.

**Step 1: Authorize**
1. Merchant clicks "Connect with Square" on `/auth/join`.
2. `GET /oauth/authorize` generates CSRF state token (32-byte `secrets.token_urlsafe`).
3. State stored in Valkey with 5-min TTL (`canary:oauth_state:{state}`), plus session fallback.
4. Redirects to `https://connect.squareup[sandbox].com/oauth2/authorize` with client_id, scopes, state, redirect_uri.
5. Required scopes: MERCHANT_PROFILE_READ, PAYMENTS_READ, ORDERS_READ, EMPLOYEES_READ, TIMECARDS_READ, ITEMS_READ, INVENTORY_READ, GIFTCARDS_READ, CUSTOMERS_READ, CASH_DRAWER_READ.

**Step 2: Callback (token exchange + provisioning)**
1. Square redirects to `GET /oauth/callback` with authorization code and state.
2. CSRF state validation: checks Valkey first (survives redirect behind TLS proxy), session fallback. Mismatch -> redirect with error.
3. Exchange code for access_token + refresh_token via `POST /oauth2/token`.
4. `_provision_merchant()`: checks if merchant exists (returns existing UUID), else fetches business name/currency/country from Square, creates Merchant + MerchantSettings rows.
5. `SquareOAuthService.store_token()` encrypts tokens (AES-256-GCM) and writes `square_oauth_tokens`.
6. `_register_square_source()` creates/updates `merchant_sources` record (status: active).
7. `_store_granted_scopes()` writes granted scopes to `merchant_sources.metadata_json`.
8. Commit all writes.

**Step 3: User Provisioning (GRO-288)**
1. `_provision_user_on_login()` upserts `app.users` row by merchant_id + email.
2. First user for a merchant gets admin role; subsequent users get viewer.
3. Race condition handled: IntegrityError on concurrent login catches duplicate, fetches existing row.
4. `_auto_match_employee()` links user to employee record by email match (best-effort).
5. Fallback: if provisioning fails entirely, returns system user UUID with viewer role.

**Step 4: Session Creation**
1. Session populated: user_id, roles, merchant_id, display_name, theme.
2. Admin elevation: if source_merchant_id is in `CANARY_ADMIN_MERCHANTS` env var, append admin role.
3. Session marked permanent (7-day lifetime via `PERMANENT_SESSION_LIFETIME`).
4. Redirect to `/welcome` (new users) or `/chirps` (returning users).

**Step 5: Onboarding Pipeline (best-effort)**
1. `_run_onboarding_pipeline()` calls `OnboardingCoordinator.run_inline()`.
2. Registers Square webhook subscriptions. Optional initial sync.
3. Auto-triggers first health check if merchant has no existing OwlSession.
4. Never blocks the OAuth flow — all errors logged and swallowed.

**Onboarding State Machine:**
`not_connected -> authorizing -> connected -> syncing -> active`. Error states: `token_expired -> refreshing -> active`, `token_revoked -> disconnected`, `sync_failed -> error (retry available)`.

### Token Lifecycle

**Refresh:** `SquareOAuthService.refresh_token_flow()` calls Square `POST /oauth2/token` with grant_type=refresh_token. Auto-refresh triggered in `get_token()` when `expires_at < now`. Manual trigger via `POST /oauth/refresh` (admin only). 30-second timeout on Square API call.

**Revocation:** `POST /oauth/disconnect` calls `SquareOAuthService.revoke_token()` (best-effort Square API call, local row always deleted) then `RaaSNamespaceResolver.disconnect_source()`.

**Encryption:** `canary/utils/crypto.py` (GRO-248). Algorithm: AES-256-GCM via `cryptography.hazmat.primitives.ciphers.aead.AESGCM`. Key: `CANARY_ENCRYPTION_KEY` env var (base64-encoded, decoded to 32-byte raw key). Format: `"GCM:<base64(nonce + ciphertext + tag)>"`. Nonce: 12 bytes (os.urandom). Migration: transparent read of legacy Fernet (`gAAAAA...`) and `UNENCRYPTED:` prefixes; always re-encrypts as GCM on next store. In production, missing key or missing `cryptography` package raises `RuntimeError`.

### Session Management

Sessions stored in Valkey (server-side, DB 0). Created by OAuth callback, consumed by `load_session_user()` on every browser request.

**Session keys:** `user_id`, `roles`, `merchant_id`, `merchant_ids`, `organization_id`, `display_name`, `theme`, `join_email` (temporary, pre-OAuth).

**Session config:**
- `SESSION_TYPE = "redis"` (Valkey-compatible)
- `SESSION_KEY_PREFIX = "canary:session:"`
- `SESSION_COOKIE_HTTPONLY = True`
- `SESSION_COOKIE_SAMESITE = "Lax"`
- `SESSION_COOKIE_SECURE = True` (production), dynamic in dev
- `PERMANENT_SESSION_LIFETIME = 7 days`

**Flask `g` context** (set by `load_session_user()` or `jwt_required()`): `g.user_id`, `g.roles`, `g.merchant_id`, `g.merchant_ids`, `g.organization_id`, `g.display_name`.

**User validation (GRO-386):** `load_session_user()` checks that `user_id` exists and `is_active=true` in DB. If user is missing or inactive, session is cleared. DB errors fail open (don't block user due to infra issues).

### JWT Authentication

`@jwt_required` decorator validates Bearer tokens or API keys.

**API key mode:** `X-API-Key` header matching `CANARY_MCP_API_KEY` env var grants admin access with hardcoded `user_id='alx-agent'`. Resolves Square merchant_id to internal UUID.

**Development mode:** Bearer token must exactly match `CANARY_DEV_JWT_SECRET` env var. Grants admin access with `user_id='dev-user'`. Resolves merchant IDs from `CANARY_DEFAULT_MERCHANTS`.

**Production mode:** Currently rejects all Bearer tokens with 401. Keycloak RS256/JWKS integration is designed but not implemented.

**Role decorators:** `@role_required(role)` requires exact role. `@roles_required(*roles)` requires ANY listed role. Both abort 403 on mismatch.

### RBAC Role Hierarchy

| Role | Capabilities |
|------|-------------|
| admin | Full access: all CRUD, config, user management, flush sessions |
| owner | Alert disposition, rule config, case management, settings, billing |
| manager | Alert disposition (acknowledge, dismiss), case management |
| operator | Case management, open cases from alerts |
| member | Read-only with limited actions |
| viewer | Read-only access (dashboard only) |

### PII Display Toggle (GRO-242)

`MerchantSettings.show_employee_names` gates employee name display across all routes. When `False`, employee names are masked in API responses, dashboard tables, and alert details. Default: `False`. Toggle exposed via `PUT /api/merchants/settings`.

### Sandbox Shortcuts

`GET /oauth/sandbox` stores sandbox tokens directly without OAuth flow. Provisions merchant, runs onboarding pipeline, creates session. Available only when `SQUARE_ENVIRONMENT=sandbox`.

Reset endpoints (sandbox only): `/oauth/reset-onboarding` (factory reset, requires admin role), `/oauth/merchant-reset` (tenant-scoped), `/oauth/factory-reset` (full truncate + Valkey flush).

## Operations

### Startup sequence

1. Shared infra starts: PostgreSQL, Valkey, Ollama (`devops/docker-compose.yml`)
2. Canary app starts: `wsgi.py` boots Flask, initializes extensions (CSRF, Session, Limiter, Talisman)
3. Valkey connection established for sessions (`SESSION_REDIS = redis.from_url(VALKEY_URL)`)
4. If Valkey unavailable: `SESSION_TYPE` degrades to `"null"` (cookie-based, logged as warning)
5. Rate limiter connects to same Valkey URL
6. Identity routes registered via blueprints: `auth_bp` at `/auth`, `square_oauth_bp` at `/oauth`

### Health checks

- Identity MCP health: `GET /identity/health` returns `{"service": "canary-identity", "healthy": true, "tools": 6}`
- No dedicated Identity health endpoint beyond MCP — relies on general app health at `/ops/health`
- Session health: implicit — `load_session_user()` validates user exists in DB on each request

### Failure modes

| Failure | Impact | Behavior |
|---------|--------|----------|
| Valkey down | Sessions degrade to cookie-based | Logged warning, `SESSION_TYPE` set to `"null"` |
| PostgreSQL down | All auth fails | 500 on login, existing sessions may work briefly (fail-open on user validation) |
| Square OAuth API down | Cannot onboard new merchants | OAuth callback returns error redirect |
| Square token refresh fails | API calls to Square stop working | Logged error, `ValueError` raised to caller |
| Encryption key missing | Token storage blocked in production | `RuntimeError` raised, app won't store tokens |
| CSRF state mismatch | OAuth callback rejected | Redirect to login with `oauth_csrf_mismatch` error |

### Monitoring

| Metric | Alert Threshold | Notes |
|--------|----------------|-------|
| OAuth callback errors | >5/hour | CSRF mismatches, token exchange failures |
| Token refresh failures | Any | Merchant loses Square API access |
| User provisioning failures | >3/hour | Fallback to system user degrades experience |
| Session validation failures | >10/min | May indicate DB connectivity issues |
| Valkey connection failures | Any | Sessions degrade to insecure cookie mode |

### Configuration (env vars)

| Variable | Required | Description |
|----------|----------|-------------|
| `CANARY_ENV` | Yes | `development` / `production` / `testing` |
| `SECRET_KEY` | Yes (prod) | Flask session signing key |
| `CANARY_ENCRYPTION_KEY` | Yes (prod) | Base64-encoded 32 bytes for AES-256-GCM |
| `SQUARE_APPLICATION_ID` | Yes | Square OAuth client ID |
| `SQUARE_APPLICATION_SECRET` | Yes | Square OAuth client secret |
| `SQUARE_ENVIRONMENT` | Yes | `sandbox` or `production` |
| `SQUARE_MERCHANT_ID` | No | Default merchant for sandbox/dev |
| `SQUARE_ACCESS_TOKEN` | No | Sandbox access token |
| `SQUARE_REDIRECT_URL` | No | OAuth callback URL (default: `{CANARY_DOMAIN}/oauth/callback`) |
| `CANARY_DOMAIN` | No | App domain (default: `http://localhost:5001`) |
| `CANARY_MCP_API_KEY` | No | API key for agent-to-agent auth |
| `CANARY_DEV_JWT_SECRET` | No (dev) | Bearer token value for dev-mode JWT |
| `CANARY_ADMIN_MERCHANTS` | No | Comma-separated Square merchant IDs for admin elevation |
| `CANARY_DEFAULT_ORG` | No | Default organization ID for dev/agent contexts |
| `CANARY_DEFAULT_MERCHANTS` | No | Comma-separated default merchants for dev JWT |
| `VALKEY_URL` | No | Valkey connection string (default: `redis://growdirect_valkey:6379/0`) |
| `RATE_LIMIT_STORAGE_URI` | No | Rate limiter storage (default: VALKEY_URL) |

## Deployment

### Docker service

Identity runs inside the Canary Flask container — not a separate service. Canary's Docker Compose is at `Canary/devops/docker-compose.dev.yml`.

- **Image:** `canary-app` (single Flask container)
- **Port:** 5001 (Flask/Gunicorn)
- **Network:** `growdirect` (external Docker network)
- **Dependencies:** `growdirect_postgres` (5432), `growdirect_valkey` (6379)

### AWS target

| Component | AWS Service | Notes |
|-----------|------------|-------|
| Canary Flask app | ECS/Fargate | Single task definition, includes all Identity routes |
| PostgreSQL | RDS (PostgreSQL 17) | `canary` database, `app` schema |
| Valkey | ElastiCache (Redis-compatible) | DB 0 for sessions + rate limiter |
| Secrets | AWS Secrets Manager | `CANARY_ENCRYPTION_KEY`, `SECRET_KEY`, Square credentials |
| OAuth callback | ALB + Route 53 | HTTPS endpoint for Square redirect |

### CI/CD requirements

- Encryption key must be rotated via Secrets Manager, not `.env`
- Square OAuth credentials must not be in container images
- Session cookie `Secure` flag must be `True` behind ALB/TLS
- Health check endpoint required for ECS task health

## Code Review Findings

### P0 — Blocks Production

**P0-1: Production JWT authentication not implemented**
- **File:** `canary/middleware/jwt_auth.py:323-326`
- **Finding:** In production mode (`CANARY_ENV=production`), `jwt_required()` rejects ALL Bearer tokens with a warning log and 401. The Keycloak RS256/JWKS path referenced in the original SDD does not exist in code. API routes protected by `@jwt_required` are completely inaccessible in production unless using the `X-API-Key` bypass.
- **Impact:** All API endpoints (`/api/merchants/*`, `/api/employees/*`, `/api/locations/*`, `/oauth/status`, `/oauth/refresh`, `/oauth/disconnect`) are non-functional in production mode via Bearer tokens.
- **Fix:** Implement JWT RS256 validation against an IdP JWKS endpoint, or formalize the API key approach as the production auth mechanism with proper key management.
- **Linear:** TBD

**P0-2: User emails stored plaintext**
- **File:** `canary/models/app/users.py:42-45`
- **Finding:** `User.email` is stored as plaintext `String(255)`. This is the merchant's login email, used for user provisioning and employee auto-matching. No field-level encryption.
- **Impact:** Database breach exposes all merchant email addresses.
- **Fix:** Apply AES-256-GCM field-level encryption using the existing `canary/utils/crypto.py` pattern. Encrypt on write, decrypt on read.
- **Linear:** TBD

**P0-3: Secrets in .env files, not Secrets Manager**
- **File:** `canary/config.py`, `canary/utils/crypto.py:29`
- **Finding:** `CANARY_ENCRYPTION_KEY`, `SECRET_KEY`, `SQUARE_APPLICATION_SECRET`, `CANARY_MCP_API_KEY`, and `CANARY_DEV_JWT_SECRET` are all loaded from environment variables, sourced from `.env` files in development. No integration with AWS Secrets Manager for production.
- **Impact:** Secrets stored in plaintext files on disk. No rotation mechanism. No access auditing.
- **Fix:** Implement `boto3` Secrets Manager retrieval at startup for production. Keep env vars for dev/test.
- **Linear:** TBD

**P0-4: API key bypass grants unrestricted admin access**
- **File:** `canary/middleware/jwt_auth.py:298-308`
- **Finding:** The `X-API-Key` bypass in `jwt_required()` grants `roles=['admin']` and uses a hardcoded `user_id='alx-agent'`. A single static API key provides full admin access to all merchants. No per-agent scoping, no audit trail, no key rotation.
- **Impact:** Compromised API key grants full read/write access to all merchant data. No way to revoke a single agent's access without rotating the shared key.
- **Fix:** Implement per-agent API keys with scoped roles, stored in DB with created_at/last_used_at/revoked_at. Log all API key authentications to audit_log.
- **Linear:** TBD

### P1 — Before GA

**P1-1: No audit logging for authentication events**
- **Finding:** Login, logout, token refresh, token revocation, role elevation, and session creation are logged via Python `logger` but not written to the `app.audit_log` table. The audit_log model exists with a SHA-256 hash chain, but Identity operations don't use it.
- **Impact:** No tamper-proof record of who logged in, when tokens were refreshed, or when admin elevation occurred.
- **Fix:** Write audit_log entries for: OAuth login, logout, token refresh, token revocation, admin elevation, user provisioning, role changes.
- **Linear:** TBD

**P1-2: Employee/customer PII stored plaintext**
- **File:** `canary/models/app/employees.py`, `canary/models/app/customers.py`
- **Finding:** `Employee.email`, `Employee.phone`, `Customer.email` are stored as plaintext. These are synced from Square and visible through MCP tools and REST APIs.
- **Impact:** Database breach exposes employee and customer contact information.
- **Fix:** Apply AES-256-GCM encryption to email and phone fields. Update MCP tool handlers to decrypt on read.
- **Linear:** TBD

**P1-3: Billing email and SMS phone stored plaintext**
- **File:** `canary/models/app/organizations.py:45-47`, `canary/models/app/merchants.py:202-203`
- **Finding:** `Organization.billing_email` and `MerchantSettings.notif_phone` are plaintext.
- **Impact:** Database breach exposes billing contacts and SMS numbers.
- **Fix:** Apply AES-256-GCM encryption.
- **Linear:** TBD

**P1-4: No rate limiting on OAuth endpoints**
- **File:** `canary/blueprints/square_oauth_wired.py`
- **Finding:** The OAuth authorize and callback endpoints use only the global default rate limit (2000/day, 500/hr). No stricter per-route limits on authentication-sensitive endpoints.
- **Impact:** OAuth endpoints could be targeted for abuse (state token enumeration, callback flooding).
- **Fix:** Apply stricter rate limits: `/oauth/authorize` at 10/min, `/oauth/callback` at 10/min, `/oauth/refresh` at 5/min.
- **Linear:** TBD

**P1-5: Session validation fails open on DB error**
- **File:** `canary/middleware/jwt_auth.py:425-427`
- **Finding:** `load_session_user()` catches DB exceptions during user validation and continues with the session data. Comment says "fail open (don't block user due to infra issues)".
- **Impact:** If PostgreSQL is down, stale sessions remain valid even if the user has been deactivated. An attacker with a stolen session cookie can access the system during DB outages.
- **Fix:** Fail closed: if DB validation fails, clear session and require re-authentication. Accept brief unavailability during DB outages rather than allowing potentially revoked sessions.
- **Linear:** TBD

**P1-6: IP addresses logged plaintext in audit_log**
- **File:** `canary/models/app/audit.py:68-71`
- **Finding:** `AuditLog.ip_address` stores raw IPv4/IPv6 addresses. No hashing or masking.
- **Impact:** Audit log becomes a PII liability. GDPR/CCPA implications for IP address storage.
- **Fix:** Hash IPs with HMAC-SHA256 (keyed, so you can still correlate) or truncate to /24.
- **Linear:** TBD

**P1-7: No data retention policy**
- **Finding:** No automated purge for sessions, audit logs, or deactivated user records. `PERMANENT_SESSION_LIFETIME` controls session cookie expiry (7 days) but orphaned Valkey keys may persist.
- **Impact:** Unbounded PII accumulation. No mechanism to honor data deletion requests.
- **Fix:** Implement retention policies: sessions auto-expire in Valkey (already via TTL), audit_log entries >24 months archived, deactivated users purged >12 months.
- **Linear:** TBD

### P2 — Post-Launch

**P2-1: No encryption key rotation procedure**
- **Finding:** `CANARY_ENCRYPTION_KEY` is a single static key. No rotation mechanism documented or implemented. The Fernet-to-GCM migration shows the pattern works (transparent re-encryption on next store), but there's no tooling to trigger a bulk re-encryption with a new key.
- **Fix:** Document and build key rotation: generate new key, update Secrets Manager, run migration script that re-encrypts all token rows, remove old key.
- **Linear:** TBD

**P2-2: Valkey sessions unencrypted and unauthenticated**
- **Finding:** Valkey DB 0 stores session data without TLS or AUTH. Session contents (user_id, roles, merchant_id) are readable by anything with network access to port 6379.
- **Fix:** Enable Valkey AUTH password and TLS in production. Update `VALKEY_URL` to use `rediss://` scheme.
- **Linear:** TBD

**P2-3: Worker-level merchant UUID cache has no TTL or size limit**
- **File:** `canary/middleware/jwt_auth.py:11`
- **Finding:** `_merchant_uuid_cache` is a plain `dict` that grows unboundedly within a Gunicorn worker process. No TTL, no eviction, no size limit.
- **Impact:** Memory growth in long-running workers. Stale cache entries if a merchant is deleted.
- **Fix:** Use an LRU cache with TTL (e.g., `cachetools.TTLCache`) or remove in favor of a Valkey lookup.
- **Linear:** TBD

**P2-4: Dev-mode JWT uses static shared secret, not signed tokens**
- **File:** `canary/middleware/jwt_auth.py:328-334`
- **Finding:** In development mode, "JWT validation" is actually a string comparison: `token == CANARY_DEV_JWT_SECRET`. This is not a JWT at all — no claims, no expiry, no signing. Any process with the secret has permanent admin access.
- **Impact:** Dev/test environments have no token expiry or claim validation. Acceptable for local dev but must not leak to staging/production.
- **Fix:** Acceptable for local development. Ensure `CANARY_ENV` is always set correctly in deployed environments. Add startup check that rejects `development` mode if running on a non-localhost address.
- **Linear:** TBD

**P2-5: MCP tool error responses may leak internal details**
- **File:** `canary/services/identity/tools.py`
- **Finding:** MCP tool error responses include `str(e)` from caught exceptions, which may contain SQL errors, file paths, or stack traces.
- **Fix:** Sanitize error responses in production. Log full errors server-side, return generic messages to callers.
- **Linear:** TBD

**P2-6: CSRF exempt on several auth endpoints**
- **File:** `canary/blueprints/auth.py:54,66,81,104`
- **Finding:** `clear_session`, `start_connect`, `join_interest`, and `session_login_redirect` are all `@csrf.exempt`. `clear_session` allows unauthenticated session destruction.
- **Impact:** CSRF attacks could clear user sessions (denial of service) or capture emails.
- **Fix:** Remove CSRF exemption from `clear_session` and `start_connect`. Keep exemption only on API-style endpoints that use their own auth (API key or JWT).
- **Linear:** TBD

## Production Readiness Checklist

- [x] OAuth tokens encrypted at rest (AES-256-GCM, GRO-248)
- [ ] User email encrypted at rest (P0-2)
- [ ] Employee/customer PII encrypted at rest (P1-2)
- [ ] Billing email and SMS phone encrypted at rest (P1-3)
- [ ] Secrets in AWS Secrets Manager, not .env (P0-3)
- [x] Health check endpoint responds (`/identity/health`)
- [ ] Audit logging for authentication events (P1-1)
- [ ] Data retention policy implemented (P1-7)
- [x] Rate limiting on public endpoints (Flask-Limiter, global defaults)
- [ ] Stricter rate limiting on OAuth endpoints (P1-4)
- [ ] Error responses don't leak internals (P2-5)
- [x] CSRF protection on forms (Flask-WTF)
- [x] Session cookies: HttpOnly, SameSite=Lax, Secure (prod)
- [x] Server-side sessions in Valkey (not cookie-stored)
- [x] Token encryption migration path (Fernet -> GCM transparent)
- [ ] Production JWT validation implemented (P0-1)
- [ ] Per-agent API key scoping (P0-4)
- [ ] Encryption key rotation procedure (P2-1)
- [ ] Valkey AUTH + TLS in production (P2-2)
- [ ] Session validation fails closed (P1-5)
- [ ] IP address hashing in audit log (P1-6)

**Production blockers (P0):** 4 findings — JWT auth, user email encryption, secrets management, API key scoping.
