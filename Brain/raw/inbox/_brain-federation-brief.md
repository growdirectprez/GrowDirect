---
type: scratch
status: phase-2-output
tags: [brain-federation, gro-520, phase-2, brief]
created: 2026-04-23
playbook: docs/playbooks/playbook-brain-scaffold-design.md
raw: Brain/raw/inbox/_brain-federation-raw/
assessment: Brain/raw/inbox/_brain-assessment-v1.md
---

# Brain Federation — Summarized Brief (Phase 2)

One page. Three sections. Success criteria come verbatim from
GRO-520's Deliverable list — paraphrased here and tightened to the
facts the [[_brain-assessment-v1|Phase 1 assessment]] has on record.

---

## Problem

Brain today is a single flat Obsidian vault with 221 wiki articles,
8 project MOCs, 7 method cards, 1,280 binary artifacts in
`raw/inbox/`, and a REGISTRY.json that indexes everything at 1.5 MB.
Prefix-as-scope (`canary-*`, `cove-*`, `growdirect-*`, etc.) is doing
80% of the federation work implicitly — but it is convention, not
contract.

Three failure modes are visible today:

1. **The `growdirect-` prefix covers three distinct sensitivity
   tiers** — ops-public (manifesto, glossary), ops-private (warchest,
   fee-window, attack-plan), and ops-sensitive (patent visuals,
   founders-case). A flat namespace cannot enforce the difference. 86
   articles sit behind one prefix.
2. **`raw/inbox/` is source material, not publishable content** —
   1,280 binaries and 68 extracted markdowns that must not be
   published but are indistinguishable from published content at the
   vault level.
3. **The personal layer is empty** — `journal/` is a `.gitkeep`
   placeholder. Pretending it does not exist leaves the vault
   vulnerable to an accidental journal entry landing in the wrong
   tier.

Cross-repo links (217 in the current inventory) are load-bearing. Any
federation must preserve them. Any migration that breaks links breaks
the vault's connective tissue and forfeits the federation's value.

## Constraints

- **Preserve prefix-as-scope.** It already works for 80% of the vault.
  Formalize it; don't replace it.
- **Preserve the 217 cross-repo links.** Migration produces a link
  manifest before it moves any file.
- **Peer the Federation SDD with the Factory Pipeline SDD.** Both
  live in `docs/sdds/platform/`. The Federation is a platform
  concern, not a project one.
- **Federation is mechanical, not philosophical.** The design locks
  layer boundaries, directory layout, manifest format, query
  protocol, exposure policy, registry format, and governance. It does
  not re-invent the method.
- **No migration before the SDD locks.** Phase 4 drafts v0.9; Phase 6
  reviews and locks v1.0; Phase 5 plans migration. File moves happen
  after all three.
- **Raw/inbox stays raw.** Source material is indexed but never
  published. The federation must express this as a first-class
  boundary, not a convention.

## Success criteria

From GRO-520, reframed in Phase 2 terms:

- [ ] A Brain Federation SDD v1.0 locked in `docs/sdds/platform/` —
      peer of factory-pipeline.md
- [ ] Layer taxonomy explicit: public / ops-public / ops-private /
      ops-sensitive / personal / raw. Each layer has a directory
      pattern and an exposure policy.
- [ ] Manifest format defined — per-layer `_manifest.yaml` (or `.json`)
      that declares ownership, exposure, and retention
- [ ] Inter-brain query protocol — how Canary Brain queries
      GrowDirect Brain, and vice versa; how the memory bus resolves
      cross-layer citations
- [ ] Exposure policy — who/what reads each layer, enforced at
      publish time (not just at read time)
- [ ] Registry format — how REGISTRY.json shape changes to accommodate
      layers; embedding lifecycle across layers
- [ ] Governance — versioning, change control, who approves a layer
      promotion/demotion
- [ ] Migration plan — file-by-file move list, link-rewriting strategy,
      validation gates. **SDD includes the plan; migration execution is
      a separate sprint.**
- [ ] All 221 wiki articles map to a layer in the SDD. No orphans.
- [ ] All 217 cross-repo links survive migration (validated by a
      post-migration audit script).

Deferred to v1.1: change-management workflow beyond versioning
(W8 in the playbook). v1.0 locks structure; v1.1 locks operations.

---

## Next (Phase 3)

Eight workstream notes, parallelizable:

1. W1 — Layer taxonomy
2. W2 — Directory layout
3. W3 — Manifest format
4. W4 — Inter-brain query protocol
5. W5 — Exposure policy
6. W6 — Registry & embeddings
7. W7 — Governance & versioning
8. W8 — Change management (deferred to v1.1)

Each produces a short design note that cites evidence from
[[_brain-assessment-v1|Phase 1 assessment]] and
[[_brain-federation-raw/README|the raw inputs]]. When all eight land,
Phase 4 drafts the SDD.
