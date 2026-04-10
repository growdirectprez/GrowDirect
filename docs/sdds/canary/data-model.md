# Data Model

Cross-cutting reference for all tables across Canary's three PostgreSQL schemas (`app`, `sales`, `metrics`) plus the separate `memory` database. One database (`canary`) hosts three schemas; ALX memory lives in `growdirect_memory` (GRO-172). 44 FK constraints enforced (GRO-lockdown Phase A). All models use SQLAlchemy 2.0 `Mapped[]` syntax.

Source SDDs: SDD-023 through SDD-032, SDD-042, SDD-043, SDD-044, SDD-057.

---

## App Schema

43 tables across 8 domain owners. All use `AppBase`. Tenant-scoped tables include `merchant_id` via `TenantMixin`.

### Identity Domain (14 tables)

| Table | Key Columns | Access Pattern | Notes |
|-------|------------|----------------|-------|
| `organizations` | id, org_name, subscription_tier, billing_status | CRUD + soft-delete | Root business entity. AuditMixin + SoftDeleteMixin. |
| `merchants` | id, organization_id (FK), merchant_id (UNIQUE), currency | CRUD + soft-delete | POS connection. One per Square account. |
| `merchant_settings` | id, merchant_id (UNIQUE), calendar_type, fiscal_pattern, timezone, lookback_days, theme, show_employee_names | CRUD | Localization, fiscal calendar (NRF 4-5-4 or calendar_month), notification prefs. Drives all period metrics. `lookback_days`: Integer, nullable, default 30 — controls history pull depth per merchant; NULL=unlimited (GRO-258). `theme`: String(30), default "canary-dark" — valid: canary-dark, canary-light, whitelabel-dark, whitelabel-light (GRO-238). `show_employee_names`: Boolean, default True — PII toggle for employee name display (GRO-242). |
| `users` | id, merchant_id, keycloak_user_id (UNIQUE), email | CRUD + soft-delete | Keycloak-linked. TenantMixin. |
| `roles` | id, role_name (UNIQUE) | CRUD | Global: admin/owner/manager/operator/member/viewer. |
| `user_roles` | id, merchant_id, user_id (FK), role_id (FK) | CRUD | Tenant-scoped role assignment. |
| `employees` | id, merchant_id, square_employee_id | CRUD + soft-delete | Staff records from Square Labor API. |
| `locations` | id, merchant_id, square_location_id | CRUD + soft-delete | Physical stores from Square. |
| `location_hierarchy` | id, parent_location_id, child_location_id | CRUD | Multi-level location grouping. |
| `customers` | id, merchant_id, square_customer_id | CRUD + soft-delete | Customer profiles from Square. |
| `products` | id, merchant_id, catalog_object_id | CRUD + soft-delete | Catalog items from Square. |
| `square_oauth_tokens` | id, merchant_id, access_token (encrypted), refresh_token | CRUD | One token per merchant. Encrypted at rest. |
| `source_systems` | code (PK), display_name, category | CRUD | Reference catalog: square/clover/toast. Not tenant-scoped. |
| `merchant_sources` | id, merchant_id, source_code (FK), raas_namespace, status | CRUD | RaaS source registry. Answers "which pipes are live?" |

### Chirp Domain (2 tables)

| Table | Key Columns | Access Pattern | Notes |
|-------|------------|----------------|-------|
| `detection_rules` | id, rule_id (UNIQUE), category, severity, default_threshold | CRUD | Global catalog. 29 frozen rules, 8 categories. Not tenant-scoped. |
| `merchant_rule_config` | id, merchant_id, rule_id (FK), is_enabled, custom_threshold, notify_enabled | CRUD | Per-merchant threshold overrides. `notify_enabled`: Boolean, default True — per-rule notification toggle (GRO-254). |

### Alert Domain (4 tables)

