---
title: BP Consulting Library — 1997–1999
type: reference-corpus
status: v0.1
tags: [consulting, reference-library, pwc, management-horizons, sap-retail, intactix, finance, branch-b, 1997-1999, smoking-gun]
created: 2026-04-24
updated: 2026-04-24
related:
  - "[[third-branch]]"
  - "[[intactix-canonical-validation]]"
  - "[[tesco-technical-library]]"
  - "[[katz-scm-2003-archetype]]"
  - "[[pwc-ebiz-web-implementation-guide]]"
  - "[[retek-rms-perpetual-inventory]]"
  - "[[academic-frame-1999-hbs]]"
sources:
  - Brain/raw/.extract/BP/Asstmgmt.doc.md  (Cluster B — smoking gun #1 — Intactix/SAP ordering gate, Jan 1998)
  - Brain/raw/.extract/BP/980128ib.doc.md  (Cluster B — smoking gun #2 — investment-buying / MRP sidestep, Jan 1998)
  - Brain/raw/.extract/BP/mrp000.doc.md  (Cluster B — supporting SAP Retail 4.0 functional gap catalog)
  - Brain/raw/.extract/BP/mfo000.doc.md  (Cluster B — CPFR scope exclusion)
  - Brain/raw/.extract/BP/BEST PRACTICES - INTEGRATED FINANCIALS.DOC.md  (Cluster C — 70+-retailer leaderboard)
  - Brain/raw/.extract/BP/.extract-failures.json  (Cluster A — 12 .ppt files failed legacy-binary extract)
last-compiled: 2026-04-24
needs-review: 2026-05-08
---

# BP Consulting Library — 1997–1999

**Governing thesis.** The `BP/` folder is a three-cluster consulting reference corpus from the late-1990s Big Five retail practice that triangulates Branch B of the [[third-branch]] thesis in a way Branch B on its own cannot. Cluster A is the generic PwC / Management Horizons retail best-practices deck library (1997–1998) — the *operating-model grammar* the consultants brought to every retail engagement. Cluster B is a January 1998 SAP Retail 4.0 implementation blueprint for a US specialty retailer — *the grammar meeting a real ERP*, and the point at which two primary-source smoking guns were quietly written into the deliverable pack. Cluster C is a 1999 Finance best-practices pack customized onto a financial-exchange-integration engagement — *the same firm applying the same template pattern outside retail*, with the same deliverable shape. Across all three clusters one pattern holds: **the questions were right, the substrate was not, and the answer was always discrete labor priced in the low millions.** That is exactly the indictment Branch B of the Third Branch thesis makes, now carrying primary-source evidence.

Folder name is a historical artifact; `BP/` is NOT Pitney Bowes internal content. It is a founder-accumulated reference library spanning three distinct engagement contexts.

## Three-cluster MECE structure

| Cluster | Corpus | Dated | Engagement context | Evidence role |
|---|---|---|---|---|
| **A** | 12 PwC / Management Horizons retail best-practices decks | 1997–1998 | Generic industry-wide templates | Vocabulary grammar: the numbered process flows, the vendor-partnership ladder, the GM-vs-F&D split |
| **B** | 16 SAP Retail 4.0 module specs + 5 workshop notes | January 1998 | A US specialty retailer SAP Retail 4.0 implementation | Two primary-source smoking guns: Intactix/planogram gating issue (1998) and ERP-sidestep statement (1998) |
| **C** | 13 Finance best-practices memos | Jun–Dec 1999 | Financial-exchange-integration engagement (three-scenario: Current / Cooperative Agreements / Integrate All Exchanges) | Same template pattern, applied to finance; 70+-retailer practice list |

Management Horizons was acquired by Price Waterhouse in 1992 and folded into PwC Consulting in 1998. The Cluster A decks are the direct lineage of that merger; Cluster B is the same firm in implementation posture; Cluster C is the same firm outside retail.

## I. Cluster A — The PwC/MH retail template vocabulary

The twelve decks cover, by file name: Return-to-Vendor (`RTV.ppt`), Vendor Management (`Vendor Mgmt.ppt`), Invoice Verification (`Invoice Verif.ppt`), Inventory Control (`Inventry Cntrl.ppt`), Import Management (`Import Mgmt.ppt`), Performance Monitoring (`Perf Mont.ppt`), Sales Audit (`Sales Audit.ppt`), Space Management (`Spc Mgmt.ppt`), Forward Buy (`Forwrd Buy.ppt`), Category Management (`Cat Mgmt.ppt`), Efficient Assortment (`Efficnt Asst.ppt`), Event Management (`Event Mgmt.ppt`).

The file-name taxonomy *is* the evidence. This is the complete operating-model grammar of late-1990s retail consulting: ten supply-chain process areas (RTV, Vendor, Invoice, Inventory, Import, Forward Buy, Sales Audit), two merchandising/space process areas (Space, Category), and two execution process areas (Efficient Assortment, Event). Each deck is a numbered process flow (10.1 – 10.5 convention) with the same standardized structure: objectives, critical success factors, assumptions, performance measures, issues, better-practices recommendations.

Crucially, this same vocabulary reappears verbatim in Cluster B — the module specs in Cluster B have "Better Practices Recommendations" as a named section header, directly lifting the deck-pack grammar into the implementation template. When we find the [[katz-scm-2003-archetype]] engagement applying these exact process names in 2003, and when [[pwc-ebiz-web-implementation-guide]] applies them to eBusiness in 2000, Cluster A is the source artifact being reused.

*(Note on extraction: the twelve .ppt files are legacy pre-OOXML PowerPoint and failed markitdown conversion — see `/Users/gclyle/GrowDirect/Brain/raw/.extract/BP/.extract-failures.json`. The taxonomy stands on file-name evidence and reappearance downstream. Full content rescue would require alternative PPT tooling.)*

## II. Cluster B — The 1998 SAP Retail 4.0 blueprint

**Engagement shape.** A US specialty retailer, SAP Retail 4.0, Intactix named as the space-management integration partner, three-day workshop series January 28–30, 1998. Sixteen M-prefix module specs covering Assortment Management (`Asstmgmt.doc`), Vendor Management (`Vm000.doc`), Purchase Order Management (`mpo000.DOC`), MRP/Replenishment (`mrp000.doc`), Forecasting (`mfo000.doc`), Physical Inventory (`Mpi000.doc`), Stock Management (`msm000.doc`), Manual Transfers (via `980130xf.doc`), Allocation (via `980130am.doc`), plus event management, discontinuation, pricing, and warehousing modules. Format signature per spec: *Objectives / Critical Success Factors / Assumptions / Requirements / Resolutions / Performance Measures / Issues / Better Practices Recommendations / Existing SAP Functionality / Jobs Analysis / Reports / Forms / Test Month Follow Up*. Every spec follows the template. The template is Cluster A's.

### Smoking gun #1 — The Intactix / planogram-gating issue

From `Asstmgmt.doc` (Assortment Management), §I.E "Issues":

> *"There is an issue with regards to the integration of a space management system (i.e. Intactix) with the assortment and listing functions in SAP. The objective is to control listing (and thus replenishment) for all SKU's in the stores through the use of planograms."*

And from §VIII.B "Define Prototype / Maintain Planograms":

> *"SAP must allow for the interface of the 'Listing Process' with an external space management system (i.e. Intactix). The objective is to control listing (and thus replenishment) for all SKU's in the stores through the use of planograms. The system would have to allow for input/update of the following data from the space management system: Planogram Name/Number (alpha numeric), Article (SKU) #, Site #, Presentation Quantity…"*

This is the **ordering-gate architecture** — location-level planogram assignment controlling item activation for replenishment — *documented as an open integration issue in January 1998*, eight years before the same architecture with the same named vendor (Intactix) was actually built at Fresh & Easy / Tesco. The Asstmgmt.doc assumption list even names it explicitly: *"New Store listing will result from planogram assignment."* See [[intactix-canonical-validation]] for the direct eight-year-later lineage, and [[tesco-technical-library]] for the closed loop on the specification side.

### Smoking gun #2 — The MRP / investment-buying ERP-sidestep

From `980128ib.doc` (Investment Buying workshop note, January 28, 1998), §P "Test Month Follow Up", under *Purchase Orders → Implementation Considerations*:

> *"Articulate exactly how promotional planning / purchases will be handled (included within or in addition to regular purchase quantities). Currently investment buying and MRP calculations will be completely separate processes (and SAP will choose the larger of the two values) but promotional purchases will be considered additions to the selected value."*

And from the cross-functional links:

> *"Use store replenishment forecast for investment buying (SAP currently uses the MRP forecast only)."*

This is **Branch A (ERP-sidestep) written down by the team installing the ERP.** Investment buying — a core retail buyer function tied to promotional windows, deal timing, and forward cost — was already being architected *around* SAP's MRP, because SAP's MRP could not carry retail's forecast logic. This is the founder-experience observation of ERP insufficiency (see [[third-branch]] §I.A "ERP — ledger substrate") captured *in real time* as a consulting deliverable. In 1998. The retail-logic-has-to-live-outside pattern was not discovered in 2006 at Fresh & Easy; it was documented, acknowledged, deferred.

### Supporting module evidence

**Replenishment / MRP gaps (`mrp000.doc`).** Test-month findings catalog eleven separate functional gaps:

> *"Safety stock is not calculated — It is only a manually entered value. Safety stock needs to be dynamically calculated based on dynamic vendor lead times, demand variability and targeted service levels."*
>
> *"DC replenishment is currently based upon DC consumption — not a sum of forecasted demand for the stores supplied by the DC. There is no provision for irregular demand."*
>
> *"Vendor lead times are not dynamic measurements — and are currently only manually entered."*
>
> *"Store replenishment was simplified in 4.0 and lost this capability."*
>
> *"Stock outs and lost sales (unfulfilled demand) are not calculated and included in SAP's forecasting and/or replenishment processes."*

SAP Retail 4.0, shipped as the flagship retail ERP of its era, could not calculate safety stock dynamically, could not aggregate store forecasts into DC demand, could not track dynamic vendor lead times, and lost functionality between releases. The retail operating model was being written into documents because it could not be written into the software.

**Forecasting module (`mfo000.doc`).** Explicit scope exclusion: *"Collaborative Forecasting and Vendor Managed Inventory are not part of this process during its initial stages."* CPFR was the named industry frontier by 1998 (the VICS CPFR committee published its first guidelines in that same year); the blueprint deferred it.

**Allocation (`980130am.doc`).** Under "Better Practices Recommendations": *"Schedule distributions for new and existing stores based on plan-o-gram and reserve store opening inventory shipments up to a specified number of weeks in advance."* — again, planogram-as-gating-object, reinforcing the Asstmgmt.doc architectural claim.

## III. Cluster C — The 1999 Finance best-practices pack

Thirteen memos dated June–December 1999 covering: AP (`best practices - AP combined.doc`), AR (`BEST PRACTICES - AR COMBINED.DOC`), General Accounting, Treasury, Shared Services, Planning, Reporting, Payroll, Outsourcing, Staffing, Performance Indicators, EDI Technology, and the capstone `BEST PRACTICES - INTEGRATED FINANCIALS.DOC`.

**Three-scenario framing.** Every memo carries the same header checkbox:

```
 FORMCHECKBOX   Current Structure
 FORMCHECKBOX   Current Structure with Cooperative Agreements
 FORMCHECKBOX   Integrate All Exchanges
 FORMCHECKBOX   Other, Please Specify: ____
```

The engagement is structured as a three-scenario integration study for a federation of financial exchanges. Each best-practice memo names the organizational option supported, the functional area impacted, the best-practice option narrative, and a list of comparator organizations.

**The 70+-retailer artifact.** `BEST PRACTICES - INTEGRATED FINANCIALS.DOC` carries a preservable list of "retailers with integrated financial systems" as of late 1999: Federated, Book-of-the-Month-Club, CBS, Mervyn's, Abercrombie & Fitch, Amazon.com, American Stores, Barnes & Noble, Bombay Company, Boston Chicken, Borders, Brooks Brothers, Carrefour, Circle K, Circuit City, Coles Myer, CVS, Delaware North, Dominos, Eckerd, Edison Brothers, Fila USA, Fingerhut, Gap, Gateway 2000, Giant, Hechinger, Hit or Miss, Home Depot, Ikea NA, J.C. Penney, Kmart, Kmart Canada, Kohl's, Long John Silver's, Lowe's, National Grocers, Navy Exchange, Neiman Marcus, Papa John's, Payless, Pier 1, Pizza Hut, Public Storage, Raley's, Ralphs, Rite Aid, Ross, Ruby Tuesday, Safeway, Schoeneckers, Scottish & Newcastle Retail, Scotty's, Sears, Spencer Gifts, Staples, Stop & Shop, Sunglass Hut, Taco Bell, Talbots, Tandy, The North West Company, Toys 'R' Us, Victoria's Secret Catalogue, Walmart, Wendy's, Winn-Dixie, Woolworth — plus Reynolds Aluminum, Puma Technology, Motorola, Mercedes-Benz, Fujitsu Network. The list is a cross-section of the US retail and services economy in 1999, indexed by who had "state of the art" financial-systems integration — a 1999 leaderboard.

**What the pack shows.** The same deliverable shape as Cluster A and Cluster B: every memo runs Policy Guidelines / Integration with Other Systems / Streamlining / Benchmarks / Comparator Examples. The Treasury memo quotes hard benchmarks (*"Bank accounts per FTE treasury employee: 227. Trades per FTE: 2,150. Foreign Exchange trades per FTE: 6,000. Collected balance per billion dollar revenue: $190,600"*). The Shared Services memo ships a full taxonomy of what belongs in a shared service center and what distinguishes it from corporate centralization.

The pack is competent, serious, and completely consistent with the Cluster A retail template. Different domain, same method, same deliverable format. The consulting firm applied its grammar to whatever industry requested it.

## IV. Cross-cluster patterns

Four patterns hold across all three clusters, and each is evidence for Branch B of the [[third-branch]] thesis:

1. **Vocabulary standardization.** The "Better Practices Recommendations" section header, the Objectives/CSF/Assumptions/Issues structure, the numbered process-flow decomposition, and the three-tier Level 1 / Level 2 / Level 3 process hierarchy appear identically in Cluster A decks, Cluster B module specs, and Cluster C finance memos. The firm shipped one template.
2. **Architectural flags correctly identified, not resolved.** Cluster B documented the Intactix/planogram-gating requirement and the MRP/investment-buying sidestep in 1998. Both survived unresolved for 8–28 years. The consultants saw the problem. The engagement shape could not solve it.
3. **Deliverable is always a document pack.** Every cluster ships as discrete written artifacts — decks in Cluster A, module specs + workshop notes in Cluster B, memos in Cluster C. Continuous observation, live instrumentation, or ongoing telemetry is not the unit of delivery. The unit of delivery is a document, handed over, and the engagement ends.
4. **Continuous instrumentation is not part of the grammar.** Not in Cluster A (decks describe target-state processes as static state diagrams), not in Cluster B (the Replenishment module explicitly lists "no simulation capabilities" as a gap with no proposed path to continuous simulation), not in Cluster C (the integrated-financials pack benchmarks point-in-time metrics, not live feeds).

Branch B's claim — *the questions were right, the substrate could not carry the weight, the answer was discrete labor* — is primary-source supported by `BP/`. The consultants of 1998–1999 knew what needed to be answered. Their deliverable shape could not answer it continuously. That is the opening the third branch resubstrates on the 2026 stack.

## Threads

- [[third-branch]] §I.B (Branch B, Strategy consulting) — this article is the primary-source backing for the Branch B indictment. Both Cluster B smoking-gun quotes belong cited inline in the thesis.
- [[intactix-canonical-validation]] — `Asstmgmt.doc` names Intactix in the planogram/SAP integration role eight years before F&E/Tesco built the same architecture. Direct lineage.
- [[tesco-technical-library]] — the TTL compile gate is one half of what eventually closed the Asstmgmt.doc Issue (specification side); the SRD planogram canonical closed the other half (location/listing side).
- [[katz-scm-2003-archetype]] *(pending)* — same vocabulary, 2003 engagement, same firm. Cluster A grammar reappearing in retail SCM consulting five years later.
- [[pwc-ebiz-web-implementation-guide]] — sibling methodology template extending the same grammar to eBusiness implementation circa 2000.
- [[retek-rms-perpetual-inventory]] *(pending)* — the `980128ib.doc` MRP smoking gun is the ledger-substrate-insufficiency statement that belongs at the head of the Retek/Oracle Retail discussion.
- [[academic-frame-1999-hbs]] — the 1999 Moon HBS note is the Branch C academic frame; the Cluster C 1999 Finance pack is the Branch B deliverable shape from the same year. Same era, different branches, same substrate ceiling.
