---
type: research
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# Canary LP — Architecture & Technical Design

> **Domain:** Stack, data model, schemas, protocols, pipeline design, data flow
> **Last Updated:** 2026-03-19 | **Classification:** Confidential

---

## Technology Stack

- **Language:** Python 3.12
- **Web Framework:** Flask with Gunicorn (single WSGI entry point: wsgi.py)
- **ORM:** SQLAlchemy 2.0 (Mapped[] syntax, no legacy declarative_base)
- **Database:** PostgreSQL 17 with pgvector extension
- **Cache/Streams:** Valkey 8 (TSP pipeline, session cache, rate limiting)
- **AI Inference:** Owl powered by qwen3:14b via Ollama (local, MacBook)
- **Payment Platform:** Square SDK (read-only sandbox, OAuth onboarding)
- **Frontend:** Jinja2 templates + CSS design tokens (mobile-first)
- **Infrastructure:** Docker Compose, Cloudflare Tunnel, Alembic migrations
- **Blockchain:** Bitcoin Ordinals (elJeffe protocol), Avalanche L2 NameRegistry

---

## Database Architecture

### Three-Schema Design
One PostgreSQL database (`canary`) with strict schema separation:

**app schema** — Master data, identity, configuration, detection, cases. Written by Flask (canary_app role). Tables: merchants, organizations, employees, locations, customers, products, detection_rules, alerts, alert_history, merchant_rule_config, fox_cases, case_subjects, case_evidence, case_timeline, case_actions, namespace_registrations, namespace_aliases, source_systems, merchant_feature_flags, merchant_settings, feature_flags.

**sales schema** — Immutable transaction records, evidence, Merkle batches. Written exclusively by TSP pipeline (canary_tsp role). Tables: transactions, transaction_line_items, transaction_tenders, refund_links, cash_drawer_shifts, gift_cards, loyalty_events, evidence_records, merkle_batches, inventory_adjustments.

**metrics schema** — Star schema analytics, aggregated from sales data. Written by Flask (canary_app role). Tables: daily_metrics, hourly_metrics, period_aggregates, employee_scores, product_metrics, location_metrics.

**canary_memory** — Separate database for ALX pgvector knowledge graph (954+ curated memories).

### Row-Level Security
All tenant-scoped tables enforce RLS via `merchant_id`. Array-aware for multi-merchant orgs: `merchant_id = ANY(string_to_array(current_setting('app.current_merchant'), ','))`.

---

## elJeffe Protocol v1.0

Self-describing, server-independent verification protocol for commercial events on Bitcoin Ordinals. Core thesis: receipts and transaction records should survive company failure and be verifiable without trusting any server.

### Seven Design Principles
1. Sovereign by default — protocol functions without any server
2. Self-describing — Genesis inscription contains full protocol spec
3. POS-agnostic — operates on canonical event hashes, not vendor-specific data
4. Accumulative — every namespace use adds to its history; history compounds value
5. Non-consumable — Ordinal is not spent when used; one key, infinite doors
6. Layered degradation — L1 Bitcoin, L2 Avalanche, L3 Postgres; any layer can fail independently
7. Math, not trust — verification is SHA-256 Merkle proof reconstruction, not database lookup

### Four Inscription Types
**Genesis** — Root of trust, contains the full protocol spec (~500 bytes). First inscription in the chain. Previous = null, sequence = 0.

**Namespace** — Pseudonymous merchant identity: `{guid}.jeffe`. GUID-only on L1 (no human-readable names on Bitcoin). Includes action field: register, renew, update_metadata.

**Merkle Batch** — Batched commercial events as a Merkle tree. Contains: event_merkle_root, event_count, optional device_attestation tree, batch time range, source system identifiers. Batch triggers: 100 events, 1-hour timeout, or manual flush.

**Revocation** — Marks a namespace as expired, suspended, or transferred. Includes reason and optional transfer_to GUID.

### Three-Layer Resolution Stack
**L1 (Bitcoin)** — GUID-only, immutable, permanent. No merchant identity, no PII. Verification by Merkle proof reconstruction alone.

**L2 (Avalanche)** — Human-readable aliases (`name.jeffe`), NameRegistry smart contract. Disposable burner sub-addresses (`label.name.jeffe` with TTL). Owner can have many aliases per GUID.

