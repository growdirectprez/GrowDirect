# NCR Vault — Framework Wiring Design

**Date:** 2026-04-27  
**Status:** Draft  
**Scope:** Wire `GrowDirect-NCR` into the GrowDirect three-vault architecture as a first-class companion vault

---

## Executive Summary

`GrowDirect-NCR` (`ncr.growdirect.io`) is the first vendor-specific companion vault — a curated projection of GrowDirect Brain content shaped for NCR Counterpoint VARs. The vault is deployed and content-complete, but it is not yet wired into the agent and knowledge infrastructure. This spec defines the work to close that gap: memory bus freshness, Brain coverage verification, Brain back-fill where needed, and agent context files in both the NCR repo and the platform CLAUDE.md.

---

## Context

### Three-Vault Architecture

| Vault | Domain | Audience | Status |
|---|---|---|---|
| `GrowDirect-CATz` (`catz.growdirect.io`) | Co-sell toolkit | Partners, prospects | Deployed, wired |
| `GrowDirect-CRB` (`crb.growdirect.io`) | Canary Retail Brain | Internal + partners | Deployed, wired |
| `GrowDirect-NCR` (`ncr.growdirect.io`) | Canary for NCR Counterpoint | NCR Counterpoint VARs | Deployed, **not wired** |

All three vaults are curated exports of `GrowDirect/Brain/wiki/`. GrowDirect is the factory; the companion vaults are the publications. Memory seeding, agent context, and source-of-truth authority all live in GrowDirect. The companion vaults are never edited directly — Brain is.

### Memory Bus State

- 402 seed embeddings, last seeded 2026-04-26 22:07 UTC
- Layers: 372 corp (Brain/wiki, SDDs, team), 28 canary, 2 shared
- NCR vault content: not seeded directly (correct — source is Brain)
- Brain/wiki additions since April 26 are not yet indexed

---

## Design

### Deliverable 1 — Memory Bus Re-seed

**What:** Re-run `seed_clean.py --drop-first` inside the `growdirect_memory_bus` container to pick up all Brain/wiki and SDD additions since April 26.

**Why:** The seed script already covers all the right paths (`Brain/wiki/*.md`, `docs/sdds/**/*.md`, `Brain/dispatches/*.md`). No changes to the seed manifest are needed. This is a pure freshness operation.

**How:**
```bash
docker exec growdirect_memory_bus python3 scripts/seed_clean.py --drop-first
```

**Success criterion:** Command exits 0 and the post-seed embedding count is ≥ 420 (current 402 + at minimum the ~20 Brain/wiki articles known to have been added or updated since April 26). If count stays at 402, the drop-first did not pick up new files — investigate before proceeding.

**Note:** `--drop-first` briefly empties the embeddings table during the run. Do not run this while another agent session is actively querying the memory bus — recall results will be empty until the seed completes.

---

### Deliverable 2 — NCR Vault Gap Analysis

**What:** Cross-reference each NCR vault section against Brain/wiki coverage. Produce a gap ledger with three outcomes per section:

| Outcome | Meaning | Action |
|---|---|---|
| **Covered** | Brain wiki article exists and aligns | None — re-seed picks it up |
| **Forward-only** | Content is audience-specific (VAR pitch, co-sell framing) with no generic Brain equivalent | Note it; no back-fill needed |
| **Missing** | NCR vault has substantive content with no Brain backing | Back-fill required (Deliverable 3) |

**NCR vault sections to audit** — all files in each section must be checked, including index files:

| NCR Section | Files to audit | Known Brain backing |
|---|---|---|
| `agents/` | architecture, vsm, roadmap, index | `growdirect-viewpoint-virtual-store-manager.md` (partial) |
| `modules/` | D, W, Q-loss-prevention, Q-loss-prevention-rule-catalog, N, EJ, F, C, L, P, J, S, R, T, A, index | `canary-module-*` functional decomps; `ncr-counterpoint-document-model.md` |
| `ncr-context/` | index | `ncr-counterpoint-phase-0-context-brief.md` (verify slug); `voyix-counterpoint-rapid-pos-engagement-context.md`; `ncr-counterpoint-rapid-pos-relationship.md` |
| `integration/` | index | `ncr-counterpoint-api-reference.md`; `ncr-counterpoint-endpoint-spine-map.md`; `ncr-counterpoint-connection-runbook.md`; `ncr-counterpoint-document-model.md` |
| `deployment/` | index | `engagement-shape-100-day-deployment.md` (candidate — audit alignment before confirming covered) |
| `verticals/` | lawn-garden, armstrong, feed-tack, beverage, gun, wine-spirits — **all 6 must be audited** | `garden-center-operating-reality.md`; `socal-home-garden-target-customers-brief.md`; `bart-mccleskey-rapid-garden-pos.md`; `rapid-pos-counterpoint-market-research-tam.md`; `rapid-pos-counterpoint-user-pain-points.md` |
| `sandbox/` | index | `ncr-counterpoint-sandbox-setup-checklist.md` |
| `why-canary/` | index | `canary-raas-positioning.md`; `canary-sales-strategy.md`; `bart-mccleskey-rapid-garden-pos.md`; `rapid-pos-counterpoint-user-pain-points.md` |
| `pitch/` | index | **Forward-only** — VAR leave-behind, intentionally external |
| root | `canary-data-model.md` (top-level file, not in a subdirectory) | `canary-data-model.md` in Brain/wiki — verify alignment |

