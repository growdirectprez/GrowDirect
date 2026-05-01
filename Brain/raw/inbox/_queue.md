---
title: Third-Branch Corpus — Running Intake Queue
type: queue
status: accumulating
created: 2026-04-24
updated: 2026-04-24 (batch intake complete: 268 notes, 0 ingest failures)
purpose: |
  Lightweight running log of uploaded / discovered source material while the
  founder is in flow. Each entry is one-to-three lines. No synthesis happens
  here. When the founder signals "build the picture" (or equivalent), the
  queue is drained in one pass — intakes written where warranted, wiki
  articles authored where warranted, thesis-layer articles updated, and a
  single dispatch produced.

  Rule: this file is a backlog, not a deliverable. Nothing gets threaded
  into the thesis from here until the founder calls the synthesis pass.
---

# Third-Branch Corpus — Running Intake Queue

## Already processed (reference, not backlog)

- ✅ **TTL Functional Spec V1.0/V1.2 + TTL043 + RedSky proposal + Service Def**
  — founder authored 18 July 2006, US Technical Library. Intake at
  `tesco-technical-library-corpus.md`, wiki at `[[tesco-technical-library]]`,
  threaded into `[[third-branch]]` and `[[intactix-canonical-validation]]`.
- ✅ **SRD S039 + S101 (SEL interfaces)** — intake at
  `srd-shelf-edge-label-interfaces.md`, wiki at `[[srd-shelf-edge-label]]`.
- ✅ **JDA Intactix 2006.2.0 (5 integration guides)** — wiki at
  `[[intactix-canonical-validation]]`.
- ✅ **Batch intake 2026-04-24** — six corpora extract+ingest via
  `content-engine/batch-intake.sh` (dispatch: `dispatches/2026-04-24-batch-inbox-intake.md`).
  268 intake notes created, 0 ingest failures. Extract manifests +
  per-corpus `.extract-failures.json` under `Brain/raw/.extract/`. Log at
  `Brain/raw/.logs/batch-intake-20260424-144143.log`.
  - `SWINDON/` — 67 intakes (PwC UK SAP Retail CoE, 1999–2000).
  - `Katz/` — 140 intakes (PwC SCM engagement Phase I+II, 2003).
  - `Other Retek Decks/` — 20 intakes (Retek v10 reference library, 2003–2005).
  - `BV Nuggets/` — 4 intakes (Saucier BroadVision playbook, 1999–2000).
  - `EBiz Def Des Dev/` — 3 intakes (PwC Web Implementation Guide template, 2000).
  - `BP/` — 34 intakes (consulting reference library 1997–1999: PwC/MH retail
    decks + PETsMART SAP blueprint + Finance best-practices pack).
  Synthesis pass still owed — wiki articles not yet authored. See
  "Threads currently tracked" and "Open decisions" below for the map.

## Queue — unprocessed, awaiting synthesis pass

### Uploaded 2026-04-24 (six files)

- **`Over Short Reporting Revised.pptx`** — Nov 2016 cash-variance dashboard
  by cashier / register / time. Distinctive: *"CRDM to summarize transactions
  by cashier, day, lane."* Thread: post-F&E / Secure-era LP-adjacent. **Flag:**
  second CRDM appearance in corpus (first was 2007 SEL delivery at F&E) —
  need founder decision on whether this is Sysrepublic's CRDM extending
  across a decade into cashier exception, or a different CRDM.
- **`Property App Overview.ppt`** — IBM BCS Project Aquarius, 2006, F&E site
  acquisition + property management requirements. Integrates MapInfo Site
  Tracker + QuickBase + Verasi + Oracle Project Costing. Thread: **new —
  potential fourth canonical (Site / Property) underneath the three retail
  canonicals.** Decision needed: does Site belong in RetailSpine or stay
  sibling?
- **`Oracle Project Costing User Guide.pdf`** — Oracle R11i standard doc,
  290 pages, no F&E specifics. Thread: supports Aquarius (project-costing
  module referenced). Hold as reference.
