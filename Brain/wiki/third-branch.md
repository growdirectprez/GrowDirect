---
title: The Third Branch
type: thesis
status: v0.3
tags: [positioning, thesis, founder-narrative, retailspine, canary, bubble, sats, broadvision, pwc, auto-id, asset-protection, loss-prevention, ae-com, pitney-bowes, intactix, fred-meyer, hbs-moon]
created: 2026-04-24
updated: 2026-04-24
related:
  - "[[retail-integration-spine]]"
  - "[[Brain/projects/RetailSpine|RetailSpine MOC]]"
  - "[[Brain/projects/Canary|Canary MOC]]"
  - "[[Brain/projects/Method|Method MOC]]"
  - "[[academic-frame-1999-hbs]]"
  - "[[intactix-canonical-validation]]"
  - "[[srd-shelf-edge-label]]"
  - "[[tesco-technical-library]]"
  - "[[retek-rms-perpetual-inventory]]"
  - "[[bp-consulting-library-1997-1999]]"
  - "[[katz-scm-2003-archetype]]"
  - "[[broadvision-1999-2000-platform]]"
  - "[[pwc-ebiz-web-implementation-guide]]"
sources:
  - Brain/raw/inbox/BV Docs/  (BroadVision platform docs + 5 client BVAs, 1998–1999)
  - Brain/raw/inbox/interactive-tec-and-crm.md  (HBS 9-599-101, Youngme Moon, "Interactive Technologies and Relationship Marketing Strategies," May 1999 — academic frame)
  - Brain/raw/inbox/lyle-edits-obsolescence-draft28slaugv3-blueprint.md  (Auto-ID Enabled Superstore, co-authored by G. Lyle, Sep 2002)
  - Brain/raw/inbox/20160608-sysrepublic-xbr-replacement-func-req---sr-comments.md  (Southeastern Grocers LP platform requirements, Jun 2016)
  - Brain/raw/inbox/060623-top-down-design--space--range---display-v04.md  (Tesco SR&D)
  - PwC consulting corpus 1996–2003 (18 extracted decks, this inbox)
  - Operator experience: AE.com (American Eagle, C&L→PwC account, 1999–2000); BroadVision + Oracle fulfillment + DirectOrder.com at Pitney Bowes/Stamps.com (~2001–2002); JDA Intactix at Fred Meyer Superstores (~2003–2005); Fresh & Easy / Tesco (2006–2013)
last-compiled: 2026-04-24
needs-review: 2026-05-08
---

# The Third Branch

> **Provenance boundary.** This article carries the full 25-year operator lineage (AE.com → BroadVision/PB → Auto-ID → Intactix/Fred Meyer → F&E SRD → Tesco International → WMT International canonical → Secure → Canary → GrowDirect). The lineage is private provenance — moat validation, due-diligence backup, investor-room context. It **does not** carry forward to CATz or any customer-facing blueprint. Public artifacts present the substrate-and-architecture claim on its own engineering merits, without autobiographical thread.

**Thesis.** In 1999, three industries converged on one question — *how do you know your customer well enough to serve them one-to-one?* ERP sidestepped it. Strategy consulting answered it with engagements. Personalization platforms answered it with software. None of the three delivered, not because the questions were wrong but because the **substrate could not carry the weight.** GrowDirect is the resubstration of the third branch — personalization and relationship — on a substrate that finally can: continuous ambient observation, satoshi-denominated attribution, agent-operated capability surfaces. We are not a better CRM, a better POS analytics tool, or an AI wrapper on retail data. We are the answer the late 1990s demanded, running on a stack the late 1990s could not build.

## Founder note

I have been operating inside this thesis since 1999, across every branch it names.

**Branch C (personalization), 1999–2002.** I built **AE.com**, American Eagle Outfitters' first website, between 1999 and 2000. American Eagle was a Coopers & Lybrand account and I was on the Price Waterhouse side — the build happened across the PwC merger, which is where the BroadVision relationship entered my operating experience. We deployed BroadVision against a custom Oracle fulfillment backend, with DirectOrder.com as the third-party B2C shipper. I then rolled out BroadVision for **Pitney Bowes / Stamps.com** around 2002, with a personalization engine so basic that the canonical output was *"if you buy stamps you might like envelopes."* That sentence is the thesis in eight words: the 1999 academic frame (Moon, HBS 9-599-101) already named *Create / Remember / Anticipate* as the trilogy, BroadVision shipped the engine, I operated the engine — and the engine's ceiling on a session-cookies substrate was content-free. Branch C's vocabulary was correct. Its substrate was not.

