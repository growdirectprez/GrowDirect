---
title: PwC eBusiness Web Implementation Guide (Definition / Design / Development)
type: methodology-template
status: v0.1
tags: [consulting, methodology, pwc, ebiz, branch-b, 2000, web-implementation, template]
created: 2026-04-24
updated: 2026-04-24
related:
  - "[[third-branch]]"
  - "[[broadvision-1999-2000-platform]]"
  - "[[bp-consulting-library-1997-1999]]"
  - "[[katz-scm-2003-archetype]]"
sources:
  - Brain/raw/.extract/EBiz Def Des Dev/Sample Web Impl Guide - Def.doc.md
  - Brain/raw/.extract/EBiz Def Des Dev/Sample Web Impl Guide - Des.doc.md
  - Brain/raw/.extract/EBiz Def Des Dev/Sample Web Impl Guide - Dev.doc.md
last-compiled: 2026-04-24
needs-review: 2026-05-08
---

# PwC eBusiness Web Implementation Guide (Definition / Design / Development)

**Governing thesis.** The PwC eBusiness Web Implementation Guide, dated circa September–October 2000, is the formal artifact-form of [[third-branch|Branch B]] — the "strategy consulting got the questions right but shipped discrete labor" branch. It is a three-phase engagement methodology — Definition → Design → Development — with prescribed work products, Excel-matrix templates, and sample outputs for every deliverable. Its grammar is humans-doing-work-for-N-weeks-then-stopping; continuous instrumentation does not exist in its vocabulary. The deliverables *were* the product.

The template is unusually candid — a working engagement playbook, not a marketing deck, with blank "Sample Work Product — TBD" placeholders, cross-references to specific client artifacts (Bank / SBS Portal, Fleet), and embedded Visio workstream diagrams. Branch B's skeleton without the paint.

---

## 1. Three-phase structure

Five parallel workstreams — Business & Creative, Content, Organizational Readiness, Technology, Testing — gate through three sequential phases.

| Phase | Workstream count | Work products per workstream | Decision gate |
|---|---|---|---|
| **Definition** | 5 | Business & Creative (10), Content (6), Organizational Readiness (4), Technology (6), Testing | Release Functionality Matrix + Go/no-go to Design |
| **Design** | 5 | Creative treatments, Categorization hierarchy, Job profiles & hiring reqs, Web page program + Data architecture + Infrastructure + Interface/Batch/Migration design | Environment build-out + Go/no-go to Development |
| **Development** | 5 | Publishing workflows, Data model build, External interface code, Unit test plans, Stress/performance test | Cutover |

Handoff is explicit: Definition produces the "Release Functionality Matrix" that constrains Design; Design produces the Blank Detailed Design Template (Purpose, Page Layout, Session Information, Edit/Validation, Object Event, Pseudo Code, Exception Handling, Components Required, Dependencies, Issues) that constrains Development. Each phase is a gated deliverable package, not a continuous flow.

**Source:** `Def.doc.md` TOC L25–143; `Des.doc.md` TOC L25–211; `Dev.doc.md` TOC L24–91 (all in `Brain/raw/.extract/EBiz Def Des Dev/`).

---

## 2. The operating-model questions the methodology asked

The Definition phase's question list is the Branch-B thesis in action. These are genuinely the right questions for 2000-era eBusiness strategy:

| # | Question category | Work product in the template |
|---|---|---|
| 1 | Who are the end users and what do they need? | User Types and Needs matrix |
| 2 | How do we segment customers? | Customer Segmentation Strategy |
| 3 | What does the business require, prioritized? | Requirements Matrix |
| 4 | What tasks will the system support? | High-Level Use Case List + Detailed Use Cases (Façade/Filled/Focused/Finished iteration) |
| 5 | How is the site navigated? | Preliminary Site Map + Functional Storyboards |
| 6 | What business rules govern the system? | Business Rules Catalog |
| 7 | How is content personalized? | ERM Classifiers, Qualifiers, Programs, Channels |
| 8 | What content exists vs. what's needed? | Content Inventory, User Content Needs, Gap Analysis |
| 9 | Who authors, reviews, publishes? | Authors, Roles and Workflow |
| 10 | Is the organization ready to run this? | Current Organizational Structure + Skills + Training Needs |
| 11 | What are the back-end integration points? | Interface / Batch / Data Migration Architecture |
| 12 | What's the infrastructure build? | Technical Infrastructure (as-is → to-be, environment strategy, config management) |
| 13 | What do we report on? | Reporting Requirements Definition |
| 14 | How do users search? | Search Requirements (incl. Verity gap analysis) |
| 15 | How do we test it? | Testing Workstream (unit / performance / stress) |

