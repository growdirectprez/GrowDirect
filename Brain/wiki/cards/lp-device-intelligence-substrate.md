---
card-type: platform-thesis
card-id: lp-device-intelligence-substrate
card-version: 1
domain: canary
layer: cross-cutting
status: draft
agent: ALX
last-compiled: 2026-05-02
needs-review: true
feeds:
  - platform-gateway-thesis
  - vertical-smb-health-hypothesis
  - growdirect-pitch-spine
receives:
  - platform-thesis
  - concept-identity-layer-triad
  - concept-substrate-discipline
  - 2026-05-02-platform-trust-boundary-architecture
  - 2026-05-02-agent-commissioning-protocol
tags:
  - loss-prevention
  - device-intelligence
  - fingerprinting
  - orc
  - ecommerce-fraud
  - gift-card-fraud
  - carding
  - cross-tenant-network-effect
  - accelerator-pack
  - investigator
  - evidentiary-rail
---

# LP Device Intelligence Substrate

## What this is

Device intelligence — the capability to recognize a specific device-and-party combination across sessions, accounts, surfaces, and platforms — is the substrate that makes specialty-retail loss prevention a *complete coverage model* rather than a discrete in-store function. The same fingerprint substrate that hardens authentication ([[2026-05-02-platform-trust-boundary-architecture]] §Device Registration & Attestation) becomes the observability layer over the theft-to-monetization pipeline that every specialty retailer is bleeding into and no single retailer can see in full.

The substrate is one. The applications are four-plus, spanning in-store theft, e-commerce fraud, external resale of stolen merchandise, organized-retail-crime ring identification, stolen-card-data resale, and the gift-card-fraud category that has become the favored monetization path for stolen credit card data. The cross-tenant signal under tenant consent is the network-effect moat. The Canary platform thesis is built on the substrate that makes this offering legitimate, defensible, and architecturally clean.

## Purpose

Big-box retail has loss prevention. They have ORC investigation teams. They subscribe to LexisNexis, Sift, Riskified, the commercial fraud intelligence vendors. They share signal through industry consortia (RILA's ORC committee, the National Retail Federation's loss prevention research). They have private device intelligence pipelines built in-house at the cost of nine-figure technology budgets.

Specialty retail has none of this. The independent retailer with $5M–$50M in revenue cannot afford the commercial fraud substrate, has no in-house investigation team, has no consortium membership, and gets fleeced repeatedly by the same actors hitting the same vertical across town and across state lines. The same fingerprint that defrauded a Counterpoint specialty pharmacy in Phoenix on Tuesday defrauds the same vertical in Tucson on Thursday, and neither retailer ever knows.

The accelerator-pack thesis ([[platform-gateway-thesis]]) names this gap directly: *the analyst, architect, developer, delivery lead, support engineer, training designer, change manager, and CSM the independent retailer was never going to hire*. Add to that list: **the loss prevention investigator the independent retailer was never going to hire** — running as a runtime function over the substrate, with the cross-tenant network effect that even the commercial vendors cannot easily match because they lack the tenant-consent substrate to pool the signal legitimately.

This card establishes device intelligence as a substrate-layer capability — not a feature in one module, but a horizontal layer that lights up loss prevention as a complete platform offering across in-store, e-commerce, marketplace, and cross-tenant surfaces.

## The theft-to-monetization pipeline

The load-bearing reframe is that retail theft is a supply chain, not a series of independent events. The pipeline:

```
THEFT                  →   FENCING / CONVERSION       →   MONETIZATION
─────                      ─────────────────────          ─────────────
In-store shoplift          eBay / FB Marketplace          Cash to thief
Boost crew theft           OfferUp / Mercari              Cash to ring
Inside-job pilferage       Craigslist                     Cash through layers
Return fraud               Pawn / fence shops             Cryptocurrency
Online order fraud         Flea markets                   Payment apps
Carded gift cards          Gift card resale (Raise,       Restocked supply
Stolen credit card data        CardCash, Reddit)              for next cycle
Phishing → carding         Carding marketplaces           
                               (Russian Market,
                                BriansClub, etc.)
```

The individual retailer sees the **theft** column from their own surface. They have no native visibility into the **fencing** or **monetization** columns. The theft economy depends on the fencing-and-monetization layer being observable to the participants but invisible to the victims. That asymmetry is the gap the device intelligence substrate closes.

