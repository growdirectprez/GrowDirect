# RaaS

## Overview

RaaS (Resolution as a Service) owns namespace resolution, source registration, merchant onboarding orchestration, and Valkey key construction. It is the identity-bridge domain that ties merchant data across POS systems. Canary is a lens, not a database -- the RaaS namespace (`raas:{merchant_id}`) is the token that lets the lens see across sources without being the system of record.

When a merchant clicks "Connect with Square," RaaS ensures a namespace exists, registers the source connection, orchestrates webhook registration, triggers initial data sync through the TSP pipeline, and computes statistical baselines. The merchant never sees any of this -- it just works.

**Blueprints:**

| Blueprint | Prefix | Purpose |
|---|---|---|
| `raas_mcp` (`canary/blueprints/raas_mcp.py`) | `/raas` | MCP server -- manifest, tools list, tool invocation, health |

**Services:**

| Module | Purpose |
|---|---|
| `canary/services/raas/namespace_resolver.py` | `RaaSNamespaceResolver` -- namespace CRUD, source registration, Valkey key construction, .jeffe identity bridge |
| `canary/services/raas/tools.py` | 7 MCP tool definitions for `canary-raas` server |
| `canary/services/onboarding/coordinator.py` | `OnboardingCoordinator` -- orchestrates post-OAuth pipeline (webhooks, sync, baseline) |
| `canary/services/onboarding/webhook_registrar.py` | `WebhookRegistrar` -- registers Square webhook subscriptions via Square API |
| `canary/services/onboarding/initial_sync.py` | `InitialDataSync` -- pulls historical Square data and publishes through TSP stream |
| `canary/services/onboarding/baseline_calculator.py` | `BaselineCalculator` -- computes merchant-specific transaction baselines for Chirp |

**Design principles:**

- Namespace creation is seamless and automatic during OAuth callback -- no merchant-facing configuration
- Source disconnection is soft-delete -- records are kept for audit trail
- Initial data sync publishes through TSP (Valkey stream `canary:events`), never writes directly to `canary_sales` (SOX compliance)
- Baseline computation reads from `sales.transactions`, writes to `app.merchant_settings` -- cross-schema but within SOX boundaries
- The `.jeffe` identity bridge connects the operational namespace (`raas:{merchant_id}`) to a permanent Bitcoin L1 inscription (UUID v4 GUID). The operational namespace serves all runtime resolution; the L1 inscription provides cryptographic permanence

**Data model (app schema):**

| Table | Purpose | Key columns |
|---|---|---|
| `namespace_registrations` | Bridge between `.jeffe` names and CRDM `merchant_id` | `namespace_guid` (UUID v4, inscribed on L1), `namespace_name` (e.g. `sunrise-coffee.jeffe`), `namespace_root`, `inscription_id`, `inscription_block`, `avalanche_address`, `tier`, `status` |
| `namespace_aliases` | L3 cache for alias-to-GUID resolution (mirrors L2 Avalanche contract) | `alias_name` (unique, human-readable), `namespace_guid` (FK to registrations), `status` (active/expired/reserved) |
| `merchant_sources` | Tracks which POS systems a merchant has authorized | `source_code` (FK to `source_systems`), `external_merchant_id`, `raas_namespace`, `status` (pending/active/disconnected/expired), `metadata_json` |

**MCP tools (canary-raas server, 7 tools):** `resolve_namespace`, `ensure_namespace`, `register_source`, `get_sources`, `disconnect_source`, `build_key`, `link_jeffe`. Six are DB-dependent, one (`build_key`) is pure computation.

**Inbound contracts:**
- Identity domain calls `OnboardingCoordinator.run_inline()` during OAuth callback
- Any MCP agent can call namespace tools via `/raas/tools/<name>`

**Outbound contracts:**
- Writes merchant records and OAuth tokens into Identity-owned tables during onboarding
- Calls `WebhookRegistrar.register()` to create Square webhook subscriptions (registers 25 event types)
- Triggers `InitialDataSync.sync()` which publishes synthetic webhook envelopes to Valkey stream `canary:events` for TSP processing
- Calls `BaselineCalculator.compute()` to store baselines in `merchant_settings.baseline_json`

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

