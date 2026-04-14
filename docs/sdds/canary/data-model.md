# Data Model

**Type:** App Service (Canary)
**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]
**Source SDDs:** SDD-023 through SDD-032, SDD-042, SDD-043, SDD-044, SDD-057

---

## Purpose

Cross-schema reference document covering all tables across Canary's three PostgreSQL schemas (`app`, `sales`, `metrics`) plus the separate `growdirect_memory` database. One database (`canary`) hosts three schemas; ALX memory lives in `growdirect_memory` (GRO-172). This SDD is the PII map anchor -- all other Canary SDDs point here for field-level data classification.

## Dependencies

- **PostgreSQL 17** (`growdirect_postgres:5432`) -- databases: `canary` (schemas: app, sales, metrics), `growdirect_memory`
- **Valkey 8** (`growdirect_valkey:6379`, DB 0) -- sessions, cache, task queue
- **Ollama** (`growdirect_ollama:11434`) -- embeddings for `alx_memories.embedding` (768-dim vectors)
- **Canary Flask app** (`canary:5001`) -- ORM layer, all reads/writes go through SQLAlchemy 2.0
- **Alembic** -- schema migrations

---

## Data Flow & PII Map

### Data Entry Points

| Source | What enters | Target schema |
|--------|------------|---------------|
| Square Webhooks (HMAC-verified) | Payment, refund, order, inventory, labor, dispute, payout events | sales (via TSP pipeline) |
| Square OAuth flow | Access/refresh tokens, merchant profile | app (identity domain) |
| Square Catalog/Team/Location APIs | Product catalog, employee profiles, store locations | app (identity domain) |
| User registration / Keycloak | User email, display name, login timestamps | app (users) |
| Merchant onboarding | Org name, billing email, phone, settings | app (organizations, merchant_settings) |
| Pre-launch join page | Prospect email | app (interest_signups) |
| Fox case management UI | Subject names, investigation notes, evidence files | app (fox_* tables) |
| Memory Bus MCP | Session context, curated memories | growdirect_memory (alx_*) |

### Data Exit Points

| Destination | What exits | PII risk |
|-------------|-----------|----------|
| Dashboard UI | Aggregated metrics, employee names (if show_employee_names=true), alert details | internal |
| Owl AI reports | Narrative summaries, heartbeat scores, findings | internal |
| Fox case exports | Subject names, evidence files, investigation notes | sensitive |
| Notification channels (email/SMS) | Alert summaries, recipient contact info | sensitive |
| Square API (token refresh) | Encrypted OAuth tokens (decrypted in-flight) | restricted |

### PII Classification

- **public**: Freely visible, no access control needed (product names, metric aggregates)
- **internal**: Visible to authenticated users within tenant (location names, alert counts)
- **sensitive**: Must be encrypted at rest, logged on access (email, phone, names, addresses)
- **restricted**: Encrypted at rest, RLS-gated, audited on every access (OAuth tokens, card data, investigation subjects)

### Comprehensive PII Map

This is the authoritative PII inventory for Canary. All other SDDs reference this table.

#### App Schema -- Identity Domain

| Table | Field | PII Classification | Encrypted at Rest? | Notes |
|-------|-------|-------------------|-------------------|-------|
| `organizations` | `org_name` | internal | NO | Business name |
| `organizations` | `billing_email` | sensitive | NO | Billing contact email -- plaintext |
| `organizations` | `billing_external_id` | internal | NO | Square subscription ID |
| `merchants` | `merchant_name` | internal | NO | Business display name |
| `merchants` | `source_merchant_id` | internal | NO | Square merchant external ID |
| `merchant_settings` | `notif_phone` | sensitive | NO | SMS phone number -- plaintext |
| `users` | `email` | sensitive | NO | User login email -- plaintext |
| `users` | `username` | sensitive | NO | User login name -- plaintext |
| `users` | `display_name` | sensitive | NO | User display name -- plaintext |
| `employees` | `employee_name` | sensitive | NO | Employee full name -- plaintext |
| `employees` | `email` | sensitive | NO | Employee email -- plaintext |
| `employees` | `square_employee_id` | internal | NO | Square external employee ID |
| `customers` | `square_customer_id` | internal | NO | Square external customer ID (no PII stored by design) |
| `locations` | `address_line1` | sensitive | NO | Physical street address -- plaintext |
| `locations` | `address_line2` | sensitive | NO | Physical address line 2 -- plaintext |
| `locations` | `city` | internal | NO | City name |
| `locations` | `state` | internal | NO | State code |
| `locations` | `postal_code` | sensitive | NO | ZIP code -- location fingerprinting risk |
| `locations` | `coordinates` | sensitive | NO | JSON lat/lng -- precise geolocation |
| `square_oauth_tokens` | `access_token_encrypted` | restricted | YES (AES-256-GCM) | Only encrypted field in the system |
| `square_oauth_tokens` | `refresh_token_encrypted` | restricted | YES (AES-256-GCM) | Only encrypted field in the system |
| `interest_signups` | `email` | sensitive | NO | Prospect email -- plaintext |

