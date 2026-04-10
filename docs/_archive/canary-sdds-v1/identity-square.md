# Identity & Square Integration

> **Status:** Complete — written from code
> **Namespace:** canary
> **Last updated:** 2026-03-30
> **Code location:** `Canary/canary/services/identity/`, `Canary/canary/services/parsers/`, `Canary/canary/blueprints/square_oauth_wired.py`, `Canary/canary/services/square_oauth.py`
> **Linear:** GRO-53, GRO-130, GRO-159, GRO-174, GRO-248, GRO-267, GRO-266, GRO-288, GRO-299

---

## 1. Overview

The Identity & Square Integration layer has two distinct responsibilities that are tightly coupled at merchant onboarding time.

**Square OAuth** connects a Square merchant account to Canary. The flow provisions a `Merchant` record (fetching business name and currency from the Square Merchants API), stores AES-256-GCM encrypted OAuth tokens in `square_oauth_tokens`, registers `square` as an active source in `merchant_sources`, persists granted scopes, triggers the onboarding pipeline (webhook subscription + optional initial sync), and provisions a Canary `User` with session state — all as a single callback transaction.

**Identity Resolution (CRDM)** provides a POS-agnostic entity bridge. Every entity that arrives from Square (employees, locations, devices, products, customers) is assigned a Canary UUID as its canonical internal identifier. The `external_identities` table maps those UUIDs to Square's native IDs. Forward resolution (`square_id → Canary UUID`) and reverse resolution (`Canary UUID → square_id`) are provided by pure service functions. This design isolates Square IDs to the identity layer; all downstream services (TSP, Chirp, Owl, Fox) operate on Canary UUIDs.

**Square Parsers** are 16 pure-function modules that normalize raw Square webhook payloads into Python dicts matching the CRDM model columns. They are the exclusive interface between Square's wire format and Canary's internal data model. TSP Sub 2 (`sub2_parse`) dispatches to the appropriate parser for every Square event type it processes, then writes the result to `canary_sales`.

---

## 2. Architecture

### Component Diagram

```
Square API
    |
    |  (1) OAuth redirect / callback
    v
square_oauth_wired.py (Blueprint: /oauth/*)
    |
    |  _provision_merchant()  → app.merchants + app.merchant_settings
    |  SquareOAuthService      → app.square_oauth_tokens (AES-256-GCM)
    |  _register_square_source() → app.merchant_sources
    |  _store_granted_scopes()  → merchant_sources.metadata_json
    |  _run_onboarding_pipeline() → OnboardingCoordinator (async)
    |  _provision_user_on_login() → app.users + session
    v
Flask Session (Valkey DB 0)
    |
    |  (2) Ongoing API calls — token retrieval
    v
SquareOAuthService.get_token()
    |  → auto-refresh via /oauth2/token if expired
    v
Square API (authenticated requests)

    |  (3) Webhook ingestion path
    v
Square Webhook → TSP Sub1 → canary:events (Valkey stream)
    |
    v
TSP Sub2 (sub2_parse.py)
    |
    |  Dispatches by event_type to one of 16 parsers
    v
canary/services/parsers/square_*_parser.py
    |
    |  Returns Python dict
    v
CRDM model row → canary_sales (PostgreSQL)

    |  (4) Identity resolution (any service)
    v
canary/services/identity/external_id_resolver.py
    |
    |  resolve_to_canary()     → app.external_identities
    |  resolve_to_external()   → app.external_identities
    |  register_external_id()  → app.external_identities (upsert)
    |  bulk_register()         → app.external_identities (batch)
    v
Canary UUID  ↔  Square native ID

    |  (5) Identity MCP (agent queries)
    v
identity_mcp.py (Blueprint: /identity/*)
    |  → canary-identity MCP server (6 read-only tools)
    v
Owl / ALX agents
```

### Request / Data Flow

**OAuth Connect (new merchant)**

1. Merchant clicks "Connect with Square" → GET `/oauth/authorize`
2. Blueprint generates CSRF state token, stores in Flask session, redirects to Square consent screen with scopes.
3. Square redirects to GET `/oauth/callback?code=<auth_code>&state=<state>`
4. Blueprint validates CSRF state, exchanges auth code for tokens via POST to Square `/oauth2/token`.
5. `_provision_merchant()`: looks up or creates `Merchant` + `MerchantSettings` (fetches business name + currency from Square Merchants API). Returns internal UUID.
6. `SquareOAuthService.store_token()`: encrypts access and refresh tokens with AES-256-GCM, upserts `square_oauth_tokens`.
7. `_register_square_source()`: upserts `merchant_sources` row with `source_code='square'`, `status='active'`.
8. `_store_granted_scopes()`: persists Square-granted scopes into `merchant_sources.metadata_json`.
9. Session commit.
10. `_run_onboarding_pipeline()`: non-blocking, registers Square webhook subscription and optionally triggers initial catalog sync.
11. `_trigger_first_health_check()`: non-blocking, starts first Owl health check session if merchant has none.
12. `_provision_user_on_login()`: upserts `app.users` row, assigns roles. Sets Flask session (`user_id`, `roles`, `merchant_id`, `display_name`, `theme`).
13. Redirect to `/welcome` (new user) or `/chirps` (returning user).

