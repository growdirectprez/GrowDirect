---
type: scratch
status: phase-1-output
tags: [brain-federation, gro-520, assessment, scratch]
created: 2026-04-23
playbook: docs/playbooks/playbook-brain-scaffold-design.md
dispatch: docs/dispatches/dispatch-brain-scaffold-design.md
---

# Brain Federation — Phase 1 Assessment (v1)

Phase 1 deliverable per `docs/playbooks/playbook-brain-scaffold-design.md`. Scratch
artifact — deletes at Phase 7. Feeds the Federation SDD as cited evidence.
Two pages, not a design. Observations only.

---

## Inventory

| Top-level | Files | `.md` | Notes |
|-----------|-------|-------|-------|
| `attachments/` | 1 | 0 | `.gitkeep` only. Infrastructure anticipated, unused. |
| `decisions/` | 1 | 0 | `.gitkeep` only. Infrastructure anticipated, unused. |
| `journal/` | 1 | 0 | `.gitkeep` only. **No personal journal content exists.** |
| `method/` | 7 | 7 | Activities, CommDocs, Models, Orchestration, Roles, Techniques, WorkProducts. |
| `playbooks/` | 1 | 1 | `neighborhood-content.md` only. Unexpected — most playbooks live in `docs/`. |
| `projects/` | 9 | 8 | Eight project MOCs + `.DS_Store`. Angel, Canary, Cove, Factory, GrowDirect, Method, Seacove, Secure. |
| `raw/` | 1365 | 81 | Bulk of filesystem weight. See raw/ breakdown below. |
| `templates/` | 7 | 7 | card, claim, daily-note, decision, meeting, raw-intake, wiki-article. |
| `wiki/` | 222 | 221 | **Flat namespace**, prefix-as-scope. See wiki/ breakdown below. |
| *root* | 4 | 3 | `Home.md`, `Brain Health Dashboard.md`, `Setup Guide.md`, `REGISTRY.json` (1.5MB). |

**raw/ subtree:**

| Path | Total | `.md` | Binaries |
|------|-------|-------|----------|
| `raw/clips/` | 1 | 0 | 1 |
| `raw/inbox/` | 1,348 | 68 | **1,280** |
| `raw/meetings/` | 1 | 0 | 1 |
| `raw/processed/` | 13 | 13 | 0 |
| `raw/research/` | 1 | 0 | 1 |

`raw/inbox/` contains 15 named engagement archives: *Katz, Harrods,
Heartbeat, CRDMSearchableBuilder, Case Management Documentation,
Documents, GAP, Other Retek Decks, RDM V 10.3, RMS Replen Training,
RPAS Client, SRD, TOM Top Down Design 9 July, Technical Library.*
Third-party consulting artifacts — most are binaries not yet extracted.

**wiki/ prefix distribution (informal scope tags):**

| Prefix | Count | Observation |
|--------|-------|-------------|
| `growdirect-` | 86 | Largest cluster. Mixes ops-public (manifesto, glossary, factory-process) with ops-private (patent visuals, warchest, fee-window, attack-plan, founders-case). |
| `angel-` | 37 | App brain (clean fit). Includes 20+ neighborhood-* raw content-pool articles. |
| `cove-` | 31 | App brain (clean fit). Governance + geology + legal. |
| `coac-` | 18 | Cove-adjacent governance (reactivation, trustee slate, yimby opposition, restated declaration). |
| `foundation-` | 10 | 501(c) legal/structural content. Legal framework, crypto donations, compensation. |
| `card-` | 9 | Local business cards (peninsula creameries, coaches, surf camps). Angel content pool. |
| `secure-` | 6 | Archived retail LP engagement content. |
| `canary-` | 6 | App brain (clean fit). Architecture, detection, alerts, sales strategy. |
| `wpbca-` | 5 | Cove-adjacent HOA board content. |
| `peninsula-` | 5 | Angel content pool. |
| `seacove-` | 3 | App brain. |
| `abalonecove-`, `501c-`, `south-`, `claim-`, `document-` | 5 total | Singletons or near-singletons. |

Frontmatter is consistent: 216 files declare `type: wiki`, 4 `type: moc`,
1 `type: claim`. Tags are freeform lists. Projects MOCs declare
`type: project-moc` + `status` (active / beta / development / operational
/ archive-active).

---

## Cross-references

Link-style audit across `wiki/`:

- **Bare style** `[[name]]` — **707 instances**
- **Full-path style** `[[Brain/path|alias]]` — **726 instances**
- **Cross-repo** `[[Cove/...]], [[Canary/...]], [[Angel/...]], [[Seacove/...]]` — **217 instances**

The bare/full split is roughly 50/50 and appears to vary by article rather
than by convention. Federation will break bare links across brain
boundaries unless they are either (a) resolved within a single index at
query time or (b) migrated to full-path form. **Material decision for W4.**

Sample cross-layer evidence from 10-article sample:

- `wiki/claim-lot-h-scope-correction.md` links to six `Cove/docs/admin/...`
  briefs and `Cove/docs/archive/originals/...` primary sources. This is
  legitimate cross-repo reference — knowledge in Brain points at app-repo
  evidence. Federation must preserve this, not forbid it.
- `wiki/coac-15-owner-network.md` links to 11 other nodes across
  `coac-*`, `501c-*`, `foundation-*`, `wpbca-*`. All Cove-governance-adjacent
  but with distinct prefixes — **strong evidence that prefix is already
  functioning as a scope tag** and the federation can mostly codify what
  is already informally present.
- `wiki/card-coach-ken-taylor.md` links to `[[Brain/Home|Home]]` — the root
  `Home.md`. A root-level landing page that cross-layer content points to
  needs its own federation-era answer.
- `wiki/coac-2026-civic-problems-memorandum.md` links to
  `[[feedback_ocean_easement_sensitive]]` — a link target that **does not
  exist as a file**. Dead link. The filename stem itself asserts
  sensitivity; suggests an intent to create redacted content.

Customer / vendor name spread across `wiki/`:

| Term | Articles | Layer implication |
|------|----------|-------------------|
| Appriss | 11 | Secure archive — ops or archive layer |
| IBM | 10 | Secure archive |
| Sysrepublic | 10 | Secure archive |
| Walmart | 7 | Canary lineage material |
| Kroger | 6 | Secure archive |
| Harrods | 1 | Archived engagement |
| Katz | 0 | Archive content is mostly in `raw/inbox/Katz/`, not yet synthesized |

---

## Exposure audit

Content types that should not leave the vault under any publication path:

1. **Patent-visual and patent-architecture material** (`growdirect-patent-*`).
   Pre-grant IP disclosure risk. At least 3 articles.
2. **Warchest / genesis-pool / fee-window / DAO treasury protocol**
   (`growdirect-warchest*`, `growdirect-dao-treasury-protocol.md`,
   `growdirect-genesis-pool.md`, `growdirect-fee-window.md`). Financial
   structure pre-public.
3. **Attack plan / first-mover / founders case** (`growdirect-attack-plan.md`,
   `growdirect-first-mover.md`, `growdirect-founders-case.md`). Investor-
   and litigation-sensitive framing.
4. **Foundation legal framework + crypto donations** (`foundation-legal-framework.md`,
   `foundation-crypto-donations.md`, `foundation-three-hat-compensation.md`,
   `foundation-llc-rescue-status.md`). Real legal structure; pre-filed material.
5. **COAC governance positioning** (`coac-yimby-opposition-landscape.md`,
   `coac-trustee-slate-preparation.md`, `coac-restated-declaration-blitz-plan.md`,
   `coac-rpv-scotus-petitions.md`). Live political posture in an active
   HOA/civic dispute. Not for public exposure while disputes are live.
6. **Consulting engagement archives** (`raw/inbox/Harrods/`, `Heartbeat/`,
   `Katz/`, `Secure/GAP/`, `RPAS Client/`, etc.). Third-party material,
   possibly NDA-covered. Some ages back 20+ years; status unclear but
   default posture: internal only.
7. **Third-party vendor/customer names** in wiki prose — Appriss, IBM,
   Sysrepublic, Kroger, Walmart. Exist in ~20+ wiki articles as
   lineage/context. Some of this is publishable (Canary-lineage
   narrative); some is not (named Kroger engagement details).

No credentials, tokens, or passwords found in filename scan. Full grep
not performed this phase — flag for W5 as a required check during
migration, not pre-design.

`journal/` is empty — **no current personal-layer content in Brain**.
All current content is some flavor of ops or app. This matters: the
personal layer today is aspirational; the hard problem is
**decomposing the monolithic `wiki/`**, not carving out journals.

---

## First impressions

1. **The federation is already informally present** — prefix-as-scope
   (`angel-*`, `canary-*`, `cove-*`, `coac-*`, `foundation-*`, etc.)
   means migration is ~80% mechanical: move each prefix into a subtree,
   update link format, publish a manifest. Design should codify what
   already works, not re-invent.