#### App Schema -- Alert & Notification Domain

| Table | Field | PII Classification | Encrypted at Rest? | Notes |
|-------|-------|-------------------|-------------------|-------|
| `notification_log` | `recipient` | sensitive | NO | Email address or phone number -- plaintext |
| `audit_log` | `ip_address` | sensitive | NO | IPv4/IPv6 address -- plaintext |
| `audit_log` | `user_id` | internal | NO | FK to users -- identity linkage |

#### App Schema -- Fox Domain

| Table | Field | PII Classification | Encrypted at Rest? | Notes |
|-------|-------|-------------------|-------------------|-------|
| `fox_subjects` | `name` | sensitive | NO | Investigation subject name -- plaintext |
| `fox_subjects` | `entity_id` | sensitive | NO | Cross-reference to employee/customer |
| `fox_cases` | `assigned_to` | internal | NO | User ID of investigator |
| `fox_cases` | `opened_by` | internal | NO | User ID |
| `fox_case_timeline` | `actor_id` | internal | NO | User ID who performed action |
| `fox_case_actions` | `performed_by` | internal | NO | User identity string |
| `fox_evidence` | `file_path` | internal | NO | Server filesystem path |
| `fox_evidence` | `uploaded_by` | internal | NO | User identity string |
| `fox_evidence_access_log` | `accessed_by` | internal | NO | User identity string |
| `fox_evidence_access_log` | `ip_address` | sensitive | NO | IPv4/IPv6 address -- plaintext |

#### App Schema -- Webhook Domain

| Table | Field | PII Classification | Encrypted at Rest? | Notes |
|-------|-------|-------------------|-------------------|-------|
| `webhook_events` | `payload` | sensitive | NO | Raw JSON -- may contain customer names, emails, addresses from Square |

#### App Schema -- Bank & Financial Domain

| Table | Field | PII Classification | Encrypted at Rest? | Notes |
|-------|-------|-------------------|-------------------|-------|
| `bank_accounts` | `holder_name` | sensitive | NO | Legal name of account holder -- plaintext |
| `bank_accounts` | `routing_number` | sensitive | NO | Bank routing number -- plaintext |
| `bank_accounts` | `secondary_routing_number` | sensitive | NO | Secondary routing number -- plaintext |
| `bank_accounts` | `account_number_suffix` | internal | NO | Last 4 digits only (PCI-safe) |

#### App Schema -- Card & Entity Domain

| Table | Field | PII Classification | Encrypted at Rest? | Notes |
|-------|-------|-------------------|-------------------|-------|
| `card_profiles` | `card_fingerprint` | internal | NO | PCI-safe hash (not PAN) |
| `card_profiles` | `card_last4` | internal | NO | Last 4 digits (PCI-safe) |
| `gift_cards` | `gan` | internal | NO | Gift Account Number (safe per Square docs, not PAN) |
| `external_identities` | `external_id` | internal | NO | Source system native ID |

#### Sales Schema

| Table | Field | PII Classification | Encrypted at Rest? | Notes |
|-------|-------|-------------------|-------------------|-------|
| `transactions` | `card_fingerprint` | internal | NO | PCI-safe hash |
| `transactions` | `card_last4` | internal | NO | Last 4 digits (PCI-safe) |
| `transactions` | `card_bin` | sensitive | NO | First 6 digits -- issuer identification, fingerprinting risk |
| `transactions` | `card_exp_month` | sensitive | NO | Card expiration month |
| `transactions` | `card_exp_year` | sensitive | NO | Card expiration year |
| `transactions` | `statement_description` | internal | NO | Cardholder statement text |
| `transactions` | `payload` | sensitive | NO | Full webhook JSON -- may contain PII |
| `transactions` | `employee_id` | internal | NO | Square employee ID (cross-reference) |
| `transactions` | `customer_id` | internal | NO | Square customer ID (cross-reference) |
| `transaction_tenders` | `card_last4` | internal | NO | Last 4 digits (PCI-safe) |
| `loyalty_accounts` | `phone_hash` | internal | NO | SHA-256 of phone (properly hashed) |
| `cash_drawer_shifts` | `employee_id` | internal | NO | Employee who opened drawer |
| `cash_drawer_events` | `employee_id` | internal | NO | Employee who initiated event |
| `disputes` | `payment_id` | internal | NO | Cross-reference to disputed payment |

#### Metrics Schema

| Table | Field | PII Classification | Encrypted at Rest? | Notes |
|-------|-------|-------------------|-------------------|-------|
| `dim_employee` | `employee_name` | sensitive | NO | Employee display name -- plaintext (SCD Type 2 snapshot) |
| `dim_employee` | `square_employee_id` | internal | NO | Square external ID |
| `dim_location` | `location_name` | internal | NO | Store name |

#### Memory Database (`growdirect_memory`)