**Output:** Gap ledger persisted as a Brain wiki article at `Brain/wiki/ncr-vault-gap-ledger.md`. This is a decision record (what has Brain backing, what is forward-only, what was back-filled) and must survive the session per session discipline rule #9. Format: table with columns `NCR Section | File | Brain Article | Outcome | Notes`.

---

### Deliverable 3 — Brain Back-fill

**What:** For each **Missing** item from the gap ledger, write a Brain wiki article at `GrowDirect/Brain/wiki/<slug>.md`.

**Scope guard:** Back-fill covers substantive technical and operational content (deployment patterns, integration architecture, vertical playbooks). It does not back-fill forward-only audience-specific materials (pitch decks, VAR co-sell framing).

**Quality bar per article:** Use the Brain wiki template at `Brain/templates/` if one exists for the content type. Minimum required sections: frontmatter (`title`, `tags`), a one-paragraph purpose statement, and the substantive content. Follow naming conventions already established: `ncr-counterpoint-*` prefix for NCR-specific articles, `canary-*` for Canary platform content.

**After back-fill:** Re-run `seed_clean.py --drop-first` (step 5 in the sequence) to index the new articles. Success criterion for that run: embedding count increases by at least the number of new articles written. Skip if gap analysis found no Missing items.

---

### Deliverable 4 — Agent Context Files

#### 4a. `GrowDirect-NCR/CLAUDE.md`

A CLAUDE.md in the NCR repo root (`/Users/gclyle/GrowDirect-NCR/CLAUDE.md`) establishing the source relationship for any agent landing in that directory.

**Required content:**
- What this repo is: vendor-specific companion vault, curated projection of GrowDirect Brain
- Source of truth: `GrowDirect/Brain/wiki/` — never edit content here directly
- Audience: NCR Counterpoint VARs (Rapid POS and others)
- How to update: write/update the Brain wiki article → re-seed memory bus → update the NCR vault file to match
- Build: `python3 build.py` → `_site/` → GitHub Pages deploys on push to `main` (build.py confirmed present in repo root)
- Key Brain articles backing this vault: list the `ncr-counterpoint-*` and relevant `canary-module-*` slugs

#### 4b. Platform `GrowDirect/CLAUDE.md` — Projects Section Update

The platform CLAUDE.md has a `## Projects` section with a four-column table (`Project | Directory | Status | What it is`). Read this section first to match the existing column format and voice.

Two changes:
1. Add a row for `GrowDirect-NCR` to the Projects table: `| NCR Companion Vault | ~/GrowDirect-NCR/ (sibling repo) | Active | Vendor-specific Canary co-sell site for NCR Counterpoint VARs. Projection of Brain/wiki/ content. |` — note the directory column uses `~/GrowDirect-NCR/` to signal it is a sibling repo at the same level as GrowDirect/, not a subdirectory. Future agents reading the table must not assume it lives inside GrowDirect/.
2. Add a `### Companion Vaults` subsection immediately after the Projects table noting: all three companion vaults (CATz, CRB, NCR) are curated Brain projections published at `*.growdirect.io`. Never edit companion vault content directly — update Brain, re-seed the memory bus, then push the vault file. NCR is the first vendor-specific vault; future vendor vaults follow the same pattern.

---

## Sequence

```
1. seed_clean.py --drop-first              (freshness baseline — run first)
2. Gap analysis: audit NCR vault vs Brain  (read NCR vault files, check Brain/wiki)
3. Write gap ledger to Brain/wiki/ncr-vault-gap-ledger.md
4. Back-fill missing Brain wiki articles   (skip if gap analysis finds no Missing items)
5. seed_clean.py --drop-first              (index back-fill; skip if step 4 was skipped)
6. Write GrowDirect-NCR/CLAUDE.md
7. Update GrowDirect/CLAUDE.md Projects section
8. Commit GrowDirect repo (Brain back-fill + gap ledger + platform CLAUDE.md update)
9. Commit GrowDirect-NCR repo (CLAUDE.md)
```

Steps 1 and 2 can run concurrently, but the step 1 success criterion (count ≥ 420) must pass before committing any outputs — if re-seed fails, investigate before proceeding. Steps 6 and 7 are independent of 1–5 and can run in parallel with the gap/back-fill work. Step 7 adds the NCR row unconditionally — it documents the vault exists and is being wired, not that wiring is complete. Steps 8 and 9 are separate commits to separate repos.

---

## Out of Scope

- Changes to the seed manifest (no new source paths needed)
- Changes to memory bus infrastructure
- Formalizing the vendor vault pattern as a reusable method (deferred — do this after running the pattern once)
- CATz or CRB gap analysis (separate session if needed)
- NCR vault content authoring (content is already in place)
