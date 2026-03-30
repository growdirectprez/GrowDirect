---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# WORK ORDER: Triangulation — Generic Frontend Blueprint for Vibe Coding

**Work Order ID:** WO-TRI-001
**Date:** February 25, 2026
**Issued by:** ALX (Chief of Staff)
**Priority:** 🔴 HIGH — Parallel track to Jeremy's Sprint 5 Phase 3
**Deadline:** Thursday February 27, 2026 EOD

---

## Mission

Produce a single, comprehensive **Generic Frontend Blueprint** in Markdown format that can be fed directly into an open-source vibe coding platform (Bolt.diy) to generate a working prototype of the Canary merchant-facing application — aligned to the Monday March 3 Level B demo.

This is a **parallel track** to Jeremy's main build. It does NOT replace Jeremy's work. It proves out a tool and workflow where non-developers (Jim, Will, Worm, and eventually merchants themselves) can rapidly prototype and iterate on frontend experiences sitting on top of Canary's rock-solid backend.

---

## The Triangulation — Four Agents, One Blueprint

| Agent | Role in This Work Order | What They Contribute |
|---|---|---|
| **Condor** | Lead Author & Sanitizer | Takes all internal product docs, strips proprietary IP, produces the generic blueprint skeleton. Functional completeness is the quality bar — can someone build from this? |
| **Tom** | Retail Process Validator | Reviews the blueprint to ensure it maps to real retail operations. Validates the API contract — what data the frontend requests, what shapes come back. Ensures the coffee-shop-owner test passes. |
| **PhD** | IP Boundary & Research Depth | Validates that Condor preserved the right bones (novel IP protected, functional value exposed). Adds research-backed substance so the blueprint conveys Canary's value proposition without revealing implementation. |
| **Art** | Visual Specification | Provides the wireframe reference (v1.1 HTML) and design system spec. The blueprint must faithfully describe Art's visual decisions so the vibe coding tool reproduces them. |

---

## Input Documents (Read These First)

All agents must read these before starting:

| # | Document | Location | Why |
|---|---|---|---|
| 1 | Art's Today's View Wireframe v1.1 | `_ALX/WorkOrders/output/Art/TodaysView_Wireframe_v1.1.html` | THE visual truth. The blueprint must describe this screen precisely enough for a vibe coder to reproduce it. |
| 2 | Art's Self-Critique v1.1 | `_ALX/WorkOrders/output/Art/TodaysView_SelfCritique_v1.1.md` | Design decisions, icon specs, component details. |
| 3 | Jim's QA Summary Brief 2C | `_ALX/WorkOrders/output/Jim/Jim_QA_Summary_Brief_2C.md` | The merchant-perspective plain-language description of every screen and flow. This IS the functional spec in human terms. |
| 4 | Jim's Wizard Flow QA Mapping | `_ALX/WorkOrders/output/Jim/Jim_2B_Wizard_Flow_QA_Mapping.md` | Step-by-step wizard flows with happy path, edge cases, evidence chain. |
| 5 | Jess's Functional Companion Guide v1.0 | `_ALX/WorkOrders/output/Jess/Canary_Functional_Companion_Guide_v1.0.docx` | Business-audience feature documentation. |
| 6 | Jess's Technical Companion Guide v2.0 | `_ALX/WorkOrders/output/Jess/Canary_Technical_Companion_Guide_v2.0.docx` | Architecture and technical feature documentation. |
| 7 | PhD Alignment Brief | `_ALX/WorkOrders/output/PhD/PhD_Alignment_Brief.md` | Terminology reconciliation, file inventory, CRDM alignment. |
| 8 | Brand Guide | `Canary/brand/BRAND_GUIDE_v3.html` | Colors, typography, tone for web/screen output. |

---

## Deliverable: The Generic Frontend Blueprint

**Format:** Single Markdown file
**Location:** `_ALX/WorkOrders/output/Triangulation/Canary_Generic_Frontend_Blueprint_v1.0.md`
**Audience:** An AI vibe coding tool (Bolt.diy) that will read this file and generate a working React/HTML frontend.

### Blueprint Structure

The Markdown file must contain the following sections, in this order:

#### Section 1: Application Overview
- What this app does (1 paragraph, plain language, no proprietary terms)
- Target user: small retail merchant, 1-6 locations, mobile-first
- Platform: Progressive Web App, React, responsive
- Tone: calm, opinionated, guided — NOT a dashboard

#### Section 2: Design System
- Color tokens (from Brand Guide — Signal Yellow, Deep Blue, Health Green, etc.)
- Typography (Inter + Space Grotesk for web/screen per Brand Guide)
- Spacing scale, border radius, shadow levels
- Icon system: 6 custom SVG icons described with geometric construction specs (from Art's v1.1 self-critique)
- Animation: health-wave gradient, bird pulse states (idle, thinking, sleeping)
- Hard rules: max 3 action cards, no charts, no tables, one-number scorecards

#### Section 3: Screen Specifications

**Screen 3.1: Today's View (Home)**
- Full layout description top-to-bottom (from Jim's 2C brief Section 1)
- Top bar: avatar, greeting, Chirp count
- Hero Chirp banner: color gradient, tappable, wizard launcher
- Chirp peek indicator: conditional render logic
- Action cards: time-of-day algorithm, max 3, module icons
- Health bar: thin gradient indicator
- Bottom navigation: 6 module icons with active/inactive states
- Role-based differences table (Owner vs. Manager)

**Screen 3.2: Chirp Detail / Wizard Launcher**
- What happens when merchant taps a Chirp
- Transition to wizard flow

**Screen 3.3: Process 1 — Open the Store**
- 4-step wizard (from Jim's 2C Section 3)
- Step descriptions, input types, completion state

**Screen 3.4: Process 2 — Count the Drawer**
- 5-step wizard
- Variance calculation display
- Conditional completion (confetti vs. serious tone)

**Screen 3.5: Process 3 — Resolve Refund Alert**
- 5-step wizard
- Role-based step variations
- Line-item detail display

**Screen 3.6: Process 4 — Resolve Cash Drawer Shortage**
- 6-step wizard (most detailed)
- Photo evidence step
- Employee lookup step
- Cause category selection
- Role-based escalation options
- Prevention tip display

**Screen 3.7: Scorecards (5 types)**
- Single-card pattern: one number, one trend arrow, one action button
- Where each scorecard appears (contextual, not dashboard)
- Access control per scorecard

**Screen 3.8: Bottom Navigation States**
- 6 module icons with active/inactive/disabled states
- Role-based module visibility

#### Section 4: Error States
- Full error state table (from Jim's 2C Section 6)
- Bird animation states for each error type
- Retry and fallback patterns

#### Section 5: Data Shapes (API Contract)
- Generic JSON shapes for each screen's data needs
- NO table names, NO column names, NO trigger logic
- Example: `{ "greeting": "Good morning, Alex", "chirp_count": 2, "chirps": [...] }`
- Condor: strip all CRDM specifics. Tom: validate the shapes are complete and correct.

#### Section 6: Navigation Flow Map
- Screen-to-screen transitions as a simple flow diagram (Markdown/Mermaid)
- Entry points, wizard launches, completion returns, error redirects

#### Section 7: Seed Data Specification
- Realistic demo data for a specialty coffee chain (5-6 locations)
- Product mix: lattes, pastries, tips
- 30+ transactions with 2-3 active Chirps
- 1 resolved Chirp for history
- Cash drawer shifts with variance scenarios
- Enough data to make every screen look real

---

## Sanitization Rules (Condor Enforces)

| Category | Rule |
|---|---|
| Company names | "GrowDirect" → not mentioned. "Canary" → "the platform" or a generic product name |
| CRDM details | NO table names, column names, trigger logic, hash chain specifics |
| Detection algorithms | NO Chirp rule names, thresholds, or detection logic internals |
| Lightning/Dome | NOT included in MVP blueprint (future phase) |
| Team members | NO agent names (Jim, Jess, Art, Tom, etc.) |
| Business metrics | Generic placeholder values only |
| PhD thesis content | NOT included — research framework is Crown Jewels |
| Square integration | Generic "POS integration" — no Square-specific API details |

**Condor's functional completeness test:** After sanitization, can Bolt.diy generate a working prototype from this blueprint? If yes, the sanitization preserved the right bones. If no, Condor over-redacted. PhD reviews for IP safety. Tom reviews for functional completeness.

---

## Tool Selection: Bolt.diy

**Selected platform:** [Bolt.diy](https://github.com/stackblitz-labs/bolt.diy) (MIT license, open source)
**Rationale:**
- Self-hostable via Docker (we already run Docker infrastructure)
- Native MCP (Model Context Protocol) integration
- Supports Anthropic, Ollama, and Qwen (aligns with local-first rule)
- Generates full-stack React apps from natural language prompts
- Active community with 40k+ GitHub stars
- Supabase-style database connectors (we'd point at Canary's API layer instead)

**Backup:** [Dyad](https://github.com/dyad-sh/dyad) (Apache 2.0, fully local, MCP support)

**Who evaluates the tool:** Tom + PhD jointly recommend which platform to use. Tom evaluates from a "does this actually work for a small retailer" perspective. PhD evaluates from an IP safety perspective (what data does the tool see? where does generated code live?). Final recommendation in the blueprint.

---

## Timeline

| Day | Who | What |
|---|---|---|
| **Wed Feb 26** | Condor | Reads all 8 input docs. Produces first draft of sanitized blueprint skeleton. |
| **Wed Feb 26** | Art | Reviews Section 2 (Design System) and Section 3.1 (Today's View) for visual fidelity. Provides corrections. |
| **Thu Feb 27 AM** | Tom | Reviews full blueprint for retail process accuracy and API contract completeness. Validates Section 5 (Data Shapes) and Section 7 (Seed Data). |
| **Thu Feb 27 AM** | PhD | Reviews full blueprint for IP safety. Validates Condor's sanitization. Confirms no Crown Jewels leaked. |
| **Thu Feb 27 PM** | Condor | Incorporates Tom + PhD + Art feedback. Produces final v1.0 blueprint. |
| **Fri Feb 28** | Jeremy (or ALX) | Feeds blueprint into Bolt.diy. Generates prototype. Jim tests on phone. |
| **Mon Mar 3** | Jim | If prototype works: use as backup/supplement to Jeremy's main build for Offset Coffee demo. |

---

## Success Criteria

1. **Functional completeness:** A person with no Canary knowledge can read the blueprint and understand what every screen does.
2. **IP safety:** Condor, PhD, and Syd (spot check) confirm zero Crown Jewels in the output.
3. **Visual fidelity:** Art confirms the blueprint describes his v1.1 wireframe accurately enough for reproduction.
4. **Retail validity:** Tom confirms the process flows, data shapes, and navigation map are correct for a real merchant.
5. **Vibe-code ready:** The blueprint, when fed to Bolt.diy as a prompt, produces a recognizable prototype of Today's View within 30 minutes.

---

## Routing After Delivery

- **Jim:** Tests the Bolt.diy prototype on phone alongside Jeremy's build. Reports gaps.
- **Will + Worm:** If the workflow proves out, they become the first non-developer users of the vibe coding tool for rapid landing page and merchant-facing prototyping.
- **Eva:** Tracks this as a parallel workstream. Does NOT replace Jeremy's Sprint 5 deliverables. Additive only.
- **Syd:** Spot-checks the blueprint before it enters any external tool. Pre-flight IP check.

---

## Long-Term Vision (What This Proves Out)

If this works, the architecture becomes:

```
HARD CORE (never changes fast, never should):
  CRDM + Immutability Triggers + Hash Chain + Detection Engine + APIs

SOFT SHELL (changes daily, vibe-coded):
  React frontends generated from natural language prompts
  Connected to hard core via MCP + API contracts
  Anyone on the team can prototype new screens
  Merchants can eventually describe what they want and see it

EXTENSION LAYER (fail fast, iterate fast):
  Third-party views built on the API
  Jim prototypes new QA flows
  Will builds merchant-facing landing pages
  Worm generates SEO content pages
  New ideas ship in hours, not sprints
```

This is Alejandro's "hard core, soft shell" architecture. Bitcoin-standard data integrity underneath. Vibe-coded interfaces on top. The blueprint is step one.

---

*Work Order issued by ALX — February 25, 2026*
*Factory Process Stage: Blueprint (parallel track)*
*Canary LP | Confidential*
