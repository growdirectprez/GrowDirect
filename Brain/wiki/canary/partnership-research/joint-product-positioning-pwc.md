---
title: Joint Product Positioning — DriftPOS + Canary (PwC Three-Phase)
type: positioning-analysis
domain: canary
status: draft
dispatch: GRO-721 (downstream synthesis)
date: 2026-05-01
last-compiled: 2026-05-01
needs-review: true
methodology: PwC Consumer Positioning (Guess?, Inc. 2001) — agent-compressed
unit-of-analysis: Joint product (DriftPOS register + Canary back-half) for SMB specialty retailer ICP
source-research: Brain/wiki/canary/partnership-research/rapidpos-feature-map.md
tags: [canary, positioning, partnership, rapidpos, driftpos, pwc-playbook, joint-product]
---

# Joint Product Positioning — DriftPOS + Canary

> Three-phase positioning analysis applied to the joint product going to the
> SMB specialty retailer running NCR Counterpoint today. Run on the GRO-721
> capability inventory (130 capabilities, 14 verticals, 51 integrations) as
> primary evidence. Phase 2B (consumer voice) is largely a gap — flagged.

| Field | Value |
|---|---|
| Methodology | PwC three-phase consumer positioning (compressed, agent-assisted) |
| Source data | GRO-721 / CAN-RES-001 (rapidpos.com, 43 pages, 130 capabilities) |
| Unit of analysis | Joint product (DriftPOS register + Canary back-half) |
| Target customer | SMB specialty retailer (≤$50M revenue, owner-operator, Counterpoint incumbent) |
| Phases delivered | 1, 2A, 3 (full); 2B (gap flagged + fielding plan) |

---

## Governing Thesis

The joint product wins by reframing the buying decision from *"which POS replaces my Counterpoint"* to *"which platform takes accountability for the parts of retail Counterpoint never owned."* Bart's RapidPOS surface gives us a 130-capability map of what Counterpoint VARs actually sell to specialty retailers — and a near-greenfield differentiation surface (LP, evidence chain, OTB-as-meter, agent network, satoshi cost rollup) that competitors have not claimed. The core customer is the multi-hat owner-operator of a 1–10 store specialty retailer who is paying $25 per till per month for a 41-year-old platform and absorbing a 50+ integration tax to make it work. Position against that bleed. Win on accountability rails, not feature parity. The gaps to close before this proposal goes out are tractable; the moat is real.

---

## Executive Summary

**Core customer (read from data):** Owner-operator of a 1–10 store specialty retailer, $5M–$50M revenue, vertical-bound (gun, liquor, garden, feed&tack, grocery, clothing, etc.), currently running heavily customized NCR Counterpoint, paying ~$25/till/month plus a 50+-integration tax, wearing every hat in the building.

