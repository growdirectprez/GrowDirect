---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# WORK ORDER: Jim — Guided Companion QA Prep & Scenario Authoring
**Dispatched by:** ALX (Chief of Staff)
**Updated by:** Eva (Program Manager) — February 24, 2026
**Date:** February 24, 2026
**Priority:** 🔴 HIGH — Both upstream dependencies DELIVERED. Full execution begins NOW.
**Mode:** DISPATCH (Eva owns timeline, Jim owns test quality)
**UAT Gate:** Monday March 3, 2026

---

## Status Update (Eva, Feb 24)

**Both upstream blockers are RESOLVED:**
- ✅ **PhD Alignment Brief** — DELIVERED at `_ALX/WorkOrders/output/PhD/PhD_Alignment_Brief.md`
- ✅ **Art v1.1 wireframe** — DELIVERED at `_ALX/WorkOrders/output/Art/TodaysView_Wireframe_v1.1.html`

Jim is now UNBLOCKED for all phases. Phase 1 and Phase 2 execute in parallel where possible. UAT is Monday March 3 — 7 days from now.

---

## ⚠️ MANDATORY PRE-READ: PhD Terminology Reconciliation

Before writing ANY test scenario or workflow description, read the **Terminology Reconciliation Table** in PhD Alignment Brief Section 6 (`_ALX/WorkOrders/output/PhD/PhD_Alignment_Brief.md`). Key terms Jim must use consistently:

| Concept | WRONG Term | CORRECT Term |
|---|---|---|
| Home screen | "Dashboard" | **Today's View** |
| Alert module | "Chirp Engine" | **Chirps** |
| Navigation module names | Various | **Canary, Owl, Fox, Bull, Rooster, Goose** |
| Settings | "Settings" | **Farm** |
| Product feature | "Canary LP" (as feature name) | **Guided Operations Companion** (the E0-F6 feature); **Canary** (the product) |
| Interaction pattern | "Incident Report Form" | **Guided Wizard** (standalone forms are deprecated) |
| Control paradigm | "Command Center" | **Companion** (guided, not command-and-control) |

**If Jim writes a test scenario using "Dashboard" instead of "Today's View," the scenario is non-conformant.** PhD's terminology table is the normalization authority.

---

## PhD-Curated Reading Lists for Jim

From PhD Alignment Brief Section 5 — these are Jim's required readings, organized by priority.

### Priority 1 — Must Read

