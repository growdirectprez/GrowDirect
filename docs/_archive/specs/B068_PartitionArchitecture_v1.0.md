---
type: spec
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# B-068-A: Partition Architecture Specification
## Per-Merchant Composite Partition Design for canary_sales

**Version:** 1.0
**Date:** February 28, 2026
**Author:** Tom (Systems Architect)
**Work Order:** B-068, Lane A
**Classification:** MAXIMUM CONFIDENTIAL
**Primary Source:** GrowDirect_UnifiedArchitectureThesis_v1.0.md (PhD, Section 3.2 + Section 4)

---

## 1. Decision: Composite Partition Key

### Evaluation

**Option A — Period only (current spec)**

```sql
CREATE TABLE transactions (...) PARTITION BY RANGE (transaction_date);
```

All merchants share each monthly partition. Deleting Merchant A's data requires
`DELETE WHERE merchant_id = ?` — row-by-row, no partition pruning, full vacuum.
RLS provides query-time isolation but the data is physically co-located.

**Verdict: Rejected.** Violates merchant-first isolation. The partition boundary
is the period boundary, not the merchant boundary. The hash chain is per-merchant
but the storage is not. This is an architectural mismatch, not a performance concern.

---

**Option B — Merchant × Period (two-level composite)**

```sql
PARTITION BY LIST (merchant_id)
  → PARTITION BY RANGE (transaction_date)  -- monthly children
```

True merchant isolation. Each merchant's data is physically separated. Archive by
DROP. Hash chain alignment is exact — each partition tree contains precisely the
records referenced by that merchant's evidence chain.

Risk: partition catalog size at scale. At 1,000 merchants × 12 months × 8 tables
= 96,000 child tables per year of active data.

**Verdict: Architecturally correct but incomplete.** Does not account for volume
variance between SMB and enterprise merchants.

---

**Option C — Flexible granularity (extends Option B)**

```sql
PARTITION BY LIST (merchant_id)
  → PARTITION BY RANGE (transaction_date)  -- period per merchant config
```

Per-merchant period granularity stored in `merchants.partition_config`:

```sql
-- In merchants table:
partition_config JSONB NOT NULL DEFAULT '{"period": "monthly"}'

-- SMB default: monthly (≤5K tx/day)
-- Enterprise override: quarterly (>5K tx/day)
-- Set at onboarding, immutable after first partition created
```

Same isolation principle as Option B. Right-sized storage granularity. Enterprise
merchants produce fewer, larger partitions. SMB merchants produce more, smaller
partitions. Net catalog pressure is lower than Option B at scale while the
isolation invariant holds identically.

**Verdict: Recommended. This is the decision.**

### Justification

The white paper (Section 3.2) states the principle directly:

> "Monthly versus quarterly is not a feature toggle. It is proof that the
> isolation is real. Each merchant's partition is genuinely independent and can
> be managed on its own terms."

Option C is the only design where the partition strategy is **visibly per-merchant**
to investors, auditors, and compliance reviewers. An SMB merchant and an enterprise
merchant coexist in the same cluster with different operational characteristics
because their data is isolated at the partition boundary. This is the Postgres
expression of the UTXO independence property.

The tradeoff — slightly more complexity in partition management — is bounded. The
`create_merchant_partitions()` function reads `partition_config` once at onboarding
and creates the appropriate child table structure. After creation, the partitions
behave identically regardless of granularity. The complexity is in provisioning, not
in query execution or maintenance.

---

## 2. Naming Convention

### Standard

```
{table}_{merchant_alias}_{year}_{period}
```

