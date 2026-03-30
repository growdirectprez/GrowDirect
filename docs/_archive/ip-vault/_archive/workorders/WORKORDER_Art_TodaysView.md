---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# WORK ORDER: Art — Today's View Wireframe
**Dispatched by:** ALX (Chief of Staff)
**Date:** February 24, 2026
**Priority:** 🔴 CRITICAL PATH — Blocks Jim QA scenarios + Jess Companion Guides
**Mode:** COORDINATE (Art owns the design decisions)

---

## Assignment

Design the **Today's View** wireframe — the merchant's first screen after login in the Canary Guided Operations Companion (E0-F6-A).

This wireframe is the anchor for two downstream deliverables:
1. **Jim** needs it to write merchant-perspective QA scenarios and day-in-the-life test scripts
2. **Jess** needs it (along with Jim's QA output) to produce the Functional and Technical Companion Guides

---

## Deliverables

### Primary: Today's View Wireframe
- **Format:** HTML file with inline CSS (single file, no external dependencies)
- **Mobile-first:** 375px viewport as primary, then desktop breakpoint
- **Brand palette:** Ink `#0D1117` / Card `#161B22` / Border `#21262D` / Signal Yellow `#FBBF24` / Accent Gold `#F59E0B`
- **Typography:** Space Grotesk (headings), Inter (body)
- **Annotated:** Include interaction notes as HTML comments or a companion annotation section

### Screen Content (from Design Spec Section 2)
1. **Top bar:** Canary avatar (idle green pulse) + personalized greeting + active Chirp count
2. **Hero Chirp banner:** Health-wave animation, most urgent Chirp, wizard launch CTA
3. **Three opinionated action cards** (max 3, never more): context-aware based on time of day + open Chirps
4. **Health bar:** Tiny, under the CANARY brand lockup

### Design Constraints (Non-Negotiable)
- **90-second screen test:** A new user identifies the #1 action item within 90 seconds
- **Guided, not dashboard:** "Here's what needs your attention" — NOT "here's all your data"
- **WCAG 2.1 AA:** Contrast ratios, touch targets 44px+, no color-only state indicators
- **Progressive disclosure:** Owner sees more than store manager. Role differences annotated.
- **No raw data escape hatches.** Every element either launches a wizard or provides context.

### Secondary: Self-Critique
Run the wireframe through Art's 7-Question Async Critique Template:
1. Merchant job fit — <10 min/day for a 19-year-old part-timer?
2. Guided & opinionated — forcing decisions or leaving too much open?
3. Visual calm/authority — navy/gold palette + whitespace working?
4. Chirp integration — flow correctly launches from triggering Chirp?
5. Accessibility/mobile — readable on phone, touch targets, contrast?
6. Rooster testability — what 2–3 Playwright tests would catch failures?
7. One big improvement — what moves the needle most?

Include the self-critique as an appendix to the wireframe or as a separate markdown file.

---

## Context Files (Read Before Starting)

| File | Path | Why |
|---|---|---|
| Design Spec v1.0 | `Canary_IP/Markdown/Specs/Canary_Guided_Companion_Design_Spec_v1.0.md` | Full creative brief — Sections 1, 2, 6, 8 are primary |
| PRD E0-F6 | `Canary_IP/Documents/Product_Guides/Canary_PRD_E0F6_Guided_Companion_v1.0.docx` | Formal requirements for E0-F6-A (Today's View) |
| Brand Guide v3 | `Canary/brand/BRAND_GUIDE_v3.html` | Color tokens, typography, tone |
| CRDM v1.0 | `Canary_IP/Markdown/Specs/CRDM_v1.0.md` | Data model — what data is available to surface |
| Art's Profile | `Company/Team/Art.md` | Your principles, UX pipeline, critique template |

---

## UX Pipeline

Follow the Qwen Lens pipeline from Art's profile:
```
Art writes UX prompt (constraints + screen spec + brand rules)
→ Qwen generates HTML wireframe (local, $0, ~60s)
→ Opus deep critique (merchant empathy, CRDM alignment, accessibility)
→ Art resolves conflicts, makes final calls
```

---

## Routing When Complete

1. **Jim** — Wireframe goes to Jim for QA scenario mapping (merchant journey clickthrough scripts, day-in-the-life test scenarios for Today's View)
2. **Jess** — Wireframe + Jim's QA output feed Jess's Functional and Technical Companion Guides
3. **Jeremy** — After Jim/Jess review, Jeremy builds the production version

---

## Gate

This wireframe opens the door for:
- Jim to write concrete test scripts against real screens (not abstract specs)
- Jess to produce the two Companion Guide documents with visual references and accurate workflow descriptions
- Jeremy to build the production Today's View after UAT prep

**Do not route to Jeremy for production build until Jim has mapped QA scenarios against the wireframe.**

---

*Work order issued by ALX · February 24, 2026*
*Factory Process Stage: BLUEPRINT*
