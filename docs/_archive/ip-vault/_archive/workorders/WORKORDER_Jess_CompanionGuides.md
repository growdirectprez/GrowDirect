---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# WORK ORDER: Jess — Canary Companion Guides (Functional + Technical)
**Dispatched by:** ALX (Chief of Staff)
**Updated by:** Eva (Program Manager) — February 24, 2026
**Date:** February 24, 2026
**Priority:** 🔴 HIGH — Both upstream dependencies DELIVERED. All sections draftable NOW.
**Mode:** DISPATCH (Eva owns the ask, Jess owns the output)

---

## Status Update (Eva, Feb 24)

**Both upstream blockers are RESOLVED:**
- ✅ **PhD Alignment Brief** — DELIVERED at `_ALX/WorkOrders/output/PhD/PhD_Alignment_Brief.md`
- ✅ **Art v1.1 wireframe** — DELIVERED at `_ALX/WorkOrders/output/Art/TodaysView_Wireframe_v1.1.html`

**ALL sections of BOTH Companion Guides are now draftable.** The PhD brief provides file currency assessment, curated reading lists, and the terminology reconciliation table. Art v1.1 provides the finalized Today's View wireframe with custom SVG icons and Chirp peek indicator.

**One soft dependency remains:** Functional Guide Section 5 (merchant workflows) benefits from Jim's QA Summary Brief (2C). Jim is now dispatched and working on it. Jess should **draft Section 5 from existing specs and refine when Jim's 2C arrives.** This is NOT a blocker — it's a refinement opportunity.

---

## ⚠️ MANDATORY PRE-READ: PhD Terminology Reconciliation

Before writing ANY section of either guide, read the **Terminology Reconciliation Table** in PhD Alignment Brief Section 6 (`_ALX/WorkOrders/output/PhD/PhD_Alignment_Brief.md`). Key terms Jess must use consistently:

| Concept | WRONG Term | CORRECT Term |
|---|---|---|
| Home screen | "Dashboard" | **Today's View** |
| Alert module | "Chirp Engine" | **Chirps** |
| Navigation module names | Various | **Canary, Owl, Fox, Bull, Rooster, Goose** |
| Settings | "Settings" | **Farm** |
| Product feature | "Canary LP" (as feature name) | **Guided Operations Companion** (the E0-F6 feature); **Canary** (the product) |
| Interaction pattern | "Incident Report Form" | **Guided Wizard** (standalone forms are deprecated) |
| Control paradigm | "Command Center" | **Companion** (guided, not command-and-control) |
| The Dome | PhD's strategic concept | Use in Technical Guide as **future architecture**, not current feature |
| ALTO | Partnership network concept | **Not in MVP scope.** Reference only in Technical Guide future roadmap section |

---

## PhD Alignment Brief Integration

### File Currency Assessment (PhD Section 1)

The PhD brief audited all 19 HTML files in `Product_Sites/`. Jess must check PhD Section 1 before referencing ANY Product_Sites file:

| Status | Count | Jess Action |
|---|---|---|
| **CURRENT** | 6 | Safe to reference |
| **STALE** | 5 | Reference with caveats — product has evolved past these |
| **SUPERSEDED** | 3 | Do NOT reference — newer version exists |
| **REFERENCE ONLY** | 4 | Historical context only — not authoritative |
| **NOT APPLICABLE** | 1 | `dashboard.html` — not a Canary file |

### PhD-Curated Reading Lists for Jess (Section 5)

**For the Functional Guide:**

| # | File | Why | What to Lift | Watch For |
|---|---|---|---|---|
| 1 | `Canary_LP_Magazine_Article_v2.0.html` | Best narrative source. Problem framing, competitive positioning, Bitcoin-native differentiation. | Problem framing ("33 million SMB retailers"). | Tone adjustment from marketing to guide voice. |
| 2 | `Canary_Board_Update_2026-02-21_v1.0.html` | Business metrics, progress milestones. | Market size, timeline, milestones. | Board-speak → guide-speak. |
| 3 | `Canary_Agent_Briefing_v1.0.html` | Agent swarm model — team structure context. | 14-agent team model, role descriptions. | Needs context framing for guide audience. |
| 4 | `Canary_Marketing_Site_v2.0.html` | Public-facing feature descriptions. | Feature summaries, module descriptions. | **Verify module names match canonical set.** |
| 5 | PRD E0-F6 (docx) | Problem statement (Section 1) is excellent source material. | Section 1 problem statement, Section 2 goals. | May lift with minimal adjustment. |

**For the Technical Guide:**

