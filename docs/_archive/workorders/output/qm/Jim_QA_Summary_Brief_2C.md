---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# QA Summary Brief — For Jess (Companion Guide Input)
**Date:** February 24, 2026
**Author:** Jim (QA Manager & CSM)
**Purpose:** Merchant-perspective descriptions of every Companion workflow, written in plain language for Jess to use in the Functional and Technical Companion Guides.
**Canonical Terminology:** Per PhD Alignment Brief Section 6 — all terms verified.

---

## 1. What the Merchant Sees: Today's View

Today's View is the first screen every merchant sees when they open Canary. It is NOT a dashboard. There are no charts, no tables, no raw numbers. It is a calm, opinionated guide that answers one question: "What needs my attention right now?"

### Screen Layout (Top to Bottom)

**Top Bar:** The Canary avatar (a small animated bird with a green pulse when everything is fine) sits in the top-left corner. Next to it, a personalized greeting: "Good morning, Alex — 2 Chirps need you." The greeting changes based on time of day and the number of active Chirps.

**Hero Chirp Banner:** If there are active Chirps, the most urgent one appears as a large, tappable banner below the greeting. It uses Canary's health-wave animation — a flowing color gradient that shifts from yellow to red based on severity. The banner tells the merchant exactly what's wrong and how long it will take to fix: "Drawer short $18 at Store #1 — 4 min wizard." Tapping the banner launches the relevant wizard immediately.

**Chirp Peek Indicator:** If there are 2 or more active Chirps, a subtle line appears beneath the hero banner showing the next Chirp: "+1 more: High no-sale frequency at Store #1." Tapping this takes the merchant to the full Chirps list — it does NOT launch a wizard. This element disappears when there are 0 or 1 Chirps, and it does not count as one of the action cards.

**Action Cards (Maximum 3):** Below the hero, up to 3 large tappable cards suggest what the merchant should do next. The cards change based on time of day. In the morning, a merchant might see "Open the Store," "Count the Drawer," and "Check Yesterday's Shrink." In the evening, they might see "Count the Drawer," "Review Today's Sales," and "Lock Up." Each card has an animal icon matching its module (Rooster for daily operations, Bull for inventory, Canary for alerts). There are never more than 3 cards — this is a hard rule.

**Health Bar:** A thin gradient bar beneath the Canary logo shows the store's overall health: green (all clear), yellow (some attention needed), red (urgent issues). It is a quick visual pulse, not a detailed metric.

### Role-Based Differences

| What | Owner Sees | Store Manager Sees |
|------|-----------|-------------------|
| Greeting | "Good morning, [name] — X Chirps need you" | Same |
| Hero Chirp | Full details including financial amounts | Same |
| Action Cards | Up to 3, including analytics-oriented cards | Up to 3, operations-focused only |
| Navigation | All 6 modules: Canary, Owl, Fox, Bull, Rooster, Goose | 4 modules only: Canary, Bull, Rooster (+ Owl if applicable). NO Fox, NO Goose |
| Team Performance Scorecard | Visible | Hidden |
| Fox Case Management | Full access | No access |
| Goose Treasury | Full access | No access |
| Farm (Settings) | Full access including team management | Limited access |

### Bottom Navigation

Six animal icons in the bottom navigation bar, each representing a module:

1. **Canary** (bird icon) — Home and Chirps. This is the alert center.
2. **Owl** (owl with twin eyes icon) — Insights and analytics. Owner-only for deep dives.
3. **Fox** (angular face icon) — Investigation and case management. Owner-only.
4. **Bull** (horned head icon) — Inventory management and cash counting.
5. **Rooster** (bird with comb icon) — Daily operations, team performance, shift routines.
6. **Goose** (long-necked bird icon) — Treasury, Bitcoin, and financial management. Owner + Manager.

The icons are custom SVGs designed in a geometric, minimal style (not cartoon, not cute). They use simple shapes — circles, triangles, rectangles — and are identifiable even at small sizes on mobile screens. The active tab is highlighted in Signal Yellow; inactive tabs use a muted gray.

---

## 2. How Chirps Work (The Alert System)

A Chirp is Canary's name for an alert. When something unusual happens in the store — a cash drawer comes up short, an employee processes too many refunds, a discount pattern looks suspicious — Canary generates a Chirp.

**Key facts about Chirps for the guide:**

