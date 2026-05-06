---
date: 2026-04-24
type: project-moc
classification: internal
owner: GrowDirect LLC
tags: [retail-spine, rbis, capability-matrix, moc]
sources:
  - Brain/raw/inbox/retail-business-intelligence-solution-v7.md
  - Brain/raw/inbox/GAP/GAP BI/RBIS background/Retail Business Intelligence Solution V7.ppt
  - Canary-Retail-Brain/modules/
status: v0.6
---

# RetailSpine — MOC

> **Linear tracker:** [GRO-522 — Retail Spine Brain documentation pairs](https://linear.app/growdirect/issue/GRO-522/retail-spine-brain-documentation-pairs-canonical-catz-spec-private) (Canary project). v1 done (GRO-523); v2.C/D/F/J open as GRO-524/525/526/527; CATz shell-fill GRO-528; inbox sweep GRO-529.

## Summary

RetailSpine is the **internal working layer** for the canonical retail-
capability decomposition that ships in the Canary repo as
[`Canary/docs/retail-capability-model.md`](../../Canary/docs/retail-capability-model.md).

The spine is derived from a 2005-era enterprise retail BI reference deck
plus a 2006-era top-down operating-model decomposition: six business-
management domains, each broken down into capabilities, with named
reports as the leaf deliverables, plus three cross-cutting operating-
model functions (People, Property, Retail Operations).

Every other retail artifact in this vault — enterprise interface specs,
Solex e-commerce fixture, prior-art wiki cards, Canary detection rules,
future microservices — gets cataloged *against this spine*. The spine is
the shape; the rest fills the cells.

**Canonical / shipping version.** Any reference outside this vault
(Canary docs, SDDs, public/customer-facing material) MUST point at
`Canary/docs/retail-capability-model.md`, which is fully vanilla — no
vendor names, client names, or proprietary product names. The Brain
artifacts below retain attribution for our own audit trail.

## Why RBIS

RBIS already did the work. It is:

- **Practitioner-validated** — IBM shipped this decomposition into Fortune-500
  retailers for years. The names, groupings, and report inventories survived
  contact with real merchandising, store-ops, and finance teams.
- **Granular enough to index against** — six domains × ~20 BSTs × dozens of
  reports gives us cells small enough that a Tesco interface or a Canary rule
  can map cleanly into one or two cells, not "well, it touches everything."
- **A real artifact, not invented taxonomy** — full transcription lives at
  [[Brain/raw/inbox/retail-business-intelligence-solution-v7|retail-business-intelligence-solution-v7]].
  Every BST in this MOC is traceable to a slide.

We use RBIS as-is even though the 2005 naming ("Corporate Finance Management")
sounds enterprise. Renaming to microservice-speak (Catalog / Pricing / Orders)
is a derived view we can produce later. The spine itself stays RBIS so it
remains traceable.

## Design principles

1. **ODS-as-EDW collapse.** The 2005 enterprise reference assumes a
   five-tier stack (Operational → ODS → EDW → marts → reports). For SMB,
   the ODS *is* the EDW — three tiers, sometimes two. The BST capabilities
   stay; the warehouse goes. Same answers, ~1/100th the infrastructure.
2. **Capability-first, not schema-first.** The spine catalogs *what
   questions a retailer answers*, not what tables hold the answers. Schema
   mapping (Canary's `app` / `sales` / `metrics` plus any new
   operational schemas — Fox tables live in `app`, despite the module
   path) is a separate session.
3. **Cells reference, they don't reproduce.** A BST cell links to source
   artifacts (Tesco interface IDs, Solex flows, Secure wiki cards). It does
   not reproduce them. The spine is the index, not the encyclopedia.
4. **Multi-Channel is a domain, not a cross-cut.** RBIS slide 19 treats
   it as a sixth peer to Customer / Products & Services / Merchandising /
   Store Ops / Corporate Finance. We follow the source rather than
   collapsing it into a delivery-channel attribute on every other domain.
5. **Build, don't organize.** v0 of this MOC is the spine and the BST
   inventory. Cross-references to Tesco / Solex / Secure / Canary fill in
   over subsequent sessions, one source at a time.

---

## The six domains

Listed in RBIS slide-19 reading order. Each domain gets a short purpose
statement, the BST inventory from RBIS slide 19 (broad), and the
sample-report inventory from RBIS slides 38–42 (deep, where present).

### 1. Customer Management

**Purpose.** Understand who the customer is, what they buy, why they buy,
how they move through segments, and when they leave. Drives loyalty,
campaign targeting, lifetime-value optimization, and customer-risk decisions.

**BST inventory (slide 19):** Campaign & Promotion Analysis · Cross Purchase
Behavior Analysis · Cross Sell Analysis · Customer Attrition Analysis ·
Customer Complaints Analysis · Customer Credit Risk Profile · Customer
Delinquency Analysis · Customer Interaction Analysis · Customer Lifetime
Value Analysis · Customer Loyalty · Customer Movement Dynamics · Customer
Profile Analysis · Customer Profitability · Involved Party Exposure · Lead
Analysis · Market Analysis

**Sample BSTs with reports (slide 38):**

| BST | Sample reports |
|---|---|
| Purchase Profiles | Category Sales by Demographics · Loyalty Points Issued by Store · Sales Value/Quantity by Products vs Customers · Product Group Avg Sales Quantity per Transaction · Product Group Avg Sales Value per Transaction · Product Penetration (geo / geo-demographic) |
| Customer Profiles | Customer Attribute report · Customer Status by Attribute · Cumulative % Sales by Decile · Sum of Purchase by Decile · Customer Base Dynamics · Loyal Purchasers Subsequent Behavior · Customer Details |
| Product Purchasing RFQ (Recency / Frequency / Quantity) | 6-Month Customer Age Group Segment RFQ · Repurchase Interval · Repurchase Propensity · Distribution of Customers by Number of Units · Distribution of Transactions by Number of Units |
| Campaign & Promotion Analysis | Sales Performance by Campaign Response · by Campaign Cell · Target Period Sales Proportion Index Sub-Class · Target Period Sales Value Index by Age Range · Target Period Sales Value Index by Product |
| Cross Purchase Behavior | Count of Cross Purchasers · Cross Purchasers Subsequent Behavior |
| Target Product Analysis | Sales Quantity Proportion · Avg Transaction Quantity · Avg Transaction Value · Sales Value Proportion |
| Customer Movement Dynamic | Customer Acquisition & Defection · Segment Migration Comparison |
| Market Basket Analysis (Clienteling) | Cross Merchandising (what's in a basket) · Demographic profile to market basket · Statistical reports · Association report (product) |

**Cross-references:** _(filled in by future sessions)_

### 2. Products & Services Management

**Purpose.** Understand the product side of the equation — what's in the
catalog, how each item is performing, what new items are landing, what's
being discontinued, and how the supplier base is supporting the assortment.

**BST inventory (slide 19):** Market Basket Analysis · Product Purchasing
RFQ Analysis · Purchase Profile Analysis · Target Product Analysis ·
Business Performance Analysis · Planning and Forecasting Analysis · Product
Analysis · Product Profitability

**Sample BSTs with reports (slide 39):**

| BST | Sample reports |
|---|---|
| Business Performance Analysis | New Item Introduction · Vendor Performance (sales by vendor) · Discontinue Analysis · Sales Quantity by Products · Vendor Compliance (billing, delivery) · Vendor Fulfillment · Vendor Rebate · Cannibalization Impact · New Item Launch Coverage · Sales Quantity Proportion by Products · Sales Value by Products · Sales Value Proportion by Products · by Sub-Department · Target Product Transactions (Avg Tx Qty/Value, Sales Qty/Value Proportion) · Vendor In-Stock Position |
| Product Analysis | Product Performance by Store/Geography · Product Category Performance · Detail Product Category Breakdown · Target Product to Customer · Product Category Breakdown · Product Equalization |

**Cross-references:** _(filled in by future sessions)_

### 3. Merchandising Management

**Purpose.** The day-to-day operational discipline of running the
assortment — what's in stock, what's on order, what's priced where, what
promotions are active, and how the physical space is performing.

**BST inventory (slide 19):** Assortment and Allocation Analysis ·
Inventory Analysis · Physical Merchandising / Space Management Analysis ·
Pricing Analysis · Promotion Analysis

**Sample BSTs with reports (slide 40):**

| BST | Sample reports |
|---|---|
| Inventory Analysis | On Order vs On Hand · Days of Supply · Lag Time Report · Out of Stock by Product · Total COGS on Hand by Location · Damages / Stressed (garments) / Aged Products · Safety Stock · Slow Moving Inventory · Transfer Report and Management |
| Assortment / Allocation Analysis | Traited vs Value · Base Profit Contribution · Product Sales by Store Format · Category Performance by Store · Product Affinity · Product to Customer Profiles |
| Promotion Analysis | Promotion Sales Performance · Overall Profit Contribution · Promotion Effect by Media (1, 2) · Promotional Response by Customer Segments · by Market Basket · Promotional Impact on Store Traffic · Promotional Category Impact · Promotion Fade |
| Physical Merchandising / Space Mgmt | Same Layout Comparisons · Demographic Response to Different Layouts · Revenue per sq Ft · Category Profitability to Physical Presence · Days of Supply of Product to Category · Optimization of Linear Footage to Total Store · Section Elasticity / Adjacency |
| Pricing Analysis | Set vs Actual Price Sold · Price Competitive Exception · Family Pricing (related products) · Competitive Marketbasket · Multi-Channel Price · Markdown Trend · Price Elasticity |

**Cross-references:** _(filled in by future sessions)_

### 4. Store Operations Management

**Purpose.** How the physical estate runs — labor, location performance,
loss, store-level optimization. The most Canary-relevant domain: Loss
Prevention is a first-class BST here.

**BST inventory (slide 19):** Activity Based Costing Analysis · Location
Exposure · Location Profitability · **Loss Prevention Analysis** · Non
Performing Loan Analysis · Organization Unit Profitability · Performance
Measurement · Staffing Analysis · Service Delivery Analysis · Store
Location Analysis · Store Optimization Analysis · Suspicious Activity
Analysis · Transaction Profitability Analysis · Vendor Performance Analysis

**Sample BSTs with reports (slide 41):**

| BST | Sample reports |
|---|---|
| **Loss Prevention** | Baseline Exception · Cashier Exceptions (over/under, voids) · Inventory Discrepancy · Employee Schedule Compliance Associated with Loss · Receiver Exception |
| Staffing | Employee Schedule Compliance · Cashier Performance Metrics · Cross Training · Sales Person Productivity · Skills vs Employees · Years of Service · Employee Details |
| Store Location Analysis | Performance by Store Format · Age of Stores · Store Geo-Demographic Profiles · Location Segmentation · Performance by Store Type · Store Detail |
| Store Optimization | Projected Inventory vs Sales Projections · Actual Inventory vs Projected Inventory · On Order Relationships vs On-Hand Inventory |

**Cross-references:** _(filled in by future sessions — Canary's chirp rules
slot here heavily)_

### 5. Multi-Channel Management

**Purpose.** The customer-facing channels other than physical store —
e-commerce, catalog, call center — and the cross-channel behavior that
ties them together. Solex (the e-commerce fixture) is the worked example
that lives in this domain.

**BST inventory (slide 19):** _(not separately enumerated on slide 19;
treated as a peer domain in sample slides)_

**Sample BSTs with reports (slide 42):**

| BST | Sample reports |
|---|---|
| eCommerce Analysis | Session Cycle Count by Period · Session Cycle Comparison by Period · Identified Shopper Segmentation by Segment by Period · Product Category Analysis by Period by Trait · Product Category Breakdown by Time Period · Product Category Customer Segmentation by Time Period · Clickstream Patterns with Sales Results · Method Used for Payment to Actual Sales |
| Catalog Analysis | Cross Catalog Purchase Profiles · Catalog Mix to Demographic Response · Product Placement to Purchase Propensity |
| Call Center Analysis | Operator Closure Rates · Script Success Rate to Demographic · Cold Call Conversions to Qualified · Failure Causes and Statistics |

**Cross-references:** _(filled in by future sessions — Solex commerce
mockup slots here)_

### 6. Corporate Finance Management

**Purpose.** The CFO-facing view of the retail business — capital,
credit, income, financial accounting. RBIS slide 19 lists this as a
peer domain but does not provide a sample-BST slide; the report
inventory below is what slide 19 surfaces directly.

**BST inventory (slide 19):** Capital Allocation Analysis · Credit Risk
Analysis · Financial Management Accounting · Income Analysis

**Sample BSTs with reports:** _(no slide 38–42 equivalent in the source
deck — gap intentionally preserved)_

**Cross-references:** _(filled in by future sessions)_

---

## What this MOC indexes (planned cross-references)

Every BST cell above will eventually carry a small set of cross-references
to artifacts elsewhere in the vault. The current cross-reference targets:

| Source | What it provides | Where it lives |
|---|---|---|
| Canonical retail integration interfaces (~76 specs, 5 active + 2 placeholder domains) | The integration surface — *which interfaces feed each BST*. Vendor-agnostic catalog at [[Brain/wiki/retail-integration-spine\|Retail Integration Spine]]. | `Brain/raw/inbox/Interface Design Documents/` (raw source) |
| Solex commerce mockup spec | A worked-out e-commerce fixture; populates Multi-Channel cells with concrete data and flows. Crosswalk at [[Brain/wiki/retail-spine-solex-crosswalk\|Solex Crosswalk]]. | [docs/superpowers/specs/2026-04-23-solex-commerce-mockup-design.md](../docs/superpowers/specs/2026-04-23-solex-commerce-mockup-design.md) |
| Secure wiki cards (NFR archetypes) | Operating-model and prior-art context per domain. Heaviest in Store Ops (LP, omnichannel, case mgmt) and Merchandising. Crosswalk at [[Brain/wiki/retail-spine-secure-crosswalk\|Secure Crosswalk]]. | `Brain/wiki/secure-*.md` |
| Heartbeat / Fireball 2002 | The OOS detection ancestor; populates Store Ops → Loss Prevention with prior-art design DNA. | [Brain/raw/inbox/Heartbeat/](../raw/inbox/Heartbeat/) (extraction pending per playbook) |
| Canary modules | The current implementation surface; populates Store Ops → Loss Prevention densely, Merchandising → Inventory partially, Customer Mgmt thinly. | `Canary/canary/` (later session) |

---

## Canary module crosswalks

The Differentiated-Five (T / R / N / A / Q) — the v1 modules that
distinguish Canary from a vendor-bundled BI surface — each get a
two-file pair: a vendor-neutral canonical article in
`Canary-Retail-Brain/modules/` and a Canary-specific wiki crosswalk
that maps the canonical spec to actual code (file paths, schema
locations, table inventories, MCP tool surfaces, open questions).

| Prefix | Module | Ring | Status | Ledger role | Canonical | Canary crosswalk |
|---|---|---|---|---|---|---|
| **T** | Transaction Pipeline | v1 | shipping | publisher (sale) | `Canary-Retail-Brain/modules/T-transaction-pipeline.md` | [[../wiki/canary-module-t-transactions\|canary-module-t-transactions]] |
| **R** | Customer | v1 | shipping (minimal) | n/a (people side) | `Canary-Retail-Brain/modules/C-customer.md` | [[../wiki/canary-module-c-customer\|canary-module-c-customer]] |
| **N** | Device | v1 | model shipping | n/a (thing side) | `Canary-Retail-Brain/modules/N-device.md` | [[../wiki/canary-module-n-device\|canary-module-n-device]] |
| **A** | Asset Management (Bubble) | v1 | design — impl pending | n/a (anomaly engine over N) | `Canary-Retail-Brain/modules/A-asset-management.md` | [[../wiki/canary-module-a-asset-management\|canary-module-a-asset-management]] |
| **Q** | Loss Prevention (Chirp+Fox) | v1 | shipping | reconciler (sale exceptions) | `Canary-Retail-Brain/modules/Q-loss-prevention.md` | [[../wiki/canary-module-q-loss-prevention\|canary-module-q-loss-prevention]] |
| **C** | Commercial | v2 | design complete | publisher (cost-update); OTB co-owner | `Canary-Retail-Brain/modules/M-merchandising.md` | [[../wiki/canary-module-m-merchandising\|canary-module-m-merchandising]] |
| **D** | Distribution | v2 | design complete | **primary publisher** (6 verbs) | `Canary-Retail-Brain/modules/D-distribution.md` | [[../wiki/canary-module-d-distribution\|canary-module-d-distribution]] |
| **F** | Finance | v2 | design complete | reconciler (3-way match) + publisher (GL) | `Canary-Retail-Brain/modules/F-finance.md` | [[../wiki/canary-module-f-finance\|canary-module-f-finance]] |
| **J** | Forecast & Order | v2 | design complete | subscriber (history) + publisher (orders) | `Canary-Retail-Brain/modules/O-orders.md` | [[../wiki/canary-module-o-orders\|canary-module-o-orders]] |
| **S** | Space, Range, Display | v3 | design complete | subscriber + **gatekeeper** (ordering gate) | `Canary-Retail-Brain/modules/S-space.md` | [[../wiki/canary-module-s-space\|canary-module-s-space]] |
| **P** | Pricing & Promotion | v3 | design complete | publisher (price/markdown events) | `Canary-Retail-Brain/modules/P-pricing-promotion.md` | [[../wiki/canary-module-p-pricing-promotion\|canary-module-p-pricing-promotion]] |
| **L** | Labor & Workforce | v3 | design complete | publisher (time entries) + subscriber | `Canary-Retail-Brain/modules/L-labor.md` | [[../wiki/canary-module-l-labor\|canary-module-l-labor]] |
| **W** | Work Execution | v3 | design complete | **reconciler + cross-domain** (capstone) | `Canary-Retail-Brain/modules/E-execution.md` | [[../wiki/canary-module-e-execution\|canary-module-e-execution]] |

**Spine walk complete.** All 13 modules have canonical CATz spec + Brain wiki crosswalk as of 2026-04-24.

## Substrate canonical layer (the spec the modules code against)

Five CATz platform articles define the substrate the spine sits on:

- `Canary-Retail-Brain/platform/stock-ledger.md` — perpetual-inventory movement ledger; verbs, invariants, publisher/subscriber/reconciler pattern. Backbone: [[../wiki/retek-rms-perpetual-inventory|Retek RMS Perpetual Inventory]].
- `Canary-Retail-Brain/platform/retail-accounting-method.md` — RIM vs Cost Method, Open To Buy as planning constraint
- `Canary-Retail-Brain/platform/satoshi-cost-accounting.md` — sub-cent unit cost on the ledger; the COGS-side foundation. Goose ([Linear GRO-117](https://linear.app/growdirect/issue/GRO-117) shipping) is the production proof.
- `Canary-Retail-Brain/platform/satoshi-precision-operating-model.md` — **the top-down unifier.** Extends satoshi precision from COGS to CAC + SG&A + IoT-tracked movement. Every cost decomposed to its originating event with audit trail. Re-reads the 13 modules as instruments of cost decomposition.
- `Canary-Retail-Brain/platform/perpetual-vs-period-boundary.md` — **the staged migration.** Phase 1 parallel observer (zero adoption friction); Phase 2 modular cutover at merchant pace; Phase 3 stock-ledger swap (the moat). Until the merchant swaps the stock ledger itself, every layer is independently cutoverable. Established by [[Canary-Retail-Brain/case-studies/canary-finance-architecture-options|v2.F ADR]].

Plus two CATz shell-fill articles closing the v0.6 broken links:

- `Canary-Retail-Brain/platform/arts-adoption.md` — POSLog/Customer/Device/Site standards alignment
- `Canary-Retail-Brain/platform/differentiated-five-add-on.md` — T+R+N+A+Q positioning brief

## Persona layer — the Virtual Store Manager

- `.claude/skills/canary-vsm.md` — composed agent skill that knows the entire 13-module spine via Owl runtime. v1 today (T/R/N/Q tools); v2 as C/D/F/J ship; v3 as S/P/L/W ship.
- `Canary-Retail-Brain/platform/module-manifest-schema.md` — machine-readable manifest format every module ships alongside its prose `.md`. First concrete example: `Canary-Retail-Brain/modules/T-transaction-pipeline.manifest.yaml`.

## Viewpoint synthesis

- [[../wiki/growdirect-viewpoint-virtual-store-manager|GrowDirect Viewpoint — VSM on a Perpetual Ledger]] — the integrated read tying capability spine + substrate + persona into the one-stop-shop SMB retail operating system pitch.

**Drift surfaced and cleared by this pass:**

- ✓ Chirp rule count corrected to **37** (was "29") across
  [[../wiki/canary-architecture|canary-architecture]],
  [[../wiki/canary-detection|canary-detection]],
  [[../wiki/canary-platform-overview|canary-platform-overview]],
  [[../wiki/canary-module-t-transactions|canary-module-t]],
  [[../wiki/canary-sales-strategy|canary-sales-strategy]], and
  [[Home|Brain Home]]
- ✓ Schema count corrected to **3** (`app` / `sales` / `metrics`) in
  [[../wiki/canary-data-model|canary-data-model]],
  [[../wiki/canary-platform-overview|canary-platform-overview]],
  [[Canary|Canary MOC]],
  [[../wiki/secure-architecture|secure-architecture]], and
  [[../wiki/canary-module-t-transactions|canary-module-t]] — Fox
  tables live in `app` via `AppBase` inheritance, despite the
  `models/fox/` Python module path
- ✓ A status reframed to "v1 (design — implementation pending)" in
  `Canary-Retail-Brain/platform/spine-13-prefix.md` — code shows
  foundation infrastructure exists (baseline_calculator, metrics
  risk schema, N's registry), the bubble layer itself is unbuilt

---

## Open work

This MOC is v0. The structure is complete; the cells are mostly empty.
The work of filling them is incremental, one source at a time:

- **v0.1** — _(this file)_ Structure + RBIS-derived BST inventory + sample
  reports. ✓
- **v0.2** — Canonical retail integration crosswalk. ~76 interfaces across
  5 active prefix domains (Commercial / Distribution / Finance / Forecasting
  & Ordering / Space-Range-Display) mapped to the BSTs they feed, plus
  reverse crosswalk per BST. Vendor-agnostic framing — system names use
  canonical roles. See [[Brain/wiki/retail-integration-spine|Retail
  Integration Spine]]. ✓
- **v0.3** — Solex crosswalk. Single-channel SMB e-commerce mockup mapped
  to Multi-Channel BSTs (full coverage), with adjacent reach into Customer,
  Products & Services, Merchandising, and Store Ops cells. See
  [[Brain/wiki/retail-spine-solex-crosswalk|Solex Crosswalk]]. ✓
- **v0.4** — Secure wiki crosswalk. 18 prior-art cards mapped to the BSTs
  they inform. Densest at Store Ops (12 cards on Loss Prevention),
  Merchandising (7 cards), Multi-Channel (3 cards). See
  [[Brain/wiki/retail-spine-secure-crosswalk|Secure Crosswalk]]. ✓
- **v0.5** — Canonical / shipping version. Vendor-neutral, client-neutral,
  product-neutral fusion of: capability layer (RBIS-derived) + operating-
  model layer (TOM-derived: People · Property · Retail Operations) +
  system-role glossary + integration-pattern catalog + SMB substrate
  collapse principles + how-to-use guidance. Lives in
  [`Canary/docs/retail-capability-model.md`](../../Canary/docs/retail-capability-model.md)
  — ships in the Canary repo. ✓
- **v0.6** — Heartbeat / Fireball (2002) essential-design extraction.
  Five-file research folder at [`docs/research/heartbeat-fireball-2002/`](../../docs/research/heartbeat-fireball-2002/INDEX.md)
  (THE_PROBLEM · THE_ARCHITECTURE · THE_ALGORITHM · THE_NOTIFICATION_SYSTEM
  · CANARY_LINEAGE_MAP). Brain wiki card at
  [[Brain/wiki/secure-heartbeat-fireball-2002|Heartbeat / Fireball
  (2002) — Essential Design]] (archetype-scrubbed). Canonical Loss
  Prevention enrichment in [`Canary/docs/retail-capability-model.md`](../../Canary/docs/retail-capability-model.md)
  §4.1 Detection-and-notification pattern (fully vanilla — pattern
  named, no historical narrative or attribution). ✓
- **v0.6** — Canary module crosswalks for the Differentiated-Five
  (T / R / N / A / Q). Each module gets a canonical vendor-neutral
  brain article plus a Canary-specific wiki crosswalk pinned to actual
  code (file paths, schema locations, column inventories, MCP tool
  surfaces). See [[#canary-module-crosswalks|Canary module crosswalks]]
  above. Surfaced three documentation drifts (rule count, schema
  count, A status) for cleanup. ✓
- **v0.7** — BST-cell schema-mapping pass. Each BST cell gets a
  "current Canary table coverage" marker tied to the modules above.
  New operational schemas surface here as the v2 C / D / F / J
  modules get their first code (likely candidates: `customer`,
  `merch`, `vendor`, `channel` schemas to extend the current 3).
  v2 module pairs (C / D / F / J) get the same two-file treatment.
- **v0.8+** — Microservice slot per capability. Each cell carries a
  "service this would live in" marker. The microservice-name index
  is already seeded per module (each module article has a
  service-name-markers table); v0.8 closes the loop by reverse-
  mapping from BST cells back to the service slots. Maps onto the
  canonical model via system-role names from
  `Canary/docs/retail-capability-model.md` §8.

## Cross-cutting wiki cards

- [[Brain/wiki/retail-foundation-data|Retail Foundation Data]] — master-data layer that every spine domain reads from
- [[Brain/wiki/retail-security-controls|Retail Security Controls]] — access-control posture across the spine

## Related

- [[Brain/projects/Secure|Secure MOC]] — the retail prior-art project this
  spine grew out of
- [[Brain/projects/Canary|Canary MOC]] — the current shipping product whose
  capability surface gets indexed against this spine
- [[Brain/wiki/canary-data-model|Canary Data Model]] — current 3-schema
  layout (`app` / `sales` / `metrics`) that the schema-mapping pass
  will extend (the wiki article still says 4; it predates the
  code-verified count and is queued for cleanup)
- [[Brain/raw/inbox/retail-business-intelligence-solution-v7|RBIS V7
  full transcription]] — the source artifact

## Sources

- `Brain/raw/inbox/GAP/GAP BI/RBIS background/Retail Business Intelligence
  Solution V7.ppt` (Oct 2005) — primary spine source
- `Brain/raw/inbox/GAP/GAP BI/RBIS background/RBIS Update.PDF` (Sep 2005) —
  companion update
- `Brain/raw/inbox/GAP/ODS Detail Slides v3.ppt` — ODS architectural pattern
  (the substrate the spine collapses onto for SMB)
- `Brain/raw/inbox/Interface Design Documents/` — 378 Tesco interface specs,
  the integration-surface source for v0.2
