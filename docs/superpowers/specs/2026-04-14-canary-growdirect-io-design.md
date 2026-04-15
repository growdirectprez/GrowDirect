# canary.growdirect.io — Design Spec

**Date:** 2026-04-14
**Type:** Landing page design spec
**Status:** Draft
**Location:** `Canary/static/landing/index.html` (served at canary.growdirect.io)
**Sources:** GrowDirect Manifesto v1.2, Canary Blue Ocean Strategy Analysis, Platform Overview SDD

---

## What This Page Is

canary.growdirect.io is a partnership recruiting page — not a SaaS product page. It exists to attract two audiences:

1. **A merchant partner** — a Square merchant willing to be the first live deployment. Someone who connects their real account, provides real transaction data, and helps build the product in a collaborative, low-pressure environment. They get the platform first and help shape it.

2. **A team/service partner** — an individual or firm that wants to work in the retail LP / data integrity space. Could be a developer, a consulting shop, a service firm. The page demonstrates that real capability has been built, there's a coherent vision, and there's room to participate.

This is the Canary-specific version of what growdirect.io does for the GrowDirect portfolio: a capability showcase and a partnership invitation.

---

## Positioning: The Canary in the Data Mine

"The Canary in the Data Mine" is the brand concept. It's catchy, the bird logo is distinctive, and the metaphor is immediately understood. That's where the cleverness ends. Everything else on the page is plain, direct, and specific about what the platform does and who built it.

The page conveys three things:

1. **What Canary does.** It connects to a Square merchant's account, reads their transaction data in real time, and identifies patterns that indicate money is being lost — voids, refunds, discount abuse, off-hours activity. It sends a weekly report with a dollar figure and plain-language explanation. That's the product.

2. **Why it's credible.** 30 years of enterprise retail systems — IBM 4690, national chains, high-volume production environments. Big 5 consulting process and support capability, applied to the SMB market. Not a startup guessing at retail.

3. **What we're looking for.** A merchant partner willing to connect real data and help build the product. Or a team/service partner who wants to work in this space.

---

## Blue Ocean Application

The Blue Ocean analysis identified the core strategic moves. Here's how they map to this page:

### ELIMINATE from the page
- **"Loss prevention" terminology** — the words "loss prevention," "shrink," "asset protection" never appear in the merchant-facing surface. These are enterprise red-ocean terms that signal "this is not for you." The partner section can use them because that audience understands the domain.
- **Feature counts and rule lists** — "29 detection rules across 8 categories" is an arms race metric. The page doesn't sell rule counts. It sells what the canary finds.
- **Dashboard screenshots** — no one is buying a dashboard. The product is the insight, not the interface.
- **SaaS pricing tiers** — this is a partnership page, not a checkout flow.

### REDUCE on the page
- **Technical architecture detail** — present at depth only in the layered reveal (the deep sections). The surface tells the story in human terms.
- **AI/ML language** — "AI-powered" is meaningless now. Don't say it. Show what the system finds. Let the intelligence be implicit.

### RAISE on the page
- **The "money found" framing** — Blue Ocean says this is the only metric that matters. The page's proof point is the weekly report mock: one number, one explanation, one action. This is what the merchant partner will actually experience.
- **The founder's credibility** — not "30 years experience" as a resume line. The actual story: the tLog problem, the LaneHawk incident, the human cost of mutable records. This is what no competitor can replicate.
- **The mission** — "come build this with me" energy. This is an invitation to participate in something being created, not a pitch to buy something that exists.

### CREATE on the page
- **The "canary in the data mine" narrative** — this doesn't exist anywhere else. No competitor has this story, this metaphor, or this origin. It's the category-creating move expressed as brand.
- **The layered reveal** — a page structure that rewards curiosity. Surface: what the canary does. Middle: how it works and why it's different. Deep: the tLog-to-gLog thesis, Bitcoin anchoring, the full vision. Each layer earns the next.
- **Partnership as the CTA** — not "sign up" or "buy now." "Let's build this together." Two paths: merchant partner (bring your data) or team partner (bring your skills).

---

## Visual Identity

