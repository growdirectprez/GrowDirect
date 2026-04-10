# Identity

## Overview

The Identity domain owns merchant registration, user authentication, RBAC, Square OAuth token management, and tenant context injection. It is the security perimeter and tenant boundary for every other domain in Canary LP. No data flows into the system until Identity establishes a merchant via Square OAuth.

**Core principle:** Organization is business identity; Merchant is POS connection. One organization owns 1..N merchants (multi-location chains). Each merchant maps to exactly one Square OAuth token. All tenant-scoped tables inherit `merchant_id` via `TenantMixin`.

**Authentication model:** Square OAuth is the only way in. No login forms, no stubs, no Keycloak in production today. The OAuth callback creates a Flask session (Valkey-backed). JWT middleware supports two modes: `keycloak` (RS256 signature validation against JWKS) and `development` (any Bearer token accepted with admin role). API key bypass (`X-API-Key` header matching `CANARY_MCP_API_KEY`) enables agent-to-agent calls.

**Blueprints:**

| Blueprint | Prefix | Purpose |
|-----------|--------|---------|
| `auth` | `/auth` | Landing page, session logout, interest signup |
| `square_oauth` | `/oauth` | Square OAuth flow, token management, sandbox shortcuts |
| `merchants_wired` | `/api/merchants` | Merchant profile and settings CRUD |
| `employees_wired` | `/api/employees` | Employee list, detail, transactions, alerts, risk |
| `locations_wired` | `/api/locations` | Location CRUD and stats |
| `identity_mcp` | `/identity` | MCP tool server (6 read-only tools) |

**MCP tools (canary-identity server, 6 tools):** `get_merchant`, `get_settings`, `list_employees`, `get_employee`, `list_locations`, `get_location`. All read-only; writes stay in REST blueprints.

**Code entry points:**
- `canary/blueprints/auth.py` — session management, landing page
- `canary/blueprints/square_oauth_wired.py` — OAuth flow, token exchange, onboarding pipeline
- `canary/blueprints/merchants_wired.py` — merchant profile/settings REST
- `canary/blueprints/employees_wired.py` — employee REST
- `canary/blueprints/locations_wired.py` — location REST
- `canary/blueprints/identity_mcp.py` — MCP blueprint registration
- `canary/services/identity/tools.py` — MCP tool handlers
- `canary/services/square_oauth.py` — `SquareOAuthService` (token encrypt/store/refresh/revoke)
- `canary/middleware/jwt_auth.py` — `jwt_required`, `role_required`, `roles_required`, `load_session_user`, `has_any_role`

**Inbound contracts:**
- All domains consume `g.merchant_id`, `g.user_id`, `g.roles` set by JWT middleware or session loader.
- RaaS `onboarding.coordinator` writes merchant + oauth records during onboarding.

**Outbound contracts:**
- Square OAuth2 API — token exchange, refresh, revocation.
- Square Merchants API — fetch business name, currency, country during provisioning.
- RaaS `OnboardingCoordinator.run_inline()` — webhook registration + initial sync post-OAuth.
- RaaS `RaaSNamespaceResolver.disconnect_source()` — on token revocation.

## API Contracts

### Auth Blueprint (`/auth`)

| Path | Method | Auth | Description |
|------|--------|------|-------------|
| `/auth/login-page` | GET | Public | Landing page with "Connect with Square" button |
| `/auth/join` | GET | Public | Alias for login-page |
| `/auth/session-logout` | POST | Session | Clear Flask session, redirect to `/auth/join` |
| `/auth/clear-session` | GET | Public | Emergency session reset, redirect to `/auth/join` |
| `/auth/join-interest` | POST | Public (CSRF exempt) | Capture email for beta interest list |
| `/auth/session-login` | POST | Public (CSRF exempt) | Deprecated redirect to login-page |

### OAuth Blueprint (`/oauth`)

