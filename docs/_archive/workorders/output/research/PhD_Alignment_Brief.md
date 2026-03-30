---
type: research
domain: protocol
status: active
created: 2026-03-18
updated: 2026-03-19
---
# PhD Alignment Brief — Product_Sites Library Audit

**Author:** PhD (Bitcoin-Native Retail Loss Prevention Research Specialist)
**Date:** February 24, 2026
**Work Order:** WORKORDER_PhD_AlignmentBrief.md
**Dispatched by:** ALX (Chief of Staff)
**Purpose:** Map PhD's Product_Sites library against the PRD (E0-F6), Design Spec v1.0, and CRDM v1.0. This brief is the bridge between PhD's research output and the downstream team (Art, Jim, Jess).

**Authoritative Sources (resolution order when conflicts arise):**

1. PRD E0-F6 Guided Companion v1.0 (Eva + Art, Feb 22)
2. Design Spec v1.0 (Art + Eva, Feb 22)
3. CRDM v1.0 Master Data Model Guide (Eva + Tom + Jeremy, Feb 20)
4. Tom's B-001 Session Output (Tom, Feb 24)
5. Live codebase

---

## 1. File Inventory with Currency Assessment

19 HTML files in `Canary_IP/Documents/Product_Sites/`. Status definitions: **CURRENT** (safe to reference), **STALE** (product has evolved past this), **SUPERSEDED** (newer version exists), **REFERENCE ONLY** (context/history, not authoritative).

| # | File | Date | Status | Superseded By | Notes |
|---|------|------|--------|---------------|-------|
| 1 | `Canary_Prototype_v2.0.html` | Feb 21 | **STALE** | Design Spec v1.0 | Dashboard-style prototype with 17+ metrics. **Directly contradicts PRD "guided, not dashboard" directive.** See Section 2 misalignment notes. |
| 2 | `canary_prototype.html` | Feb 16 | **SUPERSEDED** | `Canary_Prototype_v2.0.html` | Original prototype v1.0. Do not reference. |
| 3 | `Canary_CRDM_v2.0.html` | Feb 21 | **STALE** | CRDM v1.0 markdown is canonical | PhD's expanded data model HTML. Rich detail but diverges from canonical CRDM v1.0. See Section 3 for entity comparison. |
| 4 | `Canary_CRDM_Mapping_Analysis_v1.0.html` | Feb 16 | **REFERENCE ONLY** | CRDM v1.0 markdown | Early mapping of enterprise ancestor fields to Canary schema. Useful historical context for Jess. Superseded by CRDM v1.0 as authoritative mapping. |
| 5 | `Canary_Data_Model_Assessment_v1.0.html` | Feb 16 | **REFERENCE ONLY** | CRDM v1.0 markdown | PhD's initial architecture assessment for Jeffe. Predates scope expansion. Historical value only. |
| 6 | `Canary_Platform_Schema_Complete_v1.0.html` | Feb 17 | **STALE** | CRDM v1.0 + Tom B-001 | Detailed schema spec from Tom/PhD. Some table definitions predate Tom's Feb 20 T-3 DDL delivery and Feb 24 B-001 trigger design. Cross-reference with Tom B-001 before consuming. |
| 7 | `Canary_JSONB_Forensic_Analysis_v1.0.html` | Feb 16 | **REFERENCE ONLY** | CRDM v1.0 (line items/tenders now extracted) | Analysis of JSONB payload structure. The core finding — that line items and tenders were trapped in JSONB — drove the E1-F7 scope expansion. That expansion is now complete in CRDM v1.0. Historical reference for why the extraction was needed. |
| 8 | `Fox_Module_Technical_Specification_v1.0.html` | Feb 16 | **CURRENT** | — | Fox case management technical spec. Aligned with CRDM v1.0 Fox tables. Tom B-001 P0-2 adds immutability triggers on top. **Key reference for Jim (test scenarios) and Jess (Technical Guide).** |
| 9 | `Canary_Incident_Report_Form_v1.0.html` | Feb 16 | **STALE** | Design Spec (Guided Wizard pattern) | Placeholder incident form. **Does NOT follow the Guided Wizard pattern from Design Spec Section 3.** PRD mandates all user interactions go through wizards. This standalone form pattern is deprecated by the Companion approach. |
| 10 | `Canary_Factory_Process_v2.0.html` | Feb 21 | **CURRENT** | — | Factory Process documentation (6-stage delivery pipeline). Aligned with PRD Section 8 QA gates. Reference for Jim and Jess. |
| 11 | `Canary_Agent_Briefing_v1.0.html` | Feb 21 | **CURRENT** | — | Agent Swarm overview — 14 AI agents, roles, capabilities. Board/advisor audience. Reference for Jess (Functional Guide context). |
| 12 | `Canary_Board_Update_2026-02-21_v1.0.html` | Feb 21 | **CURRENT** | — | Board progress update. Useful for Jess as business positioning context. Not technical reference. |
| 13 | `Canary_Marketing_Site_v2.0.html` | Feb 21 | **CURRENT** | — | Marketing site. **Watch for module naming: uses "Detection Modules" framing.** Verify animal module names match canonical set. See Section 6 terminology. |
| 14 | `Canary_Demo_Site_v1.0.html` | Feb 18 | **STALE** | `Canary_Marketing_Site_v2.0.html` | Earlier demo/marketing page. Superseded by v2.0 marketing site. |
| 15 | `Canary_Command_Center_v1.0.html` | Feb 18 | **STALE** | Design Spec v1.0 | Internal team navigation hub. "Command Center" framing is pre-Companion. The product is now "Guided Operations Companion." |
| 16 | `Canary_LP_Magazine_Article.html` | Feb 17 | **SUPERSEDED** | `Canary_LP_Magazine_Article_v2.0.html` | Original magazine article. Do not reference. |
| 17 | `Canary_LP_Magazine_Article_v2.0.html` | Feb 18 | **CURRENT** | — | Long-form narrative for external/marketing use. Good Jess source for Functional Guide tone and problem/solution framing. |
| 18 | `about.html` | Feb 16 | **REFERENCE ONLY** | Marketing Site v2.0 | Simple about page. Minimal technical content. |
| 19 | `dashboard.html` | Feb 16 | **SUPERSEDED** | — | Productivity/task management dashboard. **Not a Canary product file.** Appears to be a generic productivity tool UI. Ignore for all downstream work. |