| Table | Key Columns | Access Pattern | Notes |
|-------|------------|----------------|-------|
| `alerts` | id, merchant_id, rule_id (FK), severity, source_table, source_id, employee_id, location_id, impact_cents | Append-only | Immutable once written by Chirp. Status tracked via alert_history. |
| `alert_history` | id, alert_id (FK), status, changed_by (FK) | Append-only | One row per status transition: new/acknowledged/investigating/resolved/false_positive. |
| `notification_log` | id, merchant_id, alert_id, channel, status, frequency_mode | Append-only | Delivery tracking for email/sms/in_app/push. |
| `notification_schedule` | id, merchant_id, alert_category, freq_critical..freq_info, hourly_cap, daily_cap | CRUD | Per-merchant, per-category frequency routing. |

### Owl Domain (4 tables)

| Table | Key Columns | Access Pattern | Notes |
|-------|------------|----------------|-------|
| `owl_sessions` | id, merchant_id, session_type, heartbeat_score, heartbeat_band, previous_session_id (FK self) | Append-only | One row per analysis run. Delta-chained via previous_session_id. |
| `owl_findings` | id, session_id (FK), category, severity, delta_direction, delta_detail | Append-only | One row per Chirp category that fired in a session. |
| `owl_merchant_memory` | id, merchant_id, latest_session_id (FK), score_trend, recurring_categories, running_summary | CRUD | One row per merchant. Always-current context injected into Owl prompts. |
| `owl_action_log` | id, merchant_id, finding_id (FK), action_type, outcome | Append-only | Tracks merchant responses to Owl findings. |

### Fox Domain (7 tables)

| Table | Key Columns | Access Pattern | Notes |
|-------|------------|----------------|-------|
| `fox_cases` | id, merchant_id, case_number, status, priority, assigned_to | CRUD | Investigation cases. The Vault in mobile UX. |
| `fox_case_alerts` | id, case_id (FK), alert_id (FK) | CRUD | Junction table linking alerts to cases. |
| `fox_case_timeline` | id, case_id (FK), entry_type, entry_hash, previous_hash | Append-only + hash chain | SHA-256 hash-chained audit trail. Tamper-evident. |
| `fox_case_actions` | id, case_id (FK), action_type, performed_by | Append-only | Case action log. |
| `fox_evidence` | id, case_id (FK), evidence_type, file_path | CRUD | Evidence locker attachments. |
| `fox_evidence_access_log` | id, evidence_id (FK), accessed_by, access_type | Append-only | Evidence access audit trail. |
| `fox_subjects` | id, case_id (FK), entity_type, entity_id | CRUD | Persons/entities of interest linked to cases. |

### Webhook Pipeline Domain (3 tables)

| Table | Key Columns | Access Pattern | Notes |
|-------|------------|----------------|-------|
| `webhook_events` | id, merchant_id, event_id (UNIQUE), event_type, payload, processing_status | Append-only | Raw Square webhook storage. HMAC-verified. Deduped by event_id. |
| `schema_fingerprints` | id, event_type, payload_hash (UNIQUE), occurrence_count | CRUD | SHA-256 schema signature tracking. Not tenant-scoped. |
| `schema_drift_alerts` | id, event_type, new_fields, missing_fields, is_resolved | CRUD | Alerts on Square API structure changes. |

### UI/BFF Domain (5 tables)

| Table | Key Columns | Access Pattern | Notes |
|-------|------------|----------------|-------|
| `feature_flags` | id, flag_name, is_enabled | CRUD | Global feature toggles. |
| `merchant_feature_flags` | id, merchant_id, flag_id (FK), is_enabled | CRUD | Per-merchant flag overrides. |
| `app_config` | id, config_key, config_value | CRUD | Application configuration key-value store. |
| `card_profiles` | id, merchant_id, card_fingerprint | CRUD | Card fingerprint profiles for repeat-card detection. |
| `blocked_entities` | id, merchant_id, entity_type, entity_id, blocked_by | CRUD | Merchant-blocked cards, customers, employees. |

### RaaS Domain (2 tables)

| Table | Key Columns | Access Pattern | Notes |
|-------|------------|----------------|-------|
| `namespace_registrations` | id, merchant_id, namespace, source_code | CRUD | Valkey namespace registry for multi-source routing. |
| `namespace_aliases` | id, registration_id (FK), alias | CRUD | Alternative namespace lookups. |

### Cross-Cutting (2 tables)

