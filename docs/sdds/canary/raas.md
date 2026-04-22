# RaaS — Resolution as a Service

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]
**Architecture:** [[docs/sdds/canary/architecture|Canary Architecture SDD]]
**Service type:** App Service (Canary)
**Last reviewed:** 2026-04-13
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[docs/team/Architect|Architect]] · **Operator role:** [[docs/team/Engineer|Engineer]]

---

## Purpose

RaaS owns namespace resolution, source registration, merchant onboarding orchestration, and Valkey key construction. It is the identity-bridge domain that ties merchant data across POS systems. Canary is a lens, not a database -- the RaaS namespace (`raas:{merchant_id}`) is the token that lets the lens see across sources without being the system of record.

When a merchant clicks "Connect with Square," RaaS ensures a namespace exists, registers the source connection, orchestrates webhook registration, triggers initial data sync through the TSP pipeline, and computes statistical baselines. The merchant never sees any of this -- it just works.

---

## Dependencies

| Dependency | Type | Purpose |
|---|---|---|
| PostgreSQL (`canary` DB) | Infrastructure | `app` schema (namespace_registrations, namespace_aliases, merchant_sources, merchant_settings), `sales` schema (transactions for baseline) |
| Valkey (DB 0) | Infrastructure | Stream `canary:events` for publishing synthetic webhook envelopes during initial sync |
| Square OAuth2 API | External | Token exchange (delegated to Identity domain) |
| Square Webhooks API | External | Subscription registration during onboarding |
| Square Payments/Orders/Refunds/etc. APIs | External | Historical data pull during initial sync (10 entity types) |
| TSP stream publisher | Internal | `canary/services/tsp/stream_publisher.py` -- publishes synthetic webhook envelopes |
| Identity domain tables | Internal | `merchants`, `merchant_sources`, `merchant_settings`, `square_oauth_tokens` |
| MCP shared base kit | Internal | `canary/mcp/` -- MCPTool, MCPRegistry, create_mcp_blueprint |
| JWT middleware | Internal | `canary/middleware/jwt_auth.py` -- `@jwt_required` on all MCP tool invoke routes |
| Flask-Limiter | Internal | Rate limiting on MCP endpoints (100/hr manifest+tools list, 1000/hr tool invoke) |

---

## Data Flow & PII Map

### What enters

| Source | Format | Contains PII |
|---|---|---|
| OAuth callback (Identity domain) | `merchant_id` + `access_token` via `OnboardingCoordinator.run_inline()` | Yes -- access_token is a restricted credential |
| Square Payments API | JSON (paginated) | Yes -- card details, customer info in payment objects |
| Square Orders API | JSON (paginated) | Yes -- customer names, addresses in order objects |
| Square Team Members API | JSON | Yes -- employee names, email addresses |
| Square Locations API | JSON | Yes -- business addresses, coordinates |
| Square Refunds/Timecards/Disputes/Gift Cards/Loyalty/Payouts APIs | JSON (paginated) | Varies -- dispute details may contain cardholder info |
| MCP tool invocations | JSON via POST `/raas/tools/<name>` | No -- merchant_id only (resolved from JWT context) |

### What is stored

| Table | Schema | Field | PII Classification | Encryption |
|---|---|---|---|---|
| `namespace_registrations` | app | `namespace_guid` | internal | Plaintext (UUID v4, pseudonymous) |
| `namespace_registrations` | app | `namespace_name` | internal | Plaintext (e.g., "sunrise-coffee.jeffe") |
| `namespace_registrations` | app | `inscription_id` | internal | Plaintext |
| `namespace_registrations` | app | `avalanche_address` | internal | Plaintext |
| `namespace_aliases` | app | `alias_name` | internal | Plaintext |
| `merchant_sources` | app | `external_merchant_id` | sensitive | **Plaintext -- P0** |
| `merchant_sources` | app | `raas_namespace` | internal | Plaintext |
| `merchant_sources` | app | `metadata_json` | restricted | **Plaintext -- P0** (contains `webhook_signature_key`, onboarding results, baseline data, sync metadata including team member names/emails, location addresses) |

### What exits

