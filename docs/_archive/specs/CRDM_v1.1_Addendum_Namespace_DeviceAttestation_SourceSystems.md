---
type: spec
domain: raas
status: active
created: 2026-03-14
updated: 2026-03-19
---
# CRDM v1.1 Addendum — Namespace Bridge, Device Attestation Storage, Source System Refactor

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

**Version:** 1.1-B
**Date:** March 3, 2026
**Author:** ALX (Chief of Staff), Tom (Systems Architect)
**Classification:** MAXIMUM CONFIDENTIAL — Schema Addendum
**Base Document:** `CRDM_v1.0.md` → `CRDM_v1.1_Amendment_POS_Agnostic_Entity_Model.md`
**Source Issues:** GRO-47, GRO-46, GRO-13, GRO-45, GRO-54, GRO-55
**Routes To:** Tom (DDL validation), Jeremy (migration implementation), Jim (QA)
**Gate:** Tom validates all DDL. Jim QA reviews migration plan.
**Tom Review Applied:** T-1 (FK), T-2 (batch_id join), T-3 (namespace+seq unique), T-4 (updated_at triggers), T-5 (leaf_count consolidated), T-7 (source_systems comment), T-9 (naming convention), T-10 (is_enabled BOOLEAN)

---

## 0. Purpose

This addendum consolidates three schema changes that emerged from the four-issue alignment review (GRO-47/46/13/45). Each change was designed in the Alignment Amendment work order. This document is the **build-ready DDL** — the migration script that Jeremy runs.

**What this document is:** The single source of truth for new tables and schema modifications required by the elJeffe Protocol, Namespace Registration, Device Attestation, and Source System expansion.

**What this document is not:** A design rationale document. For design decisions, see the Alignment Amendment and individual PRDs.

---

## 1. Schema Map — What's New

```
canary_app schema (existing):
  ├── merchants                    (unchanged)
  ├── external_identities          (MODIFIED — Amendment C: CHECK → FK)
  ├── devices                      (unchanged — from GRO-45 Amendment 8)
  ├── transaction_devices          (unchanged — from GRO-45 Amendment 8)
  ├── namespace_registrations      (NEW — Amendment A, GRO-58: GUID-based)
  ├── namespace_aliases            (NEW — GRO-58: L2 alias cache)
  ├── source_systems               (NEW — Amendment C)
  └── merchant_feature_flags       (NEW — Device Attestation)

canary_sales schema (existing):
  ├── evidence_records             (MODIFIED — T-2: add batch_id for direct verification join)
  ├── chirp_alerts                 (unchanged)
  └── merkle_batches               (NEW — Inscription Pipeline, T-1: FK to namespace_registrations, T-3: unique namespace+seq)
```

---

## 2. New Table: `namespace_registrations`

**Purpose:** Bridge between `.jeffe` namespace GUIDs and CRDM `merchant_id` UUIDs. Architecturally classified as an L3 hot cache — the source of truth is the Bitcoin L1 inscription. This table is rebuildable from on-chain data.

> **GRO-58 (Jeffe directive, March 3):** L1 inscriptions use pseudonymous GUIDs, not human-readable names. Human-readable aliases live on L2 (Avalanche NameRegistry). This table caches GUID→merchant_id. Alias→GUID mapping is an L2 concern (see `namespace_aliases` cache table below).

**PRD Reference:** `PRD_Namespace_Registration_v1.0.md`

