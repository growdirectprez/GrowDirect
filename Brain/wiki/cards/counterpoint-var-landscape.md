---
card-type: market-intelligence
card-id: counterpoint-var-landscape
card-version: 1
domain: canary
layer: market-research
status: approved
agent: ALX
tags: [counterpoint, ncr, var, channel, market-intelligence, partnership]
last-compiled: 2026-05-03
needs-review: 2026-08-03
---

## What this is

The 2026 state of the NCR Counterpoint Value-Added Reseller (VAR) channel — structure, tier and volume, named players, commercial economics, and the implication of the October 2026 forced migration for VAR delivery capacity. Card 3 of the Counterpoint series, sitting beneath [[ncr-ecosystem-2026]] (corporate context) and [[counterpoint-product-state-2026]] (product layer).

## Purpose

Counterpoint customers do not buy Counterpoint from NCR Voyix. They buy it from a VAR. The VAR holds the customer relationship, sells the license, implements the platform, customizes the workflow, supports the deployment, and books the migration work. For Canary, the VAR is the channel — not Voyix. Understanding which VARs exist, how they make money, where they specialize, and how the October 2026 migration window changes their workload is the load-bearing question for go-to-market design. This card lays the structure out.

The strategic frame: Voyix has approximately 80,000 platform sites globally (year-end 2025), of which 5,600–15,000 US sites are Counterpoint deployments (per [[rapid-pos-counterpoint-market-research-tam]]). Those sites are touched, almost without exception, by a VAR. The VAR channel is the practical surface area of the Counterpoint installed base.

## §1 — VAR channel structure

**The three-actor flow.** Voyix licenses the Counterpoint software and the underlying payment integration (Voyix Connect). The VAR resells the license, builds and installs the deployment, and signs the customer for ongoing support. The end-customer merchant pays the VAR; the VAR pays Voyix the license and maintenance fee, retains the implementation services revenue, and earns ongoing support contract revenue. Voyix's direct relationship with the SMB Counterpoint customer is thin to nonexistent — the merchant generally does not call NCR. They call the VAR.

```
┌─────────────────┐    license    ┌─────────────────┐   bundled deal    ┌─────────────────┐
│   NCR Voyix     │◄─────────────►│      VAR        │◄────────────────►│    Merchant     │
│  (the vendor)   │   + maint.    │ (the channel)   │  license + svcs   │  (end customer) │
└─────────────────┘                └─────────────────┘                    └─────────────────┘
                                          ▲
                                          │  customer relationship
                                          │  lives here, not at Voyix
```

**What VARs sell.** The VAR engagement is rarely just software. A typical Counterpoint VAR contract bundles:

| Component | What the VAR delivers | Approximate share of total deal |
|-----------|----------------------|--------------------------------|
| Software license | Resold from Voyix | 15–25% |
| Implementation services | Configuration, data migration, integration, training, go-live | 25–40% |
| Hardware | POS terminals, servers, peripherals, payment devices | 20–35% |
| Customization / extensions | Crystal Reports, custom workflows, e-commerce connectors, vertical-specific modules | 5–20% |
| Annual support contract | Help desk, version upgrades, troubleshooting | recurring, 15–25%/year of license cost |

**Margin structure.** Public reseller pricing pages (e.g., POS Highway, AMS Retail) suggest VARs retain meaningful margin on services (implementation, customization, support) and thinner margin on resold software and pass-through hardware. The recurring revenue stream — annual support contracts at 18–22% of license value (per [[counterpoint-product-state-2026]] pricing model) — is the franchise asset. A VAR's installed base × average annual support fee is the durable revenue line; everything else is project work.

**Why the VAR relationship is stickier than the Voyix relationship for SMB.** Three reasons compound:

