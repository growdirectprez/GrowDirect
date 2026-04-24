---
type: wiki-article
status: active
tags: [methodology, consulting, ibm-bcs, it-architecture, preserved-ip]
source: Morrisons.IT Architecture.Final Deliverable.v1.0 (IBM Business Consulting Services, 2006)
provenance: "Analyst-authored consulting deliverable, preserved for methodology study. Not a client engagement artifact; structural reference only."
skill: .claude/skills/consulting/it-architecture-options/SKILL.md
author: Geoffrey C. Lyle (custodian)
date: 2026-04-24
last-compiled: 2026-04-24
needs-review: 2026-05-08
---

# Methodology · IBM IT Architecture Options (Morrisons pattern)

The structural pattern IBM Business Consulting Services used in 2006 to deliver
the Morrisons IT Architecture review — business targets → requirements → legacy
implications → three parallel option evaluations → side-by-side summary. This
article preserves the method for reuse by the
`consulting:it-architecture-options` skill. Companion wiki:
[[Brain/wiki/methodology-ibm-retail-diagnostic|Methodology · IBM Retail Diagnostic]].

## Why it matters

The Morrisons deck is 104 pages, but every option section uses the same
seven-slide skeleton, and the front of the deck establishes one Sell/Plan/Move/Buy
process frame that all three options share. Once you see the frame, an
"evaluate legacy vs. package vs. integrated" decision for any retailer slots
into this shape. The method stays useful even if the technology names (Retek,
PeopleSoft, Oracle, SAP) are now history; the frame isn't about product names,
it's about how to force a fair comparison.

## The eight-section frame

1. **Introduction** (pp.1–10) — engagement purpose, team, document structure,
   glossary.
2. **"Optimisation" Programme — Business Targets** (pp.11–12) — the client's
   own business targets, quoted: margin up X%, overheads down £Y, headcount
   down £Z, sales up W%, profits up £V by year YYYY. **This is the sizing
   anchor for every option.** Every option's value gets compared to these
   numbers.
3. **Business Requirements — Sell / Plan / Move / Buy frame** (pp.13–28) —
   process taxonomy used throughout the deck. Twelve process areas grouped
   four ways:

   | Frame | Process areas |
   |---|---|
   | **Sell** | Sell Products · Serve Customers · Manage Branch |
   | **Plan** | Range Planning · Promotions Planning · Category Planning · Product Pricing |
   | **Move** | Supply Chain Planning · Manage Replenishment · Physical Logistics |
   | **Buy** | Product Sourcing & Buying |

   (Plus a second layer: Reporting · Control · Processing for Finance/HR.)

4. **Implications for Legacy Systems** (pp.29–39) — heat-mapped application
   architecture using a 4-color legend:
   - Green = Very good functional support — limited changes
   - Yellow = Good functional support — large number of small changes
   - Amber = Good functional support — significant changes
   - Red = Poor or no functional support — major changes or re-write / replace

   Two views of the same heat-map: one arranged by org structure (Shop
   Systems / Distribution / Retail Ops / Trading / Finance & Personnel /
   Reporting / IT), one arranged by Sell/Plan/Move/Buy process.

5. **Option A — Legacy Enhancement** (pp.40–57) — seven-slide skeleton below.
6. **Option B — Best-of-Breed Package** (pp.58–68) — same skeleton.
7. **Option C — Integrated Package (e.g. SAP or Retek)** (pp.69–83) — same
   skeleton.
8. **Summary and Conclusion** (pp.84–90) — side-by-side architecture
   diagrams (all three options rendered on one page), implementation-options
   comparison, advantages/disadvantages comparison, recommendation.

## The per-option seven-slide skeleton

Every option (A/B/C) is rendered using the exact same seven slides. This is
what makes the comparison fair, and this is what the skill enforces.

1. **Option title + one-liner** — e.g. "Legacy Enhancement Option — build on
   existing assets, bespoke development, mainframe-first."
2. **Application architecture vs. Optimisation requirements** (heat-map, org-
   structure view). How well does *this option's* future-state architecture
   support the immediate "Optimisation" programme targets? Same 4-color legend
   as Section 4.
3. **Application architecture vs. Optimisation requirements** (heat-map, process
   view — Sell / Plan / Move / Buy). Same data, different axis.
4. **Development effort estimate** — table in man-days / man-years:

   | Application Area | Design | Build/Test | Dev Total | Roll-out | Total |
   |---|---|---|---|---|---|
   | Promotion Planning (Excel) | 30 | 50 | 80 | 25 | 105 |
   | Order Pad on HHT | 400 | 500 | 900 | 800\* | 1,700 |
   | … | … | … | … | … | … |
   | **Total Man Days** | **7,455** | **13,725** | **21,180** | **3,815** | **24,995** |
   | **Total Man Years** | | | | | **111** |

   (\* = includes store training across N stores.) Footnote must state
   estimation basis — e.g. "Derived from interviews with WM IT development
   team leads; EPOS excluded assuming 2 releases/year; no contingency included."