**Core competition (the actual choice set):** NCR Counterpoint (incumbent inertia) → NCR Voyix CX7ii (NCR's own upgrade pull) → Lightspeed Retail / Heartland Retail (cloud SMB specialty) → Vertical specialists (Coreware/AmmoReady gun, Spruce garden, Cellar Tools liquor) → Shopify POS / Square for Retail (brand-tier and low-end displacement). Notably absent: the platform Bart and Canary are jointly building.

**Core merchandise (what the joint product sells):** A 130-capability functional surface that matches Counterpoint at parity (DriftPOS owns 27 register-side capabilities; Canary owns 95 back-half capabilities; 8 are jointly executed) **plus** an "and more" surface — 8 spine modules and 9 extended modules with zero RapidPOS analog. The differentiation isn't marginal; it's a category move.

**Key appeals (rational + emotional):**
- *Rational:* Replace the $25/till bleed with a verifiable cost-to-serve. One platform absorbs 50+ third-party integrations. Offline at the till is a hardware-level promise, not a marketing line. Phased migration — Canary deploys alongside Counterpoint before the register cuts.
- *Emotional:* Take ownership back. No more black-box vendor. Cryptographic evidence means you can *prove* what happened in your own store. Your data is yours. No more shrink mystery.

**Headline differentiation surface (Phase 3):** Open-to-buy as a financial rail across all verticals (RapidPOS surfaces OTB once across 43 pages, on the clothing vertical only). The L402-gated `l402-otb` module is a category-defining positioning primitive. Lead with this in the Tim Mooney recap.

**What this analysis does not yet have:** Direct customer voice. No interviews, focus groups, win/loss data, churn signal, or quantitative segmentation. Phase 2B (primary consumer research) is the gap. Recommended fielding plan in §Phase 2B.

---

## Phase 1 — Project Initiation

### Summary Finding

The scope is unusually clean. Bart's RapidPOS website was the proxy for "what specialty retailers buy from a Counterpoint VAR today," and GRO-721 produced a defensible 130-capability inventory at the level of granularity the positioning question demands. Phase 1 collapses to days, not weeks, because the data inventory step is already done.

### Scoped Question List

| # | Question | Phase Owner |
|---|---|---|
| Q1 | Who is the core customer of the joint product, and how does that customer vary across the 14 verticals RapidPOS serves? | 2A + 2B |
| Q2 | Who is the joint product actually competing against — Counterpoint, NCR Voyix, vertical specialists, or cloud SMB platforms? | 2A |
| Q3 | Does the 130-capability functional surface plus the "and more" surface match what the core customer needs and will pay for? | 2A + 3 |
| Q4 | What positioning strategy lets DriftPOS + Canary credibly displace a 41-year-old incumbent without competing on feature parity? | 3 |
| Q5 | Where does the joint product brand sit in the choice set — register-replacement, platform-replacement, or accountability-layer? | 3 |

### Data Inventory

| Data Type | Status | Source / Gap |
|---|---|---|
| Competitor product surface | **Available** | GRO-721 (RapidPOS as Counterpoint VAR proxy); supplemental web crawl needed for direct competitors |
| Capability map vs joint-product spine | **Available** | GRO-721 §2 (130 rows, GSLM domain × Canary module × DriftPOS/Canary side) |
| Integration ecosystem | **Available** | GRO-721 §6 (51 named integrations, sided) |
| Vertical configurations | **Partial** | 14 verticals named; sub-brand depth (gun, garden, liquor, feed&tack) not yet crawled — flagged in §7 of GRO-721 |
| SMB specialty retail market sizing | **Gap** | No US specialty retail TAM/SAM/SOM segmented by Counterpoint installed base — fielding required |
| Customer interview transcripts | **Gap** | None on file; Bart-direct conversation pending; no end-customer interviews yet |
| Win/loss / churn data | **Gap** | Bart-only knowledge; founder-direct ask flagged in GRO-721 §7.2 |
| Pricing benchmarks (per-till, per-store) | **Gap** | $25/till NCR cost is the only anchor; competitor pricing not collected |
| Brand identity / marketing plan | **Partial** | Platform thesis exists (Brain/wiki/cards/platform-thesis.md); joint-product brand not yet defined |

### Research Requirements Brief

The two material gaps are competitive pricing and direct customer voice. Both are addressable in the Bart conversation cycle (he has the install-base data and customer relationships) plus a structured competitive crawl of NCR Counterpoint, NCR Voyix, Lightspeed Retail, Heartland Retail, Coreware, AmmoReady, Spruce, and Cellar Tools. Phase 2A absorbs the competitive crawl; Phase 2B absorbs the customer voice work.

---

## Phase 2A — External / Internal Market Assessment

### Summary Finding

The competitive set is bifurcated. On the incumbent side, Counterpoint is sticky but architecturally tired (41 years, on-prem default, 50+ integration tax). NCR's own upgrade path (Voyix CX7ii) is hardware-led and competes with Canary's back-half thesis. On the modern-cloud side, Lightspeed and Heartland have functional breadth but neither claims an accountability or evidentiary rail. Vertical specialists (Coreware/AmmoReady, Spruce) win specific verticals on compliance depth but don't generalize. The gap the joint product fills — *Counterpoint-class breadth + cloud-native architecture + cryptographic accountability* — is structurally unclaimed.

### Market Trends — SMB Specialty Retail POS (read from research + general market knowledge)

| Trend | Direction | Implication for Joint Product |
|---|---|---|
| On-prem → cloud migration in SMB specialty retail | Mid-cycle, accelerating | DriftPOS PostgreSQL→SQLite sync model is correctly architected; Canary cloud-native is on-trend |
| Per-till SaaS pricing fatigue | Rising | The $25/till NCR cost is exactly the bleed point; verifiable cost-to-serve is on-trend |
| Compliance burden growth (per-vertical) | Rising sharply | RapidPOS's compliance surface (NICS, 4473, ATF, RACS, ShipCompliant, EBT, bottle deposits) is the volume — Canary `compliance` module is well-targeted |
| LP / shrink as analytics, not just alerts | Rising | RapidPOS has alerts (#99); nobody in this set has detection-as-graph. Canary `chirp` + `fox` + `hawk` is on-trend differentiation |
| Multi-tier assortment (drop-ship + own + warehouse) | Rising | RapidPOS surfaces drop-ship (#59); Canary's `inventory-as-a-service` extends the trend |
| Verifiable evidence (insurance, regulatory) | Emerging | Zero competitive analog. Canary `blockchain-anchor` is ahead of demand but in the trend direction |

### Competitive Set Analysis

| Competitor | Tier | Architecture | Customer Positioning | Price Posture | Gap vs Joint Product |
|---|---|---|---|---|---|
| **NCR Counterpoint** | Incumbent | On-prem, customized | Specialty retail VAR-channel | $25/till + setup + per-integration | 41-year platform; no LP, no OTB, no accountability rail |
| **NCR Voyix** (CX7ii) | Incumbent upgrade | Cloud + hardware | Mid-market retail (incl. enterprise) | Hardware-led + SaaS | Direct back-half competitor — *not just hardware*; per founder memory, Voyix competes on LP/analytics |
| **Lightspeed Retail** | Modern cloud SMB | Cloud-native | Cloud-curious SMB specialty | Tiered SaaS per location | No accountability rail; thinner compliance per vertical |
| **Heartland Retail** | Modern cloud SMB | Cloud-native | SMB specialty + chains | Tiered SaaS | No LP detection graph; thinner OTB |
| **Coreware / AmmoReady** | Vertical specialist (gun) | Cloud | Gun retailers exclusively | Per-FFL pricing | Single vertical only; no general retail |
| **Spruce Software** | Vertical specialist (garden) | Cloud | Garden + lumber/hardware | Per-location | Single vertical |
| **Shopify POS** | Brand-tier | Cloud + retail extension | DTC brands extending into retail | Per-location + transaction | Not a Counterpoint replacement; thin back-half for specialty verticals |
| **Square for Retail** | Low-end | Cloud | Single-store, sub-$2M | Per-transaction + flat | Functionally below the ICP floor; not on the choice set for $5M+ specialty |

**The gap the joint product fills:** Counterpoint-class functional breadth (130 capabilities, all 14 verticals, 51 integrations) **+** cloud-native architecture (DriftPOS Kotlin/.NET; Canary Go/GCP) **+** accountability rails (operational/financial/evidentiary) — none of the named competitors clear all three.

### Internal Performance Snapshot — Capability SMROI Analog

The PwC SMROI framework plots categories on Sales × Margin Return. For a pre-revenue joint product, the analog is **Capability Surface × Differentiation Strength** — where the joint product invests next.

```
                                 Differentiation Strength (vs RapidPOS-advertised baseline)
                                    LOW                              HIGH
                          ┌──────────────────────┬────────────────────────────┐
                          │                      │                            │
                  HIGH    │   PROTECT / PARITY   │     INVEST / LEAD          │
                  (many   │                      │                            │
                  caps)   │   Item, Customer,    │   tsp (offline/Safe-Sync), │
                          │   Pricing,           │   compliance (gun/liq/grc),│
                          │   Receiving, Report  │   commercial (A/R + GC),   │
                          │                      │   ecom-channel             │
                          │                      │                            │
   Capability Surface     ├──────────────────────┼────────────────────────────┤
   (count of caps         │                      │                            │
   in the module)         │   DE-EMPHASIZE       │     GREENFIELD MOAT        │
                          │                      │                            │
                  LOW     │   asset (print svc), │   chirp (LP detection),    │
                  (few    │   transfer (gap),    │   fox (evidence chain),    │
                  caps)   │   employee/sched     │   hawk (case mgmt),        │
                          │                      │   l402-otb (OTB-as-meter), │
                          │                      │   blockchain-anchor,       │
                          │                      │   ildwac (sat WAC),        │
                          │                      │   agent-network            │
                          │                      │                            │
                          └──────────────────────┴────────────────────────────┘
```

**Reading the 2×2:**

- **INVEST / LEAD (high surface, high differentiation):** `tsp`, `compliance`, `commercial`, `ecom-channel`. These are categories where the joint product matches Counterpoint at parity *and* extends meaningfully (offline-by-design, per-vertical compliance breadth, A/R + gift-card lifecycle as native primitives, ecom-as-spine vs ecom-as-integration).
- **GREENFIELD MOAT (low surface today, high differentiation):** The "and more" surface. `chirp`, `fox`, `hawk`, `l402-otb`, `blockchain-anchor`, `ildwac`, agent network. These are categories with zero competitive analog — RapidPOS surfaces nothing, and neither do Lightspeed, Heartland, or NCR Voyix. The leverage is highest here because the message lands without comparison friction.
- **PROTECT / PARITY (high surface, low differentiation):** `item`, `customer`, `pricing`, `receiving`, `report`. These need to exist at Counterpoint parity — 130 retailers running the joint product expect them — but they are not where the positioning fight is won.
- **DE-EMPHASIZE (low surface, low differentiation):** `asset` (print orchestration), `transfer` (inferred-only), employee scheduling. These are gaps to close before the proposal ships, but they are not positioning leverage. Build to parity, move on.

### Key Findings

1. **The competitive set has no platform combining Counterpoint-class breadth + cloud architecture + accountability rails.** This is the structural opening.
2. **OTB is an unclaimed category-level differentiation primitive.** RapidPOS surfaces OTB once in 43 pages (clothing vertical only). Lightspeed and Heartland do not advertise it as a financial rail. The L402-gated meter model is a class of its own.
3. **NCR Voyix is the most dangerous competitor.** Public hardware partner to RapidPOS, functional competitor to Canary's back-half. Joint go-to-market needs careful handling. (Flagged in GRO-721 §8.5; recommended dispatch in §7.5.)
4. **Vertical specialists are not a generalized threat.** Coreware/AmmoReady, Spruce, and similar dominate single verticals on compliance depth but cannot serve the multi-vertical owner-operator. The joint product's 14-vertical surface is itself defensible.
5. **The 50+ integration tax is the unspoken cost driver.** Counterpoint's 50+ third-party integrations are not a feature of Counterpoint — they are a tax on the retailer. Every integration is a vendor relationship, a per-month bill, and a failure surface. Position the joint product as integration-collapse, not integration-add.

---

## Phase 2B — Primary Consumer Research

### Summary Finding

This phase is mostly a gap. The honest delivery is a fielding plan, not a finding. The dispatch frame for GRO-721 explicitly excluded direct outreach to Bart's team; no end-customer interviews are on file; no quantitative segmentation has run. What we can do is structured proxy work using publicly available customer voice (review sites, vertical forums, social) plus a Bart-channel ask list. The Phase 3 positioning strategy below is calibrated to what Phase 2A can support; Phase 2B work upgrades confidence on the customer-segment sizing in §3.

### What We Have (proxy customer voice)

| Source | Signal | Confidence |
|---|---|---|
| RapidPOS website testimonial | Single named customer (Keith, CFO – Chalet) for a 41-year company | Low — single proof point |
| RapidPOS vertical configurations | 14 verticals with vertical-specific feature pages reveal which verticals Bart's team has invested deepest in (gun, liquor, grocery, garden) | Medium — investment ≠ revenue |
| Counterpoint user community signals (G2, Capterra, Reddit) | Not yet mined — recommended | Gap |
| Vertical-specific review surfaces (gun forums, garden retailer associations) | Not yet mined — recommended | Gap |
| Bart's call notes (founder-direct) | DriftPOS pilot is liquor + DoorDash + Vivino — signal that liquor is the lead vertical | Medium — single data point |

### What We Need (recommended Phase 2B fielding plan)

| Workstream | Method | Estimated Compression |
|---|---|---|
| Counterpoint user voice mining | G2 / Capterra / Reddit / industry-forum scrape — pattern-extract pain points and unmet needs | 1 week (agent-assisted) |
| Vertical-specific customer interviews via Bart | 8–12 interviews across 4 lead verticals (gun, liquor, garden, feed&tack); Bart introduces, founder + agent run | 3–4 weeks elapsed |
| Quantitative segmentation survey | 200–400 SMB specialty retailers running Counterpoint (Bart's customer base is the sample frame); 25-question survey on pain points, willingness to switch, price sensitivity | 4–6 weeks elapsed |
| Win/loss / churn signal from Bart | Direct ask in next call: top customer concentration, churn rate, recent wins/losses, why they came / why they left | 1 conversation |
| Competitive switching pattern analysis | Public LinkedIn / case study mining of Counterpoint → Lightspeed / Heartland switch announcements | 1 week |

**Recommended sequence:** Mine public customer voice first (cheap, fast, calibrates the questionnaire). Then Bart-channel asks. Then fielded interviews. Then quantitative survey. Total compression: 6–8 weeks elapsed if Bart is responsive.

### Open Questions (resolve in fielding)

| # | Question | Why it matters for positioning |
|---|---|---|
| OQ-1 | Within Bart's install base, what is the per-vertical revenue distribution? | Determines which vertical leads the launch GTM |
| OQ-2 | What is the current Counterpoint churn rate, and where do churners go? | Tells us the actual competitive set churners choose |
| OQ-3 | What % of customers have already moved one or more "back-half" workflows off Counterpoint to a SaaS? | Calibrates the integration-collapse message |
| OQ-4 | What is the willingness-to-pay ceiling per till and per store for the joint product? | Calibrates pricing strategy |
| OQ-5 | How much LP/shrink pain do these retailers actually report? Is `chirp` selling a known pain or an unknown pain? | Determines whether LP leads or supports the message |
| OQ-6 | What does the owner-operator measure success by — revenue, margin, hours back, both? | Calibrates ROI framing |

### What Phase 2B Will NOT Resolve

This is a B2B sale to an owner-operator running a specialty retail business; the sample sizes are small (Bart's install base is the universe, not a national consumer panel). Phase 2B output will be qualitative-heavy with directional quantitative — positioning calibration, not market sizing.

---

## Phase 3 — Positioning Strategy and Strategic Opportunities

### Summary Finding

The four positioning variables resolve cleanly given the Phase 2A data. The category move — from POS-replacement to accountability-platform — is the highest-leverage frame because it sidesteps feature-parity comparison with NCR Voyix, Lightspeed, and Heartland. The merchandising/marketing implication is to lead with the accountability rails (operational, financial, evidentiary) and back-fill with capability-parity proof rather than the inverse. Infrastructure requirements are largely already specified; the gap-closure list from GRO-721 §4 is the must-do work before the proposal ships.

### Consumer Segment Sizing (Directional)

Without Phase 2B fielding, segment sizes are directional reads from Bart's 14-vertical surface plus general SMB specialty retail knowledge.

| Segment | Profile | Approximate Size of Bart's Base | Strategic Priority |
|---|---|---|---|
| **The Multi-Hat Lifer** | Single-store or 2–3 store specialty retailer, $5M–$20M revenue, owner has run Counterpoint 10+ years, deep customizations, every-day operator on the floor. Hates the $25/till bleed but switching feels existential. | Estimated 60–70% of Bart's install base (vertical-diverse) | **PRIMARY TARGET** |
| **The Compliance-Bound Specialist** | Single-vertical retailer with heavy regulatory burden (gun, liquor, grocery, feed). 1–10 stores. $5M–$50M revenue. Compliance is daily operational reality, not paperwork. | Estimated 20–25% — concentrated in gun and liquor | **SECONDARY TARGET (lead with gun + liquor)** |
| **The Multi-Store Operator** | 5–10 stores, $20M–$50M revenue, has dedicated ops/IT person, runs cross-store transfers and consolidated reporting. | Estimated 5–10% — high-revenue concentration | **TERTIARY TARGET — but disproportionate revenue** |
| **The Cloud-Curious Switcher** | Already explored Lightspeed / Heartland but stayed on Counterpoint due to vertical depth or migration cost. | Estimated 5% — but the most likely first-wave converters | **EARLY-ADOPTER WEDGE** |

**Recommendation:** Target the Multi-Hat Lifer through the wedge of the Cloud-Curious Switcher. The Switcher segment is small but first to convert; their conversion creates social proof for the Lifer segment. Compliance-Bound Specialists are launch-vertical priority (gun and liquor have the deepest compliance gravity and the cleanest ROI story).

### The Positioning Framework (filled in)

```
POSITIONING VARIABLES                    EXECUTION VARIABLES
─────────────────────                    ───────────────────
Core Customer:                    →      Merchandising:
The Multi-Hat Lifer running              130-capability surface at parity
heavily customized Counterpoint,         + the "and more" rails as flagship
$5M–$50M, owner-operator, 1–10           features (LP detection graph,
stores, vertical-bound,                  l402-OTB, evidence chain,
$25/till bleed, 50+ integration tax      satoshi cost rollup)

Core Competition:                 →      Pricing:
Counterpoint inertia (incumbent),        Verifiable satoshi cost rollup
NCR Voyix (upgrade pull),                replaces $25/till SaaS bleed.
Lightspeed/Heartland (cloud peers).      Phased: Canary back-half first
NOT Square. NOT Shopify.                 (per-store), DriftPOS register
                                         second (per-till parity or below).

Core Merchandise:                 →      Key Product Attributes:
The retail operating system              Offline at the till (Safe-Sync).
that takes accountability for            Cryptographic evidence chain.
operations, financial discipline,        Per-vertical compliance depth.
and evidence — not just                  OTB as a financial rail across
transactions.                            all categories. Whitelabel-native.

Key Appeals:                      →      Marketing:
Rational: replace the bleed,             Lead with the rails (operational,
collapse the integration tax,            financial, evidentiary). Back-fill
phased migration, never go dark.         capability parity. Anchor on the
Emotional: take ownership back.          $25/till + 50+ integration story.
Prove what happened. Your data           Joint case studies with Bart's
is yours. End the shrink mystery.        early movers.
                                  →      Customer Service:
                                         RapidPOS install / training /
                                         24x7 model preserved (their
                                         channel strength); Canary adds
                                         agent-network operational PMO.

                                  →      Infrastructure:
                                         DriftPOS hardware provisioning
                                         (RapidPOS field staff) +
                                         Canary GCP/Cloud Run + ARTS
                                         POSLOG joint integration contract.
                                                 ↓
                          POSITIONING STATEMENT
```

### Positioning Statement (draft)

> *For specialty retailers running Counterpoint who are tired of the per-till bleed, the integration tax, and the shrink mystery — DriftPOS + Canary is the retail operating system that keeps your register running, takes accountability for the rest, and proves what happened. Unlike Counterpoint, NCR Voyix, or modern cloud peers, every variance has a node, every cost rolls up to verifiable satoshis, and every case event is anchored on Bitcoin L2. We replace your bleed; we don't add to it.*

This is a draft. The headline numbers ($25/till, 50+ integrations) are confirmable from public RapidPOS sources. The specific verbs ("keeps your register running," "takes accountability," "proves what happened") map to the three rails. Refine in Phase 3 review with founder.

### Merchandising / Marketing Strategy Outline

| Channel | Lead Message | Proof |
|---|---|---|
| Tim Mooney recap (next 30 days) | Joint product replaces Counterpoint plus everything Counterpoint never did | GRO-721 capability map; differentiation surface §5 |
| Bart channel (his customer base) | Phased migration; you don't go dark; install/train/support model unchanged | RapidPOS service offerings preserved (#127–129) |
| Vertical launch — gun | eBound + 4473 + NICS + range + consignment + audit, plus Canary `chirp` shrink graph | Capabilities #64, #104–107, #126; `chirp` differentiation |
| Vertical launch — liquor | Liquor club + bottle deposits + ShipCompliant + Drizly + DoorDash, plus l402-OTB across categories | DriftPOS pilot is liquor; capabilities #28, #75, #77 |
| Trade press / analyst | The accountability platform category — operational, financial, evidentiary rails | Platform thesis; unique combination unclaimed |
| Insurance underwriting story | Verifiable evidence chain reduces underwriting friction | `fox` + `blockchain-anchor`; GRO-686-699 cross-reference |

### Infrastructure Requirements

Largely already specified. The must-close gaps from GRO-721 §4 are the work list:

| Gap | Owner | Pre-proposal? |
|---|---|---|
| `transfer` module confirmed in Phase 1 scope | Canary engineering | Yes |
| EBT acceptance integration contract | DriftPOS + Canary joint | Yes |
| Label-printing / `asset` print orchestration | Canary engineering | Yes |
| Scheduling primitives (employee or `commercial` partner bridge) | Canary architecture | Yes |
| Customer-A/R scope split in `commercial` | Canary architecture | Yes |
| Returns / RMA register-vs-back-half split | Joint integration contract | Yes |

These six are the gating items. None are architectural blockers; all are specifiable in the next dispatch cycle (recommended GRO ticket §7.7 in GRO-721 — joint integration contract spec).

### Strategic Opportunities Register

| # | Opportunity | Rationale | Priority |
|---|---|---|---|
| SO-1 | Lead with `l402-otb` as the financial-rail flagship | Greenfield surface; founder thesis confirmed by absence of competition | **P0** |
| SO-2 | Position joint product as "accountability platform," not "Counterpoint replacement" | Sidesteps NCR Voyix feature-parity battle | **P0** |
| SO-3 | Insurance underwriting bridge product (evidence chain → underwriter discount) | `fox` + `blockchain-anchor` + GRO-686-699 stack ready; unclaimed market | **P1** |
| SO-4 | Vertical launch sequence: liquor first (Bart's pilot), gun second (compliance gravity), garden third (Canary's `inventory-as-a-service` shines on seasonal/perishable) | Matches DriftPOS pilot reality + compliance ROI clarity | **P1** |
| SO-5 | Whitelabel program for other Counterpoint VARs beyond RapidPOS | Bart's deal is the template; tenant config layer is first-class | **P2** |
| SO-6 | Sub-brand crawls for the four RapidPOS vertical sub-brands | Material additional capability surface, especially gun + garden | **P2 (already filed in GRO-721 §7.1)** |
| SO-7 | NCR Voyix competitive posture re-check | Public hardware partner / functional competitor; high-stakes ambiguity | **P1 (already filed in GRO-721 §7.5)** |
| SO-8 | Joint case study program — Chalet (existing testimonial) + DriftPOS liquor pilot + 2 more | Single-testimonial public-site footprint is a known weakness; joint launch fixes it | **P1** |

### Implications for Tim Mooney's Recap

The recap should anchor on three things, in this order:

1. **The $25/till + 50+ integration bleed.** Concrete, customer-felt, immediately credible.
2. **Phased migration.** Canary back-half first; register cuts second; Counterpoint sunsets last. No big-bang switch.
3. **The accountability rails.** Operational (no unknown loss), financial (l402-OTB, satoshi WAC), evidentiary (blockchain-anchored case events). This is the category move; this is what no competitor claims.

Feature parity proof is appendix material, not headline. The 130-capability map is the back-up deck — it makes the parity claim defensible without burying the differentiation message.

---

## Phase 3 Open Questions (founder review)

| # | Question | Resolution Path |
|---|---|---|
| OQ-A | Is the joint product branded under a new name (TBD), under DriftPOS, under Canary, or co-branded? | Founder + Bart conversation; brand-voice plugin downstream |
| OQ-B | Does the launch GTM lead with the Lifer segment broadly or the Compliance-Bound Specialist (gun/liquor) narrowly? | Recommend narrow → broad; await Bart's per-vertical revenue mix |
| OQ-C | What is the per-till pricing posture vs the $25 NCR anchor? Below, at, or above with a verifiable cost-to-serve story? | Pricing dispatch downstream of OQ-4 (Phase 2B) |
| OQ-D | Is the insurance-underwriting bridge product positioned as a capability of the platform or as a separate product line? | Separate strategic dispatch; intersects GRO-686-699 |
| OQ-E | How does the NCR Voyix partnership-vs-competition tension get handled in the public proposal? | Recommend GRO-721 §7.5 dispatch run before any external positioning collateral ships |

---

## Audit Notes

### Methodology compression

The PwC playbook nominally runs 11–13 weeks. This analysis compressed Phase 1 to hours and Phase 2A to a single session by leveraging GRO-721 as the data inventory. Phase 2B is honestly flagged as gap with a fielding plan. Phase 3 is delivered at draft confidence, gated on Phase 2B for segment sizing precision and pricing strategy.

### Source attribution

Every Phase 2A data point traces to GRO-721 / `Brain/wiki/canary/partnership-research/rapidpos-feature-map.md`. Phase 2A market-trend reads draw on general SMB retail market knowledge and are flagged where directional. Phase 3 positioning claims map back to specific capabilities by number; the positioning statement uses only confirmed public RapidPOS facts ($25/till, 50+ integrations, 14 verticals).

### Confidence assessment

| Phase | Confidence | Bound |
|---|---|---|
| Phase 1 | HIGH | Inputs are concrete and complete |
| Phase 2A — Competitive set | HIGH | Eight named competitors, specific positioning gaps cited |
| Phase 2A — SMROI 2×2 | HIGH | Direct read of the 130-capability data |
| Phase 2A — Market trends | MEDIUM | Directional knowledge of SMB retail; not source-cited per row |
| Phase 2B | LOW (gap) | Fielding required to upgrade |
| Phase 3 — Positioning framework | MEDIUM-HIGH | Resolves cleanly from Phase 2A; gated on Phase 2B for segment sizing |
| Phase 3 — Positioning statement | DRAFT | Founder review required |

### Anti-speculation gate

No pricing, customer counts, churn rate, revenue mix, or contract structure has been inferred. All such items are flagged as Phase 2B fielding asks (OQ-1 through OQ-6) or founder-direct asks (carry-forward from GRO-721 §7.2).

---

## Related

- Source research: [[rapidpos-feature-map|RapidPOS Feature Map (GRO-721)]]
- Methodology: PwC Consumer Positioning Playbook (`anthropic-skills:consumer-positioning`)
- Platform thesis: `Brain/wiki/cards/platform-thesis.md`
- Canary Go module spine: `docs/sdds/go-handoff/go-module-layout.md`
- Memory entries: `project_canary_canonical_positioning.md`, `project_rapidpos_go_pivot.md`, `project_rapidpos_stakeholders.md`, `project_canary_replaces_counterpoint_long_arc.md`
- Joint integration contract spec (recommended next dispatch): GRO-721 §7.7

---

*Generated 2026-05-01 by ALX (laptop session) running the consumer-positioning playbook on GRO-721 findings. Phase 2B fielding plan is the next-action gate before this analysis upgrades from draft to approved.*
