---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# ART — Today's View Wireframe v1.1 Revision Prompt
**Dispatched by:** ALX (Chief of Staff)
**Date:** February 24, 2026
**Priority:** 🔴 CRITICAL PATH — Jim + Jess still gated behind this
**Mode:** REVISION (Art owns design decisions)

---

## Context

Your v1.0 wireframe (`TodaysView_Wireframe_v1.0.html`) and self-critique (`TodaysView_SelfCritique_v1.0.md`) have been reviewed by Jeffe.

**Overall verdict: Approved.** The layout, information hierarchy, color system, Chirp integration, and accessibility foundations are all strong. The 8.8/10 self-critique score stands.

**One revision required before routing to Jim for QA scenario mapping.**

---

## Jeffe's Feedback — Icon Style Direction

> "I love our theme but the icons themselves — other than the original chirping canary, the inspiration for all of us — I don't love. Too Pixar. More South Park-ish. Simpler, linear, yet modern."

### What This Means for v1.1

**KEEP AS-IS:**
- The chirping canary SVG (top bar avatar + hero banner animated bird) — this is the original, it stays
- The entire layout, card structure, color system, spacing, typography
- The hero Chirp banner design and health-wave animation
- All accessibility work (touch targets, contrast ratios, ARIA labels)
- The annotation section

**CHANGE:**
Replace the emoji placeholders (🐦🦉🦊🐂🐓🪿) with custom inline SVG icons for all six animal modules. The new icons must follow this style direction:

| Attribute | NOT This (Pixar) | THIS (Target Style) |
|---|---|---|
| Line weight | Varied, organic strokes | Uniform stroke weight (2px) |
| Shapes | Rounded, blobby, soft | Geometric, angular, clean |
| Detail level | Eyes, feathers, texture | Minimal — silhouette-readable at 20px |
| Personality | Cute, expressive, animated | Deadpan, iconic, still |
| Construction | Organic curves | Built from circles, rectangles, triangles |
| Fill | Gradient, shaded | Flat fill OR stroke-only |
| Aesthetic | Pixar / Disney | South Park meets Figma — simple, linear, modern |

### The Six Icons Needed

1. **Canary** (🐦 → Home/Today tab) — Simple bird silhouette. NOT the chirping canary from the hero — this is the tab icon version. Minimal, one-color, recognizable as "bird" at 20px.
2. **Owl** (🦉 → Insights tab) — Geometric owl face. Two circles for eyes, triangle beak, maybe pointed ear tufts. That's it.
3. **Fox** (🦊 → Investigate tab) — Angular fox face. Pointed ears, sharp snout. Think geometric logo, not illustration.
4. **Bull** (🐂 → Inventory tab) — Bull head from front. Two curved horns, simple face shape. Minimal.
5. **Rooster** (🐓 → Daily Routines tab) — Rooster profile. Comb on top, simple beak, tail suggestion. Clean lines.
6. **Goose** (🪿 → Money tab) — Goose profile or head. Long neck, simple beak. Elegant, minimal.

### Technical Requirements for SVGs
- Inline SVG (no external files)
- ViewBox: `0 0 24 24` (standard icon grid)
- Stroke-based OR flat-fill — Art's call, but consistent across all six
- Single color: `currentColor` so they inherit the nav active/inactive states
- Must be legible at 20px (the nav icon size) AND at 24px (action card icon size)
- No gradients, no shadows, no animation on the icons themselves

### Action Card Icons
The three action cards also use emoji placeholders (Rooster for "Open the store," Bull for "Count the drawer," Fox for "Check yesterday's shrink"). Replace these with the same SVG icons from the nav set, rendered at the `action-icon` size.

---

## Self-Critique Improvement: Second Chirp Peek

Your self-critique identified the **Second Chirp peek indicator** as the #1 improvement. Jeffe agrees this is worth including in v1.1.

Add a 32px-tall element beneath the hero Chirp banner:
```
+1 more: [Second Chirp title snippet] → Chirps tab
```
- Left-aligned, muted text (`var(--text-muted)`)
- Right-arrow or chevron linking to Chirps tab
- Only renders when Chirp count > 1
- Does NOT break the max-3-cards rule (this is not a card)

---

## Deliverables

1. **`TodaysView_Wireframe_v1.1.html`** — Updated wireframe with custom SVG icons + second Chirp peek
2. **`TodaysView_SelfCritique_v1.1.md`** — Brief revision note appended to the v1.0 critique (no need to re-run all 7 questions — just note what changed and confirm scores hold)

---

## Routing

Same as v1.0:
1. **Jim** — QA scenario mapping against the finalized wireframe
2. **Jess** — Visual reference for Companion Guides
3. **Jeremy** — Production build (after Jim QA)

---

*Revision order issued by ALX · February 24, 2026*
*Factory Process Stage: Blueprint — Revision Pass*
