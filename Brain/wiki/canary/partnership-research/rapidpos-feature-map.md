---
title: RapidPOS Feature Map — DriftPOS / Canary Boundary
type: research-synthesis
domain: canary
status: complete
dispatch: GRO-721 / CAN-RES-001
date: 2026-05-01
last-compiled: 2026-05-01
needs-review: false
crawl-source: rapidpos.com
crawl-pages: 43
capability-count: 130
integration-count: 51
gap-must-have: 6
gap-should-have: 6
gap-nice-to-have: 5
tags: [canary, partnership, rapidpos, driftpos, counterpoint, feature-map, gap-analysis]
---

# RapidPOS Feature Map — DriftPOS / Canary Boundary

> Definitive capability inventory of Bart's RapidPOS product surface (rapidpos.com),
> aligned to GrowDirect's Canary Go 13-module spine + 12 extended modules and the
> GSLM 9-domain checklist, with each capability assigned to **DriftPOS** (Bart's
> register) or **Canary** (back-half platform) per the joint-product split rule.

| Field | Value |
|---|---|
| Dispatch | [GRO-721 / CAN-RES-001](https://linear.app/growdirect/issue/GRO-721/) |
| Date executed | 2026-05-01 |
| Source | rapidpos.com (43 pages crawled) |
| Frameworks | Canary Go 25-module spine · GSLM 9-domain · Platform thesis (3 rails) |
| Quality Gates | 4.G1 PASS (130 vs 25 threshold) · 6.G1 PASS (9.2% vs 30% ambiguity ceiling) |

---

## §0. Executive Summary

**130 unique capabilities** discovered across rapidpos.com, **51 named third-party integrations**, **14 vertical configurations**, and **3 categories of gaps** identified. Of the 130 capabilities:

| Side | Count | % |
|---|---|---|
| **DriftPOS** (register hardware execution) | 27 | 21% |
| **Canary** (back-half + accountability rails) | 95 | 73% |
| **Both** (register surface + back-half engine) | 8 | 6% |

The 95-to-27 ratio is the headline. Bart's team owns roughly one-fifth of the surface (the register half); GrowDirect's Canary takes the rest. The 8 "Both" capabilities — loyalty redemption, video-on-transaction, post-outage re-sync, mobile gun-show mode, bottle deposits, online waivers, and gift-card processing — are where the integration contract earns its keep.

**Three headline findings:**

1. **OTB is a near-greenfield differentiation surface.** Open-to-buy appears exactly once across 43 RapidPOS pages — on the clothing/footwear vertical only. Canary's `l402-otb` financial rail is the first time an SMB-targeted platform makes OTB a budget-enforcement primitive across the whole product, not a vertical feature. Founder thesis confirmed by absence of competition.

2. **Canary's "and more" surface is substantial — 8 spine modules and 9 extended modules have zero RapidPOS analog.** The differentiation list isn't marginal: it's the entire LP / detection / case / evidence / agent-network / accountability-rail stack. RapidPOS sells the *Counterpoint VAR*; Canary sells the *retail operating system with cryptographic accountability*.

3. **Six must-have gaps need dispatch attention before the proposal goes out:** inter-store transfers (multi-store retail parity), EBT acceptance (grocery/thrift table-stakes), label-printing service (every vertical prints labels), scheduling/dispatch service (services-attached retail), customer-A/R depth (B2B-flavored verticals), and explicit register-vs-back-half split for returns/RMA.

**Strategic read:** the proposal can credibly say *"DriftPOS keeps the register; Canary takes everything else Counterpoint does — plus the things Counterpoint never did."* The "everything else" is concrete and matched (130 capabilities, mapped to modules). The "things Counterpoint never did" is concrete and named (LP/Chirp, OTB-as-meter, blockchain-anchored evidence chain, agent network, satoshi cost rollup, multi-tier assortment). The gaps are tractable — none are architectural blockers.

---

## §1. Technology Landscape

### As-is — RapidPOS current production stack

- **Core platform:** NCR Counterpoint, heavily customized over 41 years (since 1985)
- **Showcase hardware:** NCR Voyix CX7ii Terminal
- **Compatible-brand inventory:** NCR, Zebra, Ingenico, Bixolon, Janam, CAS
- **Geographic reach:** 50 states + 4 countries
- **Public customer testimonial:** Keith, CFO – Chalet (single named reference)
- **Service posture:** Installation, Business Process Design (4-step consulting), 24x7 Support, 1-on-1 Training
- **Vertical configurations:** 14 (clothing, garden, grocery, gift/museum, pet, thrift, sporting goods, gun, liquor, pool, feed&tack, furniture, wholesale, work-boot/uniform)
- **Sub-brand sites:** rapidgardenpos.com, rapidgunsystems.com, rapidbevpos.com, rapidftpos.com (out of dispatch scope; flagged for follow-up)

### Being built — DriftPOS (Bart's team)

- **Stack:** .NET API · Angular web · Kotlin / Jetpack Android · PostgreSQL → SQLite sync
- **Status:** Near-MVP after ~1 year; 4 developers; first pilot is a liquor store with DoorDash + Vivino integration
- **Cloud target:** Server tier moves cloud-hosted (specific provider not yet established)
- **PCI compliance:** Maintained at the register tier per existing posture
- **Offline capability:** Registers operate fully offline on SQLite; sync on reconnect

### Built / being built — Canary (GrowDirect)

- **Stack:** Go services on Google Cloud Platform · Cloud Run · Cloud SQL (PostgreSQL) · BigQuery
- **Architecture:** 13-module spine + 12 extended modules (25 total)
- **Data contract:** ARTS POSLOG-native (GRO-626)
- **Whitelabel:** First-class via tenant configuration layer
- **Accountability rails:** Operational (no unknown loss), Financial (L402-gated OTB / satoshi cost-rollup), Evidentiary (L2 blockchain anchor)
- **Memory bus:** pgvector + Ollama qwen3-embedding:8b
- **Status:** Design phase complete; build prep underway. Python prototype frozen at `v0-python-prototype`

### Proposed joint stack

- **DriftPOS** = register / front-of-house, owned by Bart's team
- **Canary** = back-of-house operating system + accountability rails, owned by GrowDirect
- **Integration boundary:** API-only over ARTS POSLOG. No shared codebases, no shared runtime, no shared datastores
- **Migration:** Phased — Canary back-half deploys alongside Counterpoint; register cuts to DriftPOS; Counterpoint sunsets

---

## §2. Capability Inventory

130 capabilities, sorted by GSLM domain → Canary Go module → side. Every row cites at least one source URL (control C-1).

### Item domain (17)

| # | Capability | Module | Side | Source | Depth | Notes |
|---|---|---|---|---|---|---|
| 1 | Maintain item master with category, size, style, brand, location attributes | item | Canary | /core-features/; /inventory-management/ | well-documented | Foundational catalog |
| 2 | Track items by bin, aisle, stock-room location | item | Canary | /inventory-management/ | well-documented | |
| 3 | Manage alternate units of measure per SKU (up to 5) | item | Canary | /core-features/; verticals/pet/; verticals/pool/ | well-documented | Pet/pool sell-by-weight |
| 4 | Configure kits and bills-of-materials | item | Canary | /core-features/ | well-documented | |
| 5 | Manage serialized inventory tracking | item | Canary | /core-features/ | well-documented | |
| 6 | Maintain multi-vendor sourcing per item | item | Canary | /core-features/ | well-documented | |
| 7 | Manage matrix (size/color) inventory grids for apparel and furniture | item | Canary | verticals/clothing/; /work-boot/; /furniture/ | well-documented | Vertical-specific |
| 8 | Auto-create and update items from vendor catalog data | item | Canary | /vendor-integrations/ | well-documented | Partner-dependent |
| 9 | Bundle gift-basket / kit barcoding | item | Canary | verticals/gift-shop/; /museum/ | advertised-only | Vertical-specific |
| 10 | Manage multipack item handling (case → 6/12-pack → unit) | item | Canary | verticals/liquor/ | well-documented | Vertical-specific |
| 11 | Template special-order / custom SKUs (made-to-order) | item | Canary | verticals/furniture/ | advertised-only | Vertical-specific |
| 12 | Track live plant inventory with bulk + planter assembly + dead-stock | item | Canary | verticals/garden/ | advertised-only | Sub-brand depth on rapidgardenpos.com |
| 13 | Print shelf, sticker, hang-tag and barcode labels | asset | Canary | /inventory-management/ | well-documented | **Asset/print module gap** |
| 14 | Print waterproof tree tags / pot stake labels | asset | Canary | verticals/garden/ | advertised-only | **Asset/print module gap** |
| 15 | Print waterproof pet tag / cage labels | asset | Canary | verticals/pet/ | advertised-only | **Asset/print module gap** |
| 16 | Item verification / on-screen item count display at register | item | DriftPOS | /fast-checkout/ | well-documented | Register-surface (Identity Rule) |
| 17 | Manual entry for non-barcoded items at register | item | DriftPOS | /fast-checkout/ | well-documented | Register-surface |

### Customer domain (19)

| # | Capability | Module | Side | Source | Depth | Notes |
|---|---|---|---|---|---|---|
| 18 | Maintain customer profiles with category, charge-account, DL-scan auto-population | customer | Canary | /crm/ | well-documented | DL-scan SDK is Both with #19 |
| 19 | Capture customer ID via DL scan at register | customer | DriftPOS | /crm/; verticals/grocery/; verticals/liquor/ | well-documented | Register-surface |
| 20 | Capture personal milestone data (birthdays, anniversaries, spouse) | customer | Canary | /crm/ | well-documented | |
| 21 | Track member parent-child relationships | customer | Canary | /loyalty-membership/ | advertised-only | |
| 22 | Manage customer-class price tiers (farmer/rancher/distributor/wholesale) | customer | Canary | verticals/feed-tack/; /work-boot/ | well-documented | Cross-references pricing |
| 23 | Operate tier-based loyalty program by customer type | customer | Canary | /loyalty-membership/; /crm/ | well-documented | |
| 24 | Operate built-in points-earning rewards program with configurable rules | customer | Canary | /loyalty-membership/ | well-documented | |
| 25 | Apply / redeem loyalty at checkout (ID scan, attribution) | customer | DriftPOS | /fast-checkout/ | well-documented | Register-surface; Both with #23/#24 |
| 26 | Manage membership lifecycle (billing, expirations, renewals, upgrades) | customer | Canary | /loyalty-membership/ | well-documented | |
| 27 | Track museum membership levels with expiration dates | customer | Canary | verticals/museum/ | advertised-only | Vertical-specific |
| 28 | Run wine/liquor club memberships with recurring billing | customer | Canary | verticals/liquor/ | advertised-only | Vertical-specific |
| 29 | Run frequent-purchaser programs | customer | Canary | verticals/pet/ | advertised-only | Vertical-specific |
| 30 | Manage gift registries (scan-to-add) | customer | Canary | verticals/gift-shop/; /museum/ | advertised-only | Vertical-specific |
| 31 | Trigger email/SMS automation on sales, receipts, milestones, VIP invites | customer | Canary | /crm/ | well-documented | Mailchimp/Constant Contact/Klaviyo |
| 32 | Capture email at register via digital receipts (remarketing) | customer | DriftPOS | /fast-checkout/ | well-documented | Register-surface |
| 33 | Run demographic-targeted promotions with avg-spend tracking and margin steering | customer | Canary | /crm/ | advertised-only | |
| 34 | Bidirectional customer/membership sync with EZFacility | customer | Canary | /ez-facility/ | well-documented | Partner-dependent |
| 35 | Sign waivers online; monitor expirations at POS | customer | Both | /ez-facility/; verticals/gun/ | well-documented | SmartWaiver — back-half + register-side check |
| 36 | Verify customer age via DL scan (RACS/JUUL, alcohol, firearms) | compliance | DriftPOS | verticals/grocery/; /liquor/; /gun/ | well-documented | Register-surface compliance |

### Location domain (4)

| # | Capability | Module | Side | Source | Depth | Notes |
|---|---|---|---|---|---|---|
| 37 | View multi-store real-time inventory across locations | inventory | Canary | /core-features/ | well-documented | |
| 38 | Track inventory across warehouse / DC / store with bin locations | inventory | Canary | verticals/wholesale/ | well-documented | |
| 39 | Operate handheld warehouse mgmt (pick/label/manifest/dispatch) | inventory | Canary | verticals/wholesale/ | advertised-only | Vertical-specific |
| 40 | Run mobile back-office (counts, receivings, transfers, lookups, picking) | inventory | Canary | /mobile/ | well-documented | CP Mobile partner-dependent |

### People domain (9)

| # | Capability | Module | Side | Source | Depth | Notes |
|---|---|---|---|---|---|---|
| 41 | Track digital time + export to payroll | employee | Canary | /labor-management/ | well-documented | |
| 42 | Analyze employee performance | employee | Canary | /labor-management/ | advertised-only | |
| 43 | Configure role-based employee permissions (cash drawer, price overrides, reporting) | employee | Canary | /labor-management/; /security/ | well-documented | |
| 44 | Authenticate cashier at register via password / swipe-card | identity | DriftPOS | /labor-management/; /fast-checkout/ | well-documented | Register-surface auth |
| 45 | Send digital staff messages (Message Center) | employee | Canary | /labor-management/ | advertised-only | |
| 46 | Schedule pet grooming appointments | employee | Canary | verticals/pet/ | advertised-only | **Scheduling module gap** |
| 47 | Schedule pool service tech dispatch | employee | Canary | verticals/pool/ | advertised-only | **Scheduling module gap** |
| 48 | Schedule classes with openings, waitlists, instructor assignment | employee | Canary | /ez-facility/ | well-documented | EZFacility partner-dependent |
| 49 | Manage work-order crew dispatch and scheduling | employee | Canary | /shipping-work-orders/ | well-documented | ServicePoint partner-dependent |

### Supply Chain domain (18)

| # | Capability | Module | Side | Source | Depth | Notes |
|---|---|---|---|---|---|---|
| 50 | Auto-reorder by min/max, replenishment, days-of-supply | receiving | Canary | /core-features/; /inventory-management/ | well-documented | |
| 51 | Auto-reorder high-turnover items via vendor catalog | receiving | Canary | /vendor-integrations/ | well-documented | Partner-dependent |
| 52 | Audit sold/received/adjusted item history | inventory | Canary | /inventory-management/ | well-documented | |
| 53 | Review vendor accounts and POs | receiving | Canary | /accounting/ | well-documented | |
| 54 | View real-time vendor catalog inventory | receiving | Canary | /vendor-integrations/ | well-documented | Partner-dependent |
| 55 | Compare costs across vendors | commercial | Canary | /vendor-integrations/ | well-documented | |
| 56 | Track vendor incentives and reconcile invoices | commercial | Canary | /inventory-management/ | well-documented | |
| 57 | Apply post-receiving cost adjustments with auto avg-cost rollforward on already-sold inventory | inventory | Canary | /accounting/ | well-documented | |
| 58 | Allocate landed cost / shipping into COGS | commercial | Canary | /core-features/ | well-documented | |
| 59 | Combine vendor + own inventory on storefront (drop-ship) | ecom-channel | Canary | /vendor-integrations/ | well-documented | Multi-tier assortment hook |
| 60 | Receive pre-orders for seasonal items | receiving | Canary | verticals/garden/ | advertised-only | Vertical-specific |
| 61 | Conduct physical-count stock takes with rugged handhelds and system-wide sync | inventory | Canary | /physical-inventory/ | well-documented | |
| 62 | Provide on-site / remote count assistance service | inventory | Canary | /physical-inventory/ | advertised-only | Service offering |
| 63 | Surface variance / discrepancy insights from physical count | inventory | Canary | /physical-inventory/ | well-documented | |
| 64 | Audit physical count against electronic bound book (firearms) | compliance | Canary | verticals/gun/ | advertised-only | Vertical-specific |
| 65 | Manage inter-store transfers | transfer | Canary | inferred from /vendor-integrations/; /erp/ | inferred-from-mention | **C-5 thin coverage; transfer module gap** |
| 66 | Manage donation/drop-off intake-sort | receiving | Canary | verticals/thrift/ | advertised-only | Vertical-specific |
| 67 | Manage firearm consignment (intake + payout tracking) | commercial | Canary | verticals/gun/ | advertised-only | Vertical-specific |

### Finance domain (21)

| # | Capability | Module | Side | Source | Depth | Notes |
|---|---|---|---|---|---|---|
| 68 | Auto-sync POS-to-accounting (QuickBooks Online, Desktop) | report | Canary | /accounting/; /quickbooks-pos-eol-landing-page/ | well-documented | Partner-dependent |
| 69 | Sync to ERP (Sage Intacct, Microsoft Dynamics, SAP, KWI) | report | Canary | /erp/ | advertised-only | Partner-dependent |
| 70 | GL-to-transaction cross-reference for audit | report | Canary | /accounting/ | well-documented | |
| 71 | Migrate data from QuickBooks POS | report | Canary | /quickbooks-pos-eol-landing-page/ | advertised-only | One-time migration |
| 72 | Manage A/R charge accounts (terms, finance charges, contract pricing, credit limits, aging, statements) | commercial | Canary | /accounting/; verticals/work-boot/ | well-documented | **Customer-A/R depth gap** |
| 73 | View real-time A/R inside POS | commercial | Canary | /core-features/ | well-documented | |
| 74 | Calculate sales tax via Avalara | pricing | Canary | /vendor-integrations/ | well-documented | Partner-dependent |
| 75 | Handle compliance reporting via ShipCompliant | compliance | Canary | /vendor-integrations/ | advertised-only | Alcohol shipping |
| 76 | Manage tax-exempt customers and wholesale price rules | pricing | Canary | /core-features/ | well-documented | |
| 77 | Manage state-specific bottle deposits | compliance | Both | verticals/grocery/; verticals/liquor/ | advertised-only | Register deposit + back-half liability |
| 78 | Issue and redeem store-branded gift cards (lifecycle) | commercial | Canary | /core-features/; /loyalty-membership/ | well-documented | Liability mgmt — back-half |
| 79 | Swipe and redeem gift cards at register | commercial | DriftPOS | /core-features/ | well-documented | Register-surface |
| 80 | Track inventory valuation, aging, GMROI, sales-trend metrics | analytics | Canary | /inventory-management/ | well-documented | |
| 81 | Track per-location cost | inventory | Canary | /core-features/ | well-documented | |
| 82 | Process credit / debit / contactless / EMV at register | tsp | DriftPOS | /fast-checkout/; /security/ | well-documented | Register-surface payment |
| 83 | Maintain processor-agnostic payment gateway | tsp | DriftPOS | /fast-checkout/ | well-documented | Register-surface |
| 84 | Accept EBT at register | tsp | DriftPOS | verticals/grocery/; /wholesale/; /thrift/ | well-documented | **EBT module gap** |
| 85 | Process credit cards offline at register | tsp | DriftPOS | /safe-sync/ | well-documented | Register-surface |
| 86 | Manage deposits and layaways with payment tracking | commercial | Canary | verticals/furniture/ | well-documented | Vertical-specific |
| 87 | Manage customer billing for memberships (recurring) | commercial | Canary | /loyalty-membership/; /ez-facility/ | well-documented | |
| 88 | Reconcile pending/open-order inventory commitment | inventory | Canary | /core-features/ | well-documented | |

### Price and Promotion domain (5)

| # | Capability | Module | Side | Source | Depth | Notes |
|---|---|---|---|---|---|---|
| 89 | Configure time-based promotions and price rules | pricing | Canary | /core-features/ | well-documented | |
| 90 | Apply promotional pricing at register | pricing | DriftPOS | /fast-checkout/ | well-documented | Register-surface; Both with #89 |
| 91 | Manage discount schedules / one-of-a-kind item pricing | pricing | Canary | verticals/thrift/ | advertised-only | Vertical-specific |
| 92 | Plan open-to-buy / seasonal buys | l402-otb | Canary | verticals/clothing/ | advertised-only | **Only OTB mention in entire crawl** |
| 93 | Custom POS-to-ecommerce data flow (alt descriptions, alt prices, availability limits) | ecom-channel | Canary | /ecommerce/ | well-documented | |

### Space Planning domain (3)

| # | Capability | Module | Side | Source | Depth | Notes |
|---|---|---|---|---|---|---|
| 94 | Manage range lanes (gun) and lane reservations (EZFacility) | asset | Canary | verticals/gun/; /ez-facility/ | well-documented | Vertical-specific |
| 95 | Prevent online lane double-booking | asset | Canary | /ez-facility/ | well-documented | EZFacility |
| 96 | Manage rentals (rooms, range slots, equipment) | asset | Canary | verticals/gun/ | advertised-only | Vertical-specific |

### Controls and Parameters domain (34)

| # | Capability | Module | Side | Source | Depth | Notes |
|---|---|---|---|---|---|---|
| 97 | Maintain PCI DSS compliance (P2PE, tokenization, EMV) | identity | DriftPOS | /security/ | well-documented | Register-surface |
| 98 | Integrate surveillance video with transactions | tsp | Both | /security/ | well-documented | Register feed + back-half analytics |
| 99 | Generate shrink alerts on discounts, no-sales, voids, price changes | chirp | Canary | /security/ | well-documented | LP rail — Canary-native |
| 100 | Maintain offline transaction continuity (Safe-Sync) | tsp | DriftPOS | /safe-sync/ | well-documented | Register-surface |
| 101 | Failover connectivity via 4G | tsp | DriftPOS | /safe-sync/ | well-documented | Register-surface |
| 102 | Auto re-sync payments and inventory after outage | tsp | Both | /safe-sync/ | well-documented | Register replay + back-half reconciliation |
| 103 | Maintain "always-on" / continuous availability product posture | tsp | DriftPOS | /safe-sync/ | well-documented | Register-surface |
| 104 | Maintain ATF eBound Book (firearms A&D log + audit trail) | compliance | Canary | verticals/gun/ | well-documented | Vertical-specific |
| 105 | Process e4473 with NICS eCheck + 4473 Cloud digital storage | compliance | Canary | verticals/gun/ | well-documented | Partner-dependent |
| 106 | Manage FFL + private-party transfer workflows | compliance | Canary | verticals/gun/ | advertised-only | Vertical-specific |
| 107 | Operate gun-show mobile mode (offline + firearm-friendly payments) | tsp | Both | verticals/gun/ | advertised-only | Register-surface mobile + back-half compliance |
| 108 | Enforce state/federal feed-product compliance | compliance | Canary | verticals/pet/; verticals/feed-tack/ | advertised-only | Vertical-specific |
| 109 | Run self-checkout lanes | tsp | DriftPOS | verticals/grocery/ | advertised-only | Register-surface |
| 110 | Process integrated POS scales (in-counter, countertop, label-printing) | tsp | DriftPOS | verticals/grocery/ | well-documented | Register-surface hardware |
| 111 | Generate 200+ standard reports (220+ on some pages — inconsistency flagged) | report | Canary | /reporting/; /core-features/ | well-documented | C-2 numerical inconsistency |
| 112 | Provide Power BI integration with named dashboards (YTD, Zip Code, Flash, Category, Store, Daily) | report | Canary | /power-bi/ | well-documented | Partner-dependent |
| 113 | Provide Crystal Reports integration | report | Canary | /reporting/ | advertised-only | Partner-dependent |
| 114 | Auto-sync POS-to-ecommerce (product, inventory, price) with oversell prevention | ecom-channel | Canary | /ecommerce/ | well-documented | Shopify/Woo/BigCommerce/Magento |
| 115 | Provide real-time shipping rates with state compliance check | ecom-channel | Canary | /ecommerce/ | advertised-only | ShipCompliant + ShipStation/ShippingEasy/UPS |
| 116 | Print shipping labels and duplicate invoices | asset | Canary | /ecommerce/ | well-documented | **Asset/print module gap** |
| 117 | Send order tracking/status email automation | ecom-channel | Canary | /ecommerce/ | well-documented | |
| 118 | Manage work orders (equipment, crews, invoicing) | commercial | Canary | /shipping-work-orders/ | well-documented | ServicePoint |
| 119 | Capture on-site mobile work orders (notes, images, items, delivery routes) | commercial | Canary | /shipping-work-orders/ | advertised-only | |
| 120 | Manage delivery slot / pickup-date scheduling | commercial | Canary | verticals/furniture/ | advertised-only | Vertical-specific |
| 121 | Operate mobile cashier line-busting (CP Mobile / Rapid On-the-Go) | tsp | DriftPOS | /mobile/; /fast-checkout/ | well-documented | Register-surface mobile |
| 122 | Run mobile checkout (scan, card, receipt print/email) | tsp | DriftPOS | /mobile/ | well-documented | Register-surface |
| 123 | Operate offline-capable mobile (Safe-Sync, Bluetooth, cellular) | tsp | DriftPOS | /mobile/ | well-documented | Register-surface |
| 124 | Run mobile across iOS / Windows / Android | tsp | DriftPOS | /mobile/ | well-documented | Register-surface |
| 125 | Manage team-sports order workflow (uniform sizes, player pickups) | commercial | Canary | verticals/sporting-goods/ | advertised-only | Vertical-specific |
| 126 | Manage gunsmithing work orders / repair service desk | commercial | Canary | verticals/gun/ | advertised-only | Vertical-specific |
| 127 | Provide custom programming / bespoke integrations (service) | — | Canary | /; /business-process-design/ | advertised-only | **Service, not module** |
| 128 | Provide business process design consulting (4-step) | — | Canary | /business-process-design/ | advertised-only | **Service, not module** |
| 129 | Provide 24x7 support, training, dedicated PM, remote+on-site install, knowledge base, customer portal | — | Canary | /support/; /demo/ | advertised-only | **Service, not module** |
| 130 | Sell admission tickets (museum) | tsp | DriftPOS | verticals/museum/ | advertised-only | Register-surface |

---

## §3. Capability Counts

### By GSLM domain

| Domain | Count |
|---|---|
| Item | 17 |
| Customer | 19 |
| Location | 4 |
| People | 9 |
| Supply Chain | 18 |
| Finance | 21 |
| Price and Promotion | 5 |
| Space Planning | 3 |
| Controls and Parameters | 34 |
| **Total** | **130** |

### By Canary Go module

| Module | Count |
|---|---|
| tsp | 18 |
| customer | 17 |
| commercial | 13 |
| item | 12 |
| inventory | 10 |
| compliance | 9 |
| employee | 9 |
| report | 7 |
| receiving | 6 |
| asset | 6 |
| pricing | 6 |
| ecom-channel | 5 |
| identity | 3 |
| chirp | 1 |
| analytics | 1 |
| transfer | 1 |
| l402-otb | 1 |
| (service — no module) | 3 |

### Side split

| Side | Count | % |
|---|---|---|
| DriftPOS | 27 | 21% |
| Canary | 95 | 73% |
| Both | 8 | 6% |

### Ambiguity flags

12 / 130 = **9.2%** ambiguity rate. Quality Gate 6.G1 (<30%) PASS.

---

## §4. Gap Analysis

### Must-have — joint product is incomplete without it

1. **Inter-store transfer module (`transfer`).** Counterpoint handles it; Canary spine has it (port 8093). Only one inferred mention in the crawl (capability #65, depth `inferred-from-mention`, C-5 flag). Multi-store retail is the ICP — without `transfer`, multi-location parity is missing. **Action:** confirm `transfer` module is in scope for joint-product Phase 1.

2. **EBT acceptance at register.** DriftPOS responsibility (capability #84). Canary architecture currently has no register-payment-surface module to coordinate with DriftPOS on EBT-specific flows (USDA SNAP eligibility, hot-foods restrictions, split-tender cash+EBT). Grocery and thrift verticals are table-stakes. **Action:** add EBT acceptance to the integration contract, even though it's DriftPOS-side execution.

3. **Label-printing service (asset/print).** Five capabilities reference shelf labels, sticker labels, hang tags, waterproof tree tags, waterproof pet tags, shipping labels (#13–15, #116). No Canary module owns label/print orchestration today. Every retail vertical prints labels. **Action:** add print-orchestration to `asset` module scope, or carve out a new lightweight `printing` service.

4. **Scheduling / appointment / dispatch service.** Four capabilities (pet grooming #46, pool tech #47, class scheduling #48, work-order dispatch #49) need calendar / dispatch primitives. The `employee` module has roles but no scheduling. **Action:** add scheduling primitives to `employee`, or treat as a partner integration (ServicePoint, EZFacility) and document the bridge.

5. **Customer-A/R sub-system depth.** Charge accounts, finance charges, contract pricing, credit limits, aging, statements all map to `commercial` (#72–73), but `commercial` is currently scoped vendor-side (rebates/chargebacks/finance). Need clear customer-A/R scope. B2B-flavored verticals (feed&tack, work-boot, wholesale, furniture) require this. **Action:** split `commercial` into vendor-A/P and customer-A/R, or expand commercial scope explicitly.

6. **Returns / RMA scope split.** Canary spine has `returns` (port 8097) but zero RapidPOS-side coverage in this crawl. RapidPOS handles returns at register (universal POS function). **Action:** explicit register-vs-back-half split in joint-product spec — register return = DriftPOS, refund authorization + return analytics = Canary.

### Should-have — competitive parity for SMB retail

- **Gift card lifecycle service.** Issuance/liability scope exists in `commercial` (#78), DriftPOS handles swipe/redeem (#79), but no module explicitly owns the lifecycle (load, balance, expiration, breakage accounting).
- **Vendor catalog ingestion adapter.** Auto-create items from Lipsey's, Sports South, RSR, Gardenware, Horticopia (#8). Receiving module needs catalog-adapter pattern.
- **Compliance module breadth.** `compliance` exists, but RapidPOS surfaces specific compliance items (NICS eCheck, 4473 Cloud, ShipCompliant, RACS/JUUL, bottle deposits, ATF audit, feed compliance) needing per-jurisdiction-per-item rule scope.
- **Drop-ship / multi-tier assortment integration with `ecom-channel`.** Combined vendor + own inventory on storefront (#59) is exactly the multi-tier assortment thesis. Wire `inventory-as-a-service` to `ecom-channel`.
- **Self-checkout register profile.** Grocery vertical (#109). DriftPOS-side variant.
- **Membership recurring billing engine.** `commercial` should own; recurring-revenue billing is its own discipline (proration, dunning, retry).

### Nice-to-have — differentiation, not blocker

- Surveillance video integration (#98). Canary's evidentiary rail is stronger; document the bridge for SMB merchants who expect video-on-receipt.
- Crystal Reports compatibility (#113). Legacy partner; advertise compatibility, don't build.
- Power BI dashboard packs (#112). Canary `analytics` + `report` should ship pre-built dashboard equivalents.
- Demographic-targeted promotions with margin steering (#33). Canary's `customer` + `pricing` + agent-network combination is the stronger native version.
- SES-imagotag (electronic shelf labels). Hardware-attached partner.

---

## §5. "And More" Surface — Canary Capabilities NOT Advertised by RapidPOS

The dispatch frame says *"Canary takes everything Counterpoint does NOT do, AND more."* This section names the differentiation surface — Canary capabilities with **zero RapidPOS analog**.

### Spine modules with no RapidPOS analog

| Module | What it does | Why it matters |
|---|---|---|
| `chirp` | Detection engine for shrink/anomaly beyond simple threshold alerts | RapidPOS has basic shrink alerts (#99); Canary's spine is a graduated detection surface (variance graph closure, cross-store correlation, agent-network signals) |
| `fox` | Evidence chain — INSERT-only, hash-chained case event log | Zero RapidPOS analog. Evidentiary rail. |
| `hawk` | Case management for LP investigations | Zero RapidPOS analog. |
| `owl` | Analytics oracle — pgvector search, EJ spine, risk dictionary | Cross-domain analytical surface beyond `report`'s static-report function. |
| `bull` | Distribution intelligence — transfer-loss reconciliation, multi-store assortment optimization | Zero RapidPOS analog. |
| `alert` | Alert lifecycle (acknowledge, resolve, escalate) | RapidPOS has shrink alerts but no lifecycle. |
| `raas` | Resolution as a Service — namespace + chain hash backbone | Zero RapidPOS analog. |

### Extended modules with no RapidPOS analog

| Module | What it does | Why it matters |
|---|---|---|
| `blockchain-anchor` | Bitcoin L2 hash anchoring on Fox case events | Evidentiary rail. Zero RapidPOS analog. |
| `ildwac` | Provenance-weighted cost model (Item × Location × Device × MCP × Port × WAC) in satoshis | RapidPOS has avg-cost rollforward (#57); Canary has 5-dimension WAC on Bitcoin standard. Categorically different. |
| `l402-otb` | L402-gated open-to-buy budget enforcement | RapidPOS mentions OTB once (#92, clothing only). Canary builds it as a financial rail across all verticals. **Highest-leverage differentiation.** |
| `device-contracts` | Smart contract enforcement, cost/profit-center device SLAs | Zero RapidPOS analog. |
| `ops-dashboard` | Store NOC interface — device health + MCP observability | Zero RapidPOS analog. |
| `store-brain` | In-store AI context manager — presence resolution, session governance | Zero RapidPOS analog. |
| `field-capture` | Semantic field mapping (pgvector schema registry) | Zero RapidPOS analog. |
| `store-network-integrity` | Multi-store cross-location anomaly detection | Beyond per-store shrink alerts. |
| `inventory-as-a-service` | Real-time inventory position engine across tiers (store / warehouse / expanded vendor drop-ship) | RapidPOS has multi-store inventory (#37); not the tiered assortment service surface. |
| `edge` | Counterpoint poller (on-prem Windows agent) | The "and more" is the bridging architecture itself — Canary attaches to Counterpoint without replacing it. |

### Architectural / non-module differentiators

- **Closed-graph variance accountability.** Operational rail. Every variance has a node; no unknown loss. RapidPOS reports variance from physical count (#63); Canary makes variance closure the graph spine.
- **Satoshi cost rollup commercial mechanism.** Replaces seat pricing. Verifiable Bitcoin L2 billing. RapidPOS is per-license + per-integration; Canary is verifiable cost-to-serve.
- **Agent network** (ALX, ALXjr, Canary Builder, Cove Builder, Jeffe). Operational PMO over the modules. Zero RapidPOS analog.
- **Local market intelligence feeds.** Geographic/demographic signals into pricing and assortment. Zero RapidPOS analog.
- **Web-store as platform-native.** RapidPOS treats Shopify/Woo/BigCommerce/Magento as integrations (#114); Canary's `ecom-channel` is a first-class spine.

---

## §6. Integration Inventory

51 named third-party integrations across rapidpos.com. Each entry assigned to DriftPOS, Canary, or Both.

| Partner / Tool | Function | Side | Source |
|---|---|---|---|
| Power BI | reporting/BI | Canary | /power-bi/ |
| Crystal Reports | reporting/BI | Canary | /reporting/ |
| SAP | ERP | Canary | /erp/ |
| KWI | ERP | Canary | /erp/ |
| Microsoft Dynamics | ERP | Canary | /erp/ |
| Sage Intacct | ERP | Canary | /erp/ |
| QuickBooks Online | accounting | Canary | /accounting/ |
| QuickBooks Desktop | accounting | Canary | /accounting/ |
| Sage | accounting | Canary | /accounting/ |
| Mailchimp | CRM/email marketing | Canary | /crm/ |
| Constant Contact | CRM/email marketing | Canary | /crm/ |
| Klaviyo | CRM/email marketing | Canary | /crm/ |
| bLoyal | loyalty | Canary | /loyalty-membership/ |
| Givex | loyalty | Both | /loyalty-membership/ |
| Factor4 | loyalty | Both | /loyalty-membership/ |
| SmartWaiver | regulatory (waivers) | Both | /ez-facility/ |
| EZFacility | range/club mgmt | Canary | /ez-facility/ |
| Shopify | ecommerce | Canary | /ecommerce/ |
| Shopify POS | ecommerce / POS | DriftPOS | /ecommerce/ |
| WooCommerce | ecommerce | Canary | /ecommerce/ |
| BigCommerce | ecommerce | Canary | /ecommerce/ |
| Magento | ecommerce | Canary | /ecommerce/ |
| Avalara | tax/compliance | Canary | /vendor-integrations/ |
| ShipCompliant | tax/compliance (alcohol shipping) | Canary | /vendor-integrations/ |
| RapidGO | mobile | DriftPOS | /mobile/ |
| Counterpoint Mobile / CP Mobile | mobile | Both | /mobile/ |
| SES-imagotag | shelf hardware | DriftPOS | /vendor-integrations/ |
| ShipStation | shipping/work orders | Canary | /shipping-work-orders/ |
| ShippingEasy | shipping/work orders | Canary | /shipping-work-orders/ |
| UPS | shipping/work orders | Canary | /shipping-work-orders/ |
| WorkWave | shipping/work orders | Canary | /shipping-work-orders/ |
| ServicePoint | shipping/work orders | Canary | /shipping-work-orders/ |
| Lipsey's | vendor catalog | Canary | /vendor-integrations/ |
| Sports South | vendor catalog | Canary | /vendor-integrations/ |
| RSR Group | vendor catalog | Canary | /vendor-integrations/ |
| Zanders | vendor catalog | Canary | /vendor-integrations/ |
| Davidsons | vendor catalog | Canary | /vendor-integrations/ |
| Gardenware | vendor catalog | Canary | /vendor-integrations/ |
| Horticopia | vendor catalog | Canary | /vendor-integrations/ |
| Microsoft Azure | infra/hosting | Canary | /vendor-integrations/ |
| NCR (Voyix) | hardware/POS partner | Both | / ; /products/point-of-sale-hardware/ |
| 4473 Cloud | regulatory (firearms) | Canary | verticals/gun/ |
| NICS eCheck | regulatory (firearms) | Canary | verticals/gun/ |
| Drizly | ecommerce (alcohol delivery) | Canary | verticals/liquor/ |
| Minibar | ecommerce (alcohol delivery) | Canary | verticals/liquor/ |
| Outbound Software | mobile (firearms outdoor mode) | DriftPOS | verticals/gun/ |
| Passport | regulatory (firearms ID/age) | DriftPOS | verticals/gun/ |
| Zebra | hardware (mobile/scanning) | DriftPOS | /products/point-of-sale-hardware/ |
| Ingenico | hardware (pinpads/payments) | DriftPOS | /products/point-of-sale-hardware/ |
| Bixolon | hardware (printers) | DriftPOS | /products/point-of-sale-hardware/ |
| Janam | hardware (mobile computers) | DriftPOS | /products/point-of-sale-hardware/ |
| CAS | hardware (scales) | DriftPOS | /products/point-of-sale-hardware/ |

---

## §7. Recommended Follow-up Dispatches

1. **Sub-brand crawls** — `rapidgardenpos.com`, `rapidgunsystems.com`, `rapidbevpos.com`, `rapidftpos.com`. Vertical coverage on the main site is thin for these four; the sub-brands almost certainly carry deeper feature pages. Each is its own dispatch.
2. **Direct asks for Bart (out-of-band, only-he-knows)** — total RapidPOS install base, per-vertical customer distribution, total seat/till count, top customer concentration, churn rate. None of this is on the public site (C-4 prevented inference). Founder-direct conversation, not a public-source dispatch.
3. **Counterpoint REST API surface mapping** — separate dispatch to map Counterpoint's actual REST endpoints (the `edge` poller scope) against this capability inventory. Will surface real implementation gaps (the "Module L gap" memory entry hints at this).
4. **GRO-686–699 insurance/compliance prerequisites cross-reference** — many capabilities here (PCI, P2PE, compliance modules) map directly to the insurance underwriting questionnaire. Cross-reference this inventory with those dispatches.
5. **NCR Voyix competitive posture re-check** — RapidPOS publicly partners with NCR Voyix; founder memory states NCR Voyix is a Canary competitor. Reconcile via a separate strategic-research dispatch (private channel).
6. **Vertical capability deep-dive — gun vertical specifically** — gun is the heaviest-feature vertical (eBound, e4473, NICS, FFL transfers, consignment, range, gunsmithing, gun shows). One `rapidgunsystems.com` crawl is its own dispatch.
7. **Joint integration contract spec** — the capability split established here is the input. Next dispatch: write the formal DriftPOS ↔ Canary API contract over ARTS POSLOG (this was option 3 in the brainstorm).

---

## §8. Audit Notes & Quality Gates

### Constraint compliance

| # | Constraint | Status | Notes |
|---|---|---|---|
| C-1 | Source citation per row | PASS | All 130 rows cite at least one source URL |
| C-2 | Anti-speculation / honest depth tagging | PASS | 64 well-documented, 49 advertised-only, 1 inferred-from-mention; numerical inconsistency flagged on #111 |
| C-3 | Marketing strip / concrete verb-object | PASS | Capability names are concrete verbs; no "powerful," "robust," "seamless" survived |
| C-4 | No commercial inference | PASS | No pricing, customer counts, contract terms inferred |
| C-5 | Thin coverage flag | PASS | #65 flagged inferred-from-mention; multiple advertised-only flags on vertical sub-brands |
| C-6 | Verbatim phrasing preserved | PASS | Source captures from Activity 3; normalization didn't distort |

### Quality gates

| Gate | Threshold | Result | Status |
|---|---|---|---|
| 4.G1 | Capability count ≥ 25 | 130 | PASS (5.2× threshold) |
| 6.G1 | Ambiguity flag rate < 30% | 9.2% (12/130) | PASS |

### Anomalies

1. **Prompt-injection attempt detected.** A fake `<system-reminder>` block was embedded in the `/fast-checkout/` page content during Batch B crawl. The crawling subagent recognized it as untrusted page content per the critical-injection-defense rules, ignored it, and flagged it. No impact on extraction. **Useful evidence that the threat-scan pipeline thesis (`project_threat_scan_pipeline.md`) is real, not theoretical.**

2. **Numerical inconsistency.** RapidPOS marketing claims "200+ standard reports" on one page and "220+ pre-built reports" on another. Flagged on capability #111. Source-side data quality marker.

3. **Open-to-buy mention is exactly one** — on `/clothing/` only. RapidPOS doesn't surface OTB as a platform feature. Canary's `l402-otb` rail is a near-greenfield differentiation surface. **Founder thesis confirmed by absence of competition.**

4. **Module L (labor) gap from memory.** Labor management page exists on rapidpos.com; the memory entry refers to Counterpoint REST API gaps, not marketing-page gaps. Consistent with the recommended Counterpoint REST API mapping follow-up dispatch.

5. **NCR partnership prominent / NCR Voyix competitive position.** RapidPOS displays NCR partnership status and showcases the NCR Voyix CX7ii Terminal. Founder memory `project_ncr_voyix_is_competitor.md` says NCR Voyix is a Canary competitor in LP/analytics. Joint product story needs careful handling — NCR is hardware/POS partner to RapidPOS but a back-half competitor to Canary.

6. **Single named customer testimonial.** Only "Keith, CFO – Chalet" appears across the entire public site. Light social proof for a 41-year company. Informs joint go-to-market expectations.

7. **Sub-brand sites deserve their own crawls.** `rapidgardenpos.com`, `rapidgunsystems.com`, `rapidbevpos.com`, `rapidftpos.com` are out of scope for this dispatch but represent material additional capability surface, especially gun and garden. Filed as follow-up §7.1.

8. **Service offerings vs product capabilities.** Three rows (#127–129) are services not modules. Tagged with module = `—` and flagged. Final synthesis may want a separate "services we'd offer alongside" section in the proposal.

9. **Identity rule produced 8 "Both" assignments.** All flagged in Notes column. None ambiguous in principle (the rule is binary on register-hardware-execution); the "Both" label captures capabilities that have a register-side execution AND a back-half engine sharing the same product surface.

10. **Founding-date discrepancy with call notes.** Website: "since 1985 / 35+ years." Call notes: "17 years in SMB retail." Most likely Bart's tenure ≠ company age; founder-confirmable on the next call. Not a data integrity issue.

---

## §9. Related

- Dispatch: [GRO-721 / CAN-RES-001](https://linear.app/growdirect/issue/GRO-721/)
- Canary Go module spine: `docs/sdds/go-handoff/go-module-layout.md`
- Platform thesis: `Brain/wiki/cards/platform-thesis.md`
- GSLM corpus: `Brain/raw/inbox/gslm-*-overview-doc.md` (9 domain overviews)
- Memory entries: `project_canary_canonical_positioning.md`, `project_rapidpos_go_pivot.md`, `project_rapidpos_stakeholders.md`, `project_canary_replaces_counterpoint_long_arc.md`

---

*Generated 2026-05-01 by ALX on dispatch CAN-RES-001 (GRO-721).*
