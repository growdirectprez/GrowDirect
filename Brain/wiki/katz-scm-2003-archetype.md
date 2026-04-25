---
title: Mid-Market Drug/Pharmacy SCM Engagement, 2003 — Branch B Archetype
type: archetype
status: v0.1
tags: [retail, scm, consulting, rfp, ibm-bcs, pwc, branch-b, archetype, 2003, drug-pharmacy, retek, sap, jda, jde, i2, gartner]
created: 2026-04-24
updated: 2026-04-24
related:
  - "[[third-branch]]"
  - "[[retek-rms-perpetual-inventory]]"
  - "[[intactix-canonical-validation]]"
  - "[[bp-consulting-library-1997-1999]]"
  - "[[pwc-ebiz-web-implementation-guide]]"
sources:
  - Brain/raw/.extract/Katz/  (140 intakes, Phase I + Phase II, 2003)
  - Brain/raw/inbox/kroger-retek-project-sam-xls.md  (sibling Retek deployment)
last-compiled: 2026-04-24
needs-review: 2026-05-08
---

# Mid-Market Drug/Pharmacy SCM Engagement, 2003 — Branch B Archetype

**Governing thesis.** A 2003 North American mid-market drug/pharmacy retail holding company commissioned an IBM Business Consulting Services (ex-PwC) team to run a full-funnel supply-chain diagnosis and system selection across five vendors. The engagement produced ~140 working papers — executive interviews, store visits, as-is / to-be workshops, a balanced scorecard, an RFP, vendor responses, Gartner memos, a benefits case, and an NPV model — and recommended a merchandising/SCM platform purchase. It did **not** produce working technology. This is the canonical [[third-branch|Branch B]] artifact: the questions were correct, the process was rigorous, the deliverables were decks and spreadsheets, and the answer shipped was "buy a package and hire more people," not continuous instrumentation. The raw corpus lives at `Brain/raw/.extract/Katz/`.

---

## I. Engagement shape (the archetype)

Codename: Project Casper. Two phases, roughly April–December 2003. Selection project consultant: IBM BCS, Mississauga. Client team: President, CFO, CIO, VP Ops, VP Merch, Chief Merch, VP HR, VP Private Label, plus operating-banner GMs. Structure visible from `Brain/raw/.extract/Katz/Project Casper Documentation Index.doc.md`:

| Phase | Window | Artifact families |
|---|---|---|
| **I — SCOA** (Supply Chain Opportunity Assessment) | Apr–Jun 2003 | 11 structured executive interviews (14-question guide); 20+ store visits across 5 banners; 8 as-is process workshops (Category Mgmt, Forecasting, Inventory, Pricing, Vendor, Move, POS, ProPharm); executive visioning session with McKesson precedent deck; benchmarking vs. NA drug chains (IHL, Walgreens); balanced scorecards; inventory analysis (turns by vendor, turns by vendor×category, discontinued-by-store, service levels); benefits case v2 + Retail Systems Cost Model v5 + NPV Model v2 + Solution Contribution to Value Opportunities v3; SCOA Final Report + Appendix; Change Readiness Assessment. |
| **II — Design & Selection** | Jul–Dec 2003 | Quick Wins Final Report v2; Future Visions Options v7 (supply chain design); 7 to-be process workshops; Requirements v4 (the evaluation grid); **RFP issued to five vendors**; full responses from all five; Gartner memos (JDA vendor rating, Retek vendor rating, SAP Top-10); reference calls (CVS, H-E-B, Forzani, Sobeys, Tractor Supply, Boots); scripted demo days + scorecard; Current Assessment & Opportunities v3.4 (IT architecture); Change Management, Roles & Responsibilities, Org Design, Training Strategy, Comm Plan; Revised NPV Model v2. |

The engagement is a reference implementation of the classic Big-5 "diagnose → design → select → prepare" template applied to a mid-market retailer with ~250 stores across multiple banners.

---

## II. Operating-model questions the methodology asked

Stripped from the 14-question executive interview guide, the as-is workshop set, and Requirements v4. The consultants asked the right questions:

| Category | Representative asks |
|---|---|
| Executive KPIs | GMROI by category; inventory turns (overall and front-shop); service level; in-stock % — and whether the numbers are even available |
| Inventory position | Turns by vendor; turns by vendor × category; discontinued SKUs by store; out-of-stocks; stock accuracy vs. book |
| Service level | Current service level, best-in-class service level (reference 96.5% in the benefits case); McKesson fill rate |
| Vendor / supplier mgmt | Sourcing, negotiation, content mgmt; supplier scoring; supply-agreement structure |
| Category management | Line drawings tailored to store clusters; discontinued-by-store discipline; private-label penetration; planogram compliance |
| Pricing | Matrix pricing granularity; price-change approval levels; markdown governance; competitive-proximity pricing rules |
| Forecasting / replenishment | Automated vs. manual replenishment; model sophistication; exception handling; central-fill economics |
| POS / stock ledger | POS-to-inventory reconciliation; perpetual inventory; sales audit integration |
| Org readiness | Change-readiness assessment; store skillset gap; governance; executive sponsorship; communication plan |

These are the same questions a CTO would ask today of an instrumentation platform. The 2003 engagement asked them in full, captured the answers in Excel, and then handed the answers to five package vendors.

---

## III. Vendor landscape, circa 2003

From `short-listed-vendors-doc.md` (the one-page comparator) and the RFP evaluation scorecards:

|  | **JDA** | **SAP** | **Retek** |
|---|---|---|---|
| Positioning | Best-of-breed retail suite; 80% retail focus | ERP incumbent pushing mySAP retail; emerging retail focus | Retail-pure-play, 100% retail focus |
| 2002 revenue / EBITDA | $219M / $2M | $7.77B / $2.26B | $192M / -$61M |
| Canadian clients | 70 (floor planning); 10 (merch planning) | 6 | 12 |
| Integration posture | Limited — acquired best-of-breed pieces | Fully integrated incl. financials | Good integration, no financials |
| Functionality score | 86.0 | 95.7 | 89.7 |
| Overall RFP score | 68.2 | 78.5 | 70.1 |
| Weighted demo score | 77% | 84% | (not demoed — eliminated earlier) |

i2 and JD Edwards responded but were cut before demo. Retek — despite fielding the [[retek-rms-perpetual-inventory|perpetual-inventory substrate]] (RMS) and naming Eckerd, Longs, and Walgreens as drug-chain references — was outscored and outsold by SAP on integration and by JDA on retail depth. Gartner's memos (`gartner-s-view-on-jda-and-sap-v2-doc.md`, dated Sep–Oct 2003) positioned JDA as *"a patchwork of different technologies"* whose strength was stand-alone best-of-breed; SAP as *"not yet ready to cover all functional domains"* but with a 0.7-probability forecast of dominance by 2006. Retek's letter of transmittal (`katzse24-letter-of-transmittal-doc.md`) pitched *"the art of retail with the science of Retek"* and proposed a license-plus-subscription model spanning corporate stores and independent affiliates.

---

## IV. What got delivered vs. what got built

**Delivered (the artifacts):** 11 interview analyses, 20+ store-visit spreadsheets, 8 as-is workshop decks, 7 to-be workshop decks, balanced scorecards, benefits case v2, NPV model v2, cost model v5, SCOA final report, Future Visions Options v7, Requirements v4, 5 RFP documents, 5 vendor response packs, Gartner memos, demo scripts and scorecards, Current Assessment & Opportunities v3.4, Change Readiness Assessment, Org Design v6, Training Strategy v3, Communication Plan v4, Revised NPV Model v2. Every one of these is a document.

**Built:** nothing. No instrumentation, no stock-ledger reconciliation, no perpetual-inventory feed, no real-time service-level signal. The engagement ends at *"prepare for implementation"* (Phase II section 06 is one file, `Revised NPV Model v2.xls`).

The gap is load-bearing. The benefits case monetizes lost sales at **CDN$11.6M/year** from the 90% → 93.75% service-level gap, but the delivery mechanism is a two-year package implementation followed by manual process change — discrete consulting labor producing a recommendation, not continuous measurement. This is the Branch B shape exactly: right questions, right diagnosis, 2003-era answer.

---

## V. Primary-source quotations

**1. The VP Ops names perpetual inventory as the #1 unmet need — in a facilitated executive session, on the record.**

> "Grant / Perpetual inventory / Multiple banners and buy in" — answer to "Based on what you have heard today, what is the single most important thing you would like to change to service customers?"

Source: `Brain/raw/.extract/Katz/Phase I/04 - Executive Visioning/Katz Group Executive Visioning Session.doc.md` (June 12, 2003 minutes).

**2. The change-readiness consultant sets perpetual-inventory enablers as a 2005 milestone — framed as a dependency, not a capability.**

> "Enablers need to be put in place by 2005 to have the ability to replace McKesson (milestone)"

Source: same file, change-management section.

**3. Gartner confirms the integration gap the engagement is trying to close — and confirms the answer is years of vendor promise.**

> "After difficulties with earlier versions of its merchandising management solution, SAP is now developing a robust, integrated retail solution. But, it is not yet ready to cover all functional domains, countries or retail sub-segments… SAP will be the most prevalent software vendor for worldwide retail applications by 2006 (0.7 probability)."

Source: `Brain/raw/.extract/Katz/Phase II/03 - System Selection & Supply Chain Optimization/08. Gartner Information/Gartner's View on JDA and SAP v2.doc.md` (Sep 23, 2003).

The retailer named the gap. The consultants documented it. The answer on offer was a multi-year package implementation dependent on vendor roadmap delivery.

---

## VI. Threads to other Brain artifacts

- **[[third-branch]]** — this engagement is the load-bearing Branch B case. The 18 PwC/IBM client decks already catalogued are the supporting corpus; this engagement is the one where the full working-papers trail survives end-to-end.
- **[[retek-rms-perpetual-inventory]]** — Retek placed but did not win. The Retek response, demo materials, and Gartner vendor rating feed the perpetual-inventory wiki directly; Retek's *"art of retail, science of Retek"* pitch is the 2003 perpetual-inventory vendor voice.
- **[[intactix-canonical-validation]]** — JDA's Intactix space-planning module was explicitly praised in the demo roundtable (*"Like Intactix and forecasting tools"*). The JDA *"patchwork of different technologies"* Gartner critique is the external-validation counterpart to Intactix's canonical story.
- **[[bp-consulting-library-1997-1999]]** — same Big-5 grammar, five years earlier, applied in SAP Retail 4.0 implementation posture. Branch B's template continuity is visible across both artifacts.
- **[[pwc-ebiz-web-implementation-guide]]** — same firm's 2000 methodology template for eBiz implementations; the shape of the deliverables in this 2003 engagement is the direct descendant.
- `Brain/raw/inbox/kroger-retek-project-sam-xls.md` — Kroger Retek deployment, sibling perpetual-inventory reference.

---

*Primary sources: `/Users/gclyle/GrowDirect/Brain/raw/.extract/Katz/` — 140 intake notes across Phase I (SCOA) and Phase II (Design & Selection), extracted via the content engine on 2026-04-24. Client named in raw intakes; abstracted to archetype in this synthesis per the brain's scrub-client-names convention.*
