# Angel × Luxury Presence — Integration Spec

> **Status:** Proposed — spec for review, not yet built
> **Namespace:** angel
> **Date:** 2026-04-06
> **Author:** ALX (COO) / Jeffe (CEO)
> **Dependencies:** Angel data platform, Angel agent, web-strategy.md
> **Prototype reference:** `ownpalosverdes_v2.html`

---

## 1. What This Spec Covers

This document specifies how AngeliqueLyle.com (hosted on Luxury Presence)
connects to the GrowDirect Angel backend. It covers three things:

1. **LP Website Build** — what gets built in LP's CMS to match the prototype
2. **Lead Pipeline** — how form submissions flow from LP → Angel → Angelique
3. **Integration Points** — every webhook, script injection, and CRM bridge

It does NOT cover TheHillPV.com (Flask stack) or the Angel chat widget
(separate spec). Those are documented in `web-strategy.md` and
`angel-agent.md`.

---

## 2. Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                  LUXURY PRESENCE (LP)                         │
│                                                              │
│  CMS Pages ──→ LP IDX Feed ──→ LP Lead CRM                  │
│  (our content)   (MLS data)     (safety net)                 │
│       │                              │                       │
│       │         Global Scripts       │                       │
│       │         ┌──────────┐         │                       │
│       │         │ Head CSS │         │                       │
│       │         │ Body JS  │         │                       │
│       │         └────┬─────┘         │                       │
│       │              │               │                       │
│       ▼              ▼               ▼                       │
│  Rendered Page + Design Overrides + Form Handler             │
└──────────────────────┬───────────────────────────────────────┘
                       │
            POST /api/webhooks/lp
            (HMAC-SHA256 signed)
                       │
┌──────────────────────▼───────────────────────────────────────┐
│                  ANGEL BACKEND (Flask :5004)                  │
│                                                              │
│  Webhook Receiver ──→ Lead Model ──→ Pipeline                │
│  (verify, normalize)   (Postgres)     (enrich, notify)       │
│                                                              │
│  Future: Angel Chat Widget JS served from here               │
└──────────────────────────────────────────────────────────────┘
```

**Key principle:** LP is the CRM safety net. Every form submission goes to
LP's built-in CRM first. The webhook bridge to Angel is additive — if Angel
goes down, LP still has the lead. We never intercept or block LP's native
form handling.

---

## 3. LP Website Build Plan

### 3.1 Create New Website

Create a **new** website in LP's dashboard (not edit the existing staging or
production sites). This gives us a clean slate without Sotheby's branding
artifacts.

- **Website name:** "Angelique Lyle — Palos Verdes"
- **Template:** Start from LP's most minimal/blank template
- **Domain:** Will be assigned `angeliquelyle.com` once ready to go live
- **Build approach:** Use LP's CMS page builder for structure, Global Scripts
  for design refinement only (fonts, colors, spacing — not structural HTML)

### 3.2 Section-by-Section Build Map

Each prototype section maps to an LP CMS section type. LP's page builder
offers section types like Hero, About, Grid, Contact, etc. Where LP's native
sections can't match the prototype, we note what Global Scripts CSS must
handle.

| # | Prototype Section | LP Section Type | CSS Override Needed | Notes |
|---|-------------------|-----------------|---------------------|-------|
| 01 | Navigation | LP built-in nav | Yes — fonts, colors, sizing | Logo text "Angelique *Lyle*", 7 nav links, "Let's Connect" CTA button |
| 02 | Hero | Hero section | Yes — split-grid layout, stats overlay | Left: black bg with copy + 2 CTAs. Right: coastal image + 4 stat boxes |
| 03 | History Seam | Custom HTML section | Full custom | CSS marquee animation, 72px strip, neighborhood names |
| 04 | About | About/Bio section | Moderate — photo badge, signature | Photo with "20+" badge overlay, 3 paragraphs bio, DRE signature block |
| 05 | Neighborhoods | Grid/Cards section | Yes — card styling, overlay text | 6 neighborhood cards with images, tags, median prices |
| 06 | Featured Listings | LP IDX widget | Minimal — card styling | LP's native listing display, 3 featured properties |
| 07 | Welcome Guide | Custom HTML + Form | Moderate — chapter list, form card | Left: 4 chapter previews. Right: form (name, email, dropdown) |
| 08 | History | Content section | Moderate — photo grid, link | B&W photos + narrative copy + external link |
| 09 | Testimonials | Testimonials section | Yes — card grid layout | 4 testimonial cards with quotes, names, stars |
| 10 | Contact | Contact section + Form | Yes — split dark/light | Left: dark bg with contact details. Right: light bg with full form |
| 11 | Footer | LP built-in footer | Yes — 4-column layout | Company / Navigate / Resources / Connect columns |
| 12 | Modals | Global Scripts JS | Full custom | 4 modals: Connect, Home Worth, Listing Details, Thanks |

### 3.3 Global Scripts Injection (Design Layer Only)

The Global Scripts CSS/JS from `lp-injection/` remains useful but scoped to
**design refinement**, not structural override:

**Head CSS (style tags):**
- Font injection: DM Serif Display + DM Sans
- CSS custom properties: `--al-black`, `--al-heading`, `--al-body`, etc.
- Nav refinement: 68px height, blur backdrop, scroll shadow
- Button styles: `.btn-primary`, `.btn-ghost`, `.nav-cta`
- Section spacing and typography overrides
- Modal overlay and animation styles
- Scroll reveal animation classes

**Body JS (script tags):**
- Nav scroll shadow toggle
- IntersectionObserver scroll reveals
- Modal open/close system (keyboard + overlay click)
- Smooth scroll navigation
- History seam marquee animation
- Webhook bridge (fire-and-forget POST to Angel)
- Lazy image loading for below-fold content

### 3.4 Content That Must Be Entered in LP CMS

All copy lives in LP's CMS, not in injected code. This list is the minimum
content needed:

**Nav:** Logo text, 7 link labels, CTA button text
**Hero:** Eyebrow, headline, subhead, 2 button labels, 4 stat values
**About:** Section tag, heading, 3 paragraphs bio, signature block
**Neighborhoods:** 6 cards (image, tag line, name, median price)
**Listings:** LP's IDX widget handles this — configure featured listings
**Welcome Guide:** Section tag, heading, description, 4 chapters (title + desc), form card copy
**History:** Section tag, heading, 2 paragraphs, external link
**Testimonials:** 4 testimonials (quote, name, stars)
**Contact:** Section tag, heading, description, 4 contact details, form fields
**Footer:** 4 columns of links and text

---

## 4. Lead Pipeline

### 4.1 Form Inventory

The prototype has **4 distinct forms**, each generating a lead:

| Form | Location | Fields | Interest Type | Lead Priority |
|------|----------|--------|---------------|---------------|
| **Contact Form** | Section 10 (Contact) | first_name, last_name, email, phone, interest_select, message | varies by select | High |
| **Welcome Guide Form** | Section 07 (Welcome Guide) | name, email, interest_select | `welcome_guide` | Medium |
| **Let's Connect Modal** | Modal (from nav CTA) | name, email, message | `general` | High |
| **Home Worth Modal** | Modal (from hero CTA) | address, name, email | `selling` | High |

### 4.2 Form Submission Flow

```
Visitor fills form on AngeliqueLyle.com
         │
         ▼
