---
last-compiled: 2026-05-04
needs-review: false
type: reference
status: complete
tags: [rpas, oracle, planning, retail-systems, canary-context]
created: 2026-05-04
source: Oracle RPAS Client v11.0 WebHelp (Tesco US installation, ~2015)
---
last-compiled: 2026-05-04
needs-review: false

# RPAS Planning Paradigm

Oracle Retail Predictive Application Server (RPAS) is the enterprise planning platform used by large-format retailers — Tesco, Kroger, and others — for demand forecasting, range planning, and trading plan development. It runs a multidimensional database server; planners connect via a thick Java client (workbook-driven). This card captures the four architectural concepts most relevant to Canary's planning module design.

---
last-compiled: 2026-05-04
needs-review: false

## 1. Spread Methods — Top-Down Data Entry

The core behavioral contract for any planning system that supports aggregate-level editing. When a planner types a value at a parent level (e.g., Department / Month), the system must distribute that value down to base-level cells (e.g., SKU / Week). RPAS defines four methods:

| Method | Behavior |
|---|---|
| **Replicate** | Copy the exact value to every base cell. Recalculates aggregate after spread. |
| **Even** | Divide evenly across all base cells. |
| **Proportional** | Distribute in proportion to the existing values of base cells before edit. |
| **Delta** | Spread only the *difference* (new − old), evenly across base cells. |

**Proportional is the default expectation.** Retailers assume that editing a department total redistributes change relative to existing mix — not that it overwrites every SKU equally. Delta is used in scenarios where absolute targets are locked and the planner is adjusting a correction.

Canary's OTB, replenishment target, and labor budget modules need to implement this contract. The spread method should be selectable per operation (paste, fill, plan override).

---
last-compiled: 2026-05-04
needs-review: false

## 2. Measure Taxonomy — Role / Version / Units / Metric

RPAS identifies every measure as a 4-tuple:

| Component | Example values |
|---|---|
| **Role** | Working Plan (Wp), Last Year (Ly), Forecast (Fcst), Adjusted (Adj) |
| **Version** | Approved, Draft, Original |
| **Units** | Retail ($), Cost ($), Units (U), Margin ($), % |
| **Metric** | Sales, Receipts, Inventory, Markdowns, GMROI |

A fully addressed measure reads as `Wp Sales R` (Working Plan, Sales, Retail dollars) or `Ly Rcpt U` (Last Year, Receipts, Units). The RPAS UI lets planners filter by any of the four components to narrow the measure list before inserting into a workbook.

Canary needs an equivalent taxonomy. The Role/Version distinction maps directly to Canary's plan-vs-actual-vs-forecast triad. The Units dimension is where Canary's Bitcoin/satoshi cost model introduces a non-standard axis that legacy systems don't have.

---
last-compiled: 2026-05-04
needs-review: false

## 3. Deferred Calculation Mode — Write Batching

RPAS supports two calculation modes:

- **Automatic:** Recalculates dependencies immediately on each cell edit. Expensive on large workbooks.
- **Manual (deferred):** Cell edits queue locally. Server recalculation fires as a batch when the planner explicitly triggers it or commits.

Deferred entries can be rolled back in full (Remove All Deferred Entries) or one at a time (Remove Last Deferred Entry), restoring cells to their pre-edit state.

**Canary relevance:** The pattern is directly applicable to the write path in any planning UI. Recalculating cascading measures (OTB impact on replenishment targets, labor impact on margin) on every keystroke is untenable at scale. Deferred mode with explicit commit is the right UX contract — maps to Canary's pending-change model and the ASAP commit queue.

**Commit ASAP** — RPAS's multi-user variant: when multiple planners are hitting the same domain, Commit ASAP queues the workbook for commit as soon as server resources are available, rather than forcing synchronous commit (which causes write conflicts). Canary's multi-tenant concurrent writes face the same problem.

---
last-compiled: 2026-05-04
needs-review: false

## 4. Exception Model — Measure-Level Threshold Alerting

RPAS exceptions are per-measure rules: define a minimum and maximum acceptable range. Any cell value outside the band is flagged with configurable visual formatting (text color, fill color, font). Rules are stored per user per workbook; the Alert Manager surfaces all active violations in a single panel.

Planners can navigate violations sequentially (Find Next Alert / Find Previous Alert) or review the full list via Alert Manager.

**Canary relevance:** This is the LP exception detection paradigm at the planning layer — not the transaction layer. Canary's monitoring modules operate at transaction speed, but the *planning* modules (OTB, replenishment targets) need the same threshold-band model for plan quality control. Exception formatting at the measure level is the UX expectation any RPAS-trained planner will carry.

---
last-compiled: 2026-05-04
needs-review: false

## What RPAS Is Not

- **Not API-native.** No REST layer; data flows via proprietary MDAP bridge protocol (Retek MDAP, Java serialized). Integration requires ETL, not API calls.
- **Not real-time.** Domain data is batch-loaded; workbooks reflect a snapshot, not live store data.
- **Not SMB-viable.** Requires Oracle license, dedicated RPAS server infrastructure, and trained implementation team. Tesco's instance ran Production and Patch environments on dedicated hardware.

This is the gap Canary exploits: API-native, real-time, no separate planning server required.

---
last-compiled: 2026-05-04
needs-review: false

## Source Context

- **System:** Oracle RPAS v11.0 (Oracle Predictive Solutions, build 1.2701)
- **Installation:** Tesco US (Fresh & Easy), server `tussrddb00`, domain `RANGE_SYSTEM`, path `/rangedoms1/domain/RANGE_SYSTEM`
- **Environments:** Production (172.28.16.119) · Patch (172.28.16.118)
- **Archive:** `Brain/raw/inbox/RPAS Client/` — InstallShield installer + WebHelp documentation + binary `.fcf` client config

[[Brain/wiki/canary-go-portal]] · [[Brain/projects/Canary]]
