# External Identities

## Overview

Every entity in Canary — employee, location, device, product, customer — has a
permanent internal UUID that belongs to the merchant, not to any POS system.
The External Identities subsystem maintains the canonical mapping between these
UUIDs and the identifiers used by each connected source system.

This is a data integrity principle: **Canary owns identity. Source systems
provide identifiers.** An employee is an employee because Canary says so. The
fact that Square calls them `TM5_NpkYj2BsDrbt` and Clover calls them `CLV-456`
is metadata about the connection, not the identity itself.

**The Identity Triangle:**

```
source_systems          What POS platforms exist (square, clover, toast)
    ↓
merchant_sources        Which platforms this merchant has connected
    ↓
external_identities     How each entity maps to each platform's ID
```

`source_systems` and `merchant_sources` are already live. `external_identities`
completes the triangle and makes entity identity source-agnostic at every layer
of the stack.

**Owns:** `app.external_identities` table, identity resolution functions, parser
integration pattern.

**Consumed by:** TSP parsers, Owl search, RaaS verification, Chirp rule engine,
dashboard queries, Fox case references, Identity MCP tools.

---

## Design Principles

### 1. Canary UUID Is the Primary Key — Always

Every entity table uses a Canary-generated UUID as its primary key. This UUID
is the canonical identifier used in all internal lookups, cache keys, API
responses, alert references, and case files. Source system IDs are never used
as primary keys, foreign keys, or join targets between Canary-owned tables.

### 2. Source System IDs Are Metadata

A source system identifier (Square's `TM5_NpkYj2BsDrbt`, Clover's `CLV-456`)
describes how an external system refers to an entity. It is stored in
`external_identities`, not on the entity table itself. Entity tables carry no
vendor-prefixed columns (`square_*`, `clover_*`).

### 3. Identity Survives POS Migration

When a merchant disconnects Square and connects Clover, their employees,
locations, devices, and products retain their Canary UUIDs. The old Square
mappings remain in `external_identities` (marked `is_primary=false`). New Clover
mappings are added. Every alert, case, risk score, and metric that referenced
those entities continues to resolve correctly.

### 4. Resolution Is Bidirectional

Forward resolution (source ID → Canary UUID) serves inbound data: a webhook
arrives with a Square employee ID and the parser resolves it to the canonical
UUID before writing.

Reverse resolution (Canary UUID → source ID) serves outbound calls: Canary
needs to refresh employee data from the Square API and must provide Square's
native ID.

Cross-source resolution (Source A ID → Source B ID) serves multi-POS merchants:
the same employee appears in two systems and Canary can bridge between them
through the shared Canary UUID.

### 5. One Bridge Table, Not N Vendor Columns

Adding a new POS integration requires zero schema changes. Register a new
`source_code` in `source_systems`, then `external_identities` rows are written
by the new parser. No Alembic migration. No column additions. No model changes.

---

## Data Model

### external_identities

Bridge table mapping Canary entities to source system identifiers. Lives in
`app` schema alongside `source_systems` and `merchant_sources`.

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `id` | String(36) PK | NOT NULL | uuid4 |
| `merchant_id` | String(36) FK | NOT NULL | → merchants.id (tenant scope) |
| `entity_type` | String(30) | NOT NULL | CHECK: employee, location, device, product, customer |
| `entity_id` | String(36) | NOT NULL | Canary's internal UUID for the entity |
| `source_code` | String(50) FK | NOT NULL | → source_systems.code (e.g., 'square') |
| `external_id` | String(255) | NOT NULL | The source system's ID for this entity |
| `is_primary` | Boolean | NOT NULL | Default true. Marks the authoritative source |
| `created_at` | DateTime(tz) | NOT NULL | server_default=now() |
| `updated_at` | DateTime(tz) | NOT NULL | server_default=now() |

**Constraints:**

| Constraint | Type | Columns | Purpose |
|-----------|------|---------|---------|
| `uq_ext_id_merchant_source_entity` | UNIQUE | (merchant_id, source_code, entity_type, external_id) | One mapping per source system ID |
| `uq_ext_id_merchant_entity_source` | UNIQUE | (merchant_id, entity_type, entity_id, source_code) | One source mapping per entity per system |
| `ix_ext_id_lookup` | INDEX | (merchant_id, source_code, entity_type, external_id) | Fast forward resolution |
| `ix_ext_id_reverse` | INDEX | (merchant_id, entity_type, entity_id) | Fast reverse resolution |
| `ck_entity_type` | CHECK | entity_type | IN ('employee', 'location', 'device', 'product', 'customer') |

**Mixins:** TenantMixin, AuditMixin.

**Access pattern:** CRUD. Written by parsers during entity sync. Read by any
service that resolves between source system IDs and Canary UUIDs.

---

## Resolution Patterns

### Forward Resolution (Source → Canary)

"A webhook arrived with employee_id `TM123`. What is the canonical UUID?"