1. **Customization investment.** Counterpoint deployments accumulate Crystal Reports, custom data fields, vertical-specific workflows, and integration code over years. The VAR built it; the VAR is the only entity that can maintain it. Migrating to a different VAR is technically possible but operationally painful — the receiving VAR has to relearn the customizations.
2. **Single point of escalation.** A merchant with one IT person (often the owner) does not have the bandwidth to triage between Voyix product issues, payment processor issues, hardware vendor issues, and integration issues. The VAR is the one phone number for everything that touches the POS.
3. **Vertical knowledge.** A Counterpoint VAR with garden-center customers knows which Crystal Reports the garden vertical needs, how seasonal inventory works, how multi-tier customer pricing for landscapers vs retail-walk-ins gets configured. That vertical knowledge is not in Voyix's documentation. It's in the VAR's heads.

For Canary's go-to-market, the implication is clean: introducing Canary to a Counterpoint merchant is a VAR co-sell, not a direct sale. The merchant's first call when something goes wrong with Canary will be the VAR — so the VAR has to be a partner in the deployment, not a bystander.

## §2 — Key VAR players

The Counterpoint VAR ecosystem has a long tail. The named players below are the ones that surface repeatedly in industry coverage, partner directories, and primary brand context. All numbers below carry confidence flags — exact install counts are not publicly disclosed by Voyix or by VARs themselves; ranges are extrapolated from LinkedIn employee count, vertical site coverage, and public customer references.

| VAR | Headquarters | Geographic footprint | Primary verticals | Counterpoint install count (estimate) | Notable capabilities | Public trajectory signals |
|-----|-------------|---------------------|------------------|---------------------------------------|---------------------|--------------------------|
| **Rapid POS** | San Diego, CA | US, Canada, Mexico | Garden (Rapid Garden POS), Firearms (Rapid Gun Systems), feed & tack, food, wine | Unknown — the dispatch-named "first VAR partner candidate" — likely high hundreds to low thousands across sub-brands | Counterpoint University (training-as-channel-mindshare); vertical sub-brands; e-commerce connectors; mobile (RapidGO); 24/7/365 support; founded 1985; LinkedIn lists 51–200 employees | Active investment in vertical sub-brands; "unified commerce" positioning aligned with Voyix's strategic pillar |
| **AMS Retail Solutions** | Virginia / North Carolina (Mid-Atlantic) | Mid-Atlantic + Canada | Garden centers, farm/feed/seed, pet supply, sporting goods, hardware | Unknown — regional boutique scale | Single-source provider model; 24/7 support; specialty-retail focus; pricing pages publicly disclose ~$149/license/month Counterpoint Cloud subscription pass-through | Stable regional operator; deep specialty-retail vertical mix |
| **Retail Control Systems (RCS)** | Lebanon, NH | New England + nationwide | Thrift, garden, sporting goods, museums & attractions, wine & liquor, specialty foods, wholesale, Goodwill | Unknown — RCS publicly claims "#1 NCR Counterpoint reseller for over 20 years" | NCR Interact Premier Solution Provider; 30+ years Counterpoint tenure; named clients include the New England Patriots and Red Sox team stores, Biltmore | Strongest public reference base; high vertical breadth; geographic anchor in Northeast |
| **C&K Systems** | Murrells Inlet, SC (offices VA Beach, Orlando) | US-wide; ~5 countries | Garden, apparel/footwear, liquor, gift, outdoor outfitters, specialty | 500+ companies (vendor-stated) | NCR Voyix Platinum Partner (20+ years); PCI-QIR Certified; VISA Validated Service Provider; 30+ years in business; LinkedIn shows ~36 employees, 11–50 size band; founded 1989 | Platinum-tier status is the highest published Voyix VAR tier; small headcount despite large customer claim suggests high per-account efficiency |
| **Mariner Business Solutions** | Denver, CO | US-wide (Rocky Mountain anchor) | Liquor, cannabis (CannaPoint), garden centers/nurseries/landscaping, gift/specialty | Unknown — likely several hundred across verticals | 40 years in retail; cannabis vertical specialization (CannaPoint = Counterpoint engine + cannabis seed-to-sale); founded 1983 | Cannabis vertical is a structural growth driver; Denver HQ gives Rocky Mountain-region presence |
| **POS Highway** | New York, NY (office in Honolulu, HI) | US-nationwide | Apparel, auto accessories, beauty, building supply, furniture, garden, hardware, liquor/wine, sporting goods, restaurants | Unknown — claims "Top 5 Elite partner" status | 30+ years (since ~1986); custom Counterpoint addons by vertical; 100% US-based NCR-certified consultants | Bicoastal coverage; broad vertical mix suggests generalist over specialist |
| **RBMS (Retail Business Management Systems)** | Old Bridge, NJ (offices NYC, Philadelphia) | NJ / NY / PA / quad-state, expanded nationwide | Food, apparel, general merchandise | Thousands of users (vendor-stated, Greater NYC metro) | 25+ years in POS; Fortune-magazine recognized; Financial District demo showroom | Northeast-anchored generalist; thin vertical specialization compared to Rapid or AMS |
| **NCC** *(see footnote)* | — | — | — | — | — | — |

