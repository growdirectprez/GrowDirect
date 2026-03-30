---
type: pitch
domain: business
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# The Market

> *"Nobody else exists in this space. The market is not contested — it's empty."*

---

## The Gap Nobody Serves

Fortune 500 retailers spend $4.7 billion annually on loss prevention. They have dedicated LP teams, six-figure vendor contracts, enterprise data warehouses, and exception-based reporting platforms that can trace a $3 drawer variance to a specific register at a specific store on a Tuesday at 2:14 PM.

Small retailers have a POS terminal and a dashboard that tells them what sold today.

The National Retail Federation reports average shrinkage at 1.6% of retail sales — a 10-year high. For a coffee shop doing $800K annually, that's $12,800 walking out the door every year. And they have **zero tools** to see it, measure it, or stop it.

The tools that exist are built for enterprises with 500+ locations. A merchant with 3 locations has never been offered anything.

---

## The Square Ecosystem

Square's merchant ecosystem defines the beachhead:

| Metric | Value | Source |
|---|---|---|
| Active merchant accounts | 4.5M+ | Square 10-K, FY2024 |
| Average revenue per merchant | $300K-$500K annually | Square investor reports |
| Square's take rate | 2.6-2.9% per transaction | Square 10-K |
| Third-party marketplace apps | 17,000+ | Square App Marketplace |
| Average subscriptions per merchant | 3-5 add-on apps | Industry analysis |
| Loss prevention apps in marketplace | **Zero** | Square Marketplace audit |

Square merchants are trained to subscribe: payroll ($35/mo), loyalty ($45/mo), marketing ($15/mo), inventory ($60/mo). They already pay for software. They've never been offered loss prevention because nobody has built it.

---

## Market Sizing

### TAM (Total Addressable Market)

The U.S. retail loss prevention industry: **$4.7B annually** (NRF 2024 National Retail Security Survey). This includes all technology, personnel, and services dedicated to reducing retail shrinkage.

### SAM (Serviceable Addressable Market)

LP technology spend for multi-location merchants with 1-50 locations who use modern cloud-based POS systems. Estimated at **$1.2B** based on the portion of shrinkage attributable to SMB retail segments currently unserved by existing vendors.

### SOM (Serviceable Obtainable Market)

1% of Square's 4.5M merchant base at an average of $39/month = **$21M ARR**. This is the near-term target. At 5% penetration: **$105M ARR**.

---

## Competitive Landscape

### Enterprise LP Vendors (Not Competitors — Adjacent)

The enterprise LP market is served by a small number of vendors who sell exclusively to chains with 500+ locations:

| Characteristic | Enterprise LP Vendors |
|---|---|
| Target segment | Fortune 500 retailers, 500+ locations |
| Typical contract | $100K-$500K/yr |
| Sales motion | Enterprise sales team, 6-12 month implementation |
| Product model | On-premise or custom SaaS, analyst-dependent |
| SMB offering | **None** |

**No enterprise LP vendor serves merchants with fewer than 50 locations.** The cost structure, sales motion, and implementation complexity of enterprise LP makes it impossible to serve small merchants profitably with their current model.

### POS Platform Add-Ons (Tangential)

Major POS platforms offer basic reporting dashboards. These show what sold and what's in the bank. They do not perform exception-based reporting, anomaly detection, or loss prevention analytics. They are data display tools, not detection engines.

### Direct Competition

**None.** There is no dedicated loss prevention product for Square merchants in the Square Marketplace. No SaaS product exists that provides exception-based reporting for merchants with 1-50 locations on any POS platform.

---

## The Defensible Moat

### 1. Data Normalization Depth

Anyone can read Square's API docs and trigger an alert when a refund exceeds a threshold. That's a weekend project. The moat is the CRDM — a three-database PostgreSQL architecture that normalizes Square's complex, nested webhook payloads into a canonical retail data warehouse with referential integrity, immutability guarantees, and cryptographic hash chains.

This architecture took 25 years of enterprise experience to design. It doesn't get replicated by a startup reading API documentation.

### 2. Detection Sophistication

26 rules across 8 categories with merchant-configurable thresholds, per-location scoping, and cross-data-source correlation. This isn't "if refund > $100, alert." It's cross-referencing timecard data with payment timestamps to detect off-clock transactions. It's correlating drawer variances with specific employees across shifts. It's pattern detection across time windows.

### 3. Evidence-Grade Audit Trails

The Fox evidence chain produces tamper-proof records with INSERT-only triggers and hash verification. This evidence has legal weight. No other small-merchant tool produces anything like it.

### 4. Aggregation Network Effect

Every merchant who connects adds to the dataset. Anonymized, aggregated transaction patterns across thousands of merchants enable industry benchmarks, fraud pattern libraries, and detection rule refinement. The more merchants connect, the smarter the detection engine gets. A single-merchant tool cannot replicate this.

### 5. Temporal Moat

gLog inscription on the Bitcoin timechain creates a permanent, immutable record of evidence. Block space acquired early compounds in value as the network grows. First mover in small-retail LP data inscription owns the provenance layer.

---

## Why Now

Five forces converge to create this window:

1. **Square's API maturity.** Five years ago, Square's webhook infrastructure was unreliable. Today it's production-grade with 8+ event types, HMAC verification, and robust OAuth. The plumbing is ready.

2. **Shrinkage at a 10-year high.** 1.6% average in 2024, up from 1.4% in 2020. Small merchants feel this more acutely because they have thinner margins and zero tools.

3. **AI changes the delivery model.** Enterprise LP requires analysts to interpret data. Canary's Chirps use AI to translate detection events into plain-language, actionable alerts. The merchant doesn't need to be a data analyst.

4. **No competition in the segment.** The market is empty. Not contested — empty.

5. **The aggregation window is time-sensitive.** Whoever builds the data aggregation layer for small retail first owns the data asset. This is a land grab. Switching costs increase as merchants build history in the platform.

---

## The Platform Play

Loss prevention is the entry point. The CRDM is the platform.

Once a merchant connects their POS, their data flows into the canonical retail data warehouse. The same pipeline that powers loss prevention enables:

- **Demand forecasting** — predict what will sell tomorrow based on historical patterns
- **Labor optimization** — align staffing to transaction volume
- **Menu engineering** — identify margin contributors and underperformers
- **Inventory intelligence** — flag reorder points, track waste, detect shrinkage at the SKU level
- **Vendor analysis** — cost optimization across suppliers
- **Benchmarking** — "your shrink rate is 2.1% — similar coffee shops average 1.4%"

Each capability is a feature that enterprise retailers pay millions for and small retailers have never been offered. The merchant signs up for loss prevention. They stay for the data platform.

The end state: a retail app platform where the merchant connects once, their data populates the CRDM, and they toggle on the apps they want. Every developer building tools for Square merchants today has to solve the data problem from scratch. The CRDM solves it once.

---

*GrowDirect Confidential — Patent Pending — Provisional 63/991,596*
