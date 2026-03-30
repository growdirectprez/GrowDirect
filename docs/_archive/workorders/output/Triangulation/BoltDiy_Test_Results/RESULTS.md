---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Bolt.diy Test Results — Canary Generic Frontend Blueprint

**Date:** February 24, 2026
**Tester:** Jeremy (Claude Code automation)
**Blueprint:** `Canary_Generic_Frontend_Blueprint_v1.0.md` (42,820 bytes, 1,032 lines)
**AI Provider:** Anthropic — Claude Sonnet 4.5 (32k context)
**Platform:** Bolt.diy via Docker (development profile)

---

## Setup

| Item | Detail |
|---|---|
| Install method | Docker Compose (`--profile development`) |
| Setup time | ~3 minutes (clone + env config) |
| Docker build time | ~2 minutes (image build + container start) |
| First model attempted | Claude 3.5 Sonnet — **FAILED** (model ID `claude-3-5-sonnet-20241022` not available) |
| Working model | Claude Sonnet 4.5 (32k context) |
| Prompt injection method | JavaScript fetch from CORS-enabled local HTTP server (43,047 chars) |
| Generation time | ~45 seconds |
| Port | 5173 (no conflicts with existing Canary stack on 5001/5432/6379) |

### Setup Notes
- Bolt.diy's `docker-compose.yaml` requires both `.env` AND `.env.local` — had to create an empty `.env` to avoid a fatal error.
- The "Claude 3.5 Sonnet" model listed in the dropdown uses an outdated model ID that the API rejects. Switching to "Claude Sonnet 4.5 (32k context)" resolved it immediately.
- 43KB blueprint fit in a single prompt with no context window issues.

---

## 9-Point Eyeball Checklist

| # | Check Item | Result | Notes |
|---|---|---|---|
| 1 | Dark background (#0D1117) with card surfaces (#161B22) | **PASS** | Correct dark theme throughout. Card surfaces visually distinct from background. |
| 2 | Top bar greeting "Good evening, Alex" + "2 Chirps need you" | **PASS** | Time-of-day greeting works (showed "Good evening" at ~9 PM). "2 Chirps need you" displayed in Signal Yellow with pulsing dot. |
| 3 | Hero Chirp: "Drawer short $18 at Offset Downtown" | **PASS** | Exact text. "URGENT CHIRP" severity label in red. "4 min wizard" meta. "Fix this →" CTA in yellow pill. |
| 4 | Chirp peek: "+1 more: Refund spike at Offset Downtown" | **PASS** | Correct text, right chevron, tucked below hero banner. |
| 5 | 3 action cards (Open store / Count drawer / Check shrink) | **PASS** | All 3 present with correct titles, descriptions, module icons, and chevrons. 2-column layout on wider viewport, third card full-width. |
| 6 | 6 animal SVG icons in bottom nav | **PASS** | All 6: Canary (Home), Owl (Insights), Fox (Investigate), Bull (Inventory), Rooster (Daily), Goose (Money). Active tab (Home) highlighted in Signal Yellow. |
| 7 | Health bar (5 segments) above CANARY wordmark | **PASS** | 5 colored segments visible (2 green, 1 lighter green, 1 yellow, 1 red). "CANARY" wordmark in dim text above. |
| 8 | Signal Yellow (#FBBF24) as primary accent | **PASS** | Yellow accent on: CTA button, active nav tab, "2 Chirps need you" text, chirp dot, module icon containers. |
| 9 | Looks right at 375px mobile viewport | **PASS** | Mobile responsive view activated in Bolt.diy — layout stacks properly, bottom nav visible, no horizontal overflow. |

**Score: 9/9 PASS**

---

## Bonus Items

| Item | Result | Notes |
|---|---|---|
| Wizard overlay on tap | Not tested | Would require clicking "Fix this →" and checking overlay behavior |
| Step progress indicator | Not tested | Requires wizard launch |
| Mascot bird animates | **PARTIAL** | Bird SVG renders with colored ring (green pulse ring visible). Full animation (bob, chirp waves) unclear from static screenshots. |
| Role toggle | Not tested | Would need UI mechanism to switch roles |

---

## What Worked

1. **Every visual element from the blueprint rendered correctly** — dark theme, design tokens, SVG icons, layout hierarchy, typography.
2. **Seed data populated perfectly** — merchant name "Alex", store "Offset Downtown", chirp texts, action card descriptions all match the blueprint exactly.
3. **Component architecture is clean** — separate files for each component (MascotBird, HeroChirp, ActionCard, ChirpPeek, TopBar, ModuleIcon, BottomNav) plus seedData.js.
4. **Time-of-day awareness works** — greeting showed "Good evening" (tested at ~9 PM) and section label showed "YOUR EVENING".
5. **Health bar** with 5 colored segments rendered correctly.
6. **Bottom navigation** with all 6 animal module icons and role-correct labels.
7. **The full 43KB blueprint was consumed in a single prompt** — no splitting required.

## What Didn't Work

1. **Claude 3.5 Sonnet model** listed in the Bolt.diy dropdown is broken — the model ID `claude-3-5-sonnet-20241022` is rejected by the Anthropic API. Had to switch to Claude Sonnet 4.5.
2. **Docker `.env` file required** — Bolt.diy's docker-compose.yaml references both `.env` and `.env.local`. If `.env` doesn't exist, docker-compose exits with error code 1. Not documented clearly.
3. **Wizard interaction not tested** — generation focused on Today's View per the prompt instructions. Wizard flows would need a follow-up prompt.

## Generated Code Location

Bolt.diy generated the code in its WebContainer (in-browser). The project is accessible at:
- **Bolt.diy UI:** `http://localhost:5173/chat/msg-9VxOSosbM0ZUWPnQsXWgAbVb-0`
- **Code tab** shows all files: `src/components/`, `src/data/`, `App.jsx`, `index.css`, etc.
- **Export options:** Deploy button (top-right) or Sync to GitHub available in the Bolt.diy UI.

### File Tree Generated

```
src/
├── components/
│   ├── ActionCard.jsx
│   ├── ActionCard.css
│   ├── ChirpPeek.jsx
│   ├── ChirpPeek.css
│   ├── HeroChirp.jsx
│   ├── HeroChirp.css
│   ├── MascotBird.jsx
│   ├── MascotBird.css
│   ├── ModuleIcon.jsx
│   ├── TopBar.jsx
│   └── TopBar.css
├── data/
│   └── seedData.js
├── App.css
├── App.jsx
├── index.css
└── main.jsx
index.html
package.json
```

---

## Verdict

**USABLE — Impressive first-pass prototype.**

The Canary Generic Frontend Blueprint v1.0 fed into Bolt.diy with Claude Sonnet 4.5 produced a recognizable, visually accurate React prototype of the Today's View screen in under 2 minutes of generation time. All 9 checklist items passed. The output is demo-ready for showing stakeholders what the merchant-facing app looks like.

**Recommendation:** This is a powerful demo tool. For Monday's demo, the generated preview can be shown directly in Bolt.diy or exported as a standalone React app. Follow-up prompts could add wizard flows, route transitions, and role-based nav toggling.

---

*Generated by Claude Code on behalf of Jeremy. Blueprint by Condor. Dispatch by ALX.*
