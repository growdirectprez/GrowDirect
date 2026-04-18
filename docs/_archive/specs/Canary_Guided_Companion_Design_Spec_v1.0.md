---
type: spec
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# Guided Operations Companion — Design Specification v1.0

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

**Date:** February 22, 2026
**Source:** Jeffe Grok Session (82 messages) + Eva synthesis
**Author:** Art (UX/Creative Director), Eva (Program Manager)
**Epic:** E0-F6
**Classification:** Internal — Product Design
**Status:** Design Brief — awaiting PRD formalization and Art wireframes

---

## Jeffe's Directive

> "I want to make sure that we're really taking the time and doing a full cycle to use the Opus 4.6 code execution planning to go back through the site. Look at where our hooks are for all of our testing linked back to the factory process and make sure that we do a couple of things — a full scan for usability, but also a technical scan to make sure we've got the right hooks."

Additionally, Jeffe wants to bring Jim's QA knowledge into an agent — a "virtual gym" that lets Jim focus on analytics while his usability expertise is encoded into an automated test companion.

---

## 1. Overall Architecture — New Navigation Structure

**Stop thinking "dashboard." Start thinking "helpful farmhand that lives in your pocket."**

### Top-Level Navigation (Desktop)

| Nav Item | Description |
|----------|-------------|
| **Home** | Default landing — Today's View |
| **Chirps** | All active alerts, sorted by urgency |
| **Guided Ops** | Library of the 8 core wizards (merchants almost never land here directly) |
| **Scorecards** | The 5 views, role-gated |
| **Farm** | Settings + team + Goose treasury — hidden behind owner role |

### Guided Entry Point

Giant floating "Start My Shift" button on Home that auto-picks the most relevant wizard based on time of day + open Chirps.

### Mobile Navigation

Bottom nav with six animal avatar icons:

| Icon | Module | Purpose |
|------|--------|---------|
| 🐦 Canary | Home/Chirps | Alerts and daily view |
| 🦉 Owl | Insights | Analytics (owner only) |
| 🦊 Fox | Investigate | Case management |
| 🐂 Bull | Inventory | Counts and vendor tracking |
| 🐓 Rooster | Daily | Team performance and routines |
| 🪿 Goose | Money | Treasury and Bitcoin (owner + manager) |

**No sidebar. This is not another enterprise left-nav hell. It is a joyful, opinionated companion.**

---

## 2. Home / Today's View — What the Merchant Sees First

**The attached prototype dumps 17 metrics on load. That is retail-owner PTSD in pixel form. A 19-year-old closer will close the tab.**

### New Home Screen (Mobile-First, <10-Second Scan)

1. **Top bar:** Canary avatar (idle green pulse) + "Good morning, Alex — 2 Chirps need you"
2. **Hero Chirp banner** (health-wave animation from brand guide v3): "Drawer short $18 at Store #1 — 4 min wizard" (yellow → red wave on tap)
3. **Three big opinionated cards** (max 3, never more):
   - "Open the store" (Rooster icon)
   - "Count the drawer" (Bull icon)
   - "Check yesterday's shrink" (Canary icon)
4. **Tiny health bar** under the word "CANARY" (brand guide stacked lockup style)

**Tone:** Calm, authoritative, slightly playful. Green checkmarks feel like "you're winning the day."

---

## 3. Guided Wizard Pattern — Detailed Spec (Process 4 Example)

**Every single Chirp launches a wizard. No exceptions. No "view raw data" escape hatch.**

### Process 4: "Resolve Cash Drawer Shortage"

One of the 8 core processes. Wizard flow: 6 screens max, <8 minutes total.

