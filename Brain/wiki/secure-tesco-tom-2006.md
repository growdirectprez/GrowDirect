---
date: 2026-04-23
type: wiki
tags: [secure, retail-career, ibm-consulting, tesco, operating-model, 2006, pre-secure]
sources:
  - Brain/raw/inbox/commercial-operating-model-v4.md
  - Brain/raw/inbox/tesco-operating-model---finance-ver2.md
  - Brain/raw/inbox/top-down-design--retail-ops-jb-final.md
  - Brain/raw/inbox/060623-top-down-design--space--range---display-v04.md
  - Brain/raw/inbox/tom-forecast--ordering-v3.md
  - Brain/raw/inbox/summary-document-people-work-in-progress.md
  - Brain/raw/inbox/tom-top-down-design---property-pack-template-jul-06-v5.md
  - Brain/raw/inbox/tom-business-model-v15-supply-chain.md
last-compiled: 2026-04-23
needs-review: 2026-05-07
---

**Wiki:** [[Brain/Home|Home]]

# Tesco Operating Model — 2006 (IBM engagement)

## Summary

Eight draft Top-Down Design decks from the **Tesco International Operations Development Design Group**, June–July 2006. IBM-era consulting engagement (Jeffe's career line) to produce Phase 1 of the Tesco Operating Model: a structured set of "what we do / why we do it / how we measure it" across the major business domains of a global retailer, shaping the processes that would then be rolled into IT system design. Source decks labelled "Draft / Sample".

This is foundational pre-Secure retail-consulting IP — the same practice lineage that later produced the Appriss / Sysrepublic / Secure product line and informs Canary's CRDM / factory-process doctrine today.

## The Engagement

**Context:** Tesco was expanding internationally (UK → Central Europe, China, USA). Each country was reinventing processes locally. The TOM engagement set out to define one canonical operating model per business domain so best practice could be replicated and IT systems could be specified against a stable spec.

**Method — Phase 1:**

1. A series of workshops per business domain
2. Each workshop produced a draft operating model: Level-1 processes ("what we do") and Level-2 processes ("how we do it")
3. Decks follow a consistent structure: Executive Summary · Benefits · Principles · Dependencies · Key Decisions To Be Made · Phase-1 Model (Level 1 + Level 2 process maps)
4. Phase 2 (follow-on) detailing Level-3 processes

**Areas covered in Phase 1 (per Forecast & Ordering intro):** Space/Range/Display, Buy (Commercial), Forecast & Order, Distribution & In-store Replenishment, Front-end & Service, Finance, People.

**Further work underway at time of these decks:** Marketing, Build, Management Information, IT Services. Corporate Purchasing + Joint Buying deferred.

## The 8 Decks

### 1. Commercial (Lucy Williams, June 2006 v4)

**Role:** "Build profitable customer-driven ranges and promotions that deliver to agreed margin targets."

Scope: planning category strategy, range direction through to in-store execution; new-product development; managing cost and Buy-for-Less; size of committed/seasonal buys; retail price management; supplier base development; promotion planning & negotiation; exit planning; KPI review & re-forecasting.

Key dependencies: Marketing (customer insight, competitor activity, trade plan); Ordering & Distribution; Finance; Space/Range/Display.

Open decisions:
- Promotions — Marketing owns strategy and operational delivery; Commercial owns delivery to strategy
- Price — Marketing owns retail price strategy; Commercial owns adherence + retail price maintenance
- Logistics Income — should it sit in Commercial (UK model) or in Forecast & Ordering (International model)?

### 2. Finance (Lisa Baglin, June 2006 v2)

**Role:** Fixed-asset accounting + investment appraisal; working-capital accounting (AP, AR, stock, cash); reporting company financial performance.

Benefits: local + group legal/fiscal compliance; tight working-capital governance; simple accurate reporting; automated processes.

Dependencies: Commercial (accurate info for supplier payment + goods valuation); all Head-Office functions (PO raise + invoice authorization); Governance Committee (IODG — capital approval); Store Operations (sales + tender accuracy).

Open decisions:
- Group best practice for Invoice Matching (include self-billing?)
- Where should Finance transaction processing sit?
- How will we ensure governance over the USA Operating Model?

### 3. Retail Operations (Tim Golding, Richard Dodd, June 2006 — "JB final")

**Role:** Service productivity (work-measured staffing targets); checkout service + productivity (scheduling to trade, queue-length targets); **price integrity** (label price = scanned price); sell goods and services; manage tenders.

Supports the three customer promises: *"I don't queue" · "The prices are good" · "The staff are great."*

Dependencies: Commercial (price + product maintenance, minimizing price changes); Marketing (price/promotion/POS policy); Property (ergonomic checkouts); Replenishment (3-point check, sales forecast → staff scheduling); IT.

Open decisions:
- Group IT solution for productivity scheduling?
- Group best practice for concessions operations?
- Group best practice for central vs local price changes?

### 4. Space, Range & Display (Janet Smith, 23 June 2006 v04)

**Role:** Space allocations for new/existing stores; range + planogram building across store formats/sizes/profiles; in-store implementation; central + store processes/systems/information.

Benefits: optimal space, relevant ranges per customer profile, displays that make shopping easy and support ops, processes simple for stores.

Dependencies: Commercial (product file + hierarchy linkage); Supply Chain & Distribution (ranges to right stores on time, correct capacities in ordering); Store Operations (information); Property (new stores + refits); MIS (SR&D reporting).

Open decisions:
- Best-practice SR&D systems?
- Impact of Central European buying + regional buying in China?
- Hand-over point with Property for floor plans (new stores, extensions, refits)?
- Who owns "planning new & discontinued lines" — Supply Chain or SR&D?
- Where will depot + store range records be held? Where will capacities be calculated/held?

### 5. Forecast & Ordering (Jurrien Heynen, June 2006 v3)

**Role:** Forecast expected sales; order stock for stores + DCs from suppliers; plan volumes in the physical distribution network.

Benefits: max stock availability, minimal store waste, lowest possible store-warehouse stock, min in-store replenishment cost, simple store processes that enable max availability at min operating cost.

Dependencies: Commercial (promotions, NPL, one-off buys, logistics data); SR&D (shelf capacity, ranging by store, stock-clearance support); MIS (actual store sales).

### 6. People (Jenny Wilkinson, June 2006)

**Role:** Deliver the four Tesco people promises — *"treated with respect" · "a manager who helps me" · "an interesting job" · "an opportunity to get on."*

Benefits: Tesco is a great place to work; people are equipped to deliver the Every Little Helps shopping trip; right information for strategic decisions + legal compliance.

Dependencies: people managers throughout the business; leadership teams; People Matters Group (governance); Business Planning; Budgeting; Payroll; IT + Support Services.

Principles include: interesting jobs, welcoming workplace, clear JDs + objectives + development plans, great training, supportive managers, fair + consistent decisions, flexible + fair on attendance, fair reward, regular feedback + coaching, annual performance review (two/year for managers), non-discriminatory selection/training/development, listen to staff ideas.

### 7. Property Services (Seth Lazarus, 6 July 2006 V.5)

**Role:** Plan + build new trading space; refit/expand/maintain existing space; store blueprints + design standards; energy consumption + engineering standards.

Benefits: enable company growth via new trading/mall space; minimize capital investment while maintaining standards; minimize environmental impact; great place to shop; safe + simple workplace.

Principles: customer first; always challenge "can we design it better, simpler, cheaper?"; functional not extravagant; simplest operation; corporate responsibility; respect consultants/suppliers/contractors; capital + life-cycle cost awareness; **create once, replicate many**; world-class Property Services Teams; responsibility + integrity; beat targets.

Dependencies: Property Acquisition + Site Research; SR&D; Marketing / Property Insight; Retail Operations; Asset & Mall Management.

Open decisions:
- Who owns Site Acquisition, Site Research, Corporate Purchasing within TOM?
- Best-practice Property Services systems (International, UK, both)?
- How do other best-practice systems impact Property Services (e.g. SR&D)?

### 8. Supply Chain (V15 — image-only deck)

Deck title: *TOM-Business Model V15 Supply Chain*. Markitdown extracted slide-number markers only — the deck is image-only (diagrams rendered as raster images without a text layer). Use LibreOffice/PowerPoint/Keynote to view, or OCR the exported images, if the content is needed.

## Why This Matters

This engagement represents **the pre-Secure retail career archive in its fullest form** — a Phase-1 operating-model library covering 8 domains of a global retailer, produced during Jeffe's IBM consulting era. Direct relevance to GrowDirect / Canary:

- **Operating-model doctrine** — the same top-down method (what we do / why / how we measure) informs today's Factory Pipeline SDD, Manifesto versioning, and CRDM domain partitioning.
- **Level-1/Level-2 process decomposition** — precedent for how Canary SDDs should layer (strategic intent → functional capability → technical spec).
- **Dependency mapping + open-decision framing** — the deck template's "Key Decisions To Be Made" section is a clean pattern for any future SDD.
- **Principles section (Property Services)** — "Create once, replicate many" is an early articulation of the same reuse doctrine that lives in Canary's CRDM design today.

## Related

- [[Brain/projects/Secure|Secure MOC]]
- [[Brain/wiki/secure-retail-career-archive|Pre-Secure Retail Career Archive]] — higher-level index of the IBM consulting era
- [[Brain/wiki/secure-tesco-property-it|Tesco Property IT Discussion (2002–2006)]] — adjacent property-services IT context
- [[Brain/wiki/secure-tesco-integrated-maps-2003|Integrated Maps (2003)]] — earlier adjacent IBM/SAP integration work
- [[Brain/wiki/secure-dv-private-label-2006|DV Private Label Food Setup (Aug 2006)]] — same year design-validation follow-on
- [[Brain/projects/GrowDirect|GrowDirect MOC]] — forward lineage

## Sources

- `Brain/raw/inbox/TOM Top Down Design 9 July/Commercial Operating Model v4.ppt`
- `Brain/raw/inbox/TOM Top Down Design 9 July/Tesco Operating Model - Finance ver2.ppt`
- `Brain/raw/inbox/TOM Top Down Design 9 July/Top Down Design -Retail Ops JB final.ppt`
- `Brain/raw/inbox/TOM Top Down Design 9 July/060623 Top Down Design  Space, Range & Display v04.ppt`
- `Brain/raw/inbox/TOM Top Down Design 9 July/TOM Forecast  Ordering v3.ppt`
- `Brain/raw/inbox/TOM Top Down Design 9 July/Summary Document People Work in progress.ppt`
- `Brain/raw/inbox/TOM Top Down Design 9 July/TOM Top Down Design - Property pack template Jul 06 V5.ppt`
- `Brain/raw/inbox/TOM Top Down Design 9 July/TOM-Business Model V15 Supply Chain.ppt` (image-only deck)

Extraction path: LibreOffice converted legacy `.ppt` → `.pptx`, markitdown extracted text.