```sql
-- ============================================================
-- Table: namespace_registrations
-- Amendment: A (Namespace GUID → CRDM Merchant Bridge)
-- Schema: canary_app
-- GRO-58: GUID-based namespace (anonymized identity architecture)
-- ============================================================

CREATE TABLE canary_app.namespace_registrations (
    id                  UUID            NOT NULL DEFAULT gen_random_uuid(),
    merchant_id         UUID            NOT NULL,
    namespace_guid      UUID            NOT NULL,   -- Pseudonymous L1 identifier
    namespace_root      TEXT            NOT NULL DEFAULT 'jeffe',  -- Supports future roots
    inscription_id      TEXT,                       -- Bitcoin Ordinal inscription ID
    inscription_block   BIGINT,                     -- Block height of inscription
    avalanche_address   TEXT,                       -- NameRegistry contract address on subnet
    tier                TEXT            NOT NULL DEFAULT 'standard',
    status              TEXT            NOT NULL DEFAULT 'active',
    registered_at       TIMESTAMPTZ     NOT NULL DEFAULT now(),
    expires_at          TIMESTAMPTZ,                -- Annual renewal (GRO-13 Decision 3)
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),

    CONSTRAINT pk_namespace_registrations PRIMARY KEY (id),
    CONSTRAINT fk_nr_merchant FOREIGN KEY (merchant_id)
        REFERENCES canary_app.merchants(merchant_id) ON DELETE CASCADE,
    CONSTRAINT uix_nr_namespace_guid UNIQUE (namespace_guid),
    CONSTRAINT chk_nr_tier CHECK (tier IN ('free', 'standard', 'enterprise')),
    CONSTRAINT chk_nr_status CHECK (status IN (
        'registered', 'active', 'expired', 'suspended'
    ))
);

-- Hot lookup: resolve GUID → merchant_id (RaaS /v1/verify critical path)
CREATE INDEX idx_nr_guid_lookup
    ON canary_app.namespace_registrations (namespace_guid)
    WHERE status = 'active';

-- Reverse: what namespace GUIDs does this merchant own?
CREATE INDEX idx_nr_merchant
    ON canary_app.namespace_registrations (merchant_id);

-- NOTE: No human-readable name in this table. Names are L2 aliases.
-- See namespace_aliases table for L2 alias caching.
-- GUID format: UUID v4, stored as native UUID type for efficient indexing.

-- RLS
ALTER TABLE canary_app.namespace_registrations ENABLE ROW LEVEL SECURITY;
ALTER TABLE canary_app.namespace_registrations FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON canary_app.namespace_registrations
    USING (merchant_id = current_setting('app.current_merchant_id')::uuid);
```

### New Table: `namespace_aliases` (L2 Cache)

**Purpose:** L3 cache of L2 Avalanche NameRegistry alias→GUID mappings. Enables fast name resolution without hitting L2 on every request. Rebuildable from L2 state.

```sql
-- ============================================================
-- Table: namespace_aliases
-- Purpose: L3 cache of L2 human-readable alias → GUID mappings
-- Schema: canary_app
-- GRO-58: Aliases are L2-native, this is a cache
-- ============================================================

CREATE TABLE canary_app.namespace_aliases (
    id                  UUID            NOT NULL DEFAULT gen_random_uuid(),
    namespace_guid      UUID            NOT NULL,
    alias_name          TEXT            NOT NULL,   -- 'sunrise-coffee.jeffe'
    status              TEXT            NOT NULL DEFAULT 'active',
    synced_at           TIMESTAMPTZ     NOT NULL DEFAULT now(),  -- Last sync from L2
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),

    CONSTRAINT pk_namespace_aliases PRIMARY KEY (id),
    CONSTRAINT fk_na_namespace FOREIGN KEY (namespace_guid)
        REFERENCES canary_app.namespace_registrations(namespace_guid),
    CONSTRAINT uix_na_alias_name UNIQUE (alias_name),
    CONSTRAINT chk_na_status CHECK (status IN ('active', 'inactive'))
);

-- Hot lookup: resolve alias → GUID (RaaS /v1/resolve critical path)
CREATE INDEX idx_na_alias_lookup
    ON canary_app.namespace_aliases (alias_name)
    WHERE status = 'active';

-- Reverse: what aliases does this GUID have?
CREATE INDEX idx_na_guid
    ON canary_app.namespace_aliases (namespace_guid);

-- RLS not applied — alias data is public (L2 is public)
```

### Status Lifecycle

```
registered → active → expired → suspended
                ↑         │          │
                └─────────┘          │
                (renewal)            │
                ↑                    │
                └────────────────────┘
                (admin resolution)
```

| Status | Meaning | Transition |
|--------|---------|------------|
| `registered` | GUID created, owner assigned, no receipts yet | → `active` on first Merkle batch |
| `active` | Live namespace with receipts flowing | → `expired` if renewal lapses |
| `expired` | Past renewal date, 30-day grace period | → `active` on renewal; released after grace |
| `suspended` | Admin action (dispute, abuse, legal hold) | → `active` on resolution |

---

## 3. New Table: `source_systems`