**Eight slots, seven characterizations.** The dispatch named "NCC / National Cash Control" as a Counterpoint VAR; web research did not validate this. The closest match — National Computer Corporation in Greenville, SC — is a specialty POS company that develops its own Reflection POS Software (restaurants, retail, specialty venues) rather than reselling Counterpoint. There may be an unrelated "National Cash Control" in the mid-Atlantic that is a Counterpoint VAR but is not public-web indexed under that name. Flag for partner-directory verification before relying on this entry.

**Other VARs surfaced in the partner-directory ecosystem** (not characterized in detail; included for completeness): The Retail Computer Group (TRCG), CCS Retail Systems (~2,000 supported users across all verticals), CompuTant, Retail Data Systems (RDS), One Step Retail Solutions, Skurlas, Mainspring Retail Solutions, and a long tail of regional independents. Per [[rapid-pos-counterpoint-market-research-tam]] the total active Counterpoint VAR universe in North America likely sits in the 30–50 range, with the eight to twelve named above accounting for the bulk of installed-base coverage.

**Geographic correction note.** Three VAR characterizations in the dispatch brief diverged from public-web evidence. AMS Retail Solutions is Mid-Atlantic (VA/NC), not "upper Midwest"; POS Highway is NYC + Honolulu, not Florida; RBMS is New Jersey, not Rocky Mountain. The Rocky Mountain Counterpoint VAR most consistent with public sources is Mariner (Denver). Brain content is corrected to public-source positioning above; older intake material that named different geographies has been superseded by this card.

## §3 — VAR tier and volume sizing

**Total active Counterpoint VARs in North America: approximately 30–50.** This range is consistent with VAR-channel public listings (ElioPlus partner directory, NCR Voyix partner page, vertical association coverage) and with the publicly-stated tier of the Voyix partner program. The named eight in §2 are the most visible; the long tail consists of regional independents serving 10–50 customers each.

**Tier structure.** A working classification of VARs by deal-volume scale:

| Tier | Approximate annual new Counterpoint deployments | Count of VARs (estimate) | Examples |
|------|------------------------------------------------|-------------------------|----------|
| **Anchor** | 10+ new sites/year + large maintenance book | 5–8 | Rapid POS, RCS, C&K Systems, POS Highway |
| **Mid-tier** | 3–10 new sites/year | 8–15 | AMS Retail, Mariner, RBMS, CCS Retail Systems |
| **Long-tail** | 1–2 new sites/year, primarily maintenance | 15–30 | Regional independents |

This is a directional split derived from public install-count claims, LinkedIn employee headcount as a deal-capacity proxy, and partner-tier signals (Platinum vs unspecified). It is not a published Voyix-side tier breakdown — Voyix does not publicly disclose VAR-by-VAR volume.

**Counterpoint sites managed by VAR channel vs direct Voyix.** For SMB Counterpoint, direct Voyix is negligible. NCR Voyix as a corporate entity engages directly with enterprise retail (Voyix Commerce Platform target customers — grocery, c-store, fuel) and with restaurant chains (Aloha enterprise contracts). Counterpoint's specialty-retail SMB segment is sold and supported almost entirely through the VAR channel. The 5,600–15,000 estimated US Counterpoint sites are, for practical purposes, a VAR-managed installed base.

