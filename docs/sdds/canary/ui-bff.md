# UI/BFF (Backend for Frontend)

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]
**Architecture:** [[docs/sdds/canary/architecture|Canary Architecture SDD]]
**Service type:** App Service (Canary)
**Last reviewed:** 2026-04-13
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[Canary/docs/profiles/ops/Art|Art]] · **Operator role:** [[Canary/docs/profiles/ops/Jeremy|Jeremy]]

## Purpose

The UI/BFF domain owns page rendering, feature flags, app configuration, and the aggregation layer between Canary's backend services and the merchant-facing interface. It reads from all other domains but owns no business data -- it is a thin orchestration layer that assembles cross-domain data into renderable payloads.

**Design principle:** The BFF is a data aggregation boundary, not a business logic layer. It fetches from Alert (chirps, stats), Fox (cases), Owl (insights, chat), Analytics (dashboard), Identity (merchant profile), and Chirp (rule metadata) -- then shapes the combined payload for the UI. Business decisions happen upstream; the BFF decides what to show and how to show it.

## Dependencies

| Dependency | Type | Required | Notes |
|-----------|------|----------|-------|
| PostgreSQL (`canary` DB) | Database | Yes | `app` and `sales` schemas for read queries |
| Valkey (DB 0) | Cache/Session | Yes | Server-side session storage via Flask-Session |
| Alert service | Internal | Yes | `_get_chirps()`, `_get_stats()` -- alert feed + counts |
| Fox service | Internal | Yes | `_get_cases()` -- case lists by status |
| Owl service | Internal | Yes | `get_the_one_thing()` -- AI priority insight |
| Analytics service | Internal | Yes | `_get_dashboard_data()` -- dashboard metrics |
| Identity service | Internal | Yes | Merchant resolution via `_resolve_merchant()` |
| Chirp service | Internal | Yes | Rule metadata via `_build_rule_map()` |
| Square OAuth | External | Yes | Session creation -- BFF has no login flow of its own |

## Data Flow & PII Map

### What enters

| Source | Data | Format |
|--------|------|--------|
| Flask session (Valkey) | `user_id`, `merchant_id`, `roles`, `display_name`, `merchant_ids` | Server-side session dict |
| Alert service | Alert feed with `employee_id`, `employee_name`, `amount_cents`, `rule_id` | Python dicts from ORM |
| Fox service | Case data with `case_number`, employee references | Python dicts |
| Owl service | "The One Thing" AI-generated insight text | String |
| Analytics/Dashboard | Revenue, txn counts, employee-level transaction breakdowns | Python dicts |
| Browser | Form submissions (settings, case status, rule edits), CSRF tokens | POST body |

### What's stored (owned tables, `app` schema)

| Table | PII Fields | Encryption | Classification |
|-------|-----------|------------|----------------|
| `feature_flags` | None | N/A | public |
| `merchant_feature_flags` | `merchant_id` (FK) | Plaintext | internal |
| `app_config` | None (secrets masked via `is_secret`) | Plaintext | internal |
| `card_profiles` | `card_fingerprint`, `card_last4`, `card_brand` | Plaintext | internal |
| `blocked_entities` | `entity_id` (card fingerprint, employee ID, or device ID) | Plaintext | internal |

### What exits (rendered in HTML or returned as JSON)

| Destination | Data | PII Exposure |
|------------|------|-------------|
| Browser HTML | Employee names (masked by PII toggle), card last4, transaction amounts, display_name | internal |
| Browser HTML | `merchant_id` in `<body data-merchant-id>` attribute | internal |
| Browser HTML | `merchant_ids` in `<body data-merchant-ids>` attribute | internal |
| MCP JSON responses | Same aggregated data as HTML, structured as JSON | internal |
| CSRF meta tag | CSRF token in `<meta name="csrf-token">` | public (per-session) |
| Error JSON responses | Exception messages via `str(e)` in some routes | potential leak |

### PII classification