**Token Retrieval**

Any service that needs a Square access token calls `SquareOAuthService.get_token(merchant_id)`. If `expires_at` is in the past, the service automatically calls `refresh_token_flow()`, which exchanges the stored refresh token for new tokens via the Square `/oauth2/token` refresh grant. New tokens are encrypted and stored before returning.

**Token Revocation (Disconnect)**

POST `/oauth/disconnect` (requires `owner` or `admin` role) calls `SquareOAuthService.revoke_token()`, which calls Square `/oauth2/revoke` (best-effort) and then deletes the local `square_oauth_tokens` row regardless of Square API result. `_disconnect_square_source()` marks the `merchant_sources` row `status='disconnected'`.

**Parser Invocation (TSP Sub2)**

TSP Sub 2 reads messages from the `canary:events` Valkey stream. For each message it:
1. Extracts `event_type` and `raw_payload` (JSON string).
2. Routes to the registered parser via the webhook dispatch registry.
3. Calls the pure parser function with the deserialized payload dict.
4. Receives a Python dict whose keys match a CRDM model's column names.
5. Instantiates the SQLAlchemy model and writes to `canary_sales`.
6. Publishes to the detection stream if the route has a `detection_type`.

**Identity Resolution**

When TSP Sub 2 or any service encounters a Square entity ID (e.g., a team member ID from a payment tender), it calls `register_external_id()` to create or update the mapping, and `resolve_to_canary()` to retrieve the Canary UUID for downstream writes.

### Key Design Decisions

| Decision | Rationale |
|---|---|
| Internal UUID is canonical (GRO-237) | Square IDs are source-system artifacts. All FK references, links, cache keys, and drill paths use `merchants.id` (UUID), never `source_merchant_id`. |
| AES-256-GCM for token encryption (GRO-248) | Upgrade from Fernet. GCM provides authenticated encryption. Legacy Fernet tokens are transparently decrypted and re-encrypted on next store. |
| OAuth callback is best-effort for non-critical steps | `_register_square_source`, `_store_granted_scopes`, `_run_onboarding_pipeline`, `_trigger_first_health_check` all catch exceptions and log warnings rather than aborting the OAuth flow. The token store and merchant provisioning are the only hard requirements. |
| Parsers are pure functions | No database access, no Flask context, no side effects. Input: raw payload dict. Output: CRDM dict. This makes them independently testable and reusable in both webhook and initial-sync paths. |
| CRDM pattern for entity identity | `external_identities` decouples the parser layer from specific source systems. A future Clover integration adds a new `source_code` row in `source_systems` and populates `external_identities` — no schema changes to any entity table. |
| Privacy-first parsers | `parse_customer` stores no PII (no name, email, phone, address). `parse_loyalty_account` hashes phone numbers with SHA-256. `parse_card` omits cardholder name and billing address. |
| Sandbox shortcut route | `/oauth/sandbox` bypasses the OAuth consent flow entirely for development, reading tokens from environment variables. Guarded by `SQUARE_ENVIRONMENT != sandbox` check. |

---

## 3. Data Model

All tables are in the `app` schema unless noted. All models use SQLAlchemy 2.0 `Mapped[]` syntax.

### SquareOAuthToken (`app.square_oauth_tokens`)

Stores AES-256-GCM encrypted Square OAuth tokens. One row per merchant.

```python
class SquareOAuthToken(AppBase, TenantMixin, AuditMixin):
    __tablename__ = "square_oauth_tokens"

    id: Mapped[str]                                  # UUID PK
    # from TenantMixin:
    merchant_id: Mapped[str]                         # FK → merchants.id (internal UUID)
    access_token_encrypted: Mapped[str]              # AES-256-GCM ciphertext, never null
    refresh_token_encrypted: Mapped[Optional[str]]   # AES-256-GCM ciphertext, null if non-renewable
    token_type: Mapped[str]                          # default 'bearer'
    expires_at: Mapped[Optional[datetime]]           # UTC expiry; null = never expires
    scopes: Mapped[str]                              # comma-separated granted scopes
    # from AuditMixin:
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

Index: `idx_square_oauth_tokens_merchant_id` on `merchant_id`.

### MerchantSource (`app.merchant_sources`)

Registry of which data sources a merchant has authorized. One row per `(merchant_id, source_code)` pair.

```python
class MerchantSource(AppBase, TenantMixin, AuditMixin):
    __tablename__ = "merchant_sources"

    id: Mapped[str]                              # UUID PK
    merchant_id: Mapped[str]                     # FK → merchants.id (from TenantMixin)
    source_code: Mapped[str]                     # FK → source_systems.code (e.g. 'square')
    external_merchant_id: Mapped[Optional[str]]  # Square's merchant_id string
    connected_at: Mapped[datetime]               # server_default=now()
    disconnected_at: Mapped[Optional[datetime]]  # set on revoke; null = active
    status: Mapped[str]                          # pending|active|disconnected|expired
    raas_namespace: Mapped[Optional[str]]        # RaaS Valkey key prefix (opt-in tier)
    metadata_json: Mapped[Optional[str]]         # JSON: granted_scopes, scopes_updated_at
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