A single device fingerprint is the connective tissue across the columns:

- The fingerprint that stole the in-store merchandise via a returns-fraud scheme is also the fingerprint listing the items on Facebook Marketplace
- The fingerprint that placed the fraudulent online order at retailer A is the same fingerprint that placed similar orders at retailer B and C across the Canary tenant base
- The fingerprint that bought $500 of Walmart gift cards with a stolen credit card is the same fingerprint listing those gift cards on Raise.com at 78 cents on the dollar
- The fingerprint that operated a carding marketplace seller account is observable across the seller's own profile pages, the dropshipping sites the carded data is tested against, and the gift card resale exits

The substrate observes. The substrate fingerprints. The substrate anchors the pattern to the evidence chain. The substrate surfaces the actionable case to the retailer or to the authorized investigator. The substrate respects tenant consent for cross-retailer signal pooling. The substrate respects platform-of-record terms of service for marketplace observation. None of this is novel as individual capabilities — it is novel as a *coherent platform offering at specialty retail's price point and scale*.

## Coverage model — five quadrants

| Quadrant | Surface | What the substrate does | Existing platform module |
|---|---|---|---|
| **Q1 — In-store theft** | Retailer's POS, video, returns desk | Anchor the theft event to the substrate (existing); fingerprint the returning party where digital surface (returns app, e-receipt) is touched | Q (Loss Prevention), Fox (Case Management) |
| **Q2 — E-commerce fraud at retailer's own surface** | Retailer's own e-commerce site | Fingerprint every visitor; flag repeat-offender device patterns across accounts, payment methods, addresses; step up auth on suspicious devices; block at threshold | Extension to existing e-commerce integration surface |
| **Q3 — External resale of stolen merchandise** | Public marketplaces (eBay, FB Marketplace, OfferUp, Mercari, Craigslist) | Retailer reports stolen items (SKU, serial, distinguishing characteristics); platform monitors public marketplaces under retailer's authorized-investigator scope; fingerprints sellers of matching listings; surfaces ORC ring membership when same fingerprint appears across multiple "different" seller accounts | New — Q + Fox extension; Investigator party type per [[2026-05-02-platform-trust-boundary-architecture]] |
| **Q4 — Cross-tenant ORC ring identification** | Canary tenant base, with consent | Pool device-intelligence signal across opted-in tenants; surface ring-identification alerts when same fingerprint hits multiple retailers in the network; cross-vertical and cross-geography | New — substrate primitive; cross-tenant consent contract per [[concept-identity-layer-triad]] |
| **Q5 — Stolen card data and gift card fraud monetization** | Retailer's own surface + secondary card-resale markets + gift card resale platforms | Detect carded purchases at retailer surface (fingerprint + transaction velocity + payment-method drift); detect gift cards bought with carded data appearing on resale markets; trace fingerprint patterns from monetization layer back to original fraudulent purchase | New — Q + F (Finance) + new fraud-intelligence module |

The five quadrants are not independent products. They are facets of one substrate offering. A retailer subscribed to the loss-prevention accelerator-pack capability gets all five — Q1 because Canary already does it, Q2-Q5 because the substrate makes them substantially the same engineering investment once the device intelligence layer exists.

## The gift card fraud subcategory — why it warrants explicit treatment

Gift card fraud has become the dominant monetization path for stolen credit card data because gift cards convert plastic-stolen-card to fungible-spendable-value with high anonymity. The subspecies the substrate addresses:

| Subspecies | Pattern | Substrate detection |
|---|---|---|
| **Card draining** | Thief steals physical gift cards from racks, records the numbers, returns the cards; monitors balance via the issuer's check-balance surface; drains when victim activates | Fingerprint the balance-check device; pattern-match drain-after-activation timing; cross-reference with retailer's reported physical-card-theft events |
| **Carded gift card resale** | Thief buys gift cards with stolen credit card; sells gift cards on resale platforms (Raise, CardCash, Reddit r/giftcardexchange) at 65–80 cents on the dollar | Fingerprint the purchase device at retailer; fingerprint the seller device on resale platform; correlate; surface chain to retailer + Fox case |
| **Triangulation fraud** | Thief uses stolen card to buy gift card from retailer; sells gift card for cash/crypto; retailer eats the chargeback when the cardholder disputes | Same as above — fingerprint correlation between purchase and resale surfaces is the smoking gun |
| **OTP / code interception fraud** | Phishing victims into reading gift card codes over phone (the "tax scam," "warrant scam," "tech support scam"); thief redeems codes through gift card resale or direct conversion | Cross-reference gift card redemption patterns from mass-phishing-active periods; fingerprint redemption device; trace |
| **Refund fraud via gift card** | Return stolen merchandise without receipt; receive gift card; sell gift card | Q1 + Q5 chain — connect the no-receipt return event to the subsequent gift card resale fingerprint |

