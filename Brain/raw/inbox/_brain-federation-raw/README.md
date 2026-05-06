---
type: scratch
status: phase-2-raw-index
tags: [brain-federation, gro-520, phase-2, raw-inputs]
created: 2026-04-23
playbook: docs/playbooks/playbook-brain-scaffold-design.md
---

# Brain Federation — Raw Input Index (Phase 2)

Phase 2 of GRO-520 per
[[../../docs/playbook-brain-scaffold-design|the playbook]]. This folder is
the *raw* half of the Katz compilation triad. The *compiled* artifact is
[[_brain-assessment-v1|Phase 1 assessment]]. The *summarized* brief is
[[_brain-federation-brief|brief.md]].

Raw inputs are referenced here by path, not duplicated — duplication
would invite drift. When the SDD cites a source, cite the path.

## Input 1 — GRO-520 (Linear)

**Placeholder.** The GRO-520 issue description lives in Linear. Copy
its full text into `gro-520-linear.md` during the SDD-drafting session
so evidence citations can point at a file, not a URL. (Current author
session does not have Linear write access to extract cleanly.)

## Input 2 — CLAUDE.md (Brain rules + Session Discipline)

Source: `/Users/gclyle/GrowDirect/CLAUDE.md`

Relevant sections:
- `## Brain — Domain Knowledge` (MOC-first reading, search before writing,
  no volatile data in wiki)
- `## Session Discipline` (10 rules — especially 6 "flat archives", 7
  "commit or revert", 8 "check Brain before creating", 9 "route knowledge
  through Brain")
- `## File Layout` (the current un-federated layout)

## Input 3 — Method MOC

Source: `/Users/gclyle/GrowDirect/Brain/projects/Method.md`

The method the federation SDD must preserve: six-category navigation
(Models / Roles / Techniques / Work Products / Activities / Communication
Documents). The federation should federate *along* the method, not
against it.

## Input 4 — Factory Pipeline SDD

Source: `/Users/gclyle/GrowDirect/docs/sdds/platform/factory-pipeline.md`

The sibling SDD in the platform layer. The Federation SDD will be a
peer, not a child. Read for SDD format conventions (preamble, stages,
definition of done, open questions).

## Input 5 — Katz method reverse-engineering playbook

Source: `/Users/gclyle/GrowDirect/docs/playbooks/playbook-method-katz-reverse-engineer.md`

Method precedent — Katz's raw/compiled/summarized pattern is what this
phase borrows from. Review for evidence-handling discipline.

## Input 6 — Prior-thinking notes

**None on file as of 2026-04-23.** If the operator has private notes
(napkin sketches, draft layouts, earlier attempts), drop them into
this folder as `prior-*.md` files. Absence is fine — do not invent
prior thinking.

## Input 7 — Current Brain inventory snapshot

The Phase 1 assessment already captures the live inventory
([[_brain-assessment-v1]]). No separate artifact needed. When the SDD
cites "221 wiki articles", cite the assessment, which cited the
filesystem.

---

## Usage in Phase 3

Each workstream note (W1–W8) should cite these inputs by filename +
section when they drive a design decision. No handwaving. If a
workstream's decision cannot cite one of these inputs (or the Phase 1
assessment), it is either out of scope for v1 or needs a new source
added here first.