- **`2210 updated DS processes[1].ppt`** — **John Lewis Partnership** (not
  Tesco) property/FM RACI, June 2006. Thread: outlier. Likely F&E team
  studying JLP governance during design. Hold as competitive-intelligence
  reference; probably not load-bearing.
- **`DV Private Label Food Setup v3.ppt`** — **USA Design Validation
  Workshop**, w/c 21 Aug 2006, Tesco plc proprietary. Four product types
  (PL Food, PL non-Food, Kitchen, Branded), Aug–Mar 2006–2007 deployment
  timeline, Range 1 Sign-off → Product File Complete → Mock Store Filled.
  Thread: **TTL operator-side** — the workshop that consumes the TTL spec
  I authored five weeks earlier. Strengthens C090 canonical proposal with
  field-level detail.
- **`Copy of FnE DSD Annual Summary iRED view.xlsx`** — Apr 2018 modified
  date, 60+ vendors, Direct Store Delivery analytics, rolling 12-wk + YTD,
  variance ratios, *"iRED"* = internal retail exception dashboard. Thread:
  post-F&E (2013 shutter → 2018 date); likely **SEG / Secure / xBR-replacement
  era** despite FnE-branded filename. **Flag:** provenance question — is
  this F&E data held into the SEG era, or SEG-era analytics with FnE
  branding leftover?

### Uploaded 2026-04-24 — second drop (seven markitdown-extracted TOM files)

Pre-extracted markdown; already have frontmatter from markitdown pipeline;
tagged `[secure]` in source frontmatter (tag set looks wrong — the TOM
docs are F&E-era June 2006, not Secure-era; retag needed during intake).

- **`top-down-design--retail-ops-jb-final.md`** — 2026-04-23 extract. Tesco
  Operating Model — Retail Operations, Tim Golding + Richard Dodd, June 2006.
  Covers Service Productivity, Price Integrity (shelf-edge label matches
  checkout), Tender Management, dependencies across Commercial, Marketing,
  Property, Replenishment, IT. **Sibling artifact** to the SRD Top-Down
  Design doc already in Brain as `060623-top-down-design--space--range---display-v04.md`.
  Thread: **F&E / TOM 2006 corpus — operating model by workstream.**
- **`commercial-operating-model-v4.md`** — Lucy Williams, June 2006, v4.
  Commercial workstream: range strategy, buying, cost management,
  promotions, KPI review. 517 lines. Thread: F&E / TOM 2006.
- **`tom-forecast--ordering-v3.md`** — International Operations Development
  Design Group, June 2006. Forecasting, supplier ordering, distribution
  planning. 323 lines. JDA ASR/PRO territory. Thread: F&E / TOM 2006.
- **`tesco-operating-model---finance-ver2.md`** — Lisa Baglin, June 2006.
  Fixed assets, working capital, financial reporting. Open decisions on
  invoice matching and transaction processing location. 217 lines.
  Thread: F&E / TOM 2006.
- **`tom-business-model-v15-supply-chain.md`** — TOM v15 Supply Chain.
  29 lines — OCR failed, image-heavy deck; needs visual extraction.
  Thread: F&E / TOM 2006 (partial).
- **`copy-of-2018-02-02-eagle-eye-functional-and-non-functional-requirements-v4-0-ns-comments.md`**
  — Eagle Eye Functional & Non-Functional Requirements v4.0, Feb 2018,
  with "NS comments" (likely Sysrepublic Neil Shaw or similar reviewer).
  35 requirements covering fraud investigation case prioritisation,
  search, data storage, payment types, dashboards. Thread: **post-F&E
  Secure / xBR-replacement era** — same thread as Over/Short 2016 and
  iRED 2018.
- **`copy-of-fne-dsd-annual-summary-ired-view.md`** — the same iRED
  vendor-analytics workbook as before, now in markdown form. 269 lines.
  Thread: Secure / xBR-replacement era (still open provenance
  question: F&E-era data held, or SEG-era data with FnE branding?).

