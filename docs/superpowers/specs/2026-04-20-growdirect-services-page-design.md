# GrowDirect.io Services Page — Design Spec

**Date:** 2026-04-20
**Status:** Design — approved for planning
**Scope:** Replace the gated investor-portal homepage at growdirect.io with a public-facing "builder's shingle" services page. Move existing investor/thesis content behind `/portal`. Preserve `/canary`.

---

## Purpose

growdirect.io currently loads a password-gated investor portal pitching "immutable commerce infrastructure" built around Canary (Square loss-prevention + Bitcoin inscription). The public visitor sees an access-code prompt and nothing else.

That's the wrong front door for the operator's actual day-to-day business pitch. The operator (Greg Lyle, solo) wants the public homepage to function as a **honest builder's shingle** — personal, first-person, unpretentious, locally-grounded — that advertises three real service lanes:

1. **Products** that are already running (Cove for HOAs, Angel for Compass agents)
2. **Project work** with defined scope (permit/remodel navigation, custom builds)
3. **Day-rate small-business tech help** (file systems, bill scanning, tool setup, teach-to-fish)

Canary is deep-linked from the footer, not the front page. The investor/Bitcoin-thesis content is preserved but moved behind `/portal` with the existing access-code gate intact.

**Non-commercial driver:** the page also anchors a 2026 reskilling retrospective — a public "what I've built this year" section that doubles as CPA-facing documentation of professional-development activity for an active Schedule C trade.

---

## Relationship to Prior Specs

Two earlier specs touched this territory and are explicitly **superseded for the public homepage positioning**:

- `2026-04-14-growdirect-io-portfolio-site-design.md` — multi-page "three-pillar" portfolio site (POS / RE / Membership) pitched at Square Solutions Partner reviewers and implying team scaling. Wrong audience and wrong voice for the current positioning. Pillar structure informs this spec; surface pitch does not.
- `2026-04-15-growdirect-site-refresh-design.md` — consolidated content into a `site/` directory. Per current state (`reference_site_deployment.md`), the `site/` directory was removed; deploys happen directly from `~/growdirectprez.github.io/`. This spec aligns with the current-state deploy model, not the `site/` directory model.

The existing `/canary/` subpage and its content (streamlined single-page product pitch) are **preserved unchanged**.

---

## Target Audiences

Four audiences, ordered by expected traffic weight:

1. **Local small-business owners** (Palos Verdes Peninsula, South Bay) — reached primarily via Nextdoor, word of mouth, and wife's Compass agent network. Want: "a local person who can come help with the tech problem on my plate." Convert on: the day-rate section.
2. **Small luxury HOA boards** anywhere — reached via Cove case study distribution (CoAC / WPBCA), board-to-board referral, eventually directory/SEO. Want: "a member portal that doesn't look like 1998." Convert on: Cove product card.
3. **Compass agents outside the South Bay** — reached opportunistically when wife travels to other Compass offices for network-building. Want: "an ownpalosverdes.com-style site for my own book." Convert on: Angel product card.
4. **Remodel homeowners / builders / GCs** — reached via local SEO ("Rancho Palos Verdes permit help") and word of mouth. Want: "someone who knows the RPV planning department's quirks and can handle paperwork." Convert on: permit/remodel line item.

Explicitly **not targeted**:
- Square merchants looking for ongoing loss-prevention support (Canary is build-it-and-ship-it; no helpdesk)
- Enterprise real estate brokerages (wrong scale, wrong voice)
- VC / strategic investors (that audience reads `/portal`, not the front page)
- National SMB SaaS customers (scope is solo; volume caps at a level one person can support)

---

## Voice & Tone

First-person, unpretentious, specific. Patterns borrowed from santifer/career-ops and Paul Jarvis / Pieter Levels / Justin Jackson solo-builder template:

- **First-person hook.** Name the actual personal pain that led to each tool ("I needed this for my HOA, my wife's listings, my own remodel").
- **Concrete receipts.** Numbers from real work, not marketing. "1 HOA running on it" beats "scalable multi-tenant architecture."
- **"This is NOT a ___" paragraph.** Filter tire-kickers by disqualifying the wrong buyers directly.
- **Products are proof, not features.** The fact that Cove is live for WPBCA is the pitch. Don't describe architecture.
- **Honest scarcity.** "One person, a few things at a time, a peninsula I live on." Luxury positioning without the word "luxury."

