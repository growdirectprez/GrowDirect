---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Level B UAT Plan — Guided Demo (March 3)
**Author:** Jim (QA Manager & CSM)
**Date:** February 26, 2026
**Demo Date:** Monday, March 3, 2026
**Derived from:** Jim 1A UAT Logistics Plan (Level A → Level B downscope)

---

## What Changed from Level A → Level B

| Dimension | Level A | Level B (This Plan) |
|-----------|---------|---------------------|
| Merchants | 3–5 merchants | **1 merchant** |
| Session type | Unassisted UAT | **Guided walkthrough** |
| Duration | 90-minute sessions | **60 minutes total** |
| Personas tested | Owner + Manager + Multi-store | **Owner only** |
| Role gating | Full RBAC matrix tested | **Not tested — deferred** |
| Multi-location | Required | **Not tested — deferred** |
| Square OAuth | Live sandbox required | **Seed data only — no OAuth** |
| Webhook testing | Required | **Deferred** |
| Success threshold | All 10 UAT criteria | **Merchant says "I get it" + names one use case** |
| Jim's role | Facilitator (silent observer at M-4/M-5) | **Active guide throughout** |

**What stays the same:** Jim facilitates. Jeffe observes. Phone/tablet is the device. Today's View → Chirps → Process 4 is the flow. Jim captures merchant reactions.

---

## Pre-Demo Checklist (Must Work by Friday, February 28)

These are the minimum viable requirements. If any P0 item fails the Friday dry run, demo does not proceed Monday.

### P0 — Hard blockers (demo cannot happen without these)

| # | Requirement | Owner | Status |
|---|-------------|-------|--------|
| P0-1 | App accessible on Jim's phone or tablet over local Wi-Fi or tunnel | Jeremy | Pending |
| P0-2 | Seed data loaded — merchant "Lighthouse Coffee" visible, Alex Navarro login works | Jeremy + Jim | Pending |
| P0-3 | Today's View renders on mobile — greeting, hero Chirp banner, action cards | Jeremy | Pending |
| P0-4 | Hero Chirp banner shows CASH_VARIANCE_THRESHOLD with correct amount ($17.40) | Jeremy | Pending |
| P0-5 | Tapping hero banner launches Process 4 wizard (6 steps) | Jeremy | Pending |
| P0-6 | Process 4 completes end-to-end — Chirp marked RESOLVED, returns to Today's View | Jeremy | Pending |
| P0-7 | Chirp peek indicator visible showing HIGH_NO_SALE_FREQUENCY | Jeremy | Pending |

### P1 — Strong preferences (demo works better with these, but not fatal)

| # | Requirement | Owner | Status |
|---|-------------|-------|--------|
| P1-1 | Confetti + chirp sound on wizard completion | Jeremy | Pending |
| P1-2 | Resolved Chirp (ALC-002) visible in Chirps tab with green state | Jeremy | Pending |
| P1-3 | Health bar visible beneath CANARY lockup with non-empty state | Jeremy | Pending |
| P1-4 | Time-of-day greeting says "Good morning, Alex" | Jeremy | Pending |
| P1-5 | All 6 SVG navigation icons identifiable on phone screen | Jeremy | Pending |

### P2 — Nice to have (do not block demo if missing)

| # | Requirement |
|---|-------------|
| P2-1 | Health score number visible (71/100 or similar) |
| P2-2 | Scorecard renders (even placeholder) |
| P2-3 | Fox escalation option visible at wizard step 3 (owner role) |

---

## Friday Dry Run — Go/No-Go Criteria

Jim and Jeremy run the full 60-minute demo script together on Friday, February 28, before 4:00 PM. This is the gate for Monday.

### Go criteria (all must pass)

| # | Criterion | Pass? |
|---|-----------|-------|
| G1 | Alex login works, Today's View loads in <15 seconds on mobile | ☐ |
| G2 | Hero banner shows "Drawer short $17.40 at Lighthouse Coffee" | ☐ |
| G3 | Tapping hero banner launches wizard without page reload | ☐ |
| G4 | Jim can walk through all 6 wizard steps in <8 minutes | ☐ |
| G5 | Wizard completes and returns to Today's View with Chirp resolved | ☐ |
| G6 | Chirp peek shows +1 more (HIGH_NO_SALE_FREQUENCY) | ☐ |
| G7 | No white screens or unhandled errors during the flow | ☐ |
| G8 | Jim feels he can run this demo with a merchant watching | ☐ |

### No-go criteria (any one of these = demo postponed)

- App not accessible on a real phone (not just localhost)
- Today's View doesn't render the hero Chirp banner
- Process 4 wizard crashes, hangs, or doesn't complete
- Seed data missing or merchant can't log in
- Jim encounters a P0 bug he can't work around

**Escalation:** If any no-go criterion fails Friday before 3pm, Jim notifies Jeffe immediately. Jim and Jeremy assess whether a same-day fix is achievable. If not, demo is postponed.

---

