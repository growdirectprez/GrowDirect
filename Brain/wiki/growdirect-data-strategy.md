---
date: 2026-04-22
type: wiki
tags: [growdirect, data-strategy, north-star, crdm]
sources:
  - docs/_archive/ip-vault/strategy/Canary_Data_Strategy_NorthStar_v1.0.md
last-compiled: 2026-04-22
needs-review: 2026-05-06
---

**Wiki:** [[Brain/Home|Home]]

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

# Canary Data Strategy — North Star

**Version:** 1.1
**Date:** February 26, 2026
**Author:** ALX (Chief of Staff), per Jeffe directive
**Classification:** CONFIDENTIAL — Internal architecture document
**Status:** ACTIVE — This is not a proposal. This is how we treat data.

---

## The Rule

> The moment one merchant connects, the data is production. Every row is hashed. Every event is immutable. There is no "we'll add integrity later." It is built in from the first INSERT.

This is not aspirational. The infrastructure for this already exists:
- 22 INSERT-only triggers across 10 tables (Tom B-001, Jeremy Phase 2)
- Cryptographic hash chains on evidence tables (compute-on-INSERT via pgcrypto)
- `verify_entry_hash()` and `verify_hash_chain()` functions operational
- UPDATE and DELETE blocked on all financial tables with CRDM v1.0 error messages

What follows is the strategy for extending this from database-level integrity to externally anchored, legally defensible, production-grade immutable truth.

---

## Three Layers of Truth

### Layer 1: Database Integrity (DONE)

**What it is:** INSERT-only tables with cryptographic hash chains in PostgreSQL.

**What it proves:** Data has not been modified since it was written to the database. Each row's hash includes the previous row's hash, creating a chain. Break any link and the chain fails verification.

**Limitation:** Canary controls the database. A sufficiently motivated actor with database access could theoretically rebuild the chain from scratch. Layer 1 proves integrity *within* the system. It does not prove integrity *to the outside world.*

**Status:** ✅ OPERATIONAL. 22 triggers. 10 tables. Verified on PostgreSQL 17. Hash chain verification returns `is_valid=True`.

### Layer 2: Per-Merchant Partition Isolation (ARCHITECTURE DECISION — Sprint 6)

**What it is:** Each merchant's data lives in its own PostgreSQL partition (PARTITION BY LIST on `merchant_id`). Physically separate storage. Independently deployable migrations. Independently destroyable on merchant departure.

**What it proves:** Merchant data never co-mingles at the storage level. A legal request for Merchant A's data cannot accidentally surface Merchant B's data. Deletion is partition detach + drop — complete and verifiable.

**Design principles:**
- CI/CD pipeline treats each merchant schema as a deployable unit
- Migrations roll through per partition — can patch one without touching others
- New merchant onboarding spins up a fresh partition from the template schema
- Partition-level backup and restore — merchant data is portable
- Row-level security remains as defense-in-depth inside each partition
- Hash chains are self-contained per partition — no cross-merchant hash dependencies

**Repartitioning:** PostgreSQL supports converting an unpartitioned table to partitioned. The plan: start with the current unpartitioned schema for Phase 1 (GrowDirect Lab), implement partitioning before Phase 2 (first real merchant), and design migrations so repartitioning is a one-time operation with zero data loss.

**Compliance value:** "Your data lives in its own partition. When you leave, we detach and destroy it. There is nothing left." This is the answer Syd gives when a merchant asks about data deletion rights under CCPA.

**Status:** ⏳ B-035 in TRIAGE. Tom (architecture) + Syd (legal opinion) routed.

### Layer 3: Lightning Anchor — Immutable External Truth (THE GOAL)

**What it is:** Periodic anchoring of hash chain state to the Bitcoin Lightning Network. The head hash of each merchant's evidence chain is embedded in a Lightning transaction, pinning the chain state to a public, decentralized, immutable ledger that Canary does not control.

**What it proves:** The state of a merchant's data at a specific point in time is externally verifiable. Not "Canary says this is what the data looked like." Instead: "Here is a Lightning transaction from Tuesday at 3:14 PM containing hash `02e1ac1a29b80e2a...`. Here is the merchant's hash chain. The chain head matches the anchor. The data has not been modified since anchoring."

Nobody can forge this. Not Canary. Not the merchant. Not an attacker. Not a court order. The Lightning Network is the witness.

**How it works (conceptual — Tom + Jeremy to architect):**

```
Merchant's hash chain in PostgreSQL:
  row_1 → hash_1
  row_2 → hash_2 (includes hash_1)
  row_3 → hash_3 (includes hash_2)
  ...
  row_N → hash_N (includes hash_N-1)  ← chain head

Anchor event (periodic — hourly, daily, or on-demand):
  1. Read chain head hash for merchant partition
  2. Create Lightning transaction with OP_RETURN or equivalent carrying the hash
  3. Transaction confirms on Lightning (near-instant, sub-cent cost)
  4. Store anchor receipt: { merchant_id, chain_head_hash, lightning_tx_id, timestamp }
  5. Anchor receipt itself is appended to the evidence chain (self-referential integrity)

Verification (at any future point):
  1. Walk the merchant's hash chain — verify every link
  2. Find the most recent anchor receipt
  3. Look up the Lightning transaction
  4. Compare chain head hash at time of anchor to the hash in the Lightning transaction
  5. If they match: data integrity proven from that anchor point forward
  6. If they don't match: chain has been tampered with since the anchor
```