| Table | Field | PII Classification | Encrypted at Rest? | Notes |
|-------|-------|-------------------|-------------------|-------|
| `alx_memories` | `content` | internal | NO | May contain session context with identifiers |
| `alx_memories` | `metadata` | internal | NO | JSONB -- may reference project/domain info |
| `alx_sessions` | `context_snapshot` | internal | NO | Assembled session context |

---

## Schema Reference

### App Schema

58+ tables across 10 domain owners. All use `AppBase`. Tenant-scoped tables include `merchant_id` via `TenantMixin`.

#### Identity Domain (19 tables)

| Table | Key Columns | Access Pattern | Mixins | Notes |
|-------|------------|----------------|--------|-------|
| `organizations` | id, org_name, billing_email, subscription_tier, billing_status | CRUD + soft-delete | AuditMixin, SoftDeleteMixin | Root business entity. billing_email is PII. |
| `merchants` | id, organization_id (FK), source_merchant_id (UNIQUE), merchant_name, currency | CRUD | -- | POS connection. One per Square account. No AuditMixin. |
| `merchant_settings` | id, merchant_id (UNIQUE), calendar_type, fiscal_pattern, timezone, notif_phone, theme, show_employee_names | CRUD | Manual audit cols | notif_phone is PII. show_employee_names=false masks employee names. |
| `users` | id, merchant_id, email, username, display_name | CRUD + soft-delete | TenantMixin, AuditMixin, SoftDeleteMixin | 3 PII fields: email, username, display_name. |
| `roles` | id, role_name (UNIQUE) | CRUD | AuditMixin | Global: admin/owner/manager/operator/member/viewer. Not tenant-scoped. |
| `user_roles` | id, merchant_id, user_id (FK), role_id (FK) | CRUD | TenantMixin, AuditMixin | Tenant-scoped role assignment. |
| `employees` | id, merchant_id, square_employee_id, employee_name, email | CRUD + soft-delete | TenantMixin, AuditMixin, SoftDeleteMixin | 2 PII fields: employee_name, email. risk_score (0.0-1.0). |
| `locations` | id, merchant_id, square_location_id, location_name, address_line1/2, city, state, postal_code, coordinates | CRUD + soft-delete | TenantMixin, AuditMixin, SoftDeleteMixin | 4 PII fields: address_line1, address_line2, postal_code, coordinates. |
| `location_hierarchy` | id, merchant_id, name, level, parent_id (FK self) | CRUD | TenantMixin, AuditMixin, SoftDeleteMixin | Multi-level location grouping. |
| `customers` | id, merchant_id, square_customer_id | CRUD + soft-delete | TenantMixin, AuditMixin, SoftDeleteMixin | Privacy-first: no PII stored. Aggregates only. |
| `products` | id, merchant_id, square_item_id, product_name, sku, upc | CRUD + soft-delete | TenantMixin, AuditMixin, SoftDeleteMixin | Catalog items from Square. No PII. |
| `square_oauth_tokens` | id, merchant_id, access_token_encrypted, refresh_token_encrypted | CRUD | TenantMixin, AuditMixin | ONLY encrypted fields in entire system. AES-256-GCM. |
| `source_systems` | code (PK), display_name, category | CRUD | AuditMixin | Reference catalog: square/clover/toast. Not tenant-scoped. |
| `merchant_sources` | id, merchant_id, source_code (FK), raas_namespace, status | CRUD | TenantMixin, AuditMixin | RaaS source registry. |
| `external_identities` | id, merchant_id, entity_type, entity_id, source_code, external_id | CRUD | TenantMixin, AuditMixin | POS-agnostic entity bridge. |
| `user_employee_links` | id, merchant_id, user_id (FK), employee_id (FK) | CRUD | TenantMixin, AuditMixin | Canary user to Square employee mapping. |
| `employee_location_assignments` | id, merchant_id, employee_id (FK), location_id (FK) | CRUD | TenantMixin, AuditMixin | Employee to location assignment. |
| `gift_cards` | id, merchant_id, square_gift_card_id, gan, state, balance_cents | CRUD | TenantMixin, AuditMixin | Mutable gift card entity. GAN stored (safe per Square). |
| `bank_accounts` | id, merchant_id, square_bank_account_id, holder_name, routing_number, account_number_suffix | CRUD | TenantMixin, AuditMixin | 3 PII fields: holder_name, routing_number, secondary_routing_number. |

#### Chirp Domain (2 tables)

| Table | Key Columns | Access Pattern | Mixins | Notes |
|-------|------------|----------------|--------|-------|
| `detection_rules` | id, rule_id (UNIQUE), category, severity, default_threshold | CRUD | AuditMixin | Global catalog. Not tenant-scoped. |
| `merchant_rule_config` | id, merchant_id, rule_id (FK), is_enabled, custom_threshold, notify_enabled | CRUD | TenantMixin, AuditMixin | Per-merchant threshold overrides. |

#### Alert Domain (4 tables)