Explicit anti-patterns (from existing user memory, enforce):
- No corporate "we" or "our team" language — one person, say so
- No hype copy, no agency-speak ("partner with clients to unlock...")
- No scarcity theater ("2 slots per quarter!") — just real availability
- No Luxury Presence visual aesthetic (team-of-200-craftsmen vibe)
- No SaaS landing-page tier tables for project work

---

## Architecture

### Deploy target

Production repo: `~/growdirectprez.github.io/` (GitHub Pages, CNAME → growdirect.io).

Deploy mechanic: edit files in the repo, commit, push. GitHub Pages serves on push. No build step, no static-site generator, no `site/` subdirectory.

No changes to the GrowDirect monorepo (`~/GrowDirect/`) — the site is its own repo.

### File structure (target state after this spec ships)

```
growdirectprez.github.io/
├── index.html         ← NEW: services page (this spec's deliverable)
├── portal/
│   └── index.html     ← MOVED: current gated investor content
├── canary/
│   └── index.html     ← UNCHANGED
├── css/               ← existing; add warmer palette variables
├── img/               ← existing + new imagery (see Visual Design)
├── js/                ← existing; preserve gate-unlock logic in /portal
├── docs/              ← UNCHANGED (technical library)
├── investor/          ← UNCHANGED (preserve deep links)
├── legal/             ← UNCHANGED
├── guides/            ← UNCHANGED
├── market/            ← UNCHANGED (appears to be neighborhood pages)
├── contact.html       ← UPDATE: re-style to match new page (same Formspree endpoint)
├── 404.html           ← UPDATE: re-style to match new page
├── CNAME              ← UNCHANGED
├── robots.txt         ← UNCHANGED
├── sitemap.xml        ← UPDATE: new routes
└── favicon.svg        ← UNCHANGED
```

### Investor-content migration

Current `index.html` (the gated investor portal with Bitcoin-thesis content) moves to `portal/index.html`. The access-code gate UI, unlock JS, and all gated sections (Thesis / Platform / Market / Portfolio) move with it unchanged. URL becomes `growdirect.io/portal/` — no link from the new homepage except a small, understated footer line.

Any existing inbound links to the gated content (from investor outreach, emails, etc.) will break unless redirected. Lowest-cost fix: add `index.html` redirects for any previously-shared deep links (e.g., `/#thesis`, `/#platform`, `/#market`, `/#portfolio`) → their `/portal/#…` equivalents. Plan covers this.

### Nav structure

The new `index.html` is a single-scroll page. Nav is minimal:

- Left: wordmark `GROWDIRECT` (links to `/`)
- Right: `Build` · `Help` · `Rates` · `About` · `Contact` — in-page anchors
- No dropdowns, no mega-menus
- Mobile: collapse to simple text links, no hamburger animation theater

`/portal` is reachable only via a small `Portal` link in the footer. `/canary` is reachable via the Canary product line in the "What I'm building" section and via a footer link.

---

## Page Structure

Seven sections on a single page, ordered top to bottom.

### 1. Hero

Lighter, warmer palette than the investor portal (see Visual Design below). First-person hook, concrete receipts subhead, one short "NOT a ___" paragraph to filter.

**Content intent (not final copy — plan stage will tune):**

> **I'm Greg. I build tools in Palos Verdes.**
>
> I needed them for my HOA, my wife's real estate work, and my own remodel.
> If they fit you too, I'll set them up for you.
>
> *1 HOA running on it · 1 peninsula covered · [N] properties tracked · [N] permits navigated*

Bracketed `[N]` values are placeholders populated by the 2026 retrospective data pull (see section 5). Plan stage runs the retrospective step before final hero copy lands.
>
> **Not a consultancy. Not a helpdesk. Not an agency.** One person, a few things at a time, a peninsula I live on. If that fits, keep scrolling.

Receipts line pulls real numbers from the 2026 retrospective (see section 5).

### 2. What I'm Building

Three product cards, compact, each with status tag (Live / Beta / Shipped). No SaaS feature lists — each card is a short personal paragraph ending with "yours can look like this."

