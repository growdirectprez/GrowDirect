---
classification: internal-only
scope: HIDE
owner: GrowDirect / ALX memory-bus
type: founder-context
status: draft-awaiting-review
date: 2026-04-25
last-compiled: 2026-04-25
needs-review: 2026-05-09
---

# Founder Context — Secure Engagement Archive (Sysrepublic / 2017 era)

**Scope.** This article is HIDE — never externalised. It captures
the prior-engagement archive that informed the CATz Phase III
delivery framework, so ALX can answer "where did this methodology
come from?" when context is relevant. The sanitized templates
that landed in CATz live without these attributions on purpose.

## What this archive is

Eleven engagement-archive documents from the founder's
Sysrepublic / Secure-era career on an external drive
(`/Volumes/My Passport/`). They governed the deployment of the
Sysrepublic Secure Store loss-prevention platform — first as
on-premise, later as a SaaS subscription — across the
2013–2017 window. The 100-day deployment shape was tight,
recognizable, and well-rehearsed. It is the structural
ancestor of CATz Phase III.

The 2026-04-25 dispatch
(`dispatches/2026-04-25-secure-engagement-archive-deep-dive.md`)
mined the structural patterns out of these documents and
landed sanitized templates in the CATz vault. This article is
the source-of-record for what mapped where.

## Source corpus

All sources are read-only on the external drive. None were
modified during extraction.

| # | Source path | Type | Era |
|---|---|---|---|
| 1 | `Schedule D Secure Service 2-7-17 GLyle Edits.doc.docx` | Contract clause | 2017 |
| 2 | `Secure Engagement Overview - On Premise.doc` | Engagement frame | 2012–2016 (last edit 2016) |
| 3 | `Secure SaaS Order Form (Template) gcl comments 3-9-17.docx` | Contract template | 2017 |
| 4 | `SolutionRequirementsSurvey_20170328.docx` | Pre-deployment instrument | 2017 |
| 5 | `BaseLine Case Plan.pdf` | Project plan (generic) | 2017 |
| 6 | `Secure 3.5 Baseline Plan.pdf` | Project plan (versioned) | 2017 |
| 7 | `Secure 3.5 Resource Plan.pdf` | Resource model | 2017 |
| 8 | `Secure Data Flow.pdf` | Architecture diagram | ~2016–17 |
| 9 | `Taco Bell Secure 3.5 Timeline.pdf` | Engagement timeline (per-client) | 2017 |
| 10 | `Taco Bell Secure Resource Plan.pdf` | Resource allocation (per-client) | 2017 |
| 11 | `/Volumes/My Passport/CLIENTS/DELIVERY/Delivery Framework v1 2.pdf` | Delivery discipline | 2013 |

All eleven were successfully read and structurally analysed.
Source #11 (Delivery Framework v1.2 2013) is the foundational
artifact — it predates the 2017 work and codifies the
governance overlay (4 phases × 4 functions × 6 quality gates +
14 milestones) that the per-engagement plans implement.

## Source-to-output map

The dispatch's sanitized output map produced ten CATz
artifacts plus one Phase III synthesis article:

| Source | Sanitized CATz output |
|---|---|
| 1 (Schedule D) | `agreements/engagement-schedule-template.md` |
| 2 (Engagement Overview – On Premise) | `method/engagement-shapes/on-premise.md` |
| 3 (SaaS Order Form Template) | `agreements/saas-order-form-template.md` |
| 4 (Solution Requirements Survey) | `method/artifacts/solution-requirements-survey.md` |
| 5 + 6 (BaseLine Case Plan + Secure 3.5 Baseline Plan) | `method/artifacts/baseline-plan-template.md` |
| 7 + 10 (Secure 3.5 Resource Plan + Taco Bell Resource Plan) | `method/artifacts/resource-plan-template.md` |
| 8 (Secure Data Flow) | `method/artifacts/data-flow-template.md` |
| 9 (Taco Bell Secure 3.5 Timeline) | `method/artifacts/engagement-timeline-100-day-template.md` |
| 11 (Delivery Framework v1.2 2013) | `method/delivery-framework/overview.md` |
| 5–11 (synthesised) | `method/phases/phase-3-deploy-and-operate.md` |

## Founder context — why this engagement model