| Table | Key Columns | Access Pattern | Notes |
|-------|------------|----------------|-------|
| `audit_log` | id, merchant_id, action, resource_type, resource_id, user_id, entry_hash, previous_hash | Append-only + hash chain | SHA-256 hash-chained tamper-evident audit trail. No UPDATE/DELETE. |
| `interest_signups` | id, email, company_name | Append-only | Pre-launch interest capture. |

---

## Sales Schema

22 tables. **ALL WRITE-ONCE IMMUTABLE** -- PostgreSQL `BEFORE UPDATE OR DELETE` trigger raises `IMMUTABILITY VIOLATION` exception. Corrections use compensating INSERTs (e.g., refund_links). All use `SalesBase` + `ImmutableMixin`. Data enters exclusively via TSP (webhook pipeline); no direct ORM or SQL writes permitted.

### Transaction Core (4 tables)

| Table | Key Columns | Notes |
|-------|------------|-------|
| `transactions` | id, merchant_id, square_payment_id (UNIQUE), transaction_type, amount_cents, employee_id, location_id, entry_method, risk_score, cancel_context | Primary fact table. PAYMENT/REFUND/EXCHANGE/NO_SALE/POST_VOID. `cancel_context`: String(20), nullable — derived field for void classification: IMMEDIATE_VOID, MANAGER_VOID, EXPIRED_HOLD, TIMEOUT_VOID, UNKNOWN (GRO-257). |
| `transaction_line_items` | id, merchant_id, transaction_id (FK), product_id, quantity, unit_price_cents, is_voided | Order-level detail. Chirp void/discount detection. |
| `transaction_tenders` | id, merchant_id, transaction_id (FK), tender_type, amount_cents, card_fingerprint | Split payment detail. CARD/CASH/GIFT_CARD/WALLET/OTHER. |
| `refund_links` | id, merchant_id, refund_transaction_id (FK), original_transaction_id (FK), refund_amount_cents | Compensating INSERT pattern linking refunds to originals. |

### Cash Management (2 tables)

| Table | Key Columns | Notes |
|-------|------------|-------|
| `cash_drawer_shifts` | id, merchant_id, square_shift_id, employee_id, state, expected_cash_cents, counted_cash_cents, cash_over_short_cents | Open/close cycle. Feeds Chirp C-101..C-104. |
| `cash_drawer_events` | id, merchant_id, shift_id (FK), event_type, amount_cents, employee_id | OPEN/CLOSE/PAID_IN/PAID_OUT/NO_SALE/ADJUSTMENT within a shift. |

### Gift Card & Loyalty (3 tables)

| Table | Key Columns | Notes |
|-------|------------|-------|
| `gift_card_activities` | id, merchant_id, gift_card_id, activity_type, amount_cents, balance_after_cents | ACTIVATE/LOAD/REDEEM/DEACTIVATE. Feeds Chirp C-601/C-602. |
| `loyalty_accounts` | id, merchant_id, square_loyalty_id, customer_id, balance_points, lifetime_points | Running balance. **Exception: updatable** (balance updates on each event). Uses AuditMixin not ImmutableMixin. |
| `loyalty_events` | id, merchant_id, loyalty_account_id (FK), event_type, points, balance_after | ACCRUE/REDEEM/ADJUST/EXPIRE. Feeds Chirp C-801..C-804. |

### Disputes & Payouts (3 tables)

| Table | Key Columns | Notes |
|-------|------------|-------|
| `disputes` | id, merchant_id, square_dispute_id, payment_id (FK), state, amount_cents, reason | Chargeback lifecycle: INQUIRY/EVIDENCE_REQUIRED/ACCEPTED/WON/LOST. |
| `evidence_records` | id, merchant_id, dispute_id (FK), evidence_type, evidence_text | Merchant response documentation for disputes. |
| `payouts` | id, merchant_id, square_payout_id, status, amount_cents, arrival_date | Square settlement disbursements. SENT/FAILED/PAID. |

### Inventory & Labor (2 tables)

| Table | Key Columns | Notes |
|-------|------------|-------|
| `inventory_adjustments` | id, merchant_id, product_id, location_id, adjustment_type, quantity_change | PHYSICAL_COUNT/SALE/RECEIVE/SHRINKAGE/TRANSFER. |
| `employee_timecards` | id, merchant_id, employee_id, clock_in_at, clock_out_at, overtime_hours | Feeds Chirp C-301..C-303 (ghost shift, buddy punch, overtime). |