Unique index: `idx_ms_merchant_source` on `(merchant_id, source_code)`.

### SourceSystem (`app.source_systems`)

Reference table for POS/EHR/IoT identifiers. Primary key is the code string. Updated by INSERT — no schema changes needed to add a new source.

```python
class SourceSystem(AppBase, AuditMixin):
    __tablename__ = "source_systems"

    code: Mapped[str]                    # PK — e.g. 'square', 'clover', 'toast'
    display_name: Mapped[str]            # human-readable UI label
    category: Mapped[str]                # pos|ehr|logistics|iot|financial|identity|manual
    is_active: Mapped[bool]              # soft-disable; inactive sources reject new events
    description: Mapped[Optional[str]]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

### ExternalIdentity (`app.external_identities`)

Junction table: Canary entity UUID ↔ source system ID. One row per `(merchant, entity, source_system)` combination.

```python
ENTITY_TYPES = ("employee", "location", "device", "product", "customer")

class ExternalIdentity(AppBase, TenantMixin, AuditMixin):
    __tablename__ = "external_identities"

    id: Mapped[str]          # UUID PK
    merchant_id: Mapped[str] # FK → merchants.id (from TenantMixin)
    entity_type: Mapped[str] # CHECK: employee|location|device|product|customer
    entity_id: Mapped[str]   # Canary UUID for this entity
    source_code: Mapped[str] # FK to source_systems.code (e.g. 'square')
    external_id: Mapped[str] # Square's native ID for this entity
    is_primary: Mapped[bool] # True = this source is authoritative for this entity
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

Constraints:
- `uq_ext_id_merchant_source_entity`: UNIQUE `(merchant_id, source_code, entity_type, external_id)` — prevents duplicate forward mappings.
- `uq_ext_id_merchant_entity_source`: UNIQUE `(merchant_id, entity_type, entity_id, source_code)` — prevents duplicate reverse mappings.
- `ck_ext_id_entity_type`: CHECK `entity_type IN ('employee', 'location', 'device', 'product', 'customer')`.

Indexes:
- `ix_ext_id_lookup`: `(merchant_id, source_code, entity_type, external_id)` — forward resolution path.
- `ix_ext_id_reverse`: `(merchant_id, entity_type, entity_id)` — reverse resolution path.

---

## 4. Interfaces

### OAuth Blueprint (`/oauth/*`)

Registered as `square_oauth_bp` in `canary/blueprints/square_oauth_wired.py`.

| Route | Method | Auth | Purpose |
|---|---|---|---|
| `/oauth/authorize` | GET | None | Redirect to Square consent screen |
| `/oauth/callback` | GET | None (CSRF state) | Exchange auth code for tokens; provision merchant + user |
| `/oauth/status` | GET | JWT required | Return connection status and token expiry |
| `/oauth/refresh` | POST | JWT + admin role | Force-refresh access token |
| `/oauth/disconnect` | POST | JWT + owner/admin role | Revoke token, mark source disconnected |
| `/oauth/sandbox` | GET | None (sandbox only) | Dev shortcut: store env tokens directly |
| `/oauth/reset-onboarding` | GET | Session + admin role | Sandbox factory reset (truncate transactional data) |
| `/oauth/merchant-reset` | POST | Session auth | Sandbox tenant-scoped reset |
| `/oauth/factory-reset` | POST | Session auth | Sandbox full factory reset |

**OAuth callback response contract:**
- On success → HTTP 302 to `/welcome` (new user) or `/chirps` (returning user).
- On CSRF mismatch → HTTP 302 to `/auth/login-page?error=oauth_csrf_mismatch`.
- On Square error → HTTP 302 to `/settings?error=<error>`.
- On token exchange failure → HTTP 302 to `/auth/login-page?error=token_exchange_failed`.

**Status route JSON response:**
```json
{
  "connected": true,
  "expires_at": "2026-04-29T00:00:00+00:00",
  "merchant_id": "<uuid>"
}
```

### Square Explorer Blueprint (`/explore/*`)

