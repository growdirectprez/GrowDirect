---
type: research
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Tesco Operating Model → Canary LP Process Mapping

> **Source:** Tesco Operating Model v1.24 (OM Map, January 2007) + TOM Property Services (July 2006)
> **Archive:** `~/GrowDirect/ALX_SYS/ALX/Tom/PROCESSES/`
> **Documented by:** Jeffe — "the other Tom"
> **Purpose:** Map Tesco's enterprise operating model to Canary LP's MCP service layer, identifying scale-invariant process patterns

---

## Why This Matters

The Staples Level 2 (1996) defined **26 merchandising processes** for a single retailer. The Tesco Operating Model (2007) defines **~100 processes across the entire retail value chain** for the world's 3rd-largest retailer (at the time). Together, they bracket the complete ontology of retail operations from SMB to enterprise.

**Canary's thesis:** The process ontology is scale-invariant. A corner cafe and Tesco both need price integrity, sales validation, shrink minimization, and operational insight. The difference is complexity and volume, not category structure.

---

## Tesco Value Chain → Canary MCP Services

### TIER 1: Direct Canary Implementation

Processes where Canary provides the equivalent function for Square merchants:

| Tesco Process | Value Chain | Canary MCP Service | How |
|---|---|---|---|
| **Validating sales & tender movements** | FINANCIAL CONTROL | `canary-chirp` | This IS Chirp. Real-time validation of every Square transaction vs. expected patterns. Tesco did this in batch via sales audit; Canary does it per-webhook. |
| **Maintain price integrity** | STORE OPERATIONS | `canary-chirp` | Price override detection, below-cost alerts, markdown monitoring. Chirp Tier 1 stateless rules catch pricing errors in real-time. |
| **Minimise shrink** | STORE OPERATIONS (SELLING) | `canary-chirp` + `canary-owl` + `canary-fox` | Canary's ENTIRE purpose. Tesco had dedicated LP teams; Canary is the LP team for SMB merchants. |
| **Monitor commercial performance & take action** | STORE OPERATIONS | `canary-analytics` + `canary-owl` | Heatmap scoring, velocity engine, heartbeat. Owl surfaces The One Thing — the single most important action the merchant should take. |
| **Execute store stock take** | STORE OPERATIONS | `canary-analytics` | Inventory adjustment tracking, stock count discrepancy detection. |
| **Control tender movement** | STORE OPERATIONS (SELLING) | `canary-chirp` | Cash drawer rules — open/close anomalies, variance detection, timing patterns. |
| **Reduce to clear & waste stock** | STORE OPERATIONS | `canary-chirp` | Markdown and waste detection rules. Loss through operational process failure (Beck & Peacock Ch 7). |
| **Checkout service and performance** | STORE OPERATIONS (SELLING) | `canary-chirp` + `canary-analytics` | Transaction speed anomalies, void rates per employee, refund pattern detection. |
| **Maintain accuracy of store stock records** | STORE OPERATIONS | `canary-chirp` | Inventory adjustment rules. Discrepancies between expected and actual stock levels. |

### TIER 2: Canary Observes (Owl Context + Fox Cases)

Processes that Canary doesn't execute but monitors for anomaly patterns:

| Tesco Process | Value Chain | Canary Layer | How |
|---|---|---|---|
| **Execute promotions in store** | STORE OPERATIONS | `canary-chirp` + `canary-owl` | Promotional pricing creates highest-risk windows. Chirp detects promotional anomalies; Owl contextualizes against expected uplift. |
| **Set retail price** | DEFINE THE OFFER | `canary-owl` context | Owl's analytics lens tracks price change events and their downstream effects on transaction patterns. |
| **Receive stock into store** | STORE DISTRIBUTION | `canary-chirp` | Delivery discrepancy rules. Receiving is where "the opportunity structure" (Beck & Peacock) is highest for non-malicious shrinkage. |
| **Return stock to supplier** | STORE DISTRIBUTION | `canary-chirp` | Return-to-vendor anomalies — patterns suggesting vendor fraud or operational failure. |
| **Budget planning** | FINANCIAL CONTROL | `canary-analytics` | Plan-vs-actual variance is core context for Owl's recommendations. Heartbeat scoring uses expected baselines. |
| **Control concession sales** | STORE OPERATIONS (SELLING) | `canary-analytics` | For multi-location merchants, inter-location patterns surface via heatmap scoring. |
| **Run local marketing** | STORE OPERATIONS (SELLING) | `canary-owl` context | Marketing events create expected transaction volume changes — Owl needs this context to avoid false positives. |

### TIER 3: Strategic Layer (Condor + Future)

Processes that map to Canary's external intelligence and cross-merchant analytics:

| Tesco Process | Value Chain | Future Canary Layer | Notes |
|---|---|---|---|
| **Create commercial strategic plan** | STRATEGIC OPERATIONS | `canary-condor` | Cross-merchant benchmarking, industry trends |
| **Operational insight** | OPERATIONS DEVELOPMENT | `canary-condor` | NRF benchmarks, operational best practices |
| **Solution generation** | OPERATIONS DEVELOPMENT | `canary-condor` + `canary-owl` | Owl recommends; Condor provides external intelligence for recommendations |
| **Trial & test of solution** | OPERATIONS DEVELOPMENT | `canary-ops` | Health Check is the trial mechanism — ephemeral audit that surfaces quick wins |
| **Implement operational change** | OPERATIONS DEVELOPMENT | `canary-ops` | Post-Health-Check action plans |
| **Management Information (all reports)** | MANAGEMENT INFORMATION | `canary-analytics` + `canary-bff` | 8 report categories → dashboard views. Canary collapses these into a single merchant-facing dashboard. |

