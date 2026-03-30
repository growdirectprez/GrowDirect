---
type: research
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# IBM Retail Business Intelligence Solution — Extraction Index

> **Source:** `~/GrowDirect/ALX_SYS/ALX/Tom/FEATURES/Retail Business Intelligence Solution V7.ppt`
> **Author:** Steve Gordon (IBM), Daniel Graham (IBM, March 2004)
> **Template:** "A bluepearl baseline IBM V6" (IBM BluePearl consulting practice)
> **Period:** 2004-2005 (created April 2004, last saved October 2005, 182 revisions)
> **Context:** IBM's enterprise retail BI architecture — documented by Jeffe

---

## Why This Matters

IBM's Retail Business Intelligence Solution (V7) represents the enterprise-grade approach to retail analytics that Canary modernizes for SMB. Where IBM required DB2, ETL pipelines, data warehouse teams, and statistical staffs — Canary delivers the same analytical coverage through Square webhooks, real-time rule evaluation, and AI interpretation.

> **NOTE:** This is ARCHITECTURE and ANALYTICAL FRAMEWORK reference only — not technology. DB2, Alphablox, Lotus Freelance, and 2004-era infrastructure are irrelevant. The value is in IBM's taxonomy of retail business solution templates and how they map to Canary's detection and analytics layers.

---

## Three-Layer Architecture (RDWM + RBSTs + RSDM)