Registered as `square_explorer_bp` in `canary/blueprints/square_explorer_wired.py`. Sandbox-only (all requests blocked with 403 in production via `before_request` guard).

| Route | Method | Purpose |
|---|---|---|
| `/explore/<api_family>` | GET | Return JSON from Square capability explorer |
| `/explorer` | GET | Legacy — 301 redirect to `/ops/explorer` |

### Identity MCP Blueprint (`/identity/*`)

Registered as `identity_mcp_bp` in `canary/blueprints/identity_mcp.py`. Exposes the `canary-identity` MCP server (version 0.1.0) for agent consumption. All tools are DB-read only.

| Tool | Category | Required params | Optional params | Returns |
|---|---|---|---|---|
| `get_merchant` | merchant | `merchant_id` | — | name, business_name, email, phone, created_at |
| `get_settings` | merchant | `merchant_id` | — | timezone, currency, language, notification_preferences, label_overrides |
| `list_employees` | employee | `merchant_id` | `location_id`, `is_active` | employees[], count |
| `get_employee` | employee | `merchant_id`, `employee_id` | — | id, name, email, phone, location_id, is_active, risk_score |
| `list_locations` | location | `merchant_id` | — | locations[], count |
| `get_location` | location | `merchant_id`, `location_id` | — | id, name, address, square_location_id, is_active |

`merchant_id` may be supplied via `params` or inherited from `context`. All tools return `{"tool": "<name>", "ok": true|false, "result": {...}, "timestamp": "<iso>"}`.

---

## 5. Service Layer

### SquareOAuthService (`canary/services/square_oauth.py`)

Manages Square OAuth token lifecycle. Initialized per-request with a SQLAlchemy session.

```python
class SquareOAuthService:
    def __init__(self, db_session: Session, encryption_key: str = None)
    def store_token(merchant_id, access_token, refresh_token=None, expires_at=None) -> None
    def get_token(merchant_id) -> Optional[Dict]           # auto-refreshes if expired
    def refresh_token_flow(merchant_id) -> Dict            # explicit refresh
    def revoke_token(merchant_id) -> bool                  # revoke at Square + delete local
```

`get_token` returns `{"access_token": str, "expires_at": datetime, "merchant_id": str}` or `None` if no token exists.

`refresh_token_flow` raises `ValueError` if no refresh token is stored or if Square rejects the refresh request.

Encryption uses `canary.utils.crypto.encrypt_token` / `decrypt_token` (AES-256-GCM, key from `_get_gcm_key()`). The service transparently handles legacy Fernet-encrypted tokens in `decrypt_token`. If no encryption key is configured, tokens are stored with a plaintext prefix (logged as a warning).

### external_id_resolver (`canary/services/identity/external_id_resolver.py`)

Pure service functions — no Flask context, no HTTP calls. All take a SQLAlchemy `Session` as first argument.

```python
def resolve_to_canary(
    session: Session,
    merchant_id: str,
    source_code: str,
    entity_type: str,
    external_id: str,
) -> Optional[str]
```
Forward resolution: returns Canary entity UUID or `None` if no mapping exists. Uses `ix_ext_id_lookup` index.

```python
def resolve_to_external(
    session: Session,
    merchant_id: str,
    entity_type: str,
    entity_id: str,
    source_code: str = None,
) -> list[dict]
```
Reverse resolution: returns list of `{"source_code": str, "external_id": str, "is_primary": bool}`. Optionally filtered by `source_code`.

```python
def register_external_id(
    session: Session,
    merchant_id: str,
    entity_type: str,
    entity_id: str,
    source_code: str,
    external_id: str,
    is_primary: bool = True,
) -> ExternalIdentity
```
Upsert: if a mapping for `(merchant, entity_type, entity_id, source_code)` already exists, updates `external_id` and `is_primary` in place. Otherwise creates a new row. Idempotent.

```python
def bulk_register(
    session: Session,
    merchant_id: str,
    source_code: str,
    mappings: list[dict],   # each: {entity_type, entity_id, external_id}
) -> int
```
Batch registration for initial sync. Skips existing mappings. Returns count of new records created.

### Square Parsers (`canary/services/parsers/`)

All parsers are pure functions: `parse_<entity>(payload: dict) -> dict`. Input is the raw Square webhook payload dict (already JSON-decoded). Output is a Python dict whose keys match the target CRDM model's column names. Every parser generates a new UUID (`str(uuid.uuid4())`) for the Canary `id` field.

Square V2 webhooks nest the entity under `data.object.<entity_key>`. All parsers support both webhook format (`data.object.<type>`) and flat initial-sync format (`data.object` directly) via the pattern `obj.get("<type>") or obj`.