| # | File | Why | What to Lift | Watch For |
|---|---|---|---|---|
| 1 | CRDM v1.0 (md) | **Primary source.** Three-database architecture, 7 data sources, Chirp rule registry. | Nearly everything. | Simplify for Technical Guide audience. Add diagrams. |
| 2 | `Fox_Module_Technical_Specification_v1.0.html` | Fox case management architecture, evidence chain of custody. | Architecture diagrams, table relationships, evidence flow. | Update with Tom B-001 trigger details. |
| 3 | `Canary_Platform_Schema_Complete_v1.0.html` | Detailed schema definitions. | Table structures, column definitions. | **Cross-reference with CRDM v1.0 for accuracy — some definitions may be stale.** |
| 4 | Tom B-001 Output (md) | Immutability enforcement, hash chain verification, CRDM gap analysis. | P0-1/P0-2 trigger design, P0-3 hash chain spec. | Already well-written technical prose. |
| 5 | PhD.md Part IX (The Dome) | Lightning Network integration, L402, LNURL-auth. | Dome concept, Lightning micropayment architecture. | PhD's theoretical framing needs translation to practical architecture docs. |
| 6 | `Canary_JSONB_Forensic_Analysis_v1.0.html` | Historical context for line item/tender extraction from JSONB. | Forensic analysis methodology. | Historical context only — the extraction is done. |

---

## Assignment

Produce two Word documents that serve as condensed but thorough overviews of the Canary LP platform and the solution it brings to market. These are companion guides — not exhaustive reference manuals, but authoritative documents that give a reader a complete understanding of what Canary is, how it works, and why it matters.

**Audience intent:** Someone reading these guides should walk away understanding the full picture — the business problem, the product solution, the technical architecture, and how it all fits together. Think "the document you hand to a serious partner, investor, or enterprise prospect who wants substance, not slides."

---

## Deliverables

### Document 1: Canary Functional Companion Guide

**Audience:** Business stakeholders — investors, partners, enterprise prospects, board members, merchant decision-makers
**Tone:** Direct, professional, reader-first. No jargon inflation. Canary's brand voice: authoritative but approachable.
**Length:** Condensed — aim for 15–25 pages. Thorough, not padded.

**Content Structure:**

1. **Executive Summary** — What Canary is, who it serves, what problem it solves. One page max.

2. **The Problem** — Small merchant loss prevention today: no tools, no budget, no expertise. The gap between enterprise LP and SMB reality. Why this matters (shrinkage costs, employee trust, operational blind spots).

3. **The Canary Solution** — Platform overview. The Guided Operations Companion as the core experience. The six modules (Canary/Chirps, Owl, Fox, Bull, Rooster, Goose) and what each does in plain language.

4. **How It Works — The Merchant Experience** *(Art v1.1 wireframe now available)*
   - Today's View: what the merchant sees when they open the app — **use Art v1.1 wireframe** (`_ALX/WorkOrders/output/Art/TodaysView_Wireframe_v1.1.html`) as visual reference
   - Chirps: how alerts work, what triggers them, how they're resolved
   - Guided Wizards: the step-by-step resolution flow (use Process 4 as the worked example)
   - Scorecards: contextual analytics, role-gated, never overwhelming
   - Evidence capture: how merchants document incidents (frictionless, chain-of-custody compliant)
   - **Include annotated screenshots or wireframe excerpts from Art v1.1**
   - **Note the v1.1 Chirp peek indicator** — shows "+1 more" when multiple Chirps active

5. **Role-Based Experience** — What owners see vs. managers vs. part-timers. Progressive disclosure explained.
   - **Note:** This section benefits from Jim's QA Summary Brief (2C). Jim is now dispatched. **Draft from Design Spec + PRD; refine when Jim's 2C arrives** at `_ALX/WorkOrders/output/Jim/Jim_QA_Summary_Brief_2C.md`.

6. **The 8 Core Processes** — One paragraph each for the 8 guided processes. MVP scope (1–4) clearly marked.

7. **Security & Data Integrity** — The immutability model explained for a business reader. INSERT-only evidence, hash chain verification, blockchain anchoring. Why merchants can trust the data.

8. **Platform Integration** — Square POS as primary data source. Future integrations (Shopify, Clover). How Canary fits into the merchant's existing stack.

9. **Bitcoin-Native Infrastructure** — Lightning payments explained in merchant language ("instant payments," "tap to log in," "pay-per-use access"). The economic model (why micropayments matter for SMB pricing). No crypto jargon.

10. **What's Next** — Roadmap highlights. Alpha → Beta → GA timeline. Where the platform is headed.