The Sysrepublic Secure Store engagement was a hosted /
on-premise loss-prevention analytics platform deployed at
Tier 1 retail and quick-service restaurant operators. The
2017 era ran several deployments in parallel under a tight
delivery cadence: a 100-day Phase 1 from kickoff to go-live,
followed by Phase 2 enhancement work (single sign-on, custom
integrations, scorecards). The founder operated as the
delivery-side discipline — engagement schedule editor,
project structure designer, SOW author.

The artifacts on the drive are not aspirational. They are
production-used. The baseline plan structures, resource
allocations, and gate sequences shipped against named
customers; they reflect what worked when the work was real.

That's why they're worth mining: 25-year-refined patterns
embedded in artifacts the founder wrote, used, and signed
against. The CATz Phase III templates capture the structural
shape; they do not capture (and must not capture) the named
clients, named products, or version numbers that were
specific to that era.

## Sanitization decisions — for the record

The dispatch's scrub rules were applied with zero tolerance.
Forbidden-name grep was run against every sanitized draft
before merge proposal; all produced zero hits.

A handful of edge cases were resolved as follows:

- **"hypercare"** — kept. Generic IT-delivery industry term;
  not prior-product-specific.
- **"risk dictionary"** — kept (lowercase, descriptive of an
  industry concept). Used in the on-premise shape and the
  delivery framework's document catalogue as a generic
  descriptor of a loss-prevention rule library, not as a
  Sysrepublic feature name.
- **"loss prevention"** — kept. Generic retail domain
  function used across the industry; matches CATz's existing
  wiki anchoring.
- **"secure" as adjective (lowercase, e.g., "secure
  channel")** — kept per dispatch rules. Permitted as English
  adjective; forbidden only as a product name.
- **Schedule letter ("Schedule D")** — dropped. The original
  used "Schedule D" because it was the fourth schedule in a
  particular master agreement; CATz templates do not lock to
  that letter.
- **Specific numbers (resource hours, store counts, fee
  percentages)** — abstracted to ranges or labelled
  illustrative. Per dispatch out-of-scope rule: "abstract the
  shape, not the numbers."
- **Service-desk locations (LA, Warsaw, London),
  data-centre operator (Equinix El Segundo), specific
  amendment dates (June 2006 — January 2016)** — dropped.
  These are prior-product / prior-vendor traces.
- **Press-release exhibit content** — replaced with a
  structural placeholder. The original named a specific
  vendor CEO, a specific PR firm contact, and contained a
  brand-marketing voice that does not survive sanitization.

## What's now in CATz that wasn't before

Before this dispatch, CATz had Phase I and Phase II as
populated phases and a placeholder Phase III. The CATz
`method/artifacts/` directory was empty. The
`method/engagement-shapes/`, `method/delivery-framework/`,
and `agreements/` directories did not exist.

After this dispatch:

- Phase III is a real phase with eight workstreams,
  nine milestones, six quality gates, and explicit exit
  criteria.
- A delivery framework is documented end-to-end (four
  phases × four functions × six quality gates × fourteen
  milestones × document catalogue × workshop and meeting
  catalogue).
- An on-premise engagement shape is documented end-to-end
  (six steps from kickoff through acceptance, plus reference
  data spec and customer-deliverables checklist).
- Six artifact templates (baseline plan, resource plan,
  data flow, requirements survey, 100-day timeline, plus the
  delivery framework itself) are available as cloneable
  starters.
- Two agreement templates (engagement schedule, SaaS order
  form) cover the contract surface that bounds Phase III.

The combined effect is that an engagement landing in CATz
Phase III now has the same artifact discipline that Phase I
and Phase II already had — and the engagement-shape
distinction (on-premise vs. SaaS) is visible at the method
level.

## What ALX should do with this article

When asked about the origin of CATz Phase III, the delivery
framework, or any of the templates listed in the
source-to-output map: cite this article. Do not externalise
the source corpus, the named clients in the source corpus,
or the specific version-tagged products. The founder's prior
work earns the methodology its credibility; the products and
clients in that prior work are not GrowDirect's IP and don't
appear in any externalised CATz content.

## Related

- `dispatches/2026-04-25-secure-engagement-archive-deep-dive.md`
  (the dispatch that produced these outputs)
- [[secure-retail-career-archive]] (the broader career-archive
  context already in Brain)
- [[secure-platform-overview]] (related Brain wiki article on
  the Secure platform's structural shape)
- [[secure-architecture]] (related Brain wiki article on the
  Secure platform's architecture)