| Parser module | Function(s) | Event types handled | Target model(s) |
|---|---|---|---|
| `square_payment_parser` | `parse_payment(payload)`, `parse_refund(payload)` | `payment.*`, `refund.*` | `Transaction`, `RefundLink` |
| `square_order_parser` | `parse_order(payload)`, `parse_order_line_items(payload)`, `parse_order_tenders(payload)`, `parse_order_discounts(payload, txn_id, merchant_id)`, `parse_order_taxes(payload, txn_id, merchant_id)`, `parse_order_modifiers(payload, txn_id, merchant_id)`, `parse_order_service_charges(payload, txn_id, merchant_id)`, `parse_order_rewards(payload, txn_id, merchant_id)`, `parse_order_returns(payload, txn_id, merchant_id)` | `order.*` | `Transaction`, `OrderLineItem`, `OrderTender`, `OrderDiscount`, `OrderTax`, `OrderModifier`, `OrderServiceCharge`, `OrderReward`, `OrderReturn` |
| `square_customer_parser` | `parse_customer(payload)` | `customer.created`, `customer.updated` | `Customer` |
| `square_location_parser` | `parse_location(payload)` | `location.created`, `location.updated` | `Location` |
| `square_device_parser` | `parse_device(payload)` | `device.created`, `device.updated` | `Device` |
| `square_card_parser` | `parse_card(payload)` | `card.created`, `card.updated`, `card.disabled` | `CardProfile` |
| `square_team_member_parser` | `parse_team_member(payload)` | `team_member.created`, `team_member.updated` | `Employee` |
| `square_invoice_parser` | `parse_invoice(payload)` | `invoice.*` | `Invoice` |
| `square_loyalty_parser` | `parse_loyalty_account(payload)`, `parse_loyalty_event(payload)` | `loyalty.account.*`, `loyalty.event.created` | `LoyaltyAccount`, `LoyaltyEvent` |
| `square_gift_card_parser` | `parse_gift_card(payload)` | `gift_card.created`, `gift_card.updated`, `gift_card.customer_linked`, `gift_card.customer_unlinked` | `GiftCard` |
| `square_subscription_parser` | `parse_subscription(payload)` | `subscription.created`, `subscription.updated` | `Subscription` |
| `square_dispute_parser` | `parse_dispute(payload)` | `dispute.created`, `dispute.state.changed`, `dispute.state.updated` | `Dispute` |
| `square_payout_parser` | `parse_payout(payload)` | `payout.paid`, `payout.sent`, `payout.failed` | `Payout` |
| `square_bank_account_parser` | `parse_bank_account(payload)` | `bank_account.created`, `bank_account.updated`, `bank_account.verified`, `bank_account.disabled` | `BankAccount` |
| `square_terminal_parser` | `parse_terminal_checkout(payload)`, `parse_terminal_refund(payload)` | `terminal.checkout.*`, `terminal.refund.*` | `TerminalCheckout`, `TerminalRefund` |
| `square_transfer_order_parser` | `parse_transfer_order(payload)` | `transfer_order.created`, `transfer_order.updated` | `TransferOrder` |
| `square_auxiliary_parsers` | `parse_cash_drawer_shift(payload)`, `parse_cash_drawer_event(payload)`, `parse_timecard(payload)`, `parse_inventory_adjustment(payload)`, `parse_gift_card_activity(payload)` | `cash_drawer.*`, `labor.shift.*`, `inventory.*`, `gift_card_activity.*` | `CashDrawerShift`, `CashDrawerEvent`, `Timecard`, `InventoryAdjustment`, `GiftCardActivity` |

#### Parser details of note

**`parse_payment`** — Most complex parser. Extracts 35+ fields including card details (`fingerprint`, `brand`, `last4`, `card_type`, `bin`, `exp_month`, `exp_year`), risk evaluation, processing fees, application details, offline payment flag, and CVV/AVS statuses. Derives `transaction_type` (SALE / RETURN / VOID / POST_VOID / NO_SALE) and `cancel_context` (IMMEDIATE_VOID / MANAGER_VOID / EXPIRED_HOLD / TIMEOUT_VOID) from payment status, capabilities, delay action, and timing gap. Handles Square's ISO 8601 / RFC 3339 timestamps including `Z`-suffixed strings.

**`parse_order`** — `employee_id` is set to `None`; TSP Sub 2's `_build_models()` backfills it from order tenders' `team_member_id` after parsing. The nine child-object parsers (`parse_order_line_items`, etc.) accept the raw order payload and return lists of dicts for batch insert.

**`parse_team_member`** — Handles location assignment variants: `ALL_CURRENT_AND_FUTURE_LOCATIONS` sets `all_locations=True`; specific assignments populate `assigned_location_ids` list. PII note: `email_address` is extracted as `email` (display decoration); `square_employee_id` is the relational key.

**`parse_loyalty_account`** — Hashes phone number with SHA-256 before storing as `phone_hash`. Raw phone is never written to the database.

