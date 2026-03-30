---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Tom Session Prompt — B-035 Architecture Brief
*Dispatch: ALX | February 26, 2026*

---

Tom — two documents to read before you start. Both are required context.

**Read first:**
1. `Canary_IP/Markdown/Strategy/Canary_Data_Strategy_NorthStar_v1.1.md` — specifically the new section **"The Standardization Paradox"** added this session. This is the design philosophy that governs every architecture decision below.
2. `_ALX/WorkOrders/B035_Addendum_TemporalPartition_QueryGovernor.md` — your full brief.

---

## What You're Designing

The CRDM is the standard. The analytical lens is configurable. The merchant never touches either one.

Your job is to make that real at the PostgreSQL and tooling layer. Three deliverables:

---

### Deliverable 1: Temporal Sub-Partition DDL

Each merchant's primary partition (PARTITION BY LIST on merchant_id) is sub-partitioned by time at a fixed grain configured at onboarding.

Three grain variants to design:
- **Hour** — QSR, coffee, high-volume: 13 weeks × 24 hours = 2,184 sub-partitions per merchant
- **Day** — general SMB: 26 weeks = 182 sub-partitions per merchant
- **Week (NRF 4-5-4 aligned)** — seasonal retail: 56 weeks = 56 sub-partitions per merchant

**What you need to answer before writing DDL:**

D-1: Is hour/day/week the right set of grains or do we need finer (15-min) or coarser (month)? Recommendation with rationale.

D-2: At hourly grain, 1,000 merchants = 2.184 million sub-partitions in the PostgreSQL catalog. What is the real-world catalog load impact? Do we need a hybrid — hourly for recent 13 weeks, daily archive beyond that — to keep catalog size manageable?

Produce: DDL template for each of the 3 grain variants. Show how sub-partitions are created at merchant onboarding (this needs to be a scripted, repeatable operation — not a manual DBA task).

**Critical constraint:** Hash chains must remain self-contained per merchant partition. Sub-partitions must not break the chain. Verify this in your design.

---

### Deliverable 2: dbt + Superset Stack Assessment

The brief proposes replacing hand-written materialized view logic with:
- **dbt** for defining Layer C and Layer C+ transformations declaratively
- **Apache Superset** as the query surface, permission layer, and embedded rendering engine (already in the Technology Blueprint)

**What you need to answer:**

D-3: Materialized view refresh strategy for hourly-grain merchants. Options: Airflow micro-batch (15 min), trigger-based, scheduled hourly. What is the right cadence given the iMac's current compute profile?

D-4: Does the query contract live at the Flask blueprint layer or does Superset's dataset permission model fully replace a custom API governor? Recommendation.

Coordinate with Jeremy on D-6 (his question): Does Superset deploy cleanly into the existing Docker stack? What is the memory footprint? Is dbt additive to existing Airflow DAG patterns or does it conflict?

Produce: Architecture diagram (text is fine) showing the full stack from raw partition write through Superset embedded render. Show the two separate data paths — webhook ingestion (writes to raw partition) vs. app query (reads from materialized view via Superset). These paths must never cross.

---

### Deliverable 3: Migration Sequence

The current schema is unpartitioned. The path to production partitioning is:

```
Phase 1 (now):     Unpartitioned schema — GrowDirect Lab
Phase 2 (Sprint 6): Primary partition per merchant (merchant_id)
Phase 3 (Sprint 6): Temporal sub-partition within each merchant partition
```

Design the migration sequence for Phase 1 → Phase 2 → Phase 3 with zero data loss. PostgreSQL supports converting unpartitioned tables to partitioned via `pg_partman` or manual detach/attach sequences. What is the cleanest path given our Alembic migration pattern?

---

## Deliverable 4: SLA Architecture Validation

The North Star v1.1 defines a four-tier performance menu (Starter / Growth / Pro / Enterprise) with corresponding dashboard refresh cadences (nightly / hourly / 15-min / near-real-time). Your DDL and dbt design must support all four cadences from day one.

**Specifically:**
- `merchant_settings` must include `refresh_cadence ENUM('nightly', 'hourly', 'micro_batch')` alongside `partition_grain`
- The Airflow DAG triggering dbt runs must be parameterized by `refresh_cadence` — not hardcoded
- Confirm that a 15-minute micro-batch dbt run on the Pro tier is achievable on current iMac infrastructure without degrading the ingest pipeline
- Confirm that the Chirp evaluation path (ingest → parse → store → rule engine → alert write) is completely decoupled from the materialized view refresh path — these must never share a resource bottleneck

Add a section to your output: **SLA Deliverability Assessment** — can the architecture deliver the four-tier performance contract as specified? If not, what needs to change?

---

## Output File

`_ALX/WorkOrders/output/Tom/Tom_B035_Addendum_TemporalPartition.md`