**Cove** — "Member platform I built for my HOA (81 lots in Abalone Cove, Rancho Palos Verdes). If your small HOA wants something that doesn't look like 1998, I'll set one up for you." Status: Live for WPBCA. **Ship-time CTA:** one screenshot of the Cove dashboard inline on hover/expand + a short paragraph. A dedicated WPBCA case-study page is deferred (see *Deferred Follow-ups #8*) and will replace the screenshot target when built.

**Angel** — "Neighborhood intelligence site, live at [ownpalosverdes.com](https://ownpalosverdes.com). If you're a Compass agent outside the South Bay and want the same for your book, I'll build it for you." Status: Live. CTA: *See it live* → ownpalosverdes.com.

**Canary** — single understated line, not a full card. "Loss prevention for Square merchants. Built it. Happy to do a setup session if you want to use it. Not running a helpdesk." Link → `/canary/`.

### 3. What I'll Help With

Plain list. No tier tables, no pricing here (rates live in section 4).

- **Permits & remodels** (local only) — walking through RPV planning, pulling archive records, drawing sets, SketchUp 3D + LayOut construction docs. For homeowners, builders, Compass agents with complicated listings. Backed by the `rpv-permit-architect` skill suite.
- **A day of me** (local only) — show up for a day (or a half-day). Set up your file system. Scan and organize a month of bills. Pick and set up the tool you've been avoiding. Walk you through QuickBooks, your POS, your CRM. Teach you to fish, then leave you running it. Small businesses only.
- **Something custom** (local preferred) — if you've got a specific problem and a budget, tell me about it. Internal tools, data migrations, one-off integrations.

Each bullet has a **scope tag** (Local only / Remote OK) so buyers self-sort.

### 4. Rates

One honest paragraph. No tier table. No "Contact for pricing."

> A day of me: **$1,500**. Half-day: **$800**. Focused 1–2 hour session: **$250–$500**. Project work: quoted per scope, typically **$2,500–$25,000**. Cove for your HOA: **$249/month**, $1,500 setup. Angel for your Compass book: **$349/month**, $2,500 setup (includes the CRMLS data pull). One-page engagement letter for day work; proper contract for anything bigger. I send a W-9; you send a 1099 in January.

No strikethrough-price discount theater. No "starting at." Published rates signal confidence and filter for the right buyers.

### 5. About / What I've Been Up To in 2026

Two elements:

**Brief first-person bio** (one paragraph) — lives in Palos Verdes, wife is a Compass agent, building GrowDirect as a solo shop on purpose, reskilling year, background in [relevant prior work].

**2026 receipts timeline** — curated, bulleted, public-facing list of shipped work. Items pulled from Brain project MOCs and git history across the GrowDirect monorepo. Each item: one line, month, link if applicable.

Example shape (**illustrative only** — actual bullets produced by the retrospective data pull, verified against git + Brain before ship):
- **Jan** — Canary detection engine to 37 rules across 10 categories
- **Feb** — CoAC reactivation framework (Declaration 100 Article II §5 playbook)
- **Mar** — Angel content engine, peninsula lifestyle wiki framework
- **Apr** — Cove platform milestone for WPBCA; Foundation three-entity structure documented; 1926 PV Estates brochure archived

Every bullet reflects real, verified, shipped work — no aspirational claims. Project statuses in the `Brain/REGISTRY.json` and CLAUDE.md project table are the source of truth for status language (e.g., "near-beta," "early dev") and must not be overstated.

This list is the **public** side of the reskilling documentation. The **private** side (unfiltered inventory with dates, hours estimates, receipts, CPA framing) lives at `~/GrowDirect/docs/portfolio/2026-retro.md` — this spec does not publish that file; it's for the CPA.

**Disclaimer (explicit, in this spec):** self-education/reskilling deductibility is a CPA question. This page's public timeline is credibility copy, not a tax document. The companion private doc is organized evidence for a CPA conversation, not advice.

### 6. Contact

Simple form + email. Formspree endpoint (already in the user's stack — see `formspree.rtf` in `~/GrowDirect/`). Three fields: name, email, what you want. No phone (filter friction). No calendar embed (feels SaaS-y).

Copy: "I live here. I answer email. Based in Palos Verdes, California."

### 7. Footer

Small, understated:
- `Canary` → `/canary/`
- `Portal` → `/portal/` (gated — no description, just the word)
- Wordmark + year + "GrowDirect DAO LLC · Palos Verdes, California"

No social links unless the user wants them. No newsletter signup unless there's a newsletter.

---

## Visual Design

Explicit departure from the current investor-portal aesthetic (near-black ink, Bitcoin orange/gold, dense grain, Space Mono monospace labels). The shingle page is warmer and lighter.

**Palette (target direction, plan stage will finalize):**
- Background: off-white or warm paper (e.g., `#F8F5EE` or `#FBF8F1`)
- Ink: near-black, softened (e.g., `#1E1B17`)
- Accent: one warm accent — muted ocher, terra, or deep sea-green (PV-coastal, not Bitcoin orange)
- Borders: hairline warm gray

**Type:**
- Display: serif (e.g., DM Serif Display or Playfair) for section headers and the hero wordmark
- Body: Inter or Space Grotesk for readability
- Monospace: retained for technical callouts (rate figures, timeline dates), lighter touch

**Imagery:**
- One hero image — photograph of Palos Verdes / peninsula (user has photography assets in `~/GrowDirect/` root and Angel repo)
- Product card thumbnails: real screenshots of Cove dashboard, ownpalosverdes.com hero, Canary chirp panel
- No stock photography. No abstract "tech" illustrations.

**Canary bird icon:** the existing `canary-icon-512.png` hero bird remains reserved for Canary specifically — **do not use it as the GrowDirect wordmark or elsewhere on the new page** (per user memory `feedback_use_canary_brand_logo.md`).

**Typographic wordmark for GrowDirect:** plain text in the display serif, no logomark. If a logomark is needed later, that's a separate design exercise — not in scope.

---

## Reskilling Retrospective Sub-Deliverable

Two companion outputs produced from the same 2026-YTD data collection pass:

**Public (on the page):**
- Section 5 timeline, curated for outside readers
- Links only to public artifacts (ownpalosverdes.com, Cove demo, Canary page)

**Private (not deployed, in monorepo):**
- `~/GrowDirect/docs/portfolio/2026-retro.md`
- Unfiltered inventory: dates, project, hours estimate, skills-learned mapping, tool/course receipts (linked where digital), notes on how each ties to the active Schedule C trade
- Format: plain markdown, CPA-readable
- Explicitly marked as organizing evidence, not tax advice

Data sources for both:
- `git log --all` across `~/GrowDirect/` (project commit history)
- `Brain/projects/*.md` MOCs (Canary, Cove, Angel, Seacove)
- `Brain/wiki/` (produced knowledge artifacts)
- `~/ownpalosverdes/` git history (site work)
- `~/growdirectprez.github.io/` git history (site work)
- Linear GRO-prefixed issues (if accessible — plan stage to verify)

---

## Contract & Payment Mechanics

Surface-level copy on the page (in the Rates paragraph), details not pitched:

- **Day rate / session work:** 1-page engagement letter, no MSA. Payment on completion, net-7. Venmo, Zelle, or ACH.
- **Projects ($2,500+):** simple MSA + SOW. 50% on start, 50% on delivery. Template to be commissioned from a local small-business attorney (Torrance/PV) as a separate task — not a blocker for page ship.
- **Hosted products (Cove / Angel monthly):** Terms of Service + data processing terms. Stripe subscription billing. DPA if the client asks.

**Explicitly out of scope for this spec:** the attorney engagement, the MSA template itself, the Stripe integration for monthly SaaS billing, and the Formspree → CRM pipeline. Those are downstream tasks that show up on the page via copy only.

---

## SEO & Distribution

Light touch:
- Update `sitemap.xml` with new routes
- Set real `<meta>` descriptions for the new index (currently misleading "immutable commerce infrastructure" copy)
- Set OG image to a new peninsula hero shot + wordmark composition
- Preserve GA4 (tag `G-ELPTR2ZLP3`)
- Retain robots.txt

No schema.org markup beyond `LocalBusiness` (address: Palos Verdes, CA). No blog. No content-marketing funnel.

Nextdoor distribution: the day-rate section anchor (`/#help` or `/#day`) is the deep link. A dedicated `/day` subpage is **deferred** — ship the main page first, evaluate Nextdoor traffic behavior, then decide whether a bespoke landing page earns its keep.

---

## Non-Goals

Explicitly **not** in this spec (and not silently creeping in):

- Multi-page site with per-pillar subpages (Cove / Angel / Canary each get one card on the homepage; dedicated product microsites are a future consideration)
- Luxury Presence-style "concierge agency" aesthetic
- Square Solutions Partner certification-focused copy
- Bitcoin / ordinals / immutable-ledger thesis on the public homepage (lives at `/portal` only)
- Newsletter, blog, RSS
- Team scaling implications ("from prototype to production team")
- Scarcity theater, countdown timers, artificial availability claims
- Agency voice (no "we," no "our team")
- Any copy that could read as AI-generated ("unlock," "empower," "synergize," "journey," etc.)
- Case studies of prior employers or non-GrowDirect client work (receipts timeline covers 2026 GrowDirect work only)

---

## Deferred Follow-ups

Explicit follow-ups to track but not include in this implementation:

1. `/day` dedicated Nextdoor landing page (after main page ships, if warranted)
2. Dedicated Cove product microsite with feature pages and pricing calculator
3. Dedicated Angel product microsite with sample agent site gallery
4. MSA + SOW template (attorney engagement, $750–$1,500)
5. Stripe billing integration for Cove / Angel monthly subscriptions
6. Formspree → Linear or Notion pipeline for contact intake triage
7. Per-neighborhood landing pages for SEO (e.g., `/rpv`, `/rolling-hills-estates`) — only if local SEO becomes a priority channel
8. Case-study page for WPBCA / CoAC Cove deployment

None of these block the page ship.

---

## Success Criteria

The page ships when:

1. Visiting `growdirect.io/` loads the new services page, not the gate
2. Visiting `growdirect.io/portal/` loads the prior investor content with the gate intact
3. Visiting `growdirect.io/canary/` loads unchanged
4. All seven sections render on desktop and mobile (responsive at 375px, 768px, 1280px)
5. The Formspree contact form delivers to the user's configured address
6. GA4 tracking fires on page load for `/`, `/portal/`, and `/canary/` (regression check — the migration must not break analytics on preserved pages)
7. Receipts timeline reflects real 2026 YTD work, pulled from actual data sources
8. `docs/portfolio/2026-retro.md` exists in the GrowDirect monorepo with the private inventory
9. No broken links from the old deep links (`/#thesis`, `/#platform`, `/#market`, `/#portfolio` redirect to their `/portal/` equivalents)
10. Copy reads first-person and honest on a cold read — no AI-ish hype, no agency-speak, no tier theater

Post-ship signals (not ship blockers):
- At least one inbound inquiry via the contact form within 30 days
- Nextdoor business page created and linked to the page
- At least one HOA or Compass-agent inquiry attributed to the productized sections

---

## Open Questions

To resolve during the plan/implementation phase, not ship blockers:

1. **Palette finalization.** Three candidate palettes (paper/ocher, paper/terra, paper/sea-green) — will mock in plan stage and confirm with user before building.
2. **Hero photograph.** Which existing peninsula image from the user's archive, or new photograph? User preference needed.
3. **Receipts timeline granularity.** Month-by-month or a flatter "here's 2026 so far" bulleted list? Recommend month-by-month for clarity; confirm.
4. **Bio length.** One sentence, one paragraph, or two paragraphs? Recommend one tight paragraph; confirm.
5. **Wife's Compass network mention.** Does the user want her named/linked in the Angel card, or kept implicit ("I have real-estate domain access")? Recommend implicit — keeps the page about GrowDirect, avoids couple-branding.
6. **Investor-portal deep-link redirects.** Any specific historical URLs that were shared externally and need dedicated redirect entries? Plan stage to audit.
7. **Canary positioning on the page.** Current plan: one understated line in the "What I'm building" section + footer link. Alternate: remove from "What I'm building" entirely, footer-only. Recommend the current plan (it's real work, owning it honestly is better than hiding it); confirm.
8. **Phone contact option.** Current plan: email/form only, no phone (filter friction, avoids SaaS-y feel). Nextdoor-sourced local SMB traffic often converts better by phone — worth a round of user confirmation. If user wants phone, consider a click-to-call link on mobile only, text-only on desktop.

---

## Risks

1. **Voice drift during implementation.** Without tight copy review, the generated page could slide into hype language or agency voice. Mitigation: implementation plan includes a brand-review pass against user memory anti-patterns before ship.
2. **Investor-content regression.** Moving the gated content risks breaking the gate unlock JS or hashing the access code path. Mitigation: plan includes a regression check that `/portal/` behaves identically to the current `/`.
3. **Receipts timeline accuracy.** Pulling 2026 YTD from git + Brain carries the risk of misattributing or inflating. Mitigation: user reviews the timeline before it goes live; no unverified claims.
4. **Local SEO lift expectations.** This spec does not promise SEO traffic. Any "I'll rank for RPV permit help" expectation should be explicit. Mitigation: call this out in the plan's expected-outcomes section; the page is primarily a destination for existing traffic sources (Nextdoor, referral, wife's network), not an organic-search acquisition engine.

---

## Handoff

Once this spec is approved by the user and passes the spec-document-reviewer loop, the next step is the writing-plans skill to produce the implementation plan. The plan will:

- Break the work into independently-verifiable steps (migrate `/portal`, build new `index.html`, generate retrospective, update supporting pages, redirect legacy links, ship)
- Specify tests/verification for each step
- Identify any parallelizable work (e.g., palette mocks vs. copy drafting can proceed in parallel)
- Produce the 2026-retro data pull as its own step (git + Brain inventory) so the receipts timeline can be populated with real numbers before final copy lands

The plan does **not** include the attorney engagement, Stripe integration, or follow-up items listed in *Deferred Follow-ups*.
