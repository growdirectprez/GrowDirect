---
date: 2026-04-24
type: wiki
tags: [canary, database, models, postgresql, schemas]
sources: [Canary/canary/models/, Canary/canary/models/base.py, Canary/docs/atlas/infrastructure/]
last-compiled: 2026-04-24
needs-review: 2026-05-24
---

# Canary Data Model

## Summary

Canary uses PostgreSQL 17 with **three schemas** that separate concerns: `app` for core platform entities (including Fox case management), `sales` for the Square CRDM (canonical relational data model), and `metrics` for analytics dimensions and facts. The codebase has 60+ SQLAlchemy 2.0 models using `Mapped[]` annotations, UUID primary keys, and `created_at`/`updated_at` timestamps on every table.

**Note on Fox.** The Python source tree has a `canary/models/fox/` directory and the SDDs frequently talk about "the fox schema," but `Canary/canary/models/base.py` defines only three SQLAlchemy `MetaData(schema=...)` instances — `app`, `sales`, `metrics`. Every Fox model class inherits from `AppBase`, so `fox_cases`, `fox_evidence`, `fox_subjects`, etc. all physically live in the `app` schema. The `fox` directory is a Python organizational convention, not a database schema. Treat any reference to a "fox schema" in older docs as shorthand for "Fox tables in the app schema."

## Schema: app (Core Platform)

The `app` schema holds everything that makes Canary a multi-tenant SaaS platform. Key entities:

**Merchants** — The tenant root. Every data row in the system traces back to a merchant_id. Merchants connect via Square OAuth and are onboarded through a sync process that pulls their locations, employees, and catalog.

**Users** — Platform users authenticated via Flask-Login. Magic link is the primary auth method, password is fallback. Sessions are stored in Valkey DB 0.

**Locations** — Physical store locations synced from Square. Each location has business hours (used by after-hours detection rules) and a device inventory.

**Employees** — Synced from Square, cross-referenced with timecards for ghost employee detection. Employee links connect Square employee IDs to Canary user accounts.

**Detection Rules & Merchant Rule Config** — The `detection_rules` table is the database representation of the Chirp rule catalog (seeded on first boot). `merchant_rule_configs` stores per-merchant threshold overrides, enabled/disabled flags, and custom parameters. This is the persistence layer behind the ThresholdManager.

**Alerts & Alert History** — Append-only alert records produced by Chirp. Each alert references a rule_id, merchant, transaction, and severity. The `alert_history` table tracks status transitions (created → acknowledged → escalated → resolved) with timestamped notes.

Other app models: OAuth tokens, feature flags, notifications, notification preferences, subscriptions, organizations, external identities, products, bank accounts, card profiles, and the Vault (merchant memory locker) and Owl memory tables.

## Schema: sales (Square CRDM)

The `sales` schema is the canonical representation of everything Square sends. It is the single source of truth for merchant transaction data and the primary input to Chirp detection. Key entities:

**Transactions** — Append-only ledger. Every Square payment, refund, void, no-sale, paid-in/out, and exchange logs a row. Indexed on merchant+date, merchant+employee, merchant+location, merchant+card_fingerprint, and merchant+order. The CRDM reference table with 7 canonical sources.

**Evidence Records** — Write-once, immutable. Every byte that enters TSP Sub 1 exits exactly as received. No UPDATE, no DELETE — enforced by database triggers. Chain hashes link each record to its predecessor within a merchant's evidence chain, creating a tamper-evident sequence. This is the forensic backbone.

**Ingestion Log** — Per-event tracking: receipt → processing → completion/failure. Essential for retry logic, audit trail, and dead letter queue management. Uniquely constrained on source + source_event_id.

**Line Items** — Order-level detail: line items, modifiers, taxes, discounts, service charges. Powers the sweethearting detection rules (C-201 through C-204).

**Supporting tables**: tenders (payment methods per transaction), cash drawers, timecards, gift cards, loyalty events, inventory, invoices, payouts, disputes, devices, terminal records, order returns, order rewards, and inscription records (for Bitcoin anchoring).

## Fox tables (Case Management — within `app` schema)

Fox is the investigation layer. The Python module `canary/models/fox/`
groups its models for readability, but every class inherits from
`AppBase`, which means every Fox table physically lives in the `app`
schema. There is no separate `fox` schema. The seven Fox tables
(`fox_cases`, `fox_case_alerts`, `fox_case_timeline`, `fox_case_actions`,
`fox_subjects`, `fox_evidence`, `fox_evidence_access_log`) split into
operational, append-only, and INSERT-only integrity tiers — see
[[canary-fox-case-management|Fox Case Management]] for the full breakdown.

Selected highlights:

**FoxCase** (`fox_cases`) — Root investigation record. Status flow: open → investigating → pending_review → escalated → closed / referred_to_le. Classified by type (theft, fraud, policy_violation, cash_variance, return_abuse, transaction_review, other). Tracks priority, assigned investigator, aggregate loss amount, and resolution narrative.

**FoxEvidence** (`fox_evidence`) — INSERT-ONLY evidence chain enforced at the PostgreSQL trigger layer. Each row stores a file reference with a SHA-256 content hash and a chain hash linking to the previous evidence record. Cryptographic proof of insertion order and integrity — the chain of custody is the table itself. Evidence types: document, photo, video, receipt, screenshot, export.

**FoxSubject** (`fox_subjects`) — People or entities of interest. Subject types: employee, customer, vendor, unknown. Soft-deletable for historical tracking. Links to the actual entity record (e.g., Square employee ID) when available.

## Schema: metrics (Analytics)

Dimension tables and fact tables powering the merchant dashboard:

**Dimensions**: merchant, location, employee, and time (fiscal calendar). The fiscal calendar service generates time dimension rows for period-level aggregation.

**Facts**: period metrics (aggregated transaction counts, amounts, refund rates, void rates per period) and risk scores (per-entity risk assessments computed from Chirp alert history and case outcomes).

## Immutability Patterns

Two tables enforce write-once semantics at the database level with triggers: `evidence_records` (sales schema) and `fox_evidence` (app schema, despite the `models/fox/` module path). Neither model exposes update() or delete() methods. Any attempt to modify or remove a row fails at the PostgreSQL trigger layer. This is a deliberate design decision for forensic integrity — loss prevention evidence must be tamper-proof.

## Related

- [[Brain/wiki/canary-architecture|Canary Architecture]] — System overview and service mesh
- [[Brain/wiki/canary-detection|Canary Detection Engine]] — How Chirp uses these tables
- [[Brain/projects/Canary|Canary MOC]] — Links to ERD diagrams and field registry

## Sources

- `Canary/canary/models/` — All 60+ model files across 4 Python packages (`app/`, `sales/`, `fox/`, `metrics/`) but only 3 PostgreSQL schemas (`app`, `sales`, `metrics`); Fox models inherit from `AppBase`
- `Canary/canary/models/base.py` — Base classes, mixins (TenantMixin, AuditMixin, SoftDeleteMixin)
- `Canary/canary/models/app/detection.py` — Detection rules and alert models
- `Canary/canary/models/sales/transactions.py` — Core transaction model
- `Canary/canary/models/sales/evidence.py` — Write-once evidence records
- `Canary/canary/models/fox/cases.py` — Case management model
- `Canary/canary/models/fox/evidence.py` — Fox evidence chain
- `Canary/docs/atlas/infrastructure/fig-i02-database-schema-architecture.md` — Schema ERD
