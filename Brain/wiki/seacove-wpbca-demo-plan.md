---
date: 2026-04-19
type: wiki
status: published
tags: [seacove, wpbca, cove, arc, demo, delivery-plan, consultant-posture]
sources: [Brain/raw/processed/council/2026-04-19-seacove-wpbca-demo-delivery.md, docs/team/Condor.md]
last-compiled: 2026-04-19
needs-review: 2026-07-19
---

# Seacove → WPBCA Demo Delivery Plan

The plan for turning 25 Seacove's accumulated permit assets and the built `rpv-permit-architect` plugin into a community demo Jeffe (WPBCA ARC chairman) delivers as a neighbor-consultant. Captures the methodology so it can be re-run on the next member's remodel.

## Positioning

- **Neighbor-consultant**, not vendor
- Jeffe ran the process on his own house; he is showing the community what came out the other side and offering to run the next member through the same pipeline
- **No SaaS**, no subscription, no pitch
- Scope: one worked example (25 Seacove), one community handoff

## Assets on hand

- Blueprints: 1958 original set (plot, foundation, floor, elevations, HVAC), 1960 bedroom addition, garage addition, 2020 Phase 3, A1/A2, 2015 site survey
- SketchUp pipeline: ARC CLI, Ruby generator, LayOut templates, existing as-built model fragments
- Permit history spanning 65+ years
- Site survey PDF
- RPV public planning process (forms, checklists, fees, codes)
- [`rpv-permit-architect` plugin](https://github.com/…): six skills covering codes, sheets, archives, cost bands, SketchUp guidance, project history

## Pipeline

```
Assets → Intake → Twin → Validate → Submittal → Demo
```

1. **Intake** — drop everything into `projects/25-seacove/`. PDFs, site geojson, dated photos, permit history as YAML.
2. **Extract** — `arc extract` runs vision over scanned plans, pulls dimensions, classifies sheets, captures annotations. Confidence scores; low-confidence items flagged for manual correction.
3. **Twin** — reconcile into `spatial-model.json` with history layers: 1958 → 1960 → 2020 → 2026 proposed. Uses `archive-navigator` and `project-history` skills.
4. **Process encoding** — RPV public process becomes a checklist skill; WPBCA CCR becomes a draft manifest. Uses `rpv-building-codes` and `drawing-set-planner` skills.
5. **Validate** — run the twin against RPV checklist and WPBCA draft manifest. Output: Readiness Report naming satisfied items, gaps, and exact locations.
6. **Produce** — `arc generate` runs Ruby/LayOut pipeline. Cost-estimating skill produces a budget band. Package: site plan, elevations, narrative, material board, Readiness Report.
7. **Demo** — live walkthrough to the community, working from raw inputs to the final submittal-ready package.

## Deliverables to WPBCA

Six artifacts, light:

1. **Kickoff memo** — one page, neighbor voice, no sales tone
2. **Asset inventory** — the messy starting pile, to normalize messy starts
3. **Permit history timeline** — 25 Seacove's regulatory evolution, visualized
4. **Current-state twin** — spatial model viewable in SketchUp
5. **Readiness Report** — validator output against RPV + draft WPBCA manifest
6. **Demo drawing set** — one or two LayOut sheets from the pipeline

Handoff materials:

- **Remodel Readiness Playbook** — 3–5 pages, "run this on your own house"
- **Draft WPBCA ARC Manifest** — seed of the ARC-as-publisher thesis, published for community critique

## What it proves

- The tool works on a real, messy, decades-old house
- The ARC's standard can be written down
- Community members can prep clean submissions without needing a licensed architect for minor remodels
- The ARC can spend its time on qualitative calls, not checklist policing

## Posture rules

- Not confrontational. No "the ARC is broken."
- Not vendor-y. No branding, no login, no payment.
- Chairman-delivers-to-community — authority redirecting itself toward publishing rather than gatekeeping.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Community reads it as Jeffe formalizing his own advantage | Hand over a second member's remodel in public, using their assets |
| Draft manifest misreads the CCR | Explicit "draft, critique welcome" framing; treat community corrections as the feature |
| Pipeline accuracy on 1958 scanned drawings is marginal | Don't hide low-confidence items; show them as part of the process |

## Not in scope

- No SaaS productization during the demo
- No multi-city expansion discussion at the community meeting
- No commitment to run the pipeline for every member forever
- No Anthropic / platform branding in the materials

## Relationship to the aligned posture

The delivery plan aligns with [[cove-arc-posture|the settled ARC posture]]: concierge + transparency, not reviewer. Jeffe is not pitching a new review standard; he is showing what the city's existing process looks like when run cleanly, with artifacts.

## Related

- [[seacove-arc-module]] — The module design this demo seeds
- [[cove-arc-posture]] — Posture rules the demo honors
- [[cove-art-jury-vs-wpbca-arc]] — Why the Bylaws already frame the process
- [[Brain/projects/Seacove|Seacove MOC]]
- [[Brain/projects/Cove|Cove MOC]]