**Observation — the F&E / TOM 2006 corpus is a set.** Six workstream
decks (Retail Ops, Commercial, Forecast & Ordering, Finance, Supply Chain,
plus the already-in-Brain SRD top-down-design) authored June 2006 by
named F&E / Tesco International leaders. This is the operating-model
skeleton the TTL spec and SRD interface specs instantiated. Treat as one
corpus at synthesis time.

### Discovered 2026-04-24 (three folders already in Brain/raw/inbox/)

- **`BP/`** — 46 files (25 .doc + 21 .ppt ≈ founder says "40 files" —
  approximation), 7.9 MB, dated Oct 1997 – Jul 1999. **CORRECTED
  classification — this is a consulting reference library the founder
  accumulated, no Pitney Bowes internal content. Three sub-corpora by
  engagement provenance, not by filename pattern:**

  **Cluster A — PwC / Management Horizons retail best-practices deck
  library (12 .ppt, 1997–1998).** Source tag "MH/PW" on Vendor Mgmt.ppt
  = Management Horizons / Price Waterhouse (Management Horizons acquired
  by Price Waterhouse 1992, merged into PwC 1998). Generic industry-wide
  retail process-flow reference decks. Files: `RTV.ppt`, `Vendor Mgmt.ppt`,
  `Invoice Verif.ppt`, `Inventry Cntrl.ppt`, `Import Mgmt.ppt`,
  `Perf Mont.ppt`, `Sales Audit.ppt`, `Spc Mgmt.ppt`, `Forwrd Buy.ppt`,
  `Cat Mgmt.ppt`, `Efficnt Asst.ppt`, `Event Mgmt.ppt`. Numbered process
  flows (10.1–10.5), vendor-partnership progression ladder
  (UPC/EDI → QR → Collaborative Forecasting → VMI → Joint Dev), General
  Merchandise vs. Food & Drug comparisons. This is the canonical PwC
  Retail template library for the late-1990s.

  **Cluster B — PETsMART SAP Retail implementation blueprint (21 .doc,
  Jan 1998).** Specific client blueprint, not generic reference.
  16 M-prefix module specs + 5 date-prefix workshop docs. Format signature
  per spec: Objectives / CSFs / Assumptions / Requirements / Resolutions /
  Performance Measures / Issues / Better Practices / Existing SAP
  functionality / Jobs Analysis / Reports / Forms. PETsMART named client,
  SAP Retail 4.0 named target platform, Intactix named space-management
  integration partner. Files:
  - Module specs: `Asstmgmt.doc` (624 lines — Assortment Mgmt),
    `Vm000.doc` (695 lines — Vendor Mgmt), `mpo000.doc` (659 lines — PO
    Mgmt), `mrp000.doc` (433 lines — MRP / Replenishment), `msm000.doc`
    (277 lines — Stock Mgmt), `mfo000.doc` (297 lines — Forecast &
    Ordering), `mem000.doc` (288 lines — Event Mgmt), `Mpi000.doc`
    (319 lines — Pricing), `Mfp000.doc` (283 lines — Financial Planning),
    `Mcc000.doc` (252 lines — Cost Control), `Mrv000.doc` (241 lines —
    RTV), `Dm000.doc` (206 lines — Distribution Mgmt), `Miv000.doc`
    (189 lines — Invoice Verification), `Mwd000.doc` (155 lines —
    Warehouse Distribution), `Mws000.doc` (117 lines — Warehouse Mgmt),
    `Traffic.doc` (64 lines — Traffic).
  - Workshop notes (Jan 28–30, 1998): `980128ib.doc` (111 lines),
    `980128sr.doc` (64 lines), `980130am.doc` (254 lines — heaviest,
    likely Assortment Mgmt workshop), `980130xf.doc` (195 lines),
    `980130tb.doc` (109 lines).

  **SMOKING-GUN ARTIFACT — preserve verbatim:** `Asstmgmt.doc` Issues
  section for Assortment Management contains the sentence: *"There is
  an issue with regards to the integration of a space management system
  (i.e. Intactix) with the assortment and listing functions in SAP. The
  objective is to control listing (and thus replenishment) for all SKU's
  in the stores through the use of planograms."* This is the ordering-gate
  architecture — planogram assignment gating item activation for
  replenishment — documented in January 1998, eight years before F&E /
  SRD / Tesco built the same thing with Intactix in the same role.
  **Primary-source evidence for Branch B of Third Branch thesis:
  consulting documented this architecture in 1998, SAP couldn't solve
  it cleanly, the question re-surfaced unsolved in 2006.**

  **Addendum — ERP-sidestep birth-certificate quote (`980128ib.doc`,
  dated 1998-01-28, Vendor Management / Investment Buying workshop
  notes, section P Implementation Considerations):** *"Currently
  investment buying and MRP calculations will be completely separate
  processes (and SAP will choose the larger of the two values) but
  promotional purchases will be considered additions to the selected
  value."* The consultants building PETsMART's SAP Retail 4.0
  implementation document, as a requirement, that SAP's native MRP
  cannot reconcile investment buying against forecasted demand — so the
  retail logic has to live in a parallel process that hands values to
  SAP. Branch A (ERP-sidestep) being written down inside an SAP
  implementation by the team supposed to make SAP work for retail.
  Pair with the Asstmgmt.doc smoking-gun: same engagement, same month,
  two separate modules where retail logic has to sit outside SAP.
  Both load-bearing for Retail Manifesto draft.

  **Cluster C — Finance best-practices pack (13 .doc, Jun–Dec 1999).**
  Customized onto a financial-exchange-integration engagement (three-
  scenario header: Current Structure / Current Structure with Cooperative
  Agreements / Integrate All Exchanges). AP, AR, EDI Tech, Integrated
  Financials, Gen Acct, Shared Services, Outsource, Payroll, Perf
  Indicators, Planning, Reporting, Staffing, Treasury. Highest-leverage
  file: `BEST PRACTICES - INTEGRATED FINANCIALS.DOC` — 70+-retailer
  named list with integrated financial systems circa 1999.

  **Thread: Consulting reference library (1997–1999) — accumulated
  by founder as reference material across three engagement contexts.**
  Feeds Branch B of Third Branch thesis with primary-source evidence:
  PwC Retail template library (Cluster A), PETsMART SAP blueprint with
  the 1998 Intactix-SAP smoking-gun sentence (Cluster B), finance-
  exchange-integration best-practices pack with retailer list (Cluster C).
  Representative artifacts: `Vendor Mgmt.ppt` (Cluster A), `Asstmgmt.doc`
  (Cluster B — SMOKING GUN), `BEST PRACTICES - INTEGRATED FINANCIALS.DOC`
  (Cluster C — retailer list).