**Operational namespace vs .jeffe namespace:** The operational namespace (`raas:{merchant_id}`) serves all runtime resolution and is used by every service in the stack. The `.jeffe` identity namespace (Bitcoin L1 inscription) provides the permanent, cryptographically anchored identity. The bridge between them — `link_jeffe_namespace()` and `resolve_jeffe_to_raas()` — connects `raas:{merchant_id}` (operational) to the `.jeffe` GUID (permanent identity). This means a merchant can switch from Square to Clover and keep their `.jeffe` namespace — only the underlying `merchant_source` connection changes.

**Valkey key construction:** All Valkey keys for a merchant follow the pattern `raas:{merchant_id}:{domain}:{key}`. The `build_key()` static method constructs these. Examples:
- `raas:m-001:chirp:velocity:emp-123` -- Chirp velocity cache for an employee
- `raas:m-001:score:location:loc-456` -- risk score for a location
- `raas:m-001:owl:cache:query-hash` -- Owl response cache

**MCP tool details:**

| Tool | Category | DB | Description |
|---|---|---|---|
| `resolve_namespace` | namespace | Yes | Resolve merchant_id to `raas:{merchant_id}` if active sources or merchant exists; returns None otherwise |
| `ensure_namespace` | namespace | No | Ensure namespace exists, create if needed; called during OAuth callback |
| `register_source` | sources | Yes | Register a data source connection; idempotent (reactivates if previously disconnected) |
| `get_sources` | sources | Yes | List all active source connections for a merchant |
| `disconnect_source` | sources | Yes | Soft-delete a source connection (keeps audit trail) |
| `build_key` | keys | No | Build a fully qualified Valkey key from merchant_id + path segments |
| `link_jeffe` | identity | Yes | Bridge `raas:{merchant_id}` to `.jeffe` identity registration |

## Onboarding Pipeline

The onboarding pipeline runs inline during the OAuth callback, orchestrated by `OnboardingCoordinator.run_inline()`. It never blocks the OAuth redirect -- if any step fails, the merchant can still use the app (just without historical context). The pipeline has three sequential steps.

**Step 1: Webhook Registration (always runs).** `WebhookRegistrar.register()` creates a Square webhook subscription via the Square SDK. It checks for an existing Canary subscription at the configured `SQUARE_NOTIFICATION_URL` (idempotent). If none exists, it creates one with 25 event types covering payments, orders, refunds, cash drawers, gift cards, timecards, disputes, loyalty, inventory, and payouts. The returned `signature_key` is stored in `MerchantSource.metadata_json` for per-merchant HMAC validation of incoming webhooks. If `SQUARE_NOTIFICATION_URL` is not configured, registration fails loudly -- the merchant is connected but no webhooks will flow.

**Step 2: Initial Data Sync (gated by `CANARY_ONBOARDING_SYNC=true`).** `InitialDataSync.sync()` pulls historical data from the Square API (default 90-day lookback) and publishes each record as a synthetic webhook envelope to the Valkey stream `canary:events`. TSP consumers (Sub1-Seal, Sub2-Parse) process these identically to real-time webhooks. No direct writes to `canary_sales` -- SOX compliance via the TSP pipeline.

Sync order (reference data first, then transactional):
1. Locations -- stored in `MerchantSource.metadata_json` (app schema, not sales)
2. Team members -- published to TSP stream as `team_member.created` events
3. Payments -- published as `payment.completed` (paginated, heaviest)
4. Orders -- published as `order.created` with dual-path format for line items and tenders
5. Refunds -- published as `refund.created`
6. Timecards -- published as `labor.timecard.created`
7. Disputes -- published as `dispute.created`
8. Gift card activities -- published as `gift_card.activity.created` (capped at 50 cards)
9. Loyalty accounts -- published as `loyalty.account.created`
10. Payouts -- published as `payout.sent`

Each domain is error-isolated -- a failure in one does not block others. The `SyncProgress` dataclass tracks counts per entity type.