**Purpose:** Reference table for source system codes, replacing the hardcoded CHECK constraint on `external_identities.source_system`. Enables cross-vertical expansion (POS → EHR → logistics → IoT) without DDL migrations.

**Alignment Reference:** Amendment C

```sql
-- ============================================================
-- Table: source_systems
-- Amendment: C (Source System Reference Table)
-- Schema: canary_app
-- ============================================================

CREATE TABLE canary_app.source_systems (
    code                TEXT            NOT NULL,
    display_name        TEXT            NOT NULL,
    category            TEXT            NOT NULL DEFAULT 'pos',
    is_active           BOOLEAN         NOT NULL DEFAULT true,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),

    CONSTRAINT pk_source_systems PRIMARY KEY (code),
    -- NOTE: category CHECK is intentional. Categories are a stable taxonomy.
    -- Adding a new category requires a DDL migration (rare, ~1/year).
    -- Adding a new source system within a category is an INSERT (frequent).
    CONSTRAINT chk_ss_category CHECK (category IN (
        'pos',              -- Square, Clover, Toast, Shopify, etc.
        'ehr',              -- Healthcare (Epic, Cerner, Allscripts, etc.)
        'logistics',        -- Supply chain (SAP, Oracle SCM, etc.)
        'iot',              -- IoT platforms (AWS IoT, Azure IoT Hub, etc.)
        'financial',        -- Banking, insurance, payment processors
        'identity',         -- OAuth providers, SSO, identity platforms
        'manual'            -- Human-entered data
    ))
);

-- Seed current POS systems
INSERT INTO canary_app.source_systems (code, display_name, category) VALUES
    ('square',      'Square',           'pos'),
    ('clover',      'Clover',           'pos'),
    ('toast',       'Toast',            'pos'),
    ('shopify',     'Shopify POS',      'pos'),
    ('dutchie',     'Dutchie',          'pos'),
    ('cova',        'Cova',             'pos'),
    ('lightspeed',  'Lightspeed',       'pos'),
    ('revel',       'Revel',            'pos'),
    ('micros',      'Oracle MICROS',    'pos'),
    ('ncr',         'NCR',              'pos'),
    ('manual',      'Manual Entry',     'manual');
```

---

## 4. Migration: `external_identities` — CHECK → FK

**Purpose:** Replace the hardcoded CHECK constraint on `external_identities.source_system` with a foreign key to `source_systems`. Adding a new source system becomes an INSERT instead of a DDL migration.

**Prerequisite:** Table `source_systems` must exist and be seeded before this migration runs.

```sql
-- ============================================================
-- Migration: external_identities CHECK → FK
-- Amendment: C
-- Prerequisite: source_systems table exists and is seeded
-- ============================================================

-- Step 1: Drop the existing CHECK constraint
ALTER TABLE canary_app.external_identities
    DROP CONSTRAINT chk_ei_source_system;

-- Step 2: Add FK to source_systems
ALTER TABLE canary_app.external_identities
    ADD CONSTRAINT fk_ei_source_system
    FOREIGN KEY (source_system) REFERENCES canary_app.source_systems(code);
```

### Validation Query (Jim — run before and after migration)

```sql
-- Verify all existing source_system values have a matching code in source_systems
SELECT DISTINCT ei.source_system
FROM canary_app.external_identities ei
LEFT JOIN canary_app.source_systems ss ON ei.source_system = ss.code
WHERE ss.code IS NULL;

-- Expected result: 0 rows (all existing values are seeded)
```

---

## 5. New Table: `merchant_feature_flags`

**Purpose:** Feature flag configuration per merchant. Initial use: `device_attestation` flag for the inscription pipeline. Designed as a generic flag table to support future feature flags without new tables.

**PRD Reference:** `PRD_Device_Attestation_v1.0.md` (R-1)