- **`BV Nuggets/`** — 6 files (4 .doc/.ppt + 1 .xls + 1 .pdf), 2.3 MB, dated
  Jul 1999 – Jun 2000. Curated BroadVision implementation playbook by
  **Christian Saucier** (BV impl lead). Contains `BV Lessons Learned and Best
  Practices.doc` (66 revisions, final Jan 2000), `00-01-29 Sizing a
  BroadVision Site.ppt`, `Vignette vs Broadvision.xls`, `creativegood-guide.pdf`.
  Thread: **BroadVision 1999–2000 platform** — directly under Branch C;
  technical/competitive corpus from the era the founder was building AE.com
  and deploying BV at PB/Stamps.com. The Vignette-vs-BV spreadsheet is a
  contemporaneous competitive-intelligence artifact worth preserving.

- **`EBiz Def Des Dev/`** — 3 files (3 .doc), 5.1 MB, dated Sep–Oct 2000.
  PwC sample Web Implementation Guide — **Def**inition (20K words),
  **Des**ign (32K words), **Dev**elopment (17K words). Saved by PWCUSER,
  ~48 revisions. Classic PwC consulting methodology template.
  Thread: **PwC consulting 2000–2003** — the methodology-template layer
  parallel to the 18 extracted PwC/IBM client decks already in Brain.
  Strengthens the "consulting got the questions right but shipped discrete
  labor" claim in `[[third-branch]]` §I Branch B by giving us the actual
  template the labor was being shipped against.