| Table | Key Columns | Access Pattern | Mixins | Notes |
|-------|------------|----------------|--------|-------|
| `alerts` | id, merchant_id, rule_id (FK), severity, source_table, source_id, employee_id (FK), location_id (FK), impact_cents | Append-only | TenantMixin, AuditMixin | Immutable once written by Chirp. |
| `alert_history` | id, alert_id (FK), status, changed_by (FK), notes | Append-only | AuditMixin | Status transitions. |
| `notification_log` | id, merchant_id, alert_id, channel, status, recipient | Append-only | -- | recipient is PII (email/phone). |
| `notification_schedule` | id, merchant_id, alert_category, freq_critical..freq_info, hourly_cap, daily_cap | CRUD | -- | Per-merchant, per-category frequency routing. |

#### Owl Domain (4 tables)

| Table | Key Columns | Access Pattern | Mixins | Notes |
|-------|------------|----------------|--------|-------|
| `owl_sessions` | id, merchant_id, session_type, heartbeat_score, heartbeat_band, previous_session_id (FK self) | Append-only | TenantMixin, AuditMixin | Delta-chained via previous_session_id. |
| `owl_findings` | id, session_id (FK), merchant_id, category, severity, finding_text | Append-only | AuditMixin | One row per Chirp category per session. |
| `owl_merchant_memory` | id, merchant_id (UNIQUE), latest_session_id (FK), running_summary | CRUD | AuditMixin | One row per merchant. Always-current context. |
| `owl_action_log` | id, merchant_id, finding_id (FK), action_type, outcome | Append-only | AuditMixin | Tracks merchant responses to findings. |

#### Fox Domain (7 tables)

| Table | Key Columns | Access Pattern | Mixins | Notes |
|-------|------------|----------------|--------|-------|
| `fox_cases` | id, merchant_id, case_number, status, priority, assigned_to | CRUD | TenantMixin, AuditMixin, SoftDeleteMixin | Investigation cases. |
| `fox_case_alerts` | id, case_id (FK), alert_id | CRUD | AuditMixin | Junction table linking alerts to cases. |
| `fox_case_timeline` | id, case_id (FK), merchant_id, event_type, actor_id, description | Append-only | -- | Immutable audit trail. No AuditMixin (it IS the audit). |
| `fox_case_actions` | id, case_id (FK), merchant_id, action_type, performed_by, outcome | Append-only | TenantMixin, AuditMixin, SoftDeleteMixin | Case action log. |
| `fox_evidence` | id, merchant_id, case_id (FK), evidence_type, file_path, file_hash, chain_hash | INSERT-only | -- | Hash-chained evidence locker. No update/delete. |
| `fox_evidence_access_log` | id, evidence_id (FK), accessed_by, access_type, ip_address | INSERT-only | -- | ip_address is PII. |
| `fox_subjects` | id, merchant_id, case_id (FK), subject_type, entity_id, name | CRUD | TenantMixin, AuditMixin, SoftDeleteMixin | name is PII. |

#### Webhook Pipeline Domain (3 tables)

| Table | Key Columns | Access Pattern | Mixins | Notes |
|-------|------------|----------------|--------|-------|
| `webhook_events` | id, merchant_id, event_id (UNIQUE), event_type, payload, processing_status | Append-only | TenantMixin, AuditMixin | payload contains raw Square JSON with potential PII. |
| `schema_fingerprints` | id, event_type, payload_hash (UNIQUE), occurrence_count | CRUD | AuditMixin | SHA-256 schema signature. Not tenant-scoped. |
| `schema_drift_alerts` | id, event_type, new_fields, missing_fields, is_resolved | CRUD | AuditMixin | Square API structure change alerts. |

#### UI/BFF Domain (5 tables)

| Table | Key Columns | Access Pattern | Mixins | Notes |
|-------|------------|----------------|--------|-------|
| `feature_flags` | id, flag_key (UNIQUE), flag_name, is_enabled | CRUD | AuditMixin | Global feature toggles. Not tenant-scoped. |
| `merchant_feature_flags` | id, merchant_id, flag_key (FK), is_enabled | CRUD | TenantMixin, AuditMixin | Per-merchant flag overrides. |
| `app_config` | id, config_key (UNIQUE), config_value, is_secret | CRUD | AuditMixin | Runtime config. Secrets masked in UI. |
| `card_profiles` | id, merchant_id, card_fingerprint, card_last4 | CRUD | TenantMixin, AuditMixin | PCI-safe card fingerprints. |
| `blocked_entities` | id, merchant_id, entity_type, entity_id, blocked_by | CRUD + soft-delete | TenantMixin, AuditMixin, SoftDeleteMixin | Merchant-blocked entities. |

#### RaaS Domain (2 tables)

| Table | Key Columns | Access Pattern | Mixins | Notes |
|-------|------------|----------------|--------|-------|
| `namespace_registrations` | id, merchant_id, namespace_name, namespace_guid, status | CRUD | TenantMixin, AuditMixin | .jeffe namespace bridge. |
| `namespace_aliases` | id, alias_name, namespace_guid (FK), status | CRUD | -- | Alias resolution cache. |