```sql
-- ============================================================
-- Table: merchant_feature_flags
-- Purpose: Per-merchant feature configuration
-- Schema: canary_app
-- ============================================================

-- NOTE: Implemented in GRO-14 with is_enabled BOOLEAN instead of flag_value TEXT.
-- Boolean is simpler and eliminates the need for a conditional CHECK constraint
-- (Tom Review T-10). If future flags need richer values, add a separate column.
CREATE TABLE canary_app.merchant_feature_flags (
    id                  UUID            NOT NULL DEFAULT gen_random_uuid(),
    merchant_id         UUID            NOT NULL,
    flag_key            TEXT            NOT NULL,   -- e.g., 'device_attestation'
    is_enabled          BOOLEAN         NOT NULL DEFAULT false,
    description         TEXT,                       -- optional description
    updated_by          TEXT,                       -- admin user or system
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),

    CONSTRAINT pk_merchant_feature_flags PRIMARY KEY (id),
    CONSTRAINT fk_mff_merchant FOREIGN KEY (merchant_id)
        REFERENCES canary_app.merchants(merchant_id) ON DELETE CASCADE,
    CONSTRAINT uix_mff_merchant_flag UNIQUE (merchant_id, flag_key)
);

-- Lookup: what's this merchant's setting for a given flag?
CREATE INDEX idx_mff_lookup
    ON canary_app.merchant_feature_flags (merchant_id, flag_key);

-- RLS
ALTER TABLE canary_app.merchant_feature_flags ENABLE ROW LEVEL SECURITY;
ALTER TABLE canary_app.merchant_feature_flags FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON canary_app.merchant_feature_flags
    USING (merchant_id = current_setting('app.current_merchant_id')::uuid);
```

### Default Flag Values

```sql
-- When a new merchant onboards, insert default flags:
-- (This should be part of the merchant provisioning flow, not a migration)

-- Example: device attestation defaults to OFF
INSERT INTO canary_app.merchant_feature_flags (merchant_id, flag_key, is_enabled, updated_by)
VALUES (<merchant_uuid>, 'device_attestation', false, 'system');
```

---

## 6. New Table: `merkle_batches`

**Purpose:** Stores inscription references for each Merkle batch. This is the operational record that links the CRDM event data to the on-chain Bitcoin inscription. Used by the RaaS verification flow to locate the inscription for a given event.

**Design Spec Reference:** `Inscription_Pipeline_Design_Spec_v1.0.md` (Section 3.6)

```sql
-- ============================================================
-- Table: merkle_batches
-- Purpose: Inscription reference storage for Merkle batch inscriptions
-- Schema: canary_sales
-- ============================================================

CREATE TABLE canary_sales.merkle_batches (
    id                          UUID            NOT NULL DEFAULT gen_random_uuid(),
    merchant_id                 UUID            NOT NULL,
    namespace_guid              UUID            NOT NULL,   -- Pseudonymous L1 GUID (GRO-58)

    -- Batch identification
    batch_id                    UUID            NOT NULL,

    -- Event Merkle tree
    merkle_root                 TEXT            NOT NULL,   -- SHA-256 root hash
    event_count                 INTEGER         NOT NULL,
    tree_depth                  INTEGER         NOT NULL,

    -- Time range
    time_range_first            TIMESTAMPTZ     NOT NULL,   -- Earliest event in batch
    time_range_last             TIMESTAMPTZ     NOT NULL,   -- Latest event in batch

    -- Bitcoin inscription
    inscription_id              TEXT,                       -- Ordinal inscription ID
    inscription_txid            TEXT,                       -- Bitcoin transaction ID
    block_height                BIGINT,                     -- Confirmation block
    confirmed_at                TIMESTAMPTZ,                -- Block timestamp

    -- Device attestation (nullable — only populated when device_attestation = on)
    device_attestation_enabled  BOOLEAN         NOT NULL DEFAULT false,
    device_root                 TEXT,                       -- SHA-256 root of device tree
    device_count                INTEGER,                    -- Unique devices in batch
    device_flags                TEXT[],                     -- Chirp rule codes (e.g., '{C-901,C-904}')

    -- Chain linkage
    chain_previous              TEXT,                       -- inscription_id of prior batch
    chain_sequence              INTEGER         NOT NULL,   -- Monotonic sequence number

    -- Metadata
    created_at                  TIMESTAMPTZ     NOT NULL DEFAULT now(),

    CONSTRAINT pk_merkle_batches PRIMARY KEY (id),
    CONSTRAINT fk_mb_merchant FOREIGN KEY (merchant_id)
        REFERENCES canary_app.merchants(merchant_id) ON DELETE CASCADE,
    CONSTRAINT fk_mb_namespace FOREIGN KEY (namespace_guid)
        REFERENCES canary_app.namespace_registrations(namespace_guid),
    CONSTRAINT uix_mb_batch_id UNIQUE (batch_id),
    CONSTRAINT uix_mb_namespace_seq UNIQUE (namespace_guid, chain_sequence),
    CONSTRAINT chk_mb_event_count CHECK (event_count > 0),
    CONSTRAINT chk_mb_time_range CHECK (time_range_first <= time_range_last)
);

-- RaaS verification: find the batch containing an event by time range
CREATE INDEX idx_mb_merchant_time
    ON canary_sales.merkle_batches (merchant_id, time_range_first, time_range_last);

-- Chain traversal: find latest batch for a namespace GUID
CREATE INDEX idx_mb_namespace_seq
    ON canary_sales.merkle_batches (namespace_guid, chain_sequence DESC);

-- Filter: attested vs. unattested batches
CREATE INDEX idx_mb_device_attestation
    ON canary_sales.merkle_batches (device_attestation_enabled)
    WHERE device_attestation_enabled = true;

-- Inscription lookup
CREATE INDEX idx_mb_inscription
    ON canary_sales.merkle_batches (inscription_id)
    WHERE inscription_id IS NOT NULL;

-- RLS
ALTER TABLE canary_sales.merkle_batches ENABLE ROW LEVEL SECURITY;
ALTER TABLE canary_sales.merkle_batches FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON canary_sales.merkle_batches
    USING (merchant_id = current_setting('app.current_merchant_id')::uuid);
```

