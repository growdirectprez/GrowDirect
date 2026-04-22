# External Identities

**Service Type:** App Service (Canary)
**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]
**Architecture:** [[docs/sdds/canary/architecture|Canary Architecture SDD]]
**Linear:** GRO-267
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[docs/team/Architect|Architect]] · **Operator role:** [[docs/team/Engineer|Engineer]]

---

## Purpose

External Identities is the POS-agnostic entity resolution subsystem. It maintains
the canonical mapping between Canary's internal UUIDs and the identifiers used by
each connected source system (Square, Clover, Toast, etc.). Every entity in
Canary -- employee, location, device, product, customer -- has a permanent internal
UUID that belongs to the merchant, not to any POS system. Source system IDs are
metadata about the connection, not the identity itself.

The service completes the Identity Triangle:

```
source_systems          What POS platforms exist (square, clover, toast)
    |
merchant_sources        Which platforms this merchant has connected
    |
external_identities     How each entity maps to each platform's ID
```

---

## Dependencies

| Dependency | Type | Status | Notes |
|------------|------|--------|-------|
| PostgreSQL (`canary` DB, `app` schema) | Database | Live | Table `app.external_identities` |
| `source_systems` table | Reference data | Live | FK target for `source_code` |
| `merchant_sources` table | Reference data | Live | Tracks active POS connections per merchant |
| TenantMixin | Model mixin | Live | Provides `merchant_id` scoping + FK to `merchants` |
| AuditMixin | Model mixin | Live | Provides `created_at`, `updated_at`, `created_by`, `modified_by` |
| Entity models | Live | Live | employees, locations, devices, products, customers |

No external service dependencies. No Valkey usage. No Ollama usage.

---

## Data Flow & PII Map

### What Enters

| Source | Data | Format |
|--------|------|--------|
| TSP Sub2 (parse-route) | Employee, customer, location entity sync from Square webhooks | Parsed dict with `square_employee_id`, `square_customer_id`, `square_location_id` |
| Initial merchant sync | Bulk entity import during onboarding | List of `{entity_type, entity_id, external_id}` dicts |
| Future POS integrations | Entity mappings from Clover, Toast, etc. | Same dict format, different `source_code` |

### What's Stored

**Table: `app.external_identities`**

| Column | Type | PII Classification | Encryption | Notes |
|--------|------|-------------------|------------|-------|
| `id` | String(36) PK | public | None | Canary-generated UUID |
| `merchant_id` | String(36) FK | internal | None | Tenant scope key |
| `entity_type` | String(30) | public | None | CHECK: employee, location, device, product, customer |
| `entity_id` | String(36) | internal | None | Canary's internal UUID for the entity |
| `source_code` | String(50) | public | None | Source system identifier (e.g., 'square') |
| `external_id` | String(255) | internal | None | Source system's native ID for this entity |
| `is_primary` | Boolean | public | None | Default true. Marks authoritative source |
| `created_at` | DateTime(tz) | public | None | server_default=now() |
| `updated_at` | DateTime(tz) | public | None | server_default=now(), onupdate=now() |
| `created_by` | String(36) | internal | None | AuditMixin field |
| `modified_by` | String(36) | internal | None | AuditMixin field |