### TIER 4: Not Canary's Job (But Process Architecture Informs Design)

| Tesco Process | Value Chain | Why Not |
|---|---|---|
| Define the Offer (most) | DEFINE THE OFFER | Merchant's strategic decisions — Canary observes outcomes, not inputs |
| Acquire/Manufacture (all) | ACQUIRE/MANUFACTURE | Supply chain operations — Square doesn't surface this data |
| Forecast & Order (all) | FORECAST & ORDER | Inventory management — future opportunity if Square Inventory API used |
| Primary Distribution (all) | PRIMARY DISTRIBUTION | DC operations — not SMB-relevant |
| IT/Operations (all) | IT/OPERATIONS | Internal Canary concern, not merchant-facing |
| People (all) | PEOPLE | HR processes — Canary sees employee ID on transactions but doesn't manage people |
| Property Services (all) | PROPERTY | Physical infrastructure — not digital |

---

## The Key Insight: Tesco's Open Question

The Property Services TOM documented an unresolved question:

> **"Who has the A for Loss Prevention in TOM?"** — Status: Unresolved

In 2006, one of the world's largest retailers couldn't definitively assign accountability for loss prevention within their operating model. This is because LP cuts across every value chain category — it's not a department, it's a lens.

**This validates Canary's architectural decision:** LP is not a standalone module. It's an overlay across the entire transaction lifecycle. Chirp watches everything. Owl interprets everything. Fox investigates anything. The "A" for loss prevention is the system itself.

---

## Cross-Reference: Tesco OM × Staples Level 2

The two process architectures complement each other:

| Dimension | Staples Level 2 (1996) | Tesco OM (2007) |
|---|---|---|
| **Scale** | Single retailer, merchandising focus | Global retailer, complete value chain |
| **Depth** | 26 processes, deep L2/L3 detail | ~100 processes, L1 with some L2 |
| **Focus** | Merchandising planning & execution | End-to-end retail operations |
| **LP treatment** | Implicit — through sales audit + performance monitoring | Explicit — "Minimise shrink" as named process |
| **Financial** | Performance levers (4) | Full financial control suite (12 processes) |
| **Technology** | Batch systems, weekly cycles | Real-time ambition, JDA/Retek stack |
| **Key loop** | Price Mgmt → Sales Audit → LP → Margin Monitoring | Sales Validation → Shrink Minimisation → Performance Action |

### Combined Process Coverage for Canary

| Canary MCP Service | STPL Level 2 Processes | Tesco OM Processes | Total Coverage |
|---|---|---|---|
| `canary-chirp` | 5 (Price Mgmt, Performance, Store Inventory, Sales Audit, Receiving) | 9 (Validate sales, Price integrity, Minimise shrink, Control tender, Reduce/waste, Checkout, Stock accuracy, Receive, Returns) | **14 unique process origins** |
| `canary-owl` | 3 (Vendor Mgmt, Promotion, Merch Planning) | 4 (Monitor performance, Promotions, Pricing, Marketing) | **7 unique process origins** |
| `canary-analytics` | 4 (OTB/OTS, Replenishment, Allocation, Performance Monitoring) | 5 (Budget planning, Stock take, Concession, Performance, Reports) | **9 unique process origins** |
| `canary-fox` | 1 (implicit — LP cases) | 1 (Minimise shrink → investigation) | **2 process origins** |
| `canary-condor` | 2 (Vendor Analysis, Chainwide Planning) | 5 (Strategic plan, Insight, Solution gen, Trial, Implement) | **7 process origins** |

**Total: 39 distinct retail operations processes from two independent architectures inform Canary's 5 core MCP services.**

---

## The 4-Question Framework (from TOM Property Services)

Tesco documented each process with 4 questions. This is the template for our SDD process documentation:

1. **What we do** — Level 1 process description
2. **What does that mean?** — Detailed scope and boundaries
3. **Why do we do it** — Business value delivered
4. **How do we measure it** — KPIs and success criteria

Canary adaptation:
1. **What the MCP service does** — Tool contract + behavior
2. **What that means for the merchant** — User-facing impact
3. **Why it matters** — Loss prevented, insight gained, action enabled
4. **How we measure it** — Alert accuracy, response time, merchant action rate

---

## Lineage

```
Tom Hoover / PwC / Management Horizons (1996)
 → 26 retail merchandising processes for Staples Inc.
 → A/R/M/E accountability matrices

Tesco IT Change Programme (2001-2007)
 → ~100 retail operating processes (TOM v1.24)
 → 4-question process documentation standard
 → "Who has the A for Loss Prevention?" — unresolved

Both documented by Jeffe → GrowDirect process library
 → Canary Data Model / Secure EBR at SysRepublic (2004-2020)
 → elJeffe Protocol / Webhook Pipeline (Patent 63/991,596)
 → Canary LP MCP services (2025-present)
```

Beck & Peacock (2009) and Speights/Downs/Raz (2017) independently validated the same framework from academic perspectives. The STPL Level 2 and Tesco TOM provide the practitioner implementation evidence.

---

*Extracted and mapped 2026-03-09 | GrowDirect Inc. | Confidential*