```sql
SELECT entity_id FROM app.external_identities
WHERE merchant_id = :merchant_id
  AND source_code = 'square'
  AND entity_type = 'employee'
  AND external_id = 'TM123';
```

Used by: TSP parsers when processing inbound webhooks. The source system ID is
resolved to a Canary UUID before any write to the sales ledger.

### Reverse Resolution (Canary → Source)

"Canary employee `abc-123` — what does Square call them?"

```sql
SELECT external_id, source_code FROM app.external_identities
WHERE merchant_id = :merchant_id
  AND entity_type = 'employee'
  AND entity_id = 'abc-123';
```

Used by: Outbound API calls that require the source system's native ID (e.g.,
refreshing employee data from the Square Team Members API).

### Cross-Source Resolution (Source A → Source B)

"Employee `TM123` in Square — what is their Clover ID?"

```sql
SELECT b.external_id
FROM app.external_identities a
JOIN app.external_identities b
  ON a.entity_id = b.entity_id
  AND a.merchant_id = b.merchant_id
  AND a.entity_type = b.entity_type
WHERE a.merchant_id = :merchant_id
  AND a.source_code = 'square'
  AND a.entity_type = 'employee'
  AND a.external_id = 'TM123'
  AND b.source_code = 'clover';
```

Used by: Multi-POS merchants and RaaS receipt verification when the caller
provides a source-specific ID and the receipt originated from a different system.

---

## Entity Type Coverage

| Entity Type | Cardinality | Description |
|-------------|-------------|-------------|
| `employee` | 1 per employee per source | Staff records — cashiers, managers, supervisors |
| `location` | 1 per location per source | Physical stores, warehouses, mobile units |
| `device` | 1 per device per source | POS terminals, iPads, card readers |
| `product` | 1 per product per source | Catalog items, SKUs, PLUs |
| `customer` | 1 per customer per source | Customer profiles for loyalty and return tracking |

### Transaction Table — Denormalized Source IDs

The `sales.transactions` table carries `location_id`, `employee_id`, and
`device_id` as denormalized source system IDs for query performance on the
append-only ledger. These are not Canary UUIDs — they are the source system's
native identifiers, written at ingestion time for fast filtering without joins.

The entity tables hold the canonical identity. The transaction table holds the
receipt-level reference. `external_identities` is the bridge between them.

When a second POS source writes to the sales ledger, a `source_code` column is
added to `sales.transactions` to disambiguate which system generated each row.

---

## RaaS Integration

### Namespace Resolution Layers

RaaS provides identity resolution at two levels:

**Merchant level (live):**

```
.jeffe GUID → namespace_registrations → merchant_id → merchant_sources → source_code
```

"Which POS systems has this merchant connected?"

**Entity level (via external_identities):**

```
.jeffe GUID → merchant_id → external_identities → entity resolution
```

"Given a receipt that references employee TM123, which canonical employee entity
does that resolve to — regardless of which POS generated the receipt?"

### Receipt Verification Flow

```
POST /v1/verify
  { event_hash: "abc...", identifier: "sunrise-coffee.jeffe" }

1. Resolve "sunrise-coffee.jeffe" → namespace_guid → merchant_id
2. Verify event_hash against L1 inscription
3. If include_entities: true, resolve entity IDs in the receipt:
   - employee_id "TM123" → external_identities → Canary employee UUID
   - device_id "DEV456" → external_identities → Canary device UUID
   - location_id "LOC789" → external_identities → Canary location UUID
4. Response includes canonical Canary UUIDs alongside source IDs
```

An insurer verifying a receipt does not need to know which POS system generated
it. They receive Canary's canonical entity UUIDs — permanent, POS-agnostic
identifiers that resolve consistently regardless of whether the merchant later
changes systems.

### Device Attestation

The Device Attestation protocol specifies that RaaS verification can include
device integrity data when `include_device: true`. The receipt contains a
source-specific device ID → `external_identities` resolves it to the Canary
device entity → the device's attestation status is returned. The attestation
is bound to the canonical device, not to any particular POS system's identifier.

---

## Service API

### Resolution Functions

Located in `canary/services/identity/external_id_resolver.py`:

```python
def resolve_to_canary(
    session, merchant_id: str, source_code: str,
    entity_type: str, external_id: str,
) -> Optional[str]:
    """Forward: source system ID → Canary entity UUID."""

def resolve_to_external(
    session, merchant_id: str, entity_type: str,
    entity_id: str, source_code: str = None,
) -> list[dict]:
    """Reverse: Canary UUID → source system ID(s)."""

def register_external_id(
    session, merchant_id: str, entity_type: str,
    entity_id: str, source_code: str, external_id: str,
    is_primary: bool = True,
) -> ExternalIdentity:
    """Register or update a source system mapping. Idempotent."""

def bulk_register(
    session, merchant_id: str, source_code: str,
    mappings: list[dict],
) -> int:
    """Batch registration during initial sync. Returns count created."""
```