**Branch A-adjacent / Auto-ID pivot, 2002–2005.** When IBM acquired PwC Consulting in late 2002 and the firm became IBM Business Consulting Services, the Auto-ID stream picked up. I co-authored *The Auto-ID Enabled Superstore* blueprint at draft 28 in September 2002 with the MIT Auto-ID Center cohort (`Brain/raw/inbox/lyle-edits-obsolescence-draft28slaugv3-blueprint.md`). Every functional requirement in that document is now trivially implementable on commodity sensors, edge compute, and near-zero-cost attribution. None of it was implementable in 2002. From Auto-ID I moved into JDA **Intactix** space-planning deployments at **Fred Meyer Superstores** (Kroger) — see the five Intactix Enterprise Suite 2006.2.0 integration guides (`Brain/raw/inbox/*Integration*Guide.pdf`) and the validation memo `[[intactix-canonical-validation]]`. The IKB / Space Planning / Floor Planning / ASR / PMM / MMS noun graph in those guides is the direct ancestor of RetailSpine's C/D/F/J/S families, including the `IKB` acronym carried forward verbatim.

**Branch B (operations, the full loop), 2006–2013.** I arrived at **Fresh & Easy / Tesco in mid-2006** — the US greenfield grocery venture that was the only environment where the blueprint could be attempted without retrofitting legacy — in a senior solution/product role, not operator-side. My first named artifact at F&E is the **US Technical Library Functional Specification, V1.0, dated 18 July 2006** (see `[[tesco-technical-library]]` and `Brain/raw/inbox/tesco-technical-library-corpus.md`). That spec is the specification-and-regulatory backbone of the private-label program — TPNB and UPC generation, recipe calculation in US imperial, US Nutrition Facts, US allergen matrix (Milk/Wheat/Egg/Fish/Shellfish/Soy + Tree Nuts + Peanuts), US compound-ingredient nesting (`{ [ ( ) ] }`), pack-copy compile — authored against RedSky IT's Creations platform (UK, Nottingham) as the US clone of the UK Technical Library. Approvers: Breda Mitchell (Regulatory Lead), Charlotte Maxwell (Commercial Lead), Helen Mottram (Technical Manager), Doug Rutledge (IT Director). I was writing the spec canonical for F&E ~10 months before anybody was drafting the S-prefix interfaces of the planogram-execution layer.

The full operating stack then built out through 2007–2013. The SRD (Space, Range & Display) implementation is in `Brain/raw/inbox/SRD/` — 323 files across Architecture, Batch Jobs, Documentations, Infrastructure, Interfaces, Training, and seven operational workstreams (JDA, Range Controls, Range In Progress, Ranging System, Sales Aggregation, Service Induction, Store Range). The Interfaces sub-folder alone contains S001, S002, S003, S004, S008, S009, S018, S022, S032, S036, S039, S041.5, S047, S052.5, S057, S058, S059, S061, S074, S077, S078, S087, S089, S090, S091, S093, S095, S100, S101, S102 — a 30-interface S-prefix canonical, substantially richer than the current RetailSpine catalog. Together with TTL (specification canonical) and RMS / Oracle Retail (merchandising master), SRD is the third leg of a **three-canonical** operating model that F&E built from scratch: *what the product is* (TTL), *who the product is* (RMS), *where the product is* (SRD) — compiling onto one shelf-edge label per rail, per night.

The operating philosophy embedded in the planogram-execution canonical is what separates SRD from every contemporaneous retail system. **An item could not be ordered before it had a place on the planogram.** Location-level planogram assignment and a hard cross-reference into the Oracle Retail item set-up process were gating conditions: until the item had a location, a shelf capacity, and a known pack configuration, it could not be enrolled as orderable. This inverted the industry-standard sequence (buy first, figure out the shelf later) and closed the substrate loop in the one place retailers had always left open — the handoff between merchandise planning and store operations. With capacity and pack known, store labor was minimized to the point where the product managers were forced upstream into vendor conversations about *specific packaging sizes* — the supply chain bending to the shelf, not the shelf bending to whatever the supplier shipped. This is the operator-side instantiation of what Moon called *Customization of Channels*, and it is exactly the discipline the Third Branch inherits: **observation closes the loop; the loop disciplines procurement; procurement disciplines packaging; packaging disciplines labor.**

**The substrate still failed at F&E. The canonical and its ordering-gate discipline survived, and went international.**

