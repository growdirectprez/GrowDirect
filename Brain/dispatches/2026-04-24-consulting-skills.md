---
type: dispatch
status: ready-to-paste
target: Linear (team GRO)
author: Geoffrey C. Lyle
date: 2026-04-24
related:
  - Brain/projects/Method.md
  - Brain/wiki/methodology-ibm-retail-diagnostic.md
  - Brain/wiki/methodology-ibm-it-architecture-options.md
  - docs/sdds/consulting/SDD-consulting-skills.md
---

# Dispatch — Consulting Skills (IBM BCS Lineage)

**Why this exists.** Two IBM Business Consulting Services deliverables from 2006 —
*Clarks Retail Diagnostic* and *Morrisons IT Architecture Options* — encode a
consulting methodology Geoffrey wants to own as a toolset. These become two
Cowork/Claude Code skills under `consulting:*` so any retailer engagement can
plug in and get the same shape of deliverable, fast. This dispatch logs them
as Linear issues under a parent initiative, with the Factory stages already
assigned.

**Read before working these:** [[Brain/wiki/methodology-ibm-retail-diagnostic|Methodology · IBM Retail Diagnostic]] · [[Brain/wiki/methodology-ibm-it-architecture-options|Methodology · IBM IT Architecture Options]] · [[docs/sdds/consulting/SDD-consulting-skills|SDD · Consulting Skills]].

---

## Parent initiative

**Title:** Consulting Toolset — IBM BCS Methodology Skills

**Description:**
Codify two consulting methodologies into reusable Cowork skills so GrowDirect
can plug into a retailer's evidence (financials, POS, systems inventory) and
produce a Retail Diagnostic or IT Architecture Options deliverable with the
same structural rigor IBM BCS delivered in 2006. Source material: two Final
v1.0 decks (Clarks, Morrisons). Author of record: Geoffrey C. Lyle. Artifact
preserved in `Brain/wiki/methodology-ibm-*.md` and
`docs/sdds/consulting/SDD-consulting-skills.md`.

**Labels:** `platform`, `skills`, `consulting`, `ip-provenance`
**Milestone:** Consulting skills v1 — ready for dogfood
**Target:** Q2 2026

---

## Issue 1 — `consulting:retail-diagnostic` skill

**Title:** Build `consulting:retail-diagnostic` skill (Clarks-pattern)

**Labels:** `skill`, `consulting`, `factory-pipeline`
**Priority:** Medium
**Estimate:** 5 pts
**Owner (proposed):** Jess (documentation) + Tom (architecture review)
**Parent:** Consulting Toolset initiative (above)

**Description:**

Implement the Clarks Retail Diagnostic methodology as an executable skill at
`plugins/consulting/skills/retail-diagnostic/SKILL.md`. Skill produces a 7-section
diagnostic deck from client evidence using the IBM BCS 2006 frame:

1. Executive Summary (full deck in miniature)
2. Background, Scope & Approach
3. Financial Analysis & Industry Drivers
4. Theme 1 — Findings & Observations (drill per root-cause)
5. Theme 2 — Findings & Observations (same pattern)
6. Opportunity Priorities & Roadmap (2×2 prize vs. cost/complexity)
7. Prioritised Case for Action (Phase 1/2/3 timeline)

**Acceptance criteria:**
- `SKILL.md` triggers on "retail diagnostic", "financial baseline for retail",
  "find the prize in this retailer", "prioritized retailer roadmap"
- Includes the per-theme drill template: Overview → Findings (per root cause,
  left column) + Leading Practice (right column) + 3 bold callouts →
  Recommendations block → prize sizing table (£ low/high range)
- Produces outputs in both docx and pptx (pptx preferred; IBM decks are native)
- Companion Brain wiki `methodology-ibm-retail-diagnostic.md` is referenced
  in the skill and renders the exact slide skeleton
- Validated by running against a synthetic retailer evidence pack and
  comparing output structure to the original Clarks deck

**Dependencies:**
- Depends on SDD approval (see Issue 3 below, if separate issue filed; or
  SDD-consulting-skills.md already drafted)
- Uses anthropic-skills: `pptx`, `docx`, `pdf`, `xlsx` (xlsx for the prize
  sizing table)

**Factory stages:**
- Preflight → SDD review (Tom)
- Blueprint → Skill interface design (Jess)
- Assembly → Write `SKILL.md` + supporting templates + prompt
- Verify → Run against synthetic retailer evidence; structural diff vs. Clarks
- Ship → Commit skill; update skills index in Method MOC
- Close → Dispatch back to Geoffrey with usage log

