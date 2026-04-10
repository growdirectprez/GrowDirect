# UI/BFF (Backend for Frontend)

## Overview

The UI/BFF domain owns page rendering, feature flags, app configuration, and the aggregation layer between Canary's backend services and the merchant-facing interface. It reads from all other domains but owns no business data — it is a thin orchestration layer that assembles cross-domain data into renderable payloads.

**Design principle:** The BFF is a data aggregation boundary, not a business logic layer. It fetches from Alert (chirps, stats), Fox (cases), Owl (insights, chat), Analytics (dashboard), Identity (merchant profile), and Chirp (rule metadata) — then shapes the combined payload for the UI. Business decisions happen upstream; the BFF decides what to show and how to show it.

**Rendering:** Flask blueprint `views_bp` in `canary/blueprints/views_wired.py` serves all browser routes. Desktop uses a sidebar layout (`base.html` + `canary.css`); mobile uses a three-panel tab layout (`mobile/base_mobile.html` + `mobile-panels.css`). Desktop routes redirect to mobile equivalents — mobile is the primary merchant interface. All browser routes are gated behind `load_session_user()` session authentication.

**MCP server:** `canary-bff` at `/bff/*` with 4 tools that wrap view helpers into structured JSON. Blueprint in `canary/blueprints/bff_mcp.py`, tool handlers in `canary/services/bff/tools.py`. The MCP interface provides the same data as the browser routes in a machine-readable format for programmatic consumers and the Next.js + Capacitor native app (`frontend/`).

**Native distribution:** The `frontend/` directory contains a Next.js + Capacitor app consuming the Flask API on port 5001. Capacitor enables native iOS/Android distribution via App Store. Auth is JWT Bearer token. Both the server-rendered (Jinja2) and client-rendered (Next.js) paths consume the same BFF aggregation layer.

**Owned tables (app schema):** `feature_flags`, `merchant_feature_flags`, `app_config`, `card_profiles`, `blocked_entities`.

**Services:**

- `config_service.py` — Runtime config editor with three-layer resolution (DB > ENV > default). Secret masking (`is_secret=True` values hidden in UI). Config health dashboard showing set/default/missing status for all registered ENV vars.
- `feature_flags.py` — Feature flag resolution with three-layer chain: merchant override (`merchant_feature_flags`) > global DB default (`feature_flags`) > ENV var fallback. Categories: billing, security, analytics, ui, integration. Per-merchant overrides are rows in `merchant_feature_flags`; deleting the row reverts to global.
- `bff/tools.py` — 4 MCP tool handlers wrapping `_get_chirps()`, `_get_stats()`, `_get_cases()`, and `get_the_one_thing()` from views_wired into JSON payloads.

**Domain boundaries:** Inbound from browser (HTTP) and MCP clients (JWT). Outbound reads to Alert (chirps, stats), Fox (cases), Owl (The One Thing, chat), Analytics (dashboard), Identity (merchant lookup), Chirp (rule metadata). Writes only to its own 5 tables.

## API Contracts

### MCP Server (`canary-bff` at `/bff/*`)

4 tools registered in `canary/services/bff/tools.py`. All follow `(params: Dict, context: Dict) -> Dict` contract. Merchant ID resolved from JWT context or `merchant_id` param.

| Tool | Category | Input | Output |
|------|----------|-------|--------|
| `get_home_data` | aggregation | `merchant_id?`, `show_all?` | Chirps (capped), stats, active/resolved cases, dashboard, The One Thing, severity counts |
| `get_chirp_feed` | aggregation | `merchant_id?`, `show_all?` | Alert feed with severity ordering, counts, cap status |
| `refresh` | aggregation | `merchant_id?` | Lightweight re-fetch: severity counts + The One Thing (no cases/dashboard) |
| `get_feature_flags` | config | `merchant_id?` | All flags with resolved boolean state, source indicator (global/merchant/env) |

**Severity cap logic:** Critical/high/warning alerts always shown. Medium/low/info capped at 4 unless `show_all=true`. Cap applied by `_apply_cap()` helper. Counts computed from full alert set before cap.

### REST Page Routes (`views_bp` at `/` and `/m/*`)

All routes require session auth via `load_session_user()`. Unauthenticated requests redirect to `/auth/login-page?next={path}`.

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

### `feature_flags` — Global feature flag catalog

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

### `merchant_feature_flags` — Per-merchant overrides

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

### `app_config` — Runtime configuration key/value store

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

### `card_profiles` — Card entity profiles

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

### `blocked_entities` — Merchant-configured entity blocks

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
| `templates/base.html` | Desktop sidebar | `canary.css` | Collapsible sidebar (`partials/sidebar.html`) |
| `templates/mobile/base_mobile.html` | Mobile 3-panel | `canary.css` + `mobile-panels.css` | Bottom tab bar (Chirps / Owl / Vault) |

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
| `templates/base.html` | Desktop base template (sidebar layout) |
| `templates/mobile/base_mobile.html` | Mobile base template (3-panel tabs) |
| `templates/mobile/home.html` | Three-panel mobile home (Chirps/Owl/Vault) |
| `static/css/canary.css` | Design tokens + desktop styles |
| `static/css/mobile-panels.css` | Mobile panel/tab styles |
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

---
*Canary LP | GrowDirect Inc. | Confidential*