**Visual Assets:** Include wireframe excerpts from Art v1.1 (Today's View, wizard flow). Include any relevant brand assets (logo, palette swatches) per brand guide.

---

### Document 2: Canary Technical Companion Guide

**Audience:** Technical evaluators — CTOs, engineering leads, integration partners, security reviewers, due diligence teams
**Tone:** Precise, technical, no hand-waving. Assume the reader knows what PostgreSQL, Docker, and REST APIs are.
**Length:** Condensed — aim for 20–30 pages. Thorough coverage without becoming a reference manual.

**Content Structure:**

1. **Technical Executive Summary** — Architecture at a glance. Stack overview. Key design decisions.

2. **System Architecture** — High-level architecture diagram description. Frontend (Tailwind + HTMX + Alpine.js), Backend (Flask/Python), Database (PostgreSQL, three-database model: canary_app, canary_sales, canary_metrics), Cache (Valkey), Orchestration (Docker Compose), BI (Superset, owner-only).

3. **Data Model — CRDM** — The Canonical Retail Data Model explained. Source tables from Square. Derived tables for analytics. The mapping from POS data → Canary intelligence. Reference CRDM v1.0 but summarize — don't reproduce.

4. **The Immutability Model** — INSERT-only triggers on financial and evidence tables. Hash chain verification (pgcrypto, SHA-256). Tamper detection. Why this matters for evidence integrity and legal defensibility. Reference Tom's P0-1/P0-2/P0-3 specifications.

5. **Chirp Rule Engine** — How detection rules work. Rule types (threshold, pattern, anomaly). How Chirps fire, how they're delivered, how they connect to guided wizards. The pipeline: data ingestion → rule evaluation → Chirp generation → wizard launch.

6. **Fox Case Management** — Evidence chain of custody. Case lifecycle. How merchant-captured evidence (photos, notes) flows into the forensic record. Ordinal anchoring concept.

7. **The Guided Operations Companion — Technical View** — HTMX-powered wizard engine. Endpoint architecture (`/wizard/step/{process}/{step}`). How wizards consume backend data. How evidence is captured and stored. Progressive disclosure implementation (role-based rendering). **Reference Art v1.1 wireframe for UI target.**

8. **Integration Architecture** — Square OAuth 2.0 flow. Webhook subscriptions. Data sync patterns. API scopes (CASH_DRAWER_READ, TIMECARDS_READ, INVENTORY_READ, GIFTCARDS_READ, etc.). Future integration pattern for Shopify/Clover.

9. **Infrastructure & Deployment** — Docker Compose stack. Database migrations (Alembic). Environment strategy (dev → staging → production). Monitoring and health checks. The Rooster automated test suite (Quick Crow, Feature Patrol, Full Strut).

10. **Security Model** — Authentication (LNURL-auth, session management). Authorization (RBAC: owner, manager, part-timer). Data encryption at rest and in transit. Audit trail design. The Dome anti-spam infrastructure (L402 gates).

11. **Lightning & Bitcoin Infrastructure** — L402 middleware. LNURL-auth implementation. Micropayment pricing model. Goose treasury management. Integration with LNbits/Alby/ZBD.

12. **Development Practices** — Factory Process (Blueprint → Parts → Assembly → QC → Packaging → Ship). Local-first LLM strategy (Qwen + Claude). Test coverage model. CI/CD pipeline.

13. **Open Source Stack & Licensing** — Full dependency table with license status. Valkey (BSD-3), Directus (BSL 1.1 — under review), Grafana (AGPL — under review). Zero vendor lock-in philosophy.

---

## Format & Standards

Both documents MUST follow Jess's documentation standards:

| Standard | Requirement |
|---|---|
| **Template** | Canary Document Template (`Canary/brand/Canary_Document_Template.docx`) |
| **Brand Guide** | Full compliance with `Canary/brand/BRAND_GUIDE_v3.html` — typography, colors, tone, layout |
| **Typography** | Space Grotesk (headings), Inter (body) |
| **Color tokens** | Ink `#0D1117`, Signal Yellow `#FBBF24`, Health Green, per brand guide |
| **Version** | v1.0 for both documents |
| **Date** | Date of completion |
| **Audience** | Clearly stated on title page |
| **Classification** | Internal — Confidential (investor-ready but not public) |
| **Standing rule** | No virtual team member names in external-facing output (Jeffe directive, Feb 2026) |
| **Standing rule** | No real third-party names externally without explicit Jeffe approval |
| **Terminology** | All terms must conform to PhD Alignment Brief Section 6 reconciliation table |

---

## Context Files (Full Reading List)

| File | Path | Priority |
|---|---|---|
| PhD Alignment Brief | `_ALX/WorkOrders/output/PhD/PhD_Alignment_Brief.md` | **READ FIRST — Section 6 terminology, Section 1 file currency, Section 5 reading lists** |
| Art v1.1 Wireframe | `_ALX/WorkOrders/output/Art/TodaysView_Wireframe_v1.1.html` | **READ FIRST — visual reference for Functional Guide Section 4** |
| Art v1.1 Self-Critique | `_ALX/WorkOrders/output/Art/TodaysView_SelfCritique_v1.1.md` | HIGH — design rationale, known gaps, v1.1 changes |
| Design Spec v1.0 | `Canary_IP/Markdown/Specs/Canary_Guided_Companion_Design_Spec_v1.0.md` | **READ FIRST** |
| PRD E0-F6 | `Canary_IP/Documents/Product_Guides/Canary_PRD_E0F6_Guided_Companion_v1.0.docx` | **READ FIRST** |
| CRDM v1.0 | `Canary_IP/Markdown/Specs/CRDM_v1.0.md` | HIGH |
| Tom's B-001 Output | `Canary_IP/Markdown/Alpha3X/output/TOM_SESSION_OUTPUT_B-001_2026-02-24.md` | HIGH (Technical Guide) |
| Attack Plan v3.0 | `Canary_IP/Markdown/Strategy/Canary_Attack_Plan_v3.0.md` | MEDIUM |
| Brand Guide v3 | `Canary/brand/BRAND_GUIDE_v3.html` | HIGH (format compliance) |
| Canary Document Template | `Canary/brand/Canary_Document_Template.docx` | HIGH (template) |
| Factory Process | `Canary_IP/Markdown/Strategy/Canary_Factory_Process_v1.0.md` | Technical Guide |

---

## Input Dependencies (Updated)

| Input | Source | Status |
|---|---|---|
| Art's Today's View wireframe v1.1 | Art | ✅ DELIVERED |
| PhD Alignment Brief | PhD | ✅ DELIVERED |
| Jim's QA Summary Brief (Phase 2C) | Jim | 🔄 IN PROGRESS — Jim dispatched today. Jess drafts Section 5 now, refines when 2C arrives. |
| Design Spec v1.0 | `Canary_IP/Markdown/Specs/Canary_Guided_Companion_Design_Spec_v1.0.md` | ✅ AVAILABLE |
| PRD E0-F6 | `Canary_IP/Documents/Product_Guides/Canary_PRD_E0F6_Guided_Companion_v1.0.docx` | ✅ AVAILABLE |
| CRDM v1.0 | `Canary_IP/Markdown/Specs/CRDM_v1.0.md` | ✅ AVAILABLE |
| Tom's B-001 Architecture Output | `Canary_IP/Markdown/Alpha3X/output/TOM_SESSION_OUTPUT_B-001_2026-02-24.md` | ✅ AVAILABLE |
| Attack Plan v3.0 | `Canary_IP/Markdown/Strategy/Canary_Attack_Plan_v3.0.md` | ✅ AVAILABLE |
| Brand Guide v3 | `Canary/brand/BRAND_GUIDE_v3.html` | ✅ AVAILABLE |
| Canary Document Template | `Canary/brand/Canary_Document_Template.docx` | ✅ AVAILABLE |

**ALL sections of BOTH guides are now draftable.** Section 5 of Functional Guide (merchant workflows) refines when Jim's 2C Brief arrives — but Jess can and should draft it from Design Spec + PRD now.

---

## Routing When Complete

1. **Eva** reviews both documents for completeness and accuracy
2. **Syd** reviews for any legal/compliance/IP concerns (standing rule: all external-ready docs)
3. **Jeffe** final approval before any distribution
4. Filed to `Canary_IP/Documents/` with version control

---

## Gate

These documents are **investor-ready and partner-ready** once approved. They are the condensed authority on what Canary is and how it works. They do not ship until:
- Art's wireframe is incorporated (visual references) ✅ DELIVERED
- Jim's QA perspective is incorporated (merchant workflow accuracy) — 🔄 Jim dispatched, 2C incoming
- PhD terminology is normalized throughout ✅ Table available
- Syd reviews for compliance
- Jeffe approves for distribution

---

*Work order issued by ALX · February 24, 2026*
*Updated by Eva (Program Manager) · February 24, 2026 — PhD brief integration (file currency, reading lists, terminology table), Art v1.1 wireframe reference, all sections confirmed draftable*
*Factory Process Stage: PACKAGING (Documentation ships with product)*
