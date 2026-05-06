# Brain Scaffold Design Playbook

Apply Katz-2003-style structural rigor to the forethought phase of
GrowDirect's Brain federation (personal / ops / app brains as agent
cosmos). This is an **Assess → Design** engagement against our own
knowledge layer, closing with a locked v1.0 scaffold spec before any
files are moved.

Pairs with Linear **GRO-520** (Document hierarchical Brain architecture)
and the reverse-engineered method in
`docs/playbook-method-katz-reverse-engineer.md`.

---

## Why a playbook for this

The instinct on GRO-520 is to "just start moving folders." That is
exactly the failure mode Katz's structure prevents. Their 2003 archive
shows why forethought wins: every domain got its own compilation triad,
every phase produced version-stamped artifacts, and deprioritized
workstreams (change management) still appear on the map so they could
be *explicitly* deferred rather than silently forgotten.

We want that same property for Brain:

- **No silent folder sprawl.** Every directory we add has a declared
  layer, manifest, and exposure policy before it contains files.
- **Migration is traceable.** Every existing `Brain/*` node maps to a
  target node in the federation, with a recorded decision.
- **Deferrals are visible.** Workstreams we choose not to build in v1
  (e.g., cross-brain embeddings) are named and parked, not dropped.
- **The scaffold ships as a locked artifact.** A Brain Federation SDD
  v1.0 Final, the way Katz locked their Roadmap v1.0 Final.

---

## Goal

Produce, in order of value:

1. **Brain Federation SDD v1.0 Final** — `docs/sdds/platform/brain-federation.md`.
   The canonical spec: layer taxonomy, directory layout, manifest
   format, inter-brain query protocol, exposure policy, migration plan,
   open questions parked for v1.1.
2. **Layer taxonomy reference** — `Brain/wiki/methods/brain-layer-taxonomy.md`.
   The rule set for classifying any note into personal / ops / app.
3. **Existing-content mapping** — `Brain/raw/inbox/_brain-mapping-v1.md`
   (scratch). Every current `Brain/` path mapped to its target layer
   with a one-line rationale. Deleted after SDD finalization.
4. **Manifest template** — `Brain/templates/brain-manifest.md`. Every
   brain publishes one of these; defines scope, audience, exposure,
   index strategy.
5. **Updated Method MOC** — `Brain/projects/Method.md` gains a new
   "Knowledge Layer" section linking to the federation SDD.

Explicit non-goal for v1: **moving files**. The playbook ends at a
locked spec, not at a migrated repo. Migration gets its own playbook
(and its own Linear issue) once the spec is approved.

---

## Scope decision — before starting

How deep does this design pass go?

- [ ] **Level A (spec-only):** Produce the SDD + taxonomy + mapping +
      manifest template. No code, no file moves. One session of
      assessment, one session of design, one session of review/lock.
      **~3 sessions. Recommended default.**
- [ ] **Level B (spec + tooling prototype):** Level A plus a working
      prototype of the manifest validator and registry-scope tagging in
      `content-engine/`. Proves the design is implementable.
      **~5 sessions.**
- [ ] **Level C (spec + pilot):** Level B plus one app-brain carved
      out end-to-end (Canary is the obvious pilot — it's closest to
      beta and has the cleanest MOC). Validates the migration story.
      **~8 sessions.**

Record scope decision: ________________________

Default recommendation: **Level A**, then decide on Level B/C only after
the SDD is locked. Premature tooling is exactly what the Session
Discipline rules in `CLAUDE.md` warn against.

---

## Phase 0 — Linear linkage

GRO-520 exists. Don't create a duplicate.

- [ ] Open GRO-520. Confirm its description still matches current
      thinking. If not, update in place.
- [ ] Add this playbook as a reference:
      `docs/playbook-brain-scaffold-design.md`.
- [ ] Create child issues in GRO-520 for each workstream in Phase 3
      (see Workstream table). Title format: `GRO-520.W# — <workstream>`.