**The international port, post-2013.** After F&E shuttered, the SRD implementation corpus was carried to **Tesco International — Turkey (Kipa), Eastern Europe (Poland / Czech / Slovakia / Hungary), and Thailand (Tesco Lotus)** — as the operational canonical for the international banners. That is the first time the grammar proved portable across retailer-national contexts.

**The Walmart International canonical, ~2014–2016.** I then took the Tesco International SRD corpus and built the canonical interface model for **Walmart International**. That canonical — vendor-neutralized, generalized across retail banners, extended to non-Tesco vocabulary — is the direct upstream of the RetailSpine S-prefix catalog in `Brain/wiki/retail-integration-spine.md`. RetailSpine is not a reconstruction from memory. It is the vendor-neutralized Walmart International canonical, carried forward as the integration grammar of GrowDirect.

**Secure, ~2010–2019 (IBM → Appriss → Sysrepublic).** The Walmart International canonical was also the foundation of **Secure**, the enterprise loss-prevention platform I built across the IBM / Appriss / Sysrepublic lineage (see `[[Brain/projects/Secure|Secure MOC]]`). Secure was the first commercial product that explicitly read D-prefix movement events as LP observables — exactly the pattern the Third Branch commercial wedge now carries forward. The Sysrepublic relationship did not start with Secure, though. It started at **F&E with CRDM** — Sysrepublic's shelf-edge label delivery product consumed the `SKUItemInStore` reconciliation surface that S039 (daily SEL batch) and S101 (emergency facings) fed from IKB through Store Range into IDS (see `[[srd-shelf-edge-label]]` for the end-to-end data path). CRDM was the first out-of-band Sysrepublic capability on top of the canonical — a decade before xBR. The pattern — *Sysrepublic consumes a canonical surface and produces a capability the store physically feels* — recurs from shelf-edge label at F&E to shrink attribution at Secure-era customers. Canary is the SMB rebuild of Secure (per the Secure MOC).

**The SaaS decade, 2013–2015.** I moved to SaaS after F&E, looking for a stack where the substrate could catch up to the promise. The stack was closer. The commercial motion into retail was still missing — until Secure and the LP wedge crystallized at SEG.

**The wedge, 2016.** I returned to grocery at **Southeastern Grocers** (primary source: `Brain/raw/inbox/20160608-sysrepublic-xbr-replacement-func-req---sr-comments.md`) and discovered the commercial wedge that makes this business buildable: Loss Prevention is the one retail department that is always funded, and nobody has ever looked at the whole store through the Asset Protection lens.

**GrowDirect, 2026.** Attempt number five, with the substrate finally ready and the commercial wedge finally sharpened. Not a market observation. The thing I have been trying to ship for twenty-five years — with my own stamps-and-envelopes recommendation engine as the reductio, the Auto-ID blueprint as the requirements document, the Intactix and F&E years as the operator credentials, and the SEG LP wedge as the way in.

---

## Executive summary

Three distinct branches of late-1990s retail technology were all circling the same target. Each was right about *what* mattered. Each was wrong about *when* it could be delivered.

| Branch | Right about | Wrong about | Killed by |
|---|---|---|---|
| **ERP** (SAP, Oracle, PeopleSoft) | One record of truth across the enterprise | That the record should be transactional | Transactional truth is after-the-fact; the customer is gone by the time the row writes |
| **Strategy consulting** (PwC, IBM, C&L, Cambridge) | The questions: positioning, channel, systems, customer | The answer: buying 12 weeks of human labor to produce a slide deck | The questions are continuous; the answer was discrete |
| **Personalization** (BroadVision, Vignette, Epiphany, ATG) | The individual is the unit; rules-against-communities is a concession, not an aspiration | That 1999 web, device, and economic substrates could support continuous inference at scale | Tags too expensive, observation too partial, compute too slow, attribution too murky |

The three branches faded or consolidated by the mid-2000s. The questions did not.

What changed between 1999 and 2026 is not the question. It is the substrate. Cameras, sensors, and compute have collapsed in cost by three-to-five orders of magnitude. Attribution at unit level is economic through satoshi-denominated settlement. Agent orchestration provides the operator layer that the 1999 consultants promised but had to supply by flying people in. Every 1999 branch is now buildable. GrowDirect is what you get when you build them — together — on the right stack.

---

## I. The three branches, in their own words

### Branch A — ERP (sidestep)

ERP won the 1990s because it solved the easiest version of the problem: **make the ledger consistent across the company.** One customer ID, one product ID, one general ledger. It answered *what happened* at enterprise scale. It did not answer *who, why,* or *next.* By construction, the ledger writes after the event; the customer has already left the store.

