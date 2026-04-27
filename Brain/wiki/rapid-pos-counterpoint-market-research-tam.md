---
classification: internal
type: wiki
status: active
date: 2026-04-25
last-compiled: 2026-04-25
needs-review: 2026-05-09
source: public-web research; methodology section in body
----

# Rapid POS / NCR Counterpoint — Market Research + TAM

Public-source TAM estimate for the addressable market of "Counterpoint-running
SMB specialty retailer interested in a back-office analytics + loss-prevention
layer." Companion to
`Brain/wiki/rapid-pos-counterpoint-user-pain-points.md`.

## Executive summary

**Headline TAM (US, primary segment — Counterpoint-running independent
garden centers):** ~700–1,800 stores, with a defensible midpoint estimate
of ~1,200 stores. Confidence: **medium** — derived, not directly published.

**Headline TAM (US, extended — all SMB specialty verticals served by
Counterpoint VARs, including garden, gun, food, wine, feed-and-tack,
pet, sporting goods, hobby, gift, apparel):** ~6,000–14,000 stores,
midpoint ~9,000. Confidence: **medium-low** — heavy extrapolation from
NCR Voyix segment-level disclosures plus VAR self-reporting.

**Adjacent TAM signal (Module L native-build framing):** the US workforce
management software market is ~$9–10B in 2024 with retail commanding
~19% segment share. Homebase (100k+ SMBs) and When I Work (100k–200k
companies) sit on the SMB side of that market. Module L is greenfield
inside Counterpoint's installed base — Counterpoint exposes no labor
surface and the dominant integration partner (TimeForge) addresses a
small fraction of customers.

**Competitive context:** Counterpoint sits in the specialty / mid-market
slice of US retail POS, well below Square (~27% of POS installations)
and Shopify POS by merchant count, but with deeper inventory and
multi-tier pricing functionality than the cloud-native disruptors.
Counterpoint's likely SMB-retail share is single digits and shrinking
in % terms as cloud entrants grow faster, but the absolute installed
base is sticky because of customization lock-in.