- **`SWINDON/`** — 359 files, 68 MB, Jul 1999 – Apr 2000.
  **PwC UK SAP Retail Center of Excellence corpus** (Swindon, UK).
  Provenance (per founder): T&K is a fictitious retailer PwC
  invented for the CoE lab; prospective retail CIOs visited the
  Swindon offsite to begin their SAP Retail journey. Founder was
  on-site for six weeks. Founder *delivered* a production B2C
  multichannel home-delivery e-commerce platform circa 1999 with
  **SAP Retail backend + BroadVision front end** — the canonical
  stack this corpus documents. Top-level `index.htm` labeled
  *"PricewaterhouseCoopers & BroadVision Co-develop Methodology."*

  **Reference-material index for functional-spec reuse:**

  *Working code & reference implementations:*
  - `SWINDON/TKSITE/` — 180+ files. Full JSP/Dreamweaver e-commerce
    site build: product detail templates, shopping cart, order
    tracking, category trees, navigation. **Working code pattern
    for multichannel B2C e-commerce front end on BV.**
  - `bvsn.mdb` — Access DB with BV demo data schema.
  - 17 .jsp files + 37 HTML/templates — JSP/BV rendering patterns.
  - 16 .zip archives — release builds.

  *Functional / methodology documents (SAP Retail + BV integration):*
  - `T&KSTORYLINE v0.08.doc` / `v1.01.doc` — customer-walkthrough
    narrative = de facto functional spec for the reference build.
  - `T&K_Templates.ppt`, `T&K customization.doc`, `T&K cleanup.doc` —
    the configuration/customization patterns applied to the lab.
  - `tk_products.xls` — fictitious catalog (schema reference for
    retail product master + BV catalog structure).
  - `T&K_Demo_12_18_99.ppt` / `T&K_Demo_12_20_99.ppt` — demo decks.

  *Alternate platform track:*
  - `RSC_INTERSHOP_DEMO.ppt`, `RSC_Sitemap.ppt`, `RSC_Templates.ppt`,
    Scenario_1/2/3 templates + revised scenario docs — RSC (Retail
    Supply Chain) track on **Intershop** rather than BroadVision.
    Parallel proof / non-BV methodology path.

  *Generic retail reference:*
  - `Retail demo.ppt` (2.9 MB), `Retail_Script_12_21_99.doc`,
    `Retail.ppt`, `GemKeySOW.doc` (743 KB — GemKey codename,
    clarification needed).

  *Subfolder layout:* `TKSITE/` (full site build, with
  `fireworks/`, `BUTTONS/`, `IMAGES/`, `GEOFF/`, `Library/`,
  `Templates/`, `Ezine Sample Site/`), `Reading/` (reference
  materials — Personalization.pdf, ICE-Comms, Patricia, Which?,
  datapro), `Release Notes/` (8 version builds), `Additional
  documentation/` (3 archive sets).

  *Pair with:* `BV Nuggets/` (Christian Saucier's post-engagement
  playbook — same window, same stack) and `EBiz Def Des Dev/` (PwC
  Web Implementation Guide template, Sep–Oct 2000).

### Discovered 2026-04-24 — Retek / Katz corpus (already in inbox, previously uncatalogued)

**Flag from the founder:** "do we have stock ledger and perpetual inventory
as a concept covered? thats what a merchandising system is. perpetual inventory
movement was the buzzword back then before real time was a thing."

**Status of canonical framing, honestly:** the RMS canonical is currently
framed in `[[third-branch]]`, `[[tesco-technical-library]]`, and
`[[intactix-canonical-validation]]` as "identity master / who the product is."
That framing is incomplete to the point of being wrong. A merchandising
system is fundamentally a **perpetual inventory movement ledger** with an
identity master attached. Receipts, transfers, adjustments, cycle counts,
sales, shrink, RTVs — every one posts as a movement against on-hand. The
whole edifice of replenishment, allocation, and financial close sits on
the integrity of that ledger. SRD's ordering gate and TTL's pack-copy
compile gate are both gating *against the ledger*. Without naming the
ledger the three-canonical story has a hole where its substrate should be.
**This is a manifesto-synthesis-pass correction, logged here, not
rewritten in-session.**