| Layer | Full Name | Purpose | Canary Equivalent |
|-------|-----------|---------|-------------------|
| **RDWM** | Retail Data Warehouse Model | Logical Entity-Relationship Model for the central data warehouse | `canary_metrics` star schema + `canary_sales` transaction tables |
| **RBSTs** | Retail Business Solution Templates | Logical Measure/Dimension Models for multidimensional analysis | Chirp rules + scoring engines + dashboard queries |
| **RSDM** | Retail Services Data Model | Classification (metadata) model for defining business meaning across all models | CDM v1.0 (Canary's data serialization standard) |

### RDWM Architecture Flow

```
ETL/Messaging → Enterprise Data Warehouse → Analysis/Data Marts → Metadata Management
 ↓ ↓
 Relational Server Data Mining / Predictive Modeling
 (Accounting, Inventory, (PTM methodology)
 Products, Customers,
 Merchandising, Store Ops,
 Mgt Reporting)
```

### RBSTs — Definition

> "The Retail Business Solution Templates are a grouping of measures and dimensions that satisfy a particular business requirement."

- **Measures** = facts that quantify business performance indicators (composed of sub-measures)
- **Dimensions** = criteria or segments by which measures are broken down (with levels of members)

This is exactly what Canary's star schema implements: `daily_metrics`, `hourly_metrics`, `period_metrics`, `employee_metrics`, `product_metrics` are measure tables; `dim_*` tables are dimension tables.

---

## 5 Analysis Domains → 14 BSTs

### Store Operations Group
| BST | Key Reports | Canary Mapping |
|-----|-------------|----------------|
| **Loss Prevention** | Baseline exception reports, Cashier exceptions (over/under), Inventory discrepancy, Employee schedule compliance associated with loss, Receiver exception report | Chirp rules (29 rules across 8 categories), Fox cases, Vault evidence |
| **Store Location Analysis** | Store performance by location | Dashboard heatmap scoring, location-level metrics |
| **Store Optimization / Staffing** | Employee schedule compliance, Cashier performance metrics, Cross-training reports, Sales person productivity, Skills v Employees, Years of service, Employee details | Employee metrics star schema, timecard anomaly detection |

### Customer Management Group
| BST | Key Reports | Canary Mapping |
|-----|-------------|----------------|
| **Purchase Profiles** | Category sales by demographics, Loyalty points by store, Sales value/quantity by products vs customers, Product penetration | Future: loyalty event analysis |
| **Customer Profiles** | Customer attributes, Status by attribute, Cumulative % sales by decile, Customer base dynamics | Not applicable (Square doesn't surface customer-level analytics to merchants) |
| **Product Purchasing RFQ** | Repurchase interval, Repurchase propensity, Distribution of customers/transactions by units | Future: product velocity patterns |
| **Campaign & Promotion Analysis** | Promotion sales performance, Profit contribution, Effect by media, Response by customer segments, Market basket | Future: promotional anomaly detection (Chirp Tier 3) |

### Merchandising Group
| BST | Key Reports | Canary Mapping |
|-----|-------------|----------------|
| **Inventory Analysis** | On-order vs on-hand, Days of supply, Out of stock by product, Damages/Aged products, Safety stock, Slow-moving inventory, Transfers | Inventory adjustment detection (Chirp), stock count discrepancy |
| **Assortment / Allocation Analysis** | Traited vs value, Base profit contribution, Product sales by store format, Category performance, Product affinity | Future: category-level analytics |
| **Promotion Analysis** | Promotion sales, Profit contribution, Promotional impact on store traffic, Category impact, Promotion fade | Future: post-promotion anomaly detection |
| **Pricing Analysis** | Set vs Actual Price Sold, Price Competitive Exception, Markdown Trend, Price Elasticity, Multi-Channel Price | Chirp price integrity rules, discount detection |
| **Physical Merchandising / Space Management** | Same layout comparisons, Revenue per sq ft, Category profitability to physical presence, Section elasticity/adjacency | Not applicable (physical space data not available via Square) |

### Multi-Channel Group
| BST | Key Reports | Canary Mapping |
|-----|-------------|----------------|
| **eCommerce Analysis** | Session cycle analysis, Shopper segmentation, Product category analysis, Clickstream patterns, Payment methods | Future: Square Online integration |
| **Catalog / Call Center** | Cross-catalog profiles, Operator closure rates, Cold call conversions | Not applicable |

### Corporate Finance
| BST | Reports | Canary Mapping |
|-----|---------|----------------|
| **Capital Allocation, Finance Management, Income Analysis** | Partner credit risk, Organization profitability, Planning & forecasting | Not applicable (enterprise finance layer) |

---

## Loss Prevention BST — Deep Dive

This is the BST most directly relevant to Canary. IBM's LP BST defined 5 report categories:

| IBM LP Report | What It Detects | Canary Implementation |
|---------------|-----------------|----------------------|
| **Baseline exception reports** | Transactions outside expected patterns | Chirp Tier 1 (stateless) + Tier 2 (pattern) rules — threshold-based anomaly detection |
| **Cashier exceptions (over/under)** | Cash drawer variances by employee | Chirp cash drawer rules: C-063, C-064, C-065, C-066, C-067, C-068 |
| **Inventory discrepancy** | Stock count vs expected inventory | Chirp inventory rules: C-080, C-081, C-082, C-083, C-084, C-085 |
| **Employee schedule compliance associated with loss** | Off-schedule activity correlated with losses | Chirp timecard rules: C-040, C-041, C-042 — off-clock transaction detection |
| **Receiver exception report** | Delivery/receiving anomalies | Gap: Square API doesn't surface receiving data. Future via inventory adjustments. |

**Key insight:** IBM needed an entire BST team and DB2 data warehouse to produce these reports. Canary evaluates the same exception patterns per-webhook in real time.

---

## Embedded Analytics — PTM

IBM's **PTM** (Predictive Transaction Mining) was a patented methodology to enable DB2 to perform data mining without a data miner. Key use case: predictive promotion targeting based on purchase history.

Canary equivalent: Owl's pattern detection + ALX's entity extraction. Same goal (surface actionable patterns from transaction data), modernized approach (LLM interpretation vs statistical models).

---

## Case Study: Disney Store Acquisition (2005)

Challenge: Integrate Disney Store acquisition, develop enterprise view in 6 months, deliver transaction-level information to Finance and Marketing.

Solution: RDWM + RBSTs + Alphablox. Result: Marketing and Finance on same page, acquisition integration completed, new merchandising opportunity identified for key customer segment.

**Canary parallel:** Health Check does the same thing — takes a merchant's raw transaction data and surfaces actionable insights in minutes, not months.

---

## Value Proposition Alignment

IBM's stated value to retailers (from slide content):

| IBM Value | Canary Equivalent |
|-----------|-------------------|
| "Sense and Respond — Triggers and Alerts responding to business conditions" | Chirp rule engine + real-time webhook evaluation |
| "Real-time inventory alerts" | Chirp inventory category rules |
| "Labor scheduling" (staffing optimization) | Timecard anomaly detection |
| "Category management, buying criteria, vendor analysis/performance" | Future: Owl's analytics lens, Condor benchmarks |
| "CRM RFM and real-time promotions and offers" | Future: loyalty event analysis |
| "Delivery of data to executive decision makers" | Owl: The One Thing, Health Check reports |
| "Delivery to the store and store management" | Mobile 3-panel UX (Chirps + Owl + Vault) |
| "A common foundation for supporting all activities through an enterprise model" | Three-database architecture + Canary Data Model serialization |

---

## Architecture Subdirectory

The source directory also contains an `Architecture/` subdirectory with SRD (Space, Range, Display) implementation documents. These connect Tesco TOM to the IBM BI implementation:

| File | Size | Content |
|------|------|---------|
| `SRD Detailed Solutions Architecture v0.0.1.doc` | 4.2MB | SRD detailed architecture |
| `SRD Solutions Architecture v0.0.11.doc` | 3.8MB | SRD solutions architecture (later version) |
| `TOM SRD Hardware v0.1.ppt` | 889KB | Hardware spec for SRD system |
| `TOM Space, Range, Display System Architecture Diagrams v0.10x.vsd` | 1.5MB | Visio architecture diagrams |
| `UK and OM process flows v2.1.ppt` | 1MB | UK and Operating Model process flows |
| `Logical Technology Architecture SRD.vsd` | 291KB | Logical tech architecture |
| `OM V1 SRD Context V2.1.vsd` | 782KB | Operating Model SRD context |

> **Note:** These are Tesco-specific SRD implementation documents — relevant as process architecture reference for how a major retailer connected operating model to technology. Not extracted in this pass.

---

## Extraction Notes

- PPT format: OLE2 binary (PowerPoint 97-2003)
- Extraction method: `strings -n 8` with noise filtering
- Heavy image content: First ~550 lines are Photoshop metadata from embedded images
- Slide text starts at line 555; clean through line 1044
- Binary artifacts resume at line 1045; slide title list at line 1148
- Template metadata: "A bluepearl baseline IBM V6" — IBM's BluePearl retail consulting practice brand
- Author metadata confirms Steve Gordon (IBM) with Daniel Graham acknowledged (March 2004)

---

*Extracted 2026-03-09 | GrowDirect Inc. | Confidential*