┌─────────────────────────────────────────┐
│  LP Native Form Handler (runs first)    │
│  → Lead saved to LP CRM                │
│  → LP sends confirmation email          │
│  → LP triggers any LP automation rules  │
└─────────────────────┬───────────────────┘
                      │
         webhook (if configured in LP)
         — OR —
         JS bridge (body script captures submit event)
                      │
                      ▼
┌─────────────────────────────────────────┐
│  Angel Webhook Receiver                  │
│  POST /api/webhooks/lp                  │
│                                         │
│  1. Verify HMAC-SHA256 signature        │
│  2. Parse + normalize payload           │
│  3. Create Lead record (Postgres)       │
│  4. Return 200 OK                       │
└─────────────────────┬───────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────┐
│  Angel Lead Pipeline (async)            │
│                                         │
│  5. Enrich: match APN if address given  │
│  6. Classify: buyer/seller/relocator    │
│  7. Notify: SMS to Angelique            │
│  8. Track: update pipeline stage        │
└─────────────────────────────────────────┘
```

### 4.3 Webhook vs. JS Bridge — Decision

There are two ways to get form data from LP to Angel:

**Option A: LP Custom Webhook (preferred)**
- LP may support configuring a webhook URL in its CRM settings
- LP would POST lead data to our endpoint after its own processing
- HMAC signature verification for authenticity
- Pro: Clean separation, runs server-side, survives ad blockers
- Con: Requires LP to support custom webhooks (needs verification)

**Option B: JS Bridge (fallback)**
- Body JavaScript listens for form `submit` events
- Captures FormData, adds metadata, POSTs to Angel via `fetch()`
- Uses `keepalive: true` so the request survives page navigation
- Pro: Works without LP webhook support, we control it
- Con: Client-side, blocked by ad blockers, doesn't fire if JS fails

**Decision:** Implement both. The JS bridge is already built
(`angelique-behavior.js` → `initWebhookBridge()`). We investigate LP's
webhook support and configure it if available. Both feed the same endpoint.
Deduplication by `lp_lead_id` or email+timestamp prevents double-counting.

### 4.4 Webhook Payload Schema

The Angel webhook endpoint accepts this normalized payload:

```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "phone": "string | null",
  "interest_type": "buying | selling | relocating | welcome_guide | exploring | general",
  "message": "string | null",
  "address": "string | null",
  "page_url": "string",
  "referrer": "string",
  "source": "lp_form | lp_webhook | angel_chat",
  "timestamp": "ISO 8601",
  "lp_lead_id": "string | null"
}
```

The endpoint normalizes field name variations (e.g., `name` → split to
`first_name`/`last_name`, `phone_number` → `phone`, `source_url` →
`page_url`). This is already implemented in `angel/routes/webhooks.py`.

### 4.5 Lead Model

Existing model in `angel/models/lead.py` covers the needed fields. One
addition needed:

```python
# Add to Lead model
source: Mapped[str] = mapped_column(String(20), nullable=False, default="lp_form")
# Values: lp_form, lp_webhook, angel_chat, manual
```

This distinguishes leads from LP forms vs. the Angel chat widget vs. manual
entry. The `raw_payload` JSONB column stores the full original webhook data
for debugging and audit.

---

## 5. LP CRM Integration

### 5.1 What LP CRM Does Natively

LP's built-in CRM captures every form submission automatically:
- Lead record with name, email, phone, message
- Source page and timestamp
- Ability to tag, assign, and add notes
- Email notification to agent on new lead
- Basic drip email automation (if configured)

**We do NOT replace LP CRM.** It is the safety net. Angelique (or her team)
can always see leads directly in LP's dashboard without depending on Angel.

### 5.2 What Angel Adds on Top

Angel enriches the lead beyond what LP CRM provides:

| Capability | LP CRM | Angel |
|-----------|--------|-------|
| Lead capture | ✓ | ✓ (mirror) |
| Contact info storage | ✓ | ✓ |
| APN-level property data | ✗ | ✓ (match address → APN → full record) |
| Pipeline staging | Basic | Full (9 stages: identified → closed) |
| SMS notification | ✗ | ✓ (instant to Angelique) |
| AI-powered lead scoring | ✗ | ✓ (future: based on property + behavior) |
| Chat widget conversation | ✗ | ✓ (Angel agent with Angelique's voice) |
| Cross-site attribution | ✗ | ✓ (LP + TheHillPV + OwnPalosVerdes) |

### 5.3 Deduplication Strategy

A lead might arrive via both LP CRM webhook and JS bridge. We deduplicate:

1. **By `lp_lead_id`** — if LP assigns an internal ID, match on it
2. **By email + 5-minute window** — same email within 5 minutes = same lead
3. **By phone + 5-minute window** — fallback if email is blank
4. **Merge, don't discard** — if a duplicate arrives with additional fields
   (e.g., the webhook has `lp_lead_id` the JS bridge didn't), merge the data

---

## 6. LP Platform Capabilities to Investigate

Before building, we need to verify what LP Pro supports. These are the open
questions:

| # | Question | Why It Matters | How to Find Out |
|---|----------|----------------|-----------------|
| 1 | Does LP support custom webhook URLs for form submissions? | Option A vs Option B for lead pipeline | LP dashboard → Settings → Integrations |
| 2 | Can LP send HMAC-signed webhook payloads? | Security of webhook endpoint | LP API docs or support |
| 3 | What fields does LP include in its webhook payload? | Payload normalization mapping | Test with a form submission |
| 4 | Does LP allow `<script>` tags in custom HTML sections? | Modal system, Angel chat widget | Test in LP page editor |
| 5 | Can we embed external JS (chat widget) via Global Scripts? | Angel chat widget on AngeliqueLyle.com | Test in Global Scripts → Body |
| 6 | Does LP expose an API for lead data? | Pull leads from LP CRM into Angel | LP partner/developer docs |
| 7 | Can LP's IDX widget be styled with custom CSS? | Featured listings section design | Test with Global Scripts CSS |
| 8 | Does LP support custom form fields (beyond name/email/phone)? | Interest type dropdown, address field | LP form builder |
| 9 | What LP template gives the most minimal starting point? | Least amount of built-in branding to override | LP website creation flow |
| 10 | Can we use LP's built-in CMA (comparative market analysis) tool? | "What's My Home Worth" flow | LP dashboard features |

---

## 7. Angel Endpoints

### 7.1 Existing (built)

| Method | Path | Purpose | Auth |
|--------|------|---------|------|
| POST | `/api/webhooks/lp` | Receive LP form/webhook leads | HMAC-SHA256 |
| GET | `/api/webhooks/health` | Health check | None |

### 7.2 Needed (to build)

| Method | Path | Purpose | Auth |
|--------|------|---------|------|
| GET | `/api/leads` | List leads with filters | API key |
| GET | `/api/leads/<id>` | Single lead detail | API key |
| PATCH | `/api/leads/<id>` | Update lead stage/notes | API key |
| POST | `/api/leads/<id>/notify` | Trigger SMS to Angelique | API key |
| GET | `/api/stats/dashboard` | Lead pipeline summary | API key |
| POST | `/api/webhooks/lp/test` | Test webhook with sample payload | API key |

### 7.3 Future (Angel chat widget)

| Method | Path | Purpose | Auth |
|--------|------|---------|------|
| POST | `/api/chat/message` | Chat widget message handler | Session token |
| GET | `/api/chat/widget.js` | Serve embeddable chat widget | None (CORS) |
| GET | `/api/neighborhoods/<slug>` | Neighborhood data for chat | None |
| GET | `/api/schools/<district>` | School data for chat | None |

---

## 8. Environment & Config

### 8.1 Angel Flask Config Additions

```python
# .env additions for LP integration
LP_WEBHOOK_SECRET=<shared-secret-with-lp>    # HMAC key
LP_SITE_URL=https://angeliquelyle.com        # For CORS allowlist
TWILIO_SID=<sid>                              # SMS notifications
TWILIO_AUTH_TOKEN=<token>
TWILIO_FROM_NUMBER=+1310XXXXXXX
ANGELIQUE_PHONE=+13107518335                  # SMS destination
```

### 8.2 CORS Configuration

Angel's webhook endpoint must accept POST from:
- `https://angeliquelyle.com` (LP production)
- `https://*.luxurypresence.com` (LP staging/preview)