#### Batch D1 — `Other Retek Decks/` (29 files, ~2003-2005 Retek v10 reference library)

- **`Retek RIB.Ahlens Solution.doc`** — founder-pointed. Ahlens (Swedish
  dept-store chain) RIB (Retek Integration Bus) solution doc. RIB is the
  perpetual-inventory message bus between RMS and every downstream system
  (warehouse mgmt, POS, data mart, price mgmt). Thread: **perpetual
  inventory canonical / merchandising as ledger.**
- **`Retek.RMS to RDM Interfaces.Ahlens.xls`** — founder-pointed. RMS to
  RDM (Retek Data Mart) interface specification for Ahlens. The movement
  ledger flowing out of RMS into the analytics surface. Thread: perpetual
  inventory + reporting substrate.
- **`Pages from rib-101-intg.pdf`** — founder-pointed. RIB 10.1 integration
  guide excerpt. The canonical Retek integration architecture. Thread:
  perpetual inventory canonical.
- **`Retek 10 Architecture Overview - IBM View @ 030203.ppt`** — Feb 2003,
  IBM Global Services' view of Retek v10 architecture. Thread: Retek
  platform + IBM consulting context (Branch B).
- **`Retek Appl Arch q1 00 (Retek Ratified).ppt`** — Q1 2000, Retek-ratified
  application architecture. Thread: Retek platform history (pre-Oracle
  acquisition, which happened 2005).
- **`Retek Application Arch Data model Xi v0.1.vsd`** — Visio, Retek Xi data
  model. Thread: Retek platform — data-model artifact.
- **`Retek Full Suite.ppt` + `Retek V10 NRF Deck - SCM.ppt` + `Retek SOP POP.zip`**
  — Retek sales decks (NRF = National Retail Federation, the industry
  trade show). Thread: Retek platform marketing / competitive positioning.
- **`Retekv10-Modules.Key Blocks.doc`** — Retek v10 module inventory.
  Thread: Retek platform — module map.
- **User guides (PDFs)** — `rms-110-ug.pdf` (RMS 11), `resa-110-ug.pdf`
  (ReSA 11), `reim-100-ug.pdf` (ReIM 10 — invoice matching), `rtm-100-ug.pdf`
  (RTM 10 — trade management), `topplan-100-ug.pdf`, `ro-100-ug.pdf`
  (Retek Ordering), `Pages from rdf-100-ug.pdf` (RDF 10 — demand
  forecasting), `rpm-ips-qref.pdf` (RPM price mgmt quick ref).
  Thread: Retek platform — module-level reference.
- **Architecture/ops PDFs** — `Retek RestartRecovery.pdf`,
  `Retek Scalability.pdf`, `Retek Security.pdf`,
  `Retek  External System Integration Approach v2.pdf`,
  `Retek Hardware Architecture.pdf`, `Retek Performance Lab.pdf`. Thread:
  Retek platform — non-functional / ops artifacts.
- **`RMS 10.0 Sizing Tool Questions - v1.xls`** +
  **`Typical Retek Sizing Input Requirements 270303.doc`** — sizing
  artifacts (Mar 2003). Thread: Retek deployment — scope-and-size intake.
- **`AIP Tech Overview 1103.ppt`** — AIP (Advanced Inventory Planning),
  Nov 2003. Thread: perpetual-inventory + forecasting adjacency.
- **`Range&Space.ppt`** — Retek range & space module. Thread: parallels
  Intactix / JDA space planning on the Retek side of the industry.
- **`RPOS Presentation.ppt`** — Retek Point-of-Sale. Thread: store-side
  of the perpetual-inventory ledger (where sales movements originate).

#### Batch D2 — `Katz/` (Phase I + Phase II, 2003 PwC-style SCM engagement)