### Summary

| Status | Count | Action |
|--------|-------|--------|
| CURRENT | 6 | Safe to reference |
| STALE | 5 | Reference with caveats — product has evolved |
| SUPERSEDED | 3 | Do not reference — newer version exists |
| REFERENCE ONLY | 4 | Historical context only — not authoritative |
| NOT APPLICABLE | 1 | `dashboard.html` — not a Canary product file |

---

## 2. PRD E0-F6 Feature Mapping

### E0-F6-A: Today's View (Home Screen)

| Aspect | PRD Spec | Product_Sites Coverage | File(s) | Misalignment |
|--------|----------|----------------------|---------|-------------|
| Max action cards | **Max 3** (AC-A4) | Prototype v2.0 shows 17+ metrics as dashboard tiles | `Canary_Prototype_v2.0.html`, `canary_prototype.html` | **CRITICAL MISALIGNMENT.** Prototype shows dashboard with transaction counts, refund counts, shrinkage rates, revenue, multiple charts. PRD mandates max 3 opinionated action cards. |
| Greeting + Chirp count | Personalized greeting + active Chirp count (AC-A1) | Prototype shows "Merchant #4521" header but no personalized greeting or Chirp count | `Canary_Prototype_v2.0.html` | **Gap.** Prototype has no greeting bar, no Chirp count display. |
| Hero Chirp banner | Highest-priority Chirp with wizard launch (AC-A2) | Not present in any prototype | — | **Gap.** No prototype shows the hero Chirp banner concept. Art must design from scratch using Design Spec Section 2. |
| Health bar | Green/yellow/red gradient (AC-A6) | Not present | — | **Gap.** No prototype implements health bar. |
| Time-of-day awareness | Cards change by AM/PM (US-A3) | Not present | — | **Gap.** Prototypes are static. |
| Load time | <400ms on mobile (AC-A7) | N/A for static HTML files | — | Implementation concern, not prototype issue. |

