---
type: research
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# IBM Retail Business Intelligence → Canary LP Lineage Map

> **Source:** IBM Retail Business Intelligence Solution V7 (Steve Gordon / Daniel Graham, IBM, 2004-2005)
> **Archive:** `~/GrowDirect/ALX_SYS/ALX/Tom/FEATURES/`
> **Purpose:** Trace the architectural lineage from IBM's enterprise retail BI framework to Canary LP's modern SMB implementation
> **Documented by:** Jeffe — IBM BluePearl era

---

## The IBM Connection

IBM's Retail Business Intelligence Solution (circa 2004) was the enterprise-grade approach to retail analytics. Jeffe encountered this architecture during the SysRepublic period (2004-2020) when building Canary Data Model (Canary Retail Data Model) and Secure EBR for clients who were either IBM retail customers or competing against IBM's approach.

**What IBM built:** A three-layer analytical framework (RDWM + RBSTs + RSDM) requiring DB2, dedicated ETL teams, data warehouse infrastructure, and statistical analysis staff. Target customers: national/global retailers with $100M+ IT budgets.

**What Canary builds:** The same analytical coverage delivered through Square webhooks, real-time rule evaluation, AI interpretation, and a mobile-first UX. Target customers: SMB merchants with zero IT budget.

**The gap IBM could never close:** Delivery to the store floor. IBM's own slides acknowledge this — "Delivery to the store and store management" was aspirational. The analytics lived in executive dashboards, not in the hands of the person behind the register. Canary's Three Panel UX (Chirps + Owl + Vault) solves what IBM couldn't: making the insight actionable at the point of operation.

---

## Architecture Lineage: RDWM → Canary Star Schema

### IBM's RDWM (Retail Data Warehouse Model)

```
Data Sources → ETL/Messaging → Enterprise Data Warehouse → Data Marts → Analysis
 ↓ ↓
 Relational Server Data Mining (PTM)
 • Accounting • Predictive Models
 • Inventory • Segmentation
 • Products • Promotion Targeting
 • Customers
 • Merchandising
 • Store Ops
 • Mgt Reporting
```

### Canary's Implementation

```
Square Webhooks → Webhook Pipeline → canary_sales (raw) → Chirp (real-time) → canary_metrics (star schema)
 ↓ ↓ ↓
 WRITE-ONCE IMMUTABLE Alert + AlertHistory Measures + Dimensions
 • transactions • 29 detection rules • daily_metrics
 • refunds • 3 evaluation tiers • hourly_metrics
 • cash_drawer_shifts • auto-case triggers • period_metrics
 • gift_card_activities • employee_metrics
 • loyalty_events • product_metrics
 • inventory_adjustments • dim_* tables
```

### Layer-by-Layer Mapping

| IBM Layer | IBM Implementation | Canary Implementation | SDD |
|-----------|-------------------|----------------------|-----|
| **Data Capture** | ETL batch from POS/ERP | Real-time Square webhooks via Webhook Pipeline | SDD-001 |
| **Serialization** | RSDM metadata model | CDM v1.0 + parser suite | SDD-002, 003, 004 |
| **Raw Storage** | Enterprise Data Warehouse (DB2) | `canary_sales` (PostgreSQL, WRITE-ONCE IMMUTABLE) | SDD-027, 028, 029, 030 |
| **Detection** | RBSTs queried in batch | Chirp stateless rule engine (per-webhook) | SDD-005, 019, 021, 022 |
| **Aggregation** | Data Marts (star schema cubes) | `canary_metrics` star schema | SDD-032, 013 |
| **Analysis** | PTM data mining + Alphablox | Owl AI + heartbeat + heatmap + velocity | SDD-006, 007, 016 |
| **Metadata** | RSDM classification model | Canary Data Model field registry + detection rule config | SDD-025, 033 |
| **Presentation** | Executive dashboards | Mobile 3-panel + Owl chat + Health Check report | SDD-056, 014, 017 |

---

## BST → Chirp Rule Category Mapping

IBM defined 14+ Business Solution Templates. Here's how the operational BSTs map to Canary's Chirp detection rules:

### Loss Prevention BST → Chirp Categories

