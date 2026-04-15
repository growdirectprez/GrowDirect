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

The page is built on the manifesto's core metaphor, not the Blue Ocean's "Profit Guardian" label. "Profit Guardian" is a category name for the market — useful for positioning but too clinical for a page that needs to recruit believers.

The narrative is:

> The canary goes into the mine before the miners do. It detects what humans can't see, smell, or feel — the invisible gas that kills silently. When the canary sings, you act. When it stops singing, you run.
>
> Your transaction data is a mine. Shrink, fraud, and operational loss are the gas — invisible, odorless, accumulating. Every POS system in production today records what happened in a mutable log that can be edited, disputed, or silently forgotten. The record is only as trustworthy as the institution that holds it.
>
> Canary goes into that mine. It reads every transaction. It detects patterns that no human review would catch. And when it finds something, it tells you — in plain language, with evidence that can't be altered.
>
> This platform was built by someone who spent 30 years inside the mine — enterprise retail systems, IBM 4690, national chains — and saw what happens when the data is wrong and the record can't be trusted. Canary exists because of what the old systems couldn't do.

This is the emotional and intellectual spine of the page. Everything hangs off it.

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

**Nav:** Canary bird logo + wordmark | How It Works | The Story | Partner With Us

**Hero:**
- Animated canary bird (gold, with glow)
- Headline candidates (pick one during implementation):
  - "The Canary in the Data Mine"
  - "Something in your data is trying to tell you something."
  - "Every transaction tells a story. Most of them go unread."
- One-line subhead: "Canary reads every transaction your Square system records — and tells you what it finds."
- Two CTAs: "See What Canary Finds" (scrolls to proof) and "Partner With Us" (scrolls to partner section)
- Trust line: "Built on Square APIs · Read-only · Your data stays yours"

### Layer 2 — The Proof (what the canary finds)

**The Weekly Report Mock** — the single most important element on the page. This is the product. Not a feature preview — this is what the merchant partner will actually receive.

- Mock weekly report card (dark surface, gold accent, shadow glow)
- One dollar figure: "$437 in potential losses found this week"
- Plain-English explanation of the biggest driver
- One recommended action
- The report sells itself. No feature list needed around it.

**"Patterns you'd never spot"** — 3-4 real detection scenarios described in merchant language (not LP language):
- A sale that disappears 3 minutes after the customer leaves
- A $300 payment processed at 2 AM when you close at 10
- One employee's discount rate is 5x everyone else's
- Refunds filed faster than a real customer interaction allows

No category labels, no severity tiers, no rule names. Just "here's what we'd find in your data."

### Layer 3 — The Story (why this exists)

This is where the page earns depth. The people still reading past the proof are the ones worth talking to.

**"Why we built this"** — The canary in the data mine narrative, told in 3 beats:

1. **The mine** — Every POS system records what happened in a log that can be edited. The record is only as trustworthy as the institution that holds it. Square merchants are flying blind in a mine full of gas they can't smell.

2. **The incident** — A loss prevention system accused an employee of fraud. The employee was innocent. The data was wrong. The data couldn't be cross-examined because the institution controlled the record. (The LaneHawk story, told without naming LaneHawk — the point is the principle, not the brand.)

3. **The canary** — 30 years of watching this problem. Enterprise retail systems, national chains, billions of transactions. Waiting for the tools that would make the solution possible. Not a startup guessing at retail. This is the thing that was always going to get built.

**Data Integrity Principle callout:**
> "We treat data integrity with the utmost seriousness. This is people's lives and jobs we are analyzing. If we accuse someone, we have to be sure and have the facts."

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

This is the manifesto layer. Only the most engaged readers reach it. It rewards them.

**"The deeper problem"** — The tLog thesis in accessible language:
- IBM invented the transaction log in 1986. Every POS system since inherits the same flaw: the record is mutable. Someone controls the server. Someone can change the log.
- This isn't a hypothetical risk. It's the mechanism behind every disputed LP accusation, every contested insurance claim, every employment dispute where "the system says" is the only evidence.
- AI makes it worse. Synthetic documents, fabricated receipts, generated audit trails. The mutable record can't survive a world where anyone can generate a convincing counterfeit.

**"The gLog"** — What Canary is actually building underneath:
- Every event hashed on receipt. Hash chains link every record to the one before it. Merkle roots anchored to Bitcoin. The record exists. The record cannot be argued with.
- Not "blockchain for blockchain's sake." The direct successor to the IBM tLog, built because the old foundation was broken and the tools to fix it finally exist.
- From one receipt to one billion receipts: same architecture, different scaling.

**Open source commitment:**
> Transparency is the brand. Expertise and execution are the moat. The code will be public. Anyone can inspect how Canary detects, how it stores evidence, and how it protects data.

### Layer 6 — The Partnership (the ask)

Green accent transition. Different energy — from "here's what we built" to "here's what we're building next, and there's a seat."

**"Come build this with me"**

Two paths:

**Path A — Merchant Partner**
- "You run a Square operation. 1 location or 50. You know something's off in the numbers but you can't see it. Connect your account. Let the canary into the mine. You get the platform before anyone else, you help shape what it becomes, and you see exactly where your money is going."
- CTA: Contact form — name, email, business name, number of locations, message. Hidden `_source: merchant-partner` field. Formspree submission.
- Tone: collaborative, low-pressure, "let's work together"

**Path B — Team / Service Partner**
- "You work in retail technology, data, consulting, or loss prevention. You see what's happening in this space and you want in. Whether you're an individual contributor or a firm — if you want to build in this category, let's talk."
- CTA: Contact form (same form, different pre-filled source) + Calendly booking link (external link, not embed — keeps page lightweight). Calendly URL TBD; fallback to form-only if not set up.
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

1. **Written, not copywritten.** The manifesto's voice is direct, specific, and unafraid of substance. The page should read like it was written by the person who built the thing — because it was. No "unlock the power of" or "revolutionary platform."

2. **Show the work.** The weekly report mock, the detection scenarios, the architecture description — these are proof that something real has been built. Not a pitch deck. A portfolio piece with a pulse.

3. **Reward depth.** The surface layer is accessible to anyone. Each scroll deeper reveals more substance. The people who read the tLog-to-gLog section are exactly the people you want to hear from.

4. **No LP jargon in the first 3 layers.** "Loss prevention," "shrink," "asset protection" — these words appear only in Layer 4+ where the audience is self-selected as domain-aware.

5. **The canary metaphor does the heavy lifting.** Don't over-explain it. The bird in the hero. "The canary in the data mine" as a section title or motif. Let people make the connection. The ones who get it are the ones you want.

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

It's the digital equivalent of sitting down with someone and saying: "Let me tell you what I've been building and why. And let me show you what it finds when you point it at real data. If that interests you, let's talk."