ERP continues today as the backbone of most large retailers. It is not wrong; it is insufficient. You cannot run one-to-one retail from a ledger, because the ledger is a record of the past. The third branch exists because the ledger is not enough.

### Branch B — Strategy consulting (labor)

PwC, IBM BIS, Coopers & Lybrand, Cambridge Technology Partners, and the Big Five descendants answered the *soft* questions — positioning, channel, systems strategy, organizational change — with 8–16 week engagements priced in the low millions. The corpus is extensive and articulate. From our own extracted set:

- **Guess? (2001)** — "Who is the core customer? Has it changed over the years? Does it vary by geographic area?"
- **Saks SISP (2001)** — "Common UPC for all goods. Multi-channel merchandise locator. Reduce customer acquisition costs."
- **JC Penney (NRF 2001)** — "Lack of a shared customer repository. Do customers that shop more than one channel spend more?"
- **Rocketstop.com (1999)** — "Our Vision: Five phases of E-business evolution."
- **JVP Value Realization Partnership (Sep 25, 2002)** — "A new model for helping clients realize value through business insight and technology."

The questions are exactly the questions the third branch should be answering now — continuously, per merchant, per customer, per transaction. The consulting answer made sense in 1999 because continuous observation was impossible. It does not make sense in 2026, and the consulting industry knows it, which is why the center of gravity has moved to implementation partners and platform vendors.

**Primary-source strengthening — January 1998, a US specialty retailer SAP Retail 4.0 implementation engagement** (see [[bp-consulting-library-1997-1999]] for full provenance; files at `Brain/raw/.extract/BP/`). Two sentences from a single three-day workshop series make the evidence heavier than the 2001 quote list. On the ordering-gate architecture:

> "There is an issue with regards to the integration of a space management system (i.e. Intactix) with the assortment and listing functions in SAP. The objective is to control listing (and thus replenishment) for all SKU's in the stores through the use of planograms."
> — `Asstmgmt.doc`, Issues section, Jan 1998

That is the ordering-gate architecture — planogram assignment gating item activation for replenishment — documented *as an unresolved issue* eight years before F&E / SRD / Tesco built it with Intactix in the same role. The consultants could name it. The 1998 substrate could not carry it.

On the ERP sidestep, same workshop series, Vendor Management / Investment Buying notes:

> "Currently investment buying and MRP calculations will be completely separate processes (and SAP will choose the larger of the two values) but promotional purchases will be considered additions to the selected value."
> — `980128ib.doc`, Implementation Considerations, Jan 1998

> "Use store replenishment forecast for investment buying (SAP currently uses the MRP forecast only)"
> — same file, Test Month Follow Up

The consultants building the retailer's SAP Retail 4.0 implementation documented, as a requirement, that SAP's native MRP could not reconcile investment buying against forecasted demand — and that the retail logic therefore had to live in a parallel process that handed values to SAP. Branch A (ERP-sidestep) being written down *inside an SAP implementation* by the team supposed to make SAP work for retail. Paired with the Asstmgmt.doc quote above: same engagement, same month, two separate modules where retail logic had to sit outside the ERP and gate through the planogram. Branch B was not only asking the right questions; it was *documenting the answers the 1998 substrate could not deliver*. That is the primary-source evidence the thesis rests on.

The Branch B methodology template itself survives as a separate artifact — PwC's 2000 three-phase Definition/Design/Development Web Implementation Guide (see [[pwc-ebiz-web-implementation-guide]]) — whose grammar is humans-doing-work-for-N-weeks-then-stopping with the deliverables as the product. Five years later, the same firm ran the same template shape on a 2003 mid-market drug/pharmacy SCM engagement (see [[katz-scm-2003-archetype]]) — 140 working papers, an RFP to five vendors, a CDN$11.6M/year benefits case, and zero working technology at the end. The pattern is continuous.

**PwC/IBM got the questions right. They were not technologists.** The technology branch that *was* — BroadVision and its cohort — could not deliver on the promise. Both branches pointed at the same crater and neither could fill it. The architectural companion to the BVA/Moon material is the BroadVision platform itself, captured in [[broadvision-1999-2000-platform]] — a six-component model (session/profile store, Dynamic Content Center, rule engine against "communities," catalog, template tier, IM runtime) running two floors above what the 1999 substrate could deliver.

### Branch C — Personalization platforms (the right branch, wrong era)

*The branch I worked in. The blueprint I co-authored. The substrate that failed me.*


