---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# 2A — Today's View Day-in-the-Life Test Scripts
**Date:** February 24, 2026
**Author:** Jim (QA Manager)
**Wireframe Reference:** Art v1.1 — `_ALX/WorkOrders/output/Art/TodaysView_Wireframe_v1.1.html`
**Canonical Terminology:** PhD Alignment Brief Section 6
**Feature:** E0-F6-A (Today's View)

---

## Scenario Set 1: Morning Open (Store Manager)

### TV-S1-001: Manager Opens Today's View at 7:00 AM

```
SCENARIO: Store Manager morning login — Today's View first impression
MODULE: Canary (Home / Today's View)
ROLE: Store Manager (part-timer supervisor — restricted permissions)
STORY: As a Store Manager opening the app at the start of my shift, I want to
       see exactly what needs my attention this morning so I can prioritize my
       first 30 minutes without guessing.

PRECONDITIONS:
  - Manager "Maria" is logged in with Store Manager role
  - Current time: 7:00 AM (or time-of-day set to AM for testing)
  - Store has 2 active Chirps:
    (1) CASH_VARIANCE_THRESHOLD — drawer short $18 at Store #1
    (2) HIGH_NO_SALE_FREQUENCY — 7 no-sale opens yesterday at Store #1
  - Cash drawer shift from last night is CLOSED with variance

STEPS:
  1. Maria opens the app on her iPhone (iOS Safari)
  2. Today's View loads
  3. VERIFY: Top bar shows "Good morning, Maria — 2 Chirps need you"
  4. VERIFY: Canary avatar (top-left) shows idle green pulse animation
  5. VERIFY: Hero Chirp banner shows highest-priority Chirp:
     "Drawer short $18 at Store #1 — 4 min wizard"
     Banner uses health-wave animation (yellow → tapping reveals red)
  6. VERIFY: Chirp peek indicator visible beneath hero:
     "+1 more: High no-sale frequency at Store #1" + right chevron
  7. VERIFY: Section label reads "Your morning" (AM time-of-day)
  8. VERIFY: Max 3 action cards visible:
     - "Open the Store" (Rooster icon)
     - "Count the Drawer" (Bull icon)
     - "Check Yesterday's Shrink" (Canary icon)
  9. VERIFY: Health bar visible beneath CANARY lockup
  10. Maria taps "Open the Store" card
  11. VERIFY: Wizard launches (full-screen overlay, Process 1)
  12. Maria completes 4-step wizard in <5 minutes
  13. VERIFY: Completion screen shows confetti + chirp sound + "Store open!"
  14. VERIFY: Returns to Today's View with "Open the Store" card removed or grayed
  15. VERIFY: Time from app open to first action identified: <90 seconds

EXPECTED RESULT: Maria knows her #1 task within 90 seconds. Wizard completes
in <5 minutes. Today's View updates to reflect completed task.

EDGE CASES:
  - What if Maria's device has slow network? (<400ms load target per AC-A7)
  - What if the greeting says "Good afternoon" at 7 AM? (timezone bug)
  - What if Maria taps the hero banner instead of an action card?
    → Should launch Process 4 wizard (cash shortage resolution)
  - What if Maria is assigned to multiple locations?
    → Today's View should show her primary location's Chirps

SEVERITY: Critical
LINKED STORY: AC-A1 (greeting + count), AC-A2 (hero banner), AC-A3 (time awareness),
              AC-A4 (max 3 cards), AC-A7 (<400ms)
```

### TV-S1-002: Manager Taps Hero Chirp Banner

```
SCENARIO: Manager taps the hero Chirp banner to resolve the cash shortage
MODULE: Canary (Today's View → Wizard)
ROLE: Store Manager
STORY: As a Store Manager, when I tap the hero Chirp banner, the appropriate
       wizard launches so I can resolve the alert immediately.

PRECONDITIONS:
  - Same state as TV-S1-001 (hero shows CASH_VARIANCE_THRESHOLD)

STEPS:
  1. Maria taps the hero Chirp banner
  2. VERIFY: Wizard Process 4 launches (full-screen overlay)
  3. VERIFY: Wizard title references the specific Chirp (drawer short $18)
  4. VERIFY: No page reload — HTMX swaps content
  5. Maria can navigate through wizard steps
  6. VERIFY: Manager does NOT see "Flag for Fox investigation" button at step 3
     (progressive disclosure — Fox escalation is Owner-only)

EXPECTED RESULT: Wizard launches from hero tap. Manager sees restricted view.

EDGE CASES:
  - What if the Chirp was resolved by another user while Maria was viewing?
  - What if the wizard endpoint returns 500?
    → Graceful error state, Canary "thinking" animation, not a white screen

SEVERITY: Critical
LINKED STORY: AC-A2, AC-B4 (progressive disclosure)
```

---

## Scenario Set 2: Mid-Shift Alert (Shift Supervisor)

### TV-S2-001: Supervisor Receives CASH_VARIANCE_THRESHOLD Chirp

```
SCENARIO: Shift Supervisor receives real-time Chirp during mid-shift
MODULE: Canary (Chirps → Wizard Process 4)
ROLE: Shift Supervisor (restricted — similar to Store Manager)
STORY: As a Shift Supervisor, when a cash variance Chirp fires during my shift,
       I need to resolve it through the guided wizard before the owner sees it
       on their end-of-day review.

PRECONDITIONS:
  - Supervisor "Sam" is logged in, mid-shift (2:00 PM)
  - Cash drawer shift closes with $18 variance (triggers C-102)
  - Chirp engine fires CASH_VARIANCE_THRESHOLD alert
  - Sam has Today's View open

STEPS:
  1. VERIFY: Today's View updates to show new Chirp in hero banner
     (if Sam is on Today's View, HTMX should refresh the hero)
  2. Hero banner now reads: "Drawer short $18 at Store #1 — 4 min wizard"
  3. Sam taps the hero banner
  4. VERIFY: Process 4 wizard launches — "Resolve Cash Drawer Shortage"

  WIZARD STEP 1 — Confirm the fact (1 tap):
  5. Screen shows: "Was the drawer actually short $18?"
  6. Sam taps "Yes"
  7. VERIFY: Photo upload option available (camera + gallery)
  8. Sam takes a photo of the cash count sheet
  9. VERIFY: Photo uploads successfully, thumbnail appears

  WIZARD STEP 2 — Who touched it last?
  10. Screen shows pre-filled list of today's closers
  11. VERIFY: Most likely employee is listed first (opinionated sorting)
  12. Sam selects the employee

  WIZARD STEP 3 — Common causes:
  13. Screen shows 4 illustrated cards (brand yellow borders):
      - "Forgot to record a refund"
      - "Math error at close"
      - "Theft (I suspect…)"
      - "None of these — something else"
  14. VERIFY: Sam does NOT see "Flag for Fox investigation" button
     (Supervisor role — Fox escalation is Owner-only)
  15. Sam taps "Math error at close"

  WIZARD STEP 4 — Fix it now:
  16. Screen shows step-by-step checklist with check-off animation
  17. Sam checks each item (progress bar uses health-wave colors)
  18. VERIFY: Progress bar fills as items complete

  WIZARD STEP 5 — Learn & prevent:
  19. Screen shows one-sentence tip + "Add to team playbook" toggle
  20. Sam toggles "Add to team playbook" ON
  21. Sam taps Next

  WIZARD STEP 6 — Done:
  22. VERIFY: Confetti animation + chirp sound
  23. VERIFY: Screen shows "Great job — shrink prevented"
  24. VERIFY: Chirp is now marked as RESOLVED
  25. VERIFY: Today's View no longer shows this Chirp in hero

  Evidence Chain Verification:
  26. VERIFY: Photo from step 1 is stored in Fox evidence tables (INSERT-only)
  27. VERIFY: Evidence record has SHA-256 file_hash
  28. VERIFY: case_timeline has an entry for this wizard completion

EXPECTED RESULT: Full 6-step wizard completed in <8 minutes. Evidence captured.
Chirp resolved. Today's View updated.

EDGE CASES:
  - Photo upload fails (network timeout) — what does the wizard show?
  - Sam taps "Back" at step 4 — can they go back without losing progress?
  - Sam force-closes the app at step 3 — is progress saved? Can they resume?
  - Two supervisors try to resolve the same Chirp simultaneously
  - Drawer variance is exactly $0.00 (false alarm) — Sam taps "No" at step 1

SEVERITY: Critical
LINKED STORY: AC-B1 (HTMX swaps), AC-B2 (6 screens max), AC-B3 (evidence capture),
              AC-B4 (progressive disclosure), AC-B5 (completion UX)
```

---

## Scenario Set 3: End-of-Day Review (Owner)

### TV-S3-001: Owner Reviews the Day at 9 PM

```
SCENARIO: Owner opens Today's View at end of day to review what happened
MODULE: Canary (Today's View — Owner perspective)
ROLE: Owner (full permissions)
STORY: As the store Owner, at the end of the day I want to see a summary of
       what happened, what was resolved, and what still needs my attention
       so I can sleep knowing the store is secure.

PRECONDITIONS:
  - Owner "Oscar" is logged in at 9:00 PM
  - Day's activity: 2 Chirps resolved (by Sam), 1 Chirp still active
  - Today's View should reflect PM time-of-day awareness

STEPS:
  1. Oscar opens app on his laptop (Chrome desktop)
  2. VERIFY: Greeting reads "Good evening, Oscar — 1 Chirp needs you"
  3. VERIFY: Hero banner shows the remaining active Chirp
  4. VERIFY: Chirp peek is NOT visible (only 1 active Chirp — threshold is 2+)
  5. VERIFY: Section label reads "Your evening" or equivalent PM label
  6. VERIFY: Action cards are PM-appropriate:
     - "Count the Drawer" (Bull icon)
     - "Check Today's Shrink" (Canary icon)
     (NOT "Open the Store" — it's 9 PM)
  7. Oscar taps "Check Today's Shrink"
  8. VERIFY: Wizard or scorecard launches showing daily shrink summary
  9. VERIFY: Oscar can see Daily Shrink Score scorecard
     (single calm card: one headline number, one trend arrow, one "Fix It" button)
  10. VERIFY: Oscar can see Team Performance scorecard (Owner-only)
  11. VERIFY: Oscar can navigate to Fox tab (Owner-only)
  12. VERIFY: Oscar can navigate to Goose tab (Owner-only — Treasury Snapshot)

  Role Gating Verification:
  13. Log out Oscar. Log in as Maria (Store Manager).
  14. VERIFY: Maria cannot see Team Performance scorecard
  15. VERIFY: Maria cannot see Fox workbench in navigation
  16. VERIFY: Maria cannot see Goose tab in navigation
  17. VERIFY: Maria's bottom nav shows only: Canary, Owl (if applicable), Bull, Rooster
     (NOT Fox, NOT Goose — per Design Spec Section 5)

EXPECTED RESULT: Owner sees full picture. Manager sees restricted view.
Role gating enforced at UI and route level.

EDGE CASES:
  - Owner checks at midnight — does greeting say "Good evening" or "Good morning"?
  - All Chirps resolved — zero active. Hero banner state?
  - Owner has 0 employees — "Who touched it last?" list is empty

SEVERITY: Critical
LINKED STORY: AC-A1, AC-A3, AC-D3 (Team Performance = Owner only),
              AC-D5 (Treasury = Owner + Manager)
```

---

## Scenario Set 4: Edge Cases & Failures

### TV-S4-001: Zero Active Chirps

```
SCENARIO: Today's View with no active Chirps
MODULE: Canary (Today's View — empty state)
ROLE: Any
STORY: As a merchant with no active alerts, Today's View should show a calm,
       encouraging state — not a broken or empty page.

PRECONDITIONS:
  - Merchant has 0 active Chirps
  - All previous Chirps resolved

STEPS:
  1. Load Today's View
  2. VERIFY: Greeting still shows personalized name
  3. VERIFY: Greeting reads "0 Chirps" or equivalent positive messaging
     (e.g., "All clear, Alex — no Chirps today" — NOT "0 Chirps need you")
  4. VERIFY: Hero Chirp banner is NOT displayed (no Chirp to show)
  5. VERIFY: Chirp peek is NOT displayed
  6. VERIFY: Action cards still show time-appropriate suggestions
     (even without Chirps, the merchant may want to "Open the Store" or "Count the Drawer")
  7. VERIFY: Health bar shows green state
  8. VERIFY: No empty white space where hero banner would be
  9. VERIFY: Page layout is visually balanced without the hero section

EXPECTED RESULT: Calm, complete-looking page. Merchant feels "everything is fine."

EDGE CASES:
  - Merchant has never had any Chirps (brand new account)
  - Merchant had Chirps earlier today but all resolved
SEVERITY: High
LINKED STORY: AC-A1, AC-A2
```

### TV-S4-002: 10+ Active Chirps — Max 3 Cards Rule

```
SCENARIO: Today's View with many active Chirps — card limit enforcement
MODULE: Canary (Today's View — overflow handling)
ROLE: Owner
STORY: As an Owner with many active alerts, Today's View must still show max 3
       action cards and not overwhelm me with information.

PRECONDITIONS:
  - Merchant has 10 active Chirps (various types)

STEPS:
  1. Load Today's View
  2. VERIFY: Greeting shows "10 Chirps need you"
  3. VERIFY: Hero banner shows highest-priority Chirp
  4. VERIFY: Chirp peek shows "+1 more: [second Chirp title]"
     (peek always shows #2 Chirp, regardless of total count)
  5. VERIFY: Exactly 3 action cards displayed (max 3 rule — AC-A4)
  6. VERIFY: Cards are the 3 most relevant actions, not just first 3 alphabetically
  7. VERIFY: No scrolling reveals additional cards beyond 3
  8. VERIFY: Navigating to Chirps tab shows all 10 (full list)
  9. VERIFY: Page does not feel cluttered or panic-inducing

EXPECTED RESULT: Max 3 cards. No overflow. Chirps tab has the full list.

EDGE CASES:
  - All 10 Chirps are the same type
  - Chirps span multiple locations
SEVERITY: High
LINKED STORY: AC-A4
```

### TV-S4-003: Network Offline — Graceful Degradation

```
SCENARIO: Today's View when device loses network connectivity
MODULE: Canary (Today's View — offline)
ROLE: Any
STORY: As a merchant in a store with spotty Wi-Fi, if my connection drops,
       the app should show me something useful, not a blank white screen.

PRECONDITIONS:
  - Today's View previously loaded with data
  - Device network is then disconnected

STEPS:
  1. Load Today's View normally (with network)
  2. Disconnect network (airplane mode or Wi-Fi off)
  3. Pull to refresh or navigate away and back
  4. VERIFY: App shows last-known state or clear offline message
  5. VERIFY: No white screen, no unhandled JavaScript errors
  6. VERIFY: Canary avatar shows a visual offline indicator
     (suggestion: bird "sleeping" or gray pulse instead of green)
  7. VERIFY: Tapping an action card shows "You're offline — try again when connected"
  8. Reconnect network
  9. VERIFY: Today's View refreshes to current state within a few seconds

EXPECTED RESULT: Graceful degradation. No crash. Clear messaging.

EDGE CASES:
  - Network drops mid-wizard (step 3 of 6) — is progress preserved?
  - Server is up but returns 500 errors — similar graceful handling expected
SEVERITY: High
LINKED STORY: Design Spec "No loading spinners longer than 400ms"
```

### TV-S4-004: Wrong Role Sees Wrong Data

```
SCENARIO: Verify role-gating prevents data leakage
MODULE: Canary (Today's View + Navigation — RBAC)
ROLE: Store Manager (attempting to access Owner content)
STORY: As the security system, a Store Manager must NEVER see Fox workbench,
       Goose treasury, Team Performance scorecard, or any Owner-only content.

PRECONDITIONS:
  - Two accounts: Owner "Oscar" and Manager "Maria" for same store

STEPS:
  1. Log in as Maria (Store Manager)
  2. VERIFY: Bottom nav does NOT include Fox icon
  3. VERIFY: Bottom nav does NOT include Goose icon
  4. Attempt to navigate directly to /fox/cases (type URL)
  5. VERIFY: Returns 403 Forbidden or redirects to Today's View
  6. Attempt to navigate to /goose/treasury
  7. VERIFY: Returns 403 or redirect
  8. Attempt to navigate to /scorecard/team-performance
  9. VERIFY: Returns 403 or redirect
  10. Log in as Oscar (Owner)
  11. VERIFY: All navigation items visible (Canary, Owl, Fox, Bull, Rooster, Goose)
  12. VERIFY: Oscar can access /fox/cases, /goose/treasury, Team Performance

EXPECTED RESULT: Role gating enforced at both UI (nav hidden) and route level (403).

EDGE CASES:
  - Manager with temporarily elevated permissions
  - API calls with Manager auth token to Owner-only endpoints
SEVERITY: Critical
LINKED STORY: Design Spec Section 5
```

---

## Scenario Set 5: v1.1-Specific Test Cases

### TV-S5-001: Chirp Peek Renders When 2+ Chirps Active

```
SCENARIO: test_chirp_peek_renders_when_2_active
MODULE: Canary (Today's View — Chirp Peek Indicator)
ROLE: Any
STORY: As a merchant with multiple active Chirps, I see a subtle indicator
       beneath the hero banner showing there's more to attend to, without
       breaking the max-3-cards rule.

PRECONDITIONS:
  - Merchant "Alex" with 2+ active Chirps
  - Art v1.1 wireframe implemented (peek element exists in markup)

STEPS:
  1. Load Today's View at /companion/today
  2. VERIFY: Chirp peek element is visible beneath hero banner
  3. VERIFY: Peek text contains "+1 more:" prefix
  4. VERIFY: Peek text contains second Chirp's title (truncated with ellipsis if needed)
  5. VERIFY: Right chevron (›) is always visible even with long Chirp title
  6. VERIFY: Peek element height is 32px
  7. VERIFY: Peek text color is var(--text-muted) (#6B7280) — visually subordinate
  8. Tap the peek element
  9. VERIFY: Navigates to Chirps tab (full Chirp list)
  10. VERIFY: Does NOT launch a wizard (peek links to Chirps tab, not a specific wizard)
  11. VERIFY: Peek element has proper aria-label including Chirp count and title

EXPECTED RESULT: Peek visible, correctly formatted, links to Chirps tab.

EDGE CASES:
  - 3+ Chirps — peek still shows "+1 more" referencing Chirp #2
  - Chirp title is very long (>50 characters) — truncation with ellipsis
  - Chirp title contains special characters or emoji
SEVERITY: High
LINKED STORY: Art v1.1 Self-Critique, Test 4
```

### TV-S5-002: Chirp Peek Hidden When 0 or 1 Chirps

```
SCENARIO: test_chirp_peek_hidden_when_0_or_1_chirps
MODULE: Canary (Today's View — Chirp Peek Indicator)
ROLE: Any
STORY: As a merchant with 0 or 1 Chirps, the peek indicator should not appear,
       and no empty space should exist between the hero and action section.

PRECONDITIONS:
  - Merchant with 0 active Chirps OR 1 active Chirp

STEPS:
  For 0 Chirps:
  1. Load Today's View
  2. VERIFY: Chirp peek element is NOT present in DOM
  3. VERIFY: No empty 32px gap between hero area and action section
  4. VERIFY: Layout is visually balanced

  For 1 Chirp:
  5. Load Today's View
  6. VERIFY: Hero banner shows the single Chirp
  7. VERIFY: Chirp peek element is NOT present in DOM
  8. VERIFY: No empty space — action cards begin directly below hero

EXPECTED RESULT: Peek element is server-side conditional. NOT hidden via CSS — not in DOM at all.

EDGE CASES:
  - Chirp count changes from 2 to 1 while on Today's View (HTMX update) — peek should disappear
  - Chirp count changes from 1 to 2 — peek should appear
SEVERITY: High
LINKED STORY: Art v1.1 Self-Critique, Test 4b
```

### TV-S5-003: SVG Icon Rendering Verification

```
SCENARIO: All 6 animal SVG icons identifiable at 20px across browsers
MODULE: Canary (Navigation — Bottom Nav)
ROLE: Any
STORY: As Art's design standard, the 6 custom SVG module icons must be
       visually identifiable at their rendered size (20px) across all
       target browsers.

PRECONDITIONS:
  - Art v1.1 wireframe implemented with custom inline SVGs
  - Test devices: iPhone (iOS Safari), Android (Chrome), Desktop (Chrome, Firefox, Safari)

STEPS:
  For each device/browser:
  1. Load Today's View
  2. Inspect bottom navigation bar
  3. VERIFY: 6 icons rendered (Canary, Owl, Fox, Bull, Rooster, Goose)
  4. VERIFY: Each icon is identifiable by its key feature at rendered size:
     - Canary: beak triangle breaks circle silhouette
     - Owl: twin eye circles unmistakable
     - Fox: angular diamond shape, pointed ears
     - Bull: curved horns extend beyond head rectangle
     - Rooster: filled comb triangle on top of head
     - Goose: vertical neck line + small head at top
  5. VERIFY: Icons use currentColor (inherit active/inactive state)
  6. VERIFY: Active tab icon is highlighted (Signal Yellow?)
  7. VERIFY: Inactive tab icons are muted (text-muted color?)
  8. VERIFY: No icon is clipped, stretched, or distorted
  9. VERIFY: stroke-width is 2px, stroke-linecap is square, stroke-linejoin is miter
  10. VERIFY: No gradients, no shadows, no animation on module icons

Cross-Browser Matrix:
| Device | Browser | Icons Render? | All Identifiable at 20px? | Notes |
|--------|---------|---------------|--------------------------|-------|
| iPhone 14 | iOS Safari 17+ | | | |
| Samsung Galaxy | Chrome Android | | | |
| MacBook | Chrome 122+ | | | |
| MacBook | Firefox 123+ | | | |
| MacBook | Safari 17+ | | | |

EXPECTED RESULT: All 6 icons pass legibility test on all target browsers.

EDGE CASES:
  - Dark mode OS setting — does it affect icon colors?
  - High-contrast accessibility mode — icons still visible?
  - Very small screen (320px width) — icons don't overlap?
SEVERITY: High
LINKED STORY: Art v1.1 Self-Critique, 20px legibility test
```

---

## Test Coverage Summary

| Set | Scenarios | Severity | Total Test Cases |
|-----|-----------|----------|-----------------|
| Set 1: Morning Open | TV-S1-001, TV-S1-002 | Critical | 2 |
| Set 2: Mid-Shift Alert | TV-S2-001 | Critical | 1 (comprehensive — covers full Process 4) |
| Set 3: End-of-Day Review | TV-S3-001 | Critical | 1 (includes role gating) |
| Set 4: Edge Cases | TV-S4-001 to TV-S4-004 | High-Critical | 4 |
| Set 5: v1.1-Specific | TV-S5-001 to TV-S5-003 | High | 3 |
| **Total** | | | **11 scenario scripts** |

---

*Jim — QA Manager*
*Canary LP | Confidential*
*February 24, 2026*