- [ ] Set GRO-520 priority to High while active; revert to Medium on
      completion.

---

## Phase 1 — Assess (current state, no design yet)

Mirror Katz Phase I Workstream 1.2 (Assess). Read what exists. Write
nothing new. Produce one compilation: "What Brain contains today."

### 1.1 — Inventory

- [ ] Walk `Brain/` top to bottom. For each top-level directory,
      record: name, purpose (inferred), file count, frontmatter
      patterns used, whether MOCs link to it.
- [ ] List every file in `Brain/templates/`, `Brain/wiki/`,
      `Brain/projects/`, `Brain/method/`, `Brain/raw/inbox/`,
      `Brain/daily/`, any others. Flat table, one row per directory.
- [ ] Note unusual items: orphan files, draft notes, anything that
      feels personal vs operational.

### 1.2 — Cross-references

- [ ] Sample 10 wiki articles. For each, list its `[[wikilinks]]` and
      note which link to content that feels like a different layer
      (personal note referencing an app decision, etc.). This is the
      evidence for why federation is needed.
- [ ] Check `content-engine/registry.db` (or equivalent). Understand
      current indexing — is it one monolithic index? How are project
      scopes tagged? Record for Phase 3 Workstream W6.

### 1.3 — Exposure audit

- [ ] Scan for anything sensitive that's currently in `Brain/`:
  - Personal journal content
  - Customer names in CRM-like notes
  - Pricing/financial detail not yet public
  - Credentials, tokens, vendor-specific security context
- [ ] Flag without moving. This feeds the exposure policy in the SDD.

### 1.4 — Output

- [ ] Write `Brain/raw/inbox/_brain-assessment-v1.md` (scratch).
      Sections: Inventory, Cross-references, Exposure audit, First
      impressions. **Two pages max.**
- [ ] Stop. Do not start Phase 2 in the same session. Let the
      assessment sit overnight.

---

## Phase 2 — Compile source inputs (Katz compilation triad)

Borrow Katz's raw → compiled → summarized pattern. The assessment
above is the *compiled* source; we also need *raw* inputs and a
*summarized* brief.

- [ ] **Raw:** Gather into `Brain/raw/inbox/_brain-federation-raw/`:
  - GRO-520 description (copy verbatim)
  - Relevant sections of `CLAUDE.md` (Brain rules, Session Discipline)
  - `Brain/projects/Method.md` (full)
  - `docs/sdds/platform/factory-pipeline.md` (reference point — the
    federation SDD will be a sibling)
  - `docs/playbook-method-katz-reverse-engineer.md` (method source)
  - Any prior-thinking notes the user has on layering
- [ ] **Compiled:** The assessment from Phase 1.4 is the compiled
      artifact. No new work.
- [ ] **Summarized:** Write `Brain/raw/inbox/_brain-federation-brief.md`
      (one page). Three sections: *Problem*, *Constraints*, *Success
      criteria*. Success criteria come from GRO-520's Deliverable list.