**`parse_loyalty_event`** — Point values are positive for accumulations (`ACCUMULATE_POINTS`, `ADJUST_POINTS`) and negative for redemptions and expirations (`REDEEM_REWARD`, `EXPIRE_POINTS`). `linked_transaction_id` is set to `None` at parse time; TSP Sub 2 resolves it from `order_id` during model building.

**`parse_gift_card_activity`** — Resolves `order_id` and `payment_id` from the type-specific sub-object (e.g., `redeem_activity_details`, `load_activity_details`). `linked_transaction_id` is set to `None` at parse time; resolved by TSP Sub 2 from `payment_id`.

**`parse_auxiliary_parsers`** — The five functions in this module (`parse_cash_drawer_shift`, `parse_cash_drawer_event`, `parse_timecard`, `parse_inventory_adjustment`, `parse_gift_card_activity`) share the module to reduce file count for lower-frequency event types.

---

## 6. Configuration

| Environment variable | Purpose | Required |
|---|---|---|
| `SQUARE_APPLICATION_ID` | Square OAuth app client ID | Yes |
| `SQUARE_APPLICATION_SECRET` | Square OAuth app client secret | Yes |
| `SQUARE_REDIRECT_URL` | OAuth callback URI override | No (falls back to `CANARY_DOMAIN/oauth/callback`) |
| `SQUARE_ENVIRONMENT` | `sandbox` or `production` | Yes |
| `SQUARE_ACCESS_TOKEN` | Sandbox access token (sandbox shortcut only) | Sandbox only |
| `SQUARE_MERCHANT_ID` | Sandbox merchant ID (sandbox shortcut only) | Sandbox only |
| `CANARY_DOMAIN` | Base domain for redirect URI construction | Yes (prod) |
| `CANARY_ADMIN_MERCHANTS` | Comma-separated Square merchant IDs that receive automatic admin elevation | No |
| `TOKEN_ENCRYPTION_KEY` | AES-256-GCM key for token encryption (via `canary.utils.crypto._get_gcm_key()`) | Yes (prod) |
| `DATABASE_URL` | `postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/canary` | Yes |
| `VALKEY_URL` | `redis://growdirect_valkey:6379/0` | Yes |

Requested OAuth scopes (hardcoded in `square_oauth_wired.py`):

```
MERCHANT_PROFILE_READ
PAYMENTS_READ
ORDERS_READ
EMPLOYEES_READ
TIMECARDS_READ
ITEMS_READ
INVENTORY_READ
GIFTCARDS_READ
CUSTOMERS_READ
CASH_DRAWER_READ
```

---

## 7. Security & Compliance

### OAuth Token Encryption

Access tokens and refresh tokens are encrypted at rest using AES-256-GCM (`GRO-248`). The `SquareOAuthService._encrypt()` and `._decrypt()` methods delegate to `canary.utils.crypto.encrypt_token` / `decrypt_token`. The GCM key is loaded from the environment via `canary.utils.crypto._get_gcm_key()`.

Legacy tokens encrypted with Fernet (prior to GRO-248) are transparently handled by `decrypt_token`. On the next `store_token()` call, the token is re-encrypted as AES-256-GCM.

If no encryption key is configured (development fallback), the service logs a warning and stores tokens with a plaintext prefix. This must never occur in production.

### CSRF Protection

The OAuth authorize → callback round trip is protected by a state token. `generate_csrf_token()` produces a cryptographically random string stored in the Flask session under `square_oauth_state`. The callback validates the returned `state` parameter against the session value before proceeding. Mismatch redirects to login with `error=oauth_csrf_mismatch`.

### PCI Awareness

The parsers follow a strict PCI-safe extraction policy:
- `parse_card`: extracts fingerprint, brand, last4, card_type, prepaid_type, enabled status, and customer_id. Does NOT extract cardholder name or billing address.
- `parse_payment`: extracts CVV status and AVS status as metadata fields; does NOT store raw card numbers at any point (Square never sends them).
- Full card data never transits Canary — Square's tokenization layer handles that.

### Privacy Enforcement

- `parse_customer`: stores only `square_customer_id` and timestamps. No name, email, phone, or address fields are extracted.
- `parse_loyalty_account`: phone number is hashed with SHA-256 before storage (`phone_hash`). Raw phone is discarded.
- `parse_team_member`: `email_address` is extracted as display decoration only. PII stored is minimal; `square_employee_id` is the relational key.

### Square Webhook Signature Validation

Square webhook payloads are authenticated using HMAC-SHA256 signature validation in TSP Sub 1 (the ingestion layer, not documented in this SDD). By the time a payload reaches the parsers in TSP Sub 2, it has already passed signature validation and been committed to the `canary:events` Valkey stream. The parsers themselves perform no additional signature checks.

### Role-Based Access Controls

