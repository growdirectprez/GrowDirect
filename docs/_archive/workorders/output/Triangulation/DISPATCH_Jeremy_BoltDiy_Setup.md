---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Dispatch: Bolt.diy Prototype Test
**To:** Jeremy
**From:** ALX
**Date:** February 25, 2026
**Priority:** Ready when you are — target Friday Feb 28
**Estimated setup time:** 15–20 minutes

---

## What This Is

The Generic Frontend Blueprint is done. It's a single Markdown file that describes the entire Canary merchant-facing UI — Today's View, all 4 wizard flows, design system, seed data. The goal: feed it into Bolt.diy and see if it generates a recognizable React prototype of Today's View within 30 minutes.

**Blueprint location:**
```
_ALX/WorkOrders/output/Triangulation/Canary_Generic_Frontend_Blueprint_v1.0.md
```

---

## Step 1: Pull and Run Bolt.diy

```bash
# Clone the repo
git clone https://github.com/stackblitz-labs/bolt.diy.git
cd bolt.diy

# Copy the example env file
cp .env.example .env.local
```

Edit `.env.local` and add your API key. Bolt.diy supports multiple providers. Pick one:

```bash
# Option A: Anthropic (recommended — Claude will understand the blueprint best)
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Option B: OpenAI
OPENAI_API_KEY=sk-xxxxx

# Option C: Local via Ollama (if you have it running)
OLLAMA_API_BASE_URL=http://host.docker.internal:11434
```

Then run with Docker:

```bash
# Using Docker Compose (preferred)
docker compose --profile development up

# OR using npm directly if Docker gives trouble
pnpm install
pnpm run dev
```

The app should be running at `http://localhost:5173`.

---

## Step 2: Feed the Blueprint

1. Open Bolt.diy in your browser at `http://localhost:5173`
2. In the prompt input, paste the following lead-in, then paste the FULL contents of the blueprint Markdown file after it:

```
Build a React Progressive Web App based on the following blueprint.
Start with the Today's View (home screen) only.
Use the exact design tokens, SVG icons, and layout specifications described.
Include the seed data hardcoded so every screen looks populated.
Make it mobile-first (375px primary viewport) with the dark theme.

--- BLUEPRINT STARTS BELOW ---

[paste entire contents of Canary_Generic_Frontend_Blueprint_v1.0.md here]
```

3. Let it generate. It should produce a React app with components for the Today's View.

---

## Step 3: What to Check

**30-minute success test — does the prototype show:**

- [ ] Dark background (#0D1117) with card surfaces (#161B22)
- [ ] Top bar with greeting "Good morning, Alex" and "2 Chirps need you"
- [ ] Hero Chirp banner with "Drawer short $18 at Offset Downtown"
- [ ] Chirp peek "+1 more: Refund spike at Offset Downtown"
- [ ] 3 action cards (Open the store / Count the drawer / Check yesterday's shrink)
- [ ] 6 animal SVG icons in bottom navigation
- [ ] Health bar (5 colored segments) above bottom nav
- [ ] Signal Yellow (#FBBF24) as the primary accent color
- [ ] Mobile viewport (375px) layout

**Bonus (if it gets further):**

- [ ] Tapping hero banner opens a wizard overlay
- [ ] Wizard shows step progress (1/6)
- [ ] Role toggle (owner/manager) changes bottom nav visibility
- [ ] At least one wizard flow completes with confetti

---

## Step 4: Report Back

Send a screenshot (or screen recording) to ALX showing:
1. The Today's View on a phone-sized viewport
2. Any wizard screen it generated
3. List of what worked and what didn't

If it fails to generate anything usable, note:
- What error or result you got
- Which AI provider you used
- Whether the blueprint was too long for the context window (if so, try feeding just Sections 1–3 first)

---

## Fallback: If Bolt.diy Doesn't Work

Try Dyad instead:

```bash
# Dyad is fully local, no API key needed
git clone https://github.com/dyad-sh/dyad.git
cd dyad
# Follow their setup instructions
```

Or try pasting the blueprint into Claude.ai directly with the prompt:
```
Generate a single-file React app (index.html with inline JS/CSS)
based on this blueprint. Start with Today's View only.
```

---

*This is a parallel track. It does NOT block or replace your Sprint 5 work. Treat it as a 30-minute experiment when you have a gap.*