| Field | Classification | Notes |
|-------|---------------|-------|
| `display_name` | internal | Rendered in sidebar, top bar; from session |
| `employee_name` | internal | Masked by PII toggle (`show_employee_names` setting) |
| `card_last4` | internal | PCI-safe (last 4 only); rendered in transaction detail |
| `card_fingerprint` | internal | Square PCI-safe hash; used as entity ID |
| `merchant_id` | internal | Internal UUID; exposed in HTML data attributes |
| `email` | sensitive | Stored in `users` table; rendered on team settings page |
| `user_id` | internal | Session-stored UUID; never rendered in HTML |
| Config secrets | restricted | Masked in config health UI (`is_secret=True` hides value) |

## API Contract

### MCP Server (`canary-bff` at `/bff/*`)

4 tools registered in `canary/services/bff/tools.py`. All follow `(params: Dict, context: Dict) -> Dict` contract. Auth: JWT Bearer token via `@jwt_required` (or `X-API-Key` for agent-to-agent). Merchant ID resolved from JWT context or `merchant_id` param.

| Tool | Category | Input | Output |
|------|----------|-------|--------|
| `get_home_data` | aggregation | `merchant_id?`, `show_all?` | Chirps (capped), stats, active/resolved cases, dashboard, The One Thing, severity counts |
| `get_chirp_feed` | aggregation | `merchant_id?`, `show_all?` | Alert feed with severity ordering, counts, cap status |
| `refresh` | aggregation | `merchant_id?` | Lightweight re-fetch: severity counts + The One Thing (no cases/dashboard) |
| `get_feature_flags` | config | `merchant_id?` | All flags with resolved boolean state, source indicator (global/merchant/env) |

**Severity cap logic:** Critical/high/warning alerts always shown. Medium/low/info capped at 4 unless `show_all=true`. Cap applied by `_apply_cap()` helper. Counts computed from full alert set before cap.

**Rate limiting:** MCP endpoints are rate-limited at 100/hour for manifest/tools-list, 1000/hour for tool invocations (via Flask-Limiter).

### REST Page Routes (`views_bp` at `/` and `/m/*`)

All routes require session auth via `load_session_user()`. Unauthenticated requests redirect to `/auth/login-page?next={path}`. CSRF protection enabled via Flask-WTF `CSRFProtect` (POST/PUT/DELETE).

| Route | Method | Purpose |
|-------|--------|---------|
| `/m/chirps` | GET | Three-panel home (Chirps/Owl/Vault). Default entry point. `?tab=owl` or `?tab=vault` auto-switches panel. `?show=all` bypasses alert cap. |
| `/m/home` | GET | Dashboard pulse page (stats, one thing, case summary) |
| `/m/refresh` | POST | Pull-to-refresh JSON: `{ok, the_one_thing, counts}`. CSRF required. |
| `/m/alert/<id>` | GET | Alert detail page |
| `/m/alert/<id>/action` | POST | Alert action dispatcher (session-auth wrapper) |
| `/m/txn/<id>` | GET | Transaction detail page |
| `/m/case/<num>` | GET | Fox case detail page |
| `/m/case/<num>/status` | POST | Update case lifecycle status |
| `/m/welcome` | GET | First-time onboarding welcome page |
| `/m/welcome/complete` | POST | Mark onboarding complete |
| `/m/owl/chat` | POST | Owl chat (search-first, LLM fallback) |
| `/m/owl/action` | POST | Action dispatcher (session-auth wrapper) |
| `/m/settings` | GET | Settings page |
| `/m/settings/notifications` | POST | Save notification preferences |
| `/m/settings/general` | POST | Save general settings |
| `/m/team` | GET | Team management page |
| `/m/reports` | GET | Reports page (health check results) |
| `/m/rule/<id>` | GET | Rule editor page |
| `/m/rule/<id>/save` | POST | Save rule threshold customization |
| `/m/rule/<id>/reset` | POST | Reset rule to defaults |

**Desktop redirects:** All legacy desktop routes (`/`, `/dashboard`, `/query`, `/chirps`, `/transactions`, `/fox`, `/employees`, `/settings`, `/reports`) redirect to mobile equivalents.

**Admin routes:** `/admin/audit-log`, `/admin/users/*` (CRUD + invite), `/admin/config` (editor + health check).