Gift card fraud is the most operationally damaging fraud category for specialty retail because the chargeback economics are brutal and the victim retailers are not party to the resale market where the monetization completes. The substrate's ability to *trace from the resale market backward to the originating fraudulent purchase* is what turns gift card fraud from an unsolvable nuisance into a prosecutable case.

## Substrate dependencies

This capability does not require new substrate primitives. Every dependency is in flight or already designed:

| Dependency | Source | Status |
|---|---|---|
| Device registration with party binding | [[2026-05-02-platform-trust-boundary-architecture]] §Device Registration & Attestation | Specified v0; awaiting fingerprinting substrate decision (FingerprintJS open-source recommended for v0 per Open Question 8) |
| Investigator party type with time-bounded authority-instrument scope | [[2026-05-02-platform-trust-boundary-architecture]] §Party Taxonomy | Specified v0; investigator authorization workflow founder-mediated for v0 |
| Cross-tenant consent contract substrate | [[concept-identity-layer-triad]] §Consent-based projection | Architectural pattern locked; specific contract template for cross-tenant LP signal sharing needs drafting |
| Evidentiary rail (L2 hash anchoring) | [[platform-thesis]] · Rail 3 | Architectural pattern locked; application to fingerprint-pattern evidence is productization, not substrate change |
| Q (Loss Prevention) module | Canary Go module spine | Build-prep underway per [[platform-gateway-thesis]] |
| Fox (Case Management) module | Agent PMO architecture | Domain agent specified per [[2026-04-28-canary-go-agent-pmo-architecture-design]] |
| Marketplace observation framework | New — productization concern | Needs SDD; Investigator-party-type-anchored authorized investigation, not general scraping |
| Cross-tenant signal-pooling and pattern-matching engine | New — productization concern | Needs SDD; cross-tenant query substrate with consent-contract enforcement |

The work to productize this is **integration and contract**, not substrate invention. That is the architectural payoff of having built the substrate right.

## Vertical applicability

The substrate is vertical-agnostic by design (per [[concept-substrate-discipline]]). The loss prevention application has different urgency and economics by vertical:

| Vertical | Why the LP substrate matters | Specific monetization patterns |
|---|---|---|
| **SMB Health** (medical equipment, durable medical goods, controlled-substance-adjacent supplies) | High-value goods with FDA-tracked serial numbers; resale market exists in gray-market medical supply channels; controlled-substance-adjacent inventory has regulatory exposure on top of theft loss; ORC rings target high-margin medical inventory | Reseller listings on medical-equipment marketplaces; serial-number cross-reference against FDA tracking; investigator handoff to DEA / state pharmacy boards |
| **Liquor / spirits** | Premium spirits target for ORC; resale through bars, restaurants, secondary markets; gift card monetization significant | Bar / restaurant inventory pattern matching; gift card resale tracing |
| **Gun / firearms / sporting** | Federal serial number tracking; ATF involvement; high-stakes ORC; private sale market is the fence | ATF investigator handoff; private-sale platform observation |
| **Garden / lawn / outdoor power equipment** | Husqvarna, Stihl, Milwaukee tools — high theft value, heavy resale; manufacturer serial numbers | Marketplace serial cross-reference; pawn shop integration |
| **Grocery / specialty grocery** | Lower per-incident value, but high frequency; ORC rings hit 50+ stores on the same circuit; gift card fraud is heavy | Cross-tenant ring identification (Q4) is the dominant value; gift card monetization (Q5) is heavy |
| **Jewelry / luxury** | High per-incident value; resale through pawn, online, private sale; insurance fraud overlap | Cross-platform monitoring across luxury resale (The RealReal, eBay luxury, pawn) |
| **Hardware / building supply** | Power tools especially; jobsite theft pipeline into pawn and resale | Same as garden / lawn |