**Bottom line for Art:** The existing prototypes (v1.0 and v2.0) are **not usable as wireframe starting points** for Today's View. They represent the old dashboard paradigm that the PRD explicitly rejects. Art should design Today's View from the Design Spec Section 2 description, not from these prototypes.

### E0-F6-B: Guided Wizard Engine

| Aspect | PRD Spec | Product_Sites Coverage | File(s) | Misalignment |
|--------|----------|----------------------|---------|-------------|
| Wizard framework | HTMX step swaps, 6 screens max, <8 min (AC-B1, AC-B2) | No wizard implementation in any prototype | — | **Complete gap.** No Product_Sites file shows a guided wizard pattern. |
| Evidence capture | Photo upload → Fox INSERT-only (AC-B3) | Incident Report Form has evidence fields but as standalone form, not wizard step | `Canary_Incident_Report_Form_v1.0.html` | **Pattern misalignment.** Form exists but doesn't follow wizard pattern. Cannot be used as-is. |
| Progressive disclosure | Owner sees Fox escalation, Manager doesn't (AC-B4) | Fox Module spec discusses role-based access | `Fox_Module_Technical_Specification_v1.0.html` | **Partial coverage.** Fox spec covers role-based case access but not wizard-step-level progressive disclosure. |
| Completion UX | Confetti + chirp sound + tip (AC-B5) | Not present | — | **Gap.** No celebration/completion UX in any file. |

### E0-F6-C: Core Guided Processes (MVP: 1-4)

| Process | PRD Spec | Product_Sites Coverage | File(s) | Misalignment |
|---------|----------|----------------------|---------|-------------|
| P1: Open the Store | 4 steps, <5 min, AM trigger | Not present | — | **Complete gap.** |
| P2: Count the Drawer | 5 steps, <6 min, shift end trigger | Not present | — | **Complete gap.** |
| P3: Resolve Refund Alert | 5 steps, <7 min, HIGH_REFUND_FREQUENCY trigger | Not present | — | **Complete gap.** |
| P4: Resolve Cash Shortage | 6 steps, <8 min, CASH_VARIANCE_THRESHOLD trigger | Design Spec Section 3 has detailed step-by-step. Incident Report Form has related fields. | `Canary_Incident_Report_Form_v1.0.html` (tangential) | Incident Report Form captures cash-related data but not as wizard steps. Design Spec Section 3 is the authoritative source for P4 wizard flow. |

**Bottom line:** None of the 4 MVP processes have prototype implementations in Product_Sites. All wizard flows are net-new design work for Art and implementation work for Jeremy.

### E0-F6-D: Contextual Scorecards

| Aspect | PRD Spec | Product_Sites Coverage | File(s) | Misalignment |
|--------|----------|----------------------|---------|-------------|
| 5 scorecards | Daily Shrink, Alert Heatmap, Team Performance, Inventory Health, Treasury Snapshot | Prototype v2.0 shows multiple metric panels but not as contextual scorecards | `Canary_Prototype_v2.0.html` | **Pattern misalignment.** Prototype shows metrics as always-visible dashboard tiles. PRD says scorecards are contextual (appear based on triggers), never on first load, and have exactly 1 headline number + 1 trend arrow + 1 Fix It button. |
| Role gating | Owner-only for Team Performance; Owner+Manager for others | Not implemented in prototypes | — | **Gap.** |
| Tailwind + HTMX | Cards rendered as Tailwind + HTMX, never Superset (AC-D7) | Prototype may use different rendering approach | `Canary_Prototype_v2.0.html` | Verify implementation approach. |

---

## 3. CRDM Alignment

### CRDM v2.0 HTML (`Canary_CRDM_v2.0.html`) vs. CRDM v1.0 Markdown (Canonical)

The canonical CRDM is `Canary_IP/Markdown/Specs/CRDM_v1.0.md` (Eva + Tom + Jeremy, Feb 20). PhD's CRDM v2.0 HTML was produced Feb 21 and expands on the canonical in some areas but also diverges.

#### Entity/Table Comparison

