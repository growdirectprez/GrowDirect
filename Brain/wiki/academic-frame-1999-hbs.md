---
title: The Academic Frame — HBS 9-599-101 (Moon, 1999) and the Third Branch
type: analytical-memo
status: v0.1
tags: [third-branch, academic-frame, hbs-moon, personalization, relationship-marketing, broadvision-era, pwc, 1999]
created: 2026-04-24
updated: 2026-04-24
related:
  - "[[third-branch]]"
  - "[[retail-integration-spine]]"
  - "[[Brain/projects/RetailSpine|RetailSpine MOC]]"
sources:
  - Brain/raw/inbox/interactive-tec-and-crm.md  (HBS 9-599-101, Youngme Moon, Rev. May 17, 1999, 12pp)
  - Peppers, D. & Rogers, M. (1997), *Enterprise One to One*, Doubleday — primary citation in the note
  - Shapiro, C. & Varian, H. (1999), *Information Rules*, HBSP — footnoted on pricing
  - Brain/raw/inbox/BV Docs/  (contemporaneous commercial evidence — BroadVision platform + 5 BVAs, 1998–99)
last-compiled: 2026-04-24
needs-review: 2026-05-08
---

# The Academic Frame — HBS 9-599-101 (Moon, 1999) and the Third Branch

> **Provenance boundary.** This memo cites founder-operator experience (AE.com, BroadVision at Pitney Bowes / Stamps.com) as operator-side evidence against Moon's 1999 frameworks. That autobiographical thread is private provenance and **does not** carry forward to CATz or any customer-facing blueprint. Public artifacts present the thesis on its own academic and architectural merits.

**Governing thesis.** Youngme Moon's May 1999 HBS teaching note *Interactive Technologies and Relationship Marketing Strategies* is the cleanest academic statement we have of what BroadVision was commercially selling, PwC and IBM BCS were operationally delivering, and the founder was personally deploying at AE.com and Pitney Bowes / Stamps.com in the same eighteen-month window. Every framework the note names is correct. Every framework the note names failed to reach substrate. The Third Branch is the restoration of Moon's 1999 vocabulary — *Share of Customer, Learning Relationship, Create/Remember/Anticipate, Markets-of-One* — on a substrate that can finally carry the weight: continuous ambient observation, agent operators, satoshi-denominated attribution. This memo positions the note as the academic anchor of the Third Branch corpus and maps its taxonomy directly onto the 2026 resubstration.

## Executive summary

| Moon's 1999 frame | What it described | What shipped then | What ships now |
|---|---|---|---|
| Transaction → Relationship marketing | Philosophical flip from one-off sales to continuous knowledge | BroadVision rule-based "communities"; PwC 8–16 week engagements | Canary bubble + continuous observation; agent-operated capability surfaces |
| Share of Customer (not Market Share) | KPI flip from aggregate penetration to per-identity depth | LTV spreadsheets reconciled annually | Per-identity behavior graph with sat-denominated contribution, live |
| The Learning Relationship (Peppers & Rogers) | Both parties get smarter with each interaction | Cookie-scoped profile + registration DB | Inference-native identity graph + agent memory |
| Knowledge Acquisition (passive + active) | Clickstream, cookies, forms, surveys | DoubleClick cookies; MatchLogic cross-source aggregation | Cameras, POS journals, sensor telemetry, stream-as-canonical |
| Customer Differentiation + LTV | Segment by economic value; invest proportional to LTV | Tiering spreadsheets; "top 20%" campaigns | Per-customer continuous LTV with agent-level resource allocation |
| Create / Remember / Anticipate | Customize products via co-creation, memory, prediction | Levi's Original Spin; Amazon recs; Firefly collaborative filter | RetailSpine capability surfaces driven by observed behavior graph |
| Banner / Email / Experiential / Viral | Taxonomy of customized communications | DoubleClick, Onsale email, CK One, Hotmail footer | Contextual agent-authored channels at per-interaction attribution |
| Personalized Pricing + Versioning | Differential pricing via behavior or self-selection | Airlines yield mgmt; Priceline reverse auction; Intel 386 versioning | Continuous sat-denominated dynamic pricing with per-identity terms |
| Learning Relationship as lock-in | Cumulative personalization makes switching costly | Session-scoped; broke across devices | Behavior graph bound to identity across substrate |

The 1999 vocabulary was not wrong. It was twenty-seven years early.

---

## I. What Moon actually said

The note is twelve pages, two of them appendices. It opens on the *Transaction vs. Relationship* distinction (Figure 1), argues that relationship marketing has always been blocked by two obstacles — cost of customer information and cost of acting on it — and then spends eight pages explaining why interactive technology has, in 1999, made both obstacles economically solvable for the first time.