Katz Group (Canadian drug-store chain — Rexall, PharmaPlus, IDA, Guardian,
PPD banners). 2003 retail supply-chain optimization + system selection
engagement. **~100+ files.** This is the canonical Branch-B artifact: a
complete PwC/IBM-style methodology applied to a real mid-market retailer,
including RFP to five vendors, vendor responses, Gartner input, and a
business case. Preserves verbatim the "questions-side" of the Third
Branch thesis — the operating-model questions consulting was asking
well, before shipping discrete labor against those questions.

- **Phase I — diagnosis & vision** (22 Apr – early June 2003):
  - Executive interviews: Al Wilkie, Craig Taylor + Jonathan Alpert,
    Peter Davidson, Sue Macabe, George Edwards, Grant Schwartz, Bruce
    Moody, Larry Latowsky (8 execs).
  - Store visits: ~30 stores across banners — Commerce Court, Metro
    Centre, Church & Wellesley, Bay & Dundas, Sudbury Rexall, GDN King
    City, IDA Azilda, IDA West Mall, PPD 1st Canadian, Lakeshore,
    PPD Metro Centre, REX Sudbury Downtown, REX Milton, REX Bay &
    Dundas, Montreal Square, Bayshore, Carleton Place, Lunenburg,
    Crossroads, Fall River, others. Apr 28 – May 22, 2003.
  - As-is workshops: ProPharm, POS, Manage Pricing, Forecasting,
    Category Mgmt, Inventory, Move, Manage Vendor (May 5–12, 2003).
  - Executive visioning: McKesson precedent deck + Katz visioning
    session (Jun 4, 2003).
  - Balanced scorecards (retailer egcards, balanced scorecard xls).
  - Benchmarking: Katz Supply Chain Metrics, IHL - IT in Drug Chains.
  - Inventory analysis: turns by vendor, turns by vendor+category,
    discontinued-by-store, service levels.
  - Business case: benefits case v2, retail systems cost model draft
    v5, NPV model v2, solution contribution to value opportunities v3.
  - Kick off, SC#1, SCOA Final Report + Appendix decks.
  - Change management: Draft CRA Katzv6.ppt.
- **Phase II — selection & design** (Jul – Sep 2003):
  - To-be workshops: Manage Finance, Store Operations, Suppliers,
    Merchandising, Planning & Analysis, Planning & Distribution.
  - Katz Requirements v4 (the functional requirement set that becomes
    the RFP evaluation grid).
  - **RFP distributed to five vendors**: Retek, SAP, JDA, JD Edwards,
    i2. Separate RFP doc per vendor.
  - **RFP responses**: Retek final response (loaded into Brain-inbox),
    SAP response (with draft license agt + escrow agreements and
    Canadian exhibits), JDA response (Form 10Ks 2001 + 2002, Special
    Interest Group outline, Customer Agreement).
  - Gartner input: Retek vendor rating, SAP Top-10 Questions.
  - IT architecture: Current Assessment & Opportunities v3.4 (Aug 2003),
    Katz Architecture 08/26/03 deck.
  - Phase II SC#1 deck + To-Be Workshop Participants + Phase II Kickoff.

**Thread placement:**
- **Retek corpus** — new thread: `[[retek-rms-perpetual-inventory]]`
  (wiki not yet written). Sibling to `[[intactix-canonical-validation]]`
  and `[[tesco-technical-library]]`. Supplies the perpetual-inventory
  / stock-ledger substrate that the three-canonical story currently
  names (RMS) but does not actually describe.
- **Katz engagement** — new thread: `[[katz-scm-2003-engagement]]`
  (wiki not yet written). Branch B load-bearing artifact — the
  methodology-applied-to-a-real-retailer case that shows what PwC/IBM
  consulting was actually delivering in 2003. Parallels the 18 PwC/IBM
  client decks already in Brain and the EBiz Def/Des/Dev methodology
  templates. *Note: `kroger-retek-project-sam-xls.md` already exists
  in inbox as a sibling Retek deployment intake from the prior Secure
  sprint — these thread together.*