| Topic | CRDM v1.0 (Canonical) | CRDM v2.0 HTML (PhD) | Delta | Resolution |
|-------|----------------------|---------------------|-------|------------|
| Total table count | ~35 tables (27 existing + 8 new) | Likely expanded beyond 35 | PhD v2.0 may include additional tables not in canonical | **CRDM v1.0 is authoritative.** PhD additions are proposals, not spec. |
| Three-database boundaries | canary_app, canary_sales, canary_metrics — explicitly defined | Same three databases | **Aligned** | No conflict. |
| Chirp rule count | 22 rules (C-001 to C-602) across 6 categories | Likely matches or exceeds 22 | Verify PhD v2.0 doesn't define additional rules not in canonical registry | **CRDM v1.0 Part 5 is the authoritative Chirp registry.** |
| Transaction type enum | 8 types: SALE, RETURN, VOID, POST_VOID, NO_SALE, PAID_IN, PAID_OUT, EXCHANGE | Should match | Verify alignment | CRDM v1.0 Source #1 is authoritative. |
| Immutability categories | 3 categories: Financial (append-only), Evidentiary (insert-only), Audit trail (append-only + SHA-256) | Should match | Verify PhD v2.0 categorization matches CRDM v1.0 Principle 3 | Tom B-001 P0-1/P0-2 are the implementation authority. |
| Data source coverage | 7 canonical sources at 68% raw / ~85% LP-weighted | PhD v2.0 may report different coverage numbers | Check for stale coverage percentages | CRDM v1.0 Part 8 scorecard is current. |

#### CRDM Mapping Analysis (`Canary_CRDM_Mapping_Analysis_v1.0.html`)

This file (Feb 16) predates the CRDM v1.0 (Feb 20) and represents PhD's initial enterprise-to-Canary field mapping. Key considerations:

- The coverage percentages in this file may not reflect post-scope-expansion numbers
- Field-level mappings were incorporated into CRDM v1.0 and may have been refined
- **Status: REFERENCE ONLY** — use CRDM v1.0 for current field mappings

#### Chirp Rule Consistency

| Source | Rule Registry | Notes |
|--------|--------------|-------|
| CRDM v1.0 Part 5 | 22 rules (C-001 to C-602) | **Authoritative.** |
| Design Spec Section 3 | References C-102 (CASH_VARIANCE_THRESHOLD) as Process 4 trigger | Aligned. |
| PRD E0-F6-C | References HIGH_REFUND_FREQUENCY and CASH_VARIANCE_THRESHOLD as triggers | Aligned with CRDM rule IDs. |
| PhD CRDM v2.0 HTML | Verify rule count and IDs match canonical 22 | If additional rules defined, they are proposals only. |

#### Data Source Status Impact

| Data Source | CRDM v1.0 Status | Impact on Art Wireframe | Impact on Jim Testing |
|-------------|-------------------|------------------------|----------------------|
| Cash Drawer (C-101 to C-104) | 🆕 E1-F6 | Can show in wizard prototypes | Testable with mock data |
| Line Items (C-201 to C-203) | 🆕 E1-F7 | Required for Process 3 (refund detail) | Need line-item test fixtures |
| Timecards (C-301 to C-303) | 🆕 E1-F8 | Process 4 step 2 ("Who touched it last?") depends on this | Need timecard cross-reference test data |
| Inventory (C-501 to C-502) | 🆕 E1-F10 | Process 6 (Check Inventory Shrink) — beta scope | Not needed for MVP Processes 1-4 |
| Gift Cards (C-601 to C-602) | 🆕 E1-F11 | Not in MVP processes | Not needed for MVP |

---

## 4. Architecture & Technical Alignment