### Next.js API Consumption (target state)

Next.js app at port 3000 consumes Flask API at port 5001 via `apiGet()`/`apiPost()` with JWT Bearer auth. Key endpoints consumed:

| Endpoint | Method | Next.js Page |
|----------|--------|-------------|
| `/api/alerts/` | GET | Home (Chirps tab) |
| `/api/alerts/<id>` | GET | Alert detail |
| `/owl/one-thing` | POST | Home (Owl tab) |
| `/owl/chat` | POST | Home (Owl tab) |
| `/owl/action` | POST | Alert detail |
| `/api/fox/cases` | GET | Home (Vault tab) |
| `/api/fox/cases/<id>` | GET | Case detail |
| `/api/analytics/dashboard` | GET | Dashboard |
| `/api/chirp/rules` | GET | Chirp config |
| `/api/settings` | GET | Settings |

## Data Models

All tables in `app` schema. Models use SQLAlchemy 2.0 `Mapped[]` syntax.

### `feature_flags` -- Global feature flag catalog

Not tenant-scoped. Each flag defined once, overridden per merchant.

| Column | Type | Notes |
|--------|------|-------|
| `id` | String(36) PK | UUID |
| `flag_key` | String(100) UNIQUE | Canonical key used in code, e.g. `billing_enabled` |
| `flag_name` | String(255) | Human-readable label for UI |
| `description` | Text NULL | Optional description |
| `category` | String(50) | `billing` / `security` / `analytics` / `ui` / `integration` |
| `is_enabled` | Boolean | Global default state (default: false) |
| + AuditMixin | | `created_at`, `updated_at` |

Indexes: `flag_key`, `category`.

### `merchant_feature_flags` -- Per-merchant overrides

Tenant-scoped via TenantMixin (`merchant_id`). Row exists = override active. Delete row to revert to global.

| Column | Type | Notes |
|--------|------|-------|
| `id` | String(36) PK | UUID |
| `merchant_id` | String(36) FK | From TenantMixin |
| `flag_key` | String(100) FK | FK to `feature_flags.flag_key` |
| `is_enabled` | Boolean | Merchant-level override value |
| + AuditMixin | | `created_at`, `updated_at` |

Indexes: unique composite `(merchant_id, flag_key)`.

**Resolution chain:** `is_flag_enabled(merchant_id, flag_key)` checks: (1) `merchant_feature_flags` row for merchant+key, (2) `feature_flags.is_enabled` global default, (3) ENV var fallback via `_ENV_FALLBACKS` dict.

### `app_config` -- Runtime configuration key/value store

Not tenant-scoped. System-wide config overrides.

| Column | Type | Notes |
|--------|------|-------|
| `id` | String(36) PK | UUID |
| `config_key` | String(255) UNIQUE | ENV var name or config key |
| `config_value` | Text NULL | Current value (NULL = use ENV or default) |
| `category` | String(50) | `general` / `database` / `auth` / `square` / `monitoring` / `cms` |
| `description` | Text NULL | Optional description |
| `is_secret` | Boolean | If true, value masked in UI and not editable via config editor |
| + AuditMixin | | `created_at`, `updated_at` |

**Resolution chain:** `get_config_value(key, default)` checks: (1) `app_config.config_value` in DB, (2) `os.environ.get(key)`, (3) registry default from `CONFIG_REGISTRY`, (4) caller default.

### `card_profiles` -- Card entity profiles

Tenant-scoped. Indexed by `card_fingerprint` (Square PCI-safe hash).

| Column | Type | Notes |
|--------|------|-------|
| `id` | String(36) PK | UUID |
| `merchant_id` | String(36) FK | From TenantMixin |
| `card_fingerprint` | String(64) | Square card_fingerprint (PCI-safe) |
| `card_brand` | String(50) NULL | VISA, MASTERCARD, AMEX, etc. |
| `card_last4` | String(4) NULL | Last 4 digits (PCI-safe) |
| `card_prepaid_type` | String(50) NULL | PREPAID, UNKNOWN, or NULL |
| `first_seen_at` | DateTime | First transaction timestamp |
| `last_seen_at` | DateTime | Most recent transaction |
| `transaction_count` | Integer | Completed transaction count |
| `location_count` | Integer | Unique locations used |
| `risk_score` | Float | Chirp aggregate 0.0-1.0 |

