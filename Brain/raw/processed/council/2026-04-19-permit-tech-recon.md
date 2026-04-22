# Permit-Tech Recon — April 2026

**Author:** Condor
**Date:** 2026-04-19
**Status:** Opening brief

---

Horizon scan of civic-tech, permit automation, plan review, and
architectural-review-as-service — with a read on what newly-shipped Claude
capabilities change about our hand.

## Landscape

**CrossBeam** — AI ADU permit review, 480+ California cities, 28 files of
state code. Built at Claude Code Hackathon 2026. Applicant-side, like ours.
"Spell check for building code." Closest analog in the field. The fact that a
hackathon team shipped this means the moat is jurisdictional depth and trust,
not the tech.

**CivCheck / CodeComply.Ai / Archistar eCheck** — B2G plan review. Selling to
cities. Honolulu: 6 months → 6 days. LA, Seattle, Austin following. Big
budgets, slow sales cycles, but the wave is real. Opposite side of the table
from us.

**UpCodes + Symbium** — code-as-data infrastructure. 1,700+ codes, 160K+ local
amendments, 7K sections/month updated. Symbium's Complaw translates codes to
compliance logic. If we ever scale beyond RPV, we consume this layer instead of
doing code archaeology per city.

**Australia's NCC** — being rewritten as if-this-then-that machine-readable
rules. Federal project. The direction globally is codes-as-executable-rules,
not codes-as-PDFs.

## Regulatory tailwind

**SB 543 (eff. Jan 2026)** — California cities have 15 business days to deem
ADU applications complete, 60 days to approve or deny. Miss the deadline,
deemed approved. Cities are now legally exposed if they're slow. Every slow
California city is a buyer of anything that speeds intake. Pre-cleaning
submissions applicant-side is valuable to the city, not just the owner.

## Platform tailwind

**Opus 4.7** — SWE-Bench Pro 64.3%, up ~10% over 4.6. `/ultrareview` slash
command. The parts of the ARC pipeline that were marginal on 4.6 (vision
dimension extraction, Ruby codegen for edge geometry) are the parts 4.7 helps
most. Free capability lift on work we already did.

**Agent Skills** — formal portable architecture, same format across Claude
Code, Claude apps, and API. `anthropics/skills` public repo. Our
`rpv-permit-architect` plugin is already in this format. Skills are a
distribution channel, not just an internal structure.

## Our position

Everyone else in this space is selling to cities or licensed architects. The
`rpv-permit-architect` plugin is for a homeowner doing their own remodel. That
is a real audience and nobody serious is serving it well.

The move is not a SaaS. The move is **jurisdictional skill packs** published
publicly — one per peninsula city — consumed from inside Claude by anyone.
Cities benefit because applications arrive compliant. Owners benefit because
the expectations are legible. The ARC benefits because it stops being a
bottleneck and starts being a publisher of its own standard.

## What Condor is watching

- Whether Anthropic's skill registry becomes a civic distribution channel
- Whether any California city publishes its own skill pack (forcing function if
  one does)
- CrossBeam's pilot results — proof or disproof of the hackathon-scale thesis
- UpCodes pricing and API posture — is the code-as-data layer accessible, or
  walled
- Follow-on legislation behind SB 543 — coastal overlay, historic review,
  non-ADU remodels

## The reframe

CivCheck and CodeComply pitch the reviewer. Our move is to route around the
reviewer by making the reviewer's function trivial. White-hat civic engineering:
don't fight the ARC, make its coercive mode obsolete as friction. The ARC
transitions from gatekeeper to publisher.

That is the thread.