| Topic | PhD File(s) | Tom/Jeremy Source | Aligned? | Notes |
|-------|-------------|-------------------|----------|-------|
| **Immutability model** | `Canary_JSONB_Forensic_Analysis_v1.0.html`, `Canary_Platform_Schema_Complete_v1.0.html` | Tom B-001 P0-1 (financial), P0-2 (evidentiary) | **Partially** | PhD files discuss immutability conceptually. Tom B-001 provides the actual PostgreSQL trigger implementation. PhD files predate the trigger design and don't include `prevent_mutation()` or `prevent_evidence_mutation()` function specs. **Tom B-001 is authoritative for implementation.** PhD files provide the theoretical justification (Bitcoin UTXO analogy). |
| **Fox case management** | `Fox_Module_Technical_Specification_v1.0.html` | CRDM v1.0 (Fox tables in canary_app), Tom B-001 P0-2 | **Yes** | Fox spec is well-aligned with CRDM v1.0 Fox table definitions. Tom B-001 adds immutability triggers on `case_evidence`, `case_timeline`, `evidence_access_log`, `audit_log` which complement but don't contradict the Fox spec. **One gap:** Tom B-001 notes `case_evidence` needs a `previous_chain_hash` column (CRDM-G1) that the Fox spec doesn't mention. Jeremy must add this. |
| **Three-database architecture** | `Canary_Platform_Schema_Complete_v1.0.html`, `Canary_CRDM_v2.0.html` | CRDM v1.0 Part 2, Tom B-001 (schema prefixes) | **Yes** | All sources agree: canary_app (operational), canary_sales (transaction log), canary_metrics (analytics). Tom B-001 uses `canary_sales.` and `canary_app.` schema prefixes, confirming the boundary. |
| **Chirp rule engine** | `Canary_CRDM_v2.0.html` | Design Spec Section 3 (wizard triggers), CRDM v1.0 Part 5 | **Partially** | PhD v2.0 HTML likely includes rule definitions. Verify they match the canonical 22-rule registry in CRDM v1.0 Part 5. Design Spec maps specific rules to wizard triggers (e.g., CASH_VARIANCE_THRESHOLD → Process 4). Any PhD additions are proposals. |
| **The Dome / Lightning** | PhD.md Part IX (Softwar defense, Lightning integration) | Design Spec Section 7 (Superset + HTMX Integration) | **Separate concerns** | PhD's Dome/Lightning concept (L402, LNURL-auth, micropayments) is a strategic vision for Bitcoin-native security. Design Spec Section 7 addresses Superset vs. HTMX for UI rendering. These are orthogonal — the Dome is a future infrastructure layer, not a current implementation spec. **No conflict, but no implementation overlap either.** Jess should reference PhD.md Part IX for the Technical Guide's Bitcoin/Lightning section. |
| **Hash chain verification** | `Canary_Platform_Schema_Complete_v1.0.html` (discusses hash chain concept) | Tom B-001 P0-3 (full PostgreSQL implementation spec) | **Tom B-001 supersedes** | PhD file discusses hash chaining conceptually. Tom B-001 provides production-ready SQL: `verify_entry_hash()`, `verify_hash_chain()`, `compute_entry_hash()`. PhD concept is validated by Tom's implementation. |
| **Compensating INSERT pattern** | Mentioned conceptually in PhD files | Tom B-001 P0-1 Note #4: "INSERT a new compensating record with correction_flag" | **Aligned** | Both agree on the pattern. Tom provides explicit implementation guidance. |

---

## 5. Recommended Reading Lists

### For Art (UX/Creative Director — Today's View Wireframe)

Art is already in progress on wireframes. These readings ensure alignment with authoritative specs and prevent accidentally pulling from stale prototypes.

**Priority 1 — Must Read:**

| # | File | Why | Watch For |
|---|------|-----|-----------|
| 1 | **Design Spec v1.0** (`Canary_Guided_Companion_Design_Spec_v1.0.md`) | This IS Art's design brief. Sections 1-2 define nav structure and Today's View. Section 3 defines wizard pattern. | "Max 3 action cards" (Section 2, item 3). Hero Chirp banner. Six animal avatars for bottom nav. |
| 2 | **PRD E0-F6** (`Canary_PRD_E0F6_Guided_Companion_v1.0.docx`) | Acceptance criteria Art's designs must satisfy. | AC-A4 (max 3 cards), AC-A7 (<400ms), AC-B2 (6 screens max per wizard), AC-D6 (1 headline + 1 arrow + 1 Fix It per scorecard). |

**Priority 2 — Reference:**