Indexes: `(merchant_id, card_fingerprint)`, `(merchant_id, risk_score)`.

### `blocked_entities` -- Merchant-configured entity blocks

Tenant-scoped. Soft-delete via SoftDeleteMixin. Used by Chirp to suppress false positives.

| Column | Type | Notes |
|--------|------|-------|
| `id` | String(36) PK | UUID |
| `merchant_id` | String(36) FK | From TenantMixin |
| `entity_type` | String(50) | `card` / `employee` / `device` |
| `entity_id` | String(100) | card_fingerprint, employee_id, or device_id |
| `reason` | String(500) | Why blocked (lost card, terminated employee, etc.) |
| `blocked_by` | String(36) FK NULL | FK to `users.id` |
| `blocked_at` | DateTime | Block creation timestamp |
| `unblocked_at` | DateTime NULL | When block was lifted |
| + SoftDeleteMixin | | `db_status`, `db_effective_to` |

Indexes: `(merchant_id, entity_type)`, `(merchant_id, entity_type, entity_id)`, `(merchant_id, db_status)`.

## Rendering & Design System

### Template Hierarchy

Two base templates. Do NOT create new base templates.

| Template | Layout | Stylesheet | Navigation |
|----------|--------|------------|------------|
| `templates/app/base_app.html` | Responsive shell (phone/tablet/desktop) | `canary.css` + `mobile-panels.css` + `responsive-shell.css` | Sidebar (desktop/tablet) + bottom tab bar (phone) |

Desktop is sidebar-driven with CSS media query responsive collapse. Mobile is tab-driven: three panels rendered in a single page load, switched by JavaScript (no reload). Active panel set by `.active` CSS class; URL param `?tab=` auto-switches on load.

### Mobile Three-Panel Layout

Default panel: Chirps. Bottom tab bar switches panels client-side.

- **Chirps panel:** Filter chips (All/Critical/Warning/Info) + Owl priority card (The One Thing) + alert cards. Critical/high always shown; medium/low/info capped at 4 unless `?show=all`.
- **Owl panel:** Search input + example chips + loading indicator + dynamic results. The One Thing hero card on load.
- **Vault panel:** Quick links grid (Team, Settings, Reports, Lab) + active Fox cases + resolved cases + logout.

### Pull-to-Refresh

Touch gesture with 80px threshold, 150px max pull. `POST /m/refresh` returns JSON `{ok, the_one_thing, counts: {critical, warning, info, total}}`. JS patches DOM in-place (priority card headline, stat chip counts, badge count). CSRF token required.

### CSS Design Tokens (`canary.css`)

All tokens prefixed `--canary-*`. Key tokens: `--canary-primary` (brand), `--canary-danger` (critical/red), `--canary-warning` (high/amber), `--canary-success` (resolved/green), `--canary-info` (medium/blue), `--canary-surface` (card backgrounds), `--canary-text` (primary text), `--canary-text-muted` (secondary).

Alert severity mapping: critical = `--canary-danger`, high = `--canary-warning`, medium = `--canary-info`, low = `--canary-text-muted`.

### Next.js Design System (Tailwind)