### Pipeline Infrastructure (3 tables)

| Table | Key Columns | Notes |
|-------|------------|-------|
| `ingestion_log` | id, merchant_id, batch_id (FK), source_system, event_type, status, target_table | One row per webhook processing attempt. |
| `etl_batches` | id, merchant_id, batch_type, status, total_events, processed_events, failed_events | Batch grouping: INITIAL_SYNC/WEBHOOK/DAILY_REFRESH/BACKFILL. |
| `dead_letter_queue` | id, merchant_id, source_system, event_type, payload, error_message, retry_count, is_resolved | Failed events after exhausted retries. |

### Event Journal & Other (5 tables)

| Table | Key Columns | Notes |
|-------|------------|-------|
| `event_inscriptions` | id, merchant_id, event_type, source_id, inscription_hash | TSP event inscription records. Merkle-tree integrity. |
| `inscription_pool` | id, merchant_id, pool_hash, event_count | Inscription pool aggregation for Merkle verification. |
| `ej_links` | id, merchant_id, source_order_id, transaction_id | EJ spine: links source system order_id to local transaction. |
| `devices` | id, merchant_id, device_id, device_name, location_id | Terminal device registry from Square. |
| `invoices` | id, merchant_id, square_invoice_id, status, amount_cents | Square invoice records. |

---

## Metrics Schema

20 tables. Star schema. All use `MetricsBase`. Writes exclusively from ETL batch aggregation; read-heavy for dashboards, scorecards, and Owl reports. Fully re-derivable from sales schema (drop and rebuild).

### Fact Tables (6 tables)

| Table | Grain | Key Columns | Notes |
|-------|-------|------------|-------|
| `daily_metrics` | merchant x location x date | transaction_count, gross_sales_cents, refund_count/amount, void_count/total, no_sale_count, cash_variance_cents, discount_total_cents, alert_count | Primary aggregation. UNIQUE on (merchant_id, location_id, metric_date). |
| `hourly_metrics` | merchant x location x date x hour | transaction_count, total_sales_cents, refund_count, void_count, alert_count | Intraday pattern analysis. |
| `period_metrics` | merchant x location x fiscal period | fiscal_year, fiscal_quarter, fiscal_period (1-13 NRF / 1-12 calendar), sra_total_cents, sra_pct_sales | Aggregated from daily_metrics by period_aggregation.py. |
| `employee_daily_metrics` | merchant x employee x location x date | Same as daily_metrics + employee_id, risk_score_snapshot | Per-employee daily aggregates. |
| `employee_period_metrics` | merchant x employee x period | transaction_count, off_clock_days, avg_risk_score, max_risk_score | Per-employee period aggregates. |
| `product_daily_metrics` | merchant x product x date | catalog_object_id, item_name, units_sold, revenue_cents, discount_cents, void_count, return_count | Per-product daily aggregates. |

### Dimension Tables (3 tables)

| Table | Key Columns | Notes |
|-------|------------|-------|
| `dim_date` | date_key (PK), day_of_week, fiscal_year, fiscal_week_of_year, is_holiday | Pre-populated calendar dimension. fiscal_period computed at query time (merchant-configurable pattern). |
| `dim_location` | id, location_id, location_name, address | SCD Type 2. Mirrors location attributes at measurement time. |
| `dim_employee` | id, employee_id, employee_name, role | SCD Type 2. Mirrors employee attributes at measurement time. |

### ML Feature Store (3 tables)

| Table | Key Columns | Notes |
|-------|------------|-------|
| `transaction_features` | id, merchant_id, transaction_id (FK), feature_vector (JSON), model_id | Per-transaction feature vectors for ML input. |
| `feature_definitions` | id, feature_name, computation_metadata | Feature catalog with derivation logic. |
| `ml_models` | id, model_name, version, accuracy, deployment_state | Model registry. |

### Risk Scoring (2 tables)

| Table | Key Columns | Notes |
|-------|------------|-------|
| `entity_risk_scores` | id, merchant_id, entity_type, entity_id, risk_score (0.0-1.0), risk_band | Current risk per entity (merchant/employee/location/card). |
| `risk_score_history` | id, entity_risk_score_id, risk_score, computed_at | Risk score timeline for trend analysis. |

