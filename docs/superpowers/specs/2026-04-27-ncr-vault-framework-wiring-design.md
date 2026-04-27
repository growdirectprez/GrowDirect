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

**Success criterion:** Command completes without errors; embedding count increases above 402.

---

### Deliverable 2 — NCR Vault Gap Analysis

**What:** Cross-reference each NCR vault section against Brain/wiki coverage. Produce a gap ledger with three outcomes per section:

| Outcome | Meaning | Action |
|---|---|---|
| **Covered** | Brain wiki article exists and aligns | None — re-seed picks it up |
| **Forward-only** | Content is audience-specific (VAR pitch, co-sell framing) with no generic Brain equivalent | Note it; no back-fill needed |
| **Missing** | NCR vault has substantive content with no Brain backing | Back-fill required |

**NCR vault sections to audit:**

| NCR Section | Key files | Likely Brain backing |
|---|---|---|
| `agents/` | architecture, vsm, roadmap | `growdirect-viewpoint-virtual-store-manager.md` (partial) |
| `modules/` | D, W, Q, N, EJ, F, C, L, P, J, S, R, T, A | `canary-module-*` functional decomps |
| `ncr-context/` | index | `ncr-counterpoint-phase-0-context-brief.md`, `voyix-counterpoint-rapid-pos-engagement-context.md` |
| `integration/` | index | `ncr-counterpoint-api-reference.md`, `ncr-counterpoint-endpoint-spine-map.md`, `ncr-counterpoint-connection-runbook.md` |
| `deployment/` | index | Likely **missing** — no direct Brain equivalent found |
| `verticals/` | feed-tack (+ others in dev) | `garden-center-operating-reality.md`, `socal-home-garden-target-customers-brief.md` (partial) |
| `sandbox/` | index | `ncr-counterpoint-sandbox-setup-checklist.md` |
| `why-canary/` | index | `canary-raas-positioning.md`, `canary-sales-strategy.md` |
| `pitch/` | index | **Forward-only** — VAR leave-behind, intentionally external |

**Output:** Gap ledger written as a section in the session notes; not a persistent file.

---

### Deliverable 3 — Brain Back-fill

**What:** For each **Missing** item from the gap analysis, write a Brain wiki article at `GrowDirect/Brain/wiki/<slug>.md` using standard Brain wiki format.

**Naming convention:** Follow the `ncr-counterpoint-*` prefix already established in Brain for NCR-specific content.

**Scope guard:** Back-fill covers substantive technical and operational content (deployment patterns, integration architecture, vertical playbooks). It does not back-fill forward-only audience-specific materials (pitch decks, VAR co-sell framing). Those live only in the NCR vault and are not seeded.

**After back-fill:** Re-run the memory bus seed to index the new articles.

---

### Deliverable 4 — Agent Context Files

#### 4a. `GrowDirect-NCR/CLAUDE.md`

A CLAUDE.md in the NCR repo root establishing the source relationship for any agent landing in that directory.

**Contents:**
- What this repo is (vendor-specific companion vault, curated projection of GrowDirect Brain)
- Source of truth: `GrowDirect/Brain/wiki/` — never edit content here directly
- Audience: NCR Counterpoint VARs
- How to update: write or update the Brain wiki article, re-seed the memory bus, then sync the relevant NCR vault file
- Build: `python3 build.py` → `_site/` → GitHub Pages auto-deploys via push

#### 4b. Platform `GrowDirect/CLAUDE.md` — Three-Vault Section Update

Add NCR to the existing three-vault architecture block. The update adds one row to the vault table and a note that NCR is the first instance of the vendor companion vault pattern (vendor-scoped CRB projection).

---

## Sequence

```
1. Run seed_clean.py --drop-first          (freshness baseline)
2. Gap analysis: audit NCR vault vs Brain  (identify missing)
3. Back-fill Brain wiki articles           (close missing gaps)
4. Run seed_clean.py --drop-first again    (index back-fill)
5. Write GrowDirect-NCR/CLAUDE.md
6. Update GrowDirect/CLAUDE.md three-vault section
7. Commit all changes
```

Steps 1 and 2 are independent. Steps 3–4 only run if gap analysis finds Missing items. Steps 5–6 are independent of 1–4 and can run in parallel.

---

## Out of Scope

- Changes to the seed manifest (no new source paths needed)
- Changes to memory bus infrastructure
- Formalizing the vendor vault pattern as a reusable method (deferred — do this after running the pattern once; see Option C from brainstorm)
- CATz or CRB gap analysis (separate session if needed)
- NCR vault content authoring (content is already in place)
