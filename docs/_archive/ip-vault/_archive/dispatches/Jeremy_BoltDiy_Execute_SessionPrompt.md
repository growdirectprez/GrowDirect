---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Jeremy — Bolt.diy Install & Blueprint Test (EXECUTE NOW)

**Dispatched by:** ALX via Jeffe
**Date:** February 25, 2026
**Priority:** 🔴 HIGH — Jeffe is waiting to see this
**Mode:** EXECUTE — not plan. The plan is written. Do the work.

---

## Context

You may have already produced an execution plan for Bolt.diy setup in a prior session. Good — now run it. ALX has confirmed:

- ❌ Bolt.diy is NOT yet cloned on this machine
- ❌ No `bolt.diy` directory exists under `/Users/geofflyle/GrowDirect/`
- ❌ No test results or screenshots exist yet
- ✅ The blueprint IS ready: `/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Triangulation/Canary_Generic_Frontend_Blueprint_v1.0.md`
- ✅ The existing Canary stack uses ports 5001/5432/6379 — Bolt.diy on 5173 has no conflicts

**Cross-reference your prior plan against the dispatch at:**
`/Users/geofflyle/GrowDirect/_ALX/WorkOrders/dispatches/Jeremy_BoltDiy_Install_SessionPrompt.md`

If your plan differs from ALX's dispatch, flag the differences but default to whichever gets Bolt.diy running fastest.

---

## What To Do (4 steps, ~20 minutes)

### Step 1: Clone & Configure

```bash
cd /Users/geofflyle/GrowDirect
git clone https://github.com/stackblitz-labs/bolt.diy.git
cd bolt.diy
cp .env.example .env.local
```

Edit `.env.local` — add an API key. Preference order:
1. Anthropic: `ANTHROPIC_API_KEY=sk-ant-xxxxx` (best for understanding the blueprint)
2. Ollama: `OLLAMA_API_BASE_URL=http://host.docker.internal:11434` (if running locally)
3. OpenAI: `OPENAI_API_KEY=sk-xxxxx`

Ask Jeffe for the key if you don't have one.

### Step 2: Run It

```bash
# Try Docker first (matches our infra pattern)
docker compose --profile development up -d

# Verify
open http://localhost:5173
```

If Docker fails, fall back:
```bash
pnpm install
pnpm run dev
```

**Gate:** Bolt.diy loads in browser at localhost:5173. If it doesn't load in 10 minutes, note the error and move on to fallback.

### Step 3: Feed the Blueprint

1. Open `http://localhost:5173`
2. Paste this lead-in prompt into Bolt.diy:

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

3. Then paste the FULL contents of:
   `/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Triangulation/Canary_Generic_Frontend_Blueprint_v1.0.md`

4. Let it generate. Don't interrupt.

**If context window is too small:** Paste only Sections 1–3 (App Overview + Design System + Today's View screen spec). That's the demo money shot.

### Step 4: Report

Create the results folder and document what happened:

```bash
mkdir -p /Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Triangulation/BoltDiy_Test_Results
```

Save to that folder:
- Screenshot(s) of the generated UI
- `RESULTS.md` — what worked, what didn't, which AI provider, any issues
- Note where Bolt.diy saved the generated code (if it did)

**Checklist for RESULTS.md:**
- [ ] Dark background (#0D1117) with card surfaces (#161B22)
- [ ] Top bar: "Good morning, Alex" + "2 Chirps need you"
- [ ] Hero Chirp banner: "Drawer short $18 at Offset Downtown"
- [ ] Chirp peek: "+1 more: Refund spike at Offset Downtown"
- [ ] 3 action cards
- [ ] 6 animal SVG icons in bottom nav
- [ ] Health bar (5 colored segments)
- [ ] Signal Yellow (#FBBF24) accent
- [ ] Mobile viewport (375px)

---

## Fallback If Bolt.diy Won't Run

Try pasting the blueprint into Claude.ai directly with:
```
Generate a single-file React app (index.html with inline JS/CSS) based on this blueprint. Start with Today's View only.
```

Save the output HTML to `BoltDiy_Test_Results/fallback_claude_prototype.html`.

---

## Constraints

- This does NOT replace your Sprint 5 Phase 3 work. Parallel track only.
- 30-minute timebox. If it's not working in 30 minutes, document why and get back to the deploy script.
- Do NOT optimize or refactor what Bolt.diy generates. This is a test of the tool + blueprint, not a code review.

---

*Jeffe wants to see what comes out. Make it happen.*