Chirps are not raw data alerts. Each Chirp is tied to a specific guided wizard that helps the merchant investigate and resolve the issue. The merchant never sees a Chirp without a clear next step. There are 22 detection rules in the system (covering cash drawer anomalies, refund patterns, timecard inconsistencies, inventory shrinkage, gift card abuse, and loyalty fraud), but the merchant doesn't need to know this. They just see: "Something needs attention. Tap here. I'll walk you through it."

Chirps have severity levels that affect how they're displayed: yellow for attention-needed, red for urgent. The hero banner always shows the most urgent Chirp. When a merchant resolves a Chirp through its wizard, the Chirp is marked as resolved and disappears from Today's View.

---

## 3. The Guided Wizards (How Merchants Fix Things)

Every action in Canary goes through a wizard. There are no standalone forms, no raw data entry screens, no "figure it out yourself" pages. Each wizard is a step-by-step flow designed to take less than 8 minutes, with large touch targets for mobile use.

### Process 1: Open the Store

**Who uses it:** Store Manager, first thing in the morning.
**What happens:** 4 steps. The merchant confirms the store is ready (lights, register, signage), counts the starting cash in the drawer, confirms the opening, and gets a cheerful "Store is open!" completion screen. Behind the scenes, this creates a cash drawer shift record.
**Time:** Under 5 minutes.
**What could go wrong:** The store is already marked as open by another manager. The system catches this and tells the merchant — no duplicate records created.

### Process 2: Count the Drawer

**Who uses it:** Whoever closes the shift, or anyone triggered by a Chirp.
**What happens:** 5 steps. The merchant selects which drawer to count, enters the actual cash amount, the system automatically calculates the variance (did the drawer come up short or over?), the merchant documents any discrepancy, and the shift closes with a summary. If the variance exceeds the threshold ($10), a Chirp fires automatically.
**Time:** Under 6 minutes.
**Completion varies by outcome:** If the drawer balances perfectly, the merchant gets confetti and a "Perfect count!" message. If there's a significant variance, the tone is more serious — no celebration, just a clear next step.

### Process 3: Resolve Refund Alert

**Who uses it:** Anyone who receives a HIGH_REFUND_FREQUENCY Chirp.
**What happens:** 5 steps. The merchant reviews the facts (which employee, how many refunds, total amount), examines each individual refund with line-item detail, assesses whether the pattern is legitimate or suspicious, takes appropriate action, and resolves the Chirp.
**Role difference:** The Owner sees a "Flag for Fox investigation" option at the assessment step. The Manager does not — they see options appropriate to their authority level. If the Manager thinks something is suspicious, the wizard suggests they talk to the owner rather than exposing the Fox investigation system.
**Time:** Under 7 minutes.

### Process 4: Resolve Cash Drawer Shortage

**Who uses it:** Anyone who receives a CASH_VARIANCE_THRESHOLD Chirp.
**What happens:** 6 steps — the most detailed wizard in MVP. The merchant confirms the shortage is real (with optional photo evidence), sees who worked the drawer last (pulled from timecard data), chooses from common cause categories (forgot a refund, math error, suspected theft, or other), follows a fix-it checklist, gets a prevention tip, and sees a completion screen.
**Role difference:** Same as Process 3 — the Owner can escalate to Fox. The Manager cannot.
**Evidence chain:** If the merchant takes a photo at step 1, that photo is stored as immutable evidence. It cannot be modified or deleted. If the case is escalated to Fox, the photo is already attached to the investigation.
**Time:** Under 8 minutes.

---

## 4. What Happens After a Wizard Completes

When a merchant finishes a wizard, several things happen behind the scenes:

1. **The Chirp is resolved.** It disappears from Today's View and moves to the resolved list.
2. **A record is created.** Depending on the process, this might be a cash drawer close event, a Chirp resolution note, or a Fox case creation.
3. **Today's View updates.** The action cards refresh. If the merchant resolved their only Chirp, the hero banner disappears and the greeting changes to "All clear."
4. **Evidence is preserved.** Any photos, notes, or selections are stored permanently. They cannot be changed after the fact — this protects both the merchant and any employees involved.
5. **The Rooster (QA system) can verify** every step of this flow automatically.

---

## 5. The Scorecards (Contextual, Not Dashboard)

Canary has 5 scorecards, but merchants rarely see them all at once. Scorecards appear in context — after you've done something, or when you ask for a specific view.