**Implication for Canary.** The VAR channel is not a marketing distribution layer — it is the operational layer. There is no "go around the VAR" path to a Counterpoint merchant that doesn't burn the relationship. Canary's customer-acquisition strategy must treat the VAR as a partner with veto power, because the VAR effectively does have it.

## §4 — October 2026 migration service opportunity

**Volume of at-risk sites.** Per [[counterpoint-product-state-2026]], every Counterpoint site running v8.6.4 or earlier loses card processing capability when Voyix Secure Pay is decommissioned in October 2026. No public version-distribution data exists, but the operational pattern in SMB specialty retail is predictable: smaller sites on thin IT budgets, running stable deployments untouched for years, are the most likely to be on pre-v8.6.5. A working assumption — anchored to the 5,600–15,000 US Counterpoint site universe and a heuristic that 30–50% of sites are running pre-v8.6.5 versions — yields **2,000–7,500 US sites needing forced upgrade by October 2026**. This is the addressable migration-services market in the next 12 months.

**Estimated VAR billable hours per site.** A Counterpoint version upgrade on a site with custom modifications, third-party integrations, and aging hardware is not a patch-and-restart job. The work shape:

| Migration step | Typical hours per site (estimate) |
|---------------|----------------------------------|
| Compatibility review (custom modifications, third-party integrations, hardware drivers) | 4–12 |
| Database schema migration | 2–8 |
| Payment processor reconfiguration (Secure Pay → Voyix Connect) | 2–6 |
| Hardware refresh (where required — payment terminals, server) | 4–16 |
| Staff retraining on UI changes | 2–8 |
| Staging environment testing + cutover | 4–12 |
| **Total per-site VAR labor** | **~18–62 hours** |

At VAR loaded labor rates of $150–250/hour, this is **$2,700–$15,500 in pure migration services per site**, before any hardware revenue. Across the at-risk population, the aggregate channel revenue opportunity is **$5M–$115M in the 12-month migration window** for upgrade services alone — concentrated heavily in the anchor and mid-tier VARs that carry the largest installed bases.

**The migration window as Canary insertion point.** This is the strategic claim: every one of those 2,000–7,500 forced-upgrade engagements is a relationship touch. The VAR is in the merchant's store, in their database, reconfiguring their payment integration. The conversation has already started about "what's changing." For an anchor VAR, the question of "what else can we sell into this engagement to lift the per-site deal value" is structurally on the table.

Canary's intelligence-layer entry — low-friction, no rip-and-replace, deployed alongside the migration without disrupting the Counterpoint installation — is exactly the kind of value-add that converts a forced-upgrade conversation into a margin-expansion conversation for the VAR. The pitch: "While we're in there for the Voyix Connect cutover, let's wire up the analytics layer so the merchant can see what's actually happening in their stores." The VAR's incremental scope is small; the merchant's incremental cost is bounded; the VAR captures recurring revenue share on the Canary subscription. (See [[counterpoint-market-gtm-proposal]] §VAR Channel for the commercial model.)

The window is narrow. By Q4 2026, the forced-upgrade urgency dissipates and the VAR conversation shifts back to a slower steady-state cadence. The next 9–12 months are the highest-velocity moment in the Counterpoint channel for the next several years.

## §5 — VAR commercial model for co-sell

**T&M vs fixed-fee preference.** Public pricing pages (POS Highway, AMS Retail, others) and inferred behavior from VAR-customer review platforms suggest VARs structure new-deployment work primarily as **fixed-fee bundles** (license + hardware + implementation + first year support, all in one quoted contract) and ongoing customization work as **T&M with a not-to-exceed cap**. This protects the VAR from scope creep on greenfield deployments while preserving margin flexibility on bespoke change requests.

For subcontracted scope — a third party (Canary) inside a VAR's engagement — the prevailing model in the broader retail-IT VAR ecosystem is fixed-fee subcontract for defined deliverables, with a clear scope boundary. Time-and-materials subcontract arrangements exist but introduce friction in VAR deal modeling and are less common.

**Margin retained on subcontracted integration scope.** VARs typically mark up subcontracted services by **20–40%** before passing through to the merchant. A subcontractor billing a VAR $20,000 is reflected to the merchant at $24,000–$28,000 in the bundled engagement. This margin is the VAR's compensation for managing the relationship, owning the merchant escalation path, and standing behind the deliverable.