| Step | Screen | Description |
|------|--------|-------------|
| 1 | **Confirm the fact** (1 tap) | "Was the drawer actually short $18?" Yes / No (with photo upload) |
| 2 | **Who touched it last?** | Pre-filled list of today's closers (opinionated: most likely suspect at top) |
| 3 | **Common causes** | 4 big illustrated cards (brand yellow borders): "Forgot to record a refund" / "Math error at close" / "Theft (I suspect…)" / "None of these — something else" |
| 4 | **Fix it now** | Step-by-step checklist with check-off animation (progress bar uses health-wave colors) |
| 5 | **Learn & prevent** | One-sentence tip + "Add to team playbook" toggle |
| 6 | **Done** | Confetti + chirp sound + "Great job — shrink prevented" |

### Key UX Decisions

- **Progressive disclosure:** Owner sees "Flag for Fox investigation" button at step 3. Manager does not.
- **HTMX swaps** the entire card stack on each "Next." Zero page reloads.
- **Photo upload** at step 1 feeds directly into Fox evidence chain (INSERT-only).

---

## 4. The 5 Scorecards — Embedded and Contextual

**Never on first load. Never raw Superset charts.**

| # | Scorecard | Where It Appears | When It Appears | Who Sees It |
|---|-----------|-------------------|-----------------|-------------|
| 1 | **Daily Shrink Score** | Home widget only | Always (big yellow number + tiny canary waving) | All roles |
| 2 | **Alert Heatmap** | Inside Chirps tab | After resolving 3+ Chirps | All roles |
| 3 | **Team Performance** | Rooster tab | On demand | Owner only |
| 4 | **Inventory Health** | Bull tab | After "Count drawer" wizard completes | Owner + Manager |
| 5 | **Treasury Snapshot** | Goose tab | Behind one extra tap | Owner + Manager |

**Design rule:** Each scorecard is a single calm card with one headline number, one trend arrow, and one "Fix it" button that launches the relevant wizard.

---

## 5. Role-Based Simplification

| Role | Sees | Does NOT See |
|------|------|-------------|
| **Store Manager** (part-timer supervisor) | Home + Chirps + Guided Ops + Rooster + Bull | No Goose, no Fox workbench, no raw data ever |
| **Owner** | Everything unlocked + "Deep dive with Owl" + "Send to accountant" buttons | — |

Switching roles: One tap in Farm → "View as Manager" (for testing).

---

## 6. Mobile Layout — Key Differences

- Bottom nav icons = the six animal avatars (exactly as defined above)
- Home becomes a vertical stack
- Wizard takes full screen, big tap targets (48px+)
- Chirp banner becomes a persistent top toast with the animated bird

---

## 7. Superset + HTMX Integration Plan

- **Superset** stays for the owner's "power user" view only (hidden link in Farm)
- **All merchant-facing views** are pure Tailwind + HTMX + Alpine.js micro-interactions
- Chirp data comes from the backend via simple JSON endpoints
- No one ever sees a Superset chart unless they are the owner explicitly asking for it

---

## 8. Visual & Interaction Standards

### Color Palette (Brand Guide v3 Aligned)

| Token | Value | Usage |
|-------|-------|-------|
| Ink | `#0D1117` | Background |
| Card | `#161B22` | Card backgrounds |
| Border | `#21262D` | 1px card borders |
| Signal Yellow | `#FBBF24` | Every primary button and success state |
| Accent Gold | `#F59E0B` | Secondary accent |
| Text Primary | `#E5E7EB` | Body text |
| Text Muted | `#6B7280` | Secondary text |
| Health Green | (from animated logo) | Good state |
| Health Yellow | (from animated logo) | Warning state |
| Health Red | (from animated logo) | Alert state |

### Micro-Interactions (Joyful but Calm)

- Canary bobs gently on Home (CSS animation, 3s ease-in-out infinite)
- Every completed wizard ends with a single soft chirp sound + 0.8s scale-up animation
- "Next" button pulses yellow for 300ms when ready
- Error states use the red health wave but never scary red text
- **No loading spinners longer than 400ms.** If it takes longer, show the bird "thinking" with idle animation.

### Typography

- Headings: Space Grotesk (500, 700)
- Body: Inter (400, 500, 600)
- System fallback: `system-ui`

---

