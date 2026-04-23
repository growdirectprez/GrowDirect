# Dispatch — Brain Scaffold Design (GRO-520)

**To:** next Cowork/Claude session opened against this repo
**From:** Alejandro (owner), 2026-04-23
**Source of truth:** `docs/playbook-brain-scaffold-design.md`
**Linear:** GRO-520 (parent) — bump Medium → High on kickoff
**Scope level:** ☐ A (spec-only, default) ☐ B (+ tooling prototype) ☐ C (+ Canary pilot)

---

## Mission

Produce **Brain Federation SDD v1.0 Final** at
`docs/sdds/platform/brain-federation.md`. The SDD defines the
personal / ops / app layer taxonomy, directory layout, manifest
format, inter-brain query protocol, exposure policy, and migration
plan — locked, version-stamped, committed. **No files move in this
engagement.**

---

## Required reading (in order, before any work)

1. `docs/playbook-brain-scaffold-design.md` — the full playbook
2. `CLAUDE.md` — rule zero + Session Discipline
3. `Brain/projects/Method.md` — the six-category method MOC
4. `docs/sdds/platform/factory-pipeline.md` — SDD format reference
5. GRO-520 on Linear — context + open questions
6. `docs/playbook-method-katz-reverse-engineer.md` — the rigor we're mirroring

Do not start Phase 1 until all six are read.

---

## First deliverable (this session)

Phase 1 only — **Assess**. Output: `Brain/raw/inbox/_brain-assessment-v1.md`
(scratch, two pages max). Sections: Inventory, Cross-references,
Exposure audit, First impressions. Stop after writing it. Do not
start Phase 2 in the same session.

---

## Working rules

- **Forethought, not execution.** Every instinct to move a file is
  wrong for this engagement. The deliverable is a spec.
- **Evidence, not assertion.** When the SDD says something about the
  current state, it cites the assessment from Phase 1.
- **Eight workstreams, declared priority.** W1–W7 are v1 core/light.
  W8 (change management) is parked to v1.1 and must appear in the
  SDD as an explicit deferral, not a silent omission.
- **Version discipline.** SDD goes v0.9 Draft → overnight gap →
  second read → v1.0 Final. No shortcut.
- **One Linear parent.** GRO-520 exists. Do not create a duplicate.
  Child issues under GRO-520 only for the eight workstreams, named
  `GRO-520.W# — <workstream>`.
- **Clean up scratch.** Every `_brain-*-v1.md` under `Brain/raw/inbox/`
  gets deleted at Phase 7 after content lands in the SDD.

---

## Out of scope (for this dispatch)

- Migration execution (parked as a new Linear issue at Phase 6 lock).
- Tooling implementation (only in scope if scope level is B or C).
- Redesigning Brain templates beyond adding `brain-manifest.md`.
- Changing `content-engine/` beyond recording current state in W6.
- Anything in other apps' repos. Stay in `/Users/gclyle/GrowDirect/`.

---

## Check-in conditions (stop and report)

Return to the owner before continuing if:

- Phase 1 assessment surfaces sensitive content in `Brain/` that
  looks already-leaked or actively exposed.
- Any workstream decision materially contradicts GRO-520's proposed
  layers (personal / ops / app). Propose alternatives; don't proceed.
- You find that `content-engine/`'s registry already has scope tags
  — that changes W6's default and the migration plan.
- Scope drift: if a workstream is running >2× its sizing estimate,
  stop and surface the reason.

Otherwise, report at end of each phase with: what shipped, what's
queued, open questions accumulated for the SDD's Section 11.

---

## Done looks like

- `docs/sdds/platform/brain-federation.md` exists, frontmatter
  `version: 1.0`, `status: Final`.
- `Brain/wiki/methods/brain-layer-taxonomy.md` exists and is linked
  from the SDD.
- `Brain/templates/brain-manifest.md` exists with ops + canary
  examples.
- `Brain/projects/Method.md` has a new "Knowledge Layer" section
  pointing to the SDD.
- GRO-520 closed. Migration follow-up issue opened, parked.
- No files under `Brain/` moved. (Success criterion, not a caveat.)

---

## One-line kickoff for the receiving session

> "Execute `docs/playbook-brain-scaffold-design.md` per
> `docs/dispatch-brain-scaffold-design.md`. Start at Phase 1.
> Report after assessment."