**Step 3: Baseline Computation (runs after sync completes).** `BaselineCalculator.compute()` queries `sales.transactions` to compute merchant-specific statistical baselines: average/std/median/p95 transaction amounts, average daily count, refund rate, typical business hours (5th/95th percentile of transaction hours), and entity counts. These are stored in `MerchantSource.metadata_json` and `merchant_settings.baseline_json` for Chirp to use at evaluation time. Minimum threshold: 20 transactions for a "sufficient" baseline. If data is insufficient, defaults apply but the `sufficient_data` flag is false.

**Onboarding state machine:**

```
not_connected -> authorizing -> connected -> syncing -> active
                                  |                       |
                 token_expired -> refreshing -> active     |
                 token_revoked -> disconnected             |
                 sync_failed   -> error (retry available)
```

**OnboardingResult tracking:** The `OnboardingResult` dataclass aggregates pipeline status (webhook_registered, sync_completed, baseline_computed, errors list) and stores it in `MerchantSource.metadata_json["onboarding"]` for debugging and ops console visibility.

**Cross-reference:** OAuth flow details (token exchange, encryption, refresh, scopes) are owned by the Identity domain -- see `identity.md` and SDD-039.

## Dependencies and Cross-Domain Contracts

**Tables owned (app schema):**

| Table | Access Pattern | Rows |
|---|---|---|
| `namespace_registrations` | CRUD + partial index on active status | 1 per merchant |
| `namespace_aliases` | CRUD + FK to registrations | N per merchant (multi-location) |

**Tables read/written (owned by other domains):**

| Table | Owner | RaaS Access |
|---|---|---|
| `merchants` | Identity | Read during resolve; written during onboarding |
| `merchant_sources` | Identity | Read/write during source registration, onboarding status storage |
| `source_systems` | Identity | FK reference from merchant_sources.source_code |
| `merchant_settings` | Identity | Write baseline_json during onboarding |
| `square_oauth_tokens` | Identity | Written during onboarding (via coordinator) |
| `sales.transactions` | Webhook Pipeline | Read during baseline computation |

**Inter-domain contract matrix:**

| Caller -> Callee | Interface | Pattern |
|---|---|---|
| Identity -> RaaS | `OnboardingCoordinator.run_inline(merchant_id, access_token)` | Sync function call during OAuth callback |
| RaaS -> Identity | `INSERT INTO merchants, square_oauth_tokens` | DB write during onboarding |
| RaaS -> Webhook Pipeline | `WebhookRegistrar.register()` -> Square Webhooks API | External API call |
| RaaS -> TSP | `InitialDataSync._publish_to_stream()` -> `stream_publisher.publish_event()` | Valkey stream publish |
| RaaS -> Square API | Payments, Orders, Refunds, Timecards, Disputes, Gift Cards, Loyalty, Payouts list/search | REST API calls during initial sync |
| Any agent -> RaaS | MCP tool calls via `/raas/tools/<name>` | HTTP POST |

**Depends on:**

| Dependency | Purpose |
|---|---|
| Square OAuth2 API | Token exchange (via Identity domain) |
| Square Webhooks API | Subscription registration |
| Square Payments/Orders/etc. APIs | Historical data pull during initial sync |
| TSP stream publisher (`canary/services/tsp/stream_publisher.py`) | Publishing synthetic webhook envelopes |
| Identity domain tables | Merchant, source, settings, token storage |
| `canary/mcp/` shared base kit | MCPTool, MCPRegistry, create_mcp_blueprint |

**Depended on by:**

| Consumer | Purpose |
|---|---|
| Identity (OAuth callback) | Triggers onboarding pipeline |
| Chirp rule engine | Reads `baseline_json` from merchant_settings for threshold calibration |
| Fox cases | GUID-based evidence references survive POS changes |
| Owl | Future: resolve `.jeffe` names to `raas:{merchant_id}` for cross-source queries |
| All Valkey consumers | `build_key()` provides namespaced key prefixes |

**Linear references:** GRO-53, GRO-54, GRO-58 (GUID Amendment), GRO-130 (namespace/sources), GRO-142 (onboarding pipeline), GRO-186 (MCP server). Archive SDDs: SDD-035 (namespace registry), SDD-036 (entity profiles -- xref), SDD-037 (location hierarchy -- xref), SDD-039 (merchant onboarding OAuth -- primary owner is identity.md), SDD-057 section 3.9 (domain map).