Sections:
1. Grain recommendation (D-1) with rationale
2. Catalog load assessment at 100 / 1K / 10K merchants (D-2)
3. DDL templates — 3 grain variants
4. dbt + Superset stack recommendation (D-3, D-4)
5. Full stack architecture diagram
6. Migration sequence Phase 1 → Phase 2 → Phase 3
7. SLA deliverability assessment — four-tier performance contract

---

## Deliverable 5: Raw Event Storage Architecture

**Conditional on Jeremy's B-036 ToS verification — do not finalize DDL until Jeremy confirms Square permits raw payload storage.**

If permitted, design the `raw_events` table:

```sql
-- Conceptual shape — Tom finalizes DDL
raw_events (
    event_id        UUID PRIMARY KEY,
    merchant_id     TEXT NOT NULL,          -- partition key
    event_type      TEXT NOT NULL,          -- 'payment.created', 'cash_drawer.shift.updated' etc.
    square_event_id TEXT UNIQUE NOT NULL,   -- Square's idempotency key
    received_at     TIMESTAMPTZ NOT NULL,   -- partition sort key
    payload         JSONB NOT NULL,         -- raw webhook payload verbatim
    payload_hash    VARCHAR(64) NOT NULL,   -- SHA-256 of payload, computed on INSERT
    previous_hash   VARCHAR(64),            -- hash chain link (same pattern as fox_evidence)
    ingestion_log_id UUID REFERENCES ingestion_log(id)
)
PARTITION BY LIST (merchant_id);           -- sub-partition by received_at same as canary_sales
```

**Immutability:** INSERT-only trigger, same pattern as financial tables. No UPDATE, no DELETE. If Square permits storage, the raw payload is immutable evidence from the moment it arrives.

**Hash chain:** compute-on-INSERT trigger using pgcrypto. Hash covers the full JSONB payload + received_at + square_event_id. Chain links raw_events to itself per merchant partition — proves payload has not been altered since receipt.

**Purpose:** replay (reprocess historical events against updated Chirp logic), audit (ground truth if merchant disputes a Chirp), gap insurance (backfill parsed fields if SDK audit reveals missed data).

**If Square ToS restricts storage:** flag to ALX. Tom holds `raw_events` DDL. Syd assesses what is and isn't storable. Architecture proceeds without raw_events until Syd clears it.

## Deliverable 6: anchor_receipts Table Design

**Conditional on Jeremy's ToS verification — same gate as raw_events.**

If raw payload storage is permitted, the Ordinals anchoring pipeline needs a home in the schema:

```sql
-- Conceptual shape — Tom finalizes
anchor_receipts (
    anchor_id        UUID PRIMARY KEY,
    merchant_id      TEXT NOT NULL,
    period_start     TIMESTAMPTZ NOT NULL,
    period_end       TIMESTAMPTZ NOT NULL,
    event_count      INTEGER NOT NULL,       -- how many raw events in this anchor
    merkle_root      VARCHAR(64) NOT NULL,   -- SHA-256 Merkle root of period's event hashes
    inscription_id   TEXT,                   -- Bitcoin Ordinals inscription ID (null until confirmed)
    block_height     INTEGER,                -- Bitcoin block height of inscription
    anchored_at      TIMESTAMPTZ,            -- when inscription confirmed on-chain
    anchor_hash      VARCHAR(64) NOT NULL,   -- hash of this receipt (chain integrity)
    previous_hash    VARCHAR(64)             -- links to prior anchor_receipt for merchant
)
```

**Also assess:** Ordinals inscription tooling options. Three paths:
- `ord` CLI (self-hosted Bitcoin node required — heavyweight)
- Third-party inscription API (Ordinalsbot, Unisat — simpler, introduces a service dependency)
- Custom lightweight inscriber using Bitcoin RPC directly (most control, most build)

Recommend which path fits current infrastructure. Jeremy will implement; Tom designs the interface.

**The strategic context:** read the North Star v1.1 section "The Timestamp Layer" before designing this table. The `anchor_receipts` table is not a logging detail — it is the legal chain of custody that makes Canary's evidence Bitcoin-verifiable without Canary's involvement. Design it accordingly.

---

## Deadline

Sprint 6 architecture decision. Must be resolved before Phase 2 (first real merchant). Not a Phase 1 blocker — GrowDirect Lab runs on the existing unpartitioned schema.

**Sequencing within Sprint 6:**
1. Jeremy ships B-036 SDK audit (including ToS verification on raw payload storage)
2. Tom receives Jeremy's output and finalizes DDL
3. Tom + PhD outputs converge with ALX
4. Syd consent language follows PhD sandbox scope
5. Architecture decision locked

---

*ALX | Chief of Staff | February 26, 2026*