## Demo Participants

| Role | Person | Device | Notes |
|------|--------|--------|-------|
| Facilitator | Jim | Has the phone for demo device management | Jim drives the narration and the phone |
| Observer | Jeffe | His own device or watching Jim's screen | Jeffe does not intervene. He is watching the merchant, not the app. |
| Merchant | TBD (owner-operator, specialty coffee) | Jim's phone / tablet | Merchant holds the phone for the core "can you tap this?" moment |

---

## 60-Minute Demo Script

> **Setup:** Jim has the app open on Today's View, logged in as Alex Navarro, before the merchant sits down. The first thing the merchant sees is Today's View already loaded. No login ceremony.

---

### Phase 1 — Orientation (0:00–0:10)

**Goal:** Merchant understands what they're looking at before touching anything.

**Jim says:**
> "I'm going to show you something we built for store owners like you. It's a 60-second morning check — instead of digging through Square or asking your shift lead what happened yesterday, it just tells you. Let me show you what I mean."

**[Hand merchant the phone]**

> "Don't tap anything yet. Just look at the top. What does it say?"

**[Merchant reads the greeting aloud — "Good morning, Alex — 2 Chirps need you"]**

**Jim says:**
> "Chirps are the things that need your attention. Not everything — just the things that actually matter. How many do you see right now?"

**[Merchant answers: 2]**

**Jim says:**
> "Now look at the big card below the greeting. Read that to me."

**[Merchant reads the hero banner: "Drawer short $17.40 at Lighthouse Coffee — 4 min wizard"]**

**Jim says:**
> "That's your number one issue this morning. The system caught it automatically. It knows your drawer was short $17.40 when Diego closed Saturday night — and it's been sitting there since then. In a normal week, would you know that happened?"

**[Let merchant respond — capture their reaction.]**

**Jim's internal note:** If the merchant says "I'd check Square," ask them how long that takes and how often they actually do it. Don't push — just let them arrive at the insight.

---

### Phase 2 — Hero Chirp + Wizard Walk (0:10–0:35)

**Goal:** Merchant walks through Process 4 and understands what a wizard is.

**Jim says:**
> "Let's say it's Monday morning and you just got to the shop. You see this. Tap that card."

**[Merchant taps hero banner → Process 4 wizard launches]**

**Step 1 — Confirm the fact:**

**Jim says:**
> "It's asking: was the drawer actually short? This is the first step — just confirm it. Tap Yes."

**[Merchant taps Yes]**

**Jim says:**
> "See how it didn't ask you to fill out a form or write a report? It just needs a yes or no. You can also add a photo of the count sheet if you want — that becomes permanent documentation."

**Step 2 — Who touched it last:**

**Jim says:**
> "Now it's showing you who was working that shift. Diego is listed first because he was the closer. You don't have to remember — it pulled from your timecard data."

**[Merchant reviews the list]**

**Step 3 — Common causes:**

**Jim says:**
> "Now it gives you four choices. What does this look like to you?"

**[Let merchant read the four cards aloud. Let them choose one.]**

**Jim says:**
> "Whatever you tap, it's going to give you the next steps to actually fix it — not just note it. And as the owner, you also have the option to flag this for a formal investigation if you think something worse is going on."

> "For today, let's say math error. Tap that."

**Step 4 — Fix it now:**

**Jim says:**
> "This is the checklist. Check each box as you go — it's not just notes, it actually guides you through the fix."

**[Merchant checks each item]**

**Step 5 — Learn and prevent:**

**Jim says:**
> "This is optional — you can add this to your team playbook so the next shift lead sees it too. Toggle that on."

**Step 6 — Completion:**

**[Confetti + chirp sound plays]**

**Jim says:**
> "That's it. The issue is resolved, it's documented, and your Today's View is updated. Six steps, under eight minutes."