## 9. HTMX + Tailwind Code Skeleton

A starter skeleton is included from the Grok session. Key patterns:

```html
<!-- Chirp Banner — HTMX-powered -->
<div hx-get="/api/chirp/42" hx-trigger="load"
     class="bg-[#161B22] border border-[#21262D] rounded-3xl p-5 flex gap-4 items-center cursor-pointer"
     onclick="launchWizard(4)">
  <!-- icon + text + arrow -->
</div>

<!-- Wizard — full-screen overlay, HTMX step swap -->
<div id="wizard" class="hidden fixed inset-0 bg-[#0D1117] z-50 overflow-auto">
  <div id="wizard-step" class="space-y-8">
    <!-- HTMX will swap content here -->
  </div>
</div>
```

**Backend endpoints:** `/wizard/step/{process}/{step}` returns the next card HTML fragment. Estimated implementation: <2 hours per wizard.

---

## 10. The 8 Core Guided Processes (MVP Scope)

| # | Process | Trigger | Wizard Steps | CRDM Tables |
|---|---------|---------|-------------|-------------|
| 1 | Open the Store | Time of day (AM) | 4 | cash_drawer_shifts |
| 2 | Count the Drawer | Shift end or Chirp | 5 | cash_drawer_shifts, cash_drawer_events |
| 3 | Resolve Refund Alert | Chirp: HIGH_REFUND_FREQUENCY | 5 | transactions, refunds |
| 4 | Resolve Cash Shortage | Chirp: CASH_VARIANCE_THRESHOLD | 6 | cash_drawer_shifts, employee_timecards |
| 5 | Review Void/Post-Void | Chirp: POST_VOID_ALERT | 4 | transactions (type=VOID/POST_VOID) |
| 6 | Check Inventory Shrink | Chirp: SHRINKAGE_SPIKE | 5 | inventory_adjustments, transaction_line_items |
| 7 | Weekly Scorecard | Friday PM auto-prompt | 3 | Aggregated metrics across all tables |
| 8 | LP Self-Risk Assessment | Monthly auto-prompt | 6 | All CRDM sources |

**MVP target:** Processes 1–4 for alpha. Processes 5–8 for beta.

---

## 11. Jim's "Virtual Gym" — Testing Agent Concept

Jeffe's directive: build an agent that captures Jim's QA/usability knowledge into an automated testing companion. Jim focuses on analytics and merchant experience; the agent handles regression, compliance, and Factory Process hook validation.

### Proposed Scope

1. **Usability scan** — automated walkthrough of every merchant-facing screen against Art's 90-second screen test
2. **Technical hook audit** — verify every Chirp rule has a corresponding wizard, every wizard has HTMX endpoints, every endpoint has a test
3. **Factory Process compliance** — verify PRD → AC → Test → Code traceability for every feature
4. **Coding standards enforcement** — brand palette compliance, accessibility (WCAG 2.1 AA), tap target sizes, loading time budgets

### Implementation Path

- Start as a Claude Code skill (`jim-virtual-gym` or `rooster-gym`)
- Uses Playwright for browser-based usability checks
- Uses pytest for technical hook validation
- Outputs a scorecard per scan with pass/fail/warning per Factory Process stage

---

## Traceability

| Reference | Location |
|-----------|----------|
| Grok session (source) | `Markdown/Sessions/Jeffe_Brainstorm_2026-02-22.md` |
| MVP Epics (E0-F6) | `Markdown/Strategy/Canary_MVP_Epics_v1.0.md` |
| Brand Guide v3 | `brand/BRAND_GUIDE_v3.html` |
| CRDM | `Markdown/Specs/CRDM_v1.0.md` |
| Factory Process | `Markdown/Strategy/Canary_Factory_Process_v1.0.md` |
| Art profile | `Team/Art.md` |
| Jim profile | `Team/Jim.md` |

---

*"This is the companion small merchants actually want to open 5× a day. Calm, fast, joyful, and 100% guided."*
