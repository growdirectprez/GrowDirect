---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# B-035 Addendum: Temporal Partition Strategy + Query Governor Layer
*Architecture Decision Brief — Parallel Track: Tom + PhD*
**Date:** February 26, 2026
**Author:** ALX (Chief of Staff)
**Status:** DECISION REQUIRED — Sprint 6 architecture gate
**Parent:** B-035 (Per-merchant partition architecture)
**Classification:** CONFIDENTIAL — Internal architecture

---

## Context

B-035 established the per-merchant partition requirement (PARTITION BY LIST on merchant_id). This addendum adds a second dimension: **temporal partitioning within each merchant's partition**, and the **query governor layer** that prevents unbounded queries from degrading system performance at scale.

This brief is routed in parallel to Tom (architecture) and PhD (theoretical validation). Outputs will be converged by ALX before Sprint 6 architecture sign-off.

---

## The Problem — Two Parts

### Part 1: Merchants Think in Different Time Units

Different merchant types have fundamentally different analytical rhythms:

| Merchant Type | Natural Time Unit | Retention Need | Example |
|---|---|---|---|
| High-volume QSR / coffee | Hour | 13 weeks (91 days) | Offset Coffee: hourly variance patterns shift dramatically by daypart |
| General SMB retail | Day | 26 weeks (6 months) | Standard Square merchant: daily shrink review |
| Seasonal / fashion retail | Week (NRF 4-5-4) | 56 weeks (14 months) | Jeffe's North Star floor — full YoY comparison |

The partition grain is not dynamic — it is set at merchant onboarding based on their business type and plan tier. It does not change. If a merchant's needs change, that is a migration event, not a live reconfiguration.

**What this means for the data model:** The temporal sub-partition beneath each merchant's primary partition must reflect their configured grain. Same canonical CRDM schema throughout. Different time bucket sizing.

### Part 2: The Unbounded Query Problem

A merchant (or a third-party app developer building on the CRDM API) does not know — or does not care — what is underneath. They will issue queries like:

```sql
SELECT * FROM transactions WHERE merchant_id = 'offset-coffee-001'
```

Against a merchant with hourly partitions and 2 years of retention, this is **17,520 partition scans** in a single query. At 10 merchants doing this simultaneously: system degradation. At 1,000: outage.

The partition grain solves storage and write efficiency. It does not solve the read problem. A separate layer must govern what queries can reach the raw partition layer — and how.

---

## Proposed Architecture — Two Layers

### Layer 1: Temporal Sub-Partitioning (Tom owns the design)

Each merchant partition (PARTITION BY LIST on merchant_id) is further sub-partitioned by time:

```
canary_sales (root)
├── partition: merchant_id = 'offset-coffee-001'   ← primary partition
│   ├── sub-partition: 2026-02-24 00:00–01:00      ← hourly grain
│   ├── sub-partition: 2026-02-24 01:00–02:00
│   └── ... (91 days × 24 hours = 2,184 sub-partitions)
├── partition: merchant_id = 'some-retailer-002'
│   ├── sub-partition: week of 2026-02-16           ← weekly grain (NRF aligned)
│   └── ... (56 weeks = 56 sub-partitions)
```

**PostgreSQL capability:** Declarative sub-partitioning (PARTITION BY RANGE on timestamp within each LIST partition) is supported natively in PostgreSQL 11+. The query planner performs partition pruning automatically — a query with `WHERE created_at BETWEEN x AND y` touches only the relevant sub-partitions.

**Tom's design questions:**
1. Does sub-partitioning interact cleanly with existing INSERT-only triggers and pgcrypto hash chains? (Hash chain must be self-contained per merchant — sub-partitions should not break the chain.)
2. What is the DDL pattern for the sub-partition template that gets cloned at merchant onboarding?
3. How does Alembic handle sub-partition creation at onboarding time vs. schema migration time?
4. What is the overhead at scale — 100 merchants, 1K, 10K — in terms of partition count and PostgreSQL catalog load?
5. Repartitioning path: current unpartitioned schema → primary partition → sub-partition. What is the migration sequence with zero data loss?

**Merchant grain config:** Stored in `canary_app.merchant_settings` as a new field: `partition_grain ENUM('hour', 'day', 'week')` and `retention_weeks INTEGER`. Set at onboarding. Not user-editable post-onboarding without a migration event.

---

### Layer 2: Query Governor (Tom architects, Jeremy implements)

