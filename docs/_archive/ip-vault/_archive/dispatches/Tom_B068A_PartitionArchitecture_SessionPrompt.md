---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Tom — B-068-A: Partition Architecture
## Session Prompt

**Work Order:** B-068, Lane A
**Date:** February 28, 2026
**From:** ALX
**Priority:** 🔴 HIGH — Foundation layer. Gates Tom's own Lane D and Jeremy's Sprint 7 schema work.

---

## Read This First

Before writing a single line of DDL, read this document completely:

```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/PhD/
  GrowDirect_UnifiedArchitectureThesis_v1.0.md
```

Specifically: **Section 3.2 (The Postgres Layer)** and **Section 4 (The Unified Statement)**.

The partition is not a performance decision. It is the Postgres expression of the
same principle that produced the per-merchant hash chain in the patent. Same math.
Different language. The white paper establishes why. Your DDL must express it.

---

## Context You Already Have

You designed the current partition strategy — `PARTITION BY RANGE (transaction_date)`,
monthly child tables — in the Unified Data Model v1.0. That decision was correct for
Phase 1. It is insufficient for Phase 2, and the insufficiency is architectural, not
incidental.

The current spec puts every merchant in the same monthly partition. Row-level security
(RLS) provides tenant isolation at query time, but the data is physically co-located.
Dropping a merchant's old data requires `DELETE WHERE merchant_id = ?` — row-by-row,
no partition pruning, full-table impact.

The correct spec partitions by merchant first, then by period within each merchant.
Each merchant gets their own partition tree. Dropping Merchant A's 2024 data is a
single `DROP TABLE` on one child. Merchant B is untouched.

---

## What You Are Deciding

### Decision 1: Composite Partition Key

Three options. Evaluate all three. Recommend one. Justify it against the principle.

**Option A — Period only (current spec)**
```sql
CREATE TABLE transactions (...)
  PARTITION BY RANGE (transaction_date);
```
Problem: All merchants share each partition. Not merchant-first isolation.
Cannot archive one merchant's data without touching others.

**Option B — Merchant × Period (recommended)**
```sql
CREATE TABLE transactions (...)
  PARTITION BY LIST (merchant_id);

CREATE TABLE transactions_m001 PARTITION OF transactions
  FOR VALUES IN ('m001')
  PARTITION BY RANGE (transaction_date);

CREATE TABLE transactions_m001_2026_01
  PARTITION OF transactions_m001
  FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
```
Result: True merchant isolation. Archive by drop. Hash chain alignment exact.
Risk: Partition catalog size at scale (1,000 merchants × 12 months × 7 tables = 84,000 child tables).

**Option C — Flexible granularity**
Extend Option B so granularity is per-merchant config:
```sql
-- In merchants table:
partition_config JSONB DEFAULT '{"period": "monthly"}'

-- SMB default: monthly
-- Enterprise override: quarterly
-- Config stored at onboarding, affects child table naming only
```
Result: SMB merchants get monthly partitions. Enterprise merchants (50K+ tx/day)
get quarterly partitions. Same isolation principle, right-sized storage granularity.

**Your call.** Make it. Document the tradeoff. ALX will not second-guess the decision —
you own the schema.

### Decision 2: Naming Convention

Establish the standard. Propose it. Example:

```
transactions_{merchant_id}_{year}_{MM}       (monthly, SMB)
transactions_{merchant_id}_{year}_Q{N}       (quarterly, enterprise)
```

All six new tables (see Scope below) must follow the same convention.

### Decision 3: Archive Path

Describe the DROP PARTITION cold storage strategy:
- When does a partition become archive-eligible? (configurable retention floor — see
  14-month NRF calendar floor in Data Strategy North Star)
- What is the DROP sequence (pause writes → export to Parquet → DROP → confirm)?
- Where does it land? (S3/Glacier path, Athena-queryable)
- Who triggers it? (Airflow DAG, scheduled or manual)

### Decision 4: Hash Chain Alignment

Confirm this invariant holds under your proposed partition design:

> Each merchant's hash chain in Sub 1 (the evidence store) is co-scoped with their
> partition tree. No hash in Merchant A's chain references a record in Merchant B's
> partition. The evidence layer and the query layer are consistent by construction.

If the composite key design creates any risk of cross-merchant chain contamination,
flag it. This is a patent claim dependency — it must be watertight.

---

## Scope: Tables to Partition

Apply your decision to all of these. The CRDM has seven tables that carry
per-merchant transaction-level data:

| Table | Database | Notes |
|---|---|---|
| `transactions` | `canary_sales` | Primary fact table |
| `transaction_line_items` | `canary_sales` | E1-F6 — new |
| `transaction_tenders` | `canary_sales` | E1-F7 — new |
| `refund_links` | `canary_sales` | Existing |
| `cash_drawer_shifts` | `canary_sales` | E1-F8 — new |
| `employee_timecards` | `canary_sales` | E1-F9 — new |
| `gift_card_activities` | `canary_sales` | E1-F10 — new |
| `inventory_adjustments` | `canary_sales` | E1-F11 — new |

Produce DDL for `transactions` in full detail. For the remaining six, produce the
template pattern — Alembic migration can apply the template at Sprint 7.

---

## The gLog Investor Paragraph

One paragraph. Not technical. Investor-facing. Explain why the per-merchant partition
strategy is a scaling story and a moat story — not just a DBA decision.

The white paper (Section 3.2) gives you the framing:
- DROP TABLE not DELETE
- Each merchant independent, like a Bitcoin UTXO
- Black Friday at Merchant A doesn't touch Merchant B
- Archive is surgical: one merchant, one period, one command

Write it in plain English. ALX will route it to the investor deck.

---

## Output

```
Canary_IP/Markdown/Specs/B068_PartitionArchitecture_v1.0.md
```

Structure:
1. Decision: composite key recommendation + justification
2. Naming convention
3. Full DDL — `transactions` complete, others templated
4. Archive path + DROP sequence
5. Hash chain alignment confirmation
6. Scale assessment (partition catalog at 100 / 1K / 10K merchants)
7. Migration path from current unpartitioned schema (zero data loss)
8. The gLog investor paragraph

---

## Coordination

**Runs parallel with Lane D** (vocabulary schema). No dependency between A and D.
Both read the white paper. Both apply the same principle at different layers.

**Gates:**
- Jeremy: Sprint 7 schema migration — reads your output before writing Alembic migrations
- Syd: FCRA/CRA partition isolation opinion (B-035) — your DDL is her technical input

**Does not gate:**
- Condor's Blueprint v2.0 (Lane B) — runs in parallel
- Lane C — runs after Lane B

---

*ALX | B-068-A | February 28, 2026*
*"The partition is the hash chain. Write it that way."*
