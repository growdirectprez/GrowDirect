---
title: BroadVision 1999–2000 — the Platform Architecture
type: platform-architecture
status: v0.1
tags: [retail, ecommerce, broadvision, personalization, pwc, sap-retail, swindon, branch-c, 1999-2000]
created: 2026-04-24
updated: 2026-04-24
related:
  - "[[third-branch]]"
  - "[[academic-frame-1999-hbs]]"
  - "[[pwc-ebiz-web-implementation-guide]]"
  - "[[bp-consulting-library-1997-1999]]"
sources:
  - Brain/raw/.extract/BV Nuggets/BV Lessons Learned and Best Practices.doc.md
  - Brain/raw/.extract/BV Nuggets/Vignette vs Broadvision.xls.md
  - Brain/raw/.extract/SWINDON/  (PwC UK SAP Retail CoE reference implementation — T&K/BV stack, 67 intakes)
last-compiled: 2026-04-24
needs-review: 2026-05-08
---

# BroadVision 1999–2000 — the Platform Architecture

**Thesis.** BroadVision One-To-One 4.1 was the first commercial attempt at what the 2020s call *composable commerce*: a session/profile store, a content engine (the Dynamic Content Center), a rule engine decisioning against "communities," a catalog integrator, and a template tier (JSP + Dreamweaver + custom templates) glued to a transactional backend — typically SAP Retail. The vocabulary was right. The component model is recognisable a quarter-century later. The operating ceiling was the substrate: rules-against-communities decisioning, session cookies, relational profile tables, a DCC with no native authoring tool, and a Generic DB Accessor the vendor itself *"discourages"* over *"unspecified performance and scalability issues"* (Saucier, `BV Lessons Learned and Best Practices.doc.md`). The platform ran two floors above what 1999 could deliver at one-to-one scale. This brief is the *platform-architecture* companion to `[[third-branch]]` Branch C, which carries the Moon HBS 9-599-101 academic frame and the five BVAs. Here we describe what the engine actually was.

---

## I. Component model

BroadVision One-To-One 4.1 resolved to six identifiable components. Christian Saucier's *BroadVision Lessons Learned and Best Practices* (18pp, 66 revisions, final 12/09/1999) is the architecture-dense primary source, cited throughout.

| Component | 1999–2000 function | 2026 analogue |
|---|---|---|
| **Interaction Manager (IM) engines** | Server-side JSP evaluator parsing every file under `script-root`, resolving server-side JavaScript, caching compiled scripts | Application server / edge runtime |
| **Dynamic Content Center (DCC)** | Proprietary content repository for ads, editorials, products, incentives, templates, discussion groups; rule-resolution target | Headless CMS + content API |
| **Rule engine** | Resolves "rulesets" against profile-derived "communities," returns content ids for slot fill | Decisioning engine / feature store |
| **Profile / session store** | `BV_USER`, `BV_USER_PROFILE`, session variables, `BV_SessionID` / `BV_EngineID` cookie pair | Identity + CDP + session |
| **Commerce / catalog** | Retail Commerce 4.1 shopping cart, catalog, cross-sell, incentives, checkout | Commerce engine + PIM |
| **Generic DB Accessor / custom components** | C++ components exposed to IM; Java "a future release" | Service layer / microservices |

Canonical page-build: browser hits a JSP under `script-root`; IM initializes or rehydrates a session via the cookie pair; the template resolves slot rules against community membership; DCC returns content refs for each slot (`HP Banner Ad Ruleset`, `HP FP_A`–`FP_D Ruleset` per `rules.doc.md`); commerce hydrates catalog (joined against `sap_prices.xls.md`); the page ships.

Saucier on the engine's internal seam:

> "We can explain this by looking at a dynamic document as having three layers: the HTML layer, the server-side JavaScript layer, the component layer. Performance degradation occurs every time a jump is made from one layer to another." (*§III.2*)

Minimising script-tag transitions was a *page-level* optimisation concern in 1999. The 2026 equivalent of that boundary cost is roughly zero.

---

## II. Content, storage, and the DCC trade-off

Saucier's §II.3 — *Choosing a Home for Your Textual Data* — names three storage locations (DCC, file-system, database/external), each with a different failure mode:

> "Content designers must use the DCC to edit or add content and the DCC interface is not particularly well suited for HTML content editing. Integration between DCC and the file system or third party products is badly needed." (*§II.3.1*)

> "The migration tools used to extract and promote DCC data and rules have proven to be unreliable and unsupported by BroadVision… dates for the availability of a fix or patch have not yet been provided." (ibid.)