### Parser Integration Pattern

Every parser registers the source system mapping through `external_identities`
at entity creation time:

```python
employee = Employee(
    id=generate_uuid(),
    merchant_id=merchant_id,
    employee_name=payload["given_name"],
)
session.add(employee)

register_external_id(
    session, merchant_id,
    entity_type="employee",
    entity_id=employee.id,
    source_code="square",
    external_id=payload["id"],
)
```

This pattern is identical for every entity type and every source system. Adding
Clover support means writing a Clover parser that calls the same
`register_external_id` function with `source_code="clover"`.

---

## Implementation Phases

### Phase 1: Foundation

- `app.external_identities` table (Alembic migration)
- `ExternalIdentity` SQLAlchemy model
- Resolver functions (`external_id_resolver.py`)
- Backfill from existing entity tables
- Unit and integration tests for all resolution patterns

### Phase 2: Parser Dual-Write

- Entity parsers register mappings in `external_identities` alongside existing
  entity writes
- Entity upsert functions in TSP consumers updated
- Integration tests verify dual-write correctness

### Phase 3: Consumer Migration

- Owl search builder: entity joins routed through `external_identities`
- Dashboard and Chirp queries: resolve via `external_identities`
- Drop vendor-prefixed columns from entity models (Alembic migration)

### Phase 4: Transaction Source Tagging

- `source_code` column on `sales.transactions` (default 'square')
- Multi-POS transaction disambiguation
- Cross-source Chirp rules activated

---

## Owl Search Impact

The Owl search builder joins entity tables to resolve natural language queries
("show me transactions by employee John"). The join path routes through
`external_identities`:

```
transactions.employee_id (source ID)
  → external_identities.external_id
      WHERE source_code = 'square' AND entity_type = 'employee'
  → external_identities.entity_id
  → employees.id
  → employees.employee_name
```

During Phases 1-2, existing direct joins remain functional. Phase 3 migrates
Owl to the `external_identities` join path.

---

## Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| `source_systems` table | Live | Reference table, 'square' code seeded |
| `merchant_sources` table | Live | Tracks active POS connections per merchant |
| TenantMixin | Live | Provides merchant_id scoping |
| AuditMixin | Live | Provides created_at, updated_at |
| Entity models | Live | employees, locations, devices, products, customers |

No new external dependencies. No new packages. No new services.

---

## Depended On By

| Consumer | Integration |
|----------|-------------|
| TSP parsers (Sub2) | Register entity mappings during webhook processing |
| Owl search builder | Entity join resolution |
| RaaS verification | Entity-level identity in receipt verification |
| Chirp rule engine | Cross-source entity resolution for detection rules |
| Dashboard queries | Entity lookup and display |
| Fox cases | Entity references that survive POS migration |
| Identity MCP tools | Entity resolution across source systems |

---

## The Principle

A merchant's data belongs to the merchant. Their employees, their stores, their
devices, their products — these are business assets with permanent identities.
The POS system is a connection, not an identity. When that connection changes,
the data stays. The risk scores stay. The case files stay. The detection history
stays.

The `.jeffe` namespace preserves merchant identity. `external_identities`
preserves entity identity. Together, they ensure that Canary's value proposition
is permanent — it does not depend on which wire the data came in on.

---

## Goose Integration — Identity as Billing Anchor

The Goose (GRO-117) monetizes Canary's intelligence via L402 Lightning payments.
External Identities provides the anchor:

**The identity chain:**

```
.jeffe GUID (L1 inscription — permanent)
  → namespace_registrations → merchant_id
    → external_identities → entity resolution (POS-agnostic)
      → goose_payments → L402 macaroon (merchant_id caveat)
        → gated access to intelligence about those entities
```

**What this means:**

- The merchant pays for access to intelligence about THEIR entities — their
  employees, their locations, their devices. The macaroon's `merchant_id` caveat
  scopes access to the namespace that owns those entity mappings.

- Entity identity survives both POS migration AND subscription lapse. When a
  merchant's L402 token expires, the data and identity mappings remain. Re-subscribe
  = re-mint macaroon = instant access restoration. No data loss, no re-onboarding.

- Receipt verification (RaaS) resolves entities through `external_identities`.
  When a third-party agent pays an L402 micropayment to verify a receipt, the
  entity resolution returns Canary UUIDs — permanent identifiers that the verifier
  can trust regardless of which POS generated the receipt.

- The `.jeffe` inscription on L1 provides cryptographic proof that this merchant
  existed, these entities were registered, and these payments were made. The
  identity layer and the payment layer converge on the same immutable record.

Identity is the foundation that makes detection, analysis, and monetization
trustworthy and permanent.

---

*External Identities SDD v1.0*
*Parent domain: Identity*
*Related: raas.md (namespace resolution), identity.md (entity models)*
