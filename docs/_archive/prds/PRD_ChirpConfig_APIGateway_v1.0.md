---
type: workorder
domain: chirp
status: active
created: 2026-03-18
updated: 2026-03-19
---
# PRD: Chirp Config + API Gateway — Live Sandbox for Merchant Onboarding

**PRD ID:** E1-F14
**Version:** 1.0
**Date:** February 26, 2026
**Author:** ALX (Chief of Staff), per Jeffe directive
**Priority:** 🔴 HIGH — Critical path for live data validation
**Status:** DRAFT v1.1 — Updated with three-phase rollout per Jeffe directive (Feb 26)

---

## Problem Statement

Canary's detection engine has 26 Chirp rules across 8 categories, a working webhook router, and a ThresholdManager with per-merchant config — but today there is no way for a merchant to see which Chirps are active, turn them on or off, or receive alerts from live Square data. The Level B demo uses seed data, which proves the UI works but cannot validate whether Chirps fire correctly on real transactions. To onboard Offset Coffee as a live sandbox partner and prove product-market fit, we need two things: a merchant-facing Chirp config page and a working API gateway that connects Square's live webhook stream to our detection engine.

**Who is affected:** Jeffe (cannot validate Chirps against real data), Jeremy (cannot test webhook-to-Chirp pipeline end-to-end), Jim (cannot QA with realistic alert patterns), and ultimately the merchant (no control over which alerts they receive).

**Impact of not solving:** Without live data flowing through the detection engine, Canary remains a prototype with fake numbers. The merchant never says "I get it" because the "it" is simulated.

---

## Go-to-Market Rollout — Three Phases

> **CONFIDENTIAL.** The phased rollout below is internal strategy. Phase timing is competitive advantage — we don't announce until Phase 3. No external communication until Jeffe gives the word.

### Phase 1: GrowDirect Lab (This Week — Internal Sandbox)

**What:** GrowDirect signs up as its own Square merchant. Jeffe creates a Developer account and a Merchant account. Jeremy wires OAuth from Canary to GrowDirect Lab's own Square account. Jeffe generates real transaction data by ringing up test purchases, opening the cash drawer, processing refunds — all through Square's real POS. Canary ingests this data via webhooks and fires Chirps on it.

**Why:** Every question a merchant would ask, Jeffe has already answered — because he lived it. The onboarding flow, the OAuth consent screen, the first Chirp firing, the "does this make sense?" moment — all validated internally before any merchant conversation.

**Success gate:** Jeffe toggles on C-102 (Drawer came up short), opens a cash drawer, closes it $20 short, and sees a RED Chirp appear in Today's View within minutes. If that works, Phase 1 is done.