- `GET /oauth/status`: JWT required (`@jwt_required`).
- `POST /oauth/refresh`: JWT + `admin` role.
- `POST /oauth/disconnect`: JWT + `owner` or `admin` role.
- Identity MCP tools: read-only, no destructive operations. Write operations remain in the REST blueprints.
- Sandbox reset routes: guarded by `SQUARE_ENVIRONMENT == 'sandbox'` check and session admin role.

---

## 8. Error Handling

### OAuth Flow — Best-Effort Helpers

The OAuth callback categorizes errors into hard failures (abort the flow) and soft failures (log and continue):

**Hard failures — redirect to error page:**
- CSRF state mismatch
- Square returns `error` parameter in callback
- Missing `code` in callback query string
- Token exchange returns non-200 status

**Soft failures — log warning, continue:**
- `_provision_merchant()`: if Square Merchants API fails, falls back to `business_name="New Merchant"`, `currency="USD"`. If merchant provisioning itself fails entirely, `data_merchant_id` falls back to the raw Square merchant ID string (UUID-less path — this is a degraded state and will cause FK issues; monitoring should alert on this).
- `_register_square_source()`: catch-all exception handler, logs warning.
- `_store_granted_scopes()`: catch-all exception handler, logs warning.
- `_run_onboarding_pipeline()`: catch-all exception handler, logs warning.
- `_trigger_first_health_check()`: catch-all exception handler, logs warning.

### SquareOAuthService

- `get_token()`: returns `None` if no token record exists. Transparent auto-refresh if expired.
- `refresh_token_flow()`: raises `ValueError` on missing refresh token or Square rejection. Callers must handle this.
- `revoke_token()`: always deletes the local token row regardless of whether the Square revoke API call succeeds (best-effort at Square).
- Encryption init: logs warning if `TOKEN_ENCRYPTION_KEY` is absent; does not raise.

### Parsers

All parsers follow a consistent defensive pattern:
- `payload.get("key", {})` with empty-dict defaults for nested objects to avoid `AttributeError` on missing keys.
- `or {}` and `or []` guards on optional sub-objects.
- ISO 8601 parsing with try/except; falls back to `None` or `datetime.now(timezone.utc)`.
- Missing required fields (e.g., `square_customer_id`) log a `logger.warning` but do not raise — the parser still returns a valid (partial) dict to avoid dropping events.
- `parse_timecard` returns `None` if required fields are missing; TSP Sub 2 must check for None return.

### identity_mcp tools

All tool handlers wrap the database query in try/except. On exception, they return `{"ok": False, "error": str(e), "timestamp": "..."}`. The MCP server does not raise HTTP errors; consumers check the `ok` field.

---

## 9. Testing

### Unit Tests

Parser unit tests live in `Canary/tests/unit/`. One test file per parser module:

| Test file | Parser module tested |
|---|---|
| `test_square_parsers.py` | `square_payment_parser` (payment + refund) |
| `test_order_child_parser.py` | `square_order_parser` (all 9 functions) |
| `test_customer_parser.py` | `square_customer_parser` |
| `test_location_parser.py` | `square_location_parser` |
| `test_device_parser.py` | `square_device_parser` |
| `test_card_parser.py` | `square_card_parser` |
| `test_team_member_parser.py` | `square_team_member_parser` |
| `test_invoice_parser.py` | `square_invoice_parser` |
| `test_loyalty_parser.py` | `square_loyalty_parser` |
| `test_gift_card_parser.py` | `square_gift_card_parser` |
| `test_subscription_parser.py` | `square_subscription_parser` |
| `test_dispute_parser.py` | `square_dispute_parser` |
| `test_payout_parser.py` | `square_payout_parser` |
| `test_bank_account_parser.py` | `square_bank_account_parser` |
| `test_terminal_parser.py` | `square_terminal_parser` |
| `test_transfer_order_parser.py` | `square_transfer_order_parser` |

`test_external_identities.py` covers the `ExternalIdentity` model structure and `external_id_resolver` import assertions.

### Test Approach

Parsers are pure functions, so unit tests use simple `assert` on dict key presence and value correctness without any database setup. Test payloads must be fully populated (no null shortcuts — platform standard from `feedback_fully_populate_data.md`).

Critical assertions for each parser:
1. Output `id` is a valid UUID string.
2. `merchant_id` is propagated from the top-level payload.
3. The entity's Square ID is extracted correctly from `data.object.<type>` (webhook format).
4. Monetary amounts are extracted from nested `*_money.amount` sub-objects.
5. Privacy fields (PII) are absent from the output dict.

For the identity resolver, integration tests (requires `canary_test` database) verify:
- `register_external_id` is idempotent (second call returns same row, updated values).
- `resolve_to_canary` returns correct UUID.
- `resolve_to_external` returns list with correct shape.
- `bulk_register` skips existing and returns correct new count.

### Running