Dark theme with custom color tokens: `ink` (#0D1117 background), `surface` (#161B22 header/nav), `card` (#1C2128), `signal-yellow` (#FBBF24 primary accent), `critical-red` (#F85149), `warning-orange` (#F97316), `health-green` (#3FB950), `owl` (#8B5CF6 purple), `fox` (#F97316 orange).

Typography: Inter (body) + Space Grotesk (headings). Safe areas via `env(safe-area-inset-*)` for Capacitor native shells.

### View Helper Functions

All in `views_wired.py`. No ORM imports at module level (lazy imports inside each helper).

| Function | Purpose |
|----------|---------|
| `_resolve_merchant(merchant_id)` | Maps Square business ID to internal `merchants.id` PK. Caches on `g._merchant_cache`. |
| `_get_chirps(merchant_id)` | Full alert list with category mapping, severity dots, employee resolution. |
| `_get_stats(merchant_id)` | Revenue, txn count, active alerts, health score from app + sales schemas. |
| `_get_cases(merchant_id)` | Fox cases grouped by status (new, in_progress, resolved, etc.). |
| `_get_dashboard_data(merchant_id)` | Dashboard metrics for home aggregation. |
| `_get_activity(merchant_id)` | Audit log entries (last 6) for activity timeline. |
| `_get_settings(merchant_id)` | Merchant settings (general, notifications, integrations). |
| `_time_ago(dt)` | Formats datetime as "2 min ago", "1 hr ago", "3 days ago". |
| `_cents_to_dollars(cents)` | Formats 4250 as "$42.50". |
| `_risk_label(score)` | Converts 0.0-1.0 to "low"/"medium"/"high". |

### Key Files

| File | Purpose |
|------|---------|
| `canary/blueprints/views_wired.py` | All browser routes (mobile + desktop + admin) |
| `canary/blueprints/bff_mcp.py` | BFF MCP blueprint registration |
| `canary/services/bff/tools.py` | 4 MCP tool handlers |
| `canary/services/config_service.py` | Config health + runtime editor |
| `canary/services/feature_flags.py` | Feature flag resolution service |
| `canary/models/app/feature_flags.py` | FeatureFlag, MerchantFeatureFlag, AppConfig models |
| `canary/models/app/card_profiles.py` | CardProfile, BlockedEntity models |
| `templates/app/base_app.html` | Responsive base template (sidebar + tab bar) |
| `templates/app/chirps.html` | Three-panel home (Chirps/Owl/Vault) |
| `static/css/canary.css` | Design tokens + styles |
| `static/css/mobile-panels.css` | Panel/tab styles |
| `static/css/responsive-shell.css` | Responsive breakpoints |
| `frontend/` | Next.js + Capacitor replatform (target state) |

## Settings Page Features

### Theme Picker (GRO-238)

- Settings page theme selector on the General tab
- 4 themes: `canary-dark`, `canary-light`, `whitelabel-dark`, `whitelabel-light`
- Theme loaded via `wsgi.py` context processor (available in all templates)
- CSS tokens defined in `canary/locales/packs/whitelabel.json`
- Theme preference persisted in `MerchantSettings`

### Settings Tabs (GRO-238)

- **Locations tab:** Locations dashboard (existing)
- **General tab:** Theme picker + PII toggle + history window selector
- Tab switching is client-side (no page reload)

### PII Toggle (GRO-242)

- Show/hide employee names across all routes
- Toggle control on the General tab in Settings
- When hidden, employee names replaced with anonymized identifiers
- Setting stored in `MerchantSettings` and respected by all view helpers

### History Window Selector (GRO-258)

- Settings page `lookback_days` selector: 7d / 30d / 90d / All
- Stored in `MerchantSettings.lookback_days` (NULL = all available history)
- Affects connect page initial sync range and welcome page display
- Default: 30 days (backward-compatible with previous hardcoded value)

## Operations

### Startup sequence

The BFF has no independent startup -- it is part of the Canary Flask application (`wsgi.py`). Boot order:

1. `wsgi.py` creates Flask app, loads config from env-specific `Config` class
2. `_init_database()` -- SQLAlchemy session factory, schema verification
3. `_init_security()` -- CSRF, Talisman (CSP/security headers), Flask-Session (Valkey), Flask-Limiter
4. `_register_blueprints()` -- registers `views_bp` (CSRF-protected) and `bff_mcp_bp` (CSRF-exempt, JWT-protected)
5. Context processors inject `csrf_token()`, `csp_nonce()`, theme CSS, and display labels into all templates

### Health checks

- **App-level:** `GET /health` returns basic status (database connectivity, blueprint count)
- **BFF MCP-level:** `GET /bff/health` returns `{service: "canary-bff", healthy: true, tools: 4}`
- **Docker HEALTHCHECK:** Every 30s, `urllib.request.urlopen('http://localhost:5001/health')` -- fails container if app is down

### Failure modes

| Failure | Impact | Behavior |
|---------|--------|----------|
| Valkey down | Sessions lost | New requests get no session, redirect to login. Existing in-flight requests fail. |
| PostgreSQL down | All data queries fail | View helpers return empty lists or "ERR" strings. Pages render with empty state. No crash. |
| Alert/Fox/Owl service error | Partial data | Individual `try/except` blocks return empty results. Page renders with missing sections. |
| CSRF token mismatch | POST rejected | Flask-WTF returns 400. User must reload page. |
| Security extensions fail to init | Degraded | App continues without CSRF, Talisman, rate limiting. Logged as warning. |

### Monitoring

| Metric | Alert threshold | Source |
|--------|----------------|--------|
| 5xx error rate | >5% of requests in 5 min | Application logs |
| `/health` response time | >2s | Docker healthcheck |
| Session creation failures | Any | `canary.jwt_auth` logger |
| CSRF rejection rate | >10% of POSTs | Flask-WTF logs |

### Configuration

**Session settings (wsgi.py):**

| Setting | Value | Notes |
|---------|-------|-------|
| `SESSION_TYPE` | `redis` | Valkey-compatible |
| `SESSION_KEY_PREFIX` | `canary:session:` | Namespace isolation |
| `SESSION_COOKIE_HTTPONLY` | `True` | Prevents JS access to session cookie |
| `SESSION_COOKIE_SAMESITE` | `Lax` | CSRF protection for cross-origin |
| `SESSION_COOKIE_SECURE` | `False` (dev) / `True` (prod) | HTTPS-only in production |
| `PERMANENT_SESSION_LIFETIME` | 7 days | Session expiry |

**Security headers (Talisman):**

| Header | Value |
|--------|-------|
| Content-Security-Policy | `default-src 'self'; script-src 'self' 'unsafe-inline' cdn.jsdelivr.net` with nonce |
| X-Frame-Options | `DENY` |
| X-Content-Type-Options | `nosniff` |
| X-XSS-Protection | `1; mode=block` |
| Strict-Transport-Security | Enabled in production |
| HTTPS forced | Yes (except localhost dev) |

**Feature flags:** Three-layer resolution chain documented in Data Models section. ENV fallbacks: `BILLING_ENABLED`, `AUDIT_LOGGING_ENABLED`, `API_KEYS_ENABLED`.

## Deployment

### Docker service definition

Part of the Canary Docker Compose stack. No separate container -- BFF routes are served by the same Gunicorn process as all Canary Flask routes.

```dockerfile
# Multi-stage build: python:3.12-slim
# Non-root user: canary
# Port: 5001
# Workers: 1 (--threads 4)
# Healthcheck: every 30s against /health
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "1", "--threads", "4", "--timeout", "120", "wsgi:app"]
```

### AWS target

| Component | AWS Service | Notes |
|-----------|------------|-------|
| Application | ECS Fargate | Single task definition for all Canary routes |
| Database | RDS PostgreSQL 17 | Shared `canary` database |
| Sessions | ElastiCache (Valkey) | DB 0 for sessions and cache |
| Secrets | AWS Secrets Manager | Replace `.env` file |
| CDN | CloudFront | Static assets (`/static/`) |
| Load balancer | ALB | TLS termination, health check target `/health` |

### CI/CD requirements

- Build: Docker multi-stage build
- Test gate: `pytest tests/unit/ tests/integration/` must pass
- Static analysis: No `str(e)` in user-facing JSON responses
- Deploy: ECS rolling update (min 1 healthy task)

## Code Review Findings

### F-1: Exception messages leaked in JSON error responses (P1)

**Severity:** P1 (before GA)

**Description:** Multiple routes in `views_wired.py` return `str(e)` directly in JSON error payloads (lines 3516, 3541, 4534). The BFF MCP tool handlers in `tools.py` also return `str(e)` on failure (lines 134, 185, 234). These exception strings can expose internal implementation details -- database table names, query structure, file paths, or dependency names -- to the client.

**Affected code:**
- `views_wired.py` Owl drill route: `return jsonify({"ok": False, "error": str(e)}), 500`
- `views_wired.py` drill entry route: `return jsonify({"ok": False, "error": str(e)}), 500`
- `tools.py` all 4 MCP handlers: `return {"ok": False, "error": str(e)}`

**Recommended fix:** Replace `str(e)` with generic error messages in production. Log the full exception server-side. Pattern: `return {"ok": False, "error": "Internal server error"}` with `logger.error("...", exc_info=True)`.

**Linear issue:** TBD

### F-2: `merchant_id` exposed in HTML data attributes (P2)

**Severity:** P2 (post-launch)

**Description:** `base_app.html` line 35 renders `data-merchant-id="{{ g.merchant_id }}"` and `data-merchant-ids="{{ g.merchant_ids|join(',') }}"` directly into the HTML body tag. These are internal UUIDs. While not secret (they are in session and visible to authenticated users), exposing them in the DOM makes them accessible to any injected script and any browser extension.

**Recommended fix:** Consider whether client-side JavaScript actually needs the full merchant UUID. If needed, a short-lived opaque token or server-side resolution is safer. Alternatively, accept as low risk since pages are behind authentication.

**Linear issue:** TBD

### F-3: CSP allows `'unsafe-inline'` for scripts (P1)

**Severity:** P1 (before GA)

**Description:** The Content-Security-Policy includes `'unsafe-inline'` in `script-src`. While Talisman also adds nonce-based script allowlisting (`content_security_policy_nonce_in=["script-src"]`), the `'unsafe-inline'` directive weakens CSP because browsers that support nonces still allow inline scripts when `'unsafe-inline'` is present alongside a nonce in the CSP. Modern browsers should use nonce-only. However, if inline scripts exist without nonces, removing `'unsafe-inline'` may break functionality.

**Recommended fix:** Audit all inline `<script>` blocks in templates. Add `nonce="{{ csp_nonce() }}"` to any that lack it. Then remove `'unsafe-inline'` from the CSP `script-src` directive. The templates already use `nonce="{{ csp_nonce() }}"` for CDN scripts (Chart.js) but inline event handlers and script blocks in chirps.html, settings.html, and other templates may not have nonces.

**Linear issue:** TBD

### F-4: No audit logging for config or feature flag changes (P1)

**Severity:** P1 (before GA)

**Description:** `config_service.py` `update_config()` and `feature_flags.py` `set_global_flag()`/`set_merchant_flag()`/`remove_merchant_override()` log changes via Python logger but do not write to the audit log table. In production, admin actions that change system behavior (enabling billing, toggling security features, changing runtime config) must produce a queryable audit trail.

**Recommended fix:** Add audit log entries to all write operations in `config_service.py` and `feature_flags.py`. Include: who changed it (`g.user_id`), what changed (key, old value, new value), when (timestamp).

**Linear issue:** TBD

### F-5: No rate limiting on browser view routes (P1)

**Severity:** P1 (before GA)

**Description:** The global Flask-Limiter defaults apply (2000/day, 500/hour), but there are no per-route limits on browser view routes. The `views_bp` blueprint does not apply any route-specific limits. Data-heavy routes like `/m/chirps` (which runs multiple DB queries per request) and `/m/home` (which aggregates across 5+ services) could be abused for resource exhaustion.

**Recommended fix:** Add route-specific limits to data-heavy views. Suggested: `/m/chirps` and `/m/home` at 60/minute, `/m/refresh` at 30/minute, `/m/owl/chat` at 20/minute. MCP endpoints already have limits (100/hour manifest, 1000/hour tools).

**Linear issue:** TBD

### F-6: JWT auth for MCP is dev-mode only (P0)

**Severity:** P0 (blocks prod)

**Description:** The `jwt_required` decorator in `jwt_auth.py` has no production JWT validation. Line 326: `if canary_env == 'production': abort(401)` -- production requests are unconditionally rejected. The dev-mode path compares the Bearer token to a static secret (`CANARY_DEV_JWT_SECRET`). This means: (a) MCP tools cannot work in production, and (b) dev-mode auth is a shared static secret, not per-user tokens.

**Recommended fix:** Implement proper JWT validation for production using a signing key (RS256 or HS256 with rotatable secret). Options: integrate with an identity provider (Keycloak is already in the config registry) or implement JWT signing in the auth service and validation in `jwt_required`. This blocks the Next.js + Capacitor native app from shipping.

**Linear issue:** TBD

### F-7: No data retention policy for owned tables (P1)

**Severity:** P1 (before GA)

**Description:** `card_profiles` and `blocked_entities` have no automated cleanup. `blocked_entities` uses soft-delete (SoftDeleteMixin) but soft-deleted rows are never purged. Over time, these tables will grow unbounded, particularly `card_profiles` which gets a row per unique card per merchant.

**Recommended fix:** Define retention windows: `card_profiles` rows not seen in 12+ months eligible for purge, `blocked_entities` soft-deleted rows purged after 90 days. Implement as a scheduled task or Alembic-managed stored procedure.

**Linear issue:** TBD

### F-8: Security extensions can silently fail (P1)

**Severity:** P1 (before GA)

**Description:** In `wsgi.py` line 451-453, if `_init_security()` throws an exception, the app continues running without CSRF protection, security headers, or rate limiting. The failure is logged as a warning but there is no health check flag or startup abort. In production, running without CSRF or CSP is a security vulnerability.

**Recommended fix:** In production mode (`CANARY_ENV=production`), security extension initialization failure should abort startup. Dev mode can continue with a warning. Add a health check field: `security_extensions_active: bool`.

**Linear issue:** TBD

### F-9: `views_wired.py` is 4500+ lines (P2)

**Severity:** P2 (post-launch)

**Description:** The single file `views_wired.py` contains all browser routes, all view helpers, all admin routes, and all settings handlers. At 4500+ lines it is difficult to review, test in isolation, and reason about. Data helpers (`_get_chirps`, `_get_stats`, etc.) are interleaved with route handlers.

**Recommended fix:** Extract view helpers into `canary/services/bff/` as dedicated modules. Extract admin routes into a separate blueprint. Extract settings routes. Keep `views_wired.py` as the route registration file that delegates to service functions.

**Linear issue:** TBD

### F-10: Session validation fails open on DB error (P2)

**Severity:** P2 (post-launch)

**Description:** In `jwt_auth.py` `load_session_user()` line 425-427, if the DB query to validate the user fails (connection error, timeout), the function falls through to the non-error path and allows the request to proceed with the session data. The comment says "fail open" -- but this means a deactivated user could continue using the app during a DB outage.

**Recommended fix:** In production, fail closed: if user validation query fails, clear the session and redirect to login. This prevents deactivated users from operating during infrastructure issues.

**Linear issue:** TBD

## Production Readiness Checklist

- [x] Session cookies: HttpOnly, SameSite=Lax, Secure in prod
- [x] CSRF protection on all POST routes (Flask-WTF CSRFProtect)
- [x] CSP headers via Talisman (with nonce for scripts)
- [x] X-Frame-Options: DENY
- [x] Health check endpoint responds (`/health`, `/bff/health`)
- [x] PII masking toggle for employee names (GRO-242)
- [x] Config secrets masked in admin UI (`is_secret=True`)
- [x] No-cache headers on HTML responses
- [x] Rate limiting initialized (global defaults)
- [x] Server-side sessions (Valkey, not client-side cookies)
- [x] Non-root Docker user (`canary`)
- [ ] Error responses don't leak internals (F-1: `str(e)` in JSON)
- [ ] CSP tightened: remove `'unsafe-inline'` from script-src (F-3)
- [ ] Audit logging for config/flag changes (F-4)
- [ ] Per-route rate limits on heavy views (F-5)
- [ ] Production JWT validation for MCP tools (F-6)
- [ ] Data retention policy for card_profiles, blocked_entities (F-7)
- [ ] Security init failure aborts prod startup (F-8)
- [ ] Secrets in AWS Secrets Manager (not .env)
- [ ] Session validation fails closed in production (F-10)

---
*Canary LP | GrowDirect Inc. | Confidential*