| Destination | Data | PII Risk |
|---|---|---|
| Valkey stream `canary:events` | Synthetic webhook envelopes containing full Square API payloads | **High** -- raw payment, order, refund, team member, location data published to stream |
| Square Webhooks API | Subscription creation request (notification URL, event types) | Low -- no PII sent |
| MCP tool responses | Namespace strings, source connection status, Valkey key strings | Low -- identifiers only |
| `merchant_settings.baseline_json` | Statistical baselines (avg amounts, refund rates, business hours) | Low -- aggregate statistics, no individual PII |

### PII classification key

- **public:** freely visible (namespace_guid -- pseudonymous UUID)
- **internal:** visible to authenticated users (namespace_name, raas_namespace, alias_name)
- **sensitive:** encrypted at rest, logged on access (external_merchant_id -- Square's merchant identifier)
- **restricted:** encrypted, RLS-gated, audited (webhook_signature_key in metadata_json, access_token passed to onboarding)

---

## API Contract

### Blueprint: `raas_mcp` (`canary/blueprints/raas_mcp.py`)

Prefix: `/raas`

| Route | Method | Auth | Rate Limit | Purpose |
|---|---|---|---|---|
| `/raas/manifest` | GET | JWT | 100/hr | MCP server manifest |
| `/raas/tools` | GET | JWT | 100/hr | List available tools |
| `/raas/tools/<name>` | POST | JWT | 1000/hr | Invoke a tool |
| `/raas/health` | GET | None | None | Service health check |

### MCP Tools (canary-raas server, 7 tools)

| Tool | Category | DB | Input | Output | Description |
|---|---|---|---|---|---|
| `resolve_namespace` | namespace | Yes | `merchant_id` | `{namespace, resolved}` | Resolve merchant_id to `raas:{merchant_id}` if active sources or merchant exists |
| `ensure_namespace` | namespace | No | `merchant_id` | `{namespace}` | Ensure namespace exists (pure string construction, no DB write) |
| `register_source` | sources | Yes | `merchant_id`, `source_code`, `external_merchant_id?`, `metadata?` | `{namespace, source_code, status}` | Register/reactivate a data source connection (idempotent) |
| `get_sources` | sources | Yes | `merchant_id` | `{sources[], count}` | List all active source connections for a merchant |
| `disconnect_source` | sources | Yes | `merchant_id`, `source_code` | `{disconnected: bool}` | Soft-delete a source connection (audit trail preserved) |
| `build_key` | keys | No | `merchant_id`, `parts[]` | `{key}` | Build a fully qualified Valkey key from merchant_id + path segments |
| `link_jeffe` | identity | Yes | `merchant_id`, `namespace_name` | `{raas_namespace, jeffe_name, jeffe_guid, bridge_status}` | Bridge operational namespace to .jeffe identity registration |

### Internal interfaces

| Interface | Caller | Pattern |
|---|---|---|
| `OnboardingCoordinator.run_inline(merchant_id, access_token)` | Identity domain (OAuth callback) | Synchronous function call |
| `RaaSNamespaceResolver.ensure_namespace(merchant_id)` | Identity domain, MCP tools | Direct method call |
| `RaaSNamespaceResolver.register_source(...)` | Identity domain, MCP tools | Direct method call |
| `RaaSNamespaceResolver.build_key(merchant_id, *parts)` | All Valkey consumers (Chirp, Owl, Fox, etc.) | Static method |
| `normalize_payload(payload, merchant_uuid, source)` | TSP Sub2 | Pure function call -- canonicalizes source IDs |

---

## Operations

### Startup sequence

RaaS has no independent startup -- it lives inside the Canary Flask container. The `raas_mcp` blueprint is registered during Flask app initialization. Dependencies are lazy-loaded at call time:

1. Flask app starts, registers `raas_mcp_bp` blueprint at `/raas`
2. `_raas_health()` is bound as the health check handler
3. DB sessions are created per-request via `get_session()` (lazy import in `_get_resolver()`)
4. Square SDK clients are created per-call with merchant access tokens

### Health check

`GET /raas/health` -- returns `{"service": "canary-raas", "healthy": true, "tools": 7}`. No auth required. Does NOT verify DB connectivity or Square API reachability.

### Failure modes

| Failure | Impact | Behavior |
|---|---|---|
| PostgreSQL down | Namespace resolution fails, source registration fails | MCP tool calls return 500. `ensure_namespace` still works (pure string construction). `build_key` still works (static method). |
| Valkey down | Initial data sync cannot publish events | Sync step fails, `SyncProgress.errors` populated. Merchant connected but no historical data. Webhook registration still succeeds. |
| Square API down | Webhook registration fails, initial sync fails | `OnboardingResult.errors` populated. Merchant can still use app -- just without webhooks or historical context. |
| `SQUARE_NOTIFICATION_URL` not configured | Webhook registration fails loudly | Coordinator logs ERROR-level message. Merchant connected but no webhooks flow. Must re-onboard after configuring. |
| Access token expired/revoked during sync | Individual API calls fail | Each entity domain is error-isolated. Partial sync results stored. Other domains continue. |
| DB session stale | `_get_resolver()` creates new session per MCP tool call | Low risk -- sessions are short-lived. But `OnboardingCoordinator` reuses `app_session` across all 3 steps. |

### Monitoring

| Metric | What to alert on | Current state |
|---|---|---|
| Onboarding success rate | `result.success == False` for > 10% of onboardings | Log-based only (structured logging via `logger.info/error`) |
| Webhook registration failures | Any `SQUARE_NOTIFICATION_URL not configured` error | Log-based only |
| Sync event count | `progress.total_published == 0` for a merchant with known history | Log-based only |
| Baseline sufficiency | `baseline.sufficient_data == False` with `total_transactions > 0` | Log-based only |
| MCP tool error rate | Tool invocations returning error dicts | No monitoring -- **P1** |

### Configuration

| Env var | Default | Purpose |
|---|---|---|
| `CANARY_ONBOARDING_SYNC` | `false` | Gate for initial data sync + baseline computation during onboarding |
| `SQUARE_NOTIFICATION_URL` | None (fallback: `CANARY_DOMAIN/webhooks/square`) | Webhook subscription notification URL |
| `SQUARE_ENVIRONMENT` | `sandbox` | Square API environment (`sandbox` or `production`) |
| `SQUARE_API_VERSION` | `2026-01-22` | Square API version for webhook subscriptions |

---

## Namespace Resolution

The namespace system operates on three layers. Layer 1 (Bitcoin Ordinals) is the source-of-truth inscription, storing a pseudonymous UUID v4 (`namespace_guid`) -- never a human-readable name. Layer 2 (Avalanche NameRegistry smart contract) provides fast alias-to-GUID resolution. Layer 3 (PostgreSQL `namespace_registrations` + `namespace_aliases`) is the application cache that all runtime code hits.

**Resolution flow:**

```
Query: "sunrise-coffee.jeffe"
  L3 cache: namespace_aliases WHERE alias_name = ? AND status = 'active'
    HIT  -> return namespace_guid -> merchants.merchant_id
    MISS -> L2 Avalanche NameRegistry.resolve(alias_name)
      HIT  -> cache in L3, return namespace_guid
      MISS -> L1 Bitcoin Ordinals inscription scan (slow, fallback only)
```

**Namespace lifecycle:** `reserved -> claimed -> active -> expired -> suspended`. Annual renewal with 30-day grace period. Inscription on Bitcoin L1 confirms the claim. The `tier` field (free/standard/enterprise) gates future premium features.

**Privacy properties:** The `namespace_guid` is a UUID v4 that never contains human-readable merchant information. The Bitcoin inscription contains only the GUID. The alias-to-GUID mapping in `namespace_aliases` is the sole link between a human name and the pseudonymous identity. Multiple aliases can point to the same GUID (multi-location chains: 5 stores = 5 aliases, 1 GUID).

**Operational namespace vs .jeffe namespace:** The operational namespace (`raas:{merchant_id}`) serves all runtime resolution and is used by every service in the stack. The `.jeffe` identity namespace (Bitcoin L1 inscription) provides the permanent, cryptographically anchored identity. The bridge -- `link_jeffe_namespace()` and `resolve_jeffe_to_raas()` -- connects the two. A merchant can switch POS systems and keep their `.jeffe` namespace -- only the underlying `merchant_source` connection changes.

**Valkey key construction:** All Valkey keys for a merchant follow the pattern `raas:{merchant_id}:{domain}:{key}`. The `build_key()` static method constructs these. Examples:
- `raas:m-001:chirp:velocity:emp-123` -- Chirp velocity cache for an employee
- `raas:m-001:score:location:loc-456` -- risk score for a location
- `raas:m-001:owl:cache:query-hash` -- Owl response cache

**Payload normalizer:** `normalize_payload()` (`canary/services/raas/payload_normalizer.py`) sits between TSP Sub2's JSON parse and parser dispatch. It canonicalizes source-specific merchant IDs to our internal UUIDs, preserving originals as `_source_merchant_id` for audit. Idempotent -- skips already-normalized payloads.

---

## Onboarding Pipeline

The onboarding pipeline runs inline during the OAuth callback, orchestrated by `OnboardingCoordinator.run_inline()`. It never blocks the OAuth redirect -- if any step fails, the merchant can still use the app (just without historical context).

**Step 1: Webhook Registration (always runs).** `WebhookRegistrar.register()` creates a Square webhook subscription via the Square SDK. Checks for existing Canary subscription at configured `SQUARE_NOTIFICATION_URL` (idempotent). Creates subscription with 25 event types covering payments, orders, refunds, cash drawers, gift cards, timecards, disputes, loyalty, inventory, and payouts. The returned `signature_key` is stored in `MerchantSource.metadata_json` for per-merchant HMAC validation.

**Step 2: Initial Data Sync (gated by `CANARY_ONBOARDING_SYNC=true`).** `InitialDataSync.sync()` pulls historical data from the Square API (default 90-day lookback, configurable per-merchant via `lookback_days`, `None` = pull all history). Each record is wrapped in a synthetic webhook envelope and published to Valkey stream `canary:events`. TSP consumers process these identically to real-time webhooks. No direct writes to `canary_sales` -- SOX compliance.

Sync order (reference data first, then transactional):
1. Locations -- stored in metadata + published as `location.created`
2. Team members -- published as `team_member.created`
3. Orders -- published as `order.created` (dual-path format for line items and tenders, MUST precede payments)
4. Payments -- published as `payment.completed` (enriches existing order transactions)
5. Refunds -- published as `refund.created`
6. Timecards -- published as `labor.timecard.created`
7. Disputes -- published as `dispute.created`
8. Gift card activities -- published as `gift_card.activity.created` (capped at 50 cards)
9. Loyalty accounts -- published as `loyalty.account.created`
10. Payouts -- published as `payout.sent`

Each domain is error-isolated -- a failure in one does not block others.

**Step 3: Baseline Computation (runs after sync completes).** `BaselineCalculator.compute()` queries `sales.transactions` to compute merchant-specific statistical baselines: avg/std/median/p95 transaction amounts, avg daily count, refund rate, typical business hours (5th/95th percentile), entity counts. Stored in `MerchantSource.metadata_json` and `merchant_settings.baseline_json`. Minimum threshold: 20 transactions.

**Onboarding state machine:**

```
not_connected -> authorizing -> connected -> syncing -> active
                                  |                       |
                 token_expired -> refreshing -> active     |
                 token_revoked -> disconnected             |
                 sync_failed   -> error (retry available)
```

---

## Deployment

### Docker service definition

RaaS runs inside the Canary Flask container -- no separate service. The `raas_mcp_bp` blueprint is registered at app initialization.

```yaml
# In Canary's docker-compose.yml
canary-web:
  image: canary-web
  ports: ["5001:5001"]
  environment:
    - CANARY_ONBOARDING_SYNC=false
    - SQUARE_NOTIFICATION_URL=
    - SQUARE_ENVIRONMENT=sandbox
    - SQUARE_API_VERSION=2026-01-22
  depends_on:
    - growdirect_postgres
    - growdirect_valkey
```

### AWS target

| Component | AWS Service | Notes |
|---|---|---|
| Flask app (includes RaaS) | ECS/Fargate | Single task definition for all Canary services |
| PostgreSQL | RDS (pg17) | `canary` database, schemas: app, sales, metrics |
| Valkey | ElastiCache | DB 0 for Canary |
| Square credentials | Secrets Manager | `SQUARE_NOTIFICATION_URL`, API keys |
| Encryption keys | Secrets Manager | For future field-level encryption of metadata_json |

### CI/CD requirements

- RaaS has no independent deployment -- ships with Canary Flask container
- Integration tests must verify: namespace resolution, source registration, MCP tool dispatch
- Smoke test: `GET /raas/health` returns 200

---

## Code Review Findings

### P0 -- Blocks production

**P0-RAAS-1: Webhook signature key stored plaintext in metadata_json.**
The `webhook_signature_key` returned by Square is stored as a plaintext string inside `MerchantSource.metadata_json`. This key is critical for HMAC validation of incoming webhooks. If the database is compromised, an attacker can forge webhook payloads for any merchant. The entire `metadata_json` blob is a plaintext JSON string containing this key alongside onboarding status, baseline data, and sync metadata.

*Recommended fix:* Extract `webhook_signature_key` from `metadata_json` and store it using the same AES-256-GCM encryption pattern as OAuth tokens in `canary/services/identity/crypto.py`. Alternatively, encrypt the entire `metadata_json` field at rest. Reference: Identity domain's `EncryptedOAuthToken` pattern.

**P0-RAAS-2: Team member PII (names, emails) stored plaintext in metadata_json.**
During initial sync, `_sync_team_members()` stores employee `given_name`, `family_name`, and `email_address` directly in `MerchantSource.metadata_json["sync_team_members"]`. This is plaintext PII in a JSON blob column with no field-level encryption.

*Recommended fix:* Either (a) stop storing team member PII in metadata_json since it is also published to TSP for CRDM ingestion, or (b) encrypt the sync metadata sub-keys containing PII before storage.

**P0-RAAS-3: Location addresses stored plaintext in metadata_json.**
`_sync_locations()` stores full business addresses (street, city, state, zip, country) and GPS coordinates in `MerchantSource.metadata_json["sync_locations"]`. Business addresses are sensitive merchant data.

*Recommended fix:* Same as P0-RAAS-2 -- either remove from metadata_json (TSP handles CRDM storage) or encrypt.

**P0-RAAS-4: Raw Square API payloads published to Valkey stream with full PII.**
`_publish_to_stream()` wraps raw Square API response objects (including card details, customer info, employee names/emails) into JSON and publishes to the `canary:events` Valkey stream. While TSP consumers process these, the raw payloads persist in the stream until trimmed. No PII redaction occurs before publishing.

*Recommended fix:* Implement a PII redaction step in `_publish_to_stream()` that strips sensitive fields (card fingerprints, customer names) from synthetic envelopes, or ensure Valkey stream MAXLEN/trimming is configured with a short retention.

**P0-RAAS-5: Secrets in .env files.**
`SQUARE_NOTIFICATION_URL`, `SQUARE_ENVIRONMENT`, and `SQUARE_API_VERSION` are loaded from `.env` via `os.getenv()`. While these specific values are low-sensitivity, the pattern extends to all Square credentials in the stack. Production deployment must use Secrets Manager.

*Recommended fix:* Migrate all Square-related secrets to AWS Secrets Manager with `boto3` retrieval at startup. Non-sensitive config (environment, API version) can remain as env vars.

### P1 -- Before GA

**P1-RAAS-1: No audit logging for source registration/disconnection.**
`register_source()` and `disconnect_source()` log to Python logger but produce no audit trail records. There is no database-level audit of when sources were connected, disconnected, or reactivated. This matters for SOX compliance -- who authorized which POS connections and when.

*Recommended fix:* Add audit log entries for source lifecycle changes (register, disconnect, reactivate) with timestamps, actor (user_id from JWT context), and before/after state.

**P1-RAAS-2: No data retention policy for metadata_json.**
`metadata_json` accumulates data across onboarding runs, sync operations, and baseline computations. It is never pruned. Over time this blob grows unbounded, containing historical team member lists, location snapshots, and multiple baseline computations.

*Recommended fix:* Implement a retention policy that archives or purges sync snapshots older than 90 days. Keep only the latest baseline and onboarding result.

**P1-RAAS-3: Health check does not verify DB or downstream dependencies.**
`GET /raas/health` returns `{"healthy": true}` unconditionally. It does not test PostgreSQL connectivity, Valkey availability, or Square API reachability. A healthy response from this endpoint does not mean the service can actually resolve namespaces.

*Recommended fix:* Add a lightweight DB query (e.g., `SELECT 1`) and Valkey PING to the health check. Return `healthy: false` with degraded dependency status if either fails.

**P1-RAAS-4: `_get_resolver()` creates unmanaged DB sessions.**
The MCP tool helper `_get_resolver()` calls `get_session()` on every invocation, creating a new SQLAlchemy session that is never explicitly closed or committed. If tool invocations accumulate, this could leak DB connections.

*Recommended fix:* Use Flask's request-scoped session or add explicit session lifecycle management (try/finally with session.close()).

**P1-RAAS-5: MCP tool error responses don't use consistent HTTP status codes.**
Tool invocations that return `{"error": "..."}` come back as HTTP 200 (no `"ok"` key in the response dict). The blueprint logic checks `result.get("ok")` -- tools that return error dicts without `"ok": False` get treated as 500s by default. Inconsistent contract.

*Recommended fix:* Standardize all tool handlers to include `"ok": True/False` in their return dicts. Ensure error responses use HTTP 400 (client error) vs 500 (server error) appropriately.

**P1-RAAS-6: No rate limiting on onboarding pipeline.**
`OnboardingCoordinator.run_inline()` is called during the OAuth callback with no rate limiting or concurrency control. A malicious or buggy OAuth flow could trigger multiple concurrent onboardings for the same merchant, causing duplicate webhook subscriptions and duplicate sync data.

*Recommended fix:* Add idempotency guard at the coordinator level -- check if onboarding is already in progress for a merchant before starting.

### P2 -- Post-launch

**P2-RAAS-1: No key rotation for webhook signature keys.**
Once a webhook signature key is stored, there is no rotation mechanism. If a key is compromised, the only recovery path is to delete the Square subscription and re-create it (which generates a new key).

*Recommended fix:* Document a key rotation procedure. Consider periodic re-registration of webhook subscriptions.

**P2-RAAS-2: Initial sync runs synchronously in OAuth callback.**
When `CANARY_ONBOARDING_SYNC=true`, the full 10-entity sync runs inline in the HTTP request. For merchants with large transaction histories, this can block the OAuth callback for 30-60+ seconds.

*Recommended fix:* Move sync to a background task (Valkey-backed task queue). The coordinator documents this as "Phase 1: synchronous" with async planned.

**P2-RAAS-3: `ensure_namespace` does not actually create anything.**
Despite its name and description, `ensure_namespace()` is pure string construction -- it returns `f"raas:{merchant_id}"` without checking or creating any database record. The docstring says "Creates if needed" but no creation occurs. This is not a bug per se (the namespace is implicit), but the name and docs are misleading.

*Recommended fix:* Either rename to `build_namespace()` or update docs to clarify that the namespace is a convention, not a persisted record.

**P2-RAAS-4: `_store_sync_metadata` creates its own DB session.**
Inside `InitialDataSync._store_sync_metadata()`, a new session is obtained via `get_session()` independent of the session used by the coordinator. This means sync metadata writes and onboarding status writes happen on different sessions, creating potential consistency issues.

*Recommended fix:* Pass the app session from the coordinator through to `InitialDataSync` and use it consistently.

**P2-RAAS-5: Gift card activity sync hardcoded cap at 50 cards.**
`_publish_gift_cards()` iterates over `gc_ids[:50]`, silently dropping gift cards beyond the first 50. For merchants with large gift card programs, this means incomplete historical data.

*Recommended fix:* Make the cap configurable or remove it. Log a warning when truncation occurs.

---

## Dependencies and Cross-Domain Contracts

**Tables owned (app schema):**

| Table | Access Pattern | Rows |
|---|---|---|
| `namespace_registrations` | CRUD + partial index on active status | 1 per merchant |
| `namespace_aliases` | CRUD + FK to registrations | N per merchant (multi-location) |

**Tables read/written (owned by other domains):**

| Table | Owner | RaaS Access |
|---|---|---|
| `merchants` | Identity | Read during resolve |
| `merchant_sources` | Identity | Read/write during source registration, onboarding status/metadata storage |
| `source_systems` | Identity | FK reference from merchant_sources.source_code |
| `merchant_settings` | Identity | Write baseline_json during onboarding |
| `square_oauth_tokens` | Identity | Written during onboarding (via coordinator) |
| `sales.transactions` | Webhook Pipeline | Read during baseline computation |

**Inter-domain contract matrix:**

| Caller -> Callee | Interface | Pattern |
|---|---|---|
| Identity -> RaaS | `OnboardingCoordinator.run_inline(merchant_id, access_token)` | Sync function call during OAuth callback |
| RaaS -> Identity tables | `INSERT/UPDATE merchants, merchant_sources, merchant_settings` | DB write during onboarding |
| RaaS -> Square Webhooks API | `WebhookRegistrar.register()` | External API call |
| RaaS -> TSP | `_publish_to_stream()` -> `stream_publisher.publish_event()` | Valkey stream publish |
| RaaS -> Square APIs | Payments, Orders, Refunds, Timecards, Disputes, Gift Cards, Loyalty, Payouts list/search | REST API calls during initial sync |
| Any agent -> RaaS | MCP tool calls via `/raas/tools/<name>` | HTTP POST (JWT required) |

**Depended on by:**

| Consumer | Purpose |
|---|---|
| Identity (OAuth callback) | Triggers onboarding pipeline |
| Chirp rule engine | Reads `baseline_json` from merchant_settings for threshold calibration |
| Fox cases | GUID-based evidence references survive POS changes |
| Owl | Future: resolve `.jeffe` names to `raas:{merchant_id}` for cross-source queries |
| All Valkey consumers | `build_key()` provides namespaced key prefixes |
| TSP Sub2 | `normalize_payload()` canonicalizes source merchant IDs |

**Linear references:** GRO-53, GRO-54, GRO-58 (GUID Amendment), GRO-130 (namespace/sources), GRO-142 (onboarding pipeline), GRO-186 (MCP server), GRO-237 (payload normalizer), GRO-258 (lookback days), GRO-284 (merchant lookback settings).

---

## Source Files

| Module | Purpose |
|---|---|
| `canary/services/raas/namespace_resolver.py` | `RaaSNamespaceResolver` -- namespace CRUD, source registration, Valkey key construction, .jeffe identity bridge |
| `canary/services/raas/tools.py` | 7 MCP tool definitions for `canary-raas` server |
| `canary/services/raas/payload_normalizer.py` | `normalize_payload()` -- source-agnostic ID canonicalization for TSP Sub2 |
| `canary/services/onboarding/coordinator.py` | `OnboardingCoordinator` -- orchestrates post-OAuth pipeline (webhooks, sync, baseline) |
| `canary/services/onboarding/webhook_registrar.py` | `WebhookRegistrar` -- registers Square webhook subscriptions via Square API |
| `canary/services/onboarding/initial_sync.py` | `InitialDataSync` -- pulls historical Square data and publishes through TSP stream |
| `canary/services/onboarding/baseline_calculator.py` | `BaselineCalculator` -- computes merchant-specific transaction baselines for Chirp |
| `canary/blueprints/raas_mcp.py` | Flask blueprint -- 4 MCP routes (manifest, tools list, tool invoke, health) |
| `canary/models/app/namespace.py` | `NamespaceRegistration`, `NamespaceAlias` models |
| `canary/models/app/merchant_sources.py` | `MerchantSource` model |

---

## Production Readiness Checklist

- [ ] PII encrypted at rest -- P0-RAAS-1 (signature key), P0-RAAS-2 (team member PII), P0-RAAS-3 (location addresses)
- [ ] Secrets in AWS Secrets Manager (not .env) -- P0-RAAS-5
- [x] Health check endpoint responds -- `/raas/health` returns 200 (but does not verify dependencies -- P1-RAAS-3)
- [ ] Audit logging for sensitive operations -- P1-RAAS-1 (source registration/disconnection)
- [ ] Data retention policy implemented -- P1-RAAS-2 (metadata_json growth)
- [x] Rate limiting on public endpoints -- MCP blueprint applies Flask-Limiter (100/hr, 1000/hr)
- [ ] Error responses don't leak internals -- P1-RAAS-5 (inconsistent error contract), exception messages may leak stack traces
- [ ] PII redaction in Valkey stream -- P0-RAAS-4 (raw payloads published)
- [ ] DB session lifecycle managed -- P1-RAAS-4 (leaked sessions in MCP tools)
- [ ] Onboarding idempotency guard -- P1-RAAS-6 (concurrent onboarding risk)
