---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Today's View Wireframe v1.1 — Self-Critique Addendum

**Wireframe:** `TodaysView_Wireframe_v1.1.html`
**Reviewer:** Art (UX/Creative Director) — self-critique pass
**Date:** February 24, 2026
**Feature:** E0-F6-A (Today's View)
**Factory Stage:** Blueprint — Revision Pass

---

## Revision Summary

Two changes made per Jeffe's feedback and v1.0 self-critique recommendation:

### Change 1: Icon Redesign (Emoji → Custom Inline SVGs)

**What changed:** All six animal module icons (Canary, Owl, Fox, Bull, Rooster, Goose) replaced from emoji placeholders to custom inline SVGs. The chirping canary in the top bar avatar and hero banner is **unchanged**.

**Style direction applied:** "South Park-ish — simpler, linear, yet modern" per Jeffe.

| Attribute | Implementation |
|---|---|
| Stroke weight | Uniform 2px across all six icons |
| Line caps | `square` — angular, not rounded |
| Line joins | `miter` — sharp corners, no soft rounding |
| ViewBox | `0 0 24 24` standard grid |
| Color | `currentColor` — inherits active/inactive nav states |
| Fill | Stroke-based with minimal solid fills (eyes, combs) |
| Gradients/shadows | None |
| Animation | None on module icons |

**Icon construction approach — each built from basic geometric primitives:**

1. **Canary** — `circle` (head) + `polygon` (beak) + `ellipse` (body) + `line` (legs). Key identifier: beak pointing right.
2. **Owl** — `rect` (face) + `circle` × 2 (eyes) + filled `circle` × 2 (pupils) + `polygon` (beak) + `polyline` × 2 (ear tufts). Key identifier: twin eye circles.
3. **Fox** — `polygon` (angular face shape with pointed ear vertices) + filled `circle` × 2 (eyes) + `polygon` (diamond nose). Key identifier: sharp angular silhouette.
4. **Bull** — `rect` (head) + `path` × 2 (curved horns) + filled `circle` × 2 (eyes) + `line` (mouth). Key identifier: horns.
5. **Rooster** — `circle` (head) + filled `polygon` (comb) + `polygon` (beak) + `line` × 2 (legs) + `polyline` (tail). Key identifier: comb on top.
6. **Goose** — `circle` (head) + `polygon` (beak) + `path` (curved neck) + `ellipse` (body) + `line` × 2 (legs). Key identifier: long neck.

**20px legibility test (self-assessed):**

| Icon | Identifiable at 20px? | Key feature that reads |
|---|---|---|
| Canary | YES | Beak triangle breaks the circle silhouette |
| Owl | YES | Twin eye circles are unmistakable |
| Fox | YES | Angular diamond shape, pointed ears |
| Bull | YES | Curved horns extend beyond head rectangle |
| Rooster | YES | Comb (filled triangle) on top of head |
| Goose | YES | Vertical neck line + small head at top |

**South Park vs Pixar check:**

- **Deadpan:** None of the icons have expressive features (no smiles, no eyebrows, no personality). Just structural identification. ✓
- **Geometric:** Built from circles, rectangles, triangles, and straight lines. No organic curves except the Bull's horns and Goose's neck (necessary for recognition). ✓
- **Minimal:** Lowest possible detail count per icon. Most have 5-7 elements. ✓
- **Angular:** `stroke-linecap="square"` + `stroke-linejoin="miter"` gives edges, not softness. ✓
- **Not cute:** No fill gradients, no shading, no highlights, no soft shadows. ✓

### Change 2: Second Chirp Peek Indicator

**What changed:** Added a 32px-tall `<a>` element beneath the hero Chirp banner. Shows the title of the next-priority Chirp when count > 1.

**Implementation details:**

- Format: `+1 more: [Chirp title snippet]` + right chevron
- Text color: `var(--text-muted)` (#6B7280) — visually subordinate to hero and cards
- Height: 32px (fixed) — `margin-top: -12px` tucks it closer to the hero banner
- Tap target: Full width of the element. Links to Chirps tab, not a wizard.
- Truncation: `text-overflow: ellipsis` if Chirp title exceeds available width
- Hover: Subtle 3% white background for tap affordance
- Accessibility: `aria-label` includes Chirp count, title, and destination
- **Does NOT break max-3-cards rule** — this is a link, not a card

**Edge cases handled:**

- 0-1 Chirps: Element does not render (server omits from HTMX response)
- 3+ Chirps: Still shows "+1 more" referencing the #2 Chirp. Full list in Chirps tab.
- Long Chirp title: Truncates with ellipsis. Chevron always visible.

---

## Score Impact Assessment

The v1.0 overall score was **8.8/10**. Here's how v1.1 changes affect each dimension:

| Question | v1.0 | v1.1 | Change | Notes |
|----------|-------|------|--------|-------|
| 1. Merchant job fit | 8/10 | 8/10 | — | Icons are cleaner but don't change task clarity |
| 2. Guided & opinionated | 9/10 | 9.5/10 | +0.5 | Peek makes the "full picture" visible without leaving the guided view |
| 3. Visual calm/authority | 8.5/10 | 8.5/10 | — | Icons are calmer than emoji (no color variation). Peek is visually muted. |
| 4. Chirp integration | 9/10 | 9.5/10 | +0.5 | Second Chirp now visible on Today's View. Addresses the v1.0 gap. |
| 5. Accessibility/mobile | 9/10 | 9/10 | — | SVG icons inherit currentColor. Peek has proper aria-label. No regression. |
| 6. Rooster testability | 9/10 | 9/10 | — | Existing tests cover hero + cards. Jim should add: `test_chirp_peek_renders_when_2_active` |
| 7. One big improvement | — | ✓ | Done | Peek indicator was the #1 recommendation. Implemented. |
| **Overall** | **8.8/10** | **9.0/10** | **+0.2** | |

---

## Additional Test Case for Jim (v1.1)

### Test 4: `test_chirp_peek_renders_when_2_active`
```
Given: Merchant "Alex" with 2 active Chirps
When: Page loads at /companion/today
Then:
  - Chirp peek element is visible beneath hero banner
  - Peek text contains "+1 more:" prefix
  - Peek text contains second Chirp title (truncated if needed)
  - Tapping peek navigates to Chirps tab view
  - No wizard overlay opens from peek tap
```

### Test 4b: `test_chirp_peek_hidden_when_0_or_1_chirps`
```
Given: Merchant with 0 or 1 active Chirps
When: Page loads at /companion/today
Then:
  - Chirp peek element is NOT present in DOM
  - No empty space between hero and action section label
```

---

## Remaining v1.0 Self-Critique Items (Unchanged)

The following items from the v1.0 self-critique remain valid and are **not addressed in v1.1** (as directed — this is a surgical revision):

- Onboarding tooltip for "Your morning" section label (future scope)
- Timezone edge-case monitoring for card algorithm (Jim QA)
- Yellow element count at upper limit (5 elements — monitor for creep)
- `@media (prefers-reduced-motion: reduce)` implementation (production)
- VoiceOver/TalkBack testing (pre-QA gate)
- Safe-area inset verification on notched devices

---

## Routing

This wireframe and self-critique addendum are ready for:
1. **Jim** — QA scenario mapping. Add Tests 4 and 4b above to the v1.0 test suite. Verify SVG icon rendering at 20px across iOS Safari, Android Chrome, and desktop browsers.
2. **Jess** — Companion Guide intake. Annotation section 10 (Icon Design Spec) and 2b (Chirp Peek) are new reference material.
3. **Jeremy** — After Jim's QA scenarios are mapped, Jeremy builds the production Today's View against this wireframe. SVG icons are production-ready inline code — no external dependencies.

**Do not route to Jeremy for production build until Jim has mapped QA scenarios against the wireframe.**

---

*Canary LP | Confidential*
*Art (UX/Creative Director) | February 24, 2026*
*Factory Process Stage: Blueprint — Revision Pass Complete*