#### Vault Domain (1 table)

| Table | Key Columns | Access Pattern | Mixins | Notes |
|-------|------------|----------------|--------|-------|
| `vault_memories` | id, merchant_id, memory_type, source_type, payload (JSONB), narrative | INSERT-only | -- | Owl's long-term memory. Sealed, not edited. |

#### Subscription & Transfer Domain (2 tables)

| Table | Key Columns | Access Pattern | Mixins | Notes |
|-------|------------|----------------|--------|-------|
| `subscriptions` | id, merchant_id, square_subscription_id, customer_id, status, card_id | CRUD | TenantMixin, AuditMixin | Recurring billing tracking. |
| `transfer_orders` | id, merchant_id, square_transfer_order_id, from_location_id, to_location_id, state | CRUD | TenantMixin, AuditMixin | Inter-location inventory movement. |

#### Cross-Cutting (2 tables)

| Table | Key Columns | Access Pattern | Mixins | Notes |
|-------|------------|----------------|--------|-------|
| `audit_log` | id, merchant_id, action, resource_type, resource_id, user_id, ip_address, entry_hash, previous_hash | Append-only + hash chain | TenantMixin | SHA-256 hash-chained. ip_address is PII. |
| `interest_signups` | id, email, source | Append-only | -- | Pre-launch. email is PII. |

### Sales Schema

27+ tables. **ALL WRITE-ONCE IMMUTABLE** (except `loyalty_accounts` and `cash_drawer_shifts`) -- PostgreSQL `BEFORE UPDATE OR DELETE` trigger raises `IMMUTABILITY VIOLATION` exception. All use `SalesBase`. Data enters exclusively via TSP pipeline.

#### Transaction Core (4 tables)

| Table | Key Columns | Notes |
|-------|------------|-------|
| `transactions` | id, merchant_id, external_id (UNIQUE), transaction_type, amount_cents, employee_id, location_id, card_fingerprint, card_bin, card_last4, card_exp_month/year, payload | Primary fact table. card_bin and card_exp fields are PII. payload contains raw webhook JSON. |
| `transaction_line_items` | id, merchant_id, transaction_id (FK), catalog_object_id, quantity, base_price_cents, is_voided | Order-level detail. No PII. |
| `transaction_tenders` | id, merchant_id, transaction_id (FK), tender_type, amount_cents, card_last4, team_member_id | Split payment detail. card_last4 (PCI-safe). |
| `refund_links` | id, merchant_id, refund_external_id, original_external_id, refund_amount_cents, employee_id | Compensating INSERT pattern. |

#### Order Detail (4 tables)

| Table | Key Columns | Notes |
|-------|------------|-------|
| `line_item_discounts` | id, merchant_id, line_item_id (FK), discount_type, amount_cents | Discount detail per line item. |
| `line_item_taxes` | id, merchant_id, line_item_id (FK), tax_name, amount_cents | Tax detail per line item. |
| `line_item_modifiers` | id, merchant_id, line_item_id (FK), modifier_name, amount_cents | Modifier detail per line item. |
| `service_charges` | id, merchant_id, transaction_id, charge_name, amount_cents | Service charges per order. |
| `order_rewards` | id, merchant_id, transaction_id, reward_id | Reward redemptions per order. |
| `order_returns` | id, merchant_id, transaction_id, return_line_items | Return details per order. |

#### Cash Management (2 tables)

| Table | Key Columns | Notes |
|-------|------------|-------|
| `cash_drawer_shifts` | id, merchant_id, square_shift_id, employee_id, state, expected_cash_cents, closed_cash_cents, cash_variance_cents | **Exception: updatable** (state changes on close). |
| `cash_drawer_events` | id, merchant_id, shift_id, event_type, amount_cents, employee_id | Append-only within a shift. |

#### Gift Card & Loyalty (3 tables)

| Table | Key Columns | Notes |
|-------|------------|-------|
| `gift_card_activities` | id, merchant_id, gift_card_id, activity_type, amount_cents, balance_after_cents | Feeds Chirp C-601/C-602. |
| `loyalty_accounts` | id, merchant_id, square_loyalty_id, phone_hash, points_balance, lifetime_points | **Exception: updatable** (balance updates). phone_hash properly hashed. |
| `loyalty_events` | id, merchant_id, loyalty_account_id, event_type, points | Feeds Chirp C-801..C-804. |

#### Disputes & Payouts (3 tables)

| Table | Key Columns | Notes |
|-------|------------|-------|
| `disputes` | id, merchant_id, square_dispute_id, payment_id, state, amount_cents, reason | Chargeback lifecycle. |
| `evidence_records` | id, merchant_id, dispute_id (FK), evidence_type, evidence_text | Dispute response documentation. |
| `payouts` | id, merchant_id, square_payout_id, status, amount_cents, arrival_date | Square settlement disbursements. |