| Path | Method | Auth | Description |
|------|--------|------|-------------|
| `/oauth/authorize` | GET | Public | Redirect to Square OAuth consent screen with CSRF state |
| `/oauth/callback` | GET | Public | Exchange auth code for tokens, provision merchant, run onboarding pipeline |
| `/oauth/status` | GET | JWT | Check token connection status and expiry for current merchant |
| `/oauth/refresh` | POST | JWT + admin | Force-refresh access token via Square API |
| `/oauth/disconnect` | POST | JWT + owner/admin | Revoke token and disconnect source |
| `/oauth/sandbox` | GET | Public (sandbox only) | Dev shortcut: store sandbox tokens directly, skip OAuth flow |
| `/oauth/reset-onboarding` | GET | Session (sandbox only) | Factory reset: truncate transactional data, clear session |
| `/oauth/merchant-reset` | POST | Session (sandbox only) | Tenant-scoped reset: delete merchant data, flip onboarded=false |
| `/oauth/factory-reset` | POST | Session (sandbox only) | Full factory reset: truncate all data, flush Valkey |

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

Standard MCP protocol endpoints: `/identity/manifest`, `/identity/tools`, `/identity/tools/<name>`, `/identity/health`. Tools accept `merchant_id` in params or context. All read-only.

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
| merchant_id | String(36) UNIQUE | Square merchant ID |
| merchant_name | String(255) | From Square Merchants API |
| currency | String(3) | Default USD |
| is_active | Boolean | Default true |

Mixins: AuditMixin, SoftDeleteMixin. Access: CRUD. FKs: every tenant-scoped table references merchant_id.

### merchant_settings
Per-merchant configuration. One row per merchant. Drives fiscal calendar for all period metrics and dashboard rendering.

Key columns: timezone, language, date_format, calendar_type (nrf_454 | calendar_month), fiscal_year_start_month, fiscal_week_start_day, fiscal_pattern (4,5,4 etc.), notification prefs (email/sms/in_app, quiet hours, severity threshold, daily limit). Mixins: AuditMixin. Access: CRUD. FK: merchant_id UNIQUE.

### users
User account linked to external IdP (Keycloak). Multi-tenant via user_roles.

Key columns: keycloak_user_id (UNIQUE), username, email, display_name, is_active, last_login_at. Mixins: TenantMixin, AuditMixin, SoftDeleteMixin. Access: CRUD. FKs: merchant_id (primary tenant), referenced by audit_log, alert_history, fox timeline.

### roles
Global RBAC definitions. Not tenant-scoped. Six roles: admin, owner, manager, operator, member, viewer.

Key columns: role_name (UNIQUE), description. Mixins: AuditMixin. Access: read-mostly (seeded).

### user_roles
Tenant-scoped role assignments. A user can hold different roles across merchants.

Key columns: user_id FK -> users.id, role_id FK -> roles.id, merchant_id. Mixins: TenantMixin, AuditMixin. Access: CRUD.

### employees
Staff records synced from Square. Tenant-scoped.

Key columns: square_employee_id, name, email, phone, location_id, is_active, risk_score. Mixins: TenantMixin, AuditMixin. Access: CRUD (sync from Square). FK: merchant_id, location_id -> locations.

### locations
Physical store locations synced from Square.

Key columns: square_location_id, name, address, is_active. Mixins: TenantMixin, AuditMixin. Access: CRUD (sync from Square). FK: merchant_id.

### location_hierarchy
Parent-child location relationships for multi-level retail chains.

Key columns: parent_location_id, child_location_id. Access: CRUD. FKs: both -> locations.id.

### customers
Customer profiles synced from Square. Tenant-scoped.

Key columns: square_customer_id, name, email. Mixins: TenantMixin, AuditMixin. Access: CRUD (sync).

### products
Catalog items synced from Square. Tenant-scoped.

Key columns: square_item_id, name, category, price. Mixins: TenantMixin, AuditMixin. Access: CRUD (sync).