---

## Issue 2 — `consulting:it-architecture-options` skill

**Title:** Build `consulting:it-architecture-options` skill (Morrisons-pattern)

**Labels:** `skill`, `consulting`, `factory-pipeline`
**Priority:** Medium
**Estimate:** 5 pts
**Owner (proposed):** Tom (architecture) + Jeremy (build)
**Parent:** Consulting Toolset initiative (above)

**Description:**

Implement the Morrisons IT Architecture methodology as an executable skill at
`plugins/consulting/skills/it-architecture-options/SKILL.md`. Skill produces a
multi-option architecture evaluation deck using the IBM BCS 2006 frame:

1. Introduction
2. Programme targets (margin / overhead / headcount / sales / profit)
3. Business Requirements (Sell / Plan / Move / Buy process frame)
4. Implications for Legacy Systems
5. Option A — Legacy Enhancement (7-slide skeleton below)
6. Option B — Best-of-Breed Package
7. Option C — Integrated Package
8. Summary and Conclusion (side-by-side comparison)

**Per-option slide skeleton:**
- Application architecture heat-map vs. Optimisation processes (4-color legend)
- Same heat-map vs. Aspirational/future-state processes
- Development effort estimate (design/build-test/rollout days → man-years)
- Target application architecture (post-change)
- Advantages / Disadvantages
- Implementation timeline and risk
- Resource / sourcing plan

**Acceptance criteria:**
- `SKILL.md` triggers on "evaluate IT options", "legacy vs. package decision",
  "architecture options for retailer", "buy vs. enhance vs. replatform"
- Produces pptx output matching option-skeleton structure
- Companion Brain wiki `methodology-ibm-it-architecture-options.md` is
  referenced and renders the slide skeleton
- Validated against a synthetic inventory of a retailer's application
  landscape; structural diff vs. Morrisons deck
- Output includes the side-by-side summary matrix in final section

**Dependencies:**
- Depends on SDD approval
- Depends on `consulting:retail-diagnostic` shared utilities (Sell/Plan/Move/Buy
  process frame is shared; factor into `consulting/_shared/` if pattern emerges)

**Factory stages:** same as Issue 1.

---

## Notes for the Linear-user (Geoffrey)

1. Paste the parent initiative first to get an initiative ID.
2. Create Issue 1 and Issue 2 as children; set the parent.
3. Link both issues to the SDD at
   `docs/sdds/consulting/SDD-consulting-skills.md` (not in Linear — in the
   repo; paste the path in the description as a relative link).
4. The methodology wikis are already in Brain; they will auto-render via
   Obsidian graph links.
5. Cross-link: add both issues to the Method MOC under Techniques Index
   once they have IDs (GRO-XXX).

**When Linear MCP reconnects:** I can post these directly as `mcp__a018de2b-*__save_issue` calls rather than paste. For now this is dispatch-ready copy.

---

## Files produced by this dispatch

- `dispatches/2026-04-24-consulting-skills.md` (this file)
- `Brain/wiki/methodology-ibm-retail-diagnostic.md`
- `Brain/wiki/methodology-ibm-it-architecture-options.md`
- `docs/sdds/consulting/SDD-consulting-skills.md`
- `plugins/consulting/plugin.json`
- `plugins/consulting/README.md`
- `plugins/consulting/skills/retail-diagnostic/SKILL.md`
- `plugins/consulting/skills/it-architecture-options/SKILL.md`
- Full-text source extracts (binary working dir only; do not commit):
  `outputs/Clarks Retail Diagnostic - Final v 1.0.full.txt`
  `outputs/Morrisons.IT Architecture.Final Deliverable.v1.0.full.txt`

## Plugin decision (new — 2026-04-24)

After initial scaffolding under `.claude/skills/`, the target moved to
`plugins/consulting/` per your observation ("feels like those could be
plugins"). The plugin structure is now authoritative. To formalize and
publish, the next step is:

```
Skill(cowork-plugin-management:create-cowork-plugin)
  → point at plugins/consulting/
  → produces a .plugin file ready for install
```

Or, for targeted customization per client engagement:

```
Skill(cowork-plugin-management:cowork-plugin-customizer)
  → tune triggers, templates, taxonomy for a specific retailer vertical
```