For Canary's commercial model, this means subscription pricing should be structured to give the VAR a defensible margin layer — a model where the VAR resells at a markup, or where the VAR earns recurring rev-share on Canary subscriptions paid directly by the merchant. The latter is cleaner: it preserves Canary's ability to manage the customer success layer directly while compensating the VAR for the introduction and ongoing relationship.

**What makes a subcontractor sticky vs one-time.** From the VAR's perspective, a sticky subcontractor:

1. **Has a productized methodology.** Repeatable scope, repeatable deliverables, repeatable timeline. The VAR can quote it without asking the subcontractor to rescope every time.
2. **Plays nice with the VAR's customer relationship.** Does not go around the VAR to the merchant. Does not introduce competitive products. Does not poach the support relationship.
3. **Brings recurring revenue, not one-time fees.** Subscription rev-share is more valuable than one-time implementation margin.
4. **Owns the escalation path on its own scope.** When the subcontractor's product fails, the subcontractor's team responds — not the VAR's help desk.
5. **Generates pull-through revenue.** Sells additional VAR services as a side effect (more hardware, more integration scope, more managed services).

Canary's positioning — productized intelligence layer, recurring subscription, dedicated support, Counterpoint-installation-friendly — maps cleanly to this profile.

## §6 — Canary co-sell positioning for VARs

**The framing: "the LP team you cannot afford to hire."** Per [[voyix-counterpoint-rapid-pos-engagement-context]], the most VAR-friendly positioning of Canary is an outsourced loss-prevention organization delivered as software. Most Counterpoint VAR customers (specialty SMB retailers) have zero dedicated LP staff — the owner wears the LP hat alongside every other hat. Framing Canary as "the LP team you cannot afford to hire" maps to a real pain point every VAR's customer has, regardless of vertical (firearms, garden, liquor, hardware, gift). It does not require the VAR to invent the pain or sell against an existing solution; it surfaces a gap the merchant already lives with.

The framing extends naturally beyond LP. Canary's intelligence layer also covers OTB enforcement, vendor-scorecard automation, item authorization across regulatory zones, real-time KPI exception surfacing — all capabilities a Counterpoint merchant currently does not have, and most of which they would have to hire a separate FTE (or outsource to a consulting firm) to operationalize. "The team you cannot afford" generalizes from LP to operations.

**Why Rapid POS is the right first VAR partner.** Three reasons compound:

1. **Counterpoint University = channel mindshare disproportionate to install count.** Rapid POS operates Counterpoint University — the de facto training resource for the Counterpoint user community. VARs and merchants outside Rapid's direct customer base consume Counterpoint University content. A Canary integration that ships with Counterpoint University curriculum coverage (training modules, integration guides, vertical playbooks) reaches the channel beyond Rapid's own customer roster. This is leverage no other VAR offers.
2. **Vertical sub-brand structure.** Rapid POS has demonstrated capacity to spin specialized Counterpoint configurations for verticals (Rapid Gun Systems for firearms, Rapid Garden POS for garden centers, Rapid Feed & Tack for agricultural retail, etc.). The pattern means Rapid is structurally accustomed to layering vertical-specific value on top of base Counterpoint. Canary is a similar layer — adding LP/ops intelligence that is vertical-aware but not vertical-locked. The VAR's go-to-market muscle is already shaped to absorb Canary as a co-sell add-on.
3. **Founder-level access.** Per [[project_bart_var_partnership]] and [[project_rapidpos_stakeholders]], Bart at Rapid POS is the known operational contact and the founder of the VAR's strategic direction (DriftPOS spin-out, etc.). The relationship is warm, not cold. First-VAR-partner conversations can move at trust speed rather than vendor-procurement speed.

