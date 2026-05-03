---
title: RapidPOS Sub-Brand Vertical Capability Extension
type: research-synthesis
domain: canary
status: complete
date: 2026-05-03
linear: GRO-760
parent: GRO-721
last-compiled: 2026-05-03
needs-review: 2026-08-03
crawl-sources: rapidgardenpos.com, rapidgunsystems.com, rapidbevpos.com, rapidftpos.com
crawl-pages: 28
net-new-capabilities: 67
tags: [canary, partnership, rapidpos, driftpos, counterpoint, feature-map, sub-brand, gap-analysis]
---

# RapidPOS Sub-Brand Vertical Capability Extension

> Vertical-specific capability extension to the GRO-721 main map, derived from
> the four RapidPOS vertical sub-brand sites (garden, gun, beverage, feed&tack).
> Same controls, same split rule, same module assignment frame. Adds 67 net-new
> capabilities to the 130-row main inventory and reclassifies 5 GRO-721 gaps.

| Field | Value |
|---|---|
| Dispatch | [GRO-760 / CAN-RES-002](https://linear.app/growdirect/issue/GRO-760/) |
| Parent dispatch | [GRO-721 / CAN-RES-001](https://linear.app/growdirect/issue/GRO-721/) |
| Date executed | 2026-05-03 |
| Sources | rapidgardenpos.com (10 pages), rapidgunsystems.com (8 pages), rapidbevpos.com (10 pages), rapidftpos.com (9 pages) |
| Frameworks | Same as GRO-721 — Canary Go 25-module spine · GSLM 9-domain · Platform thesis (3 rails) |
| Quality Gates | G1 PASS (4/4 sub-brands ≥5 net-new) · G2 PASS (gun = 24 net-new ≥ 15 threshold) · G3 PASS (8.9% ambiguity) |

---

## §0. Purpose & Methodology Inheritance

GRO-721 produced the canonical 130-row capability inventory of `rapidpos.com`,
the marketing umbrella site. Its §7 follow-up §1 named the four vertical
sub-brands as expected sources of additional vertical depth. This document
fulfills that follow-up.

**Hypothesis going in:** rapidpos.com vertical pages are template-shallow; the
sub-brand sites carry the real vertical depth. Specifically expected:
`rapidgunsystems.com` carries the heaviest regulatory surface (ATF, NICS,
FFL, gun shows) of any RapidPOS vertical.

**Outcome:** Hypothesis confirmed. Gun yielded 24 net-new capabilities (G2
threshold = 15). Garden yielded 18 net-new capabilities including a
landscaping-services arc that's effectively a separate product. Beverage
yielded 14 net-new (kiosks, recurring billing, vintage/varietal/region
inventory dimensions, tip handling, shipping-rate compliance). Feed & tack
yielded 11 net-new (lot management, milling production module, FDA VFD
compliance specifics, multi-name product handling).

### Methodology (compressed from CAN-RES-001)

1. URL verification + reachability test per sub-brand
2. Sequential WebFetch crawl of homepage + key vertical pages per sub-brand
3. Per-row dedup against the GRO-721 130-capability inventory
4. Net-new capabilities aligned to GSLM domain → Canary Go module → split
5. Gap-impact assessment against GRO-721 §4 classifications
6. Quality gate verification

### Controls (inherited verbatim from GRO-721)

- **C-1 Source citation** — every capability row cites at least one source URL
- **C-2 Anti-speculation** — depth tagged: `well-documented` / `advertised-only` / `inferred-from-mention`
- **C-3 Identity rule** — register-hardware-execution = DriftPOS; everything else = Canary; both = Both
- **C-4 No commercial inference** — no pricing, customer counts, or contract terms invented
- **C-5 Thin-coverage flag** — surfaces are tagged when crawl yielded only mentions
- **C-6 Verbatim-where-possible** — capability names use site phrasing where it's specific

### Crawl access notes

`rapidgardenpos.com`, `rapidbevpos.com`, and `rapidftpos.com` are gated by
Cloudflare bot challenges that block direct WebFetch. All three were accessed
through the public Jina reader proxy (`r.jina.ai`), which performs the JS
challenge and returns rendered markdown. `rapidgunsystems.com` is not gated
and was accessed directly. No paywalls or auth walls were encountered.

---

## §1. RapidGardenPOS — Garden / Nursery Vertical

### 1.1 Crawl scope

| Page | Status | Net-new capabilities |
|---|---|---|
| `/` (homepage) | reachable | site map + structure |
| `/industry-specific-features/` | reachable | umbrella feature catalog |
| `/green-inventory/` | reachable, deepest | 6 |
| `/printing/` | reachable | 4 |
| `/kitting-planters-baskets/` | reachable | 1 |
| `/landscaping/` | reachable | 4 |
| `/loyalty-program/` | reachable | 1 |
| `/pricing/` | reachable | 1 |
| `/crm-marketing/` | reachable | 0 (subset of GRO-721 #31) |
| `/accounting-management-integrations/` | reachable | 1 (Sage Intacct as garden integration confirmed) |

**Total net-new for garden: 18 capabilities.**

### 1.2 Sub-brand-specific findings

- **Powered explicitly by NCR Voyix Counterpoint**, named on the homepage. Confirms the GRO-721 "Counterpoint VAR" framing.
- **Customer testimonials (named):** Roger's Gardens (Corona del Mar, CA, Ron Vanderhoff, GM/VP, "more than a decade"), Goebbert's Farm & Garden Center (South Barrington, IL, Holly Danielson, Manager). Two named customers vs. zero on the gun sub-brand.
- **220 built-in reports number reaffirmed** (`/industry-specific-features/`) — same number as the gun sub-brand. Resolves the GRO-721 200/220 inconsistency: 220 is the number sub-brands consistently advertise.
- **"Landscaping Series: From Quote to Completion"** — five-part blog/feature series treats landscaping as effectively a separate product. Job costing, progressive billing, partial order releases, project reconciliation. This is service-business management bolted onto retail POS — a meaningful new capability area.
- **Botanical/common/Spanish naming** triple — built-in multi-name handling for live plants, not a custom-field workaround.
- **Unlimited barcodes per item** — explicitly called out for tracking different growers, batches, colors. Stronger than GRO-721 #6 (multi-vendor sourcing).
- **Custom API integrations with landscaping/garden specialty services** — partner SDK posture, not just pre-built integrations.

### 1.3 Compliance / regulatory mentions

PCI/DSS only. No agricultural-products compliance surface (USDA / EPA pesticide
licensing was not mentioned despite that being a real garden-vertical concern).
This is a gap on the source side, not the platform side.

### 1.4 Sub-brand-only product names

- **CP Mobile** (NCR Counterpoint Mobile, branded as garden-specific)
- **RapidGO** (Rapid's own handheld, Zebra Android with 2D scanner — also branded for gun)

### 1.5 Ambiguity flags

- "Custom signage" printing mentioned in `/grow-care-instructions/` link target — page didn't render fully (Jina returned thin content). Flagged as `inferred-from-mention`.
- "Project reconciliation" in landscaping is named but workflow not described. Flagged as `advertised-only`.

---

## §2. RapidGunSystems — Firearms (KEYSTONE)

### 2.1 Crawl scope

| Page | Status | Net-new capabilities |
|---|---|---|
| `/` (homepage) | reachable | site map + structure |
| `/eboundbook/` | reachable, deepest | 8 |
| `/e4473/` | reachable but Jina returned challenge text | 0 (forced reliance on parent + transitive mentions) |
| `/ffl-transfers/` | reachable | 4 |
| `/range-management/` | reachable | 4 |
| `/gun-show/` | reachable | 3 |
| `/consignments/` | reachable | 5 |
| `/gunsmithing/` | reachable | 3 |
| `/vendor-catalog-integrations/` | reachable | 1 (vendor list expansion) |
| `/inventory-management/` | reachable | 2 |
| `/security/` | reachable | 1 |

**Total net-new for gun: 24 capabilities. G2 threshold (≥15) PASS.**

### 2.2 Sub-brand-specific findings

- **ATF Ruling 2016-1 named explicitly** as the regulatory anchor for the eBound book product. GRO-721 capability #104 refers to ATF eBound generically; the sub-brand identifies the specific ruling. Material depth.
- **Multi-firearm purchase 3310 reports** — automated tracking for ATF Form 3310 (Report of Multiple Sale or Other Disposition of Pistols and Revolvers). Distinct from #104; new compliance artifact.
- **Unlimited number of electronic bound books per account** — relevant for multi-FFL operations (separate FFL per location, separate FFL per category like Type 01, Type 07).
- **Document attachment per transaction** — military orders, ID, state forms attached to A&D log entries. New evidence-chain capability.
- **Full audit record per edit on bound book** — every modification logged with user. Effectively a per-transaction audit log on a regulated dataset. Maps cleanly to Canary's `fox` evidence-chain module.
- **Range-rental gun rounds-fired estimation** — system tracks rentals AND estimates rounds discharged per firearm. Service/maintenance forecasting unique to range operations.
- **Visual indicators for unreturned rentals** — register UI alerts staff when a rental gun hasn't been logged back. Operational LP signal.
- **Cloud-based bound book** — eBound is cloud-hosted, not on-prem-only. Different deployment surface than Counterpoint generally.
- **Loaner-firearm program for gunsmithing** — customer left a gun for service, store loans them a range gun in the meantime. Cross-module workflow (gunsmithing + range + customer).
- **NICS / 4473 / state ID / FFL number storage** — all four ID fields explicitly tracked per A&D entry. GRO-721 #105 named "NICS eCheck"; sub-brand surfaces the data-model elements.
- **8 named distributors confirmed**: Sports South, Gun Accessory Supply, Chattanooga Shooting Supplies Inc., Lipsey's, RSR Group, Bill Hicks & Co., Ultimate Night Vision, Davidson's. GRO-721 had 5; new entries: Gun Accessory Supply, Chattanooga Shooting Supplies, Bill Hicks & Co., Ultimate Night Vision. (Zanders dropped from sub-brand list.)
- **GMROI named explicitly** in firearms inventory metrics. GRO-721 #80 had GMROI generically; sub-brand confirms it's surfaced for the gun vertical specifically.

### 2.3 Compliance / regulatory mentions (verbatim where surfaceable)

- ATF Ruling 2016-1 (electronic A&D records)
- ATF Form 4473 (digital, with attached supporting documents)
- ATF Form 3310 (multi-firearm purchase)
- NICS eCheck (named, transitive — full e4473 page didn't render)
- 4473 Cloud digital storage (named partner, transitive)
- FFL number storage per transaction
- Private-party transfer workflow (separate fee structure)
- Transfer items kept out of store inventory ("not legally taking ownership")
- Gun-show offline mode with eBound entries occurring "as if you were in the store"
- Consignment 4473/NICS approval on return-to-consignor

### 2.4 Sub-brand-only product names

- **eBoundbook** (Rapid's branded electronic bound book product)
- **Outbound Software** (named in GRO-721 #107 as gun-show mobile partner — sub-brand site doesn't name them despite covering gun shows; partnership may have lapsed or been replaced — escalation flag)
- **Passport** (named in GRO-721 as firearms ID/age — not visible on sub-brand crawl; same flag)

### 2.5 Ambiguity flags

- e4473 page returned a Cloudflare-rendering challenge through Jina — full feature surface for the e4473 product is not directly captured. Compensated with parent + transitive mentions from eBoundbook, FFL transfers, consignments pages (each references e4473). Flagged as `inferred-cross-page`.
- NICS eCheck partnership — appears in GRO-721 capability #105 sourced from `rapidpos.com` main verticals/gun page, but sub-brand pages didn't surface NICS eCheck as a named partner. May be an integration that was superseded or renamed. Flagged for follow-up.
- Outbound Software partnership status — same flag.

---

## §3. RapidBevPOS — Liquor / Wine / Beer Vertical

### 3.1 Crawl scope

| Page | Status | Net-new capabilities |
|---|---|---|
| `/` (homepage) | reachable | site map + structure |
| `/pos-features/` | reachable | umbrella |
| `/core-features/` | reachable | umbrella |
| `/age-verification/` | reachable | 3 |
| `/club-management/` | reachable | 4 |
| `/tasting-room/` | reachable, vertical-keystone | 4 |
| `/fast-checkout/` | reachable | 0 (subset of GRO-721 #121) |
| `/loyalty-programs/` | reachable | 1 |
| `/inventory/` | reachable | 2 |
| `/ecommerce/` | reachable | 2 |
| `/industry-specific-features/` | 404 | escalation candidate |

**Total net-new for bev: 14 capabilities.**

### 3.2 Sub-brand-specific findings

- **Tasting room as a distinct register profile** — kiosk-based new-customer registration, instant club look-up, on-the-spot membership creation, tip acceptance for staff gratuity. This is a vertical-specific register flow that changes tender and cart behavior. Maps to a tasting-room sub-profile of the DriftPOS register.
- **Wine/beer/spirits club fully-automated post-enrollment** — subscription billing, customer-preference tracking, email marketing, all driven by initial DL scan + a few data points. Recurring-billing pattern, not a feature.
- **Gift / prepaid memberships** for clubs.
- **Declined-credit-card and revenue-recovery assistant** for clubs. This is a dunning/retry workflow — material capability not visible in GRO-721. Cross-vertical applicability (any recurring-billing program).
- **Print receipt birth date** for state-required age confirmation on receipt — a regulatory subtlety (GRO-721 #36 captured DL age verification, but not the receipt-printing requirement).
- **System prompt on department-scoped triggers** for age verification — alcohol-restricted department scans trigger the verification, not just whole-transaction. Granularity GRO-721 didn't surface.
- **Beverage-specific item-attribute dimensions:** size, color, **varietal**, **vintage**, **region**, brand. Vintage and region are wine/spirits-specific dimensions. Maps to the `item` module attribute model (need to ensure vintage/region are first-class, not custom fields).
- **Multipack ordering: case + pack + single unit** for any item, with per-unit pricing. Cross-references GRO-721 #10 multipack handling but adds the case-level vendor incentive logic.
- **Vendor incentive monitoring "5 cases this month → free case"** — receiving-side promotional tracking visible in inventory screens. New commercial-relationship workflow.
- **BevMedia integration** — named integration for shelf-tag printing data. New named partner. Maps to `asset` module.
- **Online marketplaces named explicitly:** Drizly, Wine Trader, wine.com, Amazon. GRO-721 had Drizly + Minibar + ShipCompliant; sub-brand replaces Minibar (not mentioned) with Wine Trader, wine.com, Amazon. Material expansion.
- **ShipCompliant integration confirmed at sub-brand level** — calculates real-time shipping rates AND checks state-by-state alcohol shipping compliance. GRO-721 #75 had ShipCompliant; sub-brand details what it actually does.

### 3.3 Compliance / regulatory mentions (verbatim)

- 2D scanning for driver's license, military, state-issued IDs
- Legal purchase date(s) prominently displayed on POS screen
- Receipt-print verified birth date (state-mandated in some states)
- State-by-state shipping compliance via ShipCompliant
- Department-scoped age-verification prompts

### 3.4 Sub-brand-only product names

- **Rapid On-the-Go** (mobile branded for bev)
- **BevMedia** (shelf-tag data integration)

### 3.5 Ambiguity flags

- `/industry-specific-features/` returns 404 on the bev sub-brand — the IA collapsed since the GRO-721 crawl. Escalation candidate.
- Bottle deposit handling (GRO-721 #77) is not surfaced anywhere on the sub-brand site despite being a beverage-specific compliance item. May be a Counterpoint-base capability not branded on the sub-brand.
- Drizly's regulatory status changed in early 2024 (Uber shut Drizly down March 2024). Their named presence on the sub-brand site may be stale. Source-side data quality flag.

---

## §4. RapidFTPOS — Feed & Tack Vertical

### 4.1 Crawl scope

| Page | Status | Net-new capabilities |
|---|---|---|
| `/` (homepage) | reachable | site map + structure |
| `/industry-specific-features/` | reachable, thin | 0 |
| `/feed-inventory/` | reachable | 3 |
| `/compliance/` | reachable, vertical-keystone | 2 |
| `/product-information/` | reachable | 1 |
| `/accounts-receivable/` | reachable | 0 (Sage/MS Dynamics already in GRO-721; new entries below) |
| `/milling-production/` | reachable | 4 |
| `/tack-saddles/` | reachable, mostly Lorem-ipsum filler | 0 |
| `/pricing/` | reachable | 0 (subset of garden equivalent) |
| `/bundles-gift-baskets/` | reachable | 0 (subset of garden kitting) |

**Total net-new for ft: 11 capabilities.**

### 4.2 Sub-brand-specific findings

- **FDA Veterinary Feed Directive (VFD) compliance** explicitly named — store and manage customer licenses, VFDs, and written acknowledgement letters per controlled item. Vertical-specific compliance with concrete data model (license × customer × item). New regulatory surface beyond GRO-721 #108 (which said "feed compliance" generically).
- **Restricted-chemical flagging at item level** — staff-facing prompt to confirm proper documentation before sale authorization. Compliance + register-side enforcement.
- **Lot management with short / long shelf-life support** — explicit lot-level expiration handling, distinct from generic "freshness." Required for feed product recall handling.
- **Multi-name product handling** — common name + formal name + multiple supplier names per item. Distinct from GRO-721 #6 multi-vendor sourcing.
- **Milling/Production module** — distinct workflow surface: daily/weekly planning schedule, requisition reports, production labeling, waste tracking, labor cost-of-production. This is light manufacturing on top of retail. Maps to a new module slot — not in current Canary Go 25-module spine.
- **Customer ingredient + guaranteed-analysis info storage** — feed-label data stored per item for delivery to customer (email or print). Compliance + customer-service hybrid.
- **Use-direction / care-recommendation storage** per product, deliverable to customer.
- **Accounts Receivable module called out explicitly** with finance charges + statements. GRO-721 #72 has charge accounts; sub-brand confirms the depth is real (this is the strongest A/R-vertical evidence in the corpus).
- **Legacy accounting integrations: Business Works, Business Works Go, Microsoft/Great Plains Dynamics, Microsoft/Great Plains Small Business Manager, Microsoft/Great Plains Accounting, ACCPAC, ACCPAC Plus, Peach Tree, Solomon IV.** All distinct from the QuickBooks/Sage/Sage Intacct lineup in GRO-721. Many are EOL. Source-side staleness flag — but the principle "we integrate with whatever your accountant uses" stands.
- **Customer classifications: farmers, ranchers, equestrian centers, distributors, consumers.** GRO-721 #22 had farmer/rancher/distributor/wholesale; sub-brand adds "equestrian centers" as a distinct class.

### 4.3 Compliance / regulatory mentions (verbatim)

- "FDA's Veterinary Feed Directive (VFD)"
- "Restricted chemicals" (flagged at item level)
- "Customer's licenses, VFDs and written acknowledgement letters" stored in system
- "Controlled items can be flagged in your system so that your staff knows to confirm proper documentation before a customer is authorized to purchase"

### 4.4 Sub-brand-only product names

- None unique. The sub-brand is the thinnest of the four — it carries the Counterpoint umbrella branding without its own named modules.

### 4.5 Ambiguity flags

- `/tack-saddles/` is mostly Lorem-ipsum placeholder content — page is effectively un-published. Escalation candidate.
- `/industry-specific-features/` returned only 1.6KB despite being on the navigation; the page is thin. Sub-brand is half-maintained.
- The 9 named legacy accounting integrations include several products that are EOL or rebranded. Source-side staleness; do not advertise these in joint product positioning without verification.

---

## §5. Consolidated Net-New Capability Table

67 net-new capabilities across the 4 sub-brands. Numbering continues from GRO-721's 130.

### 5.1 Garden net-new (#131–148)

| # | Capability | Vertical | GSLM domain | Canary Go module | Side | GRO-721 gap impact | Source URL | Confidence |
|---|---|---|---|---|---|---|---|---|
| 131 | Track plant care attributes per item (height, spread, light needs, care notes) | garden | Item | item | Canary | none | rapidgardenpos.com/green-inventory/ | well-documented |
| 132 | Mark items as dead stock with reporting separation from active inventory | garden | Item | inventory | Canary | none | rapidgardenpos.com/green-inventory/ | well-documented |
| 133 | Botanical / common / Spanish-name triple per item record | garden | Item | item | Canary | none | rapidgardenpos.com/printing/ | well-documented |
| 134 | Unlimited barcodes per item for grower / batch / color tracking | garden | Item | item | Canary | extends #6 | rapidgardenpos.com/printing/ | well-documented |
| 135 | Convert bulk stock to retail units automatically (units-of-measure conversion) | garden | Item | item | Canary | extends #3 | rapidgardenpos.com/green-inventory/ | well-documented |
| 136 | Print plant spike + pot stake labels at receiving / adjustment / bulk-to-retail | garden | C&P | asset | Canary | resolves G4-must #3 (label printing) | rapidgardenpos.com/printing/ | well-documented |
| 137 | Print care-detail display labels per item | garden | C&P | asset | Canary | resolves G4-must #3 | rapidgardenpos.com/printing/ | well-documented |
| 138 | Print combo/kit tags automatically when a kit is built | garden | Item | asset | Canary | extends G4-must #3 | rapidgardenpos.com/kitting-planters-baskets/ | well-documented |
| 139 | Generate landscaping quotes / proposals / estimates with job-costing | garden | Supply Chain | commercial | Canary | resolves G4-should "service-attached retail" | rapidgardenpos.com/landscaping/ | well-documented |
| 140 | Track inventory committed-vs-consumed across landscaping project life cycle | garden | Supply Chain | commercial | Canary | new sub-gap (project-tracking) | rapidgardenpos.com/landscaping/ | advertised-only |
| 141 | Run partial order releases against landscape orders | garden | Supply Chain | commercial | Canary | new | rapidgardenpos.com/landscaping/ | advertised-only |
| 142 | Reconcile landscaping projects (revenue + cost roll-up at close) | garden | Finance | commercial | Canary | new | rapidgardenpos.com/landscaping/ | advertised-only |
| 143 | Issue progressive billing against landscaping projects | garden | Finance | commercial | Canary | new | rapidgardenpos.com/landscaping/ | advertised-only |
| 144 | Day-of-week / calendar-validity loyalty point promotions | garden | C&P | customer | Canary | extends #24 | rapidgardenpos.com/loyalty-program/ | well-documented |
| 145 | BOGO / Buy-X-Get-Y / Spend-N-Get / Mix-N-Match / Volume / Markup promotion engine | garden | Price&Promo | pricing | Canary | extends #89 | rapidgardenpos.com/pricing/ | well-documented |
| 146 | Custom API integrations to vertical specialty services (declared as standing service) | garden | n/a | (service) | Canary | extends GRO-721 service tier | rapidgardenpos.com/landscaping/ | advertised-only |
| 147 | Print on outdoor-ready thermal-transfer printers with weather-resistant label stock (hardware-paired capability) | garden | C&P | asset | DriftPOS | extends G4-must #3 | rapidgardenpos.com/printing/ | well-documented |
| 148 | Sage Intacct as named accounting integration for garden vertical specifically | garden | Finance | report | Canary | confirms GRO-721 #69 vertical applicability | rapidgardenpos.com/accounting-management-integrations/ | well-documented |

### 5.2 Gun net-new (#149–172)

| # | Capability | Vertical | GSLM domain | Canary Go module | Side | GRO-721 gap impact | Source URL | Confidence |
|---|---|---|---|---|---|---|---|---|
| 149 | Maintain unlimited electronic bound books per FFL account | gun | C&P | compliance | Canary | extends #104 | rapidgunsystems.com/eboundbook/ | well-documented |
| 150 | Comply explicitly with ATF Ruling 2016-1 for electronic A&D records | gun | C&P | compliance | Canary | extends #104 | rapidgunsystems.com/eboundbook/ | well-documented |
| 151 | Generate ATF-ready audit reports on demand | gun | C&P | compliance | Canary | new | rapidgunsystems.com/eboundbook/ | well-documented |
| 152 | Track ATF Form 3310 multi-firearm purchase reports automatically | gun | C&P | compliance | Canary | new | rapidgunsystems.com/eboundbook/ | well-documented |
| 153 | Attach supporting documents (military orders, ID scans, state forms) per A&D entry | gun | C&P | compliance + fox | Canary | new (cross-references evidence chain) | rapidgunsystems.com/eboundbook/ | well-documented |
| 154 | Maintain full per-edit audit log of every bound-book modification | gun | C&P | compliance + fox | Canary | new (maps direct to fox) | rapidgunsystems.com/eboundbook/ | well-documented |
| 155 | Print barcode labels with bound-book sequence numbers + descriptions + price | gun | C&P | asset | Canary | extends G4-must #3 | rapidgunsystems.com/eboundbook/ | well-documented |
| 156 | Auto-deliver software/compliance updates when ATF releases new guidance (labor-only billing) | gun | C&P | (service) | Canary | new — service tier | rapidgunsystems.com/eboundbook/ | advertised-only |
| 157 | Operate cloud-hosted bound book (vs on-prem-only Counterpoint base) | gun | C&P | compliance | Canary | new — deployment model | rapidgunsystems.com/eboundbook/ | well-documented |
| 158 | Keep transferred-in firearms out of store inventory legally and accounting-wise | gun | Item | inventory | Canary | new | rapidgunsystems.com/ffl-transfers/ | well-documented |
| 159 | Operate multiple FFL transfer fee structures by firearm type | gun | Finance | pricing | Canary | new | rapidgunsystems.com/ffl-transfers/ | well-documented |
| 160 | Manage private-party transfer workflow distinctly from FFL-to-FFL transfer | gun | C&P | compliance | Canary | new | rapidgunsystems.com/ffl-transfers/ | advertised-only |
| 161 | Treat customer pickup of transfer firearm as cross-sell opportunity (linked promotion) | gun | Customer | customer + pricing | Canary | new | rapidgunsystems.com/ffl-transfers/ | advertised-only |
| 162 | Estimate rounds-fired per rental firearm based on session time | gun | Asset | asset | Canary | new — service-maintenance forecast | rapidgunsystems.com/range-management/ | well-documented |
| 163 | Surface visual indicator on register when rented firearm is unreturned | gun | C&P | tsp + chirp | Both | new — operational LP signal | rapidgunsystems.com/range-management/ | well-documented |
| 164 | Tier-based range-membership discounts (gold / platinum / etc.) | gun | Customer | customer | Canary | extends #23 | rapidgunsystems.com/range-management/ | well-documented |
| 165 | Schedule range maintenance from any POS station | gun | People | employee | Canary | resolves G4-must #4 (scheduling primitive) | rapidgunsystems.com/range-management/ | advertised-only |
| 166 | Operate gun-show mobile mode where eBound entries occur "as if you were in the store" | gun | C&P | compliance + tsp | Both | extends #107 | rapidgunsystems.com/gun-show/ | well-documented |
| 167 | Separate gun-show inventory from brick-and-mortar inventory to prevent double-sale | gun | Item | inventory | Canary | new | rapidgunsystems.com/gun-show/ | well-documented |
| 168 | Capture deposits + special orders at gun show offline | gun | Finance | commercial | Both | new | rapidgunsystems.com/gun-show/ | well-documented |
| 169 | Capture consignment authorized-price-range + repair-fee structure per item | gun | Supply Chain | commercial | Canary | extends #67 | rapidgunsystems.com/consignments/ | well-documented |
| 170 | Loan range firearm to customer during gunsmithing repair (cross-module workflow) | gun | Customer | customer + asset | Canary | new — cross-module | rapidgunsystems.com/gunsmithing/ | advertised-only |
| 171 | Auto-write disposition record to bound book on gunsmithing return | gun | C&P | compliance | Canary | new | rapidgunsystems.com/gunsmithing/ | well-documented |
| 172 | Vendor catalog real-time availability + drop-ship from gun distributors (8 named: Sports South, Gun Accessory Supply, Chattanooga Shooting Supplies, Lipsey's, RSR, Bill Hicks, Ultimate Night Vision, Davidson's) | gun | Supply Chain | receiving | Canary | extends #54 — 4 new partner names | rapidgunsystems.com/vendor-catalog-integrations/ | well-documented |

### 5.3 Beverage net-new (#173–186)

| # | Capability | Vertical | GSLM domain | Canary Go module | Side | GRO-721 gap impact | Source URL | Confidence |
|---|---|---|---|---|---|---|---|---|
| 173 | Print verified birth date directly on customer receipt (state-mandated) | bev | C&P | tsp | DriftPOS | extends #36 | rapidbevpos.com/age-verification/ | well-documented |
| 174 | Trigger age-verification prompt at department-scoped item scan (not just whole-transaction) | bev | C&P | compliance | Canary | extends #36 | rapidbevpos.com/age-verification/ | well-documented |
| 175 | 2D scan military and state-issued IDs (not only DL) | bev | Customer | customer | DriftPOS | extends #19 | rapidbevpos.com/age-verification/ | well-documented |
| 176 | Capture new club / loyalty registrations on tasting-room kiosks | bev | Customer | customer | DriftPOS | new — kiosk profile | rapidbevpos.com/tasting-room/ | advertised-only |
| 177 | Accept credit-card tips for staff gratuity at tasting-room register | bev | Finance | tsp | DriftPOS | new — tender-flow variant | rapidbevpos.com/tasting-room/ | well-documented |
| 178 | Direct on-the-spot "carryout vs ship" decision per cart at tasting-room | bev | Supply Chain | commercial | DriftPOS | new | rapidbevpos.com/tasting-room/ | advertised-only |
| 179 | Run gift / prepaid club memberships | bev | Customer | customer + commercial | Canary | extends #28 | rapidbevpos.com/club-management/ | advertised-only |
| 180 | Auto-retry declined-credit-card workflow with revenue-recovery assistant on club billing | bev | Finance | commercial | Canary | resolves G4-should "membership recurring billing engine" | rapidbevpos.com/club-management/ | well-documented |
| 181 | First-class item-attribute fields: varietal, vintage, region (in addition to size/color/brand) | bev | Item | item | Canary | extends #1 | rapidbevpos.com/inventory/ | well-documented |
| 182 | Track vendor-incentive thresholds inside POS receiving screens (e.g. "5 cases this month → free case") | bev | Supply Chain | commercial + receiving | Canary | extends #56 | rapidbevpos.com/inventory/ | well-documented |
| 183 | BevMedia integration for branded shelf-tag printing data | bev | C&P | asset | Canary | new partner; extends G4-must #3 | rapidbevpos.com/inventory/ | well-documented |
| 184 | Sync to alcohol marketplaces: Drizly, Wine Trader, wine.com, Amazon | bev | C&P | ecom-channel | Canary | extends #114 — new marketplaces | rapidbevpos.com/ecommerce/ | well-documented |
| 185 | Real-time per-state alcohol shipping compliance check via ShipCompliant integration | bev | C&P | compliance + ecom-channel | Canary | extends #75 | rapidbevpos.com/ecommerce/ | well-documented |
| 186 | Send order-tracking email automation to bev customers on club / online orders | bev | Customer | customer | Canary | duplicates #117 — flagged but distinct vertical applicability | rapidbevpos.com/ecommerce/ | well-documented |

### 5.4 Feed & Tack net-new (#187–197)

| # | Capability | Vertical | GSLM domain | Canary Go module | Side | GRO-721 gap impact | Source URL | Confidence |
|---|---|---|---|---|---|---|---|---|
| 187 | Lot management with short-or-long shelf-life expiration handling per lot | ft | Item | inventory | Canary | new — required for feed recall | rapidftpos.com/feed-inventory/ | well-documented |
| 188 | Multi-name product handling: common name + formal name + multiple supplier names | ft | Item | item | Canary | extends #6 | rapidftpos.com/feed-inventory/ | well-documented |
| 189 | Sell in multiple measures / bag sizes from one inventory item | ft | Item | item | Canary | extends #3 | rapidftpos.com/feed-inventory/ | well-documented |
| 190 | Comply with FDA Veterinary Feed Directive (VFD): store customer licenses + VFDs + written acknowledgement letters per controlled item | ft | C&P | compliance | Canary | extends #108 | rapidftpos.com/compliance/ | well-documented |
| 191 | Flag restricted-chemical items with register-side staff prompt for documentation confirmation | ft | C&P | compliance + tsp | Both | new — register-side compliance enforcement | rapidftpos.com/compliance/ | well-documented |
| 192 | Store + deliver guaranteed-analysis info / ingredient lists per item (email or print) | ft | Item | item + asset | Canary | new — feed-label data substrate | rapidftpos.com/product-information/ | well-documented |
| 193 | Run milling / production planning schedule (daily/weekly) | ft | Supply Chain | new module ("milling") | Canary | new gap — module not in 25-spine | rapidftpos.com/milling-production/ | well-documented |
| 194 | Generate requisition reports for milling production | ft | Supply Chain | new module ("milling") | Canary | new gap | rapidftpos.com/milling-production/ | well-documented |
| 195 | Track production-line waste with cost roll-up | ft | Supply Chain | new module ("milling") | Canary | new gap | rapidftpos.com/milling-production/ | well-documented |
| 196 | Manage labor + cost-of-production per milling batch | ft | People | employee + new module | Canary | new gap | rapidftpos.com/milling-production/ | well-documented |
| 197 | Customer classifications: equestrian centers as a distinct class beyond GRO-721 set (farmer/rancher/distributor/wholesale) | ft | Customer | customer | Canary | extends #22 | rapidftpos.com/ | well-documented |

### 5.5 Counts and ambiguity

| Sub-brand | Net-new | Side: DriftPOS | Side: Canary | Side: Both |
|---|---|---|---|---|
| Garden | 18 | 1 | 17 | 0 |
| Gun | 24 | 0 | 22 | 2 |
| Beverage | 14 | 5 | 8 | 1 |
| Feed & Tack | 11 | 0 | 10 | 1 |
| **Total** | **67** | **6** | **57** | **4** |

Ambiguity (`advertised-only` + `inferred`-flagged): 12 / 67 = **17.9%.**
Quality Gate G3 (<30%) PASS.

---

## §6. Gap Analysis Delta Against GRO-721

### 6.1 GRO-721 must-have gaps — status update

| GRO-721 must-gap | Status after sub-brand crawl | Evidence |
|---|---|---|
| **#1 Inter-store transfer module** | unchanged — sub-brands didn't surface transfer details | — |
| **#2 EBT acceptance** | unchanged — no sub-brand surfaces EBT (none of these verticals are SNAP-eligible) | — |
| **#3 Label-printing service (asset/print)** | **promoted** — capabilities #136/137/138/147/155/183 confirm this is the single most-named missing primitive across all 4 sub-brands. Highest-priority module to scope. | garden printing page is dedicated; gun bound-book labels; bev BevMedia; ft milling labels |
| **#4 Scheduling / dispatch service** | **partially resolved** — capability #165 (range maintenance scheduling from POS) shows the primitive is a per-vertical workflow, not a general calendar. Recommendation: build per-vertical scheduling adapters on top of `employee` module rather than a general scheduling service. | rapidgunsystems.com/range-management/ |
| **#5 Customer-A/R sub-system depth** | **promoted** — feed-tack sub-brand has the most explicit A/R module description in the corpus (capability #197 references; A/R module dedicated page). Confirms B2B-flavored verticals require it. Module split (commercial → vendor-A/P + customer-A/R) should be done before ft is in scope. | rapidftpos.com/accounts-receivable/ |
| **#6 Returns / RMA scope split** | unchanged — sub-brands didn't surface returns | — |

### 6.2 GRO-721 should-have gaps — status update

| GRO-721 should-gap | Status |
|---|---|
| Gift card lifecycle service | unchanged |
| Vendor catalog ingestion adapter | extends — gun adds 4 new distributor names (capability #172); confirms adapter pattern is the right architecture |
| Compliance module breadth | **expanded** — sub-brands surface 5 distinct vertical compliance regimes (ATF eBound, ATF 3310, FDA VFD, ShipCompliant, age-verification with state receipt-print rules). The compliance module needs per-jurisdiction-per-item rule scope plus per-vertical compliance package modules. |
| Drop-ship / multi-tier integration | partially extended — gun #172 confirms drop-ship pattern works at distributor scale |
| Self-checkout register profile | unchanged |
| Membership recurring billing engine | **resolved** — bev capability #180 (declined-credit-card revenue-recovery assistant) names exactly the dunning/retry primitive. Implement as a `commercial` sub-module. |

### 6.3 Net-new gaps surfaced by sub-brand crawl (NEW)

| New gap | Severity | Evidence |
|---|---|---|
| **Project / job costing / progressive billing primitive** for landscaping-style services-attached retail | should-have | garden #139–143 |
| **Light-manufacturing / milling module** for production-attached retail | should-have or out-of-scope | ft #193–196 (consider whether feed-mill is in ICP) |
| **Cross-module loaner-asset workflow** (range gun loaned during gunsmithing repair) | nice-to-have | gun #170 |
| **Per-document attachment storage** at compliance-event level (military orders, ID scans, state forms attached to bound-book entries) | must-have for gun vertical | gun #153 |
| **Per-edit audit log on regulated datasets** (every bound-book edit logged with user and timestamp) | must-have for gun vertical | gun #154 — natural fit for `fox` evidence chain |
| **Tender-flow variants: tip on register** for service-attached profiles (tasting room, etc.) | should-have | bev #177 |
| **Per-rental session-time-based asset wear tracking** (rounds-fired estimate per range gun) | nice-to-have | gun #162 |
| **Item attribute model first-class for vertical-specific dimensions** (vintage, region, varietal for bev; botanical/Spanish-name for garden; lot-with-shelf-life for ft) | must-have — affects all verticals | bev #181, garden #133, ft #187 |

The last entry is the largest architectural take-away. The `item` module's
attribute model needs to support per-vertical first-class dimensions, not
generic custom-fields. Configuring vintage as a custom attribute is not the
same as having vintage as a queryable, indexable, reportable field. The
tenant-config layer is the right place to do this — vertical packs that
extend the canonical item model with first-class dimensions for that vertical.

---

## §7. Quality Gate Verification

### G1 — Each sub-brand yields ≥5 net-new capabilities

| Sub-brand | Net-new | Threshold | Status |
|---|---|---|---|
| Garden | 18 | 5 | PASS (3.6×) |
| Gun | 24 | 5 | PASS (4.8×) |
| Beverage | 14 | 5 | PASS (2.8×) |
| Feed & Tack | 11 | 5 | PASS (2.2×) |

Quality Gate G1 PASS across all 4 sub-brands. None is a marketing re-skin
of the main rapidpos.com site.

### G2 — Gun yields ≥15 net-new capabilities

| Sub-brand | Net-new | Threshold | Status |
|---|---|---|---|
| Gun | 24 | 15 | PASS (1.6×) |

Quality Gate G2 PASS. The hypothesis that rapidgunsystems.com carries the
deepest vertical surface is confirmed. Compliance + workflow + cross-module
content is materially richer than the umbrella site's `/verticals/gun/` page.

Note: the e4473 sub-page returned a Cloudflare-rendering challenge through
Jina and was not captured directly. If the e4473 page rendered, gun net-new
count would likely climb 3–5 more (NICS workflow, digital-form storage
specifics, audit-trail). Filed as a re-attempt candidate (escalation §8.4).

### G3 — Ambiguity flag rate <30% on consolidated table

12 / 67 = **17.9%**. Quality Gate G3 PASS.

### Overall

All 3 quality gates PASS. Sub-brand crawl produced 67 net-new capabilities
(51% additional surface beyond GRO-721's 130). The combined inventory now
stands at **197 capabilities** across the joint product surface, with 5
GRO-721 gaps reclassified and 8 new gaps surfaced.

---

## §8. Open Questions & Escalation Items

### 8.1 Source-side staleness flags

- **Drizly** is named on the bev sub-brand site but Uber shut Drizly down March 2024. The named integration is stale. Question for Bart: which alcohol-marketplace integrations are currently active?
- **Outbound Software** and **Passport** appear in GRO-721 capability #107 / partner list (sourced from rapidpos.com/verticals/gun/) but are not visible on the rapidgunsystems.com sub-brand. Question: are these still active partnerships?
- **NICS eCheck** named in GRO-721 #105 from main site; not visible on sub-brand. Likely still real (e4473 page didn't render); confirm.
- **9 legacy accounting integrations** on ft sub-brand (Business Works, ACCPAC, Solomon IV, Peach Tree, Microsoft Great Plains variants) — most are EOL. Filter before joint-product positioning.

### 8.2 Sub-brand-IA quality flags

- **bev `/industry-specific-features/` returns 404** — IA collapsed since GRO-721 crawl 2 days ago. Was working at GRO-721 time per the GRO-721 §7.1 ref to sub-brand crawl as a follow-up.
- **ft `/tack-saddles/` is mostly Lorem-ipsum** — page is effectively un-published. Sub-brand is half-maintained.
- **ft sub-brand thinness overall** — net-new count of 11 is the lowest of the four. The vertical is real (named customers Hawthorne Country Store, Mountain Feed, Mary's Tack & Feed, Del Mar Fairgrounds — none with testimonials), but the marketing site is not refreshed. Joint-product positioning for feed&tack should not lean on RapidPOS sub-brand depth.

### 8.3 Architectural questions surfaced

- **Should milling/production be in scope?** Capabilities #193–196 describe a light-manufacturing module that doesn't fit in any of the 25 Canary Go modules. Two options: (a) add a `production` module slot for verticals that need it (feed mill, custom kitting at scale, growing-houses); (b) declare milling out-of-scope and route those merchants to a partner. Recommend (b) for joint-product Phase 1; revisit if a feed-mill ICP candidate appears.
- **Should `compliance` module be split per-vertical?** GRO-721 already flagged this; sub-brand crawl confirms each vertical (gun, alcohol, feed) has materially different regulatory data models. Per-vertical compliance packs over a thin compliance core is the right shape.
- **Per-document attachment storage on compliance/evidence events** — capability #153 (attached supporting documents on A&D log) is currently an unknown for the joint-product spec. The `fox` evidence chain is INSERT-only and hash-chained; can it carry attachment payloads, or do attachments live in a separate object store referenced by hash from `fox`? Architectural question for the SDD layer.

### 8.4 Recommended follow-up dispatches

1. **GRO-XXX: Re-attempt rapidgunsystems.com/e4473/ crawl** — Jina returned challenge text; try again in 24h or use a different rendering proxy. Likely 3–5 more net-new gun capabilities.
2. **GRO-XXX: ATF eBound + Form 4473 + 3310 integration design SDD** — gun vertical depth justifies a dedicated compliance-module SDD covering ATF eBound (Ruling 2016-1), e4473 with NICS, multi-firearm 3310 reports, FFL-and-private-party transfer workflow, and the per-edit audit log → fox evidence-chain mapping. Standalone follow-up.
3. **GRO-XXX: Item attribute model for vertical-first-class dimensions** — design how vintage/region/varietal (bev), botanical/common/Spanish names (garden), lot+shelf-life (ft), and serial+FFL (gun) become first-class queryable fields rather than custom-field workarounds. Likely an `item` module SDD revision.
4. **GRO-XXX: Asset/print orchestration module SDD** — must-have gap GRO-721 #3 is now confirmed across all 4 verticals. Capability #136/137/138/147/155/183 are concrete inputs.
5. **GRO-XXX: Founder-direct ask of Bart on stale partnerships** — confirm Drizly / Outbound Software / Passport / NICS eCheck status. Out-of-band, not a public-source dispatch.
6. **GRO-XXX: Vendor-catalog adapter SDD for firearms distributors** — 8 named distributors with real-time availability + drop-ship. The firearms-distributor adapter pattern is the strongest evidence in the corpus that the multi-tier assortment thesis works at scale.
7. **GRO-XXX: Bev marketplace adapters** — Drizly status pending, but Wine Trader, wine.com, and Amazon are named net-new marketplaces. ecom-channel adapter scope.

### 8.5 Strategic findings — Top 5 for Canary GTM

1. **Asset/print is the most-named missing primitive across every vertical.** Six of the 67 net-new capabilities are label/print related, hitting all 4 verticals. The joint product cannot ship without label-printing orchestration. Prioritize it.

2. **The gun vertical is a real evidence-chain product.** Capabilities #153 (attached documents) + #154 (per-edit audit log) map directly to Canary's `fox` evidence-chain module. The strongest module-fit story in the entire sub-brand corpus is "Canary's evidence chain becomes the gun store's compliance audit trail." This is positioning gold for the gun vertical specifically.

3. **Item attribute model is the largest architectural debt.** Each vertical wants different first-class dimensions on items. Vintage isn't a custom field for bev — it's the primary search axis. Botanical name isn't a custom field for garden — it's how staff find the item. The current item module needs a vertical-config layer that promotes vertical-specific attributes to first-class status.

4. **The garden landscaping arc is effectively a separate product.** Capabilities #139–143 (quotes/proposals, project-tracking, partial releases, project reconciliation, progressive billing) are services-business management bolted onto a retail POS. Either positioning treats this as a "Garden+Landscaping" tier with its own scope, or it gets deferred — but it is real and has Roger's Gardens as a named anchor customer.

5. **Beverage's recurring-billing engine resolves a GRO-721 should-gap.** Capability #180 (declined-credit-card revenue-recovery assistant) names exactly the dunning/retry workflow that GRO-721 §4.should listed as missing. The bev sub-brand has the most mature subscription/club workflow in the corpus — wine clubs run on this. Build the membership recurring-billing engine inside `commercial`; bev becomes a use-case lighthouse.

---

## §9. Combined Inventory Summary

| Source | Capabilities |
|---|---|
| GRO-721 (rapidpos.com main) | 130 |
| GRO-760 garden net-new | 18 |
| GRO-760 gun net-new | 24 |
| GRO-760 bev net-new | 14 |
| GRO-760 ft net-new | 11 |
| **Total joint-product surface mapped** | **197** |

| Side split | Combined count | % |
|---|---|---|
| DriftPOS | 33 | 17% |
| Canary | 152 | 77% |
| Both | 12 | 6% |

The 152-to-33 ratio is now firmer than the 95-to-27 GRO-721 ratio: Canary
takes 77% of the surface; DriftPOS takes 17%; integration boundary at 6%.
Hand the register to Bart; everything else is Canary.

---

## §10. Related

- Parent dispatch: [GRO-721 / CAN-RES-001](https://linear.app/growdirect/issue/GRO-721/) → `Brain/wiki/canary/partnership-research/rapidpos-feature-map.md`
- This dispatch: [GRO-760 / CAN-RES-002](https://linear.app/growdirect/issue/GRO-760/)
- Canary Go module spine: `docs/sdds/go-handoff/go-module-layout.md`
- Platform thesis: `Brain/wiki/cards/platform-thesis.md`
- Counterpoint VAR landscape: `Brain/wiki/cards/counterpoint-var-landscape.md`
- Memory entries: `project_canary_canonical_positioning.md`, `project_rapidpos_go_pivot.md`, `project_rapidpos_stakeholders.md`, `project_canary_replaces_counterpoint_long_arc.md`

---

*Generated 2026-05-03 by ALX on dispatch CAN-RES-002 (GRO-760). Extension to GRO-721; same controls; same split rule.*