#### Inventory & Labor (2 tables)

| Table | Key Columns | Notes |
|-------|------------|-------|
| `inventory_adjustments` | id, merchant_id, product_id, location_id, adjustment_type, quantity_change | PHYSICAL_COUNT/SALE/RECEIVE/SHRINKAGE/TRANSFER. |
| `employee_timecards` | id, merchant_id, employee_id, clock_in_at, clock_out_at, overtime_hours | Feeds Chirp C-301..C-303. |

#### Terminal (2 tables)

| Table | Key Columns | Notes |
|-------|------------|-------|
| `terminal_checkouts` | id, merchant_id, square_checkout_id, amount_cents, status | Square Terminal checkout records. |
| `terminal_refunds` | id, merchant_id, square_refund_id, amount_cents, status | Square Terminal refund records. |

#### Pipeline Infrastructure (3 tables)

| Table | Key Columns | Notes |
|-------|------------|-------|
| `ingestion_log` | id, merchant_id, batch_id (FK), source_system, event_type, status, target_table | One row per webhook processing attempt. |
| `etl_batches` | id, merchant_id, batch_type, status, total_events, processed_events, failed_events | Batch grouping. |
| `dead_letter_queue` | id, merchant_id, source_system, event_type, payload, error_message, retry_count | payload may contain PII from failed events. |

#### Event Journal (5 tables)

| Table | Key Columns | Notes |
|-------|------------|-------|
| `event_inscriptions` | id, merchant_id, event_type, source_id, inscription_hash | TSP Merkle-tree integrity. |
| `inscription_pool` | id, merchant_id, pool_hash, event_count | Pool aggregation for Merkle verification. |
| `ej_links` | id, merchant_id, source_order_id, transaction_id | EJ spine: links source order to local transaction. |
| `devices` | id, merchant_id, device_id, device_name, location_id | Terminal device registry. |
| `invoices` | id, merchant_id, square_invoice_id, status, amount_cents | Square invoice records. |

### Metrics Schema

21 tables. Star schema. All use `MetricsBase`. Writes exclusively from ETL batch aggregation; read-heavy for dashboards and Owl reports. Fully re-derivable from sales schema.

#### Fact Tables (6 tables)

| Table | Grain | Notes |
|-------|-------|-------|
| `daily_metrics` | merchant x location x date | Primary aggregation. 40+ KPI columns including gift card, loyalty, dispute, invoice, shrinkage. |
| `hourly_metrics` | merchant x location x date x hour | Intraday pattern analysis. |
| `period_metrics` | merchant x location x fiscal period | NRF 4-5-4 period aggregation. SRA v2 computed here. |
| `employee_daily_metrics` | merchant x employee x location x date | Per-employee daily aggregates with off-clock and discount decomposition. |
| `employee_period_metrics` | merchant x employee x period | Per-employee period aggregates with risk scoring. |
| `product_daily_metrics` | merchant x product x location x date | Per-product daily aggregates with return rate. |

#### Dimension Tables (3 tables)

| Table | Notes |
|-------|-------|
| `dim_date` | Pre-populated calendar dimension. Fiscal fields populated by fiscal calendar service. |
| `dim_location` | SCD Type 2. `location_name` is internal, no PII. |
| `dim_employee` | SCD Type 2. `employee_name` is PII (sensitive). Mirrors employee attributes at measurement time. |

#### ML Feature Store (3 tables)

| Table | Notes |
|-------|-------|
| `transaction_features` | Per-transaction ML feature vectors. No direct PII. |
| `feature_definitions` | Feature catalog with derivation logic. No PII. |
| `ml_models` | Model registry. No PII. |

#### Risk Scoring (2 tables)

| Table | Notes |
|-------|-------|
| `entity_risk_scores` | Current risk per entity. `entity_id` can cross-reference employees/cards. |
| `risk_score_history` | Risk score timeline. Append-only. |

#### Baselines & Scorecards (7 tables)

| Table | Notes |
|-------|-------|
| `metric_baselines` | Statistical baselines for anomaly detection. |
| `velocity_baselines` | Rate-of-change baselines with day/hour granularity. |
| `scorecard_thresholds` | Heatmap band boundaries. Seeded on onboarding. |
| `weekly_scorecard` | Weekly KPI snapshots. |
| `monthly_scorecard` | Monthly KPI snapshots. |
| `dashboard_config` | Per-merchant widget layout. |

### Memory Schema

2 tables in separate `growdirect_memory` database. Managed by ALX domain via MCP server on port 8003 (GRO-172).

#### `alx_memories`

| Column | Type | Notes |
|--------|------|-------|
| id | String(36) | PK, uuid4 |
| content | Text | Memory content (4000 char max for embedding) |
| memory_type | String(50) | CHECK constraint: architecture/decision/finding/context/work_product/team_profile/context_block/foundation/session_summary/procedure |
| metadata | JSONB | Structured metadata |
| embedding | Vector(768) | nomic-embed-text via Ollama. HNSW cosine index. |
| narrative | String(50) | Five narratives classification |
| created_at / updated_at | DateTime(tz) | |