The argument decomposes cleanly into five movements. Each one names a problem, names the interactive mechanism that addresses it, and cites case evidence.

### I.A — Knowledge acquisition

Moon distinguishes *passive* (clickstream, cookies, server logs, DoubleClick, MatchLogic) from *active* (forms, surveys, registration, value-in-exchange) data collection. The note is explicit that passive observation is cheaper per-bit but sparser, and that active acquisition requires exchange value — content, discount, or service — to sustain. Privacy tension is acknowledged via Geocities (FTC settlement, 1998) and AOL (subscriber outing) sidebars and the Truste trust-mark remedy.

**What she did not anticipate:** that passive observation would need to move from the channel (cookies, clickstream) to the *physical substrate* (cameras, sensors, shelf telemetry) before the sparsity problem would actually be solved. Web-native observation was the *only* observation available to her. It is the one form of observation that 2026 has de-monopolized.

### I.B — Customer differentiation and LTV

Moon's LTV stack (Figure 3) has six components: acquisition cost (negative), base profit, revenue growth, cost savings, referrals, price premium. The note argues that firms should invest in customers in proportion to LTV, which requires computing LTV continuously, which requires knowing customers continuously, which is what interactive technology enables.

**What she did not anticipate:** that LTV itself would become computable per-interaction, not per-customer-year. Moon's frame still assumes the LTV computation is an annual exercise. The 2026 substrate moves LTV into the live attribution stream — every satoshi attributed to an action updates every identity's vector in real time.

### I.C — Mass customization and the product trilogy

This is the sharpest part of the note. Moon names three modes of product customization:

1. **Create.** The customer specifies the product. Exemplars: Levi's Original Spin (jeans to measurement), CDuctive and CustomDisc (mix CDs), Dell (build-to-order PCs).
2. **Remember.** The firm remembers past behavior and acts on it. Exemplars: Amazon and Barnes & Noble (recommendation based on purchase history).
3. **Anticipate.** The firm predicts what the customer will want before they know it themselves. Exemplar: Firefly (collaborative filtering), acquired by Microsoft 1998.

**The founder's operator trace:** the BroadVision engine deployed at Pitney Bowes / Stamps.com (~2001–2002) was a live instance of Moon's *Remember/Anticipate* combination. The engine shipped. The engine ran. The engine's output was *"if you buy stamps you might like envelopes."* The content-free adjacency is not a failure of the algorithm. It is the *ceiling* of Moon's trilogy on 1999 substrate — where behavior is session-scoped, catalog is SKU-flat, identity is cookie-bound, and no richer vector is available to the recommender.

The Third Branch thesis follows: Moon's trilogy was correct. Create/Remember/Anticipate remain the right primitives. Substrate, not algorithm, was the ceiling. The 2026 substrate — continuous observation, identity graphs across devices and physical presence, agent-authored content — dissolves the ceiling. The trilogy runs on it properly for the first time.

### I.D — Customized communications

Moon's four-category taxonomy:

1. **Banner advertising** — DoubleClick as the canonical example; real-time targeted to user profile.
2. **Email marketing** — Permission-based; Onsale as the canonical example; cheap and targeted vs. direct mail.
3. **Experiential marketing** — Creating interactive brand environments; Calvin Klein CK One, Stolichnaya.
4. **Viral marketing** — Hotmail (0 to 12M in 18 months via the email footer), ICQ, Amazon Associates, Yoyodyne (acquired by Yahoo!).

**What she did not anticipate:** that the category structure itself would dissolve. In 2026, the channel is not what differentiates messages; *attribution per message* does. An agent-authored, per-identity communication that lands in banner, email, push, shelf display, and checkout receipt *simultaneously* is neither a banner ad nor an email nor an experiential activation — it is an attribution event in a sat-denominated ledger, addressed to a behavior graph. Moon's taxonomy collapses into one primitive: *observed-response-to-observed-stimulus*.

### I.E — Customized channels and pricing

On channels: Norwest (as counter-example — the mortgage lender fighting the online trend because of its 4,000-person sales force and branch network) and American Airlines (direct email for fare specials) are the two sidebars. The framing is classic channel conflict — existing infrastructure vs. digital disintermediation.

On pricing: *Personalized pricing* (per-user terms — airlines, Virtual Vineyards real-time offers, eBay/Onsale dynamic auction, Priceline reverse auction) and *Versioning* (product-line self-selection — Mathematica student edition, Intel 386 with disabled math coprocessor). Moon credits Shapiro & Varian's *Information Rules* as the primary source on this material and notes — with evident discomfort — that "Leveling the Information Playing Field" via shopping bots (MySimon, Compare.net, Jango, Junglee, Yahoo! Shopping, C2B) may erode differential pricing.

