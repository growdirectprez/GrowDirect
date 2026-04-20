# The ARC Protocol — Publisher Manifest + Permit Twin

**Author:** Condor
**Date:** 2026-04-19
**Status:** Speculative sketch. R&D, not a plan.

---

This is a concept memo. Not a product, not a spec, not a commitment. A shape
worth looking at.

## The core idea

Architectural review today is a black box. The applicant sends plans. The
reviewer judges them against rules the reviewer holds. Back-and-forth fills
the gap between applicant's guess and reviewer's standard. That gap is where
time, money, and resentment live.

Replace the gap with a shared artifact.

**Publisher side — the ARC Manifest.** The reviewing body publishes a
structured, machine-readable document describing what it expects from a
submission for a given project type. Setbacks. View-corridor constraints.
Acceptable exterior palettes. Sheet index requirements. Required studies.
Named, typed, versioned.

**Applicant side — the Permit Twin.** The applicant maintains a living
spatial + documentary model of the project (blueprints, photos, descriptions,
dimensions, sheet set). The twin can be validated against any ARC Manifest.
The validator says: here are the 14 things this manifest asks for; here are
the 11 you satisfy; here are the 3 gaps with exact locations.

The ARC reviews a submission that was already validated against its own
published manifest. Its job narrows from gatekeeper to judge of aesthetic and
qualitative calls that can't be encoded. The coercive mode — secret standards,
surprise comments, slow cycles — becomes obsolete as friction.

## What the Manifest looks like

Not a PDF. Not a web form. A file the ARC publishes and versions, like a
`tax-package.yml` or an `openapi.json`.

Sketch:

```yaml
body: WPBCA ARC
jurisdiction: Abalone Cove / Rancho Palos Verdes
version: 2026.04
effective: 2026-05-01

project_types:
  - id: exterior-remodel
    triggers:
      - any_facade_change
      - roof_material_change
      - window_geometry_change
    requirements:
      setbacks:
        front: 25ft
        side: 10ft
        rear: 15ft
      view_corridor:
        reference: wpbca-ccr-section-9.4
        check: no_addition_above_ridge_of_1960_envelope
      exterior_palette:
        allowed: [earth-tones, coastal-whites, weathered-wood]
        disallowed: [primary-saturations, reflective-finishes]
      submittals:
        - site-plan
        - elevations-all-sides
        - proposed-material-board
        - neighbor-notification-log
```

Human-readable. Machine-readable. Versioned. Public.

When the ARC updates its standard, it bumps the version. Every submission is
timestamped against the version it targeted. No more "the rule changed since
you submitted."

## What the Twin looks like

A project directory — the same shape as `arc/projects/seacove/` today, extended.

```
projects/25-seacove/
  manifest-target.yml       # which ARC manifest + version this targets
  structure/
    spatial-model.json      # dimensions, envelope, roof ridge, openings
    materials.yml           # exterior palette choices
    site/
      parcel-polygon.geojson
      setbacks-measured.json
  history/
    1958-original.yml
    1960-bedroom-addition.yml
    2020-phase-3.yml
    2026-current-remodel.yml
  submittals/
    site-plan.pdf
    elevations.pdf
    material-board.pdf
  validation/
    2026-04-19-wpbca-2026.04.json   # last validation report
```

The twin persists between permits. It ages with the house. Next time a new
owner remodels, they inherit 70 years of documented state instead of rebuilding
from scratch. That is the multi-generational moat.

## The validator

A function:

```
validate(twin, manifest) -> ValidationReport
```

Returns structured findings: which requirements are satisfied, which have
gaps, where the gap is in the twin (specific sheet, dimension, material
choice), what would fix it. The ARC runs the same validator on submission.
Applicant and reviewer see the same report.

The validator is where Claude skills live. Each manifest requirement maps to
a skill that knows how to check it against the twin. View-corridor compliance
is a skill. Setback measurement is a skill. Material-palette check is a skill.

## Why this is interesting

- **Everyone else is building one side.** CivCheck, Archistar, CrossBeam do
  reviewer-side OR applicant-side validation in isolation. Nobody has sketched
  the shared artifact that lets both sides converge.
- **It's not SaaS.** The manifest is a file. The twin is a directory. The
  validator is a skill. Distribution is a git repo, not a subscription.
- **It composes with what exists.** UpCodes provides the code corpus.
  Anthropic Skills provides the agent format. Claude 4.7 provides the
  intelligence. The protocol is the connective tissue.
- **The pilot venue is already in hand.** WPBCA has 81 lots and Jeffe on the
  inside. If the first ARC Manifest ever published is
  `wpbca-arc-2026.04.yml`, that's a story.

## What would kill this

- If the ARC bodies refuse to publish. (Likely, at first. Work around by
  publishing the *inferred* manifest from public CCRs, label it
  "unofficial," and let the ARC either adopt or dispute it. Either outcome is
  useful.)
- If the validator's judgment calls produce false confidence. (Mitigation:
  confidence scoring on every finding, humans remain in the loop for
  qualitative calls, never claim approval — only completeness.)
- If UpCodes / Symbium / equivalent gates the code corpus behind pricing that
  kills the owner-builder angle. (Mitigation: RPV is narrow enough to
  maintain by hand; peninsula cities are ~5 total.)

## Open questions for Condor to chew on

- Does the manifest belong in the jurisdiction's git repo, a neutral registry,
  or both (mirror)?
- What's the minimum-viable manifest schema that still captures the WPBCA
  CCR? Try to draft it against existing CCR text.
- How does the twin version across owners? Transfer on sale, with what
  privacy posture?
- Is there a way to make the validator produce a human-readable PDF so that
  legacy reviewers can consume it without adopting the protocol?

## Next

Nothing is committed. The tractable experiments, in rough order of
information-per-effort:

1. Draft `wpbca-arc-manifest.yml` v0.1 against the existing CCR text. Just
   see if the CCR *can* be expressed this way. Two hours of work, answers the
   hardest question.
2. Sketch the validator's contract — input types, output shape, confidence
   model — not the code. Half a page.
3. Look at what Anthropic Skills' `anthropics/skills` repo structure would
   hold for a "manifest validator" skill. Does it fit the existing format, or
   need a new one?

Condor picks these up when called. Nothing else on a clock.