Every one of these questions survives into 2026. What has not survived is the *form* of the answer — a bound stack of Excel matrices and Word templates, frozen at hand-off.

---

## 3. Artifact families

The template specifies the *file type* for each output:

- **Excel matrices** — User Types/Needs, Requirements, Use Case lists, Business Rules, Content Inventory, ERM Classifiers. ("The typical working document is prepared and managed in an MS Excel worksheet in a matrix form that provides for ease of manageability and organization." — Def.md L219, repeated near-verbatim across sections.)
- **Word templates** — Detailed Use Cases; Detailed Design specs (10-section template: Purpose, Page Layout, Session Information, Edit/Validation, Object Event, Pseudo Code, Exception Handling, Components Required, Dependencies).
- **Photoshop mock-ups** — Creative Treatments ("A creative treatment is typically a Photoshop mock-up of the web page layout, to define colors, images or a 'user experience.'" — Des.md L281).
- **Visio workstream diagrams** — one per workstream, embedded at each phase front.
- **Generated HTML/JSP** — the Development phase ships actual code samples (INBOX.JSP, New_ip.jsp) preserved verbatim — 200+ lines of BroadVision-specific JavaScript / JSP.

---

## 4. The discrete-labor evidence

The methodology is organized *by role and deliverable*, not by continuous service. The Development phase is a checklist of one-time produce-and-verify tasks: "Develop Publishing Workflows," "Develop Instant Publisher Forms," "Implement Third Party Tools," "Develop Data Model," "Design Low-Level External Interface," "Develop External Interface," "Load and Tag Content," "Develop Business Rules" (Dev.md L126–132).

Three grammatical features give the labor model away:

1. **Estimates are hour-denominated.** Definition-phase effort estimates appear as explicit hour counts — "268.8," "211.2," "28.8" (Def.md L703, L776, L711) — tied to use cases. Time-and-materials language, not subscription language.
2. **"Release" is terminal.** Every use case carries a Rel 1 / Rel 2 / Other flag. Post-release operations are explicitly out of scope: "Fulfillment process for customer application follow-up. […] N/A — Not in scope for phase 1" (Def.md L726–730).
3. **Technology is vendor-specific and pre-purchased.** The Technology workstream is written *around BroadVision* — "Review BroadVision 'Out of the Box' Functionality," "Design Physical BroadVision Data Model," "Design BroadVision Schema for External Data Sources" (Des.md L115, L159, L165). The consultants integrate against a licensed product, then leave.

There is no post-launch operating model, no telemetry-driven iteration. Testing terminates in "Perform Stress Test." After that, the engagement ends.

---

## 5. What this template proves

The 18 PwC / IBM / MH client decks catalogued in [[third-branch]] §I.B — Guess, Saks, JCP, Rocketstop, JVP, Swindon, Swarovski, Kenneth Cole, Muji, VF, Sports Authority, Staples, Morrisons, Lenox, Talbots — were produced against some close relative of *this* template. That is why they look the way they look: phase-gated slideware, matrices, org charts, business-case ROI, and a cutover date. The questions were right. The artifact form was a dead-end. Branch C keeps the question list and replaces the Word-and-Excel artifact with a running instrumented system.

---

## 6. Threads

- [[third-branch]] §I.B — the existing client-deck quote list belongs to the same era and came off this or an adjacent template.
- [[broadvision-1999-2000-platform]] *(pending)* — the technology-branch sibling; this PwC template is written *around* BroadVision.
- [[katz-scm-2003-archetype]] *(pending)* — concrete engagement applying the same or successor methodology 2.5 years later, post-dot-com.
- [[bp-consulting-library-1997-1999]] *(pending)* — earlier PwC / MH consulting library; shows methodology evolution into this 2000 template.

**Sources:** raw at `Brain/raw/inbox/EBiz Def Des Dev/Sample Web Impl Guide {Def,Des,Dev}.doc`; extract markdown at `Brain/raw/.extract/EBiz Def Des Dev/Sample Web Impl Guide {Def,Des,Dev}.doc.md` (primary citation target).