> "BroadVision discourages the use of the Generic DB Accessor because of unspecified performance and scalability issues… a tool that is likely to be required by many projects." (*§II.3.3*)

A content engine with no authoring tool, a data-access component the vendor told you not to use, and a rules layer whose dev-to-prod promotion was *unreliable and unsupported*. Hallmark's *"extensive profiling is the only personalization feature used on this site"* (see `[[third-branch]]`) is what happens when DCC migration tooling is unsafe.

---

## III. The PwC + BroadVision co-develop methodology (Swindon CoE)

Between late 1999 and February 2000, PwC's UK SAP Retail Center of Excellence at Swindon co-developed a reference implementation with BroadVision under the fictional retailer **T&K** (`T&KSTORYLINE v1.01.doc.md`, 15 Feb 2000). The storyline is the canonical 1999–2000 multichannel B2C stack — the pattern that shipped live at AE.com (see `[[third-branch]]` §Founder note).

### Architecture

The T&K architecture diagram (`Arch.doc.md`) is terse to the point of being a label list:

- **Real-time tier:** BroadVision · NetPerceptions · Loyalty Card · Customer Interface · Kiosk · POS · Customer PC
- **Non-real-time tier:** SAP / RIS · Data Warehouse · Valex (campaigns) · SAS / SPSS / Quadstone (data mining) · Business Objects · Aria (analytics)

BroadVision is explicitly *not* the personalisation — NetPerceptions does collaborative filtering, SAS does offline segmentation, Valex orchestrates campaigns. BroadVision is the *content and rules* layer for a web tier the other engines feed. Seven vendors, two-speed integration, one fictional customer.

### Reference implementation

- **Catalog** loaded from SAP (`product_load.xls`, `sap_prices.xls.md`) into a merchandise hierarchy (`Merchandise Hierarchy.doc.md`).
- **Cross-sells** authored as a relational lookup (`crossells.xls.md`), hundreds of `PROD_ID → RC_CONTENT_KEY → CrossSell` rows joining BV and SAP ids (`bv107 → sap245 CrossSell bv115`). The cross-sell engine is a hand-maintained table.
- **Customer data model** (`customer data model 12_28_99.xls.md`) extends `BV_USER` / `BV_USER_PROFILE` with language, currency, gold card #, price/brand sensitivity, purpose-of-use, service demands, and category preferences — plus side tables for addresses, history, wish list, reminders, auto-replenishment. The late-1990s CDP, hand-rolled per retailer.
- **Communities** (`rules.doc.md`): three labels — *Full range value shopper*, *Brand aware Luxury Shopper*, *Quality Basics shopper* — with homepage slot rulesets (BA_A banner, FP_A–D featured product, AD_A–C ads, IN_A incentive), one selection per slot per visit.
- **Customisation path** (`T&K customization.doc.md`): rebrand the demo for a client pitch by swapping ads, editorials, rule product references, and incentives via the Command Center. Retailer-by-retailer re-templating, not multi-tenant.
- **Functions inventory** (`Website_Functions.xls.md`) scored 59 features on Priority × Effort. Basket, persistent basket, cookies, cross-sell indicators, order confirmation — all *"Standard BroadVision Feature."* Rules-based matching, collaborative filtering, Community definitions — *"Majority of effort involves business analysis of data model."* The labour envelope of a BV engagement in one sheet.

Eleven demo scenarios stitched the components together: WAP birthday reminder → BV rule-triggered purchase → Valex direct mail → personalised home page from BV + Valex + NetPerceptions slots → kiosk → POS loyalty reconciliation. Every box on the Arch diagram touched. This is the frame AE.com, Pitney Bowes / Stamps.com, and the 1999–2000 BV retail cohort shipped against.

---

## IV. Competitive positioning — BV vs. Vignette

Two sources at `Brain/raw/.extract/BV Nuggets/`: *Vignette compete.doc* (BV internal, April 1998) and *Vignette vs Broadvision.xls* (side-by-side).

BroadVision framed the fight as *"BroadVision is an application; Vignette is a publishing platform"* — nine out-of-box personalisation capabilities against Vignette's *"no out-of-the-box support for personalization"* (*§2.B*). The caching critique is substrate-revealing:

> "Vignette does caching by pre-generating the entire page… if the TCL script is based on six parameters each with ten values then you are need to pre-generate a million pages (10*10*10*10*10*10)." (*§2.C*)