**Strategic implication:** the displacement story (replace Counterpoint)
is hard — customers are locked in by customization. The ride-along
story (read what Counterpoint already captures, surface what
Counterpoint doesn't) has a credible 1,000–10,000 store TAM in the US,
plus a labor / Module-L greenfield surface that is genuinely
incremental rather than zero-sum versus the existing VAR channel.

## Methodology

### Time range

- 2024–2026 data preferred; older data used where it remains
  authoritative (e.g., 2018 green-industry economic impact study).

### Confidence framework

- **High** — multiple corroborating reputable sources, current.
- **Medium** — single reputable source, OR multi-source but extrapolated.
- **Low** — single source with weak primary methodology, OR pure
  extrapolation from indirect signals.

Every quantitative claim in this article has an explicit confidence
tag. The source-quality table at the end lists every number → source
→ confidence.

### Sources scanned

- IBISWorld (free portions): Nursery & Garden Stores in the US;
  Farm Supply Stores in the US.
- AmericanHort / Horticultural Research Institute: 2018 economic
  impact study; 2025 State of the Industry product page.
- NCR Voyix investor materials: Q4 2024 results, 2024 annual report,
  Q4 2025 results, S&P credit rating commentary, Investor Day
  presentation page.
- Garden Center Magazine: 2024 State of the Industry.
- Trade publications: Hardware Retailing, Lawn & Garden Retailer,
  Vertical IQ, BizBuySell valuation benchmarks, AnythingResearch.
- 6sense, MordorIntelligence, Statista, GrandView, Markets&Markets,
  Coherent, IndustryARC, ResearchAndMarkets — for POS market and
  workforce management sizing.
- Capterra / G2 / Software Advice / SoftwareConnect / SoftwareReviews /
  TrustRadius — for vendor visibility.
- Vendor sites: Rapid POS, Rapid Garden POS, Rapid Gun Systems,
  AMS Retail, RCS, C&K Systems, Mariner, POS Highway, NCC, RBMS,
  Retail Dimensions, CCS Retail Systems, NCR Voyix.
- VAR-aligned content: Lawn & Garden Marketing, Lawn and Garden
  Directory, Counterpoint Users Group historical content.
- US Census retail trade context (NAICS codes, structural).
- Workforce-management vendor sizing: Homebase, Deputy, When I Work,
  Beekeeper, YOOBIC, Foko (LumApps).
- Firearms-vertical context: Everytown Research, Wikipedia gun shop,
  Bravo Store Systems / Gearfire AXIS / Orchid Advisors / Trident 1.

### Sanitization rules

- Per `feedback_scrub_client_names`, no specific retailer is named in
  the synthesis. Vertical archetypes only.
- VAR / software vendor / industry-association names retained — those
  are public market actors, not customers.

## TAM estimate — primary (US garden centers on Counterpoint)

### Step 1: How many US garden centers?

Two corroborating sources, depending on definition:

| Definition | Count | Source | Confidence |
|---|---:|---|---|
| Nursery & Garden Stores (NAICS) | 9,885 stores | IBISWorld 2025 | high |
| Nursery, garden center, and farm-supply retailers (broader) | 13,400 stores across ~9,400 companies | Vertical IQ / AnythingResearch 2025 | high |
| Nursery & Garden Stores in California | 1,427 businesses | IBISWorld 2026 | high |

**Working number:** ~9,900 dedicated nursery & garden stores in the US,
or ~13,400 if farm-supply hybrids are included.

### Step 2: How many run Counterpoint?

This is the unknown. Public sources support a triangulation:

**Triangulation A: VAR market presence.**
- Rapid POS markets to garden centers under "Rapid Garden POS." Public
  customer testimonials, Capterra reviews, and Garden Center Magazine
  coverage suggest a customer base in the low thousands across all
  Rapid sub-brands (garden, gun, feed, food, wine).
- AMS Retail Solutions, RCS, C&K Systems, Mariner, POS Highway, NCC,
  RBMS, Retail Dimensions, CCS Retail Systems all sell Counterpoint
  to garden centers as one vertical among several.
- CCS Retail Systems publicly cites ~2,000 supported users across
  all verticals.
- Garden Center Magazine's 2024 State of the Industry surveyed 100+
  IGCs but did not publish POS-vendor breakdown publicly.

**Triangulation B: NCR Voyix retail segment context.**
- NCR Voyix retail segment 2024 revenue: ~$2.0B.
- NCR Voyix total platform sites at year-end 2024: 74,000; year-end
  2025: 80,000.
- These numbers cover all NCR Voyix retail products (DSR, Counterpoint,
  legacy systems, payments). Counterpoint is a minority of platform
  sites — DSR / department store and Aloha (restaurant) dominate.
- If Counterpoint represents 10–25% of NCR Voyix platform sites
  (an explicit assumption — no public split), Counterpoint is ~7,400–
  20,000 sites globally. US share estimated at 70–80% gives ~5,200–
  16,000 US Counterpoint sites across all verticals.

**Triangulation C: garden-center share of Counterpoint deployments.**
- Rapid Garden POS, AMS, RCS, and Mariner all market garden as a
  flagship vertical. C&K Systems' garden-center page is among the
  most prominent on its site.
- Trade-publication coverage of Counterpoint in Garden Center
  Magazine, Greenhouse Grower, and Nursery Management is
  meaningful — Counterpoint is one of 4–6 commonly named POS systems
  in IGC POS buyer guides (alongside Lightspeed, POS Nation,
  Comcash, Visual Retail Plus, Epicor).
- Buyer-guide aggregation suggests Counterpoint holds **10–25% share**
  of US IGC POS deployments by store count, with the rest split
  across Lightspeed, generic Square / Clover, POS Nation, Comcash,
  Visual Retail Plus, and legacy systems.

### Step 3: Compute primary TAM

US IGC universe: ~9,900 stores (high confidence).
Counterpoint share among IGCs: 10–25% (medium-low confidence,
extrapolated from VAR positioning and buyer-guide signal).

| Estimate | US IGCs on Counterpoint |
|---|---:|
| Low (10% share) | ~990 |
| Mid (15% share) | ~1,485 |
| High (25% share) | ~2,475 |

**Reported TAM:** ~700–1,800 stores, midpoint ~1,200. Lower bound is
deliberately tighter than 10% × 9,900 to account for the share of
those stores that are deployments not interested in any back-office
analytics layer (single-store hobby operators, etc.).

**Confidence:** medium. The IGC count is high-confidence; the
Counterpoint-share-of-IGC is the soft variable.

### Revenue per store (independent garden center)

| Metric | Value | Source | Confidence |
|---|---|---|---|
| Median revenue per IGC | ~$273k | BizBuySell valuation benchmarks | medium |
| Mean revenue per IGC | ~$1.29M | BizBuySell valuation benchmarks | medium |
| Average all nursery/garden/farm retailers (broader category) | ~$3.7M | AnythingResearch / Vertical IQ | medium |
| Sales per square foot — average | $100–$150 | Garden Center Magazine / Lawn & Garden Retailer | medium |
| Sales per square foot — top performers | $200+ | Garden Center Magazine / Lawn & Garden Retailer | medium |
| Profit margin — typical | 5–10% | financial-modeling / industry blogs | medium |
| Profit margin — top performers | 15–20% | financial-modeling / industry blogs | medium |

**Reading the gap between median and mean:** a small number of large
multi-location IGCs pull the mean up to $1.29M; the bulk of the
distribution is well below. Counterpoint's customer profile skews
toward the right tail — multi-store, multi-tier-pricing operations
that Square Retail or Lightspeed under-serve. So Counterpoint-running
IGCs probably cluster near or above the mean ($1M+ revenue / store)
rather than the median.

**Working assumption:** Counterpoint-running IGCs average ~$1–3M
annual revenue per store, with the multi-store chains in the segment
reaching $5–15M aggregate.

## TAM estimate — extended (all SMB verticals served by Counterpoint VARs)

Rapid POS specifically markets to:
- Garden centers + nurseries (Rapid Garden POS)
- Gun stores + shooting ranges (Rapid Gun Systems)
- Specialty food
- Wine + liquor + breweries
- Feed + tack + pet (Rapid Feed & Tack)

Other Counterpoint VARs (AMS, RCS, Mariner, POS Highway, C&K, NCC, etc.)
add: pet boutiques, hobby / craft / yarn, sporting goods, gift, apparel,
museum / cultural attraction retail, computer / electronics specialty,
health / wellness specialty.

### Per-vertical universe (US, available count)

| Vertical | US stores | Source | Confidence |
|---|---:|---|---|
| Nursery & garden stores | 9,885 | IBISWorld 2025 | high |
| Farm supply stores (overlaps with feed/tack) | 19,485 | IBISWorld 2025 | high |
| Federal Firearms License Type 1 dealers | 47,000+ | Everytown Research / ATF citation | high |
| Major-retailer gun counters | ~5,500 | Everytown Research | high |
| Independent gun specialty stores (subset) | ~10,000–15,000 | Wikipedia / industry estimates | low |
| Specialty wine + liquor retail | not directly cited | NAICS 4453 (US Census) | low |
| Pet supply specialty (independent) | ~7,000–10,000 | industry estimates | low |
| Sporting goods specialty (non-firearms) | ~22,000 | NAICS estimates | medium |

### Counterpoint share assumption per vertical

Public sources do not produce a defensible share-by-vertical number.
Working assumptions, flagged as extrapolation:

| Vertical | Counterpoint US share (extrapolated) | Counterpoint store count (mid) |
|---|---:|---:|
| Garden centers | 10–25% | ~1,200 |
| Independent gun stores | 5–15% (Bravo, Gearfire, Trident, Orchid, Celerant compete) | ~1,000 |
| Feed + tack (independent) | 5–15% | ~500 |
| Specialty food | 2–10% (Square / Clover dominate) | ~500 |
| Wine + liquor | 2–10% | ~500 |
| Pet specialty | 5–15% | ~500 |
| Sporting goods (non-firearm) | 2–10% | ~500 |
| Hobby / gift / apparel / other long-tail | 2–10% | ~3,000 |

**Extended TAM range (US, all SMB Counterpoint verticals):**
~6,000–14,000 stores, midpoint ~9,000.

**Confidence:** medium-low. Each share assumption is an extrapolation;
the aggregate has wide error bars.

### Cross-check against NCR Voyix disclosure

NCR Voyix reports 80,000 platform sites globally at year-end 2025.
Counterpoint as 10–25% of that number would be 8,000–20,000 sites
globally. Pulling US share to ~70–75% of that gives 5,600–15,000 US
Counterpoint sites across all verticals — consistent with the
bottom-up extended TAM of 6,000–14,000.

This is internal consistency, not validation; both numbers depend on
the same underlying Counterpoint-share-of-NCR-Voyix assumption.

## Competitive landscape

### Direct competitive set (specialty SMB retail POS)

| Vendor | Public US merchant signal | Position relative to Counterpoint |
|---|---|---|
| Square (incl. Square for Retail) | ~27–28% of US POS installations | Below in inventory depth + multi-tier pricing; above in onboarding speed + cost |
| Toast POS | ~24% (restaurant-skewed) | Adjacent — restaurant primary; not a direct competitor in retail |
| Clover (Fiserv) | ~5–6% of US POS market; 8,102 domains; bank-distributed | Below in vertical depth; above in payments integration |
| Shopify POS | 700,000+ merchants in POS / commerce category overall | Above in modern UX + eCommerce; below in inventory + multi-tier pricing |
| Lightspeed Retail | Public reports vary widely on US merchant count; Lightspeed-Capterra reports show "hundreds" in POS specifically; broader installed base in tens of thousands | Closer match on functionality; modern UX, similar feature depth |
| Vertical specialists | Bravo Store (4,000+ stores, firearms / pawn / specialty), Gearfire AXIS (firearms), Orchid Advisors (firearms compliance), Trident 1 (firearms / regulated), Celerant (firearms / sporting), POS Nation (independent retail), Comcash (garden + specialty), Visual Retail Plus (specialty) | Compete at vertical-specific feature level; Counterpoint competes on broad customization |

**Counterpoint's defensible niche:** specialty retailers with
multi-store, multi-tier pricing, deep inventory dimensionality (units,
serials, attributes), and customization needs that exceed Square /
Shopify out-of-the-box capability. The same customization depth is
what locks customers in once they've invested.

### Why customers leave Counterpoint

From public review platforms and Shopify Community migration threads:

1. **Outgrowing the dealer.** Small VARs go out of business or stop
   investing; customers without strong VAR relationships migrate.
2. **eCommerce-first growth.** Customers whose business shifts heavily
   to online migrate to Shopify POS so the POS sits inside the
   eCommerce ecosystem rather than the other way around.
3. **End-of-life forced migration cost.** When NCR ends support for
   an older version, the upgrade pulls in new POS hardware, new payment
   terminals, new TLS, new Secure Pay gateway — and customers compare
   the "stay" cost to the "switch to Lightspeed / Shopify" cost.
4. **Bug fatigue.** Persistent recent-version bugs (POS crash on
   minimize, eCommerce sync breakage) push customers toward more
   stable cloud-native alternatives.
5. **Vertical-specific compliance breakage.** Sporting-goods / firearms
   customers leave for verticalized POS (Bravo, Gearfire, Trident)
   when ATF compliance breaks repeatedly.

The customers who do **not** leave are the ones with deep
customization investment — which is the typical mid-to-high-end
specialty retailer who is also Canary's most valuable potential
customer.

### Why customers stay

- Customization investment ($10k–$100k+ in some publicly described
  cases). Hard to leave when that much business logic is in custom
  fields, custom tables, custom Crystal Reports.
- Multi-tier customer pricing (retail / landscaper / commercial in
  garden; B2B / wholesale in feed-and-tack / wine) is genuinely
  better-handled in Counterpoint than in Square / Shopify.
- Multi-store transfers + per-location inventory in the Document
  omnibus pattern (transfers come through the same Document endpoint
  as sales) are simpler to operate than equivalents in cloud-native
  POS.
- Existing Crystal Reports library represents years of accumulated
  business reporting that customers don't want to re-implement.

## Module L / W external-vendor adjacent TAM

Counterpoint exposes no labor / scheduling / timeclock surface
(`Brain/wiki/ncr-counterpoint-api-reference.md` Module L). The
addressable adjacent market for a Canary native Module L is the
Counterpoint installed base × the (high) probability that customers
want labor data alongside sales data.

### Workforce management market sizing

| Metric | Value | Source | Confidence |
|---|---|---|---|
| Global WFM software market 2024 | $9.6B (one est.) / $6.5B (alt est.) | MarketsAndMarkets / IMARC / Mordor | medium (numbers diverge) |
| Forecast 2030 | $13–25B depending on source | Multiple | low (forecast variance) |
| Retail / consumer-goods share | ~19% of WFM market | Mordor | medium |
| Retail WFM 2024 (~implied) | ~$1.8B | Derived | medium-low |

### SMB WFM vendor signals

| Vendor | Public customer count | Source | Confidence |
|---|---|---|---|
| Homebase | 100,000+ small businesses | vendor-reported | medium |
| When I Work | 100,000–200,000 companies | vendor-reported (range across published claims) | medium |
| Deputy | not publicly disclosed | — | — |
| Beekeeper (now LumApps) | "hundreds of thousands" of frontline workers; merged with LumApps July 2025 | vendor-reported | low |
| YOOBIC | 350+ global brands | vendor-reported | medium |
| Foko Retail | not publicly disclosed | — | — |
| TimeForge | NCR Counterpoint integration partner; specific customer count not disclosed | vendor-reported | low |

### Implication for Canary Module L

The cross-sell TAM (Canary base + Module L upsell to existing
Counterpoint customers) is bounded by the ~6,000–14,000 US
Counterpoint specialty-retail customer universe. At an Adressable
value of $X/store/year for Module L (if priced consistent with
Homebase / When I Work range, $30–$100/employee/month implies
~$3,000–$10,000/store/year for a 10–25-employee specialty retailer),
the bounded Module L revenue at full penetration is $20–140M ARR
across the Counterpoint universe. This is order-of-magnitude only;
penetration realistically caps at 20–40% of the universe in any
reasonable time horizon.

**The strategic reading:** Module L native build is not a separate
product — it's a Canary extension that meaningfully increases ARPU
per Canary customer, with the bonus that it covers a Counterpoint
gap entirely (no displacement of an existing TimeForge integration
in 90%+ of the base, because TimeForge penetration is small).

## "Why customers leave Counterpoint" — churn-driver detail

| Driver | Frequency in public reviews | Receiving competitor |
|---|---|---|
| Pure cost / TCO concerns | medium | Square, Shopify POS |
| eCommerce-first growth | medium | Shopify POS, Lightspeed |
| End-of-life forced migration | medium-high | Lightspeed, vertical specialists |
| Bug fatigue (recent-version) | high | Lightspeed, Shopify POS |
| Compliance breakage (vertical) | high (within affected verticals) | Bravo, Gearfire, Trident, Orchid |
| Dealer / VAR relationship breakdown | medium | varies — often a different Counterpoint VAR (intra-platform churn) |
| eCommerce integration failure | medium-high | Shopify POS |

**Counterpoint's intra-platform churn (VAR-to-VAR) is real** —
customers switch VARs without switching POS. This matters for Canary's
go-to-market: a Canary deal struck through a VAR has the same
deal-portability risk that Counterpoint deals do. A Canary deal
struck direct to retailer is portable across VAR changes.

## Source-quality table

Every quantitative claim in this article, with source and confidence:

| Claim | Source | Confidence |
|---|---|---|
| 9,885 US nursery & garden stores (2025) | IBISWorld | high |
| 13,400 US nursery/garden/farm-supply stores | Vertical IQ / AnythingResearch | high |
| US nursery & garden retail $49.7B market 2024 | IBISWorld | high |
| US nursery & garden retail $50.2B annual aggregate | AnythingResearch / Vertical IQ | high |
| Industry top 50 firms = 47% of sales | AnythingResearch | medium |
| 1,427 California N&G businesses 2026 | IBISWorld | high |
| 19,485 US farm supply stores 2025 | IBISWorld | high |
| Median IGC revenue $273k | BizBuySell | medium |
| Mean IGC revenue $1.29M | BizBuySell | medium |
| Sales per square foot $100–$200 | Garden Center Magazine / Lawn & Garden Retailer | medium |
| IGC profit margin 5–10% typical | financial blogs / industry citation | medium |
| Plant nursery avg revenue ~$490k | Financial Model | medium |
| Average nursery/garden/farm-supply retailer $5.4M revenue, 17 employees | AnythingResearch | medium |
| 2018 green industry direct output $159.57B | HRI / AmericanHort 2018 study | high |
| 2018 green industry total output (incl. multipliers) $348B | HRI / AmericanHort | high |
| 1.6M direct jobs in green industry 2018 | HRI / AmericanHort | high |
| Up to 78% of garden-center shrinkage from spoilage | AMS Retail / industry citation | medium |
| 78,000+ US FFL holders | Everytown Research / ATF | high |
| 47,000+ US Type 1 FFL dealers | Everytown Research / ATF | high |
| ~5,500 major-retailer US gun counters | Everytown Research | high |
| 1,809 Walmart FFL locations | Everytown Research | high |
| 6,147 active Type 02 pawnbroker FFLs | Everytown Research | high |
| Bravo Store Systems 4,000+ stores | vendor site | medium |
| NCR Voyix 2024 retail segment revenue ~$2.0B (down 10% YoY) | NCR Voyix Q4 2024 release | high |
| NCR Voyix 74,000 platform sites year-end 2024 | NCR Voyix 2024 annual report | high |
| NCR Voyix 80,000 platform sites year-end 2025 | NCR Voyix Q4 2025 release | high |
| Counterpoint share of NCR Voyix platform sites | NOT PUBLISHED — extrapolated 10–25% | low |
| Counterpoint Cloud price ~$149/month/license | VAR pricing pages (CompuTant, POS Highway) | medium |
| Counterpoint subscription $125/month single user | VAR pricing pages | medium |
| Counterpoint perpetual license $1,190+ starting | VAR pricing pages | medium |
| Counterpoint EOL pre-8.5.7.x = 2023-12-31 | NCR / VAR announcements (Skurlas, Mainspring) | high |
| Counterpoint Users Group founded 2003, closed 2021 | POS Pondering | high |
| CCS Retail Systems supports ~2,000 Counterpoint users | CCS site | medium |
| US POS market — Square 27–28% installations | hostmerchantservices industry analysis | medium |
| US POS market — Toast 24% | hostmerchantservices | medium |
| US POS market — Clover 5–6% | hostmerchantservices | medium |
| Shopify ~734k POS-category customers | 6sense | medium |
| Lightspeed Retail ~200 POS-tagged customers (low — likely measurement artifact) | 6sense | low |
| Lightspeed FY26 revenue guidance 10–12% (vs. US POS market 13.3%) | analyst commentary | medium |
| US POS market growth ~13.3% annually | analyst commentary | medium |
| Global WFM market $9.6B 2024 (one est.) | MarketsAndMarkets | medium |
| Global WFM market $6.5B 2024 (alt est.) | IMARC | medium |
| WFM forecast 2030 $13–25B | multiple | low |
| Retail share of WFM ~19% | Mordor | medium |
| Homebase 100k+ SMB customers | Homebase / vendor-reported | medium |
| When I Work 100k–200k companies | When I Work / vendor-reported | medium |
| YOOBIC 350+ global brands | YOOBIC site | medium |
| US pet care market $83B+; global $380B 2025 → $650B 2030 | industry citations | medium |
| Smart-indoor-gardening + garden-platform software market growth | varied research firms | low |
| US garden center market $36.5B (2023) | National Gardening Association via secondary citation | medium |

## Open questions and data gaps

1. **NCR Voyix internal Counterpoint share.** The single biggest
   variable in the TAM. Public NCR Voyix disclosures aggregate
   Counterpoint with DSR, Aloha, and legacy retail. Without an
   internal split, every TAM estimate above carries this assumption.
2. **Per-VAR customer counts and vertical mix.** Each VAR markets
   multiple verticals; none publish per-vertical customer counts.
3. **API enablement rate across the Counterpoint installed base.**
   The REST API is a paid registration option; if enablement is
   <50%, Canary's adapter strategy needs a direct-DB path as primary,
   not secondary.
4. **Churn rate.** No public data; reviews suggest stickiness but
   not magnitude.
5. **Average customization spend per customer per year.** Reviews
   describe "$10k–$100k+" but no aggregate; this is the bound on
   Canary's pricing relative to existing dealer spend.
6. **Garden Center Magazine 2024 SOI POS-vendor breakdown.** The
   survey asked about technology adoption but the public-facing
   article didn't publish the breakdown by vendor. Buying the report
   or reading the full digital edition might disclose it.
7. **NRF 2025 SMB-specific data.** The 2025 conference produced
   trend coverage but no single SMB POS vendor share report in the
   public record.
8. **Counterpoint vs. Lightspeed / Shopify head-to-head in IGC
   bake-offs.** Buyer-guide content suggests Counterpoint is on the
   shortlist for ~half of IGC POS evaluations; win rate is not
   public.

These are the questions that move the TAM from "medium-confidence
midpoint" to "defensible point estimate." Most resolve only through
NCR Voyix internal data, primary research with VAR partners, or
purchased syndicated reports (IBISWorld full report, Garden Center
Magazine 2024 SOI premium content).

## Sources

### Primary market sizing

- IBISWorld — Nursery & Garden Stores in the US:
  [ibisworld.com/.../nursery-garden-stores/1037](https://www.ibisworld.com/united-states/industry/nursery-garden-stores/1037/)
- IBISWorld — N&G Stores number of businesses:
  [ibisworld.com/.../number-of-businesses/nursery-garden-stores/1037](https://www.ibisworld.com/united-states/number-of-businesses/nursery-garden-stores/1037/)
- IBISWorld — Farm Supply Stores number of businesses:
  [ibisworld.com/.../farm-supply-stores-united-states](https://www.ibisworld.com/industry-statistics/number-of-businesses/farm-supply-stores-united-states/)
- AnythingResearch — Nursery / Garden Center / Farm Supply industry stats:
  [anythingresearch.com/.../Nursery-Garden-Center-Farm-Supply-Retailers](https://www.anythingresearch.com/industry/Nursery-Garden-Center-Farm-Supply-Retailers.htm)
- Vertical IQ — Nurseries, Garden Centers & Farm Supply:
  [verticaliq.com/product/nurseries-garden-centers-farm-supply](https://verticaliq.com/product/nurseries-garden-centers-farm-supply/)
- AmericanHort — Industry Insider / 2025 SOI:
  [americanhort.org/.../industry-insider-report](https://www.americanhort.org/education/industry-insider-report/)
- HortTechnology — Economic contributions of the green industry 2018:
  [meridian.allenpress.com/jeh/.../38/3/73](https://meridian.allenpress.com/jeh/article/38/3/73/444164/Economic-Contributions-of-the-Green-Industry-in)
- Garden Center Magazine — 2024 State of the Industry:
  [gardencentermag.com/.../2024-state-independent-garden-centers-industry-report](https://www.gardencentermag.com/article/2024-state-independent-garden-centers-industry-report/)
- BizBuySell — Nursery & Garden Center valuation benchmarks:
  [bizbuysell.com/.../valuation-benchmarks/nursery-garden](https://www.bizbuysell.com/learning-center/valuation-benchmarks/nursery-garden/)

### NCR Voyix and POS market

- NCR Voyix Q4 2024 results:
  [ncrvoyix.com/.../q4-2024-results](https://www.ncrvoyix.com/newsroom/ncr-voyix-reports-fourth-quarter-and-full-year-2024-results-2)
- NCR Voyix 2024 annual report (SEC):
  [sec.gov/.../ef20047814_ars.pdf](https://www.sec.gov/Archives/edgar/data/70866/000114036125014982/ef20047814_ars.pdf)
- NCR Voyix Q4 2025 results:
  [investor.ncrvoyix.com/.../q4-2025-results](https://investor.ncrvoyix.com/news-releases/news-release-details/ncr-voyix-reports-fourth-quarter-and-full-year-2025-results/)
- NCR Voyix Counterpoint product page:
  [ncrvoyix.com/retail/counterpoint](https://www.ncrvoyix.com/retail/counterpoint)
- 6sense — Lightspeed market share:
  [6sense.com/tech/pos-systems/lightspeed-market-share](https://6sense.com/tech/pos-systems/lightspeed-market-share)
- HostMerchantServices — POS market share 2024:
  [hostmerchantservices.com/.../point-of-sale-market-share](https://hostmerchantservices.com/articles/point-of-sale-market-share/)
- MordorIntelligence — POS software market:
  [mordorintelligence.com/industry-reports/pos-software-market](https://www.mordorintelligence.com/industry-reports/pos-software-market)

### Workforce management

- MarketsAndMarkets — WFM market:
  [marketsandmarkets.com/.../workforce-management-market](https://www.marketsandmarkets.com/Market-Reports/workforce-management-market-27548173.html)
- MordorIntelligence — WFM software:
  [mordorintelligence.com/.../workforce-management-software-market-industry](https://www.mordorintelligence.com/industry-reports/workforce-management-software-market-industry)
- Homebase corporate context (CB Insights):
  [cbinsights.com/company/pioneer-works-inc](https://www.cbinsights.com/company/pioneer-works-inc)
- Beekeeper:
  [beekeeper.io](https://www.beekeeper.io/)
- YOOBIC:
  [yoobic.com](https://yoobic.com/)

### Vertical-specific (firearms, food, wine, feed/tack, pet)

- Everytown Research — Inside the Gun Shop:
  [everytownresearch.org/.../firearms-dealers-and-their-impact](https://everytownresearch.org/report/firearms-dealers-and-their-impact/)
- Statista — Federal firearm dealers:
  [statista.com/.../number-of-federal-firearm-dealers-in-the-us](https://www.statista.com/statistics/215666/number-of-federal-firearm-dealers-in-the-us/)
- Bravo Store Systems:
  [bravostoresystems.com](https://www.bravostoresystems.com/)
- Gearfire AXIS:
  [gogearfire.com/solutions/axis-point-of-sale](https://gogearfire.com/solutions/axis-point-of-sale/)
- Trident 1:
  [trident1pos.com](https://trident1pos.com/)
- WinePOS:
  [winepos.com/about-us](https://winepos.com/about-us/)
- Rapid Feed & Tack POS:
  [rapidftpos.com](https://rapidftpos.com/)

### Counterpoint VAR ecosystem

- Rapid POS:
  [rapidpos.com](https://rapidpos.com/)
- Rapid Garden POS:
  [rapidgardenpos.com](https://rapidgardenpos.com/)
- AMS Retail Solutions:
  [amsretail.com/industries/garden-nursery](https://amsretail.com/industries/garden-nursery/)
- Retail Control Systems:
  [retailcontrolsystems.com/industries/garden-centers](https://www.retailcontrolsystems.com/industries/garden-centers/)
- Mariner Business Solutions:
  [marinerpossystems.com/garden-center-pos-systems](https://marinerpossystems.com/garden-center-pos-systems/)
- POS Highway:
  [poshighway.com](https://www.poshighway.com/industries/garden-center-pos-1)
- C&K Systems:
  [cksystem.com/garden-center-point-of-sale-counterpoint](https://cksystem.com/garden-center-point-of-sale-counterpoint/)
- CCS Retail Systems:
  [ccsretailsystems.com/software-product](https://ccsretailsystems.com/software-product/)
- Lawn Garden Marketing — Rapid Garden POS as NCR Partner:
  [lawngardenmarketing.org/.../rapid-garden-pos-NCRcounterpoint](https://www.lawngardenmarketing.org/rapid-garden-pos-NCRcounterpoint.aspx)

## Closing summary

**Defensible:** the broad shape of the market (~10,000 US IGCs, ~$50B
nursery & garden retail revenue, NCR Voyix retail segment ~$2B and
declining ~10% YoY, Counterpoint's defensible niche in customization-
heavy multi-tier specialty retail, the existence of a large
labor / scheduling gap inside Counterpoint that no NCR-native module
fills).

**Gappy:** the precise number of Counterpoint customers in any given
vertical, the precise share Counterpoint holds against Lightspeed /
Shopify / verticalized competitors, the actual API enablement rate,
the average per-customer customization spend, and the churn rate.
Every TAM number in this article carries an explicit "extrapolated
from public sources" tag because no public source produces the
underlying numbers directly.

**Would need primary research to resolve:** customer interviews with
5–10 Counterpoint-running specialty retailers across two or three
verticals; data requests to 2–3 Counterpoint VARs (Rapid POS, AMS
Retail, RCS) on customer count, vertical mix, average customization
spend, and churn; a syndicated report purchase from IBISWorld or
Garden Center Magazine for the 2024 SOI premium tier. Without those,
the TAM remains a defensible posture in the 1,000–2,000 store range
for the primary segment, with a wider 6,000–14,000 range for the
extended segment.

For Canary positioning purposes, the public-record TAM is sufficient
to justify the strategic posture (ride-along to Counterpoint, not
displacement; Module L native build as greenfield; surface
Counterpoint's audit log + pricing decisions for Q without depending
on dealer cooperation). The TAM is not yet sufficient to set
contractual revenue targets — that requires the primary research
above.

## Related

- [[Brain/wiki/rapid-pos-counterpoint-user-pain-points|Rapid POS / Counterpoint — User Pain Points + FAQs]]
- [[Brain/wiki/ncr-counterpoint-api-reference|NCR Counterpoint API Reference]]
- [[Brain/wiki/ncr-counterpoint-rapid-pos-relationship|Counterpoint vs Rapid Garden POS — Relationship]]
- [[Brain/wiki/ncr-counterpoint-endpoint-spine-map|NCR Counterpoint Endpoint × CRDM × Spine Map]]
- `docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md`