BroadVision, Vignette, ATG, Epiphany/E.piphany, and Andromedia (Aria) tried to build the platform. The *academic* statement of what the platform was meant to do is cleanest in Harvard Business School teaching note **9-599-101**, *Interactive Technologies and Relationship Marketing Strategies* (Youngme Moon, May 1999) — see `Brain/raw/inbox/interactive-tec-and-crm.md` and the companion memo `[[academic-frame-1999-hbs]]`. Moon's taxonomy — *Transaction → Relationship* marketing, *Share of Customer* (not market share), the *Create/Remember/Anticipate* trilogy for product customization, the *Banner/Email/Experiential/Viral* taxonomy for communications, *Personalized Pricing / Versioning* — is the precise vocabulary the BroadVision BVAs shipped against. The note names the targets; the platform vendors shipped the tools; neither reached the substrate.

BroadVision's own language is the cleanest commercial statement of intent from the era. From the company's 1998 white paper on *Extended Relationship Management* and the five Business Value Assessments in this inbox (American Airlines, Hallmark, Vodafone, Le Shop, RS Components, all dated between Nov 1998 and Mar 1999):

- **One-to-one** as the stated unit of service
- **Communities** as the implementation concession when 1:1 couldn't be delivered
- **Rule-based matching** as the decisioning mechanism
- **Session-based profiling** as the observation mechanism
- **Real-time personalized content** as the output
- **XRM** (Extended Relationship Management) as the business promise — CRM plus content plus commerce plus analytics, unified around the customer

And the gaps, visible in the BVAs themselves:

- *Vodafone (Nov 1998):* "Vodafone has not been utilizing BroadVision's One-To-One marketing capabilities."
- *Hallmark (Mar 1999):* "At this time extensive profiling is the only personalization feature used on this site."
- *Le Shop (Dec 1998):* 7,000 profiled users, 1,500 active purchasers. A 21% activation rate on the tightest-bound personalization use case of the era (grocery).
- *RS Components (Oct 1998):* "Rules are written against a 'community', offers are then put together, distributed to profiled 'communities.'" One-to-one as the brand name; many-to-many in the implementation.

BroadVision went to $230/share in March 2000 and to $0.41 by December 2002. The promise was correct. The substrate was not.

**Operator-side evidence** (founder, 2001–2002): the personalization engine deployed against Pitney Bowes / Stamps.com on BroadVision + custom Oracle fulfillment + DirectOrder.com logistics. The canonical output was *"if you buy stamps you might like envelopes."* That is the literal ceiling of rules-against-communities on 1999 substrate — content-free adjacency. Moon's *Anticipate* was the stated target; stamps-and-envelopes was what the substrate would bear.

---

## II. The substrate gap

What every 1999 branch was working around:

```
┌──────────────────────────────────────────────────────────────────────┐
│  1999 SUBSTRATE                                                      │
│                                                                      │
│  Observation:  transactional (ledger), sampled (panels/surveys),     │
│                session-scoped (cookies), after-the-fact               │
│  Identity:     explicit registration; cookies broke across devices   │
│  Attribution:  weeks/months after the event; funnel reconstruction   │
│  Settlement:   card rails, days of clearing, high minimums           │
│  Compute:      server-room, batch, expensive per transaction          │
│  Operator:     humans (consultants, agency, in-house marketing)      │
└──────────────────────────────────────────────────────────────────────┘
```

What 2026 now makes possible:

```
┌──────────────────────────────────────────────────────────────────────┐
│  2026 SUBSTRATE                                                      │
│                                                                      │
│  Observation:  continuous, ambient (camera + sensor), per-atomic     │
│                event, pre-transaction through post-transaction       │
│  Identity:     inferred from behavior graph; device-, location-,     │
│                and token-bound                                       │
│  Attribution:  unit-of-satoshi precision, realtime, live-streamed    │
│  Settlement:   near-zero marginal, near-instant (Lightning / L2)      │
│  Compute:      near-zero marginal at the edge, continuous inference   │
│  Operator:     agent orchestration over capability surfaces           │
└──────────────────────────────────────────────────────────────────────┘
```

The gap between the two is five-to-ten orders of magnitude in every dimension. That gap is why 1999 promises did not deliver. That gap is now closed.

---

## III. The resubstration map

Every 1999 capability has a 2026 equivalent. The vocabulary is the same; the substrate is not.