---

## 7. Migration: `evidence_records` — Add `batch_id` Column

**Purpose:** Enable direct batch-to-event join for verification. The current time-range-based lookup (Pipeline Spec §4.1) has boundary gap/overlap issues. Sub 3 stamps `batch_id` on each event when the batch is assembled, making verification a deterministic FK join.

**Tom Review:** T-2 (Blocker). Must land before Phase 1 pipeline work.

```sql
-- ============================================================
-- Migration: evidence_records — add batch_id for direct batch join
-- Tom Review: T-2 (Blocker)
-- Prerequisite: merkle_batches table exists
-- ============================================================

-- Add batch_id column (nullable — existing events won't have it)
ALTER TABLE canary_sales.evidence_records
    ADD COLUMN batch_id UUID REFERENCES canary_sales.merkle_batches(batch_id);

-- Index for verification join: find all events in a batch
CREATE INDEX idx_er_batch
    ON canary_sales.evidence_records (batch_id)
    WHERE batch_id IS NOT NULL;
```

### Verification Query (New — Replaces Time-Range Lookup)

```sql
-- Verification: find the batch containing a specific event
-- This replaces the time-range query in Pipeline Spec §4.1
SELECT mb.* FROM canary_sales.merkle_batches mb
JOIN canary_sales.evidence_records er ON er.batch_id = mb.batch_id
WHERE er.event_hash = ? AND er.merchant_id = ?
```

**Note:** The time-range index on `merkle_batches` is retained as a convenience for dashboard queries, but verification MUST use the direct `batch_id` join.

---

## 8. Triggers: `updated_at` Auto-Update

**Purpose:** Ensure `updated_at` columns on `namespace_registrations` and `merchant_feature_flags` stay current on any row update.

**Tom Review:** T-4 (Blocker).

```sql
-- ============================================================
-- Trigger Function: update_updated_at_column
-- Create once, reuse across tables
-- Tom Review: T-4 (Blocker)
-- ============================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- namespace_registrations
CREATE TRIGGER set_updated_at
    BEFORE UPDATE ON canary_app.namespace_registrations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- merchant_feature_flags
CREATE TRIGGER set_updated_at
    BEFORE UPDATE ON canary_app.merchant_feature_flags
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

---

## 9. Migration Order

Migrations must run in this order due to foreign key dependencies:

```
Step 1: source_systems              (no dependencies)
Step 2: external_identities FK      (depends on source_systems)
Step 3: namespace_registrations     (depends on merchants) — GUID-based (GRO-58)
Step 4: namespace_aliases           (depends on namespace_registrations) — L2 cache (GRO-58)
Step 5: merchant_feature_flags      (depends on merchants)
Step 6: merkle_batches              (depends on merchants, namespace_registrations)
Step 7: evidence_records.batch_id   (depends on merkle_batches)
Step 8: updated_at triggers         (depends on namespace_registrations, merchant_feature_flags)
```

### Migration Script Header Template

```sql
-- ============================================================
-- Migration: CRDM v1.1 Addendum
-- Date: 2026-03-XX
-- Author: Jeremy (implementation), Tom (DDL validation)
-- Issue: GRO-47, GRO-46, GRO-13, GRO-45, GRO-54
-- Prerequisite: CRDM v1.1 (GRO-45 Amendments 1-8) applied
-- Rollback: See rollback script in same directory
-- ============================================================

