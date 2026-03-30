---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# WORK ORDER: PhD — Product_Sites Alignment Brief
**Dispatched by:** ALX (Chief of Staff)
**Date:** February 24, 2026
**Priority:** 🟡 HIGH — Blocks Jim and Jess dispatch (their work orders depend on this output)
**Mode:** COORDINATE (PhD owns the research and assessment; ALX routes the output)

---

## Assignment

Review the HTML library you've built in `Canary_IP/Documents/Product_Sites/` and produce a structured **Alignment Brief** that maps your work to the current PRD (E0-F6), the Design Spec, and the CRDM. This brief is the bridge between PhD's research output and the downstream team — Art (wireframe in progress), Jim (QA scenarios), and Jess (Functional + Technical Companion Guides).

**Why this matters:** You've produced 19 HTML files covering prototypes, specs, marketing positioning, data model architecture, Fox case management, forensic analysis, and more. Jim and Jess need to consume this work, but they need a guide — what's current, what's superseded, what maps to which PRD feature, and what's the authoritative source for each topic.

---

## Deliverable: PhD Alignment Brief

**Format:** Single markdown file
**Length:** Thorough but scannable — use tables, not prose walls
**Save to:** `GrowDirect/_ALX/WorkOrders/output/PhD/PhD_Alignment_Brief.md`

### Required Sections

#### 1. File Inventory with Currency Assessment

For each file in `Product_Sites/`, assess:

| File | Version | Date | Status | Superseded By | Notes |
|---|---|---|---|---|---|
| (filename) | v1.0/v2.0 | (date) | CURRENT / STALE / SUPERSEDED / REFERENCE ONLY | (newer file if applicable) | (one-line note) |

**Status definitions:**
- **CURRENT** — Reflects the latest state of the product/spec. Safe to reference.
- **STALE** — Was accurate when written but the product has evolved. Needs caveats.
- **SUPERSEDED** — A newer version exists. Do not reference this version.
- **REFERENCE ONLY** — Useful for context/history but not authoritative for current state.

#### 2. PRD E0-F6 Feature Mapping

Map your Product_Sites files to PRD E0-F6 sub-features:

| PRD Feature | Product_Sites Coverage | File(s) | Gaps / Misalignment |
|---|---|---|---|
| E0-F6-A: Today's View | (what your files show for this feature) | (which files) | (any differences from PRD spec) |
| E0-F6-B: Guided Wizard Engine | ... | ... | ... |
| E0-F6-C: Core Guided Processes 1–4 | ... | ... | ... |
| E0-F6-D: Contextual Scorecards | ... | ... | ... |

**Be specific about misalignment.** If the prototype shows 17 metrics on the home screen but the PRD says "max 3 action cards," call that out. If the module names differ (e.g., "Dog" in marketing site vs. "Rooster" in Design Spec), flag it. If a wizard flow is spec'd differently in the prototype than in the Design Spec Section 3, note the delta.

#### 3. CRDM Alignment

Compare your `Canary_CRDM_v2.0.html` and `Canary_CRDM_Mapping_Analysis_v1.0.html` against the canonical CRDM at `Canary_IP/Markdown/Specs/CRDM_v1.0.md`:

- What tables/entities are in CRDM v2.0 HTML that aren't in CRDM v1.0 markdown (or vice versa)?
- Are the three-database boundaries (canary_app, canary_sales, canary_metrics) consistent?
- Are Chirp rule definitions consistent between your HTML and the Design Spec?
- Are there any data source status changes (Ready/New/Warning/Missing) that affect what Art can show in the wireframe or what Jim can test?

#### 4. Architecture & Technical Alignment

Compare your technical files against Tom's B-001 session output and the current codebase state:

| Topic | PhD File(s) | Tom/Jeremy Source | Aligned? | Notes |
|---|---|---|---|---|
| Immutability model | JSONB Forensic Analysis, Platform Schema | Tom's P0-1/P0-2/P0-3 | Y/N | (deltas) |
| Fox case management | Fox Module Technical Spec | CRDM v1.0, Tom B-001 | Y/N | (deltas) |
| Three-database architecture | Platform Schema Complete | Tom B-001, Jeremy migrations | Y/N | (deltas) |
| Chirp rule engine | CRDM v2.0 HTML | Design Spec Section 3 | Y/N | (deltas) |
| The Dome / Lightning | PhD thesis Part IX | Design Spec Section 7 | Y/N | (deltas) |

#### 5. Recommended Reading List for Downstream Team

Produce a curated, prioritized reading list for each downstream consumer:

**For Art** (Today's View wireframe — already in progress):
- Which Product_Sites files should Art reference to ensure alignment?
- Any visual patterns, component structures, or interaction models Art should adopt or explicitly depart from?
- Specific callout: does the existing prototype (v2.0) align with or contradict the Design Spec's "guided, not dashboard" directive?

**For Jim** (QA scenarios):
- Which files contain testable workflows, forms, or user journeys?
- What data states, edge cases, or failure modes are visible in your specs?
- Fox Module spec — what case management scenarios should Jim write tests for?
- Incident Report Form — does it align with the Guided Wizard pattern from the Design Spec?

**For Jess** (Functional + Technical Companion Guides):
- Which files serve as source material for the Functional Guide (business positioning, merchant experience, problem/solution narrative)?
- Which files serve as source material for the Technical Guide (architecture, data model, security, Lightning infrastructure)?
- What content can Jess lift directly vs. what needs rewriting for the guide audience?
- Any terminology inconsistencies (module names, feature names, technical terms) that Jess should normalize?

#### 6. Terminology Reconciliation

Produce a terminology table resolving any naming inconsistencies across your files, the PRD, and the Design Spec:

| Concept | PhD Files Term | PRD/Design Spec Term | Canonical Term | Notes |
|---|---|---|---|---|
| (e.g., employee module) | "Dog" | "Rooster" | (which is correct?) | (context) |

This is critical — Jim and Jess cannot have different names for the same thing in their deliverables.

---

## Context Files (Read Before Starting)

| File | Path | Why |
|---|---|---|
| PRD E0-F6 | `Canary_IP/Documents/Product_Guides/Canary_PRD_E0F6_Guided_Companion_v1.0.docx` | **Authoritative source** — your output must align to this |
| Design Spec v1.0 | `Canary_IP/Markdown/Specs/Canary_Guided_Companion_Design_Spec_v1.0.md` | UX and interaction spec — Art is building from this |
| CRDM v1.0 (markdown) | `Canary_IP/Markdown/Specs/CRDM_v1.0.md` | Canonical data model |
| Tom's B-001 Output | `Canary_IP/Markdown/Alpha3X/output/TOM_SESSION_OUTPUT_B-001_2026-02-24.md` | Latest architecture decisions |
| Your Product_Sites library | `Canary_IP/Documents/Product_Sites/` (all 19 files) | Your own work — audit it |
| PhD Profile | `Company/Team/PhD.md` | Your principles and mandate |

---

## What This Is NOT

This is not a rewrite of your work. This is not a critique. This is an alignment audit — PhD reviewing their own research output against the team's current authoritative specs, so that Jim and Jess get clean, consistent source material without having to reconcile contradictions themselves.

**You produced the intellectual foundation.** This brief makes it consumable by the rest of the team.

---

## Routing When Complete

1. **ALX** reviews the Alignment Brief
2. ALX uses the brief to **update Jim and Jess work orders** with PhD-curated reading lists and terminology reconciliation
3. Jim and Jess dispatch with PhD's brief as their first read — it tells them exactly which Product_Sites files to consume and what to watch for
4. Art receives any supplemental notes about prototype alignment

---

## Gate

Jim and Jess **do not dispatch** until this brief is complete and ALX has integrated it into their work orders. Art is already in progress and unaffected — but if the brief reveals prototype misalignment with the PRD, ALX will send Art a supplemental note.

---

*Work order issued by ALX · February 24, 2026*
*This is a COORDINATE task — PhD owns the assessment, ALX routes the output.*