The raw partition layer is **write infrastructure and audit trail, not a query surface.** No app — first-party or third-party — touches it directly.

**Two-component governor:**

#### Component A: Materialized View Tier

Pre-computed aggregations maintained by Airflow DAGs. These are what apps query — not the raw partitions.

| View | Grain | Retention | Purpose |
|---|---|---|---|
| `mv_daily_summary` | Day | 36 months | Standard dashboard queries — Today's View, scorecards, trends |
| `mv_weekly_summary` | NRF week | 56 weeks | Period-over-period comparisons, OTB planning |
| `mv_hourly_summary` | Hour | 13 weeks | High-frequency merchants: daypart analysis, labor matching |
| `mv_chirp_activity` | Alert-level | 14 months | Chirp firing rates, false positive analysis, threshold tuning |

Airflow refreshes these on a schedule (hourly for hourly-grain merchants, nightly for the rest). Apps read from materialized views. The raw partition layer is never touched by application queries.

**What this solves:** `SELECT * FROM mv_daily_summary WHERE merchant_id = 'x' AND date BETWEEN y AND z` is a bounded, pre-aggregated query hitting an indexed view. Fast. Predictable. No partition scan.

#### Component B: Apache Superset — Query Surface + Permission Layer

Rather than building a custom query governor at the Flask blueprint layer, Canary adopts **Apache Superset** as the managed query surface sitting above the materialized view tier. Superset is already in the Technology Blueprint — this is a deployment decision, not a new vendor.

**What Superset handles natively:**
- Dataset-level permissions — PhD sandbox is a Superset dataset scoped to `benchmark_consent` whitelist. No whitelisted merchant = not in the dataset. Enforced by Superset, not by custom code.
- Role-based access control — merchant sees only their partition's materialized views. PhD sees the Layer C+ dataset. Internal ops see everything. Zero custom permission code.
- Time-bound query enforcement — Superset dataset config enforces mandatory date filters. Unbounded queries are rejected at the dataset level before they reach PostgreSQL.
- Embedded rendering — Superset dashboards embed directly in the Canary app via iframe or Superset's Embedded SDK. Today's View scorecards, trend charts, and PhD benchmark views all render from the same Superset layer.
- Row-level security — Superset RLS rules map `merchant_id` to the authenticated merchant session. One dataset definition serves all merchants safely.

**What dbt handles:**
Instead of hand-writing Airflow DAGs to compute materialized views, **dbt models** define the Layer C and Layer C+ transformations declaratively. Airflow triggers dbt runs on schedule. The Layer C+ whitelist filter is a dbt model `WHERE merchant_id IN (SELECT merchant_id FROM benchmark_consent WHERE syd_approval_date IS NOT NULL)`.

**The resulting stack:**
```
canary_sales (raw partitions — PostgreSQL)
    → dbt models (define mv_daily_summary, mv_weekly_summary, mv_hourly_summary, mv_chirp_activity, Layer C+)
        → Airflow (schedules dbt runs — hourly for hourly-grain merchants, nightly for the rest)
            → Superset (query surface — dataset permissions, RLS, time-bound enforcement, embedded SDK)
                → Canary app (embeds Superset dashboards — merchant scorecards, PhD benchmark views)
```

**What this eliminates from Tom's build list:**
- Custom query governor at the Flask layer
- Custom materialized view refresh logic
- Custom permission enforcement code
- Custom PhD sandbox access control

All of the above become Superset configuration + dbt model definitions. Tom designs the schema. Jeremy deploys Superset and wires the Embedded SDK. PhD configures their dataset in Superset against the consent-gated Layer C+ model.

**Operational cost:** Superset is another service to run. Jeremy assesses whether it deploys cleanly alongside the existing Docker stack and what the memory footprint looks like on current infrastructure. This is the one open question before committing.

#### Component C: API Query Contract (Thin Layer — Superset Handles Most of This)

All data access goes through Canary's API. The API enforces:

1. **Mandatory time bounds** — every query must include a date range. No range = rejected with HTTP 400.
2. **Maximum window** — configurable per tier. Default: 90 days per API call. Enterprise: up to 56 weeks.
3. **Result set limits** — maximum row count per response (pagination required for large sets).
4. **Query routing** — API layer inspects the requested time range and routes to the appropriate materialized view, not the raw partition.

**What this solves:** `SELECT *.*` is not a valid API call. A developer building on the CRDM API cannot accidentally (or intentionally) issue an unbounded scan. The API translates merchant intent into a partition-aware, view-routed, bounded query.