| 1999 concept | 2026 equivalent | What changed |
|---|---|---|
| Customer segment (rule-based community) | Revealed-preference vector per identity | Continuous observation replaces survey sampling |
| Session analytics (Aria, Omniture) | Continuous behavior trace | Post-session batch replaced by live stream |
| Profile registration | Inferred identity graph | Explicit registration replaced by ambient signal |
| ERP ledger | Observation-as-truth stream + ledger | Ledger becomes derived view; stream is canonical |
| Retail Inventory Method (RIM) | Atomic unit-cost accounting | "Before Computers" becomes "With Continuous Observation" |
| Engagement (8–16 weeks, then over) | Value Realization Partnership (continuous) | Discrete labor replaced by continuous instrumentation |
| Business Value Assessment (BVA, case study) | Value Realization Attribution (VRA, live) | Annual review replaced by live accounting |
| CAC (reconciled) | CAC (observed, per-satoshi attribution) | After-the-fact estimate replaced by continuous precision |
| One-to-one marketing | Agent-per-customer decisioning | Human-authored rules replaced by agent inference |
| Merch planning & allocation | Continuous sat-denominated contribution by SKU | Periodic review replaced by live optimization |
| Space, range & display (SR&D) | Bubble-observed shelf-to-customer fit | Planogram discipline plus ambient verification |

The grammar of retail consulting does not change. The measurement regime does.

---

## IV. What GrowDirect actually is

Against that map, GrowDirect has four things to build — and only four. Each maps to a 1999 branch that failed, and inherits the vocabulary of that branch updated for the substrate.

### 1. The bubble (Canary)

The observation substrate, instantiated per merchant. For Square merchants today, the bubble is software-only — Square data in, behavior graph out. For larger merchants and future deployments, the bubble extends to ambient observation — camera, sensor, shelf-level. The bubble is what BroadVision tried to simulate with session cookies and what Auto-ID tried to instantiate with RFID. It is now the table stakes of retail technology, not the frontier.

*Inherits from:* BroadVision One-to-One, Andromedia Aria, the 2002 Staples Auto-ID pilot.

### 2. The spine (RetailSpine)

The capability lexicon — six domains, ~76 canonical interfaces, the C/D/F/J/S families. Not a reconstruction from memory. **The direct, vendor-neutralized descendant of the Walmart International canonical I authored ~2014–2016**, which itself was the international port of the F&E / Tesco SRD corpus, which itself was the on-the-ground implementation of the JDA Intactix 2006.2.0 noun graph. RetailSpine inherits the *ordering-gate discipline* from SRD: in the spine's grammar, an item has no place in the catalog until it has a location, a capacity, and a pack configuration — procurement is downstream of planogram, not upstream. This is the grammar that lets the bubble speak to retail the way retail thinks of itself. Without the spine, the bubble is surveillance. With the spine, it is *retail.*

*Inherits from:* JDA Intactix Enterprise Suite (2006) → Tesco SRD at F&E (2006–2013) → Tesco International (Kipa / EE / Lotus, post-2013) → Walmart International canonical (~2014–2016) → RetailSpine (2026). Oracle Retail item master as the system-of-record anchor for the ordering gate. The 18 PwC/IBM engagement decks as the consulting-side vocabulary.

**Substrate correction — the merchandising canonical is a ledger.** Both gates (SRD's ordering gate, TTL's compile gate) gate *against* something load-bearing: the perpetual-inventory movement ledger that RMS/Oracle Retail actually is. RMS is not primarily an identity master; it is a signed-movement ledger (receipts, transfers, adjustments, cycle counts, sales, shrink, RTV, allocation, reclass, period close) with an item master attached as a supporting attribute set. SRD's ordering gate enforces that the ledger is ready to receive an item's first receipt without violating conservation or cost-method consistency. TTL's compile gate refuses to produce a physical shelf-edge label for an item the ledger has not confirmed is live, priced, and UoM-consistent. The three-canonical model becomes coherent when the ledger is named as substrate rather than treated as one identity master among peers. See [[retek-rms-perpetual-inventory]] for the full primary-source map of movement verbs, invariants, and the RIB/RDM topology that publishes the ledger to every downstream consumer.

### 3. The agents

The operator layer. Every 1999 engagement reserved slides for "PwC + Client + Vendor project team." The project team was human. The 2026 equivalent is an agent team — planning agents, merchandising agents, marketing agents, loss-prevention agents — each with read/write access to spine interfaces, each operating continuously, each attributable per action. The agent layer is what consulting tried to externalize (PwC billed hours) and what BroadVision tried to automate away with rules (and failed).