**What she did not anticipate:** that *pricing itself* would become substrate-native once settlement collapsed to near-zero marginal cost. Moon assumed price was a rendered number; in 2026 price is a live stream denominated in sats, renegotiable per transaction by agents operating on both sides. Priceline was directionally correct and eighteen years early.

### I.F — The Learning Relationship as lock-in

The note's closing argument, borrowed from Peppers & Rogers (1997), is that learning is bi-directional: the firm accumulates customer knowledge; the customer accumulates awareness of the irreplicability of the firm's personalized service. The combined effect is switching-cost lock-in that a competitor cannot replicate by price or feature.

**What she did not anticipate:** that the lock-in would itself become portable via user-owned identity. A behavior graph owned by the customer and licensed to the firm inverts Moon's model — the customer keeps the accumulated knowledge; the firm rents access. The thesis of customer lock-in becomes the thesis of *merchant earning* against a persistent identity. RetailSpine is architected to this inversion.

---

## II. Where Moon sits in the 1999 corpus

The note is not isolated. It sits inside a three-layer commercial-academic stack we now have full evidence of, all dated within a single eighteen-month window:

```
┌─────────────────────────────────────────────────────────────────┐
│  ACADEMIC LAYER (1999)                                          │
│  HBS 9-599-101 (Moon), Enterprise One to One (Peppers &         │
│  Rogers, 1997), Information Rules (Shapiro & Varian, 1999)      │
│  → names the vocabulary: Share of Customer, Learning            │
│    Relationship, Markets-of-One, Create/Remember/Anticipate     │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│  COMMERCIAL / PLATFORM LAYER (1998–1999)                        │
│  BroadVision One-to-One Enterprise + XRM white paper            │
│  BVAs: American Airlines, Hallmark, Vodafone, Le Shop,          │
│  RS Components                                                  │
│  → ships the engine: rules against communities, session-        │
│    scoped profiling, real-time personalized content             │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│  CONSULTING LAYER (1999–2002)                                   │
│  PwC/C&L/IBM BCS decks: Saks SISP, JCP NRF, Guess?, JVP,        │
│  Rocketstop.com, welcome2b onboarding, PKTMP* master templates  │
│  → sells the transformation: Ascendant® IS Strategy 10-phase,   │
│    5 phases of E-business, Value Realization Partnership        │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│  OPERATOR LAYER (1999–2002, founder)                            │
│  AE.com build on PwC/C&L side (1999–2000)                       │
│  BroadVision + Oracle fulfillment + DirectOrder.com at          │
│  Pitney Bowes / Stamps.com (~2001–2002)                         │
│  → deploys the engine; discovers the ceiling: "if you buy       │
│    stamps you might like envelopes"                             │
└─────────────────────────────────────────────────────────────────┘
```

The four layers agree on the vocabulary. They disagree on where the work lives.

- Academic layer (Moon): describes the space without prescribing implementation.
- Platform layer (BroadVision): ships the engine, assumes infrastructure catches up.
- Consulting layer (PwC/IBM BCS): sells the transformation with human labor filling the infrastructure gap.
- Operator layer (founder): runs the engine; sees the gap directly at the SKU and session level.

All four are correct about the space. None of them closes the loop. The loop does not close until the substrate — cameras, sensors, agents, sats — closes it.

---

## III. The specific translations (Moon 1999 → Third Branch 2026)

| Moon 1999 | Third Branch 2026 | The substrate change that enabled it |
|---|---|---|
| "Share of Customer" as the KPI flip | Per-identity sat-denominated contribution, continuous | Attribution moves from monthly reconciliation to live stream |
| "Learning Relationship" bi-directional knowledge | Inference-native identity graph + agent memory | Memory is not a DB row; it is an embedding with recall |
| Passive data (cookies, clickstream) | Ambient observation (cameras, sensors, shelf, voice) | Observation moves from channel to physical substrate |
| Active data (forms, surveys, registration) | Exchange-value-for-signal as agent-negotiated contract | Exchange becomes a sat-priced transaction, not a trust gift |
| LTV as annual computation | LTV as live-updating vector | Continuous computation is economic at sub-cent cost |
| Create (co-specification) | Agent co-specification against capability surface | Levi's Original Spin model generalized to every SKU via RetailSpine |
| Remember (history-based recs) | Behavior graph with substrate-grade identity | Graph escapes the session-cookie substrate |
| Anticipate (collaborative filtering) | Agent inference over continuous observation | The Firefly idea, now with inputs and compute it always needed |
| Banner targeting (DoubleClick) | Per-moment agent-authored context | Targeting moves from rule evaluation to agent decision |
| Email personalization (Onsale) | Multi-channel message as sat-attribution event | Channel distinction collapses; attribution replaces it |
| Experiential (CK One) | Agent-orchestrated multi-touchpoint experience | Experience becomes a composable capability, not a campaign |
| Viral (Hotmail, ICQ) | Network effects via identity-graph portability | Virality becomes a property of user-owned identity |
| Personalized pricing (Priceline) | Dynamic per-identity sat-denominated pricing | Settlement cost no longer pins pricing to batch |
| Versioning (Mathematica student) | Capability-level toggles per identity, continuous | Versioning becomes live config, not product-line decision |
| Learning Relationship lock-in | User-owned identity as merchant-earning surface | Lock-in inverts: customer keeps the graph, merchant rents access |