### square_oauth_tokens
Encrypted OAuth credentials. One per merchant. AES-256-GCM encryption at rest.

Key columns: merchant_id (UNIQUE), access_token (encrypted), refresh_token (encrypted), expires_at, scopes. Access: CRUD (managed by SquareOAuthService). FK: merchant_id.

### source_systems
Registry of external data sources (Square, future integrations).

Key columns: source_code (UNIQUE), display_name, is_active. Access: read-mostly (seeded).

### merchant_sources
Junction between merchants and source systems. Tracks connection status and granted scopes.

Key columns: merchant_id, source_code, external_merchant_id, status (active/disconnected), metadata_json (granted_scopes, onboarded flag), disconnected_at. Access: CRUD. FKs: merchant_id, source_code -> source_systems.

## Workflows

### Merchant Onboarding (Square OAuth)

This is the primary entry point for all merchants. No data flows until OAuth completes.

**Step 1: Authorize**
1. Merchant clicks "Connect with Square" on `/auth/join`.
2. `GET /oauth/authorize` generates CSRF state token, stores in session.
3. Redirects to `https://connect.squareup[sandbox].com/oauth2/authorize` with client_id, scopes, state, redirect_uri.
4. Required scopes: MERCHANT_PROFILE_READ, PAYMENTS_READ, ORDERS_READ, EMPLOYEES_READ, TIMECARDS_READ, ITEMS_READ, INVENTORY_READ, GIFTCARDS_READ, CUSTOMERS_READ, CASH_DRAWER_READ.

**Step 2: Callback (token exchange + provisioning)**
1. Square redirects to `GET /oauth/callback` with authorization code and state.
2. CSRF state validation (mismatch -> redirect with error).
3. Exchange code for access_token + refresh_token via `POST /oauth2/token`.
4. `SquareOAuthService.store_token()` encrypts tokens (AES-256-GCM) and writes `square_oauth_tokens`.
5. `_register_square_source()` creates/updates `merchant_sources` record (status: active).
6. `_store_granted_scopes()` writes granted scopes to `merchant_sources.metadata_json`.
7. `_provision_merchant()`:
   - Checks if merchant already exists (returns existing internal UUID if so).
   - Fetches business name, currency, country from Square Merchants API.
   - Creates `Merchant` record (internal UUID generated).
   - Creates `MerchantSettings` with defaults (timezone inferred from country).
8. Commit all writes.

**Step 3: Onboarding Pipeline**
1. `_run_onboarding_pipeline()` calls `OnboardingCoordinator.run_inline()` (best-effort, never blocks OAuth).
2. Coordinator registers Square webhook subscriptions for all event types (payment, order, cash_drawer, inventory, gift_card, loyalty, timecard, dispute).
3. Optional: triggers initial data sync (employees, locations, catalog).
4. Optional: calculates baseline metrics.

**Step 4: Session Creation**
1. If new user (no existing session): set session with user_id=internal_merchant_uuid, roles=[merchant_owner].
2. Admin elevation: if merchant_id is in CANARY_ADMIN_MERCHANTS env var, append admin role.
3. Redirect to `/connect` (onboarding welcome page).

**Onboarding State Machine:**
`not_connected -> authorizing -> connected -> syncing -> active`. Error states: `token_expired -> refreshing -> active`, `token_revoked -> disconnected`, `sync_failed -> error (retry available)`.

### Token Lifecycle

**Refresh:** `SquareOAuthService.refresh_token_flow()` calls Square `POST /oauth2/token` with grant_type=refresh_token. Background job checks `expires_at` proactively. Manual trigger via `POST /oauth/refresh` (admin only).

**Revocation:** `POST /oauth/disconnect` calls `SquareOAuthService.revoke_token()` then `RaaSNamespaceResolver.disconnect_source()` to mark the source as disconnected.

### Session Management