**Related already in Brain:** `kroger-retek-project-sam-xls.md` (prior
Secure/Kroger intake) — Kroger Retek deployment. Shares the perpetual-
inventory-canonical thread with the new Retek/Ahlens material and
the Katz Retek RFP response.

### Threads currently tracked

- **TTL** — spec canonical (what the product is). Founder-authored 2006.
  Wiki exists; may grow with DV v3 field detail + Jan 2007 snapshot zip.
- **SRD** — planogram canonical (where the product is). 323 files; S-prefix
  interface catalog; SEL compile wiki exists.
- **RMS / Oracle Retail** — merchandising canonical (who the product is).
  Not yet its own wiki; referenced through TTL kill-switch and SRD ordering
  gate.
- **Site / Property / Project Aquarius** — candidate fourth canonical (pre-
  retail, enables retail). **Open decision.** Files: Property App Overview,
  Oracle Project Costing guide.
- **Post-F&E LP / Secure-era** — 2016 Over/Short + 2018 iRED DSD. **Open
  provenance question.**
- **JLP reference material** — outlier, hold.
- **Pitney Bowes 1997–1999 dual corpus** — new. `BP/`. Founder-confirmed
  two layers: (1) PB-era retail consulting / client work (12 retail-ops .ppt
  + 16 M-prefix module-code .doc + Jan 1998 three-day workshop) feeds Branch B
  questions-side — PB was running retail engagements, founder accumulating
  merchandising-process vocabulary that resurfaces at Katz/F&E/Intactix;
  (2) PB internal finance best-practices pack (13 .doc, 1999) — non-retail
  slice. 46 files total.
- **BroadVision 1999–2000 platform** — new. `BV Nuggets/`. Implementation
  playbook + Vignette competitive intel, curated by Saucier. Directly under
  Branch C. 6 files.
- **PwC consulting methodology 2000–2003** — new. `EBiz Def Des Dev/`. Def/Des/Dev
  template. Parallels the 18 PwC/IBM client decks already in Brain; supplies the
  template-layer to the "consulting got the questions right" argument. 3 files.
- **Retek / RMS / perpetual inventory canonical** — new. `Other Retek Decks/`
  (29 files) + Ahlens deployment + `kroger-retek-project-sam-xls.md` already
  in Brain. Wiki not yet written. Supplies the perpetual-inventory-ledger
  substrate the three-canonical framing currently names but does not
  describe. Founder-flagged as a load-bearing gap.
- **Katz Group 2003 SCM engagement** — new. `Katz/` Phase I + Phase II, ~100+
  files. PwC-style SCM diagnosis → system selection across 5 vendors (Retek,
  SAP, JDA, JDE, i2). Branch B artifact — the canonical "consulting got
  the questions right" engagement with all the working papers preserved.

### Open decisions (for the synthesis pass, not now)

1. Site as fourth canonical vs. sibling-stack — does RetailSpine carry it or
   not?
2. CRDM decade-spanning reading vs. two-CRDMs reading.
3. Over/Short + iRED — F&E-provenance or SEG-provenance?
4. JLP DS-processes doc — cite once as F&E-design-era reference or drop?
5. Canary fresh-prep module timing — when does C090 TTL-descendant canonical
   land on the Canary roadmap?
6. **Stock ledger / perpetual inventory as canonical property, not sibling
   canonical.** Proposal for the manifesto synthesis pass: name the RMS
   canonical's core as *perpetual inventory movement ledger + item master*,
   not just "identity master / who the product is." The ledger is the
   substrate; SRD gates ordering *against the ledger*; TTL gates pack-copy
   compile *for items the ledger knows exist*. Do not add a fourth
   canonical for inventory — fold it into RMS as its reason-for-existing.
   Decision to confirm at synthesis time.

## Adding to the queue

When the founder drops more files, append under a new dated subsection:

```
### Uploaded YYYY-MM-DD (<n> files)

- **`filename.ext`** — one-to-three line note. Thread: <which>. Flags: <any>.
```

No synthesis until the founder calls it. Append-only.