#### `alx_sessions`

| Column | Type | Notes |
|--------|------|-------|
| id | String(36) | PK, uuid4 |
| session_id | String(50) | UNIQUE (alx-YYYYMMDD-HHMMSS-hash) |
| gro_issues | JSONB | Linear issues loaded |
| context_snapshot | Text | Assembled context at session start |
| summary | Text | End-of-session summary |
| started_at / closed_at | DateTime(tz) | |

---

## Cross-Cutting Patterns

**Mixins** (defined in `canary/models/base.py`):
- `AuditMixin`: created_at, updated_at, created_by, modified_by
- `SoftDeleteMixin`: db_status (draft/active/archived), db_effective_from, db_effective_to
- `TenantMixin`: merchant_id (indexed, FK to merchants)
- `ImmutableMixin`: PostgreSQL BEFORE trigger prevents UPDATE/DELETE (sales schema)

**FK Constraints:** 44+ foreign key constraints enforced at database level. All FK references resolve Square external IDs to internal UUIDs before write.

**Immutability:** Sales schema enforces write-once via PostgreSQL trigger (`prevent_update_delete()`). Corrections use compensating INSERTs. Exceptions: `loyalty_accounts` (updatable balance), `cash_drawer_shifts` (state changes on close).

**Hash Chains:** `audit_log` and `fox_case_timeline` use SHA-256 hash chains for tamper-evident sequencing. `fox_evidence` uses chain_hash for evidence integrity.

**Tenant Isolation:** All merchant-scoped tables include `merchant_id` via TenantMixin. Future: PostgreSQL RLS policies enforce isolation at DB level.

---

## Operations

### Startup Sequence

1. PostgreSQL must be running with `canary` database and all three schemas created
2. Alembic migrations run on app startup (auto-upgrade in dev)
3. Detection rules seeded if `detection_rules` table is empty
4. Fiscal calendar `dim_date` populated if empty
5. Hash chain integrity verified for `audit_log` on startup

### Failure Modes

| Failure | Impact | Recovery |
|---------|--------|----------|
| PostgreSQL down | All reads/writes fail, app returns 500 | Restart growdirect_postgres, connections auto-reconnect via pool |
| Schema migration fails | App may boot with stale schema | Fix migration, run `alembic upgrade head` manually |
| Hash chain broken (audit_log) | Raises `AlarmRecordTamperedError` on startup | Investigate tampered rows, restore from backup |
| Immutability trigger fires | UPDATE/DELETE on sales schema rejected | Use compensating INSERT pattern instead |
| Tenant isolation breach | Data leak across merchants | Add PostgreSQL RLS policies (not yet implemented) |

### Monitoring

| Metric | Normal | Alert threshold |
|--------|--------|-----------------|
| Table row counts (sales) | Growing with webhook volume | Delta = 0 for >1 hour during business hours |
| Dead letter queue depth | < 10 | > 50 unresolved entries |
| Hash chain verification | Passes on every startup | Any failure = P0 |
| FK constraint violations | 0 | Any > 0 |

### Configuration

| Env Var | Purpose | Default |
|---------|---------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://growdirect:growdirect_dev@localhost:5432/canary` |
| `CANARY_ENCRYPTION_KEY` | AES-256-GCM key for OAuth tokens | (from .env -- must move to Secrets Manager) |
| `FERNET_KEY` | Legacy Fernet key (backward compat) | (from .env) |

---

## Deployment

### Docker Service

Canary database runs within `growdirect_postgres` container (shared infrastructure). No separate database container.

```yaml
# devops/docker-compose.yml (shared)
growdirect_postgres:
  image: postgres:17
  ports: ["5432:5432"]
  volumes: ["pgdata:/var/lib/postgresql/data"]
```

### AWS Target

| Component | AWS Service | Notes |
|-----------|-------------|-------|
| PostgreSQL | RDS for PostgreSQL 17 | Multi-AZ, encrypted at rest (EBS encryption) |
| Encryption keys | Secrets Manager | CANARY_ENCRYPTION_KEY, FERNET_KEY |
| Backups | RDS automated snapshots | 7-day retention, point-in-time recovery |

---

## Code Review Findings

### P0 -- Blocks Production