**[Return to Today's View — hero banner is gone, Chirp count drops to 1]**

---

### Phase 3 — The Full Picture (0:35–0:50)

**Goal:** Merchant sees the second Chirp and the resolved one. Understands this is a system, not a one-time alert.

**Jim says:**
> "See how the number changed? It said 2 before, now it's 1. The cash shortage is handled. But there's still one more thing."

> "See that line under the hero? The '+1 more' — tap that."

**[Merchant taps peek indicator → navigates to Chirps tab]**

**Jim says:**
> "This is everything that's flagged. The yellow one is Cody — he opened the drawer four times on Thursday without ringing anything. Classic no-sale pattern. Not necessarily theft, but worth a conversation."

> "Scroll down a little."

**[Merchant scrolls, sees the green resolved Chirp — HIGH_REFUND_FREQUENCY from Saturday]**

**Jim says:**
> "That green one — that was Diego's refund pattern from Saturday. Alex already handled it Sunday morning. The system shows you what was resolved and when, so nothing falls through the cracks."

> "In a normal week — how often do you know about refund patterns this fast?"

**[Let merchant respond. Don't fill the silence.]**

---

### Phase 4 — Merchant's Turn (0:50–0:57)

**Goal:** Merchant drives solo. Can they find and identify a Chirp without Jim prompting?

**[Reset Today's View by reloading the page or navigating home]**

**Jim says:**
> "Now you drive. Pretend it's Monday morning. You're the first one in. What's the first thing you'd do with this?"

**[Hand merchant the phone. Step back. Observe.]**

**What Jim watches for:**
- Does the merchant tap the hero banner without being told?
- Do they verbalize what they're reading?
- Do they look confused, or do they get it?
- How long until they identify an action they'd take?

**Target:** Merchant taps the hero or an action card within 90 seconds.

**Jim does NOT intervene** unless the merchant is genuinely stuck for more than 2 minutes. If they need a hint: "What does that card at the top say?"

---

### Phase 5 — Close (0:57–1:00)

**Jim says:**
> "So — what do you think? If this was in your store, what's one thing you'd use it for?"

**[Let merchant answer. This is the key data point.]**

**Jim says:**
> "That's exactly what it's built for. We're testing it with a small group of shop owners right now. We'd love to have you as one of the first."

> "I'll have Jeffe follow up with next steps. Any questions for me before we wrap up?"

**[Collect questions. Don't sell. Just listen.]**

---

## Observation Template

Jim fills this out DURING the demo, or immediately after (before debrief).

### Merchant Reactions

| Moment | Merchant Said / Did | Jim's Read |
|--------|---------------------|------------|
| First saw greeting | | |
| First saw hero banner | | |
| First tapped wizard | | |
| Wizard step 3 (common causes) | | |
| Saw completion confetti | | |
| Saw resolved Chirp | | |
| Solo phase (unguided) | | |
| Final "what would you use this for?" | | |

### Key Captures

| Question | Answer |
|----------|--------|
| Did merchant identify the #1 action within 90 seconds? | Y / N — took \_\_ seconds |
| Did merchant verbalize understanding at any point? | Y / N — quote: |
| Where did merchant hesitate or look confused? | |
| What excited the merchant? | |
| What confused the merchant? | |
| Did merchant say "I get it" (or equivalent)? | Y / N |
| What did merchant say they'd use it for? | |
| Any feature they wished they saw? | |
| Would this merchant want to continue? | Y / N / Maybe |

### Technical Issues Encountered

| # | Issue | When | Impact |
|---|-------|------|--------|
| 1 | | | |
| 2 | | | |

---

## Post-Demo Debrief (Jim + Jeffe — immediately after merchant leaves)

15 minutes. No phones. Jim reads from the observation template. Jeffe listens.

### Questions

1. **The big one:** Did the merchant get it? What was the moment they visibly understood?
2. **The confusion point:** Where did they hesitate? What did that tell us about the UI?
3. **The excitement point:** What lit them up? Is that what we expected?
4. **The 90-second test:** Did they find the action on their own, or did Jim have to redirect?
5. **The "I'd use it for" answer:** What did they say? Does it match the use case we designed for?
6. **Wizard pacing:** Did the 6 steps feel fast or slow to the merchant?
7. **Device feel:** Did the app feel like a phone app or a website? Any scroll / tap friction?
8. **Merchant temperature:** Is this someone who would become a beta user? How likely (1–5)?
9. **What do we need to change before the next demo?** (Not a wish list — just the one or two things that actually mattered today.)
10. **Go / no-go for pursuing Offset Coffee?** If Jeffe's scouting visit goes well today, does Monday's data support moving forward?

### Jim's debrief write-up

Jim files a one-page debrief to `_ALX/WorkOrders/output/Jim/Jim_LevelB_DemoDebrief_Mar3.md` by end of Monday. Jeffe reviews Tuesday morning.

---

## Success Criteria (Level B)

Simple pass/fail. Both must be true for Monday to count as a win.

| # | Criterion | Pass/Fail |
|---|-----------|-----------|
| 1 | Merchant says "I get it" or equivalent verbalization of understanding | |
| 2 | Merchant identifies at least one specific thing they would use Canary for in their store | |

**Bonus (not required, but notable):**
- Merchant asks "how do I sign up?"
- Merchant says something was surprising or better than expected
- Merchant completes the Process 4 wizard without Jim narrating each step

---

## What We Are NOT Testing Monday

To stay in scope and avoid demo sprawl:

- ❌ Role-gating (Manager vs. Owner views)
- ❌ Multi-location switching
- ❌ Square OAuth or live transaction sync
- ❌ Fox workbench (unless merchant asks about investigations)
- ❌ Scorecard detail (health bar is enough)
- ❌ Processes 1, 2, or 3 (if time remains, we can show briefly, but don't plan for it)
- ❌ Webhook delivery
- ❌ Performance benchmarking

These are all Level A scope. Level B is: Today's View → hero Chirp → Process 4 wizard → complete → merchant gets it.

---

*Jim — QA Manager & CSM*
*Canary LP | Confidential*
*February 26, 2026*