**Raw partition access:** Reserved for two things only:
- Airflow DAGs computing materialized view roll-ups (controlled, scheduled, isolated)
- Evidence chain verification (Fox module — single-row lookups by hash, not range scans)

---

## What This Is NOT

- **Not dynamic.** The partition grain is fixed at onboarding. Changing it is a migration event, not a config toggle. This is correct — a merchant who says "I think in weeks" should stay in weeks until they make a deliberate decision to change.
- **Not a new storage layer.** The materialized views are computed FROM the raw partitions. Same data, pre-aggregated. Not a separate database.
- **Not complex for the merchant.** The merchant never thinks about any of this. They see Today's View, scorecards, Chirps. The partition architecture is invisible to them.
- **Not a blocker for Phase 1.** GrowDirect Lab runs on the existing unpartitioned schema. Partitioning is implemented before Phase 2 (first real merchant).

---

## Decision Points Required

Tom and PhD need to converge on answers to the following before Sprint 6:

| # | Decision | Who Answers | Options |
|---|---|---|---|
| D-1 | Sub-partition grain options: hour / day / week only, or finer? | Tom | Keep it to 3 options — complexity scales with grain count |
| D-2 | Does hourly sub-partitioning at 2 years = 17,520 partitions per merchant create PostgreSQL catalog load issues at 1,000 merchants? | Tom | May need a hybrid: hourly for recent 13 weeks, daily archive for older data |
| D-3 | Materialized view refresh strategy for hourly-grain merchants — how close to real-time? | Tom | Airflow micro-batch (15 min) vs. trigger-based vs. scheduled hourly |
| D-4 | Does the API query contract live at the Flask blueprint layer or a dedicated API gateway? | Tom + Jeremy | Blueprint layer is simpler; dedicated gateway is more scalable |
| D-5 | PhD: Does the unbounded query problem constitute a "debasement" of system performance analogous to monetary inflation? Can PhD frame the query governor as an economic incentive mechanism (cost per query beyond the free tier) rather than a hard technical limit? | PhD | L402 micropayment per API call above the base tier — PhD to assess fit |
| D-6 | Jeremy: Does Superset deploy cleanly into the existing Docker stack? What is the memory footprint on current iMac infrastructure? Is dbt additive or does it conflict with existing Airflow DAG patterns? | Jeremy | Superset ~2GB RAM typical. dbt runs inside Airflow as BashOperator or via dbt-airflow provider — likely additive. Jeremy confirms. |

---

## PhD-Specific Questions

PhD's lens is particularly valuable here on two dimensions:

**1. The aggregation boundary (Layer C)**
The North Star defines Layer C (canary_metrics) as anonymized cross-merchant aggregations. PhD needs to validate that the materialized view tier (Layer 2 Component A) does not accidentally create a Layer C exposure — i.e., that `mv_daily_summary` per merchant cannot be reverse-engineered to identify individual transactions or employees.