Every row is a 2026 build specification dressed as a 1999 category translation.

---

## IV. What Moon explicitly named that the Third Branch inherits by name

Four pieces of vocabulary from Moon (1999) are load-bearing in the Third Branch doc and should be used in external positioning:

1. **"Share of Customer."** The KPI flip. Market share is Branch A / ERP framing. Share of customer is Branch C / relationship framing. RetailSpine's attribution model reports share-of-customer by default; share-of-market is a derived aggregate.

2. **"Learning Relationship."** The Peppers & Rogers phrase Moon adopts. This is what the Canary bubble + agent layer actually produces — a learning relationship between the merchant's capability surface and each identity's behavior graph, priced in sats.

3. **"Markets-of-One."** Implicit throughout the note; the logical endpoint of mass customization. The Third Branch position: markets-of-one was rhetorical in 1999 because the substrate rounded down to communities. Sats make markets-of-one economically literal for the first time.

4. **"Create / Remember / Anticipate."** The product customization trilogy. This maps directly to RetailSpine capability families. Adopt it as the naming scheme for customer-facing capability documentation.

---

## V. What Moon did *not* see coming (and the Third Branch must)

Four substrate changes post-1999 that Moon's frame cannot natively absorb. Each is load-bearing for GrowDirect:

1. **Observation leaves the channel.** Moon's "interactive technology" = web. The real revolution was ambient observation outside the web — cameras, sensors, phones-as-sensors, voice, shelf telemetry. The Third Branch bubble is substrate-native, not web-native.

2. **The operator is not human.** Moon assumes marketers implement the frameworks. PwC assumed consultants. BroadVision assumed rule-authors. The 2026 operator is an agent. This is the single biggest break from the 1999 frame.

3. **Attribution is priced in the smallest universal unit.** Moon treats LTV as a management accounting exercise. It becomes a *stream accounting* exercise once the unit of attribution is a satoshi and settlement is near-zero marginal. The accounting primitive changes; the thesis follows.

4. **Identity is user-owned.** The 1999 frame assumes the firm owns the customer record. The 2026 frame supports — and arguably requires — the customer owning the behavior graph and licensing access. This inverts the lock-in thesis and changes the commercial motion.

These four are the Third Branch's load. Moon wrote the vocabulary for three of them. The fourth (agents as operators) was not visible from 1999.

---

## VI. Why this memo exists

The Third Branch thesis needs an academic anchor. Without one, it reads as a founder-autobiographical pitch dressed as a retail-tech position paper. With the 1999 HBS note in the corpus, the argument becomes:

> The vocabulary the industry already speaks was named correctly in 1999 by the academy, shipped commercially by BroadVision, sold as transformation by PwC/IBM BCS, and operated at the SKU level by the founder. The vocabulary is right. The failure was entirely substrate. The substrate is now fixed. GrowDirect is the restoration.

That argument has four independent witnesses (academy, platform, consulting, operator) and one single cause of failure (substrate). It is defensible in front of an investor, a Big-4 partner, a skeptical CIO, and — most importantly — the retail industry's own memory of 1999.

The memo's job is to make the HBS note a first-class citizen of the corpus. It now is.

---

*Source: `Brain/raw/inbox/interactive-tec-and-crm.md` (HBS 9-599-101, Youngme Moon, Rev. May 17, 1999, 12pp, via `pdftotext -layout`). Companion thesis: `[[third-branch]]`. Contemporaneous commercial evidence: `Brain/raw/inbox/BV Docs/` (BroadVision platform + 5 BVAs, 1998–99). Operator-side evidence: AE.com build 1999–2000, BroadVision at Pitney Bowes/Stamps.com ~2001–2002.*