| IBM LP Report | Chirp Category | Rules | Detection Method |
|---------------|---------------|-------|------------------|
| Baseline exception reports | `refund`, `void`, `discount` | C-001 through C-030 | Threshold-based anomaly detection |
| Cashier exceptions (over/under) | `cash_drawer` | C-063 through C-068 | Cash variance per shift/employee |
| Inventory discrepancy | `inventory` | C-080 through C-085 | Adjustment anomaly detection |
| Employee schedule compliance | `timecard` | C-040 through C-042 | Off-clock transaction correlation |
| Receiver exception report | (gap) | — | Square API doesn't surface receiving data |

### Pricing Analysis BST → Chirp Price Rules

| IBM Pricing Report | Chirp Implementation | Rule |
|-------------------|---------------------|------|
| Set vs Actual Price Sold | Price override detection | C-010 (below-cost), C-011 (deep discount) |
| Markdown Trend | Discount pattern tracking | Velocity engine: discount rate trending |
| Price Competitive Exception | Price anomaly detection | Threshold manager: merchant-specific limits |

### Staffing BST → Chirp Employee Rules

| IBM Staffing Report | Chirp Implementation | Rule/Engine |
|--------------------|---------------------|-------------|
| Employee schedule compliance | Timecard anomaly detection | C-040, C-041, C-042 |
| Cashier performance metrics | Employee-level metrics | `employee_metrics` star schema |
| Sales person productivity | Per-employee transaction scoring | Heatmap: employee dimension |

### Inventory Analysis BST → Chirp Inventory Rules

| IBM Inventory Report | Chirp Implementation | Rule |
|---------------------|---------------------|------|
| On-order vs on-hand | Adjustment anomaly detection | C-080, C-081 |
| Damages / Stressed / Aged | Reason-code anomaly detection | C-083, C-084 |
| Slow-moving inventory | (future) | Velocity engine: product-level |
| Transfer report | Transfer anomaly detection | C-085 |

---

## The Analytical Evolution: Batch → Real-Time → AI

| Generation | Era | Approach | Latency | Insight Delivery |
|------------|-----|----------|---------|------------------|
| **IBM RDWM** | 2004 | ETL → Data Warehouse → Cubes → Reports | Hours to days | Executive dashboards |
| **SysRepublic Canary Data Model** | 2004-2020 | Canary Data Model serialization → Secure EBR → Scorecards | Minutes to hours | Operations manager screens |
| **Canary LP** | 2025+ | Webhook → Chirp → Alert → Owl interpretation | Seconds | Merchant's phone (The One Thing) |

**What changed:**
1. **Data ingestion:** IBM needed ETL teams and batch schedules. Canary receives webhooks in real-time.
2. **Detection:** IBM's RBSTs were query templates run against data marts. Chirp evaluates per-transaction against configurable thresholds.
3. **Aggregation:** IBM built multi-dimensional cubes with dedicated infrastructure. Canary's star schema aggregates incrementally via PostgreSQL.
4. **Interpretation:** IBM required statistical staff to read reports. Owl interprets patterns and surfaces The One Thing in natural language.
5. **Delivery:** IBM delivered to executive dashboards. Canary delivers to the store floor via mobile UX.

---

## RSDM → Canary Data Model Lineage

IBM's RSDM (Retail Services Data Model) defined a metadata classification layer — a common vocabulary for business terms across all models and databases. This is architecturally identical to what Canary Data Model (Canary Retail Data Model) provides.

| Concept | IBM RSDM | Canary Canary Data Model |
|---------|----------|-------------|
| **Purpose** | Common business language across enterprise | Canonical data serialization for multi-source retail data |
| **Scope** | All IBM retail models | All Square webhook event types |
| **Implementation** | Metadata repository (DB2) | Parser suite + schema fingerprints + field registry |
| **Governance** | ARTS compliance (retail industry standard) | CDM v1.0 spec + Square API schema tracking |
| **Evolution** | Static metadata maintained by consultants | Schema drift detection auto-updates field registry |

### ARTS Compliance

