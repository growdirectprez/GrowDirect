---
date: 2026-04-19
type: wiki
status: stub
tags: [seacove, arc, cove, wpbca, rpv, permits, architecture]
sources: [docs/team/Condor.md, Brain/raw/processed/council/2026-04-19-permit-tech-recon.md, Brain/raw/processed/council/2026-04-19-arc-posture-correction.md, Brain/raw/processed/council/2026-04-19-art-jury-vs-wpbca-arc.md, Brain/raw/processed/council/2026-04-19-seacove-wpbca-demo-delivery.md]
last-compiled: 2026-04-19
needs-review: 2026-07-19
---

# Seacove → Cove ARC Module

**Wiki:** [[Brain/projects/Seacove|Seacove MOC]] · [[Brain/projects/Cove|Cove MOC]]

The thread that connects the Seacove hobby pipeline to a Cove platform feature: **a per-APN ARC file + neighborhood reference library, serving WPBCA members through the city's existing permit process.** This article stubs out what the module is, what it isn't, and what we still need to decide.

---

## What this is

A concierge-and-transparency layer for remodels in WPBCA, built as a Cove module. Each APN gets an ARC file — owner-controlled — that accumulates permit history, spatial model, submittal artifacts, and neighbor-visible status across decades and owners. The `rpv-permit-architect` plugin is the content engine beneath it.

## What this is not

- Not a new review authority. The city permits; WPBCA's ARC is a process concierge, not a design court. See [[Brain/wiki/cove-declaration-100|Declaration 100]] vs. the 2012 WPBCA Bylaws for why the coercive mode already drained out between 1929 and 2012.
- Not a SaaS. No subscription, no vendor posture. A Cove module for WPBCA's 81 lots.
- Not a re-imagination of the Art Jury. The AIA composition didn't survive 1949; we are not re-aspiring to it.

## Why now

Abalone Cove is at a generational turnover point. Original owners cycling out, new owners arriving with bigger plans, neighbor friction rising. Concurrently:

- **SB 543 (Jan 2026)** — California cities have 15 business days to deem ADU applications complete, 60 days to approve. Forcing function on the city side.
- **Claude Opus 4.7** — SWE-Bench Pro +10%, `/ultrareview`, meaningful vision improvements. The plugin's pipeline gets free capability lift.
- **Anthropic Skills** — formalized, portable, distributable. `rpv-permit-architect` is already in this format.

See [[Brain/projects/Seacove|Seacove MOC]] and [[cove-permit-tech-landscape|the permit-tech landscape]] for competitive context.

## Architecture (stub)

### Per-APN ARC file

Four layers, each with owner-controlled visibility (private / ARC-visible / neighbor-visible / public):

1. **Public record** — auto-populated: RPV permit history, parcel data, public case status
2. **Owner-contributed** — blueprints, photos, surveys, spatial twin, materials
3. **In-flight** — current filings with city, scope, stage, milestones
4. **Neighbor view** — owner-selected subset for community transparency

### Neighborhood reference library

Shared technical assets across the 81 lots, professional-grade formats (`.dxf`, `.geojson`, `.pdf`, `.dwg`):

- Tract 14649 survey
- Road centerlines, right-of-way geometry
- Easements (with the ocean path easement held off-platform — [[Brain/wiki/wpbca-ocean-path-easement|sensitive]])
- Historical aerials
- Geology / landslide boundary polygons (see [[Brain/wiki/cove-property-geology|Property & Geology]])
- Base maps, topo, contours
- Tract map + CCRs + subdivision history

Library assets auto-stitch onto the owner's parcel page as a basemap layer. Any engineer the owner hires starts the job a week ahead.

### The plugin as content engine

The six `rpv-permit-architect` skills stay intact, invoked by the module:

- `archive-navigator` — processes owner uploads
- `project-history` — maintains the permit timeline layer
- `rpv-building-codes` — completeness checks against RPV process
- `drawing-set-planner` — prep the submittal
- `cost-estimating` — owner budget bands
- `sketchup-guide` — 3D twin for owners who want it

## What bylaws say this must produce

From [[cove-art-jury-vs-wpbca-arc|the Art Jury vs. WPBCA ARC comparison]] — the module operationalizes what WPBCA's 2012 Bylaws already require:

- **§16.4.1** Completeness determination → module's readiness check
- **§16.4.2** Open meeting scheduling → concierge view of in-flight applications
- **§16.4.3–§16.4.4** Written decision with time limits → durable per-APN record
- **§16.4.5–§16.4.9** Appeals ladder (ARC → Board → Membership) → appeal status tracking
- **§13.17** Annual Notice of Architectural Review and Approval Procedures → auto-generated
- **§16.5** ARC Brochure for Members → the "Remodel Readiness Playbook" is this artifact

## Open questions (what we still need to decide)

1. **Data model.** How does the ARC file extend Cove's parcels schema? New table or JSON column? Versioning across owner turnover? Privacy attribute at item-level or section-level?
2. **Upload UX.** What's the smallest owner interface that feels useful on day one? A dropbox? A guided wizard? An import-from-email flow?
3. **City process coupling.** RPV's case-status data — is it scrapeable, API-accessible, or manual-only? How fresh does "in-flight" status need to be?
4. **Neighbor view default.** Opt-in or opt-out for transparency? Default privacy posture for new filings?
5. **Library governance.** Who adds to the neighborhood reference library? ARC chairman only, or board-delegated? Versioning rules for superseded assets?
6. **Transfer on sale.** What carries with the property when title changes? Twin? Permit history? Opt-in subset? Legal review needed.
7. **Ocean path easement boundary.** The [[Brain/wiki/wpbca-ocean-path-easement|ocean path easement]] is explicitly not for public library layers. Where exactly does the exclusion live in the visibility model?
8. **Linear / GRO scoping.** When this becomes real work, what's the first issue? Suggested: data model + minimum per-APN file view, no library, no upload UX — just "show what we already know about a parcel."

## Relationship to existing projects

- [[Brain/projects/Seacove|Seacove]] — the hobby pipeline and the worked example (25 Seacove)
- [[Brain/projects/Cove|Cove]] — the platform host; module lives here
- [[Brain/wiki/seacove-project|Seacove Project Overview]] — the pipeline itself, unchanged
- [[Brain/wiki/cove-platform|Cove Platform]] — tech stack the module plugs into
- [[Brain/wiki/wpbca-compliance-framework|WPBCA Compliance Framework]] — the Davis-Stirling + Bylaws context the module serves

## Governance posture

The module does not reform the ARC. It systematizes what the 2012 Bylaws already bind the Board to produce (§16.4, §13.17, §16.5) and makes those obligations easy to meet. Not an activist posture. Boring-is-the-feature during turnover.

## Not in scope for v1

- Multi-HOA support (PVE ARC, Rolling Hills, RHE) — different animals, later conversation
- Design-standard publishing (the "ARC Manifest" concept from an earlier Condor memo was retracted — see [[cove-arc-posture]])
- Direct city-of-RPV integration beyond public case status
- Any branding / SaaS productization

## Condor thread

Condor watches this thread in the council folder. See [[docs/team/Condor]] and the dated memos in `docs/council/` for the strategic framing. The wiki captures the decided state; the council folder captures the thinking.

## Related

- [[Brain/projects/Seacove]]
- [[Brain/projects/Cove]]
- [[Brain/wiki/seacove-project]]
- [[Brain/wiki/cove-declaration-100]]
- [[Brain/wiki/wpbca-compliance-framework]]
- [[Brain/wiki/cove-platform]]