- **Dark theme** — near-black (#0D1117) background, gold (#FBBF24) accent. Own identity, distinct from growdirect.io's light theme.
- **The canary bird** — prominent in the hero. Animated (gentle bob). The brand mark. The contrast between playful bird and serious capability is intentional and distinctive.
- **Typography** — Space Grotesk throughout. The manifesto's voice is direct, specific, and unafraid of long sentences when the thought requires it. The page should feel written, not designed-by-committee.
- **Green accent for partner section** — shifts from gold to green (#059669) to signal the transition from "what the canary does" to "come work with us."

---

## Page Structure

### Layer 1 — The Hook (above the fold)

**Nav:** Canary bird logo + wordmark | How It Works | Background | Partner With Us

**Hero:**
- Animated canary bird (gold, with glow)
- Headline: "The Canary in the Data Mine"
- Subhead: "Transaction monitoring for Square merchants. Connect your account. Get a weekly report showing exactly where you're losing money."
- Two CTAs: "See How It Works" (scrolls to proof) and "Partner With Us" (scrolls to partner section)
- Trust line: "Built on Square APIs · Read-only access · Your data stays yours"

### Layer 2 — The Proof (what the canary finds)

**The Weekly Report Mock** — the single most important element on the page. This is the product. Not a feature preview — this is what the merchant partner will actually receive.

- Mock weekly report card (dark surface, gold accent, shadow glow)
- One dollar figure: "$437 in potential losses found this week"
- Plain-English explanation of the biggest driver
- One recommended action
- The report sells itself. No feature list needed around it.

**What Canary flags** — 3-4 concrete examples in plain language:
- A voided sale 3 minutes after the customer left
- A $300 payment processed at 2 AM — you close at 10
- One employee's discount rate is 5x the store average
- Refunds filed faster than a real return takes

No category labels, no rule names. Specific things the system catches.

### Layer 3 — The Credentials (who built this)

Short, factual. No narrative arc, no origin story. State the background, state the capability.

- **Enterprise retail background** — 30 years. IBM 4690 POS systems, national chains, high-volume production environments. Transaction processing at scale.
- **Big 5 process capability** — Enterprise-grade methodology and support practices, applied to the SMB market through automation.
- **Data integrity commitment** — "If we flag something, we have the evidence. Every finding is backed by immutable, timestamped records."

This section exists so the reader understands this isn't someone's weekend project. Three short blocks, no storytelling.

### Layer 4 — The Platform (what's actually been built)

For the reader who wants to understand the engine. Technical but accessible.

- **How Canary works** — Connect Square → transactions flow in real-time via webhooks → detection engine evaluates every event → patterns surface as plain-language insights → evidence sealed and timestamped
- **Architecture cards** (brief, not exhaustive):
  - Real-time Square webhook ingestion with HMAC verification
  - Detection engine with configurable rules per merchant
  - Immutable evidence store — INSERT-only, hash-chained, trigger-enforced
  - Case management with court-ready documentation
  - AI analysis layer (Ollama) for pattern narrative
- **Stack tags:** Python · Flask · PostgreSQL · Square SDK · Docker

### Layer 5 — The Vision (the deep reveal)

For the reader who scrolls this far. Technical substance, no pitch language.

**The tLog problem:**
- IBM created the transaction log in 1986. Every POS system since uses the same model: a mutable record on a server someone controls. The log can be edited. It happens.
- Canary's evidence store is different. INSERT-only. Hash-chained. Merkle roots anchored to Bitcoin. Records can't be altered after the fact.

**The gLog:**
- Canary is building the successor to the tLog — an immutable transaction record that works from one receipt to one billion.
- Not blockchain for its own sake. A direct fix for a specific problem in how retail transactions have been recorded for 40 years.

**Open source:**
- The detection logic, evidence storage, and data handling will be public. Transparency is the standard. Execution is the differentiator.

### Layer 6 — The Partnership (the ask)

Green accent transition. Shift from capability showcase to contact.

Two paths:

**Path A — Merchant Partner**
- Copy states what we need: a Square merchant willing to connect their account, work with real data, and help refine the product. Any size operation. Read-only access. No commitment beyond trying it.
- CTA: Contact form — name, email, business name, number of locations, message. Hidden `_source: merchant-partner` field. Formspree submission.

**Path B — Team / Service Partner**
- Copy states what we're building: enterprise-level retail tooling delivered to the SMB market. Looking for people or firms who want to work in this space — development, consulting, or service delivery.
- CTA: Contact form (same form, different pre-filled source) + Calendly booking link (external link, not embed). Calendly URL TBD; fallback to form-only if not set up.
- Hidden `_source: team-partner` field.

**Both paths converge on the same form** — differentiated by copy and a hidden field, like the growdirect.io `?from=` pattern.

### Footer
- Canary by GrowDirect
- gclyle@growdirect.io
- Link back to growdirect.io

---

## Technical Implementation

### Hosting
The page lives at `Canary/static/landing/index.html` within the Canary Flask app. Two serving options:

**Option A — Flask serves it directly.** Add a route that checks the `Host` header: if `canary.growdirect.io`, serve the landing page. If the app's primary domain, serve the authenticated dashboard. Nginx passes all traffic to Flask; Flask handles the routing.

**Option B — Nginx routes by subdomain.** Separate `server` block for `canary.growdirect.io` that serves static files from `Canary/static/landing/` directly, bypassing Flask entirely. Faster, simpler, no app changes needed.

**Recommendation: Option B** for launch. Static HTML doesn't need Flask. Nginx serves it faster. When the landing page needs dynamic features (e.g., real OAuth flow for merchant partners), switch to Option A.

### DNS
- Add CNAME record: `canary` → wherever the Canary app is hosted
- Or if using a separate static host (GitHub Pages, Vercel): CNAME to that target

### Form Handling
- Formspree for launch (same account as growdirect.io, new form endpoint)
- Hidden `_source` field for partner type attribution
- AJAX submission with success state, mailto fallback on error

### Analytics
- GA4 tag: same property as growdirect.io (`G-ELPTR2ZLP3`) — keeps all GrowDirect traffic in one view, filterable by hostname
- Custom events:
  - `partner_form_submit` — with `source` param (merchant-partner / team-partner)
  - `section_scroll` — fires once per section via Intersection Observer (50% threshold) on Layers 2-6. Tracks how deep people read.
  - `calendly_click` — fires when team partner Calendly link is clicked

### Static Assets
- Single HTML file with embedded CSS (like the sample — no build step)
- Google Fonts: Space Grotesk
- Inline SVG for the canary bird and any icons
- No external JS dependencies

### SEO
- Title: "Canary — The Canary in the Data Mine"
- Meta description: focused on the partnership angle, not SaaS conversion
- `robots.txt` allowing indexing
- Canonical: `https://canary.growdirect.io/`
- OG/Twitter meta for link previews

---

## Content Principles

1. **State facts.** Say what the system does. Say what background built it. Say what you're looking for. No inspirational copy, no storytelling arcs, no "imagine if" framing.

2. **Show the product.** The weekly report mock is the centerpiece. The detection examples are concrete. The architecture section lists what's built. Everything is evidence, not promise.

3. **The brand does the personality.** "The Canary in the Data Mine" is the catchy part. The bird logo is the visual hook. Everything else is straight.

4. **No LP jargon in the first 3 layers.** "Loss prevention," "shrink," "asset protection" appear only in Layer 4+ where the audience knows the domain.

5. **Credibility = enterprise background + working software.** Real-world enterprise-level tooling, process, and delivery experience. That's the differentiator. Not a story about why it was built — just proof that someone serious built it.

---

## Responsive & Mobile

- **Breakpoints:** 768px (tablet), 480px (mobile). Single-column below 768px.
- **Weekly report mock:** Full-width card on mobile, max-width 480px centered on desktop.
- **Partner section:** Two-path layout stacks vertically on mobile (merchant first, then team).
- **Nav:** Collapses to hamburger below 768px. "Partner With Us" stays visible as a CTA button even in collapsed state.
- **Canary bird animation:** Scales down to ~80px on mobile. Reduce glow intensity to avoid performance issues on low-end devices.
- **Architecture cards (Layer 4):** Stack single-column on mobile.
- **Touch targets:** All CTAs and form inputs minimum 44px hit area.

---

## Canary Bird Animation

- **Source:** Inline SVG (no external image files). Gold fill (#FBBF24) with soft radial glow (CSS box-shadow or SVG filter).
- **Animation:** Gentle vertical bob — CSS `@keyframes` with `translateY(-4px)` over 3s, `ease-in-out`, infinite. No JavaScript animation libraries.
- **Reduced motion:** Wrap in `@media (prefers-reduced-motion: no-preference)`. Static bird with glow is the fallback.
- **Size:** ~120px wide in the hero on desktop. SVG scales naturally.
- **Reference:** The existing sample at `Canary/static/landing/index.html` has a working canary SVG with animation. Use that as the starting point and refine.

---

## Accessibility

- **Color contrast:** Gold (#FBBF24) on near-black (#0D1117) passes WCAG AA for large text (18px+). For body text, use white (#E6EDF3) on the dark background; reserve gold for headings, accents, and the bird.
- **Semantic HTML:** Use `<nav>`, `<main>`, `<section>`, `<footer>`. Each layer is a `<section>` with an `aria-label`.
- **Focus management:** Visible focus rings on all interactive elements. Skip-to-content link.
- **Form labels:** All form inputs have associated `<label>` elements.
- **Font loading:** `font-display: swap` on Google Fonts import to prevent invisible text during load.

---

## What This Page Is Not

- Not a SaaS product page with pricing tiers
- Not a "sign up for a free trial" funnel
- Not a technical documentation site
- Not a pitch deck converted to HTML
- Not competing on feature counts or rule lists

It shows what the platform does, states the background behind it, and provides a way to get in touch.