| # | File | Why | Watch For |
|---|------|-----|-----------|
| 3 | `Canary_Marketing_Site_v2.0.html` | Brand tone and positioning. How the product is described externally. | Module names — verify they match canonical animal names. |
| 4 | `Canary_LP_Magazine_Article_v2.0.html` | Long-form narrative. Useful for understanding the merchant persona and pain points Art is designing for. | The "19-year-old closer" persona mentioned in Design Spec. |

**DO NOT reference for wireframe design:**

| File | Why Not |
|------|---------|
| `Canary_Prototype_v2.0.html` | **Dashboard paradigm.** 17+ metrics on load. Directly contradicts "guided, not dashboard" directive. |
| `canary_prototype.html` | Superseded v1.0. Even more dashboard-heavy. |
| `Canary_Command_Center_v1.0.html` | "Command Center" framing is pre-Companion. Wrong mental model. |

**Specific guidance for Art:** The existing prototypes (v1.0 and v2.0) show what the product is NOT. They are useful as counter-examples. The Design Spec Section 2 quote is explicit: *"The attached prototype dumps 17 metrics on load. That is retail-owner PTSD in pixel form. A 19-year-old closer will close the tab."* Design from the spec, not the prototypes.

---

### For Jim (QA Manager & Test Architect — QA Scenarios)

Jim needs to write test scenarios for E0-F6 acceptance criteria. These readings give him testable workflows, data states, and edge cases.

**Priority 1 — Must Read:**