Why bother: when the SDD cites evidence ("based on the current Brain
inventory, 34% of wiki articles cross a layer boundary"), it cites
these compiled documents, not handwaves. Same discipline Katz applied
to their vendor/licensing/system compilations.

---

## Phase 3 — Design workstreams (parallel)

Eight workstreams. Each produces a short design note that feeds the
SDD. Assign priority to each so v1 vs v1.1 is explicit up front.

| # | Workstream | v1 priority | Output |
|---|-----------|-------------|--------|
| W1 | Layer taxonomy | **v1 core** | Classification rules (personal / ops / app) |
| W2 | Directory layout | **v1 core** | File tree for the federation |
| W3 | Manifest format | **v1 core** | `brain-manifest.md` template + fields |
| W4 | Inter-brain query protocol | **v1 core** | How agents query across brains |
| W5 | Exposure policy | **v1 core** | Public / internal / private rules + redaction |
| W6 | Registry & embeddings | **v1 core** | One shared index w/ scope tags, or federated |
| W7 | Governance & versioning | v1 light | Who creates a brain, version bumps, sunset |
| W8 | Change management | **v1.1 park** | How humans + agents learn the new layout |

Katz pattern to follow: W8 is explicitly listed even though we're
parking it. That's the point — deprioritization is a declared decision,
not an oversight.

### 3.1 — Layer taxonomy (W1)

- [ ] Define personal layer: private, never leaves vault, not indexed
      for external agents. Examples: daily notes, drafts, journal.
- [ ] Define ops layer: internal-cross-project operational knowledge.
      Examples: factory pipeline, infra runbooks, session discipline
      writeups, method MOCs.
- [ ] Define app layer: project-scoped domain knowledge. Examples:
      Canary chirp rule specs, Cove HOA governance notes, Angel real
      estate research.
- [ ] Edge cases: where does `Brain/raw/inbox/` live? (Proposal: ops by
      default, retag on synthesis.) Where do meeting notes live?
      (Proposal: tagged by dominant project; cross-project goes to ops.)
- [ ] Output: `Brain/wiki/methods/brain-layer-taxonomy.md` draft.

### 3.2 — Directory layout (W2)

- [ ] Propose file tree. Two candidates to evaluate:
  - **Flat federation:** `Brain/personal/`, `Brain/ops/`,
    `Brain/apps/canary/`, `Brain/apps/cove/`, etc. One repo, scope via
    subdirs.
  - **Separate vaults:** personal is a different Obsidian vault
    entirely (gitignored), ops is the current repo, each app brain is
    a submodule/subtree under its app repo.
- [ ] Trade-off matrix: simplicity, git-exposure safety, Obsidian
      backlink behavior across vaults, agent access patterns.
- [ ] Pick one, justify, note the rejected alternative (so future-you
      doesn't re-litigate the decision).

### 3.3 — Manifest format (W3)

- [ ] Draft `Brain/templates/brain-manifest.md`. Minimum fields:
  - `brain_id:` (canary, cove, ops, personal, etc.)
  - `layer:` (personal / ops / app)
  - `scope:` one-paragraph description
  - `audience:` (owner-only / internal-agents / collaborators / public)
  - `exposure:` (private / internal / publishable-with-redaction / public)
  - `index:` (embeddings scope tag, search scope)
  - `depends_on:` (list of brain_ids this brain queries)
  - `version:` (semver)
  - `last_reviewed:` (ISO date)
- [ ] Write an example manifest for `ops` and for `canary`. Stops you
      discovering missing fields while drafting the SDD.

### 3.4 — Inter-brain query protocol (W4)

- [ ] Pick the simplest workable model. Leading candidate: each brain
      exposes a *read* interface via its MCP; agents in other brains
      call it by `brain_id`. Complex cross-brain joins are deferred.
- [ ] Document three canonical queries as examples:
  - Canary agent asks ops: "what's the deploy checklist?"
  - Ops agent asks canary: "what chirp rules exist?"
  - Any agent asks personal: **denied** (personal is read-only to owner)
- [ ] Error modes: brain not available, permission denied, stale
      content.

### 3.5 — Exposure policy (W5)

- [ ] Rules table: by layer × by action (read / publish / export).
- [ ] Redaction rules: what gets stripped before external publication
      (author email, customer names, internal URLs).
- [ ] Publication workflow: "publish Canary brain" means what, exactly?
      (Proposed: run redactor, write to `public/canary-brain/`, commit
      to open repo, tag version.)
- [ ] Explicit list of content types that **never** publish regardless
      of layer (daily notes, drafts, anything with `private: true`
      frontmatter).

### 3.6 — Registry & embeddings (W6)

- [ ] Decision: shared index with scope tags, or one index per brain?
- [ ] Proposal to evaluate: **one index, scope-tagged.** Simpler
      ops story, lets agents query across brains when permitted.
      Scope filters enforced at query time.
- [ ] Alternate: **one index per brain**, federated query layer.
      Stronger isolation, more infra.
- [ ] Pick one. Note implications for `content-engine/registry.db`.

### 3.7 — Governance & versioning (W7)

- [ ] Who can create a new brain? (Solo founder today → owner.
      Codify anyway so future-you doesn't have to re-decide.)
- [ ] Brain version bump rules: layout change → minor; new field in
      manifest → minor; layer change for existing content → major;
      content-only change → patch.
- [ ] Sunset protocol: how to deprecate a brain (Seacove might
      eventually roll into Cove).

### 3.8 — Change management (W8, parked to v1.1)

- [ ] One-paragraph placeholder in the SDD explaining: change
      management for the humans and agents using the new layout is out
      of scope for v1. Will be addressed once the structural spec has
      been in use for ≥4 weeks and we have real friction points to
      design around.
- [ ] This section exists *specifically* so it can't be forgotten.

---

## Phase 4 — Draft the SDD v0.9

Synthesize the workstream notes into one document.

- [ ] Create `docs/sdds/platform/brain-federation.md`. Use the same
      structure as `factory-pipeline.md`.
- [ ] Sections:
  1. Context & motivation (cite Phase 2 brief)
  2. Layer taxonomy (W1)
  3. Directory layout (W2)
  4. Manifest format (W3)
  5. Inter-brain query protocol (W4)
  6. Exposure policy (W5)
  7. Registry & embeddings (W6)
  8. Governance & versioning (W7)
  9. Deferred: change management (W8)
  10. Migration plan (Phase 5)
  11. Open questions parked for v1.1
- [ ] Mark it **v0.9 Draft** in frontmatter. Not Final. Not locked.

---

## Phase 5 — Migration mapping

One file, one decision per row. Not executed yet — captured.

- [ ] Create `Brain/raw/inbox/_brain-mapping-v1.md` (scratch).
- [ ] Columns: `current_path | target_layer | target_path | rationale | redaction_needed`.
- [ ] One row per existing top-level `Brain/*` directory, and for
      anything ambiguous, per file.
- [ ] Ambiguity log: anything you can't confidently classify gets its
      own row with `target_layer: UNRESOLVED` and a note. These feed
      the "open questions parked for v1.1" section of the SDD.
- [ ] Reference the mapping from SDD section 10 (Migration plan).

---

## Phase 6 — Review & lock

Katz marked artifacts "Final" deliberately. Do the same.

- [ ] Read the SDD straight through in one sitting. Don't edit — list
      concerns in a separate file.
- [ ] Sleep on it.
- [ ] Second pass: resolve concerns or demote them to open questions.
- [ ] Bump version to **v1.0 Final**. Update frontmatter. Commit with
      message: `Brain Federation SDD v1.0 Final (GRO-520)`.
- [ ] Update `Brain/projects/Method.md`: add "Knowledge Layer" section
      linking to the SDD.
- [ ] Close GRO-520 as the design phase.
- [ ] Open follow-up Linear issue: `GRO-###: Execute Brain migration
      per Federation SDD v1.0`. Not scheduled yet — just parked.

---

## Phase 7 — Cleanup

Per `CLAUDE.md` "Clean up your own artifacts."

- [ ] Delete `Brain/raw/inbox/_brain-assessment-v1.md`,
      `_brain-federation-brief.md`, `_brain-federation-raw/`,
      `_brain-mapping-v1.md`. Content now lives in the SDD.
- [ ] Keep: the SDD, the taxonomy wiki article, the manifest template,
      the updated Method MOC.

---

## Non-obvious considerations

- **Personal layer is the hardest.** Everyone underestimates what
  leaks into it. Plan on the exposure audit (Phase 1.3) finding more
  than you expect.
- **Obsidian backlinks don't cross vaults.** If W2 picks the
  separate-vaults model, you lose cross-brain `[[wikilinks]]` rendering.
  Mitigation: use explicit `brain_id:path` references, render through
  a plugin or agent. This is a real constraint, not a hypothetical.
- **Agents don't know about layers until they're told.** The layer
  system means nothing until the `CLAUDE.md` rules and agent
  invocations reference it. Plan W4's output to feed those updates.
- **Migration is not part of this playbook.** Resist the urge to start
  moving files as design clarifies. That's scope creep and violates
  Session Discipline rule 1 (build, don't organize).
- **Don't try to design for every future app brain.** Design for the
  four that exist (canary, cove, angel, seacove) plus a clear
  extension story. Over-generalizing now locks in the wrong
  abstractions.
- **`raw/inbox/` is a special case.** It's where intakes land before
  classification. Proposal: it lives in ops by default, gets retagged
  when synthesized. Document this; don't let it be ambiguous.
- **Katz lesson — be willing to version.** The SDD being "v1.0 Final"
  does not mean it's right forever. It means it's locked enough to
  build against. v1.1 and v2 will happen.

---

## What we already know (initial recon)

From reading `Brain/projects/Method.md` and GRO-520:

- Brain has ≥6 top-level subtrees today (`projects/`, `wiki/`,
  `method/`, `templates/`, `raw/inbox/`, `daily/`, probably more).
- Method MOC uses six categories (Models, Roles, Techniques, Work
  Products, Activities, Communication Documents). These map *within* a
  brain, not across brains — the federation layer sits above them.
- `content-engine/` has a registry DB. Whether it currently supports
  scope tags is the question W6 needs to answer.
- GRO-520's open questions already surface three of the workstreams
  above (registry scope, cross-brain backlinks, personal-as-separate-vault).
  Treat them as required answers, not optional.

---

## Related Linear context

- **GRO-520** — parent. Document hierarchical Brain architecture.
  Currently Backlog, Medium. Bump to High on kickoff.
- **GRO-496** — Distill manifesto + warchest into wiki articles.
  Complementary knowledge-distillation work; may produce content that
  needs layer classification.
- **GRO-144** — Ops Dashboard (done). Example of cross-brain content:
  the dashboard spec is ops; its implementation is Canary.
- **Factory Pipeline SDD** — sibling document. The federation SDD
  should match its depth and format.

---

## Sizing

**Level A (spec-only, recommended):**

- Phase 1 (Assess): 2-3 hours
- Phase 2 (Compile inputs): 1 hour
- Phase 3 (8 workstreams): 1-2 hours each, parallelizable across
  sessions, ~8-16 hours total
- Phase 4 (SDD draft): 3-4 hours
- Phase 5 (Migration mapping): 2-3 hours
- Phase 6 (Review & lock): 2-3 hours (spread across 2 sessions with
  the overnight gap)
- Phase 7 (Cleanup): 30 min
- **Total: 3 sessions minimum, 5 comfortable.**

**Level B (+ tooling prototype):** add 1-2 sessions for manifest
validator + registry scope-tag experiment.

**Level C (+ Canary pilot):** add 2-3 more sessions to migrate Canary
end-to-end and validate the migration story.

---

## Success criteria (how we know Phase 6 is done)

- [ ] An external reader (Claude in a future session with no memory of
      this design) can read the SDD and correctly classify a new note
      into personal / ops / app on the first try.
- [ ] Every existing `Brain/*` top-level directory has a declared
      target layer.
- [ ] Every open question in GRO-520 is either answered in the SDD or
      explicitly parked in Section 11.
- [ ] The SDD is version-stamped v1.0 Final and committed.
- [ ] GRO-520 is closed. Migration issue is parked with a reference to
      the SDD.
- [ ] No files have been moved. (Yes, this is a success criterion.)