BEGIN;

-- Step 1: source_systems
-- [DDL from Section 3]

-- Step 2: external_identities migration
-- [DDL from Section 4]

-- Step 3: namespace_registrations (GUID-based, GRO-58)
-- [DDL from Section 2]

-- Step 4: namespace_aliases (L2 cache, GRO-58)
-- [DDL from Section 2]

-- Step 5: merchant_feature_flags
-- [DDL from Section 5]

-- Step 6: merkle_batches (FK to namespace_registrations via GUID, unique on GUID+sequence)
-- [DDL from Section 6]

-- Step 7: evidence_records.batch_id column + index
-- [DDL from Section 7]

-- Step 8: updated_at trigger function + triggers
-- [DDL from Section 8]

COMMIT;
```

---

## 10. Rollback Script

```sql
-- ============================================================
-- Rollback: CRDM v1.1 Addendum
-- WARNING: Drops tables and data. Use only in development/staging.
-- ============================================================

BEGIN;

-- Step 7 rollback: drop triggers and function
DROP TRIGGER IF EXISTS set_updated_at ON canary_app.merchant_feature_flags;
DROP TRIGGER IF EXISTS set_updated_at ON canary_app.namespace_registrations;
DROP FUNCTION IF EXISTS update_updated_at_column();

-- Step 6 rollback: remove batch_id from evidence_records
DROP INDEX IF EXISTS canary_sales.idx_er_batch;
ALTER TABLE canary_sales.evidence_records DROP COLUMN IF EXISTS batch_id;

-- Step 5 rollback: drop merkle_batches
DROP TABLE IF EXISTS canary_sales.merkle_batches CASCADE;

-- Step 4 rollback: drop merchant_feature_flags
DROP TABLE IF EXISTS canary_app.merchant_feature_flags CASCADE;

-- Step 4 rollback: drop namespace_aliases (L2 cache)
DROP TABLE IF EXISTS canary_app.namespace_aliases CASCADE;

-- Step 3 rollback: drop namespace_registrations
DROP TABLE IF EXISTS canary_app.namespace_registrations CASCADE;

-- Step 2 rollback: restore CHECK constraint on external_identities
ALTER TABLE canary_app.external_identities
    DROP CONSTRAINT IF EXISTS fk_ei_source_system;
ALTER TABLE canary_app.external_identities
    ADD CONSTRAINT chk_ei_source_system CHECK (source_system IN (
        'square', 'clover', 'toast', 'shopify', 'dutchie',
        'cova', 'lightspeed', 'revel', 'micros', 'ncr', 'manual'
    ));

-- Step 1 rollback: drop source_systems
DROP TABLE IF EXISTS canary_app.source_systems CASCADE;

COMMIT;
```

---

## 11. Summary

| Table | Schema | Type | Rows (est. Year 1) | Critical Path |
|-------|--------|------|--------------------|--------------|
| `namespace_registrations` | canary_app | NEW | ~100–500 | RaaS /v1/verify (GUID→merchant_id) |
| `namespace_aliases` | canary_app | NEW | ~200–2,000 | RaaS /v1/resolve (alias→GUID L2 cache) |
| `source_systems` | canary_app | NEW | ~20–50 | external_identities FK |
| `merchant_feature_flags` | canary_app | NEW | ~100–500 | Sub 3 device attestation toggle |
| `merkle_batches` | canary_sales | NEW | ~5,000–50,000 | RaaS verification, inscription chain |
| `external_identities` | canary_app | MODIFIED | existing | source_system FK swap |
| `evidence_records` | canary_sales | MODIFIED | existing | batch_id column for direct verification join |

---

*CRDM v1.1 Addendum | March 2, 2026*
*MAXIMUM CONFIDENTIAL*