5. **Application architecture vs. "Aspirational" requirements** (heat-map,
   org-structure view). Same heat-map as slide 2, but now evaluated against
   future-state ambitions, not just the current programme.
6. **Application architecture vs. "Aspirational" requirements** (heat-map,
   process view). Same heat-map as slide 3, same shift to future-state.
7. **Advantages / Disadvantages + Target architecture diagram** — left column
   Advantages, right column Disadvantages. Beneath: target-state application
   architecture diagram labelled with which boxes are Legacy-enhanced, which
   are Re-Written, which are Packaged, which are Out-of-scope.

## The side-by-side summary (Section 8)

This is the deck's money section. Three pages:

**Page 1 — Architecture comparison.**
A single slide with three target architectures rendered adjacent —
"Integrated Package / Best of Breed / Enhanced Legacy" — using consistent
Sell/Plan/Move/Buy row structure so the eye can compare box-for-box.

**Page 2 — Implementation comparison.**
Three columns, one per option, each with bullet list covering:

- Implementation timescale (e.g. "under 4 years" vs. "6 years")
- Risk of overrun
- External resource dependency
- Technology lock-in
- Phasing / modularity
- Time to first benefits

**Page 3 — Recommendation.**
Single recommendation with reasoning, explicitly mapped back to the Section 2
business targets. The recommendation names:

- Chosen option
- Phasing sequence (which modules first)
- Major decision gates (where the client can still re-evaluate)
- Resource commitment (internal + external)
- First-90-day actions

## What makes this methodology durable

Four properties, in order:

1. **The frame predates the options.** Section 3 (Sell/Plan/Move/Buy) and
   Section 4 (legacy heat-map) are authored *once*. Every option is
   evaluated against that frame — same process taxonomy, same heat-map
   legend, same estimation schema. The client cannot be sold a story
   where one option is evaluated on criteria another isn't.
2. **Two-axis heat-maps.** Every option's architecture is rendered twice —
   once by org structure, once by process taxonomy — so different reader
   audiences (IT leadership vs. business leadership) each get the view
   that makes sense to them without the analyst repeating work.
3. **Dual time-horizons.** Every option is evaluated against *both*
   Optimisation requirements (the programme now running) *and* Aspirational
   requirements (where the business wants to be). This prevents a
   "cheap-now, dead-end-later" option from winning on cost alone.
4. **Side-by-side is the only judgment.** The recommendation slide is
   literally the only place IBM renders an opinion. Everything prior is
   structured, symmetric, defensible frame. The client is given the
   analytical scaffolding and then told, on one page, which leg of it
   to pick.

## How the skill applies it

The `consulting:it-architecture-options` skill plugs into:

- **Client systems inventory ingest.** CSV / JSON of the retailer's
  application landscape: app name, function, technology, age, vendor,
  integration pattern.
- **Process-taxonomy loader.** The Sell/Plan/Move/Buy frame is the
  default; the skill allows the analyst to swap in a different frame
  (e.g. an IBM Component Business Model overlay) if the engagement calls
  for it.
- **Heat-map generator.** Given the systems inventory and a target
  requirement set (Optimisation or Aspirational), produce the 4-color
  heat-map. Both org-structure and process views auto-generated from
  the same source data.
- **Option scaffolder.** For each named option (Legacy / BoB / Integrated,
  or user-specified), instantiate the seven-slide skeleton populated
  with the heat-maps and an effort-estimate template ready for the
  analyst to fill.
- **Side-by-side renderer.** The summary section auto-builds from the
  three option scaffolds — architectures aligned by Sell/Plan/Move/Buy
  row, implementation bullets driven by the slide-7 advantages/
  disadvantages fields.
- **pptx output** matching IBM BCS deck structure.

The methodology's discipline — same frame, two axes, dual time-horizons,
side-by-side judgment — is the skill's system prompt. The client's landscape
is the input. The skill enforces the comparison.

## Source provenance

**File:** Morrisons.IT Architecture.Final Deliverable.v1.0.ppt (converted
to 104-page .pdf)
**Author of record:** IBM Business Consulting Services, 2006
**Custodian:** Geoffrey C. Lyle (archive; IBM BCS era)
**Use:** Methodology reference only. Client data and specific vendor
recommendations redacted from this wiki article; structural frame and
heat-map legend preserved. Full-text extract stays in a working directory
and is not committed to the public repo. All specific numbers in this
article (e.g. 24,995 man-days, 111 man-years) are direct quotes from a
public 2006 IBM deliverable and serve only as illustration of the
estimation pattern.

## Related

- [[Brain/wiki/methodology-ibm-retail-diagnostic|Methodology · IBM Retail Diagnostic]]
- [[docs/sdds/consulting/SDD-consulting-skills|SDD · Consulting Skills]]
- [[Brain/projects/Method|Method MOC]]
- [[Brain/projects/Secure|Secure]]
- [[Brain/wiki/secure-retail-career-archive|Secure — retail career archive]]
