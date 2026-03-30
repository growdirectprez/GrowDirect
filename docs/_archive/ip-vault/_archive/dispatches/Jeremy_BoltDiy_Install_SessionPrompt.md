---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Session Prompt: Jeremy — Bolt.diy Install + Blueprint Test

**Dispatched by:** ALX
**Date:** February 25, 2026
**Priority:** 🔴 HIGH — Jeffe wants to see this today
**Estimated time:** 20–30 minutes
**Mode:** DISPATCH (ALX owns outcome, Jeremy executes)

---

## Context

The Triangulation work order produced a Generic Frontend Blueprint — a single sanitized Markdown spec that describes the entire Canary merchant-facing UI (Today's View, 4 wizard flows, design system, seed data). Condor wrote it. It's clean and ready. Jeffe wants to see what happens when we feed it to Bolt.diy.

**This runs alongside our existing Docker stack. No conflicts — Bolt.diy uses port 5173, our localhost stack is on 5001/5432/6379.**

---

## Task 1: Install and Run Bolt.diy via Docker

```bash
# From the GrowDirect root
cd /Users/geofflyle/GrowDirect

# Clone Bolt.diy into its own directory (parallel to Canary, not inside it)
git clone https://github.com/stackblitz-labs/bolt.diy.git
cd bolt.diy

# Copy env template
cp .env.example .env.local
```

Edit `.env.local` — add ONE provider key. Recommended order of preference:

```bash
# Option A: Anthropic (best results — Claude understands the blueprint natively)
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Option B: If Ollama is running locally
OLLAMA_API_BASE_URL=http://host.docker.internal:11434

# Option C: OpenAI
OPENAI_API_KEY=sk-xxxxx
```

Then start it:

```bash
# Docker Compose (preferred — matches our infra pattern)
docker compose --profile development up -d

# Verify it's running
open http://localhost:5173
```

If Docker Compose fails (Bolt.diy's Docker setup can be finicky), fall back to npm:

```bash
pnpm install
pnpm run dev
```

**Gate:** Bolt.diy loads in the browser at `localhost:5173`. Move to Task 2.

---

## Task 2: Feed the Blueprint

The blueprint is at:
```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Triangulation/Canary_Generic_Frontend_Blueprint_v1.0.md
```

1. Open Bolt.diy at `http://localhost:5173`
2. In the prompt input, paste this lead-in FIRST:

```
Build a React Progressive Web App based on the following blueprint.
Start with the Today's View (home screen) only.
Use the exact design tokens, SVG icons, and layout specifications described.
Include the seed data hardcoded so every screen looks populated.
Make it mobile-first (375px primary viewport) with the dark theme.
Include the animated mascot bird SVG with the idle green pulse state.
Include all 6 bottom navigation icons exactly as specified in the SVG code.

--- BLUEPRINT STARTS BELOW ---
```

3. Then paste the FULL contents of the blueprint Markdown file after the lead-in.
4. Let Bolt.diy generate. Don't interrupt it.

**If the blueprint is too long for the context window:** Feed just Sections 1–3 (Application Overview + Design System + Screen 3.1 Today's View) first. That's the money shot for the demo.

---

## Task 3: 30-Minute Eyeball Test

Does the generated prototype show:

- [ ] Dark background (`#0D1117`) with card surfaces (`#161B22`)
- [ ] Top bar with greeting "Good morning, Alex" and "2 Chirps need you"
- [ ] Hero Chirp banner with "Drawer short $18 at Offset Downtown"
- [ ] Chirp peek "+1 more: Refund spike at Offset Downtown"
- [ ] 3 action cards (Open the store / Count the drawer / Check yesterday's shrink)
- [ ] 6 animal SVG icons in bottom navigation
- [ ] Health bar (5 colored segments) above the CANARY wordmark
- [ ] Signal Yellow (`#FBBF24`) as the primary accent color
- [ ] Looks right at 375px mobile viewport

**Bonus (if it gets further):**
- [ ] Tapping hero banner opens a wizard overlay
- [ ] Wizard shows step progress (Step 1 of 6)
- [ ] Mascot bird animates (gentle bob + green pulse)
- [ ] Role toggle changes bottom nav visibility

---

## Task 4: Report Back

Take a screenshot or screen recording and save to:
```
_ALX/WorkOrders/output/Triangulation/BoltDiy_Test_Results/
```

Create that folder. Drop in:
- Screenshot(s) of what Bolt.diy generated
- A quick `RESULTS.md` with: what worked, what didn't, which AI provider you used, any context window issues
- If it generated usable code, note where Bolt.diy saved it

---

## What This Is NOT

- This does NOT replace your Sprint 5 Phase 3 work. Your priority is still: deploy script → Today's View → Process 4 wizard → seed data → phone access.
- This is a 20–30 minute parallel experiment. If Bolt.diy install takes more than 15 minutes, stop, note the issue, and go back to Sprint 5 work.
- If it works well, this becomes a powerful demo tool for Monday. If it doesn't, no harm — Jeremy's real build is the primary path.

---

## Port Map (no conflicts)

| Service | Port | Stack |
|---|---|---|
| Canary Flask | 5001 | Existing localhost stack |
| PostgreSQL 17 | 5432 | Existing localhost stack |
| Valkey 8 | 6379 | Existing localhost stack |
| **Bolt.diy** | **5173** | **NEW — this task** |

---

## Files to Read

| What | Path |
|---|---|
| Blueprint (THE INPUT) | `_ALX/WorkOrders/output/Triangulation/Canary_Generic_Frontend_Blueprint_v1.0.md` |
| Bolt.diy setup reference | `_ALX/WorkOrders/output/Triangulation/DISPATCH_Jeremy_BoltDiy_Setup.md` |
| Art's wireframe (visual truth) | `_ALX/WorkOrders/output/Art/TodaysView_Wireframe_v1.1.html` |

---

*Jeffe is watching this one. He wants to see what vibe coding can do with our blueprint. Make it sing.*