**PII note:** The `external_id` column stores source system identifiers (e.g.,
Square's `TM5_NpkYj2BsDrbt`). These are opaque vendor IDs, not human-readable
PII. However, they constitute a cross-reference that could be used to correlate
records across systems. Classification: **internal** -- visible to authenticated
users within the merchant's tenant, not encrypted at rest.

The `entity_id` column points to entity tables that DO contain PII (employee
names, customer emails, location addresses). External Identities itself does not
store PII directly but acts as a resolution bridge to tables that do.

**Constraints:**

| Constraint | Type | Columns | Purpose |
|-----------|------|---------|---------|
| `uq_ext_id_merchant_source_entity` | UNIQUE | (merchant_id, source_code, entity_type, external_id) | One mapping per source system ID |
| `uq_ext_id_merchant_entity_source` | UNIQUE | (merchant_id, entity_type, entity_id, source_code) | One source mapping per entity per system |
| `ix_ext_id_lookup` | INDEX | (merchant_id, source_code, entity_type, external_id) | Fast forward resolution |
| `ix_ext_id_reverse` | INDEX | (merchant_id, entity_type, entity_id) | Fast reverse resolution |
| `ix_ext_id_merchant` | INDEX | (merchant_id) | Tenant-level queries |
| `ck_ext_id_entity_type` | CHECK | entity_type | IN ('employee', 'location', 'device', 'product', 'customer') |

### What Exits

| Consumer | Data Provided | Notes |
|----------|--------------|-------|
| TSP Sub2 parser | Canary UUID for entity (forward resolution) | On entity sync during webhook processing |
| Owl search builder | Entity join resolution (planned Phase 3) | Not yet consuming |
| RaaS verification | Entity-level identity in receipt verification (planned) | Not yet consuming |
| Chirp rule engine | Cross-source entity resolution (planned) | Not yet consuming |
| Dashboard queries | Entity lookup and display (planned) | Not yet consuming |
| Fox cases | Entity references that survive POS migration (planned) | Not yet consuming |
| Identity MCP tools | Entity resolution across source systems (planned) | Not yet consuming |

---

## API Contract

### Resolution Functions

Located in `canary/services/identity/external_id_resolver.py`:

```python
def resolve_to_canary(
    session: Session, merchant_id: str, source_code: str,
    entity_type: str, external_id: str,
) -> Optional[str]:
    """Forward: source system ID -> Canary entity UUID. Returns None if not found."""

def resolve_to_external(
    session: Session, merchant_id: str, entity_type: str,
    entity_id: str, source_code: str = None,
) -> list[dict]:
    """Reverse: Canary UUID -> source system ID(s).
    Returns list of {source_code, external_id, is_primary}.
    Optionally filter by source_code."""

def register_external_id(
    session: Session, merchant_id: str, entity_type: str,
    entity_id: str, source_code: str, external_id: str,
    is_primary: bool = True,
) -> ExternalIdentity:
    """Register or update a source system mapping. Idempotent.
    If mapping exists for (merchant, entity, source), updates external_id and is_primary.
    Otherwise creates a new row."""

def bulk_register(
    session: Session, merchant_id: str, source_code: str,
    mappings: list[dict],
) -> int:
    """Batch registration during initial sync.
    Each mapping: {entity_type, entity_id, external_id}.
    Returns count of new records created. Skips existing mappings."""
```

### Resolution Patterns

**Forward Resolution (Source -> Canary):**
A webhook arrives with employee_id `TM123`. The parser resolves it to the
canonical Canary UUID before any write to the sales ledger.

```sql
SELECT entity_id FROM app.external_identities
WHERE merchant_id = :merchant_id
  AND source_code = 'square'
  AND entity_type = 'employee'
  AND external_id = 'TM123';
```

**Reverse Resolution (Canary -> Source):**
Canary needs to refresh employee data from the Square API and must provide
Square's native ID.

```sql
SELECT external_id, source_code FROM app.external_identities
WHERE merchant_id = :merchant_id
  AND entity_type = 'employee'
  AND entity_id = 'abc-123';
```

**Cross-Source Resolution (Source A -> Source B):**
The same employee appears in two systems and Canary bridges between them through
the shared Canary UUID.

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

### Parser Integration Pattern

Every parser registers the source system mapping through `external_identities`
at entity creation time. Currently implemented in `sub2_parse.py` for employee,
customer, and location entities:

```python
from canary.services.identity.external_id_resolver import register_external_id

register_external_id(
    session, merchant_id,
    entity_type="employee",
    entity_id=employee.id,
    source_code="square",
    external_id=payload["id"],
)
```

### No HTTP Routes

External Identities has no HTTP API. All access is through the resolver functions
called internally by other services. No public endpoints exist.

---

## Entity Type Coverage

| Entity Type | Cardinality | Dual-Write Status | Description |
|-------------|-------------|-------------------|-------------|
| `employee` | 1 per employee per source | Live (Sub2) | Staff records -- cashiers, managers, supervisors |
| `location` | 1 per location per source | Live (Sub2) | Physical stores, warehouses, mobile units |
| `device` | 1 per device per source | Not implemented | POS terminals, iPads, card readers |
| `product` | 1 per product per source | Not implemented | Catalog items, SKUs, PLUs |
| `customer` | 1 per customer per source | Live (Sub2) | Customer profiles for loyalty and return tracking |

### Transaction Table -- Denormalized Source IDs

The `sales.transactions` table carries `location_id`, `employee_id`, and
`device_id` as denormalized source system IDs for query performance on the
append-only ledger. These are the source system's native identifiers, written at
ingestion time for fast filtering without joins. The entity tables hold the
canonical identity. `external_identities` is the bridge between them.

### Vendor-Prefixed Columns on Entity Models (Current State)

Entity models still carry vendor-prefixed columns that duplicate what
`external_identities` stores:

- `employees.square_employee_id` (String(36), NOT NULL, indexed)
- `locations.square_location_id` (String(36), NOT NULL, indexed)

These are Phase 3 removal targets. The dual-write pattern in Sub2 currently
writes to BOTH the vendor column on the entity table AND the
`external_identities` bridge table. Phase 3 migrates all consumers to the bridge
table, then drops the vendor columns via Alembic.

---

## Design Principles

### 1. Canary UUID Is the Primary Key -- Always

Every entity table uses a Canary-generated UUID as its primary key. Source system
IDs are never used as primary keys, foreign keys, or join targets between
Canary-owned tables.

### 2. Source System IDs Are Metadata

A source system identifier is stored in `external_identities`, not on the entity
table itself. Entity tables should carry no vendor-prefixed columns. (Current
state: employees and locations still have `square_*` columns pending Phase 3.)

### 3. Identity Survives POS Migration

When a merchant disconnects Square and connects Clover, their entities retain
their Canary UUIDs. Old Square mappings remain (marked `is_primary=false`). New
Clover mappings are added. Every alert, case, risk score, and metric that
referenced those entities continues to resolve correctly.

### 4. Resolution Is Bidirectional

Forward (source -> Canary), reverse (Canary -> source), and cross-source
(Source A -> Source B) resolution all use the same bridge table.

### 5. One Bridge Table, Not N Vendor Columns

Adding a new POS integration requires zero schema changes. Register a new
`source_code` in `source_systems`, then `external_identities` rows are written
by the new parser. No Alembic migration. No column additions.

---

## Operations

### Startup Sequence

External Identities is a service module within the Canary Flask app. It has no
independent startup. The `ExternalIdentity` model is registered via
`canary/models/app/__init__.py` when the app starts. The resolver functions in
`canary/services/identity/external_id_resolver.py` are imported on demand by
consumers (currently Sub2 parser).

### Health Checks

No dedicated health check for External Identities. Service health is implicitly
validated through:

1. Database connectivity (Canary app health check covers PostgreSQL)
2. Table existence (Alembic migration `gro267a00001`)
3. Sub2 parser successful entity sync (TSP pipeline health)

### Failure Modes

| Failure | Impact | Behavior |
|---------|--------|----------|
| PostgreSQL down | All resolution fails | Sub2 parser fails on entity sync, TSP pipeline halts |
| Missing source_code in source_systems | Registration fails | FK violation if enforced; currently no FK in migration |
| Duplicate external_id for same source | UNIQUE constraint violation | `register_external_id` handles via upsert (idempotent) |
| Entity table FK target missing | Orphaned mapping | No FK from `entity_id` to entity tables -- orphan possible |
| Bulk registration timeout | Partial sync | `bulk_register` is not transactional per-batch -- partial writes possible |

### Monitoring

No monitoring currently configured. Recommended alerts:

- Orphaned mappings: `external_identities` rows where `entity_id` has no match
  in the corresponding entity table
- Missing mappings: Entity rows (employees, locations) with no corresponding
  `external_identities` entry
- Stale `is_primary` flags: Multiple primary sources for the same entity

### Configuration

No environment variables. No feature flags. The service is always active when
the Canary app is running.

---

## Deployment

### Docker Service Definition

External Identities is part of the Canary Flask app container. No separate
service or container.

```yaml
# In Canary/devops/docker-compose.yml
canary-app:
  image: canary-app
  ports: ["5001:5001"]
  # external_identities is a module within this container
```

### AWS Target

| Component | AWS Service | Notes |
|-----------|------------|-------|
| Application | ECS/Fargate (Canary task) | Part of main Canary container |
| Database | RDS PostgreSQL 17 | `canary` DB, `app` schema |
| Secrets | AWS Secrets Manager | DB credentials (not used by this module directly) |

### CI/CD Requirements

- Alembic migration `gro267a00001` must run before app startup
- Unit tests: `python3 -m pytest tests/unit/test_external_identities.py`
- No integration tests exist yet (see P1 findings)

---

## RaaS Integration

### Namespace Resolution Layers

RaaS provides identity resolution at two levels:

**Merchant level (live):**
```
.jeffe GUID -> namespace_registrations -> merchant_id -> merchant_sources -> source_code
```

**Entity level (via external_identities):**
```
.jeffe GUID -> merchant_id -> external_identities -> entity resolution
```

### Receipt Verification Flow

```
POST /v1/verify
  { event_hash: "abc...", identifier: "sunrise-coffee.jeffe" }

1. Resolve "sunrise-coffee.jeffe" -> namespace_guid -> merchant_id
2. Verify event_hash against L1 inscription
3. If include_entities: true, resolve entity IDs in the receipt:
   - employee_id "TM123" -> external_identities -> Canary employee UUID
   - device_id "DEV456" -> external_identities -> Canary device UUID
   - location_id "LOC789" -> external_identities -> Canary location UUID
4. Response includes canonical Canary UUIDs alongside source IDs
```

### Device Attestation

The Device Attestation protocol specifies that RaaS verification can include
device integrity data when `include_device: true`. The receipt contains a
source-specific device ID, `external_identities` resolves it to the Canary
device entity, and the device's attestation status is returned.

---

## Goose Integration -- Identity as Billing Anchor

The Goose (GRO-117) monetizes Canary's intelligence via L402 Lightning payments.
External Identities provides the anchor:

```
.jeffe GUID (L1 inscription -- permanent)
  -> namespace_registrations -> merchant_id
    -> external_identities -> entity resolution (POS-agnostic)
      -> goose_payments -> L402 macaroon (merchant_id caveat)
        -> gated access to intelligence about those entities
```

Identity is the foundation that makes detection, analysis, and monetization
trustworthy and permanent. Entity identity survives both POS migration AND
subscription lapse.

---

## Implementation Status

### Phase 1: Foundation -- COMPLETE

- `app.external_identities` table (Alembic migration `gro267a00001`)
- `ExternalIdentity` SQLAlchemy model in `canary/models/app/external_identities.py`
- Resolver functions in `canary/services/identity/external_id_resolver.py`
- Unit tests for model structure and resolver imports

### Phase 2: Parser Dual-Write -- PARTIAL

- Sub2 parser registers mappings for employee, customer, location -- LIVE
- Device and product entity parsers -- NOT YET IMPLEMENTED
- Backfill from existing entity tables -- NOT YET DONE

### Phase 3: Consumer Migration -- NOT STARTED

- Owl search builder migration to `external_identities` join path
- Dashboard and Chirp queries routed through bridge table
- Drop vendor-prefixed columns (`square_employee_id`, `square_location_id`)

### Phase 4: Transaction Source Tagging -- NOT STARTED

- `source_code` column on `sales.transactions`
- Multi-POS transaction disambiguation
- Cross-source Chirp rules

---

## Code Review Findings

### P0 -- Blocks Production

**P0-1: No FK constraint from `external_identities.source_code` to `source_systems.code` in migration**

The model declares `source_code` as `String(50)` but the Alembic migration
(`gro267a00001`) does not create a foreign key constraint to `source_systems.code`.
Any string can be inserted as a source code, including typos and nonexistent
systems. The model file also lacks a `ForeignKey()` declaration -- it documents
the intent in a `doc=` string but does not enforce it.

Recommended fix: Add Alembic migration to create FK constraint
`fk_ext_id_source_code` referencing `app.source_systems(code)`. Add `ForeignKey`
to the model's `source_code` column definition.

**P0-2: No FK from `entity_id` to any entity table -- orphaned mappings possible**

The `entity_id` column is a freeform `String(36)` with no referential integrity.
If an entity is deleted (soft or hard), its `external_identities` rows become
orphans with no detection mechanism. Since the bridge table is the identity
resolution layer, orphaned rows could cause phantom entity references in RaaS
verification and Owl search.

Recommended fix: While a polymorphic FK across 5 entity tables is impractical,
add a scheduled integrity check that detects orphans (query
`external_identities` rows where `entity_id` has no match in the corresponding
entity type table). Log and flag for cleanup.

**P0-3: `bulk_register` is N+1 -- will timeout on large merchant sync**

`bulk_register()` executes one SELECT per mapping to check for existence, then
one INSERT per new mapping. For a merchant with 5,000 products, this is 5,000+
individual queries. At scale, this will timeout or cause connection pool
exhaustion during onboarding sync.

Recommended fix: Rewrite using `INSERT ... ON CONFLICT DO NOTHING` with
`session.execute(insert(...).on_conflict_do_nothing())` for batch efficiency.
Single round-trip per batch.

### P1 -- Before GA

**P1-1: No integration tests for resolver functions**

Unit tests verify model structure and imports only. No tests exercise
`resolve_to_canary`, `resolve_to_external`, `register_external_id`, or
`bulk_register` against a real database. The idempotent upsert behavior of
`register_external_id` is untested with actual DB constraints.

Recommended fix: Write integration tests in `tests/integration/` that create
entities, register mappings, and verify all four resolution functions against
PostgreSQL with constraint enforcement.

**P1-2: Device and product dual-write not implemented**

Sub2 parser registers external identities for employee, customer, and location
but not for device or product entities. Any device or product created during
entity sync has no `external_identities` mapping, meaning forward resolution
will fail for those entity types.

Recommended fix: Add `register_external_id` calls to device and product entity
sync paths in Sub2 parser.

**P1-3: No backfill for existing entities**

Migration `gro267_backfill_external_ids.py` exists but the backfill has not been
verified as complete. Existing entities created before GRO-267 may lack
`external_identities` rows. This means forward resolution fails for pre-existing
entities.

Recommended fix: Run and verify backfill migration. Add a one-time audit query
to confirm all entities have corresponding `external_identities` rows.

**P1-4: No audit logging on identity resolution operations**

`register_external_id` creates and updates identity mappings with no audit trail
beyond the `AuditMixin` timestamps. There is no record of WHO changed a mapping,
no logging when a mapping is updated (external_id changed or is_primary toggled),
and no event emitted for downstream consumers.

Recommended fix: Add structured logging (`logger.info`) for register and update
operations. Populate `created_by` / `modified_by` fields from the session context
(currently always NULL).

**P1-5: `register_external_id` inline import in Sub2 parser**

The Sub2 parser uses `from canary.services.identity.external_id_resolver import
register_external_id` inside function bodies (inline import) rather than at
module level. This pattern is used three times in the same file. Inline imports
bypass linting, hide dependencies, and make circular import issues harder to
diagnose.

Recommended fix: Move imports to module level in `sub2_parse.py`.

**P1-6: No data retention policy for identity mappings**

External identity mappings accumulate indefinitely. When a merchant disconnects a
POS system, old mappings are marked `is_primary=false` but never cleaned up. Over
years of POS migrations, the table will accumulate stale rows.

Recommended fix: Define retention policy (e.g., non-primary mappings older than
24 months auto-archived). Implement as a scheduled cleanup job.

### P2 -- Post-Launch

**P2-1: Vendor-prefixed columns on entity models not yet removed**

`employees.square_employee_id` and `locations.square_location_id` duplicate the
data in `external_identities`. Phase 3 migration will drop these, but until then,
data is written to two places with potential for drift if one write succeeds and
the other fails.

Recommended fix: Complete Phase 3 -- migrate all consumers to use
`external_identities` for resolution, then drop vendor-prefixed columns.

**P2-2: No index on `is_primary` for filtering queries**

Queries that filter for `is_primary = true` (the common case for forward
resolution when multiple sources exist) do a full scan of the filtered result set.
Not critical at current scale but will matter for multi-POS merchants.

Recommended fix: Add composite index
`(merchant_id, entity_type, entity_id, is_primary)` for filtered reverse lookups.

**P2-3: `resolve_to_canary` does not distinguish between "not found" and "multiple found"**

`scalar_one_or_none()` will raise `MultipleResultsFound` if the unique constraint
is violated (should be impossible, but defensive coding matters). The caller gets
an unhandled exception instead of a clear error.

Recommended fix: Wrap in try/except `MultipleResultsFound` with structured error
logging.

---

## Production Readiness Checklist

- [x] Table created via Alembic migration (`gro267a00001`)
- [x] Model uses `Mapped[]` syntax (SQLAlchemy 2.0 compliant)
- [x] TenantMixin provides `merchant_id` scoping
- [x] AuditMixin provides `created_at` / `updated_at`
- [x] Unique constraints enforce one-mapping-per-source invariant
- [x] Indexes cover forward and reverse resolution paths
- [x] Unit tests pass for model structure
- [ ] FK constraint enforced for `source_code` -> `source_systems.code` (P0-1)
- [ ] Orphan detection mechanism for `entity_id` references (P0-2)
- [ ] `bulk_register` rewritten for batch efficiency (P0-3)
- [ ] Integration tests for all resolver functions (P1-1)
- [ ] Device and product dual-write implemented (P1-2)
- [ ] Backfill verified complete for existing entities (P1-3)
- [ ] Audit logging for register/update operations (P1-4)
- [ ] Inline imports moved to module level (P1-5)
- [ ] Data retention policy defined and implemented (P1-6)
- [ ] Secrets in AWS Secrets Manager (not .env) -- N/A for this module
- [ ] Health check endpoint responds -- N/A (no HTTP routes)
- [ ] Rate limiting on public endpoints -- N/A (no public endpoints)
- [ ] Error responses don't leak internals -- N/A (no HTTP routes)

---

*External Identities SDD v2.0 -- Ops Upgrade*
*Service type: App Service (Canary)*
*Parent domain: Identity*
*Related: raas.md (namespace resolution), identity.md (entity models)*
*Source files: canary/models/app/external_identities.py, canary/services/identity/external_id_resolver.py*
