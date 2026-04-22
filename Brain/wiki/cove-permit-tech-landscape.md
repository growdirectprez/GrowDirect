---
date: 2026-04-19
type: wiki
status: published
tags: [cove, wpbca, rpv, permits, civic-tech, competitive-landscape, plan-review]
sources: [Brain/raw/processed/council/2026-04-19-permit-tech-recon.md, docs/team/Condor.md]
last-compiled: 2026-04-19
needs-review: 2026-07-19
---

# Permit-Tech Landscape — April 2026

Civic-tech, permit automation, plan review, and architectural-review-as-service horizon scan. Frames where the [[seacove-arc-module|Cove ARC module]] sits relative to the broader market.

## Landscape

### CrossBeam — Applicant-side AI ADU permit review
- 480+ California cities covered, 28 files of state code
- Built at Claude Code Hackathon 2026
- Closest analog to the Cove ARC module's posture
- Tagline equivalent: "spell check for building code"
- **Implication:** A hackathon team shipped this. The moat is jurisdictional depth and trust, not the tech.

### CivCheck / CodeComply.Ai / Archistar eCheck — B2G plan review
- Selling to cities, not applicants
- Honolulu pilot: 6 months → 6 days
- LA, Seattle, Austin following
- Big budgets, slow sales cycles
- **Implication:** Opposite side of the table from us. They serve the reviewer; the Cove module serves the applicant.

### UpCodes + Symbium — Code-as-data infrastructure
- 1,700+ codes indexed
- 160K+ local amendments tracked
- 7K sections updated per month
- Symbium's Complaw translates codes into compliance logic
- **Implication:** If we ever scale beyond RPV, we consume this layer instead of doing code archaeology per city.

### Australia's NCC — Government-led codes-as-rules rewrite
- Federal project rewriting the National Construction Code as if-this-then-that machine-readable rules
- **Implication:** The global direction is codes-as-executable-rules, not codes-as-PDFs.

## Regulatory tailwind

### SB 543 (effective January 2026)
- California cities have **15 business days** to deem ADU applications complete
- **60 days** to approve or deny
- Miss the deadline → deemed approved
- **Implication:** Every slow California city is now legally exposed. Pre-cleaning submissions applicant-side becomes valuable to the city, not just to the owner.

## Platform tailwind

### Claude Opus 4.7
- SWE-Bench Pro 64.3% (~10% over 4.6)
- `/ultrareview` slash command
- The marginal parts of the ARC pipeline on 4.6 (vision dimension extraction, Ruby codegen for edge geometry) are exactly the parts 4.7 helps most
- **Implication:** Free capability lift on work already shipped.

### Anthropic Agent Skills
- Formal portable architecture, same format across Claude Code, Claude apps, and API
- `anthropics/skills` public repo
- The `rpv-permit-architect` plugin is already in this format
- **Implication:** Skills are a distribution channel, not just an internal structure.

## Cove's position

Everyone else in this space is selling to cities or licensed architects. The `rpv-permit-architect` plugin is for a homeowner doing their own remodel. That is a real audience and nobody serious is serving it well.

The move is **jurisdictional skill packs** published publicly — one per peninsula city — consumed from inside Claude by anyone:

- **Cities benefit** because applications arrive compliant
- **Owners benefit** because expectations are legible
- **The ARC benefits** because it stops being a bottleneck and starts being a publisher of its own standard

## What Condor is watching

- Whether Anthropic's skill registry becomes a civic distribution channel
- Whether any California city publishes its own skill pack (forcing function if one does)
- CrossBeam's pilot results — proof or disproof of the hackathon-scale thesis
- UpCodes pricing and API posture — is the code-as-data layer accessible, or walled
- Follow-on legislation behind SB 543 — coastal overlay, historic review, non-ADU remodels

## The reframe

CivCheck and CodeComply pitch the reviewer. Cove's move is to route around the reviewer by making the reviewer's function trivial. White-hat civic engineering: don't fight the ARC, make its coercive mode obsolete as friction. The ARC transitions from gatekeeper to publisher.

That is the thread.

## Related

- [[seacove-arc-module]] — The Cove ARC module this landscape contextualizes
- [[cove-arc-posture]] — Why we route around rather than reform
- [[Brain/projects/Cove|Cove MOC]]
- [[Brain/projects/Seacove|Seacove MOC]]