| Scorecard | What It Shows | Where It Appears | Who Can See It |
|-----------|-------------|-----------------|----------------|
| Daily Shrink Score | One big number: today's estimated shrinkage | Today's View widget | Everyone |
| Alert Heatmap | Pattern of Chirps over time | Inside the Chirps tab | Everyone (after resolving 3+ Chirps) |
| Team Performance | Employee-level metrics | Rooster tab | Owner only |
| Inventory Health | Stock accuracy, adjustment frequency | Bull tab (after counting) | Owner + Manager |
| Treasury Snapshot | Cash position, payment trends | Goose tab (one extra tap) | Owner + Manager |

**Design rule:** Every scorecard is a single calm card with one headline number (e.g., "$42"), one trend arrow (up or down from last period), and one "Fix It" button that launches the relevant wizard. No charts. No tables. One number, one direction, one action.

---

## 6. Error States and How They're Handled

Canary never shows a white screen, a stack trace, or a generic "Something went wrong" message. Error handling follows the Companion philosophy: calm, specific, and actionable.

| Situation | What the Merchant Sees |
|-----------|----------------------|
| Network offline | Canary bird shows a "sleeping" state. Message: "You're offline — we'll refresh when you're back." Last-known data stays visible. |
| Server error (500) | Canary bird shows "thinking" animation (not a spinner). Message: "Canary is taking a moment. Try again shortly." |
| Wizard step fails to load | "This step couldn't load. Tap to retry." Retry button, not a dead end. |
| Photo upload fails | "Photo didn't upload. You can try again or skip for now." Wizard continues without blocking. |
| Permission denied (wrong role) | "This area is for store owners. Talk to [owner name] if you need access." Redirect to Today's View. |
| Session expired | Redirect to login with message: "Please log in again to continue." |
| Data not available (missing timecards, etc.) | "We don't have timecard data for today. You can still complete this step manually." Wizard adapts, doesn't crash. |

**The Canary bird is the error state mascot.** When something goes wrong, the bird's animation changes — from the idle green pulse (everything is fine) to a "thinking" state (loading/error) to a "sleeping" state (offline). This gives the merchant a visual cue without alarming text.

---

## 7. The Phone Test Assessment

Jim's "phone test" question: would this design make my phone ring at 2 AM?

**Today's View:** Low ring risk. It's a simple, read-heavy screen. The main risk is the time-of-day card algorithm showing the wrong suggestions (e.g., "Open the Store" at 9 PM). This needs timezone testing but is unlikely to generate support calls.

**Wizard Flows:** Medium ring risk, concentrated in Process 4 (cash shortage). This is the most complex wizard and involves photo uploads, employee data lookups, and Fox escalation. The most likely support call: "I took a photo but it didn't upload" or "The wizard didn't show my employee's name." Both are handled by the edge case fallbacks designed into the wizard (skip photo, manual entry for missing employees).

**Role Gating:** Low ring risk if implemented correctly. The danger zone is a Manager seeing Owner-only content (Fox cases, financial data). If the 403 redirects work properly, this never surfaces. If they don't, it's a P1 bug.

**SVG Icons:** Low ring risk. The icons are simple and geometric. The only concern is the 20px legibility test on older Android devices with lower pixel density. Needs real-device testing during UAT.

**Overall assessment:** This design should NOT make Jim's phone ring. The guided wizard pattern eliminates the #1 source of merchant confusion (figuring out what to do with raw data). The max-3-card rule prevents information overload. The role gating prevents permission-related confusion. The error states prevent blank-screen panic calls. If Jeremy implements it faithfully to Art's v1.1 wireframe, merchant support calls should be limited to actual bugs, not UX confusion.

---

## 8. Terminology Reference for Jess

Per PhD Alignment Brief Section 6, use ONLY these terms in the Companion Guides:

| Concept | Correct Term | DO NOT Use |
|---------|-------------|------------|
| Home screen | **Today's View** | Dashboard, Home Page, Landing Page |
| Alert | **Chirp** | Alert, Notification, Warning, Chirp Engine |
| Guided interaction | **Wizard** | Form, Incident Report, Workflow |
| Product name | **Canary** (product), **Guided Operations Companion** (feature) | Canary LP (as feature name), Command Center |
| Settings area | **Farm** | Settings, Preferences, Admin |
| The 6 modules | **Canary, Owl, Fox, Bull, Rooster, Goose** | Any other names |
| Control paradigm | **Companion** | Command Center, Dashboard |

---

*Jim — QA Manager & CSM*
*Canary LP | Confidential*
*February 24, 2026*
*Output: `_ALX/WorkOrders/output/Jim/Jim_QA_Summary_Brief_2C.md`*