IBM's RDWM was explicitly "ARTS Compliant" — built to the Association for Retail Technology Standards data model. Canary doesn't claim ARTS compliance (SMB merchants don't care about standards compliance), but the Canary Data Model data model covers the same entities: transactions, tenders, line items, refunds, inventory, employees.

---

## What IBM Had That Canary Doesn't (Yet)

| IBM Capability | IBM BST | Canary Status | Priority |
|---------------|---------|---------------|----------|
| Customer segmentation | Customer Profiles, Purchase Profiles | Not applicable (Square doesn't expose customer analytics) | Low |
| Promotion effectiveness | Promotion Analysis, Campaign Analysis | Future: promotional anomaly detection | Medium |
| Space management | Physical Merchandising | Not applicable (no physical space data) | None |
| Vendor collaboration | Vendor Performance | Future: Condor external intelligence | Low |
| Multi-channel analytics | eCommerce, Catalog, Call Center | Future: Square Online integration | Medium |
| Predictive modeling | PTM (Predictive Transaction Mining) | Owl + ALX entity extraction + Cognee knowledge graph | In progress |
| Executive dashboards | All BSTs via Alphablox | Dashboard (GRO-144) — heatmap + velocity | Shipping |

---

## What Canary Has That IBM Never Did

| Canary Capability | Why IBM Couldn't |
|-------------------|------------------|
| **Real-time per-transaction detection** | IBM batch ETL had inherent latency |
| **AI interpretation of patterns** | LLMs didn't exist; required statistical staff |
| **Mobile-first delivery** | 2004 mobile was WAP/flip phones |
| **Self-service alert configuration** | IBM required consultant engagement for rule changes |
| **Tamper-evident evidence chain** | Hash-chained audit trails + elJeffe protocol |
| **Sub-$2/month per merchant** | IBM solutions required $100K+ implementations |
| **Natural language search** | Owl NL→SQL pipeline (GRO-137) vs SQL-only querying |
| **Merchant-configurable sensitivity** | IBM thresholds were consultant-managed |

---

## Five Foundational Sources — Complete Lineage

Canary LP's detection and analytics architecture draws from five independent sources:

```
1. Tom Hoover / PwC / Management Horizons (1996)
 → 26 retail merchandising processes for Staples Inc.
 → Performance levers, A/R/M/E accountability

2. IBM BluePearl / Retail BI Solution (2004-2005)
 → RDWM + RBSTs + RSDM — enterprise retail analytics taxonomy
 → 14 Business Solution Templates across 5 analysis domains
 → Loss Prevention BST: 5 exception report categories

3. Tesco IT Change Programme / TOM (2001-2007)
 → ~100 retail operating processes across 13 value chain categories
 → "Who has the A for Loss Prevention?" — unresolved
 → 4-question process documentation standard

4. Beck, A. & Peacock, C. (2009)
 → "New Loss Prevention" — Total Retail Loss framework
 → Operational failure as primary shrinkage driver
 → Figure 7.1 shrinkage taxonomy (20/26 rules mapped)

5. Speights, Downs & Raz (2017)
 → Statistical modeling + risk analytics for retail
 → Threshold-based detection methodology
 → Star schema analytics validation

All five documented by Jeffe → SysRepublic Canary Data Model/Secure EBR (2004-2020)
 → elJeffe Protocol / Webhook Pipeline (Patent 63/991,596)
 → Canary LP MCP services (2025-present)
```

---

## Combined Coverage Matrix

| Canary MCP Service | STPL (1996) | IBM RBSTs (2004) | Tesco TOM (2007) | Beck & Peacock (2009) | Speights et al. (2017) |
|-------------------|-------------|-------------------|-------------------|-----------------------|------------------------|
| `canary-chirp` | 5 processes | LP + Pricing + Staffing + Inventory BSTs | 9 processes | Figure 7.1 (20/26 rules) | Threshold methodology |
| `canary-owl` | 3 processes | All BSTs (interpretation layer) | 4 processes | Holistic LP lens | — |
| `canary-analytics` | 4 processes | RDWM star schema + all BST measures | 5 processes | Total Retail Loss measurement | Star schema validation |
| `canary-fox` | 1 process | LP BST (exception → investigation) | 1 process | Case management | — |
| `canary-condor` | 2 processes | Vendor Performance + benchmarks | 5 processes | Industry context | External benchmarks |

**Total: 5 independent foundational sources, spanning 1996-2017, from practitioners (PwC, IBM, Tesco) and academics (Beck/Peacock, Speights/Downs/Raz), all converge on the same process architecture that Canary implements.**

---

*Extracted and mapped 2026-03-09 | GrowDirect Inc. | Confidential*