**What Jeffe does:**
1. Sign up for Square Developer account at developer.squareup.com (business name: "GrowDirect" or "GrowDirect Lab")
2. Sign up for Square Merchant account at squareup.com (free tier — $0/month, no EIN required)
3. Download Square POS app on phone (optional — can also use Square's Virtual Terminal in browser)
4. Jeremy wires OAuth: Canary app redirects to Square → Jeffe authorizes on his own merchant account → tokens flow back
5. Jeremy registers webhook subscriptions → Square starts sending events
6. Jeffe generates test data: ring up a latte ($5.50), do a refund, open the drawer, short it, void a transaction
7. Watch Chirps fire in Today's View on real data from your own Square account

**Square Developer Account Setup Checklist:**

| Step | Action | Where | Notes |
|---|---|---|---|
| 1 | Create developer account | developer.squareup.com | Email, password, business name "GrowDirect" |
| 2 | Create application | Developer Console → Applications | Name it "Canary LP" or "Canary Dev" |
| 3 | Note Application ID | OAuth page in console | This is the `client_id` |
| 4 | Note Application Secret | OAuth page in console | This is the `client_secret` — never share publicly |
| 5 | Set OAuth redirect URL | OAuth page in console | `http://localhost:5002/auth/square/callback` for dev, ngrok URL for webhook testing |
| 6 | Set webhook URL | Webhooks page in console | ngrok tunnel URL → `https://{tunnel}.ngrok.io/webhooks/square` |
| 7 | Select webhook event subscriptions | Webhooks page in console | All 8 event types (payment, refund, order, cash_drawer, labor, gift_card, inventory) |
| 8 | Note webhook signature key | Webhooks page in console | Used for HMAC-SHA256 verification (already implemented) |

**Square Merchant Account Setup Checklist:**

| Step | Action | Where | Notes |
|---|---|---|---|
| 1 | Create merchant account | squareup.com/signup | Free tier. Business type: "Individual" or "Retail" |
| 2 | Business name | Signup flow | "GrowDirect Lab" — this appears on receipts |
| 3 | Skip hardware | Signup flow | Don't need a card reader for testing — use Virtual Terminal |
| 4 | Access Dashboard | squareup.com/dashboard | This is the merchant view — where a real merchant lives |
| 5 | Create test items | Dashboard → Items | "Latte" ($5.50), "Pastry" ($3.75), "Drip Coffee" ($3.00) — simulate a coffee shop |
| 6 | Enable Cash Drawer tracking | Dashboard → Settings → Cash Drawers | Required for C-101 to C-104 Chirps |
| 7 | Create test employees | Dashboard → Team | "Maria Santos" (shift lead), "Test Employee 2" — for timecard Chirps |
| 8 | Process test transactions | Virtual Terminal or POS app | Ring up items, do refunds, open drawer, close short |

### Phase 2: Friendly Local Merchant (Week 2 — Offset Coffee or Referral)

**What:** One merchant. Local. Friendly. Ideally a referral or someone Jeffe has a relationship with. Completely confidential — NDA signed before any data flows. Jeffe walks in with GrowDirect Lab already running and shows real results: "Here's what Canary found on our own test store. Want to see yours?"

**Why:** Phase 1 proves the pipeline works. Phase 2 proves the *product* works — that the Chirps firing on a real merchant's real data are useful, actionable, and make sense. This is where we learn if our 26 rules produce signal or noise.

**The merchant pitch (Jeffe's script — see separate doc):**
- You're not asking them to test software. You're offering them a free look at what's happening in their business that they can't see today.
- You already know the flow because you did it in Phase 1. You're the guide, not the one asking questions.
- Syd's merchant pack (NDA, Beta Tester Agreement, DPA) gets signed before any OAuth connection.
- The merchant goes through the same OAuth flow Jeffe already tested — they authorize on Square's page, data starts flowing, Chirps fire within the hour (backfill pulls their last 7 days).

**Onboarding flow (what the merchant actually does):**

| Step | What Happens | Who Does It | Time |
|---|---|---|---|
| 1 | Jeffe pitches the concept, shows GrowDirect Lab results on his phone | Jeffe | 10 min |
| 2 | Merchant signs NDA + Beta Tester Agreement (Syd's pack) | Merchant + Jeffe | 5 min |
| 3 | Merchant taps "Connect Square" in Canary on Jeffe's device | Merchant | 30 sec |
| 4 | Square OAuth page loads — merchant logs into their own Square account | Merchant | 1 min |
| 5 | Merchant sees Square's consent screen: "Canary wants to access: Payments, Orders, Cash Drawers, Timecards, Employees, Items, Profile" | Merchant | 30 sec |
| 6 | Merchant taps "Allow" — Square redirects back to Canary | Merchant | instant |
| 7 | Canary backfills 7 days of transaction history | Automatic | 1-5 min |
| 8 | Merchant opens Chirp Config, scrolls the list, toggles on 3-5 Chirps | Merchant + Jeffe guiding | 3 min |
| 9 | Today's View loads with real Chirps from their actual last week | Automatic | instant |
| 10 | Jeffe walks merchant through the first Chirp and wizard | Jeffe + merchant | 5 min |

**Total onboarding time: ~25 minutes** (including pitch). Jeffe has done this before — no fumbling.

**Success gate:** Merchant sees a real Chirp from their own data, says "oh wow, I didn't know that was happening," and asks "what else can it do?"

### Phase 3: Blitz (After Phase 2 Validates)

**What:** Worm goes underground. Full push — social media, Google Business Profile, local SEO, content marketing, Square Marketplace listing. Big bang. All channels at once.

**Why:** By now we have a proven onboarding flow (tested in Phase 1, validated in Phase 2), real screenshots from a real merchant (anonymized), a tight pitch script, and confidence that the Chirps produce value. We're not launching a beta — we're launching a product that already works.

**Trigger:** Jeffe gives the word. Not before.

**What Worm prepares during Phases 1-2 (silent):**
- Google Business Profile for Canary LP — optimized, ready to go live
- 10 service-area landing pages for top Square merchant metros
- 30-day content calendar (GBP posts, blog content, social media)
- Square Marketplace listing draft (Condor sanitizes, PhD reviews IP, Syd reviews legal)
- Launch announcement assets (Will + Art collaborate)

**What fires on launch day:**
- GBP goes live
- Social media push across all channels
- Square Marketplace listing submitted
- Content calendar begins executing
- Will's LEO playbook activates — agent discoverability, API schema optimization

**Confidentiality:** Nothing from Phase 3 prep is visible externally until Jeffe says go. Worm builds in the dark. When the switch flips, everything goes live simultaneously.

---

## Goals

1. **Merchant controls their own alerts.** A merchant can see all 26 Chirp types, toggle each on/off, and have that decision immediately affect what alerts fire.
2. **Live Square data flows into Chirp engine.** Offset Coffee's real transactions, refunds, cash drawer shifts, and timecards enter Canary via Square webhooks, are parsed, stored, and evaluated against active rules.
3. **First real Chirp fires within 48 hours of merchant onboarding.** Once OAuth is connected and Chirps are toggled on, the system produces a real alert from real data — not seed data.
4. **Merchant sees value without noise.** Default state is all Chirps OFF. Merchant opts in to what they care about. No alert fatigue on day one.
5. **Developer can debug the full pipeline.** Jeremy can trace a Square webhook from ingestion → parsing → storage → rule evaluation → Chirp creation → Today's View rendering.

---

## Non-Goals

1. **Not building a settings page.** This is a single-purpose Chirp toggle list, not a general settings/preferences UI. No profile, no notifications prefs, no account management.
2. **Not customizing thresholds in v1.** The ThresholdManager supports per-merchant threshold overrides, but v1 of the config page is ON/OFF only. Threshold tuning is Phase 2 (the slider beneath the toggle).
3. **Not multi-location scoping.** v1 applies Chirp config at the merchant level, not per-location. Multi-location config is Sprint 7+.
4. **Not real-time push notifications.** v1 fires Chirps into the queue for Today's View. Push notifications (SMS, email, mobile push) are a separate feature (E1-F13, Sprint 3+).
5. **Not building Square OAuth from scratch.** We use Square's standard OAuth 2.0 flow. No custom auth layer.

---

## User Stories

### As a Merchant Owner (Offset Coffee)

- **US-1:** As a merchant, I want to see a list of every type of alert Canary can watch for, so I understand what the product does before I turn anything on.
- **US-2:** As a merchant, I want to toggle individual alert types on or off with a simple switch, so I only get alerts about things I actually care about.
- **US-3:** As a merchant, I want all alerts to start OFF by default, so I'm not overwhelmed the moment I connect my account.
- **US-4:** As a merchant, I want to connect my Square account with one tap, so Canary can start watching my real transactions.
- **US-5:** As a merchant, I want to see my first real alert within a day of turning on a Chirp, so I know the system is actually working with my data.

### As Jeffe (CEO / Product Validator)

- **US-6:** As the product owner, I want to plug into a real merchant's Square account and see what Chirps fire on their actual data, so I can validate that our detection rules produce useful, actionable alerts — not noise.
- **US-7:** As the product owner, I want to sit with the merchant while they scroll through the Chirp list and choose which ones to turn on, so I can observe which loss prevention concerns resonate with a real small business operator.

### As Jeremy (Developer)

- **US-8:** As a developer, I want to see Square webhook events arrive, get parsed, get stored, and trigger Chirp evaluation in a single traceable pipeline, so I can debug and optimize the detection engine against real-world data shapes.
- **US-9:** As a developer, I want a local development path where I can replay captured webhooks against the Chirp engine, so I can iterate without depending on live Square events.

---

## Feature 1: Chirp Config Page

### Route

`/companion/chirps/config`

### Layout

A single scrollable page. No tabs, no nested navigation, no settings categories. The merchant scrolls a list.

**Header:**
- Page title: "Your Alerts"
- Subtitle: "Turn on the things you want Canary to watch for."
- Active count badge: "3 of 26 active" (updates live as toggles change)

**List:**
- Each row is one Chirp type
- Grouped by category with a thin section divider and category label (Payment, Cash Drawer, Order/Line-Item, Timecard, Void, Gift Card, Loyalty)
- 8 category groups, 26 total rows

**Each Row Contains:**

| Element | Description |
|---|---|
| Severity indicator | Color dot — RED (critical/high), YELLOW (medium), GREEN (low) — matches Art's v1.1 color system |
| Chirp name | Human-readable, one line. E.g., "Drawer came up short" not "CASH_VARIANCE_THRESHOLD" |
| Description | One sentence. What this watches for in plain merchant language. E.g., "Alerts you when a cash drawer count doesn't match what the register says." |
| Toggle switch | ON/OFF. Default: OFF. Saves immediately on toggle (no save button). |

**Behavior:**
- Toggle saves via PUT to `/api/chirp/rules/{rule_id}/thresholds` (sets `enabled: true/false`)
- No confirmation dialog on toggle — instant, reversible
- Active count in header updates immediately
- Scrolls naturally on mobile — full list visible, no pagination
- Category sections are collapsible (nice-to-have, not required for v1)

### Human-Readable Chirp Names

The spec below maps each rule ID to a merchant-friendly name and one-line description. These are the strings that appear on the config page. No rule IDs, no technical jargon.

#### Payment Alerts

| Rule ID | Merchant Name | Description |
|---|---|---|
| C-001 | Quick refund after sale | Flags when a refund happens within minutes of the original sale |
| C-002 | Too many refunds from one employee | Flags when an employee's refund rate is unusually high |
| C-003 | Round-dollar pattern | Flags clusters of round-dollar transactions that may indicate test charges |
| C-004 | After-hours transaction | Flags sales or refunds that happen outside your normal business hours |
| C-005 | Same card used repeatedly | Flags when the same card is used many times in a short window |
| C-006 | Split payment pattern | Flags clusters of split-tender transactions in a short window |
| C-007 | Large refund | Flags any single refund above a dollar threshold |
| C-008 | Too many manual card entries | Flags when an employee keys in card numbers instead of swiping or tapping |

#### Cash Drawer Alerts

| Rule ID | Merchant Name | Description |
|---|---|---|
| C-101 | Too many no-sale drawer opens | Flags when the drawer is opened without a sale too many times in a shift |
| C-102 | Drawer came up short | Flags when a cash drawer count doesn't match what the register says |
| C-103 | Unusual paid-out | Flags paid-out amounts above a threshold without manager override |
| C-104 | After-hours drawer open | Flags when the cash drawer is opened outside business hours |

#### Order & Line-Item Alerts

| Rule ID | Merchant Name | Description |
|---|---|---|
| C-201 | Heavy discounting | Flags when average discounts on orders are unusually high |
| C-202 | Too many voided items | Flags when the void rate on line items exceeds a threshold |
| C-203 | Discount without approval | Flags discounts on high-value items that weren't manager-approved |

#### Timecard Alerts

| Rule ID | Merchant Name | Description |
|---|---|---|
| C-301 | Sale while off the clock | Flags when a payment is processed by an employee with no active timecard |
| C-302 | Sale during a break | Flags when a payment is processed by an employee during their declared break |
| C-303 | Wrong location | Flags when an employee processes a sale at a different location than where they clocked in |

#### Void Alerts

| Rule ID | Merchant Name | Description |
|---|---|---|
| C-501 | Too many voids in a shift | Flags when an employee voids more than a set number of transactions per shift |
| C-502 | Post-void detected | Flags when a completed transaction is voided after the fact |

#### Gift Card Alerts

| Rule ID | Merchant Name | Description |
|---|---|---|
| C-601 | Rapid gift card loading | Flags multiple gift card loads in a short window |
| C-602 | Gift card load-and-drain | Flags when a gift card is fully redeemed shortly after being loaded |

#### Loyalty Alerts

| Rule ID | Merchant Name | Description |
|---|---|---|
| C-801 | Rapid point accumulation | Flags clusters of loyalty point events in a short window |
| C-802 | Large point redemption | Flags when loyalty points redeemed exceed a threshold |
| C-803 | Points earned at multiple locations quickly | Flags loyalty activity at multiple locations in a short time |
| C-804 | Bulk enrollment from one employee | Flags when one employee enrolls many new loyalty members |

### React Component Shape

```
ChirpConfigPage
├── Header (title, subtitle, active count)
└── ScrollView
    ├── CategorySection ("Payment Alerts")
    │   ├── ChirpRow (C-001)
    │   ├── ChirpRow (C-002)
    │   └── ...
    ├── CategorySection ("Cash Drawer Alerts")
    │   ├── ChirpRow (C-101)
    │   └── ...
    └── ... (8 total categories)
```

**ChirpRow props:**
```
{
  rule_id: string,          // "C-102"
  name: string,             // "Drawer came up short"
  description: string,      // "Alerts you when..."
  severity: "critical" | "high" | "medium" | "low",
  enabled: boolean,         // toggle state
  onToggle: (rule_id, enabled) => void
}
```

### API Contract

**GET** `/api/chirp/config`
Returns all 26 rules with current merchant-specific enabled state and thresholds.

```json
{
  "merchant_id": "offset-coffee-001",
  "active_count": 3,
  "total_count": 26,
  "categories": [
    {
      "category": "cash_drawer",
      "label": "Cash Drawer Alerts",
      "rules": [
        {
          "rule_id": "C-102",
          "name": "Drawer came up short",
          "description": "Alerts you when a cash drawer count doesn't match what the register says.",
          "severity": "high",
          "enabled": true,
          "default_thresholds": { "variance_cents": 2000 },
          "merchant_thresholds": null
        }
      ]
    }
  ]
}
```

**PUT** `/api/chirp/rules/{rule_id}/toggle`
Toggles a single rule on or off for the merchant.

```json
// Request
{ "enabled": true }

// Response
{ "rule_id": "C-102", "enabled": true, "effective_thresholds": { "variance_cents": 2000 } }
```

> **Note:** The existing `chirp_wired.py` blueprint already has GET `/rules`, GET `/config`, and PUT `/rules/{rule_id}/thresholds`. The toggle endpoint is a thin wrapper — it sets `enabled` in `merchant_rule_config` without requiring threshold values.

---

## Feature 2: API Gateway — Square Live Data Pipeline

### Overview

The API gateway connects a merchant's Square account to Canary's detection engine. It handles OAuth authorization, webhook registration, event ingestion, parsing, storage, and Chirp evaluation. Most of this pipeline already exists in code (`webhooks_wired.py`, `webhook_router.py`, `chirp_service.py`). What's needed is wiring the OAuth flow and standing up the webhook subscription with Square.

### OAuth Flow

**Route:** `/auth/square/connect`

1. Merchant taps "Connect Square" on the Chirp Config page (or a dedicated onboarding screen)
2. Canary redirects to Square's OAuth authorization page with scopes:
   - `PAYMENTS_READ` — transactions, refunds
   - `ORDERS_READ` — line items, tenders, discounts
   - `TIMECARDS_READ` — employee clock-in/out
   - `CASH_DRAWERS_READ` — shift open/close, events
   - `EMPLOYEES_READ` — employee roster
   - `ITEMS_READ` — product catalog
   - `MERCHANT_PROFILE_READ` — business name, locations
3. Merchant authorizes on Square's page
4. Square redirects back to `/auth/square/callback` with authorization code
5. Canary exchanges code for access token + refresh token
6. Tokens stored in `canary_app.merchant_integrations` (encrypted at rest)
7. Canary registers webhook subscriptions with Square for all supported event types

### Webhook Subscription Registration

After OAuth completes, Canary calls Square's Webhook Subscriptions API to register for:

| Event Type | Maps To |
|---|---|
| `payment.created`, `payment.updated` | Transactions → Payment Chirps (C-001 to C-008) |
| `refund.created` | Refund records → Refund Chirps (C-001, C-002, C-007) |
| `order.created`, `order.updated` | Line items + tenders → Order Chirps (C-201 to C-203) |
| `cash_drawer.shift.created`, `cash_drawer.shift.updated` | Cash drawer shifts → Cash Chirps (C-101 to C-104) |
| `cash_drawer.event.created` | Cash drawer events → No-sale, paid-out Chirps |
| `labor.shift.created`, `labor.shift.updated` | Timecards → Timecard Chirps (C-301 to C-303) |
| `gift_card.activity.created` | Gift card activity → Gift Card Chirps (C-601 to C-602) |
| `inventory.count.updated` | Inventory adjustments → future Chirps |

**Webhook URL:** `https://{canary_host}/webhooks/square`
**Verification:** HMAC-SHA256 signature validation (already implemented in `webhooks_wired.py`)

### Ingestion Pipeline (Existing — Verify & Harden)

The webhook router (`webhook_router.py`) already handles the full event routing:

```
Square Webhook → HMAC Verify → Idempotency Check → Parse → Store → Chirp Evaluate → Alert Write
```

**What exists:**
- HMAC-SHA256 signature verification ✅
- Idempotency via `IngestionLog` ✅
- Event routing by type (payment, refund, order, cash_drawer, labor, gift_card, inventory) ✅
- Dead letter queue for failed events ✅
- ChirpRuleEngine evaluation ✅
- Alert + AlertHistory persistence ✅

**What needs work:**
- OAuth token management (store, refresh, revoke)
- Webhook subscription registration with Square API
- Tunnel or public URL for Square to reach the dev server (ngrok or Cloudflare Tunnel)
- Token refresh cron job (Square tokens expire — need refresh before expiry)
- Rate limiting awareness (Square webhook delivery retries)
- Backfill: after OAuth, pull recent transaction history via Square API to seed the detection engine (so Chirps can fire on Day 1, not Day 2)

### Backfill on Connect

When a merchant first connects, Canary should pull the last 7 days of transaction data via Square's Payments API, Orders API, and Cash Drawer API. This lets the detection engine evaluate historical data immediately, so the merchant sees Chirps on their first visit to Today's View — not 24 hours later after enough webhooks accumulate.

**Backfill sequence:**
1. OAuth completes → tokens stored
2. Pull last 7 days: payments, refunds, orders, cash drawer shifts, timecards
3. Store in `canary_sales` (same tables as webhook pipeline)
4. Run `ChirpRuleEngine.evaluate_batch()` across all backfilled data
5. Merchant opens Today's View → sees real Chirps from their actual last week

---

## Requirements

### Must-Have (P0)

| # | Requirement | Acceptance Criteria |
|---|---|---|
| P0-1 | Chirp Config page renders all 26 rules grouped by category | Page loads at `/companion/chirps/config`, shows 8 categories, 26 toggles, all default OFF |
| P0-2 | Toggle saves immediately and updates active count | Tapping a toggle calls PUT, header count updates, no page reload |
| P0-3 | Square OAuth flow completes and stores tokens | Merchant taps "Connect Square" → authorizes → callback stores access + refresh tokens |
| P0-4 | Webhook subscriptions registered after OAuth | All 8 event types registered with Square. Verification succeeds on first webhook delivery. |
| P0-5 | Live webhooks flow through existing pipeline | Square event → HMAC verify → parse → store in `canary_sales` → Chirp evaluate → alert write |
| P0-6 | Backfill pulls 7 days of history on connect | After OAuth, historical transactions pulled and evaluated. Chirps appear on first Today's View load. |
| P0-7 | Config page accessible from Today's View | Navigation link or button from Today's View to Chirp Config (and back) |

### Nice-to-Have (P1)

| # | Requirement | Acceptance Criteria |
|---|---|---|
| P1-1 | Category sections collapsible | Tap category header to expand/collapse. All expanded by default. |
| P1-2 | "Turn all on" / "Turn all off" per category | Category-level toggle in section header |
| P1-3 | Webhook event log visible to developer | `/admin/webhooks/log` shows last 100 events with parse status |
| P1-4 | Connection status indicator on Config page | Shows "Connected to Square" with green dot, or "Not connected" with connect button |
| P1-5 | Webhook replay for development | Jeremy can replay a captured webhook JSON against the pipeline locally |

### Future Considerations (P2)

| # | Requirement | Notes |
|---|---|---|
| P2-1 | Threshold sliders beneath each toggle | Merchant adjusts sensitivity per Chirp (ThresholdManager already supports this) |
| P2-2 | Per-location Chirp config | Different rules per store location |
| P2-3 | Push notifications (SMS, email) | E1-F13, Sprint 3+ |
| P2-4 | Chirp scheduling (business hours only) | Don't fire alerts outside merchant's operating hours |
| P2-5 | Chirp analytics (which rules fire most, false positive rate) | Feeds into threshold auto-tuning |

---

## Success Metrics

### Leading Indicators (change within days)

- **Phase 1 gate: GrowDirect Lab Chirp fires** — Jeffe shorts his own cash drawer, C-102 fires in Today's View within minutes
- **Phase 1 gate: Full pipeline traced** — Jeremy can show webhook → parse → store → evaluate → alert → render for a single event
- **Phase 2 gate: Merchant OAuth completes** — Friendly merchant's Square account connected, tokens stored, webhooks registered
- **Phase 2 gate: First real merchant Chirp** — a detection rule triggers on actual merchant transaction data within 1 hour of connect (via backfill)
- **Phase 2 gate: Merchant "aha" moment** — merchant sees a Chirp from their own data and says something like "I didn't know that was happening"
- **Config page interaction** — merchant scrolls the full list, toggles at least 3 Chirps on, understands what each one does without explanation

### Lagging Indicators (change over weeks)

- **False positive rate < 30%** — of Chirps that fire on real data, fewer than 30% are dismissed as irrelevant by the merchant
- **Merchant returns to Today's View 3+ times in first week** — indicates the alerts are useful enough to check
- **Zero webhook ingestion failures** — no events lost in the pipeline (dead letter queue empty)
- **Backfill-to-first-Chirp time < 1 hour** — from OAuth complete to first alert appearing in Today's View

---

## Open Questions

| # | Question | Who Answers |
|---|---|---|
| Q-1 | Do we need a public URL for Square webhooks during the sandbox phase, or can we use ngrok/Cloudflare Tunnel? | **Jeremy** — ngrok is fine for sandbox. Production needs a real endpoint. |
| Q-2 | Should the merchant see which Chirps have never fired vs. which have fired recently? (e.g., "Last triggered: 2 days ago") | **Jeffe** — nice for validation, could clutter the config page |
| Q-3 | Does Offset Coffee use gift cards or loyalty? If not, those categories might confuse during onboarding. | **Jeffe** — verify during Thursday recon |
| Q-4 | Square sandbox vs. production credentials for initial development? | **Jeremy** — GrowDirect Lab merchant account IS the dev sandbox. Real data, controlled by us. Square Sandbox (fake data) useful for unit tests only. |
| Q-5 | Does the "Connect Square" button live on the Config page, or is it a separate onboarding screen? | **Art** — UX decision. Recommendation: separate onboarding screen for first connect, status indicator on Config page after. |
| Q-6 | Provisional patent filing status for the detection rule architecture before exposing rule names to a merchant? | **Syd** — flagged in TRIAGE. Must clear before merchant sees rule list. |

---

## Timeline Considerations

### Phase 1 — GrowDirect Lab (Sprint 6 Week 1)

| Milestone | Target | Owner | Dependency |
|---|---|---|---|
| Jeffe creates Square Developer + Merchant accounts | Day 1 | Jeffe | None — 15 min task |
| Jeremy wires OAuth flow against GrowDirect Lab | Day 1-2 | Jeremy | Square app credentials from Jeffe |
| Webhook subscriptions registered + ngrok tunnel live | Day 2 | Jeremy | OAuth working |
| Chirp Config page UI (React) | Day 2-3 | Jeremy | Art v1.1 design language |
| Jeffe generates test transactions via Square POS/Virtual Terminal | Day 3 | Jeffe | Webhook pipeline live |
| First real Chirp fires on GrowDirect Lab data | Day 3 | All | Full pipeline verified |
| Backfill pulls 7 days of GrowDirect Lab history | Day 3-4 | Jeremy | OAuth + Payments API |
| Jim dry-runs onboarding flow as "test merchant" | Day 4-5 | Jim | Everything above working |

### Phase 2 — Friendly Merchant (Sprint 6 Week 2)

| Milestone | Target | Owner | Dependency |
|---|---|---|---|
| Jeffe recon at Offset Coffee (or identifies referral) | Week 2 Day 1 | Jeffe | Phase 1 complete |
| Merchant signs NDA + Beta Tester Agreement | Before OAuth | Jeffe + Syd | Syd merchant pack ready ✅ |
| Merchant OAuth connected — live data flowing | Week 2 Day 2 | Jeffe onsite | Onboarding script tested in Phase 1 |
| Backfill + first real Chirps on merchant data | Week 2 Day 2 | Automatic | Backfill pipeline |
| Jeffe + merchant validate Chirps together | Week 2 Day 2-3 | Jeffe | Chirps firing on real data |
| Syd confirms provisional patent status | Before merchant sees rule names | Syd | Flagged in TRIAGE |

### Phase 3 — Blitz (Jeffe trigger — after Phase 2 validates)

| Milestone | Target | Owner | Dependency |
|---|---|---|---|
| Worm silent prep (GBP, landing pages, content) | During Phases 1-2 | Worm + Will | Brand Guide, screenshots from Phase 2 |
| Square Marketplace listing draft | During Phase 2 | Condor + PhD + Syd | IP sanitized, legal reviewed |
| Jeffe gives go signal | TBD | Jeffe | Phase 2 success gate met |
| All channels go live simultaneously | Launch day | Worm + Will + Art | Everything above |

---

## Routing

| Agent | Action |
|---|---|
| **Jeffe** | Review this PRD. Validate merchant-facing Chirp names and descriptions — do these make sense to a coffee shop owner? Verify during Offset recon which categories are relevant. |
| **Jeremy** | Estimate effort. The webhook pipeline exists — main new work is OAuth, webhook subscription registration, backfill, and the React config page. |
| **Art** | Design the Chirp Config page. Follow the scrollable list pattern. Match Art v1.1 design language (severity colors, typography, spacing). |
| **Jim** | Write QA scenarios for the config page (toggle on/off, verify Chirp fires, verify Chirp stops). Add to Level B test plan. |
| **Syd** | Confirm provisional patent status before rule names are exposed to merchants. Review OAuth token storage for DPA compliance. |
| **Tom** | Validate API contract shapes. Confirm `merchant_rule_config` table can support the toggle endpoint without schema changes. |
| **PhD** | Review merchant-facing Chirp names for IP safety. Do the names reveal detection methodology? (They shouldn't — they describe what's watched, not how.) |

---

## Reference Files

| Document | Location |
|---|---|
| Rule definitions (26 rules) | `Canary/canary/services/chirp/rule_definitions.py` |
| Rule engine | `Canary/canary/services/chirp/rule_engine.py` |
| Threshold manager | `Canary/canary/services/chirp/threshold_manager.py` |
| Webhook router | `Canary/canary/services/webhook_router.py` |
| Webhook blueprint | `Canary/canary/blueprints/webhooks_wired.py` |
| Chirp API blueprint | `Canary/canary/blueprints/chirp_wired.py` |
| Companion service | `Canary/canary/services/companion_service.py` |
| Companion blueprint | `Canary/canary/blueprints/companion_wired.py` |
| CRDM v1.0 | `Canary_IP/Markdown/Specs/Canary_CRDM_v1.0.md` |
| Art wireframe v1.1 | `_ALX/WorkOrders/output/Art/TodaysView_Wireframe_v1.1.html` |
| Art self-critique v1.1 | `_ALX/WorkOrders/output/Art/TodaysView_SelfCritique_v1.1.md` |
| PhD alignment brief | `_ALX/WorkOrders/output/PhD/PhD_Alignment_Brief.md` |
| Syd merchant pack | `_ALX/WorkOrders/output/Syd/branded/` |

---

*Canary LP | GrowDirect | Confidential*
*ALX (Chief of Staff) | February 26, 2026*
*PRD E1-F14 v1.0 — DRAFT*
