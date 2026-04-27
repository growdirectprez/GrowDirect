---
id: sdd-cp-solution-guide
title: Canary for NCR Counterpoint — Solution Guide
status: draft-1
version: 0.1.0
date: 2026-04-27
author: GrowDirect Engineering
audience: [partner, installer, merchant-cto, engineer]
phase: 1
modules: [S, I, F, R, D, Q]
---

# Canary for NCR Counterpoint — Solution Guide

> **Governing thesis:** NCR Counterpoint is the richest data source in SMB
> retail — tender taxonomy, item cost floors, drawer flags, inventory snapshots,
> customer tiers — and it has never been wired to a detection layer. Canary
> closes that gap. Six modules, one activation sequence, one agent layer on top.
> Every alert is traceable back to a Counterpoint record.

---

## Executive Summary

Canary is a loss prevention and retail analytics platform. For merchants running
NCR Counterpoint through Rapid POS, Canary ingests the Counterpoint data that
operators already generate — transactions, tender types, item costs, inventory
levels — and continuously evaluates it against a detection rule set tuned for
the garden center and hardgoods verticals.

Phase 1 delivers six interconnected modules:

| Module | What it does |
|---|---|
| S — Store & Device | Establishes operational context: which store, which station, which session |
| I — Item Catalog | Sets the cost and margin floor for every item sold |
| F — Finance/Tender | Classifies how money moves: cash, card, AR, gift card |
| R — Customer | Identifies who is buying, their tier, and their AR standing |
| D — Distribution/Inventory | Tracks on-hand quantity against what the register reports sold |
| Q — Loss Prevention | Detects when S/I/F/R/D signals diverge from expected patterns |

The detection output surfaces as Chirp alerts in the Canary dashboard.
ALX — the Canary retail ops agent — explains every alert in plain language
and holds context across sessions. A human investigator owns every case
from triage to closure.

---

## 1. Frame — Strategy

### The problem Counterpoint merchants actually have

NCR Counterpoint gives SMB operators more operational data than any other
SMB POS: cost-of-goods on every line item, a tender taxonomy with drawer
flags, per-customer AR balances, and a full transaction audit log. Most
merchants have none of that wired to anything. They get a Z-report at the
end of the day and a gut feeling.

The result is predictable. Margin erosion happens at the item level — a
cashier discounts below cost on an item the owner never flagged as discountable.
Cash handling problems accumulate across sessions before they're visible in
the bank account. Inventory shrinkage in a garden center is written off to
plant death when it's actually a receiving dock pattern. None of these are
caught by the POS. All of them are detectable with the data Counterpoint
already holds.

### Why these six modules

The six Phase 1 modules are not six features. They are one system. S, I, F,
and R are **substrates** — they supply the context that makes detection
meaningful. D is **enrichment** — it adds the inventory signal that
transactions alone can't provide. Q is the **output** — it fires when the
substrates diverge from the norm.

You cannot run Q without S (no store context), I (no cost floor), or F
(no tender classification). The activation sequence enforces this dependency.
The detection rules are as good as the substrate data beneath them.

### The Rapid POS angle

Rapid POS deploys and supports Counterpoint for garden centers and hardgoods
retailers. The VAR relationship means:

- Rapid POS already holds the merchant relationship and trust
- Installation is a field operation — the VAR rep runs activation
- Calibration draws on the VAR rep's knowledge of how each merchant
  has configured their system (which pay codes are cash-vendor payments,
  what MIN_PFT_PCT they're running, which stores have loose drawer policy)

Canary doesn't replace the VAR relationship. It gives the VAR something to
sell on renewal and a reason for the merchant to stay on the platform.

### Phase 1 scope boundary

Phase 1 is detection against transaction and inventory data. The following
are explicitly deferred:

| Capability | Phase |
|---|---|
| Labor / timecard anomalies (Module L) | Phase 6 |
| Pricing & promotion analysis (Module P) | Phase 3 |
| Commercial / B2B AR analysis (Module C) | Phase 3 |
| Forecast & order anomalies (Module J) | Phase 4 |
| Gift card fraud (Module G) | Phase 2 |
| Loyalty manipulation | Phase 2 |

Detection rules for deferred modules exist in the rule catalog but are
seeded in `is_dry_run = True` and never surfaced to the tenant.

---

## 2. People — Roles & Responsibilities

### Tenant side

| Role | Who | What they do in Canary |
|---|---|---|
| **Owner / Operator** | Business owner | Reviews Chirp alerts, approves Fox case findings, sets rule calibration with VAR rep at go-live |
| **Store Manager** | Location-level manager | Receives location-scoped alerts, provides context on flagged sessions ("that was the vendor delivery"), escalates patterns to owner |
| **LP Investigator** | Owner or designated staff | Works Fox cases from triage to closure — reviews evidence, documents findings, marks resolved |
| **Cashier / Associate** | Front-line staff | Subject of detection. Never interacts with Canary directly. No visibility into the system. |

### Delivery side

| Role | Who | What they do |
|---|---|---|
| **VAR Installer** | Rapid POS field rep (Bart's team) | Runs the onboarding wizard, enters Counterpoint credentials, validates Phase A reference data, sets vertical profile and dry-run duration |
| **GrowDirect Platform** | Canary engineering | Monitors activation health, resolves credential errors, manages platform upgrades. Not in the activation flow for standard deployments. |

### Responsibility matrix

| Action | Owner/Op | Store Mgr | LP Inv | VAR Installer | GrowDirect |
|---|---|---|---|---|---|
| Counterpoint credential entry | | | | **R** | |
| Phase A–C activation | | | | **R** | C |
| Dry-run → live decision | **R** | | | C | |
| Alert triage | C | **R** | C | | |
| Fox case investigation | C | C | **R** | | |
| Case closure | **R** | | C | | |
| Rule threshold adjustment | **R** | | | C | |
| Credential rotation | | | | **R** | C |

R = responsible, C = consulted.

### Who never touches the system

Cashiers and associates have no Canary account, no visibility into alerts,
and no notification of any kind during Phase 1. Investigation is conducted
by the LP investigator reviewing transaction records. Canary surfaces
evidence; it does not confront individuals.

---

## 3. Agents — Automation Layer

Canary operates on two planes: automated (runs without human instruction)
and assisted (responds to human queries). The line between them is fixed
and intentional.

### The four agents

**Chirp — Detection Engine**

Automated. Runs continuously. Evaluates every ingested Counterpoint
transaction against the active rule set the moment it is parsed. No human
triggers it. No human approves individual rule evaluations. Chirp fires or
it doesn't — the result is a Chirp alert or silence.

Chirp is not configurable by cashiers or managers. Thresholds are set
at tenant activation by the owner + VAR installer and adjusted at scheduled
calibration reviews.

**ALX — Retail Ops Agent**

Assisted. Responds to queries from the merchant owner and LP investigator.
ALX holds the full context of the tenant's Canary deployment — their rule
configuration, alert history, active Fox cases, and the Counterpoint data
model that feeds them. A merchant can ask "why did this alert fire on Tuesday
afternoon?" and ALX will trace it back to the specific transaction, tender
type, and rule threshold that triggered it.

ALX does not act. It informs. It does not close cases, adjust thresholds,
or send communications without a human instruction.

**Owl — Analytics AI**

Assisted. Responds to analytical queries: period-over-period comparisons,
cash share trends, category margin drift, drawer session anomaly frequency.
Owl operates at the aggregate level — it surfaces patterns that Chirp's
per-transaction evaluation misses because they only become visible across
sessions or weeks.

**Onboarding Agent**

Assisted, activation-scoped. Guides the VAR installer through the four-step
wizard (connection test → Phase A → Phase B → go-live). Surfaces open
questions against the tenant's specific configuration (unexpected PAY_COD
values, walk-in sentinel discovery, store count mismatch). Retired after
Phase C activation completes.

### Where automation stops and people start

```
Counterpoint data →  Chirp (automated)  →  Alert created
                                              │
                                        ALX available for context
                                              │
                                        Store manager triages
                                              │
                                        LP investigator reviews evidence
                                              │
                                        Owner approves / closes case
```

**Nothing in Canary closes a case without a human decision.** Chirp fires,
ALX explains, a person decides. This is a design constraint, not a limitation.
Loss prevention findings that drive HR or legal action require a documented
human decision chain. Canary preserves that chain.

### Automation boundaries by module

| Module | Automated | Human-in-loop |
|---|---|---|
| S — Store/Device | Session detection, drawer open event tracking | Store manager confirms session anomalies |
| I — Item Catalog | Cost floor computation, margin substrate refresh | Owner reviews threshold calibration |
| F — Tender | Tender classification, cash-share computation | Store manager explains vendor payment patterns |
| R — Customer | Customer resolution, tier context | LP investigator reviews high-value customer patterns |
| D — Inventory | Snapshot ingestion, delta computation | Store manager explains write-offs |
| Q — Loss Prevention | Rule evaluation, alert creation, case auto-open | LP investigator owns triage and closure |

---

## 4. Model — Operational System

The six modules do not run in parallel. They run in a dependency order
that mirrors how a retail operation actually produces observable data.

### The substrate → enrichment → detection flow

```
┌─────────────────────────────────────────────────────────┐
│  SUBSTRATES  (must be loaded before detection runs)      │
│                                                          │
│  S — Store/Device                                        │
│    What store? What station? What session?               │
│    Provides: str_id → location, opn_drw sessions,        │
│              walk-in sentinel, timezone, cost floor cfg  │
│                                                          │
│  I — Item Catalog                                        │
│    What was sold? At what cost? Is it discountable?      │
│    Provides: item_no → lst_cost, min_pft_pct,            │
│              is_discntbl, prompt_for_prc                 │
│                                                          │
│  F — Finance/Tender                                      │
│    How did money move? Cash or card or AR?               │
│    Provides: pay_cod → canonical_type, opn_drw flag      │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  ENRICHMENT  (context layered onto transaction records)  │
│                                                          │
│  R — Customer                                            │
│    Who bought? Known account or walk-in?                 │
│    Provides: cust_no → tier, AR balance, disc_pct        │
│                                                          │
│  D — Distribution/Inventory                              │
│    What should be there vs. what the register shows?     │
│    Provides: qty_on_hnd snapshots, delta vs. sales       │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  DETECTION                                               │
│                                                          │
│  Q — Loss Prevention                                     │
│    Where do the signals diverge from expected?           │
│    Consumes: all five substrates above                   │
│    Produces: Chirp alerts → Fox cases → human action     │
└─────────────────────────────────────────────────────────┘
```

### How the modules speak to each other

Every Counterpoint transaction document (`PS_DOC`) arrives with a `STR_ID`,
one or more `ITEM_NO` line items, one or more `PAY_COD` payment lines, and
optionally a `CUST_NO`.

- `STR_ID` resolves via **S** → Canary location + session context
- Each `ITEM_NO` resolves via **I** → cost floor, margin flag, discount flag
- Each `PAY_COD` resolves via **F** → canonical tender type, drawer-open flag
- `CUST_NO` resolves via **R** → customer tier and AR standing (or walk-in if
  `CUST_NO` matches the store's walk-in sentinel)
- The parsed transaction + current inventory snapshot from **D** feeds the
  delta computation

**Q** evaluates the assembled record. Every rule in Q has an explicit substrate
dependency — no rule fires against raw Counterpoint fields. If a substrate is
missing (e.g. PayCodes not yet synced), the transaction is queued and the
missing sync is triggered. Detection does not proceed on incomplete data.

### Activation ordering enforces the data dependency

```
Phase A (reference data)
  A1: Store & Station sync    → S substrate ready
  A2: Item Categories sync    → I category taxonomy ready
  A3: PayCode sync            → F substrate ready

Phase B (entity seeding, parallel)
  B1: Customer roster sync    → R substrate ready
  B2: Item catalog sync       → I substrate ready

Phase C (live, after B complete)
  C1: Document poll loop      → transactions flow
  C2: Inventory poll loop     → D substrate refreshes hourly
  Q:  Chirp evaluation        → fires on every ingested document
```

A `Phase C` transaction evaluated before `Phase B` completes would have
no item cost floor and no customer context. The activation service enforces
the gate. There is no bypass.

### The canonical data model

Regardless of POS source, every Canary tenant operates against the same
canonical tables:

| Canonical table | Populated by | Consumed by |
|---|---|---|
| `app.locations` | S adapter | Q rules (store context) |
| `app.products` | I adapter | Q rules (item identity) |
| `app.customers` | R adapter | Q rules (customer context) |
| `sales.transactions` | T (document) adapter | Q rules, Owl analytics |
| `sales.transaction_line_items` | T adapter | Q rules (item-level) |
| `sales.transaction_tenders` | T adapter + F substrate | Q-TM rules |
| `app.external_identities` | all adapters | cross-source resolution |

Counterpoint-specific attributes (cost floor, tender type, drawer flag,
inventory qty) live in `cp_*` tables and are joined at rule evaluation time.
The canonical tables are POS-agnostic; the `cp_*` tables are Counterpoint's
contribution to them.

---

## 5. Blueprint — Module Implementation

One section per module. Each section states the retail spine capability
(what the module does in any retail operation), the Canary implementation
(what we built), the Counterpoint contract (what CP provides), and the
Phase 1 scope boundary.

---

### Module S — Store & Device

**Retail spine capability (L1–L3):**
Every retail operation is organized around physical locations and the
devices operating within them. A transaction without store and station
context is not auditable. Store configuration — discount limits, drawer
policy, loss prevention thresholds — varies by location and must be
respected by any detection system.

**Canary implementation:**
- `app.locations` — canonical store record (vendor-agnostic)
- `app.cp_store_config` — Counterpoint-specific config: `max_disc_pct`,
  `use_void_comp_reas`, `allow_drw_reactiv`, `min_pft_pct`, `login_per_tkt`
- `app.cp_station_config` — per-station: `edc_present`, `drwr_present`,
  `allow_rcpt_print`
- `walk_in_cust_no` — per-store anonymous customer sentinel (read from
  `PS_STR_CFG_PS`, not hardcoded)
- State → IANA timezone lookup — 50-state table for after-hours rule
  normalization (Counterpoint stores carry no timezone field)

**Counterpoint contract:**
`PS_STR` + `PS_STA` + `PS_STR_CFG_PS` via `GET /Stores/{id}` +
`GET /Stations` + `GET /CustomerControl`. Synced daily (Phase A1).

**Phase 1 scope:** Store and station config only. Multi-company
(multiple `company_alias` on one server) is deferred.

**Reference SDD:** `ncr-counterpoint-store-station-adapter.md`

---

### Module I — Item Catalog

**Retail spine capability (L1–L3):**
The item catalog is the merchant's product master. Every line item on
every transaction references it. For detection purposes, the catalog
provides the cost floor (below what price is a sale a loss?), the
discount authorization flag (is this item discountable at all?), and
the category margin target (what margin does this product family carry?).

**Canary implementation:**
- `app.cp_item_catalog` — per-item: `lst_cost`, `min_pft_pct`,
  `trgt_pft_pct`, `is_discntbl`, `prompt_for_prc`, `is_weighed`,
  `restricted_flags` (JSONB)
- `app.cp_item_categories` + `app.cp_item_subcategories` — category
  taxonomy with margin targets
- Cache-miss pattern: unknown `ITEM_NO` on a transaction triggers
  on-demand `GET /Item/{no}` within the same poll cycle

**Counterpoint contract:**
`IM_ITEM` + `IM_CATEG_COD` via `GET /Items` (incremental, `RS_UTC_DT`
watermark) + `GET /Categories`. Item catalog synced daily (Phase B2).
Categories synced daily (Phase A2).

**Phase 1 scope:** Item master and categories. Bill-of-materials /
kit components deferred. Mix-and-match bundle margin (Q-MM) is seeded
dry-run only.

**Reference SDD:** `ncr-counterpoint-item-catalog-adapter.md`

---

### Module F — Finance/Tender

**Retail spine capability (L1–L3):**
Payment method classification is the foundation of cash handling analysis.
A register that processes only card tenders behaves differently than a
cash-heavy register. Detecting tender manipulation — swapping card for
cash after the fact, unusual cash share in a session — requires a
normalized taxonomy across all payment methods.

**Canary implementation:**
- `app.cp_pay_codes` — per pay code: `canonical_type`, `opn_drw`,
  `edc_auth_flg`, `pay_typ`
- `canonical_type` — normalized across POS sources: `cash | card | ar |
  gift_card | store_credit | check | foreign | other`
- `sales.transaction_tenders.source_pay_code` — raw `PAY_COD` string
  preserved for audit join
- `resolve_tender_type()` — resolves `PAY_COD` → canonical at parse time;
  cache-miss triggers PayCode re-sync

**Counterpoint contract:**
`PS_PAY_COD` via `GET /PayCodes`. Full re-sync daily (no watermark —
PayCodes is small, < 50 rows typically). `ServerCache: no-cache` header
on first poll of the day.

**PAY_TYP → canonical mapping:**

| PAY_TYP | Canonical |
|---|---|
| C | cash |
| K | check |
| E | card |
| A | ar |
| G / V | gift_card |
| S | store_credit |
| F | foreign |
| other | other |

**Phase 1 scope:** Tender classification and cash-share substrate.
Gift card reconciliation and SVS voucher fraud deferred to Phase 2.

**Reference SDD:** `ncr-counterpoint-paycode-adapter.md`

---

### Module R — Customer

**Retail spine capability (L1–L3):**
Knowing who is buying provides essential context for detection. A 40%
discount to a Gold-tier AR account is a loyalty program in action. The
same discount to a walk-in cash customer is a red flag. Customer tier,
AR standing, and purchase history modulate what is normal for any given
transaction.

**Canary implementation:**
- `app.customers` — canonical customer record (vendor-agnostic bridge)
- `app.cp_customer_profiles` — Counterpoint attributes: `categ_cod`,
  `cust_typ`, `allow_ar_chrg`, `disc_pct`, `loy_pts_bal`, `bal` (AR balance),
  `terms_cod`
- `app.cp_tier_definitions` — `CATEG_COD` taxonomy for the tenant
- PII strip at parse time — name, address, phone, email never stored in
  Canary; `loy_pts_bal` and `disc_pct` retained as operational signals
- Walk-in resolution: `CUST_NO == walk_in_cust_no` (per-store sentinel
  from Module S) → customer resolved as anonymous, not bridged

**Counterpoint contract:**
`AR_CUST` via `GET /Customers` (incremental, `RS_UTC_DT` watermark).
Full roster seeded at Phase B1. Daily incremental thereafter.

**Phase 1 scope:** Customer identity resolution and tier context.
GDPR/CCPA deletion flow deferred. Loyalty manipulation rules seeded
dry-run only.

**Reference SDD:** `ncr-counterpoint-customer-adapter.md`

---

### Module D — Distribution/Inventory

**Retail spine capability (L1–L3):**
Inventory is the ground truth that transaction records approximate.
When on-hand quantity drops faster than sales explain, something is
wrong — whether theft, write-off, receiving fraud, or data entry error.
A detection system that only watches the register misses everything
that happens on the floor and at the dock.

**Canary implementation:**
- `app.cp_inventory_snapshots` — point-in-time snapshots per
  `(item_no, loc_id)`: `qty_on_hnd`, `qty_on_ord`, `qty_commit`,
  `qty_avail`, `lst_cost`, `avg_cost`, `lst_cnt_dt`, `lst_rcv_dt`
- Delta query: snapshot-before minus snapshot-after minus qty-sold
  = `unexplained_drop` → Q-IS-02 input
- Retention: 90-day rolling window; nightly prune
- Poll: hourly per store (one `GET /InventoryLocations?Loc={id}` per
  known store ID)

**Garden center vertical context:**
Live-goods write-offs are legitimate inventory drops without corresponding
sales. Seasonal write-off baselines (Q1–Q4) are seeded at vertical
activation and suppress false positives during expected die-off periods.
Vendor cash payments (RECVR + cash tender) are pre-classified as
legitimate via the `C-1601` allow-list.

**Counterpoint contract:**
`IM_INV` via `GET /InventoryLocations` (incremental, `RS_UTC_DT`
watermark). Hourly poll, Phase C alongside document polling.

**Phase 1 scope:** Inventory snapshot and shrinkage detection.
Receiving dock variance (C-1603) seeded dry-run for calibration.
BOM / kit inventory deferred.

**Reference SDD:** `ncr-counterpoint-inventory-adapter.md`

---

### Module Q — Loss Prevention

**Retail spine capability (L1–L3):**
Loss prevention is the synthesis layer. It consumes every operational
signal the other modules produce and evaluates whether the observed
pattern is consistent with legitimate retail behavior. It does not
work in isolation — a void is not inherently suspicious; a void on
a cash transaction by a cashier with seven voids in a session, on an
item that was below cost, is.

**Canary implementation:**

*Rule scheme:*
- Square-origin rules: `C-001` through `C-D03` (existing, 37 rules)
- Counterpoint-specific rules: `C-1001` through `C-2001` (new, 4-digit scheme)

*Phase 1 active rule families:*

| Family | Rule IDs | What they detect |
|---|---|---|
| Discount / Markdown | C-1001, C-1003 | Discount cap exceeded; below-cost sale |
| Void | C-1101, C-1102 | Void without original; return without original |
| Audit Trail | C-1401 | Document edited after payment |
| Margin Erosion | C-1501, C-1502 | Below category margin; free item override |
| Inventory Shrink | C-1601, C-1602, C-1603, C-1604 | Cash vendor payment; session drop; receive no increase; seasonal spike |
| Compliance | C-2001 | Restricted item sold without override |
| Tender Mix | Q-TM-01, Q-TM-02 | Cash-only register; tender swap |
| Drawer Session | Q-DS-01 | Drawer session shrinkage |

*Deployment model:*
All rules activate in `is_dry_run = True` at Phase C. No alerts surface
to the tenant during the calibration period (default 7 days). The VAR
installer and owner review the dry-run alert volume before flipping live.
This prevents false positive floods on day one.

*Garden center allow-lists (pre-seeded at vertical activation):*

| Rule | Allow-list behavior |
|---|---|
| C-1601 | Cash-vendor-payment = informational; routes to ad-hoc vendor review queue |
| C-1604 | Seasonal write-off baselines by quarter; informational mode |
| C-1901 | Bundle margin computation; mix-and-match expected overlap |
| C-2001 | Restricted flags empty at activation; evidence retention 2555 days |

**Counterpoint contract:**
Q consumes no Counterpoint endpoints directly. It reads the canonical
and `cp_*` tables populated by S, I, F, R, and D. Q is POS-source-agnostic
at evaluation time — the substrates are the contract.

**Phase 1 scope:** The rule families above. Loyalty manipulation,
gift card fraud, and labor rules are seeded dry-run and deferred.

**Reference SDDs:**
`ncr-counterpoint-module-q-chirp-wiring.md` · `ncr-counterpoint-paycode-adapter.md`
(Q-TM) · `ncr-counterpoint-inventory-adapter.md` (Q-IS)

---

## 6. Activation — How It Goes Live

The complete activation sequence, from credential entry to first live alert:

```
Day 0 — Installation
  VAR installer enters Counterpoint credentials + company alias
  test_connection() validates against GET /APIVersion
  Credentials stored encrypted in pos_tenant_credentials

  Phase A (same day, ~15 minutes):
    A1: Store & station sync  →  2 stores, 6 stations loaded
    A2: Item categories sync  →  taxonomy ready
    A3: PayCode sync          →  8 pay codes, canonical types mapped

Day 0–1 — Seeding (runs overnight)
  Phase B (parallel, 2–8 hours depending on catalog size):
    B1: Customer roster sync  →  all AR accounts loaded (PII stripped)
    B2: Item catalog sync     →  all items loaded with cost floors

Day 1 — Go Live (dry run)
  Phase C activates:
    Document poll loop starts  →  transactions ingested every 5 minutes
    Inventory poll loop starts →  snapshots taken hourly
    Chirp evaluates every document
    ALL rules in is_dry_run = True — alerts fire internally, not surfaced

Days 1–7 — Calibration
  VAR installer + owner review dry-run alert volume
  Adjust thresholds: cash-share threshold, discount cap, write-off baseline
  Confirm allow-lists are correct for this merchant's patterns

Day 7 — Live flip
  Owner approves  →  is_dry_run = False
  First live Chirp alerts appear in dashboard
  ALX available for alert explanation
```

---

## 7. What Phase 2 Unlocks

Phase 1 delivers the substrate + detection foundation. Phase 2 builds on it:

| Capability | Requires from Phase 1 |
|---|---|
| Gift card fraud (C-G rules) | F tender substrate (gift_card canonical type) |
| Loyalty manipulation | R customer substrate (loy_pts_bal) |
| Pricing & promotion analysis (Module P) | I item catalog (price points, promo flags) |
| Commercial AR analysis (Module C) | R customer substrate (AR balance, terms) |
| Labor timecard anomalies (Module L) | S store/station (session timing) |

None of Phase 2 requires additional POS endpoints. The data is already
flowing. Phase 2 is rule development against an established substrate,
not a new integration effort.

---

## Related

- `docs/sdds/canary/pos-adapter-substrate.md` — POSAdapter ABC; the generic integration contract
- `docs/sdds/canary/ncr-counterpoint-merchant-onboarding.md` — Activation service; wizard UI
- `docs/sdds/canary/ncr-counterpoint-auth-adapter.md` — Credential storage and lifecycle
- `docs/sdds/canary/ncr-counterpoint-open-questions.md` — Open questions register; Bart call prep
- `Brain/wiki/ncr-counterpoint-phase-0-context-brief.md` — Engagement background
- `Brain/wiki/canary-module-q-counterpoint-rule-catalog.md` — Full rule catalog with garden-center annotations