**The repeatable methodology angle.** A successful Canary co-sell engagement with one Rapid POS customer (e.g., the Boutique Home & Garden chain referenced in [[voyix-counterpoint-rapid-pos-engagement-context]]) is not a one-off. The engagement methodology — four-week audit, transformation engagement, operating-system mode (per [[counterpoint-market-gtm-proposal]]) — is designed to be productized. Once Rapid POS has run it once, the same methodology applies to every other Counterpoint customer in their book. The unit economics for Rapid: a defined-scope subcontract that adds margin to existing customer engagements without requiring net-new acquisition cost.

Extended to other VARs: the same methodology runs through C&K Systems' garden-and-apparel customer base, RCS's New England specialty-retail base, AMS Retail's Mid-Atlantic farm-and-garden base, Mariner's liquor-and-cannabis customer base. Vertical knowledge vault content (per [[counterpoint-market-gtm-proposal]] §Pillar 1–3) gets vertical-tuned per VAR. The methodology is the asset; the vertical content is the personalization layer.

**The October 2026 migration acceleration.** The migration window (§4) is the natural acceleration moment. Rapid POS — and every other anchor VAR — is about to walk into hundreds of upgrade engagements. Each one is a relationship touch where Canary co-sell is a margin lift. The first VAR that productizes the migration-plus-Canary bundle establishes the channel template. The bet for Canary's GTM cadence: lock in Rapid POS as the lead reference VAR before Q4 2026, establish proof points in 2–4 customers by Q1 2027, and use Counterpoint University curriculum to scale the methodology to the broader VAR ecosystem in 2027.

## Open questions

1. **VAR-by-VAR exact install counts.** None of the eight named VARs publishes a precise Counterpoint customer count. C&K Systems' "500+ companies" and CCS Retail Systems' "2,000 supported users" are the only public anchors; both are vendor-stated. Resolving this requires partner-directory access or direct conversation with each VAR.
2. **NCC / National Cash Control verification.** The dispatch-named "NCC" was not validated by web research. The closest public-web match (National Computer Corporation, Greenville SC) develops its own POS rather than reselling Counterpoint. Confirm with the dispatch source whether NCC is a different entity, or substitute another mid-Atlantic VAR.
3. **Voyix partner tier disclosure.** C&K Systems publicly identifies as an NCR Voyix Platinum Partner. The full Voyix VAR tier structure (Platinum / Gold / Silver / Authorized?) is not publicly documented in current Voyix marketing materials. Resolving the tier map would clarify which VARs Voyix itself ranks highest.
4. **Pre-v8.6.5 site distribution.** The 30–50% pre-v8.6.5 estimate driving the §4 migration sizing is an extrapolation from "smaller sites running stable deployments untouched for years." A primary-source datapoint from Voyix or any anchor VAR would tighten the addressable-services market estimate substantially.
5. **Voyix Payments Partner Readiness Program details.** The migration-services preparation program launched by Voyix targets VARs directly. The exact training, certification, and tooling provided is not yet public. This affects how prepared the VAR channel will be in Q3–Q4 2026 to absorb the migration volume.

## Related

- [[ncr-ecosystem-2026]] — Card 1; NCR Voyix corporate structure, Candescent divestiture, Voyix Commerce Platform NRF 2026 signal
- [[counterpoint-product-state-2026]] — Card 2; Counterpoint product architecture, October 2026 migration, investment posture
- [[voyix-counterpoint-rapid-pos-engagement-context]] — engagement context, three-actor structure, "LP team you cannot afford to hire" framing
- [[rapid-pos-counterpoint-market-research-tam]] — TAM sizing, VAR landscape source notes, source-quality table
- [[counterpoint-market-gtm-proposal]] — VAR co-sell GTM motion, three-pillar vertical strategy (Lawn & Garden, Farm/Ranch/Firearms, Regulated Beverage)
- [[icp-murdochs-reference]] — canonical ICP for the platform; farm/ranch/firearms/hardware
- [[platform-thesis]] — infrastructure displacement as the primary SMB value proposition
- [[project_ncr_voyix_is_competitor]] — strategic framing: integration access via customer, not NCR partnership
- [[project_bart_var_partnership]] — Rapid POS partnership context (founder-level access)
- [[project_rapidpos_stakeholders]] — RapidPOS stakeholder map (Bart, Tim Mooney, founder roles)