```bash
# All parser unit tests (no DB required)
python3 -m pytest tests/unit/ -k "parser" -v

# External identity model + resolver imports
python3 -m pytest tests/unit/test_external_identities.py -v

# Full unit suite
python3 -m pytest tests/unit/ -v

# Integration tests (requires canary_test DB)
python3 -m pytest tests/integration/ -m postgres -v
```

---

## 10. Dependencies

### Upstream

| Dependency | Purpose |
|---|---|
| Square OAuth API (`/oauth2/authorize`, `/oauth2/token`, `/oauth2/revoke`) | Token issuance, refresh, revocation |
| Square Merchants API (`GET /v2/merchants/<id>`) | Business name + currency fetch during merchant provisioning |
| Square Webhooks (all event types) | Raw payload delivery to TSP Sub 1 |
| `canary.utils.crypto` | AES-256-GCM encrypt/decrypt for token storage |
| `canary.middleware.jwt_auth._provision_user_on_login` | User provisioning + role assignment at OAuth callback |

### Downstream

| Service | Consumes |
|---|---|
| TSP (all subsystems) | `SquareOAuthService.get_token()` for authenticated Square API calls |
| TSP Sub 2 (`sub2_parse`) | All 16 parser modules; invokes the appropriate parser for every event type |
| Chirp | Customer aggregate metrics seeded by `parse_customer`; employee risk scores from `app.employees` |
| Owl | Merchant/employee/location data via Identity MCP tools (`get_merchant`, `list_employees`, `list_locations`, etc.) |
| Fox | Dispute records produced by `parse_dispute` |
| OnboardingCoordinator | Called from OAuth callback via `_run_onboarding_pipeline()` |
| RaaSNamespaceResolver | Called from OAuth disconnect via `_disconnect_square_source()` |
| Health check runner | Called from OAuth callback via `_trigger_first_health_check()` |

### Shared Infrastructure

| Component | Usage |
|---|---|
| `growdirect_postgres:5432` | `canary` database — `app.square_oauth_tokens`, `app.merchant_sources`, `app.source_systems`, `app.external_identities`, `app.merchants` |
| `growdirect_valkey:6379/0` | Flask session storage (merchant_id, user_id, roles, theme); `canary:events` stream (TSP) |
| Flask session | Carries `square_oauth_state` (CSRF), `merchant_id`, `user_id`, `roles`, `display_name`, `theme` between OAuth redirect and callback |

---

## 11. Known Issues & Reconciliation

### Degraded merchant provisioning path

If `_provision_merchant()` encounters an exception and returns `None`, the callback falls back to using the raw Square merchant ID string as `data_merchant_id`. This string cannot satisfy FK constraints that reference `merchants.id` (a UUID). In practice this means `store_token` will fail with an FK violation or silently write a bad merchant_id. This path should be treated as a hard failure. GRO issue recommended to add an explicit guard and redirect to error on `internal_id is None`.

### Sandbox shortcut bypasses scope collection

The `/oauth/sandbox` route passes `SQUARE_SCOPES.split()` to `_store_granted_scopes` rather than scopes granted by the actual token. In production sandbox testing, the stored `metadata_json` scopes may not reflect what the sandbox token actually supports. Acceptable for development; would need fixing before any scope-gated feature is tested in sandbox.

### `parse_order.employee_id` is always `None` from parser

Order events do not carry a `team_member_id` at the order level in Square's V2 format. The employee is in the tenders array. TSP Sub 2's `_build_models()` backfills `employee_id` from tenders after parsing. If a transaction has tenders with no `team_member_id`, TSP Sub 2 calls `_lookup_primary_employee()` (GRO-299) to assign the primary employee for the location. Transactions with no assignable employee remain with `employee_id=None` — these should be treated as unattributed rather than assumed to be manager overrides.

### Legacy Fernet tokens

`decrypt_token` transparently handles legacy Fernet-encrypted tokens from before GRO-248. These are not automatically re-encrypted until the next `store_token()` call. Merchants who have not re-authorized since GRO-248 shipped still have Fernet-encrypted tokens in `square_oauth_tokens`. No immediate action required; re-authorization rotates to GCM.

### `parse_auxiliary_parsers.parse_timecard` returns `None` on missing fields

Unlike other parsers that return a partial dict, `parse_timecard` returns `None` when required fields (`shift_id`, `team_member_id`, `location_id`, `start_at`) are absent. TSP Sub 2 must check for this `None` return before attempting model instantiation, or an `AttributeError` will occur when constructing the Timecard model.

### `resolve_category_name` in `parse_order_line_items`

The `resolve_category_name` helper in `square_order_parser` depends on `payload.order.catalog` being present in the payload. Square does not always include catalog data in webhook payloads. When absent, a warning is logged and the function returns `None`. Category names are populated as best-effort decoration; downstream services must not rely on them being present.