The JS bridge makes cross-origin `fetch()` calls, so CORS headers are
required. The webhook endpoint should return:

```
Access-Control-Allow-Origin: https://angeliquelyle.com
Access-Control-Allow-Methods: POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, X-Webhook-Signature
```

---

## 9. Build Sequence

This is the order of work, with dependencies shown:

### Phase 1: LP Website (CMS work, no code)
1. Create new LP website from blank template
2. Configure Global Scripts — inject CSS variables and fonts
3. Build homepage sections 01-11 using LP's CMS page builder
4. Enter all copy from the prototype blueprint
5. Configure LP's IDX widget for Featured Listings section
6. Test on LP preview domain

### Phase 2: Design Refinement (Global Scripts)
7. Inject override CSS for typography, spacing, colors
8. Inject behavior JS for modals, scroll reveals, seam animation
9. Visual QA against prototype — section by section comparison
10. Mobile responsive testing

### Phase 3: Lead Pipeline (code)
11. Verify LP webhook support (investigate question #1-3 from §6)
12. Configure LP webhook → Angel endpoint (if supported)
13. Enable JS bridge as fallback (flip `WEBHOOK_ENABLED = true`)
14. Test form submission → Angel lead creation → LP CRM capture
15. Implement deduplication logic
16. Add SMS notification via Twilio

### Phase 4: Go Live
17. Point `angeliquelyle.com` DNS to new LP website
18. Verify webhook endpoint is reachable from LP servers
19. Test all 4 forms end-to-end on production domain
20. Monitor LP CRM + Angel dashboard for first 48 hours

---

## 10. What We Are NOT Building (Scope Boundaries)

To keep this spec honest about scope:

- **Angel chat widget** — separate spec, separate build cycle
- **TheHillPV.com** — Flask stack, separate project
- **OwnPalosVerdes.com** — needs spam cleanup first, separate project
- **LP API integration** — only if LP offers one; not assumed
- **Automated email drip sequences** — LP CRM handles basic drip natively
- **Custom IDX search** — LP's built-in IDX is sufficient for now
- **Neighborhood sub-pages** — homepage only in this build; sub-pages are Phase 2

---

## 11. Open Decisions

| # | Decision | Options | Recommendation |
|---|----------|---------|----------------|
| 1 | Where does Angel run? | GrowDirect Docker stack vs. hosted | Docker stack (port 5004, consistent with platform) |
| 2 | SMS provider | Twilio vs. other | Twilio — proven, simple API |
| 3 | Welcome Guide delivery | Email attachment vs. hosted PDF link | Hosted PDF link (update quarterly without re-sending) |
| 4 | "What's My Home Worth" | Manual CMA vs. automated estimate | Manual — Angelique's differentiator is personal, not algorithmic |
| 5 | Neighborhood cards | Static content vs. data-driven | Static for launch, data-driven in Phase 2 via Angel data platform |

---

*Filed per GrowDirect doc standards: `docs/sdds/angel/lp-integration.md`*
*Prototype reference: `ownpalosverdes_v2.html` (1107 lines, 12 sections)*
*Existing code: `angel/models/lead.py`, `angel/routes/webhooks.py`, `lp-injection/`*