**L3 (PostgreSQL)** — GrowDirect's cache layer. namespace_registrations bridges GUID → merchant_id. namespace_aliases caches L2 aliases. Serves merchant dashboards with fast lookups.

---

## TSP Pipeline — Triple Subscriber Architecture

### Ingestion Flow
Square POS → Webhook HTTP POST → Flask endpoint → HMAC-SHA256 verification → Valkey Stream write → Three sequential subscribers process the event.

### Sub 1: Seal
Hashes the raw webhook payload with SHA-256. Stores the hash in `evidence_records` table (sales schema). Creates the chain by linking each evidence record to the previous via `chain_hash = SHA-256(evidence_hash + previous_chain_hash)`. This is the immutability foundation — raw data is hashed before any transformation.

### Sub 2: Parse
Routes the event to a vendor-specific parser (currently Square, extensible to other POS systems via `source_systems` reference table). Transforms vendor data into canonical CRDM (Canary Retail Data Model) format. Six event types: payment.created/updated, refund.created, order.created/updated, cash_drawer_shift, loyalty, inventory. Each parser outputs standardized records into the sales schema tables.

### Sub 3: Merkle + Inscribe
Accumulates sealed events into batches. When a trigger fires (100 events, 1-hour timeout, or manual flush), builds a binary Merkle tree where each leaf = SHA-256(event_id || event_hash || timestamp). Optionally builds a parallel device attestation tree when merchant_feature_flags.device_attestation is enabled. Inscribes the Merkle root on Bitcoin via `ord` CLI. Stores inscription reference in `merkle_batches` table. Chain links via `chain.previous` field (monotonic per namespace).

### Sub 4: Detect
Runs the Chirp detection engine against newly parsed records. Evaluates rules per-webhook (Tier 1 stateless), per-velocity-window (Tier 2 trending), and generates structured alerts with evidence references.

---

## CRDM — Canary Retail Data Model

### Current Entity Relationships (Built)
- **transactions** — Central fact table: amount, timestamp, employee, device, payment method, risk level, transaction type
- **transaction_line_items** — Individual items within a transaction (product, quantity, price, discount)
- **transaction_tenders** — Payment methods used (card, cash, gift card, split tender)
- **refund_links** — Links return transactions to their original sale
- **evidence_records** — SHA-256 hashes of raw webhook payloads, chain-linked
- **merkle_batches** — Inscription references, batch metadata, chain linkage
- **external_identities** — POS system mappings (merchant_id, location_id, employee_id, device_id per source system)
- **namespace_registrations** — GUID-to-merchant bridge (L3 cache of L1 inscriptions)
- **source_systems** — Reference table for POS-agnostic source system abstraction

### Target Tables (GRO-266 — Not Yet Built)
Six new tables required for full Square data coverage:
- **line_item_discounts** — Discount identity, type, percentage, scope, reward link, pricing_rule_id
- **line_item_taxes** — Tax identity, type, rate, scope per line item
- **line_item_modifiers** — Modifier identity, price delta, quantity per line item
- **order_service_charges** — Service charge identity, type, amount per order
- **order_returns** — Return detail, source order link, line item mapping (not just is_voided flag)
- **order_rewards** — Loyalty reward links per order (loyalty-to-transaction bridge)

Without these, Chirp rules C-201 (excessive discount), C-203 (sweethearting), C-009 (delay hold), C-010 (partial auth), C-602 (gift card drain) are partially or fully blind.

### CRDM v1.1 Amendment Scorecard (GRO-267)
The CRDM v1.1 spec (Tom + ALX, March 2026) defined 11 amendments. Only 2 are fully implemented:

| # | Amendment | Target | Status | Blocked Rules |
|---|-----------|--------|--------|---------------|
| 1 | `external_identities` | POS-agnostic entity IDs replacing 25 `square_*` columns | NOT BUILT (P1) | All multi-POS support |
| 2 | `product_identifiers` | Multi-barcode registry (UPC/EAN/ISBN/SKU/PLU) | NOT BUILT | Barcode swap detection |
| 3 | `product_compositions` | Bundle/kit decomposition | NOT BUILT | Bundle shrink detection |
| 4 | `categories` hierarchy | Self-referential + materialized path | NOT BUILT | Category-scoped Chirp rules |
| 5 | Canonical renames | `square_product` → `source_channel`, `*_name` → `display_name` | NOT BUILT | Vendor-neutral naming |
| 6 | JSONB `attributes` | Open-ended POS-specific attrs per entity | NOT BUILT | Non-Square field extensibility |
| 7 | `location_product_authorizations` | Authorized product list per location | NOT BUILT | Diversion, unauthorized sales |
| 8 | Device graph | Hierarchical `devices` + `transaction_devices` join | PARTIAL | Multi-device per transaction |
| A | `namespace_registrations` | .jeffe namespace bridge | DONE | — |
| B | Device attestation | Inscription payload attestation block | NOT BUILT | Protocol v1.1 |
| C | `source_systems` ref table | POS-agnostic source registry | DONE | — |