The SMB Health vertical is the highest-leverage first vertical for explicit LP-substrate productization because the value-per-event is high, the regulatory framing makes investigator handoff cleaner (DEA, state pharmacy boards, FDA), and the [[vertical-smb-health-hypothesis]] is the next vertical the platform is scoping. The cross-tenant network effect (Q4) is the biggest moat for the lower-per-event-value verticals (grocery, garden) because no single retailer in those verticals can afford the LP overhead, and the network signal is what makes the math work.

## Competitive frame

| Tier | Substrate | Cost | Specialty-retail availability |
|---|---|---|---|
| Big-box internal | In-house investigation team + commercial fraud vendors + RILA / NRF consortium | Nine-figure budget | None — gated by scale |
| Mid-market commercial | LexisNexis, Sift, Riskified, Forter, Signifyd | Five- to six-figure annual subscription minimum + per-transaction cost | Sometimes — gated by per-transaction economics on small basket sizes |
| Specialty retail today | Manual investigation; insurance writes off the loss; police reports go nowhere | None | None — the gap |
| **Canary LP substrate** | Open-protocol device intelligence + cross-tenant consent network + accelerator-pack runtime | Bundled with platform | The gap that becomes the moat |

The competitive moat is not the device intelligence substrate itself — that is buyable from FingerprintJS and Sift and others. The moat is **the cross-tenant consent substrate that pools specialty retailer signal under terms only Canary's platform thesis permits**. The commercial vendors can identify a fingerprint; they cannot legitimately tell merchant A that the same fingerprint is also defrauding merchants B, C, and D in the same vertical because their data licenses do not permit cross-merchant disclosure under that framing. The Canary substrate's tenant-consent contract architecture (per [[concept-identity-layer-triad]]) is what makes the cross-merchant disclosure legitimate — *because the merchant is an opted-in party to a contractual signal-sharing arrangement, not a counterparty whose data is being aggregated under a vendor's terms of service*.

The capability-language pitch (per [[platform-gateway-thesis]] §invariants — public artifacts use capability language only):

> *Independent retailers lose 1.4% of revenue to theft and fraud — and the same actors hit the same verticals across town and across state lines without the retailers ever knowing. We give them the loss prevention investigator they were never going to hire, the marketplace monitoring they could never staff, and the cross-retailer ring intelligence the big-box chains have had for a decade. One substrate. Five surfaces. Verifiable cost-to-serve. Cryptographic evidence on every case.*

## Productization open questions

| # | Question | Resolution path |
|---|---|---|
| OQ-1 | Marketplace observation legal posture — Investigator-party-type-anchored authorized investigation per retailer-reported items, or broader monitoring under platform-of-record terms? | Outside-counsel review required before Q3/Q5 substrate ships; recommend strict authorized-investigator framing for v0 with broader monitoring deferred to Phase 2 |
| OQ-2 | Cross-tenant consent contract — template, opt-in framing, opt-out mechanics | Sibling SDD needed; founder + counsel; recommend opt-in default with one-click opt-out, transparent signal-sharing dashboard for opted-in tenants |
| OQ-3 | Fingerprinting substrate — open-source FingerprintJS for v0 vs commercial FingerprintJS Pro vs custom WebAuthn-only | Per [[2026-05-02-platform-trust-boundary-architecture]] §Open Questions OQ-8; recommend open-source for v0, graduate to commercial when fraud volume or sales conversation warrants |
| OQ-4 | Marketplace targeting prioritization — eBay first (largest), Facebook Marketplace second (most ORC activity), or a vertical-specific resale market (carding marketplace, gift card resale)? | Founder gate; recommend eBay + Facebook Marketplace for v0 baseline (broadest signal); vertical-specific markets as accelerator-pack manifest entries |
| OQ-5 | Cross-tenant signal-pooling architecture — single shared pattern-match engine vs federated per-tenant matchers with cross-query | Architectural; recommend single engine with strict consent-contract enforcement per query; avoids the federation tax and matches the substrate-discipline thesis |
| OQ-6 | Fox case workflow extension — how does an LP case originate from a fingerprint pattern alert, what does the case packet contain, who can see it | Sibling SDD or Fox-module specification extension |
| OQ-7 | Investigator handoff substrate — for cases that go to law enforcement (DEA for medical, ATF for firearms, local PD for general theft), what does the platform produce as the handoff packet? | Sibling SDD; needs to interoperate with subpoena response substrate and the IR plan ([[ir-plan-v0.1]]) |
| OQ-8 | Pricing model — bundled with the accelerator pack, à la carte per quadrant, or tiered (Q1+Q2 baseline, Q3+Q4+Q5 premium)? | Founder gate; recommend bundled with accelerator pack for the network-effect economics (more participants = better signal for everyone) |
| OQ-9 | False positive handling — when a fingerprint pattern flags a legitimate customer, what is the recourse process and how does the substrate learn? | Productization concern; recommend dual-track — automated suppression on appeal + investigator review on disputed flags + signal-quality feedback to the pattern-match engine |
| OQ-10 | Vertical-specific substrate extensions — controlled-substance tracking for SMB Health, ATF integration for firearms, etc. | Per-vertical SDD as each vertical lights up |