### Baselines & Scorecards (6 tables)

| Table | Key Columns | Notes |
|-------|------------|-------|
| `metric_baselines` | id, merchant_id, metric_name, mean, stddev, percentiles | Statistical baselines from historical data. Dynamic thresholding for Chirp. |
| `velocity_baselines` | id, merchant_id, metric_name, rate_of_change | Rate-of-change baselines for anomaly detection. |
| `scorecard_thresholds` | id, merchant_id, metric_name, normal_upper_pct, watch_upper_pct, review_upper_pct, direction | Heatmap band boundaries. Seeded on onboarding. |
| `weekly_scorecard` | id, merchant_id, week_start, scores | Weekly scorecard snapshots. |
| `monthly_scorecard` | id, merchant_id, month, scores | Monthly scorecard snapshots. |
| `dashboard_config` | id, merchant_id, widget_layout | Per-merchant widget layout. Seeded on onboarding. |

---

## Memory Schema

2 tables in separate `growdirect_memory` database. Isolated from app schema for operational independence. Managed by ALX domain. Served by memory bus MCP server on port 8003 (GRO-172).

### `alx_memories`

Institutional knowledge store with pgvector semantic search.

| Column | Type | Notes |
|--------|------|-------|
| id | String(36) | PK, uuid4 |
| content | Text | Memory content (4000 char max for embedding) |
| memory_type | String(50) | CHECK constraint: architecture/decision/finding/context/work_product/team_profile/context_block/foundation/session_summary/procedure |
| metadata | JSONB | Structured metadata (domain, sdd_ref, narrative, tags) |
| embedding | Vector(768) | nomic-embed-text via Ollama. HNSW cosine index for approximate nearest neighbor. |
| narrative | String(50) | Five narratives classification: founder/retail_process/retail_systems/platform/tech_stack |
| created_at | DateTime(tz) | |
| updated_at | DateTime(tz) | |

**Search strategy:** (1) pgvector cosine similarity (primary), (2) PostgreSQL full-text `tsvector/tsquery` (fallback), (3) `ILIKE` pattern match (last resort). 954+ curated memories covering 60 SDDs, process architecture, detection patterns, and retail LP ontology.

**Index:** HNSW cosine on `embedding` column for fast approximate nearest neighbor search.

### `alx_sessions`

Agent session tracking for context continuity.

| Column | Type | Notes |
|--------|------|-------|
| id | String(36) | PK, uuid4 |
| session_id | String(50) | UNIQUE session identifier (alx-YYYYMMDD-HHMMSS-hash) |
| gro_issues | JSONB | Linear issues loaded for this session |
| context_snapshot | Text | Assembled context at session start |
| summary | Text | End-of-session summary (written by session_close) |
| started_at | DateTime(tz) | |
| closed_at | DateTime(tz) | NULL if still active |

---

## Cross-Cutting Patterns

**Mixins** (defined in `canary/models/base.py`):
- `AuditMixin`: created_at, updated_at, created_by, modified_by
- `SoftDeleteMixin`: db_status (draft/active/archived), db_effective_from, db_effective_to
- `TenantMixin`: merchant_id (indexed, FK to merchants)
- `ImmutableMixin`: PostgreSQL BEFORE trigger prevents UPDATE/DELETE

**FK Constraints:** 44 foreign key constraints enforced at database level (GRO-lockdown Phase A, PR #9). All FK references resolve Square external IDs to internal UUIDs before write.

**Immutability:** Sales schema enforces write-once via PostgreSQL trigger (`prevent_update_delete()`). Corrections use compensating INSERTs. Exception: `loyalty_accounts` uses AuditMixin (updatable balance).

**Hash Chains:** `audit_log` and `fox_case_timeline` use SHA-256 hash chains for tamper-evident sequencing. Each entry's `entry_hash = SHA256(serialize(current) + previous_hash)`.

**Tenant Isolation:** All merchant-scoped tables include `merchant_id` via TenantMixin. Future: PostgreSQL RLS policies enforce isolation at DB level.