**2. The query governor as economic mechanism**
Tom will design the query governor as a technical constraint (time bounds, row limits). PhD should assess whether it also works as an **economic constraint** — L402-gated API access where each call above a base tier costs sats. This would:
- Make unbounded queries economically irrational (they cost money)
- Align with the Dome architecture (PhD Principle #21-23)
- Create a natural tier structure: free tier (bounded, materialized views), paid tier (wider windows, more rows), enterprise tier (raw access under contract)

PhD deliverable: one-page assessment of the economic constraint model as complement or alternative to the technical constraint model.

---

## Alignment with North Star

This addendum extends the Data Strategy North Star (v1.0) in one dimension:

**North Star (current):** "Each merchant gets their own PostgreSQL partition (PARTITION BY LIST on merchant_id)."

**This addendum adds:** "Within each merchant's partition, data is sub-partitioned by a fixed temporal grain (hour/day/week) configured at onboarding. The materialized view tier sits above the raw partition layer and is the exclusive query surface for all application-layer reads. The API query contract enforces time bounds on all requests."

No conflicts with the existing document. This is an additive extension.

---

## PRD Alignment

The PRD (E1-F14) references the API Gateway and Chirp Config page. The query governor layer is infrastructure beneath the API gateway — it is not a PRD feature but an architectural constraint that the API gateway must enforce.

**API Gateway requirement addition:** The Square webhook ingestion pipeline writes to raw partitions. The merchant-facing API reads from materialized views. These are two separate data paths that must never be reversed.

---

## Layer C+ — PhD Analytical Sandbox (Whitelisted Cross-Merchant Aggregations)

PhD requires a controlled access path into anonymized cross-merchant data for internal industry benchmark research. This is distinct from Layer C (canary_metrics) which is computed by Airflow and read by first-party apps. Layer C+ is a research sandbox — internal eyes only, never customer-facing, never externally published without Jeffe approval.

### Architecture

```
Layer A  →  canary_sales partition (merchant data — merchant eyes only)
Layer B  →  canary_app (detection & ops — per-merchant, never shared)
Layer C  →  canary_metrics (anonymized aggregations — Airflow computed, app-readable)
Layer C+ →  PhD sandbox (whitelisted subset of Layer C, consent-gated, Syd-approved, audit-logged)
```

### Access Control — Non-Negotiable Rules

1. **Legal-approved gate. No exceptions.** A merchant's anonymized data cannot contribute to Layer C+ until Syd has reviewed and approved the consent language covering that use. No whitelist entry without Syd sign-off. This is not a technical toggle — it is a legal gate.

2. **Whitelist registry** — `canary_app.benchmark_consent` table. Fields: `merchant_id`, `consent_document_version`, `syd_approval_date`, `approved_by`, `scope` (what data can be used), `expiry`. Syd owns entries. PhD queries only against merchants in this table.

3. **Aggregation only — no drill-through.** PhD sandbox operates on Layer C (`canary_metrics`) only. No access to Layer A (`canary_sales`). PhD can see "coffee shops with 2-3 locations average 0.8% cash variance" — cannot see Offset Coffee's individual transactions, employees, or evidence chains.

4. **Audit log on every sandbox query.** Every query PhD runs against Layer C+ is logged immutably: who, what, when, which whitelisted merchants contributed. If a merchant asks "was my data used in your research" — the answer is verifiable from the log.

5. **Anonymization verified before Layer C population.** No PII, no card fingerprints, no employee names, no merchant-identifiable detail crosses from Layer A to Layer C. PhD validates the anonymization boundary (see PhD deliverables below).

### Consent Language

Syd must draft or amend the following before PhD sandbox goes live:
- Beta Tester Agreement addendum: opt-in clause for anonymized benchmark contribution
- DPA amendment: explicit scope of what "anonymized aggregated data" means and how it is used internally
- Opt-out mechanism: merchant can withdraw consent without losing access to Canary LP

**Syd deliverable:** `_ALX/WorkOrders/output/Syd/Syd_B035_BenchmarkConsentLanguage.md`
**Gate:** PhD sandbox does not receive a single real merchant row until Syd delivers and ALX confirms receipt.

---

## Deliverables Requested

### Tom
- `_ALX/WorkOrders/output/Tom/Tom_B035_Addendum_TemporalPartition.md`
- Sub-partition DDL template (3 grain variants)
- Partition count / catalog load assessment at 100 / 1K / 10K merchants
- Materialized view schema for the 4 standard views
- Answer to D-1 through D-4
- Migration sequence: unpartitioned → partitioned → sub-partitioned

### PhD
- `_ALX/WorkOrders/output/PhD/PhD_B035_QueryGovernor_Economic_Assessment.md`
- Layer C exposure risk assessment (can mv_daily_summary leak cross-merchant signal?)
- L402 query pricing model as economic governor (D-5)
- Theoretical validation that the 3-grain system (hour/day/week) covers the full SMB merchant spectrum without gaps
- Anonymization boundary specification: what fields must be stripped/hashed before a row can cross from Layer A to Layer C
- Layer C+ sandbox scope definition: what benchmark questions PhD intends to answer (feeds Syd's consent language drafting)

### Syd
- `_ALX/WorkOrders/output/Syd/Syd_B035_BenchmarkConsentLanguage.md`
- Beta Tester Agreement addendum (opt-in clause for anonymized benchmark contribution)
- DPA amendment (scope of internal anonymized data use)
- Opt-out mechanism language
- **Gate: PhD sandbox is blocked until this deliverable is confirmed received by ALX**

---

## Deadline

**Sprint 6 architecture decision.** Not a Phase 1 blocker. Must be resolved before Phase 2 (first real merchant onboarding) to ensure the partition template is correct before real data flows.

---

*ALX | Chief of Staff | February 26, 2026*
*B-035 Addendum | Temporal Partition + Query Governor | CONFIDENTIAL*