## Consumers

| Consumer | What they do with this card |
|---|---|
| Specialty retail prospect conversation (Counterpoint VARs, Square SMB, future) | The substrate is the differentiated LP offering; the four-quadrant coverage is the deck slide; the cross-tenant network effect is the moat |
| SMB Health hypothesis ([[vertical-smb-health-hypothesis]]) | Direct vertical productization — medical equipment LP is one of the highest-value first applications |
| Bart conversation / DriftPOS joint product | LP substrate becomes part of the joint-product positioning ([[joint-product-positioning-pwc]]) — DriftPOS + Canary + LP substrate as a complete specialty-retail operating offering |
| Square partnership conversation | LP substrate is one of the operations + decision substrate capabilities ([[platform-gateway-thesis]] Layer 5) above-the-till that Square's marketplace cannot provide |
| Investor pitch | Network-effect moat is a TAM-expanding thesis — every retailer added increases the value to every other retailer |
| Linear epic dispatch (when scoped) | Productization plan; module spine extensions to Q + Fox; consent contract template; marketplace observation framework SDD |
| Brand voice plugin | Source for capability-language pitch on the LP substrate; tone calibration for investigator/legal-adjacent communication |

## Sources

| Source | Role |
|---|---|
| [[2026-05-02-platform-trust-boundary-architecture]] | Device registration substrate, party taxonomy (including Investigator), attestation depth ladder |
| [[concept-identity-layer-triad]] | Consent-based projection model that legitimizes cross-tenant signal sharing |
| [[platform-gateway-thesis]] | Accelerator-pack thesis that frames LP-substrate as the next runtime function |
| [[platform-thesis]] | Three accountability rails plus vendor accountability — LP substrate operates under all four |
| [[2026-04-28-canary-go-agent-pmo-architecture-design]] | Q (Loss Prevention) and Fox (Case Management) module ownership |
| [[ir-plan-v0.1]] | Incident response plan that intersects with investigator handoff substrate |
| [[vertical-smb-health-hypothesis]] | Vertical that benefits most acutely from LP substrate productization |
| [[joint-product-positioning-pwc]] | Joint-product positioning that LP substrate becomes part of |
| [[concept-substrate-discipline]] | Fractal rule that keeps LP substrate horizontal across verticals |
| [[2026-05-02-agent-commissioning-protocol]] | Agent commissioning model that the LP-substrate's pattern-match agent inherits |
| Industry: RILA ORC committee, NRF Loss Prevention Research Council | Big-box LP intelligence consortium precedent |
| Industry: LexisNexis Risk Solutions, Sift, Riskified, Forter, Signifyd, FingerprintJS | Commercial fraud-intelligence substrate precedent |
| Industry: card-resale and gift-card-resale market intelligence (open-source research) | Pattern data for the monetization-layer half of the pipeline |

## Invariants

Hard constraints. These are non-negotiable for the substrate to remain legitimate.