| # | File | Why | Watch For |
|---|------|-----|-----------|
| 1 | **PRD E0-F6** (docx) | Every acceptance criterion (AC-A1 through AC-D7) needs a test. Test scenario tables are already drafted in the PRD. | P0 scenarios: Complete Process 4 wizard (P0), Photo evidence capture (P1). |
| 2 | **Design Spec v1.0** (md) | Section 3 (Process 4 wizard step-by-step) is the most detailed testable workflow. Section 10 lists all 8 processes with CRDM table dependencies. | Step-by-step wizard flow: 6 screens, specific UI at each step. Progressive disclosure (Owner sees Fox button, Manager doesn't). |
| 3 | **Tom B-001** (md) | P0-3 section includes explicit QA test suite additions for hash chain verification, trigger rejection, and cross-merchant isolation. | 7 specific test cases Tom wrote for Jim (INSERT verification, chain walk, tamper detection, genesis test, cross-merchant isolation, two trigger rejection tests). |
| 4 | **CRDM v1.0** (md) | Part 5 (Chirp Detection Registry) — every rule needs a test scenario. Part 11 has explicit "Rules for Jim." | 22 Chirp rules. Each needs: test data that triggers it, test data that doesn't, threshold boundary tests. |

**Priority 2 — Testable Workflows:**

| # | File | Why | Watch For |
|---|------|-----|-----------|
| 5 | `Fox_Module_Technical_Specification_v1.0.html` | Fox case management workflows: case creation, evidence upload, case timeline, role-based access. | Evidence INSERT-only constraint (now enforced by Tom B-001 P0-2 triggers). Case status transitions. BOLO patterns. |
| 6 | `Canary_Incident_Report_Form_v1.0.html` | **Negative test:** This form pattern is deprecated by the wizard approach. Jim should verify that NO standalone forms ship — everything goes through wizards. | Verify this form is NOT implemented in the final product. It represents the wrong pattern. |

**Do NOT use as test baseline:**

| File | Why Not |
|------|---------|
| `Canary_Prototype_v2.0.html` | Dashboard paradigm. Tests written against this UI will be invalid. |
| `dashboard.html` | Not a Canary file. Ignore completely. |

**Fox Module test scenarios Jim should write:**

1. Case creation from wizard escalation (Owner at wizard step 3 taps "Flag for Fox")
2. Evidence upload during wizard (INSERT-only — attempt UPDATE/DELETE must fail per Tom B-001)
3. Hash chain integrity verification after evidence upload
4. Case timeline append on wizard completion
5. Role-based visibility: Manager cannot see Fox workbench or escalation button
6. BOLO creation and cross-merchant matching (if in scope)

---

### For Jess (Documentation Lead — Functional + Technical Companion Guides)

Jess needs source material for two guides: a Functional Guide (business-facing) and a Technical Guide (architecture-facing). These readings are organized by guide.

**For the Functional Guide (Business Positioning, Merchant Experience, Problem/Solution):**

| # | File | Why | What to Lift | What to Rewrite |
|---|------|-----|-------------|-----------------|
| 1 | `Canary_LP_Magazine_Article_v2.0.html` | Best narrative source. Long-form story of the problem and Canary's solution. Written for external audience. | Problem framing ("33 million SMB retailers"), competitive positioning, Bitcoin-native differentiation. | Tone may need adjustment from marketing to guide voice. |
| 2 | `Canary_Board_Update_2026-02-21_v1.0.html` | Business metrics, progress milestones, market positioning. | Market size, timeline, milestones. | Board-speak → guide-speak. |
| 3 | `Canary_Agent_Briefing_v1.0.html` | Agent swarm model — how the team is structured. | 14-agent team model, role descriptions. | Needs context framing for guide audience. |
| 4 | `Canary_Marketing_Site_v2.0.html` | Public-facing feature descriptions and value propositions. | Feature summaries, module descriptions. | **Verify module names match canonical set before lifting any text.** |
| 5 | **PRD E0-F6** (docx) | Problem statement (Section 1) is excellent Functional Guide source material. | Section 1 problem statement, Section 2 goals. | Already well-written. May lift with minimal adjustment. |

**For the Technical Guide (Architecture, Data Model, Security, Lightning):**

| # | File | Why | What to Lift | What to Rewrite |
|---|------|-----|-------------|-----------------|
| 1 | **CRDM v1.0** (md) | **Primary source.** Three-database architecture, 7 canonical data sources, design patterns, Chirp rule registry. | Nearly everything. This is the authoritative data model reference. | Simplify for Technical Guide audience. Add diagrams. |
| 2 | `Fox_Module_Technical_Specification_v1.0.html` | Fox case management architecture, evidence chain of custody, BOLO network. | Architecture diagrams, table relationships, evidence flow. | Update with Tom B-001 trigger details. |
| 3 | `Canary_Platform_Schema_Complete_v1.0.html` | Detailed schema definitions. | Table structures, column definitions, indexing patterns. | **Cross-reference with CRDM v1.0 for accuracy.** Some definitions may be stale. |
| 4 | **Tom B-001** (md) | Immutability enforcement, hash chain verification, CRDM gap analysis. | P0-1/P0-2 trigger design, P0-3 hash chain spec, CRDM gaps (G1-G3). | Already well-written technical prose. |
| 5 | **PhD.md** Part IX (The Dome) | Lightning Network integration, L402, LNURL-auth, Softwar defense model. | Dome concept, Lightning micropayment architecture, implementation phases. | PhD's theoretical framing needs translation to practical architecture docs. |
| 6 | `Canary_JSONB_Forensic_Analysis_v1.0.html` | Historical context for why line items and tenders were extracted from JSONB. | The forensic analysis methodology. Useful as "how we discovered the problem" narrative. | Historical context only — the extraction is done. |

**Terminology Jess must normalize (see Section 6):** Module names, feature names, Chirp rule naming conventions. Use the terminology table in Section 6 as the normalization guide.

---

## 6. Terminology Reconciliation

| Concept | PhD/Product_Sites Term | PRD/Design Spec Term | CRDM v1.0 Term | Canonical Term | Notes |
|---------|----------------------|---------------------|----------------|----------------|-------|
| Home module | "Dashboard" (prototypes) | "Home" / "Today's View" | — | **Home / Today's View** | Prototypes use "Dashboard" — this is deprecated framing. PRD/Design Spec say "Today's View." |
| Alerts module | "Chirp Engine" (prototype v2.0) | "Chirps" (Design Spec nav) | `alerts` table, `detection_rules` table | **Chirps** | Navigation label is "Chirps." Backend table is `alerts`. Chirp = the user-facing concept. |
| Insights module | "Owl Analytics" (prototype v2.0) | "Owl" (Design Spec nav) | `canary_metrics` database | **Owl** | Animal name is canonical. |
| Investigation module | "Fox Cases" (prototype v2.0) | "Fox" (Design Spec nav) | Fox tables in `canary_app` | **Fox** | Consistent across all sources. |
| Inventory module | — | "Bull" (Design Spec nav) | — | **Bull** | Consistent. |
| Daily operations module | — | "Rooster" (Design Spec nav) | — | **Rooster** | Consistent. Some marketing files may not mention Rooster by name. |
| Treasury/Bitcoin module | — | "Goose" (Design Spec nav) | — | **Goose** | Consistent. |
| Settings | "Settings" (prototype) | "Farm" (Design Spec nav) | — | **Farm** | Design Spec rebrands Settings as "Farm" (settings + team + Goose treasury). |
| Product name | "Canary LP" (all files) | "Guided Operations Companion" (PRD title) / "Canary" (Design Spec) | — | **Canary** is the product. **Guided Operations Companion** is the E0-F6 feature name. | The PRD is for the Companion feature within Canary. Don't conflate product name with feature name. |
| The 6 animal modules | Canary, Owl, Fox, Bull, Rooster, Goose | Canary, Owl, Fox, Bull, Rooster, Goose | — | **Canonical set: Canary (home), Owl (insights), Fox (investigate), Bull (inventory), Rooster (daily), Goose (money)** | Verify marketing site doesn't use alternative names. |
| Command Center | `Canary_Command_Center_v1.0.html` | Not referenced | — | **Deprecated term.** The product is a "Companion," not a "Command Center." | Command Center implies dashboard/control paradigm. Companion implies guided/helpful paradigm. |
| Wizard | Not present in older prototypes | "Guided Wizard" (PRD), "Wizard" (Design Spec) | — | **Wizard** | Core interaction pattern. Every Chirp launches a wizard. |
| Incident Report Form | `Canary_Incident_Report_Form_v1.0.html` | Not referenced (subsumed by wizard pattern) | — | **Deprecated pattern.** Standalone forms are replaced by wizards. | The form's data fields are valid; the standalone form pattern is not. |
| The Dome | PhD.md Part IX | Design Spec Section 7 mentions HTMX/Superset but not "The Dome" | — | **The Dome** is PhD's strategic concept (Softwar defense layer). Not yet a product feature name. | Use in Technical Guide as future architecture, not current feature. |
| ALTO | PhD.md (partnership network) | Not in PRD or Design Spec | — | **ALTO** is a future concept (LP service provider network). Not in MVP scope. | Reference only in Technical Guide future roadmap section. |

---

## Appendix: Quick Reference — File by Audience

### Files Safe to Reference (CURRENT status)

1. `Fox_Module_Technical_Specification_v1.0.html` — Fox case management (Jim, Jess)
2. `Canary_Factory_Process_v2.0.html` — Delivery pipeline (Jim, Jess)
3. `Canary_Agent_Briefing_v1.0.html` — Agent team model (Jess)
4. `Canary_Board_Update_2026-02-21_v1.0.html` — Business context (Jess)
5. `Canary_Marketing_Site_v2.0.html` — Public positioning (Jess, Art for tone)
6. `Canary_LP_Magazine_Article_v2.0.html` — Narrative source (Jess)

### Files Requiring Caveats (STALE status)

7. `Canary_Prototype_v2.0.html` — Counter-example only; dashboard paradigm is deprecated
8. `Canary_CRDM_v2.0.html` — Cross-reference against CRDM v1.0 before using
9. `Canary_Platform_Schema_Complete_v1.0.html` — Cross-reference against Tom B-001
10. `Canary_Incident_Report_Form_v1.0.html` — Standalone form pattern deprecated
11. `Canary_Command_Center_v1.0.html` — "Command Center" framing deprecated

### Files to Ignore

12. `canary_prototype.html` — Superseded by v2.0
13. `Canary_LP_Magazine_Article.html` — Superseded by v2.0
14. `dashboard.html` — Not a Canary product file
15. `Canary_Demo_Site_v1.0.html` — Superseded by Marketing Site v2.0

---

*PhD Alignment Brief v1.0 — February 24, 2026*
*Work order completed. Ready for ALX review and downstream routing to Jim and Jess.*