**The protocol matters as much as the agents.** The SRD canonical has been a grammar human operators could read since 2006. Model Context Protocol (MCP) is the first interface layer over which the canonical becomes native to agents: every S-prefix planogram record exposed as an MCP resource, every F-prefix movement event as an MCP event stream, every J-prefix replenishment parameter as an MCP tool, every D-prefix observable as an LP-addressable signal, and the ordering gate itself enforced as an MCP precondition no procurement agent can bypass. **SRD meets MCP is the specific architectural moment the third branch closes.** The canonical *was* the discipline; MCP makes the discipline native to the operator layer. See `[[intactix-canonical-validation]] §V.E`.

*Inherits from:* PwC delivery model, BroadVision rule engine, modern agent frameworks, MCP as the protocol that finally lets agents speak the retail canonical without a translation layer.

### 4. The accounting primitive (sats)

Satoshi-denominated attribution. Every observed action, every attributed contribution, every CAC component settled in the smallest universal accounting unit available. This is what makes *continuous* attribution economically possible — the measurement regime does not cost more to operate per event than the signal it generates. Without a near-zero-cost accounting primitive, continuous attribution defaults back to batch. With sats, it does not.

*Inherits from:* Retail Inventory Method → Cost Method → sat-denominated direct cost.

---

## V. Positioning

**What we are not:**

- Not "AI for retail." That category is empty by construction — it names the tool, not the substrate.
- Not "better CRM." CRM is Branch C framing; the framing works, the implementation does not.
- Not "POS analytics." That is Branch A (ledger-based) on faster servers.
- Not a consultancy. Branch B is other people's revenue model; it is not ours.

**What we are:**

- The third branch, built on the substrate that was missing.
- Specifically: a **Value Realization Partnership** (BroadVision/IBM-PwC language, reclaimed and updated) that delivers continuous observation, continuous attribution, continuous optimization — measured in sats — against the retail grammar the industry already speaks (the spine).

The positioning borrows language from the people who got the questions right, updates the substrate, and ships.

---

## VI. What we build first

Three deliverables, in order, each underwritten by this thesis:

1. **Canary for Square merchants.** The smallest possible bubble, instantiated on the smallest possible merchant, with observable loss-prevention value inside 30 days. This is the proof the substrate carries the weight for one class of merchant, for one class of use case. It also becomes the reference case for the VRP model.

2. **The RetailSpine v1 release.** The spine codified — six domains, canonical interfaces, mapped to Square data today, mapped to larger-merchant systems next. RetailSpine is the language; without it, we are selling surveillance rather than retail.

3. **The agent layer on top of the spine.** Each agent a capability surface; each action attributable; each outcome denominated in sats. This is the operator substrate that lets the VRP model scale beyond the merchants where we can spend human time.

Each deliverable is a refutation of one 1999 failure mode. Together they instantiate the third branch.

---

## VII. The commercial wedge — Asset Protection

A correct thesis is not a company. Companies ship on the commercial motion.

The other retail-tech categories all sell into discretionary budgets — merchandising, marketing, customer experience. Those budgets are soft, contested, and the first to get cut in a downturn. Every retail-tech vendor since BroadVision has fought for the same three line items, and every retail-tech vendor since BroadVision has been underfunded in the critical first two years of deployment.

**Loss Prevention is different.** LP / Asset Protection is:

- **Mandatorily funded.** Shrink happens whether the retailer wants it to or not. Every publicly traded retailer reports shrink. Every private retailer budgets against it. The budget does not negotiate with the quarter.
- **Vendor-protected.** LP contracts tend to be multi-year because investigations, chain-of-custody, and integration work all bleed across fiscal years.
- **Observation-native.** LP already wants full-store visibility — cameras, POS journal, RFID, associate behavior, exception reporting. LP is the one department that buys observation infrastructure as its reason for existing.

But historically, nobody has built a platform for LP that also serves the rest of the store. LP vendors deliver narrow shrink analytics. Merchandising vendors deliver narrow planning. Marketing vendors deliver narrow personalization. Nobody connects them — because each vendor only has budget access to one silo.

**GrowDirect's motion: enter through LP. Expand through observation.**

The full-store observation substrate we deploy for LP purposes — POS journal analysis, exception detection, shrink attribution — is, by construction, the same substrate that can serve merchandising, marketing, planning, customer service, and corporate finance. Every capability in RetailSpine can run on it. But the merchant pays for it out of the LP line item, where the money is, and only later — after the substrate is proven — opens additional use cases out of other budget lines.

This is the commercial thesis in one sentence:

> **Asset Protection is the Trojan horse. The observation substrate is the payload. RetailSpine is the capability layer the substrate supports. Sats are how we price it.**

This is the motion that makes Canary-for-Square-merchants coherent with the enterprise future. Square merchants have no LP department, but they have shrink — and it comes out of the owner's margin, which is the most motivated budget in all of retail. We enter through the same wedge, at a smaller scale, with the same substrate. As the substrate proves itself at small-merchant scale, it graduates up-market — and when it graduates, it lands in enterprise retail through *exactly* the same door, just labeled "Asset Protection" instead of "owner shrink."

---

## VIII. The one-paragraph version

> *In 1999 I built AE.com on BroadVision, on the PwC side of the C&L merger. In 2001 I deployed the same engine at Pitney Bowes / Stamps.com — where the ceiling of the rec engine was "if you buy stamps you might like envelopes." The 1999 HBS teaching note named the trilogy correctly (Create / Remember / Anticipate). BroadVision shipped the engine. I operated it. The substrate was the limit. In 2002 I co-authored the Auto-ID Superstore blueprint to replace the substrate; IBM bought PwC Consulting that year and the project moved to RFID pilots and then JDA Intactix planograms at Fred Meyer. In July 2006 I authored the US Technical Library functional specification at Fresh & Easy / Tesco — the specification canonical that sits beside Oracle Retail and SRD as the third leg of a three-canonical operating model for private-label food. SRD gated ordering through the planogram: no item was orderable until it had a location, a capacity, and a pack configuration known in Oracle Retail, and product managers worked upstream to bend packaging to the shelf. TTL gated pack-copy compile through specification: no item hung on the rail until its Statement of Identity, Nutrition Facts, ingredient nesting, and allergen matrix reconciled. The canonical survived F&E's close. I ported it to Tesco International (Kipa, Eastern Europe, Tesco Lotus), then built the Walmart International canonical from it ~2014–2016, then built Secure (IBM → Appriss → Sysrepublic) on the same grammar as the first commercial LP platform that read D-prefix movement events as asset-protection observables. In 2016 Southeastern Grocers confirmed the commercial wedge: Loss Prevention is the only retail department with the mandated budget to fund full-store observation. Canary is the SMB rebuild of Secure; the TTL canonical is its fresh-prep capability module waiting to be reauthored on 2026 substrate. GrowDirect is attempt number five: continuous observation is now cheap, attribution is atomic in sats, agents replace consultants, the ordering gate closes the loop, the spec gate closes the rail tag, and Asset Protection is the commercial wedge that nobody else has been willing to use as the entry point. We keep the retail vocabulary the industry already speaks — because I wrote it — update the substrate, enter through LP, and finish the third branch the 1990s promised. The engine is no longer going to tell you that if you buy stamps you might like envelopes.*

That is the pitch. Everything else is support.

---

*Sources: the eighteen PwC/C&L/IBM decks and spreadsheets (1996–2003); the forty-six BroadVision platform documents and Business Value Assessments (1998–1999); HBS teaching note 9-599-101 (Youngme Moon, May 1999, `interactive-tec-and-crm`) as the academic frame; the 2002 Auto-ID Superstore blueprint co-authored by G. Lyle (`lyle-edits-obsolescence-draft28slaugv3-blueprint`); the five JDA Intactix Enterprise Suite 2006.2.0 integration guides and the validation memo `[[intactix-canonical-validation]]`; the Tesco SRD corpus at Fresh & Easy (`Brain/raw/inbox/SRD/`, 323 files, 30 S-prefix interfaces, ordering-gate discipline against Oracle Retail item master); the Tesco International port (Kipa / Eastern Europe / Tesco Lotus, post-2013); the founder-authored Walmart International canonical (~2014–2016, direct upstream of RetailSpine); the Secure platform lineage (IBM → Appriss → Sysrepublic, ~2010–2019; see `[[Brain/projects/Secure|Secure MOC]]`); the 2016 Sysrepublic xBR replacement requirements from Southeastern Grocers; Tesco Space, Range & Display (2006); and operator-side experience at AE.com (1999–2000), Pitney Bowes / Stamps.com (~2001–2002), Fred Meyer Superstores Intactix (~2003–2005), Fresh & Easy (2006–2013), Tesco International (post-2013), Walmart International (~2014–2016), and Secure (~2010–2019). All primary sources currently in `Brain/raw/inbox/`. Retail grammar from the RetailSpine MOC v0.5. Companion memos: `[[academic-frame-1999-hbs]]`, `[[intactix-canonical-validation]]`.*