**Cost model:** Lightning transactions cost fractions of a cent. At one anchor per merchant per day, 10,000 merchants = 10,000 transactions/day ≈ $1-5/day total. The cost is negligible. The value is incalculable.

**Legal weight:** A Fox evidence chain anchored to Lightning transforms the output from "Canary's records say X" to "a cryptographically verifiable chain, externally anchored to a public ledger, proves X." This has implications for:
- Insurance claims (proof of loss, proof of process followed)
- Employee disputes (evidence of investigation, tamper-proof timeline)
- Legal proceedings (chain of custody for digital evidence)
- Regulatory compliance (audit trail with external verification)
- Merchant trust (we can prove we haven't altered your data)

**Status:** 🔴 NOT YET BUILT. Layer 1 (database integrity) is the foundation. Layer 2 (partition isolation) is the Sprint 6 architecture decision. Layer 3 (Lightning anchor) is the goal — Sprint 7+ or whenever Jeremy and Tom are ready to architect the anchor service.

---

## Data Retention — The 14-Month Floor

### Why 14 Months

The NRF 4-5-4 retail calendar divides the year into 4-week and 5-week periods for comparable week-over-week analysis. A clean year-over-year comparison requires 53 weeks of historical data. 13 months is close but misses the holiday shift and leap week edge cases. 14 months is the safe floor.

**Without 14 months:** "Your shrink was $2,400 last month." (So what?)
**With 14 months:** "Your shrink was $2,400 last month — up 31% from the same period last year. Here's where it's coming from." (Now we're talking.)

### Retention Tiers

| Tier | Retention | What's Stored |
|---|---|---|
| **Transaction detail** | 14 months minimum | Full row-level data in `canary_sales` partition. Every payment, refund, line item, tender, cash drawer event, timecard. |
| **Aggregated metrics** | 36 months | Daily/weekly/monthly roll-ups in `canary_metrics`. Shrink rates, variance trends, category performance, labor efficiency. No PII. |
| **Anchor receipts** | Indefinite | Lightning anchor transaction IDs and chain head hashes. Tiny footprint. Proves historical integrity even after detail is aged out. |
| **Evidence chains** | Indefinite (or per legal hold) | Fox evidence records. These are legal artifacts — retention follows Syd's guidance on document preservation requirements. |

### The 4-5-4 Calendar in Canary

Canary metrics align to the NRF 4-5-4 retail calendar for all period-over-period comparisons:

- **Week:** Sunday–Saturday (NRF standard)
- **Month:** 4 weeks, 5 weeks, 4 weeks per quarter (445 pattern with the 5 in the middle)
- **Quarter:** 13 weeks
- **Year:** 52 weeks (53 in leap years)

Scorecards, trend analysis, and benchmarking all use 4-5-4 periods, not calendar months. This is what makes Canary's metrics comparable to enterprise retail reporting and unlike anything a small merchant has ever seen.

### Aging Strategy

When transaction detail ages past the 14-month window:
1. Aggregated metrics already exist in `canary_metrics` (computed daily by Airflow DAG)
2. Detail rows can be archived or purged from the merchant's partition
3. Anchor receipts remain — proving the integrity of the data that was there
4. The merchant's metric trends are uninterrupted — they just can't drill into individual transactions from 15 months ago

This keeps storage costs predictable while preserving the analytical value indefinitely.

---

## The Three-Layer Data Model

This is the CRDM, restated as a data strategy:

### Layer A: Merchant Schema (Private — Per-Partition)

**Database:** `canary_sales` (partitioned by merchant_id)

The merchant's own data. Full transaction detail. Append-only. Immutable. Hash-chained. Lightning-anchored.

- Transactions, refunds, line items, tenders
- Cash drawer shifts and events
- Employee timecards
- Gift card activity
- Inventory adjustments
- Evidence chains (Fox)

**Access:** Merchant-only. Row-level security within partition. Partition-level isolation between merchants. Merchant can request full data export or deletion at any time.

**Retention:** 14 months detail, indefinite evidence chains.

### Layer B: Detection & Operations (Private — Per-Merchant in `canary_app`)

**Database:** `canary_app`

Merchant configuration, detection rules, alert history, wizard state.

- Merchant profile, locations, employees, products
- Detection rule config (which Chirps are on, custom thresholds)
- Alert records and status history (new → acknowledged → resolved)
- Wizard completion records
- OAuth tokens (encrypted at rest)
- Webhook subscription records

**Access:** Merchant + Canary operations. Never shared cross-merchant.

### Layer C: Aggregated Intelligence (Anonymized — Cross-Merchant)

**Database:** `canary_metrics`

Anonymized, aggregated metrics computed from Layer A. No PII crosses this boundary. No card fingerprints. No employee names. No merchant-identifiable detail.

- Shrink rates by vertical (coffee shops, retail, restaurants)
- Variance trends by geography and season
- Detection pattern libraries (which rules fire most, false positive rates)
- Category performance benchmarks
- Labor efficiency benchmarks
- Consumer spend trends (anonymized, statistical)

**Access:** Powers Canary's benchmarking features ("your shrink rate vs. similar businesses"), detection rule auto-tuning, and — eventually — the industry intelligence layer that makes the aggregated dataset valuable beyond any single merchant.

**Retention:** 36 months aggregated. Indefinite for statistical summaries.

---

## What This Means for the Build

### For Jeremy:
- Every table in `canary_sales` must have INSERT-only triggers (already done for 10 tables — extend to all)
- Every table must support partitioning by `merchant_id` (Tom architects, Jeremy implements)
- Hash chain computation must be per-partition (no cross-merchant hash dependencies)
- Aggregation DAGs (Airflow) must compute daily roll-ups from detail to metrics
- Lightning anchor service is a future deliverable — design the interface now, implement when ready
- 14-month retention policy enforced by an aging DAG (archive/purge detail beyond window)

### For Tom:
- Validate partition design works with existing immutability triggers
- Confirm hash chain is self-contained per partition
- Design the `canary_metrics` aggregation schema (dimensional model on top of the ODS)
- Architect the Lightning anchor service interface (even if implementation is Sprint 7+)
- Assess repartitioning plan — from current unpartitioned to partition-per-merchant

### For Syd:
- Legal opinion on per-partition data isolation vs. FCRA/CRA requirements
- Data retention requirements for evidence chains (legal hold scenarios)
- DPA language updates to reflect partition isolation and deletion guarantee
- Lightning anchoring — does external hash anchoring create any new regulatory exposure?
- CCPA "right to delete" — confirm partition detach + drop satisfies the requirement

### For PhD:
- Validate that aggregated metrics in Layer C cannot be reverse-engineered to identify individual merchants
- Review the anonymization boundary — what can and cannot cross from Layer A to Layer C
- Research precedent for Lightning-anchored evidence chains in legal proceedings

---

## Layer 4: The Retail App Platform

### The Vision

The CRDM isn't just Canary's data layer. It's the data layer for every app a small merchant will ever need.

Today, every developer who wants to build something useful for Square merchants has to solve the same problem from scratch: connect to Square's API, parse the webhook payloads, normalize the data, store it, and make it queryable. That's months of plumbing work before they write a single line of business logic. Most give up.

The CRDM solves that problem once. A clean, normalized, real-time retail data warehouse — transactions, line items, tenders, cash drawers, timecards, gift cards, inventory — already flowing, already stored, already queryable. Any developer can build on top of it.

### How It Works

The merchant controls everything. Same UX pattern as the Chirp Config page — a scrollable list of apps, each with a toggle.

```
Merchant App Store
├── Loss Prevention (Canary Chirps)         [ON]
├── Demand Forecasting                      [OFF]
├── Labor Optimization                      [OFF]
├── Menu Engineering / Merchandising        [OFF]
├── Inventory Intelligence                  [OFF]
├── Cash Flow Forecasting                   [OFF]
├── Vendor Performance Analysis             [OFF]
└── ... (third-party apps)                  [OFF]
```

Each app reads from the same CRDM. The merchant's partition. Their data. Their permission. No app sees another merchant's data. No app sees data from apps the merchant hasn't enabled.

### First-Party Apps (GrowDirect builds)

These are the apps Jeffe knows how to build because he's built them at enterprise scale for 30 years:

| App | What It Does | CRDM Tables Used | Retail Math |
|---|---|---|---|
| **Canary LP** | Loss prevention — Chirps, wizards, evidence chains | All of `canary_sales` + alerts | Shrink rate, variance analysis |
| **Demand Forecasting** | Predict next week's sales by item, day, daypart | transactions, line_items | Weeks of supply, sell-through rate, trend decomposition |
| **Labor Optimizer** | Match staffing to demand curves | timecards, transactions (hourly) | Sales per labor hour, labor cost %, coverage ratio |
| **Menu Engineer** | Classify items by margin × volume (stars, puzzles, dogs, plowhorses) | line_items, product catalog | GMROI, contribution margin, menu mix %, BCG matrix |
| **OTB Planner** | Open-to-buy for retail inventory | transactions, inventory_adjustments | OTB = planned sales + planned markdowns + planned EOM − BOM |
| **Cash Flow** | 13-week rolling cash flow projection | transactions (daily revenue), tenders (payment mix) | DSO, payment cycle, cash conversion |
| **Vendor Scorecard** | Rate suppliers on fill rate, lead time, quality | inventory_adjustments, purchase orders (future) | Fill rate %, on-time %, cost variance |

Every one of these exists as an enterprise product costing $50K–$500K/year. None of them exist for a merchant doing $800K through Square. The retail math is the same. The data is the same. The delivery is different — Chirps and scorecards instead of BI dashboards and analyst reports.

### Third-Party Developer Platform (Future)

Once the first-party apps prove the model, open the CRDM API to third-party developers:

- Developer registers an app on the GrowDirect platform
- App declares which CRDM tables/fields it needs access to
- Merchant authorizes the app (same OAuth-like consent pattern)
- App reads from the merchant's partition via API
- GrowDirect takes a revenue share on third-party app subscriptions

This is the retail app store. Not built top-down by Oracle or SAP. Built bottom-up from the data layer that the merchant already populated when they connected their Square account.

### Why This Wins

The big enterprise vendors have tried to build the retail app store for decades. They fail because:

1. **They build top-down.** Start with enterprise, push down to SMB. But SMB merchants won't adopt enterprise tools — too complex, too expensive, too much implementation.
2. **They don't own the data layer.** Each app brings its own data silo. Nothing integrates. The merchant ends up with 5 apps that don't talk to each other.
3. **They don't have distribution.** Enterprise sales cycles are 6-18 months. Square Marketplace distribution is instant — tap install, OAuth, done.

GrowDirect builds bottom-up:
1. **Start with SMB.** Purpose-built for the merchant with 200 SKUs and one register. If a coffee shop owner can't use it in 5 minutes, it doesn't ship.
2. **Own the data layer.** The CRDM is the single source of truth. Every app reads from the same normalized, immutable, hash-chained data. No silos.
3. **Distribution is built in.** Square Marketplace puts you in front of 4.5 million merchants. Onboarding is OAuth. Billing is subscription. No sales team required.

### The Stickiness Flywheel

```
Merchant connects Square account
    → CRDM populates with their data
        → Loss prevention app fires useful Chirps
            → Merchant trusts the data
                → Merchant enables forecasting app
                    → More value from same data
                        → Merchant enables labor app
                            → Switching cost increases with every app enabled
                                → Merchant is never leaving
```

Each app the merchant turns on makes the platform stickier. Not because of lock-in tricks — because of genuine value accumulation. Their 14 months of trended data, their evidence chains, their configured thresholds, their historical metrics — that's *their* asset, built on *our* platform. Moving to a competitor means starting from zero.

### Jeffe's Playbook

The retail math library — OTB, BTC-STP, GMROI, sell-through, markdown optimization, menu engineering, labor modeling — this is 30 years of domain expertise that lives in Jeffe's head and in spreadsheets at enterprise HQs. Packaging it as apps on the CRDM is the entire play:

- **The knowledge exists.** Jeffe knows how to build every one of these apps because he's built them at scale.
- **The data exists.** Square captures everything needed — transactions, line items, tenders, timecards, inventory.
- **The delivery model exists.** Chirps and scorecards on a phone. Not BI dashboards. Not analyst reports.
- **The distribution exists.** Square Marketplace. 4.5 million merchants. Tap to install.

The only thing that didn't exist was the data layer in the middle. That's the CRDM. That's what we're building right now.

---

## The Standardization Paradox — Why Every Other Vendor Failed and How We Solve It

### The Problem They Never Solved

Every enterprise retail vendor — SAP, Oracle, JDA, Blue Yonder — attempted to build the universal retail data model. Every one of them failed to achieve genuine standardization at scale. The reason is always the same: **they standardized on the schema and forced merchants to adapt their thinking to the tool.**

The result: every implementation became a custom project. Every "standard" became a special case. Every rollout required a systems integrator, a 12-month timeline, and a $500K budget. The standard never held because retail merchants do not think about their business the same way — and no amount of configuration complexity can paper over that fundamental truth.

This is not a technology failure. It is a design philosophy failure.

### The Insight

> **All retail is the same. It is how merchants want to spin their data that makes them unique — and makes standardization hard. If we start correctly, we can do both.**

The canonical data model is identical for every merchant on the platform. The same transactions, the same cash drawer events, the same timecards, the same refunds, the same line items — captured in the same CRDM schema, hashed the same way, partitioned the same way, immutable the same way.

What is not identical is the **analytical lens** through which each merchant sees that data.

- A coffee shop owner thinks in **dayparts**. The morning rush is a different business than the afternoon slump. Hourly partitions, 13 weeks of history, labor matched to transaction velocity by the hour.
- A fashion buyer thinks in **sell weeks**. Week 1 of a new style tells you everything about whether it will sell through or mark down. Weekly partitions on the NRF 4-5-4 calendar, 56 weeks of history for clean year-over-year comparison.
- A grocery manager thinks in **days-of-supply**. How many days until I run out? Daily partitions, 26 weeks of history, replenishment triggers based on velocity.
- A multi-location operator thinks in **location cohorts**. How does my Torrance store compare to my Manhattan Beach store in the same daypart? Same grain as their primary business type, cross-location materialized views.

Same underlying data. Completely different analytical reality. Both are correct.

### The Architecture That Solves It

**Standardization happens at the schema layer. Personalization happens at the lens layer. The merchant never sees either one.**

```
CRDM Schema (identical for every merchant)
    ↓
Partition Layer (merchant_id × temporal grain)
    ↓ grain configured at onboarding, invisible to merchant
dbt Materialized Views (pre-computed at the merchant's natural grain)
    ↓
Superset Analytical Layer (merchant sees their lens, not the schema)
    ↓
Canary App (Today's View, scorecards, Chirps — zero data infrastructure visible)
```

The merchant does not configure a data warehouse. They connect their Square account and select a business type (or it is inferred from their Square category). The partition grain, retention window, materialized view schedule, and default analytical periods are all set automatically from that single input.

**What the merchant experiences:** their data, in the time units that match how they run their business, with comparisons against the periods that are meaningful to them — from their first day on the platform.

**What they never experience:** schema design, partition configuration, SQL, materialized view refresh schedules, or any other piece of the infrastructure underneath.

### Why We Can Do This When SAP Cannot

The big vendors failed because they came in at the top — enterprise contracts, big bang implementations, armies of consultants, and an implicit demand that merchants change how they think to match the tool.

We enter at the bottom through Square OAuth. Thirty seconds of authorization. The merchant never touches infrastructure. The business type they already declared to Square tells us everything we need to configure their analytical lens. By the time they see Today's View, the partition grain, the materialized views, and the Superset dataset are already configured correctly for how they think.

**The standardization is in the schema. The competitive moat is in the lens.**

No enterprise vendor can replicate this from the top down. The complexity of adapting their universal schema to merchant-specific analytical lenses requires exactly the custom implementation work they have always charged $500K to perform. We do it automatically at onboarding for every merchant on the platform, at the same marginal cost regardless of scale.

### Design Principles (Binding on All Architecture Decisions)

These principles govern every data model, partition design, materialized view, and API contract decision made on this project:

1. **The CRDM schema is canonical and fixed.** No merchant-specific schema variations. No custom tables per merchant. The schema is the standard. Period.

2. **The analytical lens is configurable at onboarding and fixed thereafter.** Partition grain (hour/day/week), retention window, and default comparison periods are set once from business type. Changing them is a migration event, not a config toggle.

3. **The merchant never touches infrastructure.** Business type → lens configuration is automatic. No merchant ever selects a partition grain, defines a materialized view, or writes a query.

4. **The raw partition layer is write infrastructure, not a query surface.** Application queries hit materialized views via Superset. Raw partitions are touched only by Airflow/dbt DAGs and Fox evidence chain verification.

5. **Superset is the analytical rendering layer.** Not custom charting code. Not custom query logic. Superset configuration defines what each role sees, what time bounds apply, and what datasets are accessible. The Canary app embeds Superset output.

6. **dbt defines the materialized view tier.** Not hand-written SQL. Not custom Airflow tasks. dbt models are the source of truth for every aggregation from Layer A to Layer C+. Versioned. Tested. Documented.

7. **Layer C+ requires Syd's gate.** No merchant data enters the PhD analytical sandbox without legal-approved consent. The `benchmark_consent` whitelist is a legal artifact, not a technical toggle.

8. **The lens is the moat.** The schema is replicable. The lens configuration system — auto-provisioned at onboarding, invisible to the merchant, correct from day one — is not. This is where we win.

---

## Service Level Framework — Transaction to Dashboard

### The Performance Contract

This is not a contractual SLA document. It is the architectural performance narrative that informs product tiering, contract language, and investor positioning. It demonstrates that GrowDirect has thought through the full latency chain — from Square POS to merchant dashboard — at the design level, before a single enterprise contract is signed.

> **The principle:** Chirps are always real-time. Dashboards are near-real-time by tier. These are two intentionally separate data paths with different latency profiles — designed that way from the first merchant.

### The Latency Chain

Every transaction that flows through Canary traverses this chain:

```
Square POS event created
    → Square webhook delivery          [Square SLA: ~60 seconds]
    → Canary HMAC verification         [<100ms — we own this]
    → Idempotency check + parse        [<100ms — we own this]
    → Store to canary_sales partition  [<500ms — we own this]
    → Chirp rule evaluation            [<500ms — we own this]
    → Alert write → Today's View       [<1 second end-to-end from ingest]
    → dbt materialized view refresh    [tier-dependent — see below]
    → Superset cache refresh           [seconds — configurable TTL]
    → Merchant opens dashboard         [render: negligible]
```

**What we control:** everything from HMAC verification through alert write. Sub-second. Consistent. Regardless of tier.

**What we don't control:** Square's webhook delivery latency (~60 seconds typical, no contractual guarantee from Square). We disclose this clearly — our SLA clock starts at webhook receipt, not at POS event creation.

**Where tier-dependent latency lives:** the dbt materialized view refresh. This is the only material variable in the chain for dashboard visibility. Chirps fire in real time at every tier.

### Product Menu — Performance Tiers

The SLA is in the contract. The tier is on the menu. Every merchant selects a plan; the plan defines their performance contract; the architecture delivers it automatically.

| Tier | Chirp Latency | Dashboard Refresh | Temporal Grain | Target Merchant |
|---|---|---|---|---|
| **Starter** | Real-time (< 2 min from webhook) | Nightly (up to 24h) | Day or Week | Low-volume SMB, seasonal retail, first 30 days |
| **Growth** | Real-time (< 2 min from webhook) | Hourly (up to 60 min) | Day | General SMB retail, steady-state operations |
| **Pro** | Real-time (< 2 min from webhook) | 15-minute micro-batch | Hour or Day | High-volume QSR, coffee, multi-location |
| **Enterprise** | Real-time (< 2 min from webhook) | Near-real-time + contractual SLA | Hour | Multi-location operators, franchise groups, investors |

**The Chirp promise never degrades.** A Starter merchant's loss prevention alerts fire within 2 minutes of Square webhook delivery — the same as Enterprise. What the tier buys is how fast the aggregated analytical picture catches up.

### Grain-to-Tier Mapping

The merchant's temporal grain (set at onboarding from business type) creates a natural commercial gate:

| Temporal Grain | Minimum Tier | Rationale |
|---|---|---|
| **Hour** | Pro | Hourly grain with nightly refresh is incoherent — you'd have 24 sub-partitions that never appear in the dashboard until morning. Hourly grain requires micro-batch refresh. |
| **Day** | Growth | Daily grain with nightly refresh loses only the current day's detail until midnight. Acceptable for Starter; Growth is the right default. |
| **Week** | Starter | Weekly grain with nightly refresh loses at most one day of the current week. Starter is sufficient. |

Onboarding flow consequence: "You told us you're a high-volume coffee shop. That means hourly grain — which means Pro tier minimum." The architecture enforces the commercial model automatically. No upsell conversation required.

### Enterprise SLA Language (Syd Drafts)

For enterprise contracts, the performance commitment is named and contractual. Draft language for Syd's review:

> *Dashboard latency shall not exceed fifteen (15) minutes, measured from confirmed webhook receipt by GrowDirect systems to availability of updated metrics in the merchant dashboard, during Business Hours (6:00 AM – 11:00 PM local merchant time), excluding (a) Square's webhook delivery latency, (b) scheduled maintenance windows with 24-hour advance notice, and (c) force majeure events. GrowDirect will provide documented remediation within four (4) business hours of any SLA breach.*

Syd reviews and finalizes. This is the floor — not the ceiling.

### Investor and Buyer Positioning

This framework exists not because merchants will read it but because investors and enterprise buyers will ask about it. The answer is:

> "We know exactly where the latency lives. Square delivers the webhook — that's their 60 seconds, disclosed. We ingest, parse, store, and fire a Chirp in under 2 minutes from receipt at every tier. The dashboard refresh cadence is a commercial variable — it's on the pricing page, it's in the contract, and the architecture delivers it through dbt micro-batch scheduling and Superset cache TTL. We designed the performance contract before we designed the DDL."

That is what a serious data platform company says. It is also true.

### What Tom and Jeremy Must Deliver Against This Framework

- **Tom:** dbt refresh schedule must be configurable per merchant tier. The Airflow DAG that triggers dbt runs must be parameterized by `refresh_cadence` from `merchant_settings`. Nightly, hourly, and 15-minute cadences must all be supported from day one — even if only Starter merchants exist at launch.
- **Jeremy:** Superset cache TTL must be configurable per dataset and aligned to the merchant's tier refresh cadence. A Pro merchant's Superset dataset should never serve a cache older than 15 minutes.
- **Syd:** Review and finalize enterprise SLA language before any enterprise conversation.
- **Eva:** Tier names and feature matrix go on the pricing page. This is Sprint 6 scope — not Sprint 5.

---

## The Timestamp Layer — Bitcoin as Evidentiary Infrastructure

### The Insight

> *We are not the evidence. We are the timestamp. The merchant's data proves itself.*

Canary does not testify. Canary does not produce records under subpoena. Canary does not need to be trusted. The Bitcoin network is the witness — and it has been running continuously, publicly, verifiably since January 3, 2009. No one questions its integrity. No one can tamper with block 892,847.

A coffee shop owner with one register and three employees now has the same evidentiary infrastructure as a federal investigation. Not because Canary is powerful. Because Bitcoin is. Canary helped them plug into it.

### What This Is Not

This is not a Layer 2 solution. It is not a sidechain. It is not a token. It is not a Lightning channel. Every layer added beyond L1 introduces a trust assumption — a counterparty, a sequencer, a validator, a bridge — that an attorney can question in court.

A Bitcoin L1 inscription has none of that. It is in the block. The block is in the chain. The chain has 800,000+ blocks of proof-of-work behind it. The only question is whether the Merkle proof validates — and that is pure mathematics. No counterparty to subpoena. No sequencer to question. No custody chain to audit. The inscription exists.

This is Bitcoin used for exactly what Satoshi designed it for: **immutable timestamped proof of existence.** The simplest, most legally defensible use of the protocol.

### The Architecture

Every raw webhook event received from Square is hashed on INSERT (pgcrypto, compute-on-INSERT trigger). Periodically — hourly for Enterprise, daily for Pro, weekly for Growth — the accumulated event hashes for each merchant are assembled into a Merkle tree. The 32-byte Merkle root is inscribed on Bitcoin L1 via Ordinals.

```
Raw events arrive from Square
    → hash each payload on INSERT (pgcrypto)
        → accumulate hashes per merchant per anchor period
            → build Merkle tree across the period's events
                → inscribe 32-byte Merkle root on Bitcoin L1
                    → store: inscription_id, block_height,
                              period_start, period_end,
                              merchant_id, merkle_root
                        → anchor_receipt appended to hash chain
                            (self-referential integrity)
```

**The Merkle tree is the key design decision.** Individual events are not inscribed — only the root that commits to all of them. A single event's inclusion in the root is provable with a Merkle proof: O(log n) hashes, computed locally, verified against the on-chain root. Compact on-chain. Complete off-chain. Any individual event verifiable without trusting Canary.

**Cost:** A Merkle root is 32 bytes. At current Bitcoin fee rates, inscribing 32 bytes costs fractions of a cent during normal mempool conditions. Even at peak congestion: $5-10 per inscription. One inscription per merchant per day at 10,000 merchants is under $100/day total at normal fees. Batch during low-mempool periods for cost optimization. Enterprise merchants anchor hourly. The batch size never changes the inscription cost — 1 event or 1 million events, same 32 bytes on-chain.

### What This Proves

When a merchant's attorney needs to establish that POS data has not been altered:

1. Retrieve the Merkle root inscription from Bitcoin L1 (public, permanent, anyone can look it up by block height and inscription ID)
2. Retrieve the raw event hashes from Canary's `raw_events` table for the period
3. Recompute the Merkle tree
4. Compare the root to the inscription
5. If they match: every event in that period is proven unaltered since the inscription timestamp
6. If they don't match: the chain has been tampered with since anchoring

Canary does not need to be present for steps 1-6. The merchant's attorney runs this verification independently. The Bitcoin network is the only authority required.

### What the Merchant Sees

One line in their dashboard: **"Your records are Bitcoin-verified."**

They never think about Ordinals. They never know what a Merkle tree is. They never interact with the inscription. If they ever need it — insurance claim, employee dispute, regulatory audit, legal proceeding — their attorney knows what to do with a Bitcoin inscription ID and a Merkle proof.

### The Product Positioning

This is not loss prevention software. It is **evidentiary infrastructure that happens to catch theft.**

The Chirps are the daily value proposition — operational intelligence, real-time alerts, process improvement. The Bitcoin anchor is the legal backstop that most merchants will never need and will never stop paying for once they understand what it is.

**For the small merchant:** FBI-level evidence at coffee-shop prices. We are giving the little guy the same timestamping infrastructure that federal investigators use — without requiring them to understand any of it. They just run their business. Their records prove themselves.

**For the enterprise buyer:** When LVMH's Rodeo Drive store manager is terminated for theft and their attorney demands to see POS data, the current answer is a CSV export from a system the company controls. Canary's answer is a Bitcoin inscription from the night in question that neither the merchant, nor Canary, nor anyone else could have altered. The block timestamp is the testimony. The Merkle proof is the chain of custody. The attorney rests.

**For the investor:** The combination of canonical CRDM schema, per-merchant partition isolation, hash-chained raw events, and Bitcoin L1 Merkle anchoring is not a feature. It is an architecture that no enterprise vendor has ever offered and that cannot be replicated top-down. It is the moat.

### The Philosophical Point

Satoshi built a system for trustless verification of events in time. Every major use case since has been about money.

Canary applies it to something older than money: **evidence.** The record of what happened, when it happened, that no one can dispute. Not a crypto product. A justice product. Built on the most secure timestamping network ever created. Available to a coffee shop owner for pennies a day.

*We are not the evidence. We are the timestamp. The little guy's data proves itself.*

### Jeffe's Directive — February 26, 2026

> *"We are giving the little guy FBI level evidence. We don't have to even be involved. We are just helping them timestamp their network." — Jeffe*

This is the product. Everything else is how we build it.

### What Needs to Happen

- **Jeremy (B-036):** Verify Square ToS permits raw payload storage. This is the foundation — if we can store the raw payload, we can hash it. If we can hash it, we can anchor it.
- **Tom (B-035):** Design `raw_events` table (JSONB, hash-chained, partitioned) and `anchor_receipts` table (inscription_id, block_height, period, merchant_id, merkle_root). Assess Ordinals inscription tooling (ord, custom service, or third-party API).
- **PhD:** Frame the Merkle-Ordinals architecture in the theoretical framework. This is Satoshi's timestamping system applied to retail evidence — not Layer 2, not a token, pure L1 protocol use. Draft the investor-facing explanation.
- **Syd:** Confirm that a public L1 inscription of a 32-byte Merkle root — which reveals nothing about underlying data, only commits to its existence — creates no regulatory exposure. Confirm that this architecture satisfies or exceeds evidence preservation requirements under applicable law.
- **Eva:** The anchor tier maps to the product menu. Enterprise anchors hourly. Pro anchors daily. Growth anchors weekly. Starter does not anchor (or anchors monthly). This is a Sprint 6 pricing decision.

## Forward Architecture — The Heartbeat Network

*Strategic note captured February 26, 2026. Not Sprint 6. Not Sprint 7. The idea that must be held correctly now so it is built correctly later.*

### Jeffe's Observation

> *"The other play for this heartbeat idea is the time sync issue for IoT devices in store — they are all over the place, connected to different subnets. But if they have a heartbeat to sync on all the time that's immutable. And if other networks do that you can chain it across external too — scary — but the play is there. If we don't do it someone will." — Jeffe, February 26, 2026*

### The Problem Being Solved

Every IoT device in a retail store — cameras, RFID readers, door sensors, cash drawer triggers, POS terminals — runs on its own clock, synced to its own NTP server, on its own subnet. When a forensic event spans multiple devices, the first thing a defense attorney challenges is time synchronization. "Your Honor, the camera and the POS were on different networks. We cannot establish these events are causally related."

This is not a hypothetical. It is the standard defense in retail theft and employee misconduct cases. The evidence exists. The correlation is unprovable because the clocks don't share a common reference.

### The Heartbeat Architecture

Every device in the store anchors its event timestamps to a shared Bitcoin-derived heartbeat. The heartbeat is published periodically — derived from the current Bitcoin block hash, broadcast to all devices on the store network, logged immutably in `anchor_receipts`.

```
Bitcoin L1 block confirmed
    → heartbeat derived from block hash
        → broadcast to all store devices (camera, RFID, door sensor, POS)
            → each device timestamps its events relative to heartbeat block N
                → events from different devices on the same block N
                   are provably simultaneous against an external immutable reference
```

**What this proves in court:** the camera and the POS weren't just close in time — they were on the same Bitcoin block. The network proved it. No NTP dispute. No subnet defense. The shared time reference is public, permanent, and secured by proof-of-work.

**What this enables operationally:** Chirps that correlate across devices. Not just "POS no-sale at 14:32" but "POS no-sale + back room door open + high-value RFID tag last seen + not seen — all on block N+2." That is not a Chirp. That is a case, built automatically, across every sensor in the store, against a shared immutable clock.

### The Cross-Network Implication

This is where the architecture becomes significant beyond a single store.

If one merchant's devices heartbeat to Bitcoin time, their events are on a shared clock with every other merchant whose devices do the same. A BOLO fires in Manhattan Beach. A matching card fingerprint appears in Torrance 40 minutes later. Then Santa Monica. The cross-merchant sequence is not just "we saw this card at three stores" — it is **provably ordered against an external immutable time reference** that no single merchant, no single network, and no single attorney can dispute.

That is a distributed witness network for physical commerce. Every store a node. Bitcoin the shared clock. The correlation engine on top.

### Why This Is "Scary" and Why the Governance Must Be Designed In

The same architecture that proves a shoplifter hit three stores in sequence also proves anything else that happened at those stores at those times. When heartbeats chain across external networks, the system stops being a retail tool and starts being **infrastructure for coordinated real-world event verification at scale.**

That is powerful enough to be misused if governance is not designed from the first merchant.

**What this means for Syd:** the network participation agreement — drafted before any cross-merchant heartbeat correlation exists — must define:
- What a merchant consents to when their heartbeat joins a cross-merchant chain
- What event data leaves their node and in what form
- What cross-merchant correlations are permissible without a warrant
- What requires law enforcement authorization
- What Canary's obligations are as the network operator

This is not a future legal problem. It is a present architectural decision. The governance framework must be built into the network participation agreement before the second merchant joins the heartbeat network. After that it is too late to retrofit.

### The Competitive Position

The heartbeat concept in isolation is not defensible IP — Bitcoin timestamping is prior art. What is defensible is the specific combination:

- Per-merchant partition isolation (data sovereignty)
- Hash-chained raw events (immutable evidence)
- Ordinals Merkle anchoring (external verification)
- IoT heartbeat synchronization (shared time reference)
- Cross-merchant correlation governance (Syd's network participation framework)

That stack, built together with governance embedded from day one, is the moat. No enterprise vendor can replicate it top-down. No startup can replicate it without the merchant base. The network effects compound with every store that joins the heartbeat.

**If we don't build this, someone will.** The architecture is apparent to anyone who thinks carefully about Bitcoin timestamping applied to physical retail. The difference is whether it gets built with Syd's governance framework or without it. We build it with the governance. That is the only responsible way to build it. And it is the version that survives regulatory scrutiny when this becomes a category.

### What Does Not Happen Yet

- No cross-merchant heartbeat correlation before Syd's network participation agreement exists
- No IoT device integration before the heartbeat architecture is formally specified
- No external network chaining before the single-store architecture is proven
- No public discussion of the cross-network implication

This section is internal strategic architecture. It is not a pitch deck slide. It is not a press release. It is the idea held correctly so it gets built correctly.

### What Happens Next (When the Time Is Right)

- PhD: extend the Timestamp Layer theoretical framework to cover multi-device heartbeat synchronization and cross-merchant correlation. Frame the network participation governance requirement.
- Tom: heartbeat broadcast architecture for in-store device sync. How does a device register with the heartbeat? How does it timestamp events relative to block N?
- Syd: network participation agreement framework. Draft before cross-merchant correlation exists, not after.
- Jeremy: heartbeat service design. Lightweight. Runs alongside existing ingest pipeline. Does not touch the hot path.

---

## North Star — Restated

> **The data is the product. The CRDM is the platform. Loss prevention is the first app. It won't be the last.**
>
> Every row is hashed from day one. Every merchant's data is isolated in its own partition. Every evidence chain is externally anchored to Lightning. 14 months of transaction detail on the NRF 4-5-4 calendar. 36 months of aggregated metrics. Indefinite proof of integrity.
>
> We are building the retail data warehouse that 4.5 million small merchants never knew they needed — and the app platform that every retail developer has wanted since the beginning of time. Built bottom-up. Built on open source. Built right from the first merchant.
>
> The merchant gets their data back — organized, analyzed, and actionable. They connect their Square account and for the first time in their career, they can see what's actually happening in their business. Loss prevention today. Forecasting tomorrow. Labor optimization next week. Menu engineering next month. All from the same data. All on their phone. All controlled by them.
>
> "We don't want to add to the stress. We want to ease it." That applies to the data too. The merchant never thinks about integrity, retention, compliance, or infrastructure. They just trust that it works. Because it does. Because it's hashed. Because it's on-chain. Because someone finally built the thing that should have existed all along.

---

*GrowDirect | Canary LP | CONFIDENTIAL*
*February 26, 2026*

## Related

- [[Brain/projects/GrowDirect|GrowDirect MOC]]
- [[Brain/wiki/growdirect-working-papers|Working Papers Structure]]

## Sources

- `docs/_archive/ip-vault/strategy/Canary_Data_Strategy_NorthStar_v1.0.md` — the source doc this card summarizes