| # | Finding | Affected Tables | Recommended Fix |
|---|---------|----------------|-----------------|
| 1 | **User email stored plaintext** | `users.email`, `users.username`, `users.display_name` | Field-level AES-256-GCM encryption using `canary.utils.crypto` pattern already in OAuth service |
| 2 | **Employee PII stored plaintext** | `employees.employee_name`, `employees.email` | Same field-level encryption pattern |
| 3 | **Organization billing email plaintext** | `organizations.billing_email` | Field-level encryption |
| 4 | **Merchant settings phone plaintext** | `merchant_settings.notif_phone` | Field-level encryption |
| 5 | **Bank account holder name and routing numbers plaintext** | `bank_accounts.holder_name`, `bank_accounts.routing_number`, `bank_accounts.secondary_routing_number` | Field-level encryption -- financial PII |
| 6 | **Notification recipient plaintext** | `notification_log.recipient` | Field-level encryption -- contains emails and phone numbers |
| 7 | **Fox subject names plaintext** | `fox_subjects.name` | Field-level encryption -- investigation subject PII |
| 8 | **Interest signup email plaintext** | `interest_signups.email` | Field-level encryption |
| 9 | **Location addresses plaintext** | `locations.address_line1`, `locations.address_line2`, `locations.coordinates`, `locations.postal_code` | Field-level encryption for address fields; consider hashing coordinates |
| 10 | **Webhook payload contains raw PII** | `webhook_events.payload`, `transactions.payload`, `dead_letter_queue.payload` | Redact PII fields (customer name, email, address) from payload before storage, or encrypt entire payload column |
| 11 | **Encryption keys in .env files** | All encrypted fields | Move `CANARY_ENCRYPTION_KEY` and `FERNET_KEY` to AWS Secrets Manager with `boto3` retrieval at startup |
| 12 | **Transaction card_bin stored plaintext** | `transactions.card_bin` | First 6 digits of card number is a fingerprinting risk; encrypt or hash |
| 13 | **Card expiration data stored plaintext** | `transactions.card_exp_month`, `transactions.card_exp_year` | Encrypt -- combined with card_last4 this approaches PAN reconstruction |
| 14 | **dim_employee stores plaintext employee names** | `dim_employee.employee_name` | This is a metrics snapshot; encrypt or reference the app schema employee by ID instead of copying the name |

### P1 -- Before GA

| # | Finding | Affected Area | Recommended Fix |
|---|---------|--------------|-----------------|
| 1 | **IP addresses logged plaintext** | `audit_log.ip_address`, `fox_evidence_access_log.ip_address` | Hash or mask IPs (store hashed value for anomaly detection, not raw IP) |
| 2 | **No data retention policy** | All schemas | Implement automated purge: audit logs >24mo, dead letter queue >90d, webhook payloads >12mo, notification logs >12mo |
| 3 | **No audit trail for token access** | `square_oauth_tokens` | Log every decrypt operation in `audit_log` |
| 4 | **RLS policies not implemented** | All tenant-scoped tables | Implement PostgreSQL RLS with `SET canary.current_merchant_id` pattern described in TenantMixin |
| 5 | **Merchants table missing AuditMixin** | `merchants` | Add AuditMixin -- no created_by/modified_by tracking on merchant record changes |
| 6 | **No key rotation documented** | OAuth encryption | Document rotation procedure + scheduled rotation for `CANARY_ENCRYPTION_KEY` |
| 7 | **Fox subject cross-DB entity linking deferred** | `fox_subjects.entity_id` | Implement FK validation -- currently a free-text string with no referential integrity |
| 8 | **Notification log lacks audit columns** | `notification_log` | No created_by/modified_by -- add AuditMixin for compliance |
| 9 | **fox_case_timeline missing hash chain** | `fox_case_timeline` | SDD describes hash chain but code has no entry_hash/previous_hash columns -- implement or remove from SDD claim |

### P2 -- Post-Launch

| # | Finding | Affected Area | Recommended Fix |
|---|---------|--------------|-----------------|
| 1 | **Valkey session keys unencrypted** | Session data in Valkey DB 0 | Enable Valkey AUTH + TLS in production |
| 2 | **No PII access logging** | All sensitive fields | Implement field-level access audit for encrypted PII columns |
| 3 | **Evidence files on local filesystem** | `fox_evidence.file_path` | Migrate to S3/blob storage with server-side encryption |
| 4 | **No virus scanning on evidence upload** | `fox_evidence` | Add ClamAV or cloud scanning before storage |
| 5 | **Memory bus content not classified** | `alx_memories.content` | Content may contain session references; classify and potentially encrypt |

---

## Production Readiness Checklist

- [ ] PII encrypted at rest (P0 findings 1-14 above)
- [ ] Secrets in AWS Secrets Manager (not .env)
- [ ] Health check endpoint responds (exists at `/health`)
- [ ] Audit logging for sensitive operations (token access logging missing)
- [ ] Data retention policy implemented (no automated purge exists)
- [ ] Rate limiting on public endpoints (not applicable -- data model SDD)
- [ ] Error responses don't leak internals (not applicable -- data model SDD)
- [ ] PostgreSQL RLS policies implemented for tenant isolation
- [ ] Hash chain integrity on Fox case timeline
- [ ] Key rotation procedure documented and scheduled
- [ ] IP addresses hashed in audit and evidence access logs
- [ ] Webhook/transaction payloads redacted of PII before storage
- [ ] dim_employee name field encrypted or replaced with FK reference