| # | File | Path | Why | Watch For |
|---|---|---|---|---|
| 1 | PRD E0-F6 | `Canary_IP/Documents/Product_Guides/Canary_PRD_E0F6_Guided_Companion_v1.0.docx` | Every acceptance criterion (AC-A1 through AC-D7) needs a test. | P0 scenarios: Complete Process 4 wizard, Photo evidence capture. |
| 2 | Design Spec v1.0 | `Canary_IP/Markdown/Specs/Canary_Guided_Companion_Design_Spec_v1.0.md` | Section 3 (Process 4 wizard step-by-step) is the most detailed testable workflow. Section 10 lists all 8 processes. | 6 screens max per wizard. Progressive disclosure (Owner sees Fox button, Manager doesn't). |
| 3 | Tom B-001 Output | `Canary_IP/Markdown/Alpha3X/output/TOM_SESSION_OUTPUT_B-001_2026-02-24.md` | P0-3 section includes 7 explicit QA test cases for hash chain verification, trigger rejection, cross-merchant isolation. | 7 specific test cases Tom wrote for Jim. |
| 4 | CRDM v1.0 | `Canary_IP/Markdown/Specs/CRDM_v1.0.md` | Part 5 (Chirp Detection Registry) — every rule needs a test scenario. Part 11 has explicit "Rules for Jim." | 22 Chirp rules, each needing trigger/non-trigger/boundary tests. |

### Priority 2 — Testable Workflows

| # | File | Path | Why | Watch For |
|---|---|---|---|---|
| 5 | Fox Module Tech Spec | `Canary_IP/Documents/Product_Sites/Fox_Module_Technical_Specification_v1.0.html` | Fox case management workflows. **CURRENT** per PhD brief. | Evidence INSERT-only constraint (now enforced by Tom B-001 P0-2 triggers). Case status transitions. |
| 6 | Incident Report Form | `Canary_IP/Documents/Product_Sites/Canary_Incident_Report_Form_v1.0.html` | **NEGATIVE TEST reference.** This form pattern is deprecated by wizards. Verify NO standalone forms ship. | Verify this form is NOT implemented in the final product. |

### DO NOT Use as Test Baseline

| File | Why Not |
|---|---|
| `Canary_Prototype_v2.0.html` | Dashboard paradigm. Tests written against this UI will be invalid. |
| `dashboard.html` | Not a Canary file. Ignore completely. |

### Fox Module Test Scenarios Jim Should Write (from PhD brief)

1. Case creation from wizard escalation (Owner at wizard step 3 taps "Flag for Fox")
2. Evidence upload during wizard (INSERT-only — attempt UPDATE/DELETE must fail per Tom B-001)
3. Hash chain integrity verification after evidence upload
4. Case timeline append on wizard completion
5. Role-based visibility: Manager cannot see Fox workbench or escalation button
6. BOLO creation and cross-merchant matching (if in scope)

---

## Assignment

Prepare the QA foundation for the Guided Operations Companion (E0-F6). Two phases:

**Phase 1 (IMMEDIATE — independent of wireframe):** UAT logistics, Alpha Gate Checklist, Tom's QA scenarios, untested route prioritization.
**Phase 2 (NOW UNBLOCKED — Art v1.1 delivered):** Today's View day-in-the-life scripts against real wireframe, Wizard Flow QA mapping, QA Summary Brief (2C) for Jess.

Jim's output from both phases feeds directly into Jess's Companion Guide documents — she needs Jim's merchant-perspective walkthrough to write accurate functional descriptions.

---

## Phase 1 Deliverables (Start Immediately)

### 1A. UAT Logistics Confirmation
- Confirm merchant participants for Monday March 3 UAT — names, availability, devices, store locations
- Confirm test environment readiness requirements (what Jeremy must deliver before Jim can test)
- Draft UAT schedule: which merchants test what, in what order, how long per session
- **Eva tracking:** Jim must have merchant list confirmed by **Wednesday Feb 26** or Eva escalates to ALX → Jeffe for network outreach

### 1B. Alpha Gate Checklist Review
- Review the 10-item Alpha Gate Checklist at `Canary_IP/Markdown/QA/Alpha_v0.1.0_QA_Handoff.md`
- Flag any items that are not yet achievable given current Sprint 5 status
- Note dependencies on Jeremy (Phase 2 Alembic migrations — in progress on iMac QA box)

### 1C. Tom's Data Integrity Scenarios
- Review Tom's 7 QA test scenarios at `Canary_IP/Markdown/Alpha3X/output/TOM_SESSION_OUTPUT_B-001_2026-02-24.md`
- Map each scenario to Jim's test format (SCENARIO / MODULE / ROLE / STORY / STEPS / EXPECTED / EDGE CASES)
- Identify which scenarios can be tested before UAT vs. which require production-like data

### 1D. Untested Route Prioritization (B-007)
- 20 routes still without tests (companion_wired.py x5, fox_wired.py x3, others)
- Classify each: **Must have coverage before UAT** vs. **Can wait until post-alpha**
- Output: prioritized list with rationale

---

## Phase 2 Deliverables (NOW UNBLOCKED — Art v1.1 Delivered)

**Wireframe reference:** `_ALX/WorkOrders/output/Art/TodaysView_Wireframe_v1.1.html`
**Self-critique:** `_ALX/WorkOrders/output/Art/TodaysView_SelfCritique_v1.1.md`

### 2A. Today's View — Day-in-the-Life Test Scripts
Write merchant-perspective test scripts for the Today's View screen. **Test against Art v1.1 wireframe** — this is the finalized wireframe with custom SVG icons and the Chirp peek indicator.

**Scenario Set 1: Morning Open (Store Manager role)**
- Manager opens app at 7:00 AM
- Sees greeting + Chirp count
- Hero Chirp banner shows most urgent item
- Manager taps "Open the Store" action card
- Wizard launches → completes in <5 minutes
- Returns to Today's View with updated state

**Scenario Set 2: Mid-Shift Alert (Shift Supervisor role)**
- Supervisor receives Chirp: CASH_VARIANCE_THRESHOLD
- Opens app, sees hero banner updated with cash shortage alert
- Taps banner → Wizard Process 4 launches
- Completes 6-step resolution in <8 minutes
- Evidence captured (photo + notes) feeds Fox chain

**Scenario Set 3: End-of-Day Review (Owner role)**
- Owner opens app at 9 PM
- Sees summary of day's resolved Chirps
- Action cards show "Count the Drawer" and "Check Yesterday's Shrink"
- Owner sees scorecard data that Manager does not (role gating verified)

**Scenario Set 4: Edge Cases & Failures**
- No active Chirps — what does Today's View show?
- 10+ Chirps — does the "max 3 cards" rule hold?
- Network offline — graceful degradation?
- Wrong role sees wrong data — role gating enforcement

**Scenario Set 5: v1.1-Specific Test Cases (from Art's Self-Critique)**
- `test_chirp_peek_renders_when_2_active` — When 2+ Chirps active: peek element visible beneath hero, shows "+1 more:" prefix + second Chirp title, tapping navigates to Chirps tab (NOT a wizard)
- `test_chirp_peek_hidden_when_0_or_1_chirps` — When 0-1 Chirps: peek element NOT in DOM, no empty space between hero and action section
- SVG icon rendering verification: all 6 animal icons identifiable at 20px across iOS Safari, Android Chrome, and desktop browsers

### 2B. Wizard Flow QA Mapping (Processes 1–4)
For each of the 4 MVP wizard processes, write:
- Happy path test script (step-by-step)
- Edge case scenarios (missing data, wrong role, timeout, photo upload failure)
- Evidence chain validation (does captured data appear in Fox?)
- Completion confirmation (confetti + chirp sound + "shrink prevented" message)

### 2C. Companion Guide Input Package for Jess
Compile a **QA Summary Brief** specifically for Jess's use in writing the Companion Guides:
- Merchant workflow descriptions (plain language, no code references)
- Screen-by-screen descriptions of what the merchant sees and does
- Role-based differences (what owner sees vs. manager vs. part-timer)
- Common error states and how they're handled
- The "phone test" assessment: would this make Jim's phone ring?

**Format:** Markdown file, organized by screen/flow, written for a non-technical reader.
**Output to:** `_ALX/WorkOrders/output/Jim/Jim_QA_Summary_Brief_2C.md`

---

## Context Files (Read Before Starting)

| File | Path | Why | Priority |
|---|---|---|---|
| PhD Alignment Brief | `_ALX/WorkOrders/output/PhD/PhD_Alignment_Brief.md` | Terminology reconciliation (Section 6), curated reading lists (Section 5), file currency assessment (Section 1) | **READ FIRST — Section 6 terminology table is mandatory** |
| Art v1.1 Wireframe | `_ALX/WorkOrders/output/Art/TodaysView_Wireframe_v1.1.html` | The actual screens Jim will test against. Final version with custom SVGs + Chirp peek. | **READ FIRST** |
| Art v1.1 Self-Critique | `_ALX/WorkOrders/output/Art/TodaysView_SelfCritique_v1.1.md` | Known UX gaps, v1.1 test cases (Tests 4, 4b), remaining items for future QA | HIGH |
| PRD E0-F6 | `Canary_IP/Documents/Product_Guides/Canary_PRD_E0F6_Guided_Companion_v1.0.docx` | Feature requirements, user stories, acceptance criteria | HIGH |
| Design Spec v1.0 | `Canary_IP/Markdown/Specs/Canary_Guided_Companion_Design_Spec_v1.0.md` | Full UX spec — wizard flows, role gating, scorecards | HIGH |
| Alpha Gate Checklist | `Canary_IP/Markdown/QA/Alpha_v0.1.0_QA_Handoff.md` | 10-item checklist Jim must sign off on | HIGH |
| Tom's B-001 Output | `Canary_IP/Markdown/Alpha3X/output/TOM_SESSION_OUTPUT_B-001_2026-02-24.md` | 7 data integrity QA scenarios | HIGH |
| CRDM v1.0 | `Canary_IP/Markdown/Specs/CRDM_v1.0.md` | Data model — what data backs each screen | HIGH |
| Jim's Profile | `Company/Team/Jim.md` | Test scenario template, Rooster framework, principles | Reference |

---

## Routing When Complete

1. **Phase 1 output** → Eva reviews, feeds into UAT planning
2. **Phase 2A + 2B** → Jeremy uses to validate implementation against real test scripts
3. **Phase 2C (QA Summary Brief)** → Goes directly to Jess as input for the Functional and Technical Companion Guides
4. **All scenarios** → Become part of the permanent Rooster test library

---

## Dependencies

| Dependency | Owner | Status | Impact |
|---|---|---|---|
| Art's Today's View wireframe v1.1 | Art | ✅ DELIVERED | Phase 2 is UNBLOCKED |
| PhD Alignment Brief | PhD | ✅ DELIVERED | Terminology + reading lists integrated |
| Sprint 5 Phase 2 (Alembic on Postgres) | Jeremy | 🔄 IN PROGRESS | UAT requires live database — Jeremy targeting Feb 28 |
| Sprint 5 Phase 3–4 (triggers + validation) | Jeremy | PENDING | Data integrity scenarios require working triggers |

---

## Gate

Jim's QA sign-off on the Companion is a hard dependency for:
- Jess's Companion Guide documents (can't describe what isn't validated)
- Jeremy's production build (no build without test scripts mapped)
- Monday March 3 UAT (Jim owns the test, Eva owns the timeline)

**Jim's veto is non-negotiable. If it doesn't pass Jim's phone test, it doesn't ship.**

---

*Work order issued by ALX · February 24, 2026*
*Updated by Eva (Program Manager) · February 24, 2026 — PhD brief + Art v1.1 integration, Phase 1/Phase 2 confirmed, terminology reconciliation added*
*Factory Process Stage: BLUEPRINT → QC prep*