2. **The `growdirect-*` cluster (86 files) is the hardest classification
   problem.** It's not one layer. It contains ops-public (manifesto,
   glossary, factory-process), ops-private (patent, warchest, investor
   thesis), and ops-sensitive (attack-plan, founders-case, patent
   visuals). W1 (taxonomy) must not treat "ops" as monolithic — needs
   a **publishable / internal / private** sub-axis within ops, or a
   distinct "founder" layer for pre-public IP/financial content.

3. **Link-style inconsistency is a pre-existing debt.** 707 bare vs 726
   full-path is not by design — it accumulated. Federation forces a
   decision. Cheapest path: normalize to full-path `[[brain_id:path|alias]]`
   as part of migration, not as a separate effort.

4. **Cross-repo links are load-bearing.** 217 `[[Cove/...]]` / `[[Canary/...]]`
   links mean Brain content is already coupled to app-repo content.
   Federation cannot treat apps as black boxes — the Cove brain needs
   to reference `Cove/docs/...` and that must survive migration.

5. **`raw/inbox/` dominates filesystem weight** (1,348 files, mostly
   binaries). None of this is "Brain" in the synthesized sense — it's
   primary source material awaiting ingestion. Exposure policy must
   treat `raw/inbox/` differently from `wiki/`; probably it lives at
   ops-layer by default and is explicitly never published. Consistent
   with the ingestion pipeline pattern.

6. **Templates, method MOCs, and project MOCs are the operating system
   of Brain** — they're small (22 files total across `templates/`,
   `method/`, `projects/`) but every piece of `wiki/` references them.
   These are the most unambiguously "ops" content in the vault and
   the most natural migration pilot.

7. **Personal, decisions, attachments are infrastructure-only.** Three
   `.gitkeep` directories with no content suggest the original author
   anticipated these layers but never used them. Federation v1 can
   either (a) formalize them in the new layout or (b) remove them and
   re-introduce at v1.1 when actual content appears. Leaning (a) —
   empty slots with a manifest are cheap and prevent silent drift.

8. **Two named playbook artifacts are already in `docs/`, not
   `Brain/`.** The dispatch/playbook for this very engagement live in
   `docs/`. The existing `Brain/playbooks/` folder has one unrelated
   file. Federation should resolve: are playbooks Brain content
   (method-layer knowledge) or repo content (working docs)?

9. **Dead link found:** `[[feedback_ocean_easement_sensitive]]`
   referenced but not present. Flag for cleanup during migration. Likely
   one of many — full dead-link scan should happen at W2/W5.

10. **No blocker surfaced that requires return to owner per dispatch
    check-in rules.** No active exposure leak detected. No content
    confirms scope-tag already exists in registry. Proceed to Phase 2
    compilation in next session.

---

## Open questions accumulated (for SDD §11)

- Does `growdirect-*` split into ops-publishable + ops-private, or does
  "private" become a distinct founder/owner layer above ops?
- Where do playbooks live — `Brain/method/` (as executable technique) or
  `docs/` (as working operational doc)? Current state is split.
- Does `Brain/Home.md` (root landing) survive federation as-is, or
  become a per-brain index page?
- Cross-repo links today go to `Cove/docs/...`, `Canary/docs/...`. In
  federation, does the brain reference the app-repo path directly or
  does the app publish its own brain with its own manifest?
- `raw/inbox/` — one shared inbox fed by the intake protocol, or one
  inbox per brain? If shared, how does synthesis route to the right
  brain?
- `Brain/REGISTRY.json` (1.5MB) — single federated index, or per-brain
  index files that compose? W6 decision but Phase 1 surfaced the size.
- Empty `.gitkeep` dirs (attachments/decisions/journal): formalize or
  remove?

---

## Numbers summary

- Total files in `Brain/`: ~1,612
- Total markdown: 338 (wiki 221 + raw 81 + method 7 + projects 8 + templates 7 + playbooks 1 + root 3 + ~10 assorted)
- Binary content concentrated entirely in `raw/inbox/` (1,280 files, 15 engagement archives)
- Wiki prefix clusters implying natural federation boundaries: 13 distinct prefixes
- Cross-layer evidence: 707 bare links, 726 full-path links, 217 cross-repo links
- Top-level empty-infrastructure dirs: 3 (`attachments/`, `decisions/`, `journal/`)

Phase 1 complete. Stopping per dispatch.