Sessions are stored in Valkey (server-side). Created by OAuth callback, consumed by `load_session_user()` on every browser request.

Session keys: `user_id`, `roles`, `merchant_id`, `merchant_ids`, `organization_id`, `display_name`.

Flask `g` context (set by `load_session_user()` or `jwt_required()`): `g.user_id`, `g.roles`, `g.merchant_id`, `g.merchant_ids`, `g.organization_id`, `g.display_name`.

### JWT Authentication

`@jwt_required` decorator validates Bearer tokens. In keycloak mode: RS256 signature against JWKS (cached 5 min), extracts sub/roles/merchant_id/organization_id. In development mode: accepts any token with admin defaults. API key mode: `X-API-Key` header matching `CANARY_MCP_API_KEY` grants admin access for agent-to-agent calls.

`@role_required(role)` requires exact role. `@roles_required(*roles)` requires ANY listed role. Both abort 403 on mismatch.

### RBAC Role Hierarchy

| Role | Capabilities |
|------|-------------|
| admin | Full access: all CRUD, config, user management, flush sessions |
| owner | Alert disposition, rule config, case management, settings, billing |
| manager | Alert disposition (acknowledge, dismiss), case management |
| operator | Case management, open cases from alerts |
| member | Read-only with limited actions |
| viewer | Read-only access (dashboard only) |

### Token Encryption

All OAuth tokens are encrypted at rest using `canary/utils/crypto.py` (GRO-248).

- **Algorithm:** AES-256-GCM via `cryptography.hazmat.primitives.ciphers.aead.AESGCM`
- **Key source:** `CANARY_ENCRYPTION_KEY` env var (base64-encoded 32 bytes, decoded to raw 256-bit key)
- **Functions:**
  - `encrypt_token(plaintext, key=None)` — returns `"GCM:<base64(nonce + ciphertext + tag)>"`. Nonce is 12 bytes, tag is 16 bytes (appended by GCM mode).
  - `decrypt_token(ciphertext, key=None)` — dispatches by prefix: `GCM:` -> `_decrypt_gcm()`, `UNENCRYPTED:` -> strip prefix, no prefix -> `_decrypt_fernet_legacy()`.
  - `_get_gcm_key()` — decodes `CANARY_ENCRYPTION_KEY` from base64, returns first 32 bytes.
  - `_decrypt_gcm(encoded, key)` — unpacks nonce + ciphertext, decrypts via AESGCM.
  - `_decrypt_fernet_legacy(ciphertext)` — decrypts legacy Fernet-encrypted tokens using the same env key. Migration path: reads Fernet format, `SquareOAuthService` re-encrypts as GCM on next store.
- **Prefix markers:** `"GCM:"` = AES-256-GCM encrypted, `"UNENCRYPTED:"` = plaintext stub (testing only), no prefix = legacy Fernet.
- **Security:** In production (`CANARY_ENV != "testing"`), missing encryption key or missing `cryptography` package raises `RuntimeError`. Plaintext fallback is only allowed when `CANARY_ENV=testing`.
- **Migration:** Transparent. `decrypt_token()` reads any format. On next `store_token()`, `SquareOAuthService` calls `encrypt_token()` which always writes GCM. Legacy Fernet values migrate automatically.

### PII Display Toggle (GRO-242)

`MerchantSettings.show_employee_names` gates employee name display across all routes. When `False`, employee names are masked in API responses, dashboard tables, and alert details. Default: `True`. Toggle exposed via `PUT /api/merchants/settings`.

### Sandbox Shortcuts

`GET /oauth/sandbox` stores sandbox tokens directly without OAuth flow. Provisions merchant, runs onboarding pipeline, creates session. Available only when `SQUARE_ENVIRONMENT=sandbox`.

Reset endpoints (sandbox only): `/oauth/reset-onboarding` (full factory reset), `/oauth/merchant-reset` (tenant-scoped), `/oauth/factory-reset` (full truncate + Valkey flush).