Where:
- `{table}` — canonical table name (e.g., `transactions`, `transaction_line_items`)
- `{merchant_alias}` — short alias assigned at onboarding, format `m` + zero-padded
  4-digit number (e.g., `m0001`). Stored in `merchants.partition_alias`. Immutable
  after assignment. The actual `merchant_id` (Square's value, e.g., `MLE55GCYANCYT`)
  is used in the `FOR VALUES IN` clause; the alias is for table naming only.
- `{year}` — 4-digit year
- `{period}` — either `{MM}` (monthly, zero-padded) or `Q{N}` (quarterly)

### Examples

```sql
-- Merchant-level parent partition (LIST on merchant_id)
transactions_m0001                       -- merchant alias m0001

-- Monthly children (SMB)
transactions_m0001_2026_01               -- January 2026
transactions_m0001_2026_02               -- February 2026
transaction_line_items_m0001_2026_01
transaction_tenders_m0001_2026_01
refund_links_m0001_2026_01
cash_drawer_shifts_m0001_2026_01
employee_timecards_m0001_2026_01
gift_card_activities_m0001_2026_01
inventory_adjustments_m0001_2026_01

-- Quarterly children (Enterprise)
transactions_m0042_2026_Q1               -- Q1 2026
transactions_m0042_2026_Q2               -- Q2 2026
transaction_line_items_m0042_2026_Q1
```

### Alias Assignment

```sql
-- merchants table addition:
partition_alias VARCHAR(10) NOT NULL UNIQUE
  -- Format: m0001, m0002, ...
  -- Assigned by onboarding function
  -- IMMUTABLE after first partition created
  -- Used in child table naming only; partition key is merchant_id
```

Alias sequence: `nextval('merchant_alias_seq')`, formatted as `m` + lpad(val, 4, '0').
At 10,000 merchants, expand to 5-digit (automatic — lpad handles it).

---

## 3. Full DDL — `transactions` Table

```sql
-- =============================================================================
-- B-068-A: transactions — Composite Merchant × Period Partition
-- Author: Tom (Systems Architect)
-- Date: February 28, 2026
-- Principle: The partition IS the hash chain expressed in Postgres.
-- =============================================================================

-- ---------------------------------------------------------------------------
-- 3.1  Parent table (partitioned by merchant)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS transactions (
    id                      VARCHAR         NOT NULL,
    merchant_id             VARCHAR         NOT NULL,
    external_id             VARCHAR         NOT NULL,
    order_id                VARCHAR,
    receipt_number          VARCHAR,
    source_type             VARCHAR         NOT NULL DEFAULT 'WEBHOOK',
    location_id             VARCHAR         NOT NULL,
    employee_id             VARCHAR,
    customer_id             VARCHAR,
    device_id               VARCHAR,
    transaction_type        VARCHAR         NOT NULL,
    transaction_date        TIMESTAMP       NOT NULL,
    amount_cents            BIGINT          NOT NULL,
    tax_amount_cents        BIGINT          NOT NULL DEFAULT 0,
    discount_amount_cents   BIGINT          NOT NULL DEFAULT 0,
    tip_amount_cents        BIGINT          NOT NULL DEFAULT 0,
    currency                VARCHAR         NOT NULL DEFAULT 'USD',
    card_fingerprint        VARCHAR,
    card_brand              VARCHAR,
    card_last4              VARCHAR,
    card_prepaid_type       VARCHAR,
    cvv_status              VARCHAR,
    avs_status              VARCHAR,
    entry_method            VARCHAR,
    square_product          VARCHAR,
    risk_level              VARCHAR,
    payload                 TEXT,
    created_at              TIMESTAMP       NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP       NOT NULL DEFAULT NOW(),

    -- Primary key MUST include partition key columns
    CONSTRAINT pk_transactions PRIMARY KEY (merchant_id, id),

    -- Uniqueness constraint scoped to merchant
    CONSTRAINT uq_transactions_merchant_external
        UNIQUE (merchant_id, external_id)
)
PARTITION BY LIST (merchant_id);

-- ---------------------------------------------------------------------------
-- 3.2  Indexes on parent (inherited by all children)
-- ---------------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS ix_txn_merchant_date
    ON transactions (merchant_id, transaction_date);

CREATE INDEX IF NOT EXISTS ix_txn_merchant_employee
    ON transactions (merchant_id, employee_id)
    WHERE employee_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS ix_txn_merchant_location
    ON transactions (merchant_id, location_id);

CREATE INDEX IF NOT EXISTS ix_txn_merchant_card_fp
    ON transactions (merchant_id, card_fingerprint)
    WHERE card_fingerprint IS NOT NULL;

CREATE INDEX IF NOT EXISTS ix_txn_merchant_order
    ON transactions (merchant_id, order_id)
    WHERE order_id IS NOT NULL;

-- Cross-merchant card fingerprint index (C-005 Chirp: cross-merchant fraud ring)
-- This is the ONLY index that intentionally crosses the merchant boundary.
-- Reads only — never writes to another merchant's chain.
CREATE INDEX IF NOT EXISTS ix_txn_card_fingerprint_global
    ON transactions (card_fingerprint, merchant_id)
    WHERE card_fingerprint IS NOT NULL;

-- ---------------------------------------------------------------------------
-- 3.3  Immutability trigger (inherited by children)
-- ---------------------------------------------------------------------------
-- INSERT-only enforcement per CRDM spec. UPDATE and DELETE are blocked.
-- This trigger is defined on the parent and inherited by all child partitions.

CREATE OR REPLACE FUNCTION fn_immutable_transactions()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'CRDM v1.0: transactions is append-only. '
        'UPDATE and DELETE are prohibited. '
        'Evidence chain integrity requires immutable records.';
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_immutable_transactions
    BEFORE UPDATE OR DELETE ON transactions
    FOR EACH ROW
    EXECUTE FUNCTION fn_immutable_transactions();

-- ---------------------------------------------------------------------------
-- 3.4  RLS policy (defense in depth — partition + RLS)
-- ---------------------------------------------------------------------------
-- Partition provides physical isolation. RLS provides query-time enforcement.
-- Belt and suspenders. Neither alone is sufficient for compliance argument.

ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;

CREATE POLICY rls_transactions_merchant ON transactions
    USING (merchant_id = current_setting('app.current_merchant_id', true))
    WITH CHECK (merchant_id = current_setting('app.current_merchant_id', true));

-- ---------------------------------------------------------------------------
-- 3.5  Example: Onboarding merchant m0001 (SMB, monthly)
-- ---------------------------------------------------------------------------

-- Step 1: Create merchant-level partition (LIST on merchant_id)
CREATE TABLE transactions_m0001 PARTITION OF transactions
    FOR VALUES IN ('MLE55GCYANCYT')
    PARTITION BY RANGE (transaction_date);

-- Step 2: Create period children (monthly for SMB)
CREATE TABLE transactions_m0001_2026_01 PARTITION OF transactions_m0001
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

CREATE TABLE transactions_m0001_2026_02 PARTITION OF transactions_m0001
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');

CREATE TABLE transactions_m0001_2026_03 PARTITION OF transactions_m0001
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');

-- ... (repeat for each month in retention window)

-- ---------------------------------------------------------------------------
-- 3.6  Example: Onboarding merchant m0042 (Enterprise, quarterly)
-- ---------------------------------------------------------------------------

CREATE TABLE transactions_m0042 PARTITION OF transactions
    FOR VALUES IN ('ENT_MERCHANT_42')
    PARTITION BY RANGE (transaction_date);

CREATE TABLE transactions_m0042_2026_Q1 PARTITION OF transactions_m0042
    FOR VALUES FROM ('2026-01-01') TO ('2026-04-01');

CREATE TABLE transactions_m0042_2026_Q2 PARTITION OF transactions_m0042
    FOR VALUES FROM ('2026-04-01') TO ('2026-07-01');

CREATE TABLE transactions_m0042_2026_Q3 PARTITION OF transactions_m0042
    FOR VALUES FROM ('2026-07-01') TO ('2026-10-01');

CREATE TABLE transactions_m0042_2026_Q4 PARTITION OF transactions_m0042
    FOR VALUES FROM ('2026-10-01') TO ('2027-01-01');
```

### 3.7 Key DDL Decisions

**Primary key includes partition key:** PostgreSQL requires that partition key
columns appear in all unique constraints (including PK). Therefore PK is
`(merchant_id, id)` not just `(id)`. All foreign key references must include
`merchant_id`.

**Indexes on parent:** Defined on the parent table so they are automatically
created on every child partition. PostgreSQL 11+ supports this.

**Immutability trigger on parent:** Inherited by all children. No per-partition
trigger maintenance.

**RLS on parent:** Defense in depth. The partition provides physical isolation;
RLS provides query-time enforcement. Both exist simultaneously. For compliance
(FCRA/CRA), the argument is: even if RLS is misconfigured, the partition boundary
prevents data co-mingling in storage.

**Global card_fingerprint index:** The only index that intentionally crosses
merchant boundaries. Required for C-005 (cross-merchant fraud ring detection).
Per B-048 resolution: `card_fingerprint` is network-universal by design. C-005
queries across partitions using this index as a read-only operation. Detection
results are written to the querying merchant's evidence chain only.

---

## 4. Template DDL — Remaining 7 Tables

The following template applies identically to all remaining tables. Only the
column definitions and table-specific indexes change. The partition structure,
naming convention, immutability enforcement, and RLS policy are identical.

### 4.1 Template Pattern

```sql
-- =============================================================================
-- Template: {TABLE_NAME} — Composite Merchant × Period Partition
-- Apply this pattern to: transaction_line_items, transaction_tenders,
--   refund_links, cash_drawer_shifts, employee_timecards,
--   gift_card_activities, inventory_adjustments
-- =============================================================================

CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    {COLUMNS},                              -- table-specific columns

    -- PK must include partition key
    CONSTRAINT pk_{TABLE_NAME} PRIMARY KEY (merchant_id, id)
)
PARTITION BY LIST (merchant_id);

-- Table-specific indexes (all merchant-first)
CREATE INDEX IF NOT EXISTS ix_{TABLE_ALIAS}_{INDEX_NAME}
    ON {TABLE_NAME} ({INDEX_COLUMNS});

-- Immutability trigger (append-only tables only — see note below)
CREATE OR REPLACE FUNCTION fn_immutable_{TABLE_NAME}()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'CRDM v1.0: {TABLE_NAME} is append-only. '
        'UPDATE and DELETE are prohibited.';
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_immutable_{TABLE_NAME}
    BEFORE UPDATE OR DELETE ON {TABLE_NAME}
    FOR EACH ROW
    EXECUTE FUNCTION fn_immutable_{TABLE_NAME}();

-- RLS
ALTER TABLE {TABLE_NAME} ENABLE ROW LEVEL SECURITY;

CREATE POLICY rls_{TABLE_NAME}_merchant ON {TABLE_NAME}
    USING (merchant_id = current_setting('app.current_merchant_id', true))
    WITH CHECK (merchant_id = current_setting('app.current_merchant_id', true));

-- Merchant partition (created at onboarding)
CREATE TABLE {TABLE_NAME}_{MERCHANT_ALIAS} PARTITION OF {TABLE_NAME}
    FOR VALUES IN ('{MERCHANT_ID}')
    PARTITION BY RANGE ({TEMPORAL_COLUMN});

-- Period children (created per config)
CREATE TABLE {TABLE_NAME}_{MERCHANT_ALIAS}_{YEAR}_{PERIOD}
    PARTITION OF {TABLE_NAME}_{MERCHANT_ALIAS}
    FOR VALUES FROM ('{RANGE_START}') TO ('{RANGE_END}');
```

### 4.2 Table-Specific Details

| Table | Temporal Column | Immutable | FK to transactions | Notes |
|---|---|---|---|---|
| `transaction_line_items` | `created_at` | YES | `(merchant_id, transaction_id)` | LP marker: `is_voided`, `total_discount_cents` |
| `transaction_tenders` | `created_at` | YES | `(merchant_id, transaction_id)` | Tender mix analysis |
| `refund_links` | `created_at` | YES | `(merchant_id, original_transaction_id)` | Refund-to-original chain |
| `cash_drawer_shifts` | `opened_at` | NO* | None | *Updated at close: `closed_at`, `closed_cash_cents`, `state` |
| `employee_timecards` | `start_at` | NO* | None | *Updated at clock-out: `end_at`, `status` |
| `gift_card_activities` | `occurred_at` | YES | Optional `linked_transaction_id` | Running balance tracking |
| `inventory_adjustments` | `occurred_at` | YES | None | Shrinkage analysis |

**Note on mutable tables:** `cash_drawer_shifts` and `employee_timecards` are
operational tables that receive updates (shift close, clock-out). They do NOT
get the immutability trigger. They still get merchant-level partitioning and RLS.
The hash chain for these tables uses the INSERT event only — updates are not
hashed. Sub 1 records the initial state at INSERT; Sub 2 (application DB)
reflects the current state. This is consistent with the evidence model: the
evidence chain proves "this shift was opened at this time" — not "this is the
current state of the shift."

### 4.3 Temporal Column Selection

The temporal column for `PARTITION BY RANGE` must be the column that represents
when the record's business event occurred — not `created_at` (system insertion
time). This ensures partition pruning aligns with business queries ("show me
January's transactions" prunes to the January partition).

| Table | Temporal Column | Rationale |
|---|---|---|
| `transactions` | `transaction_date` | When the sale/refund occurred |
| `transaction_line_items` | `created_at` | No separate business timestamp; created_at = insertion time |
| `transaction_tenders` | `created_at` | Same as line items |
| `refund_links` | `created_at` | Refund link creation time |
| `cash_drawer_shifts` | `opened_at` | When the shift started |
| `employee_timecards` | `start_at` | When the clock-in occurred |
| `gift_card_activities` | `occurred_at` | When the gift card event occurred |
| `inventory_adjustments` | `occurred_at` | When the adjustment was recorded |

**Important:** For `transaction_line_items` and `transaction_tenders`, the
temporal column is `created_at` because these records are children of a
transaction and share the parent's temporal context. An alternative is to
denormalize `transaction_date` onto these tables (adds a column, enables
direct partition pruning on business date). **Recommendation: denormalize.**
Add `transaction_date TIMESTAMP NOT NULL` to both tables, populated from
the parent transaction at INSERT time. This allows the period partition
to align exactly with the parent `transactions` table's period boundaries.

---

## 5. Archive Path — DROP PARTITION Cold Storage

### 5.1 Retention Floor

**14-month rolling window** per NRF calendar standard (Data Strategy North Star).
Any partition whose period ends more than 14 months before the current date is
archive-eligible.

Example: On March 1, 2027, partitions ending before January 1, 2026 are eligible.

The retention floor is a **minimum**. Per-merchant overrides are stored in
`merchants.partition_config`:

```json
{
  "period": "monthly",
  "retention_months": 14,
  "archive_tier": "glacier_instant"
}
```

Enterprise merchants may require longer retention (24, 36 months) per contract.
The floor is never less than 14 months.

### 5.2 DROP Sequence

```
┌─────────────────────────────────────────────────────────────────────┐
│  ARCHIVE PIPELINE — Per Merchant, Per Period                        │
│                                                                     │
│  1. MARK        partition_config.status = 'archiving'               │
│                 (prevents new INSERTs to this child table)          │
│                                                                     │
│  2. EXPORT      pg_dump → Parquet conversion                        │
│                 Target: s3://canary-archive/{alias}/{year}/{period}/ │
│                 Include: all 8 tables for this merchant+period      │
│                                                                     │
│  3. VERIFY      Row count: pg vs Parquet must match                 │
│                 SHA-256 checksum of export file                     │
│                 Athena test query: SELECT COUNT(*) succeeds         │
│                                                                     │
│  4. DROP        DROP TABLE {table}_{alias}_{year}_{period};         │
│                 One DDL statement per child table                   │
│                 No row-by-row deletion. No VACUUM needed.           │
│                 Execute for all 8 tables in single transaction.     │
│                                                                     │
│  5. RECORD      partition_config.status = 'archived'                │
│                 partition_config.archive_path = S3 URI              │
│                 partition_config.archived_at = NOW()                │
│                 partition_config.row_count = verified count          │
│                                                                     │
│  6. REGISTER    Glue catalog entry for Athena queryability          │
│                 Partition registered in external Hive metastore     │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.3 Cold Storage Tiers

| Age | Tier | Access Pattern | Cost Model |
|---|---|---|---|
| 0–14 months | PostgreSQL (live) | Real-time queries, Sub 2 projections | Compute + storage |
| 14–28 months | S3 Standard | Historical queries via Athena, compliance pulls | Storage + query |
| 28+ months | S3 Glacier Instant Retrieval | Rare access, legal/compliance retention | Storage only |

### 5.4 Trigger Mechanism

**Airflow DAG:** `archive_merchant_partitions`

- **Schedule:** Monthly, 1st of month, 02:00 UTC
- **Logic:** For each merchant, check partition_config against retention floor.
  Archive-eligible partitions enter the pipeline.
- **Manual override:** DAG can be triggered manually per merchant via Airflow CLI
  or API. Use case: merchant offboarding (archive all periods immediately).
- **Parallelism:** Each merchant's archive runs independently. Merchant A's archive
  does not block Merchant B. This is the operational expression of merchant-first
  isolation.

### 5.5 Merchant Offboarding

When a merchant leaves the platform:

1. All active partitions enter the archive pipeline simultaneously
2. After archive + verification, all merchant-level parent partitions are dropped
3. `merchants.status` set to `offboarded`
4. Archived data retained per contractual obligation (minimum 14 months from
   last transaction, configurable)
5. Evidence chain (Sub 1) is preserved independently — Bitcoin inscriptions are
   permanent regardless of merchant status

This is the operational proof of "DROP TABLE, not DELETE." Offboarding a merchant
is a bounded operation on their partition tree. No other merchant is touched.

---

## 6. Hash Chain Alignment Confirmation

### The Invariant

> Each merchant's hash chain in Sub 1 (the evidence store) is co-scoped with
> their partition tree. No hash in Merchant A's chain references a record in
> Merchant B's partition. The evidence layer and the query layer are consistent
> by construction.

### Proof Under Composite Partition Design

1. **Sub 1 hash computation:** `hash(raw_payload + previous_hash)` where
   `previous_hash` is the last entry in **this merchant's** chain. The
   `merchant_id` is part of the payload. The chain is keyed by `merchant_id`.

2. **Partition scope:** `transactions_m0001_*` contains ONLY records where
   `merchant_id = 'MLE55GCYANCYT'`. The LIST partition enforces this at the
   storage layer. No record from another merchant can physically exist in
   this partition tree.

3. **Co-scoping:** Every record in `transactions_m0001_2026_01` has a
   corresponding hash entry in merchant m0001's evidence chain. Every hash
   in m0001's chain references a record that exists in `transactions_m0001_*`.
   The partition boundary and the chain boundary are identical.

4. **Archive consistency:** When `transactions_m0001_2024_01` is archived
   (exported to Parquet + dropped), the hash entries for those records remain
   in Sub 1's evidence store. The hashes are permanent (write-once). The
   Parquet file in S3 can be verified against the hash chain at any time.
   The chain does not break when the partition is dropped — it references
   record IDs, and the archived Parquet preserves those IDs.

**Confirmed: The invariant holds. No cross-merchant chain contamination is
possible under this design.**

### Edge Case: C-005 Cross-Merchant Card Fingerprint Query

Per B-048 resolution (Jeffe directive, Feb 27): `card_fingerprint` is
network-universal by design. C-005 ("detect refunds issued to the same card
from multiple merchants") queries across merchant partitions using
`card_fingerprint` as the join key.

This is a **READ** across partition boundaries, not a **WRITE**. The detection
result is written to the evidence chain of the merchant whose refund triggered
C-005 — not to the other merchant's chain. The other merchant's partition and
chain are untouched.

The global index `ix_txn_card_fingerprint_global` supports this query pattern.
PostgreSQL's partition pruning will scan only partitions where `card_fingerprint`
matches, across all merchant partitions. This is intentional and correct.

**C-005 evaluation logic confirmation:** C-005 queries
`SELECT merchant_id, COUNT(*) FROM transactions WHERE card_fingerprint = ? GROUP BY merchant_id HAVING COUNT(*) > 1`.
The `merchant_id` in the result set provides the "different merchant" condition.
The partition design supports this query natively. No schema change needed.

---

## 7. Scale Assessment

### Assumptions

- **Active retention window:** 14 months (NRF floor)
- **Merchant mix:** 80% SMB (monthly partitions), 20% enterprise (quarterly)
- **Tables partitioned:** 8
- **Each child table generates:** 1 pg_class entry + ~3 index entries = ~4 pg_class entries

### Per-Merchant Active Partitions

| Config | Periods in 14-Month Window | × 8 Tables | Child Tables/Merchant |
|---|---|---|---|
| Monthly (SMB) | 14 | × 8 | 112 |
| Quarterly (Enterprise) | 5 | × 8 | 40 |

### Catalog Size at Scale

| Merchants | SMB (80%) | Enterprise (20%) | Active Child Tables | + Merchant Parents | + Index Entries (3×) | Total pg_class |
|---|---|---|---|---|---|---|
| **100** | 80 × 112 = 8,960 | 20 × 40 = 800 | 9,760 | + 800 | ~29,280 | **~39,840** |
| **1,000** | 800 × 112 = 89,600 | 200 × 40 = 8,000 | 97,600 | + 8,000 | ~292,800 | **~398,400** |
| **10,000** | 8,000 × 112 = 896,000 | 2,000 × 40 = 80,000 | 976,000 | + 80,000 | ~2,928,000 | **~3,984,000** |

### Assessment

| Scale | pg_class Size | Verdict | Notes |
|---|---|---|---|
| **100 merchants** | ~40K entries | Trivial | Single PostgreSQL instance. No special tuning. |
| **1,000 merchants** | ~400K entries | Comfortable | Single PostgreSQL instance with pg_partman automation. `ANALYZE` and `VACUUM` schedules tuned per partition. Catalog queries remain fast. |
| **10,000 merchants** | ~4M entries | Requires mitigation | Catalog pressure is real. Three mitigation paths: |

### Mitigation at 10,000 Merchants

1. **Aggressive archival:** Strictly enforce 14-month floor. Active catalog
   stays at 14 months × 8 tables. Older data is in S3/Athena, not pg_class.

2. **pg_partman automation:** Automated partition creation, detach, and drop.
   Eliminates manual DDL management. Tested at 100K+ partitions in production
   PostgreSQL deployments.

3. **Horizontal sharding:** At 5,000+ merchants, evaluate Citus (distributed
   PostgreSQL) or application-level sharding by merchant_id range. Each shard
   hosts 1,000–2,000 merchants. Catalog per shard stays in the 400K range.

4. **Index pruning on archived partitions:** Before archiving, drop non-essential
   indexes on soon-to-be-archived partitions. Reduces pg_class pressure during
   the final retention months.

**Phase 1 (< 100 merchants):** No concerns. Single instance.
**Phase 2 (100–1,000 merchants):** pg_partman. Monitor pg_class size monthly.
**Phase 3 (1,000–10,000 merchants):** Sharding evaluation. Architecture supports
it — each merchant's partition tree is self-contained and can be moved between
shards without breaking the hash chain alignment.

---

## 8. Migration Path — Unpartitioned to Partitioned

### Current State

- `transactions` and `refund_links`: exist as unpartitioned tables with data
- E1-F6 through E1-F11 tables: not yet created (Sprint 7)
- GrowDirect Lab (single merchant) is the only active data source

### Strategy

**New tables (E1-F6 through E1-F11):** Created directly as partitioned in the
Sprint 7 Alembic migration. No migration needed — they start life partitioned.

**Existing tables (transactions, refund_links):** Atomic swap migration.

### Migration Sequence for Existing Tables

```
┌─────────────────────────────────────────────────────────────────────┐
│  MIGRATION: transactions (unpartitioned → partitioned)              │
│                                                                     │
│  PRECONDITION: Application writes paused (maintenance window)       │
│  DURATION: Minutes for current data volume (< 1M rows)              │
│  DATA LOSS: Zero. Guaranteed by atomic rename.                      │
│                                                                     │
│  1. CREATE     transactions_new (partitioned parent)                │
│                + merchant partition for GrowDirect Lab               │
│                + period children covering existing data range        │
│                                                                     │
│  2. COPY       INSERT INTO transactions_new                         │
│                SELECT * FROM transactions;                          │
│                                                                     │
│  3. VERIFY     SELECT COUNT(*) from both tables must match          │
│                SELECT SUM(amount_cents) from both must match        │
│                                                                     │
│  4. SWAP       BEGIN;                                               │
│                ALTER TABLE transactions                              │
│                  RENAME TO transactions_unpartitioned;               │
│                ALTER TABLE transactions_new                          │
│                  RENAME TO transactions;                             │
│                COMMIT;                                               │
│                                                                     │
│  5. VALIDATE   Application queries work against new table           │
│                Hash chain verification passes                       │
│                RLS policies active                                   │
│                                                                     │
│  6. CLEANUP    After 48h validation window:                         │
│                DROP TABLE transactions_unpartitioned;                │
│                                                                     │
│  Repeat for refund_links.                                           │
└─────────────────────────────────────────────────────────────────────┘
```

### Alembic Migration Structure

```python
# Sprint 7 migration: 005_composite_partition.py

def upgrade():
    """
    Phase 1: Migrate existing tables to composite partition.
    Phase 2: Create new tables as partitioned from birth.
    """
    # --- Phase 1: Existing tables ---
    # Create partitioned parent
    op.execute("""
        CREATE TABLE transactions_new (...)
        PARTITION BY LIST (merchant_id);
    """)

    # Create merchant partition for GrowDirect Lab
    op.execute("""
        CREATE TABLE transactions_new_m0001
        PARTITION OF transactions_new
        FOR VALUES IN ('MLE55GCYANCYT')
        PARTITION BY RANGE (transaction_date);
    """)

    # Create period children covering existing data
    # (determined dynamically from MIN/MAX transaction_date)

    # Copy data
    op.execute("""
        INSERT INTO transactions_new SELECT * FROM transactions;
    """)

    # Atomic swap
    op.execute("ALTER TABLE transactions RENAME TO transactions_old;")
    op.execute("ALTER TABLE transactions_new RENAME TO transactions;")

    # --- Phase 2: New tables (born partitioned) ---
    # transaction_line_items, transaction_tenders, cash_drawer_shifts,
    # employee_timecards, gift_card_activities, inventory_adjustments
    # Created with PARTITION BY LIST (merchant_id) from the start.


def downgrade():
    """
    Reverse: swap back to unpartitioned.
    """
    op.execute("ALTER TABLE transactions RENAME TO transactions_partitioned;")
    op.execute("ALTER TABLE transactions_old RENAME TO transactions;")
```

### Foreign Key Considerations

PostgreSQL partitioned tables support foreign keys referencing them (PG 12+)
and foreign keys from them (PG 12+). However, FKs referencing a partitioned
table require the partition key in the FK columns. Therefore:

- `transaction_line_items.transaction_id` → `transactions(merchant_id, id)`
  becomes `(merchant_id, transaction_id)` referencing `(merchant_id, id)`
- All child table FKs must include `merchant_id`
- This is already natural since `merchant_id` exists on every table

---

## 9. The gLog Investor Paragraph

Every merchant on the Canary platform operates inside their own data partition —
a physically isolated segment of the database that belongs to one merchant and
one merchant only. When a coffee shop's oldest data reaches the end of its
retention window, archiving it is a single command: drop the partition. The coffee
shop's data is gone from the live database instantly. The pizzeria next door is
untouched — their partitions, their evidence chains, their performance are
completely independent. This is the same architectural property that lets Bitcoin
scale: independent state. A Black Friday surge at one merchant does not slow down
any other merchant. Adding a thousand new merchants does not reorganize a single
byte of existing merchant data. Each merchant is a bounded, independent unit —
like a Bitcoin UTXO. Their evidence chain is theirs. Their data partition is
theirs. Their archive path is theirs. Scale the platform, and the unit economics
improve. The architecture does not bend.

---

## 10. Onboarding Function — Reference Implementation

```sql
-- =============================================================================
-- create_merchant_partitions(merchant_id, partition_alias, partition_config)
--
-- Called once at merchant onboarding. Creates the full partition tree for all
-- 8 tables. Reads period config from partition_config JSONB.
-- =============================================================================

CREATE OR REPLACE FUNCTION create_merchant_partitions(
    p_merchant_id   VARCHAR,
    p_alias         VARCHAR,
    p_config        JSONB DEFAULT '{"period": "monthly", "retention_months": 14}'
)
RETURNS VOID AS $$
DECLARE
    v_period    VARCHAR := p_config->>'period';
    v_tables    TEXT[] := ARRAY[
        'transactions', 'transaction_line_items', 'transaction_tenders',
        'refund_links', 'cash_drawer_shifts', 'employee_timecards',
        'gift_card_activities', 'inventory_adjustments'
    ];
    v_temporal  TEXT[] := ARRAY[
        'transaction_date', 'created_at', 'created_at',
        'created_at', 'opened_at', 'start_at',
        'occurred_at', 'occurred_at'
    ];
    v_table     TEXT;
    v_tcol      TEXT;
    v_year      INT := EXTRACT(YEAR FROM NOW());
    v_sql       TEXT;
    i           INT;
BEGIN
    FOR i IN 1..array_length(v_tables, 1) LOOP
        v_table := v_tables[i];
        v_tcol  := v_temporal[i];

        -- Create merchant-level partition
        v_sql := format(
            'CREATE TABLE %I PARTITION OF %I FOR VALUES IN (%L) PARTITION BY RANGE (%I)',
            v_table || '_' || p_alias,
            v_table,
            p_merchant_id,
            v_tcol
        );
        EXECUTE v_sql;

        -- Create period children for current year
        IF v_period = 'monthly' THEN
            FOR m IN 1..12 LOOP
                v_sql := format(
                    'CREATE TABLE %I PARTITION OF %I FOR VALUES FROM (%L) TO (%L)',
                    v_table || '_' || p_alias || '_' || v_year || '_' || lpad(m::TEXT, 2, '0'),
                    v_table || '_' || p_alias,
                    make_date(v_year, m, 1)::TEXT,
                    (make_date(v_year, m, 1) + INTERVAL '1 month')::DATE::TEXT
                );
                EXECUTE v_sql;
            END LOOP;
        ELSIF v_period = 'quarterly' THEN
            FOR q IN 0..3 LOOP
                v_sql := format(
                    'CREATE TABLE %I PARTITION OF %I FOR VALUES FROM (%L) TO (%L)',
                    v_table || '_' || p_alias || '_' || v_year || '_Q' || (q+1),
                    v_table || '_' || p_alias,
                    make_date(v_year, q*3 + 1, 1)::TEXT,
                    (make_date(v_year, q*3 + 1, 1) + INTERVAL '3 months')::DATE::TEXT
                );
                EXECUTE v_sql;
            END LOOP;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Usage:
-- SELECT create_merchant_partitions('MLE55GCYANCYT', 'm0001', '{"period": "monthly"}');
-- SELECT create_merchant_partitions('ENT_MERCHANT_42', 'm0042', '{"period": "quarterly"}');
```

---

## 11. Coordination Notes

**Jeremy (Sprint 7 Alembic):** Read this document before writing migrations.
The Alembic migration calls `create_merchant_partitions()` for the GrowDirect Lab
merchant. New tables (E1-F6 through E1-F11) are created as partitioned parents
in the migration. The function handles child table creation.

**Syd (B-035 / FCRA/CRA):** The partition design provides two layers of tenant
isolation: (1) physical partition boundary (LIST on merchant_id), (2) RLS policy
(query-time enforcement). For the FCRA/CRA opinion: even if RLS is misconfigured
or bypassed, Merchant A's data physically cannot appear in Merchant B's partition.
The isolation is structural, not policy-based.

**Condor (Lane B — Blueprint v2.0):** No dependency. Token registry keys do not
affect partition naming or structure. Reconcile when Condor delivers.

**Lane D (Vocabulary Schema):** No dependency. The `merchant_vocabulary` table
is in `canary_app`, not `canary_sales`. It is not partitioned by period (it is
a configuration table, not a transaction table). Merchant-level isolation for
vocabulary is provided by the `merchant_id` column + RLS, not by partitioning.

---

*Tom | B-068-A | February 28, 2026*
*"The partition is the hash chain. Written that way."*