1. **Tenant consent is the gate for cross-tenant signal sharing.** No signal pooling happens without an active opted-in consent contract per tenant. Opt-out is one-click. Revocation is immediate at the substrate. The contract is itself an evidentiary chain entry.
2. **Authorized-investigator framing is the gate for marketplace observation.** Marketplace monitoring (Q3, Q5) operates on a per-reported-stolen-item basis under the retailer's investigator authorization, not as general scraping. The Investigator party type with time-bounded authority-instrument scope is the substrate primitive that enforces this.
3. **Device intelligence is transparent to the device owner where the device is on the platform.** Customer staff devices, customer-owned consumer devices on the retailer's e-commerce surface — every such device has a visible registration record viewable by the relevant party (staff sees their own; consumer sees their own; merchant admin sees all staff and all consumers under their tenant). One-click revocation. No silent fingerprinting of platform-resident devices.
4. **Marketplace-observed device intelligence is anchored to the investigation, not stored as ambient profile.** When the platform fingerprints a public seller profile on eBay under a retailer's authorized investigation, that fingerprint is associated with the case, not with a global "person" record. The substrate does not become an ambient surveillance database of marketplace participants.
5. **Evidence chain integrity is mandatory on every case.** Every fingerprint pattern that supports an LP case is hash-anchored to the L2 chain. A case packet that cannot prove its evidence chain does not get to be a case packet — same discipline as the broader evidentiary rail per [[platform-thesis]].
6. **Substrate respects platform-of-record terms of service.** Marketplace observation operates within the marketplace's published terms or with explicit marketplace partnership. No ToS-violating scraping. Where ToS prohibits the activity, the substrate does not perform the activity at that marketplace.
7. **False positive recourse is a substrate primitive, not a customer-service afterthought.** A fingerprint pattern that flags a legitimate customer must have a recourse path that is fast, visible, and tied to substrate signal-quality feedback. The substrate gets better when it learns from its mistakes; that loop is required, not optional.
8. **No facial recognition. No facial image gathering.** Per the platform's harmful-content posture and the substrate-discipline rule that the platform observes commercial behavior, not biometric identity. Device intelligence is the substrate; biometric intelligence is not.

## Routing

```
Theft event (in-store, e-commerce, return fraud, etc.)
  ↓
  Q (Loss Prevention) module
  ↓
  ├─→ Q1 surface: existing in-store anchor + fingerprint where digital
  │
  ├─→ Q2 surface: e-commerce fingerprint + repeat-offender pattern match
  │     ↓
  │     └─→ Per-tenant signal + (with consent) cross-tenant signal pool
  │
  ├─→ Q3 surface: marketplace observation under investigator authorization
  │     ↓
  │     └─→ Same fingerprint across listings → ORC ring case
  │
  ├─→ Q4 surface: cross-tenant pattern match
  │     ↓
  │     └─→ Cross-tenant ring alert delivered to participating retailers
  │
  └─→ Q5 surface: stolen-card-data + gift-card-fraud monetization tracing
        ↓
        └─→ Trace from monetization layer back to originating fraud event

Every case → Fox (Case Management) → evidentiary chain anchor
                                  → investigator handoff packet (when escalated)
                                  → law enforcement / regulator delivery
                                    (DEA / ATF / local PD / state board)
```

## Related

- [[platform-thesis]] — three accountability rails plus vendor; LP substrate operates under all four
- [[platform-gateway-thesis]] — accelerator-pack thesis that frames the LP-substrate productization
- [[concept-identity-layer-triad]] — consent-based projection that legitimizes cross-tenant signal pooling
- [[concept-substrate-discipline]] — fractal rule keeping the substrate vertical-agnostic
- [[2026-05-02-platform-trust-boundary-architecture]] — device registration, party taxonomy, investigator authority
- [[2026-05-02-agent-commissioning-protocol]] — pattern-match agent commissioning model
- [[2026-05-02-disaster-recovery-and-continuity]] — evidence chain recovery posture (S4 tier)
- [[2026-04-28-canary-go-agent-pmo-architecture-design]] — Q (Loss Prevention) and Fox (Case Management) module ownership
- [[vertical-smb-health-hypothesis]] — first-vertical productization candidate
- [[joint-product-positioning-pwc]] — joint-product positioning that absorbs the LP substrate as a capability
- [[ir-plan-v0.1]] — incident response, with which the investigator handoff substrate intersects
- [[mission-main-street]] — civic mission that the LP substrate serves (Main Street accountability against organized crime targeting independent retail)

---

*Captured 2026-05-02 by ALX (Cowork session). One concept per card — device intelligence as the substrate that lights up loss prevention as a complete platform offering across in-store, e-commerce, marketplace, cross-tenant, and stolen-monetization surfaces. Founder gate: confirm OQ-1 (marketplace observation legal posture), OQ-2 (cross-tenant consent contract), and OQ-8 (pricing model) before any prospect or partner conversation positions the LP substrate as a productized offering.*