**Critical path:** Amendment 1 (`external_identities`) is the foundation. Amendments 5, 6, 7 all depend on it. Every parser shipped before this migration adds more `square_*` columns that will need migration later.

### Data Coverage: Current vs Target
Current state: 28% coverage of the 86-table schema (GRO-265 audit). Three tiers of gaps:

**Tier 1 (data arrives, fields dropped):** Order discounts, taxes, service charges, modifiers, rewards, fulfillments, return detail. Gift card activity fields (order_id, line_item_uid, payment_id). Payment fields (delay_action, approved_money, card_type, bin, verification_method, processing_fee).

**Tier 2 (tables exist, no parser):** invoices (8 webhook events → log_only), devices (events → log_only), gift card customer link/unlink, loyalty account deletion.

**Tier 3 (no model, no parser):** catalog.version.updated, customer.* events, terminal.checkout/refund, card.* events, subscription.*, labor.scheduled_shift.*, bank_account.*, vendor.*, location.* events.

### Field Mapping: Square → CRDM
Amount: cents → integer (direct). Tax/discount: nested JSON extraction with defaults. Transaction type: composite logic mapping (NO_SALE when amount=0 and no line items; SALE for standard payments; RETURN for refunds; POST_VOID/VOID based on cancel context). Evidence: SHA-256(raw_payload) + chain_hash computation.

### Schema Versioning
Current: CRDM v1.1 (adds namespace_registrations, namespace_aliases, source_systems, merkle_batches, merchant_feature_flags; modifies external_identities CHECK→FK, adds batch_id to evidence_records). Migration managed by Alembic with explicit FK dependency ordering and rollback scripts. Next migration: `external_identities` (Amendment 1) — the vendor-lock liberation that all future POS integrations depend on.

---

## Project Structure

```
canary/
  blueprints/    # Flask route handlers (27 blueprints: *_wired + *_mcp)
  models/        # SQLAlchemy 2.0 (AppBase, SalesBase, MetricsBase)
  services/      # Business logic (14 service domains)
  middleware/    # JWT auth, session management
  migrations/    # Alembic (single config, three schemas)
  extensions.py  # CSRF, Limiter, Talisman
templates/       # Jinja2 (extends base.html)
static/          # CSS design tokens
tests/           # pytest (unit, integration, smoke)
devops/          # Docker, compose, init-db, scripts, seeds, pgAdmin
docs/            # SDDs, specs, profiles, infra docs
wsgi.py          # Single WSGI entry point (the only one)
```

### Service Domain Structure
Every service follows the same pattern:
```
canary/services/<service_name>/
├── __init__.py          # Service exports
├── routes.py            # Flask blueprint
├── service.py           # Business logic (no Flask imports)
├── models.py            # SQLAlchemy models
└── tests/
    ├── test_service.py      # Unit tests
    ├── test_routes.py       # Route/HTTP contract tests
    └── test_integration.py  # End-to-end data flow tests
```

14 service domains: identity, tsp, chirp, alert, owl, fox, analytics, alx, raas, ops, ui_bff, and supporting services.

---

## Verification Round-Trip

The verification path works without Canary's infrastructure: given a transaction, compute its leaf hash, reconstruct the Merkle proof against the inscribed root on Bitcoin. If the proof passes, the transaction is verified as included in the batch — no database required, no server required. This is the "math, not trust" principle in action.

Batch-to-event join uses `evidence_records.batch_id` (direct FK, no time-range gaps). L1-only verification is possible: download the inscription, extract the Merkle root, reconstruct the proof from the event hash.

---

*Canary LP | GrowDirect Inc. | Confidential*