The spreadsheet is Vignette's rebuttal. Vignette scored harder on content management (workflow, version control, XML services, Office authoring, Dreamweaver) and visual template development (*"BroadVision: None. Partnership with Dreamweaver 2 for future visual development functionality."*); claimed N-tier against BroadVision's *"proprietary architecture [that] breaks down into… presentation logic, business logic, application server, and data."* Headcount: Vignette 340/250 customers/hundreds of live sites (largest >10M page views/day); BroadVision 234/274 customers/111 live sites (largest 230,000/day).

Two engines partitioning the category: BroadVision owned *rules-against-communities personalisation plus commerce*; Vignette owned *content workflow plus publishing scale*. Neither owned both. The 2020s unification into a single composable stack is the unresolved seam visible in every row.

---

## V. Sizing and ops

The sizing deck (`Brain/raw/inbox/BV Nuggets/00-01-29 Sizing a BroadVision Site.ppt`, 29 Jan 2000) is present as binary but not yet extracted to markdown. Operational-ceiling evidence therefore comes from Saucier.

Three deployment-discipline notes expose the substrate:

1. **IM-per-developer.** *"Your development environment should be setup with an IM engine for each developer (or at least one IM for each 2 or 3 developers)… Some organizations even go as far as creating a separate database table space for each developer!"* (*§VI.1*). Process isolation was per-developer because an IM crash took down everyone sharing it.
2. **Cache layering.** *"The BroadVision IM engines may keep a cached copy… The Web server may keep a cached copy… The browser may keep a cached copy… Any other layers in between, like a proxy server, may also keep a cached copy."* (*§V.2*). Four caches in series, none reliably invalidating.
3. **C++ components only.** *"Custom components can currently only be developed in C++; a future release of BroadVision will provide the ability to create components in Java."* (*§III*). *"The BroadVision IM engines are very sensitive to memory leaks within components"* (*§III.1*); Rogue Wave and Rational Purify were recommended.

Cross-checked against the 230,000-page-view/day BV ceiling in the Vignette comparison, rules-per-second throughput was bounded by IM count × cache-hit rate × component-layer transition cost. This is the engineering ceiling underneath the stamps-and-envelopes commercial ceiling in `[[third-branch]]`.

---

## VI. Saucier in his own voice

Three quotes closing the loop with the BVA gap quotes in `[[third-branch]]` §I.C:

- *"BroadVision is still evolving. Although it is one of the leading and best tools in its category, it has quite a bit of maturity to gain."* (*§VII*)
- *"The only sure way to make sure that a page does not get confused with a cached copy is to give each page a unique URL."* (*§V.2.3*)
- *"Failure to comply with this rule [no re-used function names] can lead to erratic results where an already cached function will be executed instead of a newly re-defined function of the same name within the script."* (*§IV.2*)

Sentences a client-facing BVA would never contain. Together with the DCC and Generic DB Accessor quotes in §II, they describe a platform whose personalisation promise was architecturally sound but whose implementation substrate leaked at every layer — caches, function-name collisions, component memory, DCC promotion, cross-layer call cost. Saucier's playbook explains how the BVAs end up counting 21% activation (Le Shop) and *"extensive profiling is the only personalization feature used on this site"* (Hallmark).

---

## VII. Threads

- `[[third-branch]]` §I.C — the BVA/Moon material this brief architecturally backs. The stamps-and-envelopes operator quote there is the commercial ceiling; Saucier's quotes here are the engineering ceiling underneath it.
- `[[academic-frame-1999-hbs]]` — Moon's *Create/Remember/Anticipate* and *Banner/Email/Experiential/Viral* taxonomies are the external frame BroadVision shipped the tools for.
- `[[pwc-ebiz-web-implementation-guide]]` (pending) — the methodology-template sibling of the Swindon CoE reference implementation in §III.

---

*Primary sources: `Brain/raw/.extract/BV Nuggets/BV Lessons Learned and Best Practices.doc.md` (Saucier, PwC, 12/09/1999, 18pp); `Vignette vs Broadvision.xls.md`; `Vignette compete.doc.md` (BV internal, Apr 1998). PwC Swindon T&K reference at `Brain/raw/.extract/SWINDON/` — `T&KSTORYLINE v1.01.doc.md`, `Arch.doc.md`, `rules.doc.md`, `T&K customization.doc.md`, `customer data model 12_28_99.xls.md`, `Merchandise Hierarchy.doc.md`, `Website_Functions.xls.md`, `crossells.xls.md`, `sap_prices.xls.md`, `Release Notes/Retail Commerce 4.1 NT release notes.pdf.md`. Sizing deck `Brain/raw/inbox/BV Nuggets/00-01-29 Sizing a BroadVision Site.ppt` binary present, not yet extracted.*
