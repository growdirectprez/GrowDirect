---
classification: confidential
owner: GrowDirect LLC
---

# growdirect.io Portfolio Site

**Date:** 2026-04-14
**Status:** Approved
**Scope:** Replace current Bitcoin-focused single-page site with a multi-page portfolio site for GrowDirect consulting

---

## Problem

growdirect.io currently shows a single-page Bitcoin notarization pitch (pushed Feb 2026). It doesn't reflect what GrowDirect actually does — build full-stack platforms across multiple verticals. Two immediate revenue paths need a professional web presence:

1. **Square partnership network** — Solutions Partner certification (waitlisted), POS consulting contracts. Square reviewers will look at this site.
2. **Real estate agents** — Compass/Redfin/LP agents paying $2K+/year for basic hosted websites that GrowDirect can replace with dramatically better tooling.

A third pillar (membership/governance platforms) proves range and has future BPO potential.

The site also needs to imply team scaling capacity (Poland dev contacts) without being explicit — "from prototype to production team."

---

## Decision

**Approach B: Multi-Page Static Site.** Homepage + one page per pillar + contact. Plain HTML/CSS/JS on GitHub Pages via existing `growdirectprez.github.io` repo (CNAME already points to growdirect.io). No framework, no build step. Fresh design language distinct from all three products.

---

## Site Map

```
growdirect.io/
├── index.html           — Homepage: two lead service lines + capabilities + about + contact
├── pos-platform.html    — Retail & POS Intelligence (Canary/RaaS showcase)
├── re-toolkit.html      — Real Estate Agent Toolkit (Angel showcase)
├── membership.html      — Membership Framework (Cove showcase)
├── contact.html         — Simple form + email
├── assets/
│   ├── css/style.css    — GrowDirect base styles + CSS custom properties per pillar
│   ├── js/main.js       — GA4 event tracking, Formspree form submit, mobile nav toggle, sticky nav border on scroll
│   └── img/             — GrowDirect wordmark, OG images, pillar brand marks
├── favicon.svg
├── 404.html             — Branded "page not found" with nav back to homepage
├── CNAME                — growdirect.io (existing, do not change)
├── robots.txt
└── sitemap.xml
```

---

## Homepage (index.html)

### Navigation

Sticky top nav bar, visible on all pages. Left: GrowDirect wordmark (links to `/`). Right: text links — `POS Platform`, `RE Toolkit`, `Membership`, `Contact`. On mobile (< 768px), collapse to a hamburger menu. Nav background matches page background (#F8F7F4) with a subtle bottom border on scroll. No dropdowns, no mega-menus.

### Section 1 — Hero

Clean, light background. GrowDirect wordmark (new — not the canary bird). V1 wordmark: "GrowDirect" set in Space Grotesk 700, near-black (#1A1A1A). No logomark needed for launch — the typographic wordmark is the brand. Iterate to a designed mark later if warranted.

Headline: *"From prototype to production. Platforms that ship."*

No subheadline. No buzzwords. The sections below do the talking.

### Section 2 — Two Lead Service Lines

Equal-weight cards, each with its product's brand color as accent:

**Retail & POS Intelligence**
- Accent: Canary gold
- What: Event pipelines, real-time detection, merchant analytics, Bitcoin notarization
- Who it's for: Square merchants and the Square partnership ecosystem
- Links to: `/pos-platform.html`

**Real Estate Agent Toolkit**
- Accent: Angel coastal teal
- What: Content engines, MLS market data, SEO, neighborhood intelligence, agent chat, lead capture
- Who it's for: Compass, Redfin, and LP agents who are overpaying for basic websites
- Links to: `/re-toolkit.html`

### Section 3 — Third Pillar (Supporting)

Smaller card, same pattern:

**Membership Framework**
- Accent: Cove deep blue
- What: GIS/mapping, governance workflows, member management, document vault, county services integration
- Who it's for: HOAs, membership organizations, BPO automation
- Links to: `/membership.html`

### Section 4 — Capabilities Strip

Horizontal scannable tags — proof of range without paragraphs:

`Data Modeling` · `API Gateway` · `MCP Architecture` · `Agentic Systems` · `Machine Learning` · `Dashboards` · `SEO` · `Data Governance` · `Event Pipelines` · `GIS / Mapping` · `Content Engines` · `Lead Generation` · `Factory Process`

### Section 5 — About

3-4 sentences distilled from the Manifesto (GRO-496 will produce the full Brain wiki article, but this section can be written now from what we know):

- 30 years in retail technology (IBM 4690, LaneHawk, POS systems)
- The observation: every POS system has mutable transaction logs — records that can be silently edited
- Built platforms that solve this — from prototype to production, solo or with a team
- AI-assisted development, ships real products

Links to Square blog one-pager when GRO-497 ships. Until then, just the text.

### Section 6 — Contact

Email address displayed directly (gclyle@growdirect.io). Link to `/contact.html` page: *"Have something to build?"*

### Section 7 — Footer

Minimal. Copyright 2026 GrowDirect. Email. GA4 tracking note (privacy signal).

---

## Pillar Pages

Each pillar page follows the same template but carries its product's brand identity as a feature — demonstrating that GrowDirect doesn't just build products, it builds brands.

### Template Structure

1. **Header** — Pillar name + product brand mark/color
2. **What Was Built** — Architecture description, not marketing copy. What the system does, how it's structured, what technologies it uses. A developer or Square reviewer reads this and understands the depth.
3. **Capability Breakdown** — 6-8 specific capabilities with brief descriptions. No stats, no fake numbers — just what each piece does.
4. **Stack** — Technologies used (Flask, PostgreSQL, Valkey, Tailwind, etc.)
5. **CTA** — Link back to contact. Contextual: "Want something like this?" or "Let's talk about your merchants."

### POS Platform Page (`pos-platform.html`)

Product identity: Canary (gold accent)

**What Was Built:**
A real-time loss prevention and analytics platform built on Square's API. Captures every webhook event, seals it cryptographically, runs 29 detection rules, and surfaces alerts to merchants in plain language.

**Capabilities:**
- Square Webhook Pipeline — OAuth, HMAC validation, real-time event capture
- Transaction Stream Processing — 4-stage pipeline (hash, parse, merkle, detect)
- Chirp Detection Engine — 29 rules across 3 severity tiers, plain-language alerts
- Fox Case Management — Investigation workflows with evidence chains
- Owl AI Analytics — Ollama-powered analysis, MCP tool interface
- RaaS Namespace — Bitcoin Ordinal inscription, namespace resolution
- Merchant Dashboard — Risk scoring, KPI visualization, alert management
- Multi-POS Architecture — Adapter pattern for source-agnostic ingestion

**Stack:** Python/Flask, PostgreSQL 17 with pgvector, Valkey 8, SQLAlchemy 2.0, Alembic, Tailwind, Alpine.js, Ollama, Docker Compose

### RE Toolkit Page (`re-toolkit.html`)

Product identity: Angel (coastal teal accent)

**What Was Built:**
A neighborhood intelligence platform for real estate agents. Combines MLS listing data, county parcel records, community content, and conversational AI into a toolkit that replaces basic hosted websites with a data-driven content engine.

**Capabilities:**
- Neighborhood Hub System — DB-backed pages with voice overlays, Schema.org markup, SEO optimization
- MLS Data Platform — CRMLS integration, 214-column listing ingest, APN-based parcel bridge
- Market Snapshots — Automated monthly/quarterly aggregations by area
- Community Intelligence — RSS crawl pipeline, entity/event database, keyword classification
- Agent Chat Widget — Claude-powered sidecar with 12 MCP tools, trained on neighborhood knowledge
- Lead Capture Pipeline — Webhook integration, CRM sync, contact management
- SEO Foundation — Sitemap, robots.txt, OG meta, canonical URLs, school guide pages

**Stack:** Python/Flask, PostgreSQL 17, Tailwind, Alpine.js, Leaflet.js, Claude API, Docker Compose

### Membership Page (`membership.html`)

Product identity: Cove (deep blue accent)

**What Was Built:**
A governance and operations platform for a real HOA (81 lots, Davis-Stirling compliant). GIS-integrated parcel management, secret ballot elections with row-level security, treasury, document vault, and AI-powered legal document search.

**Capabilities:**
- GIS Parcel Engine — 5,514 APN-keyed parcels, Leaflet mapping, GeoJSON rendering, county data enrichment
- Governance Engine — Proposal lifecycle, quorum calculation, Davis-Stirling compliance
- Secret Ballot Elections — Two-envelope scheme, PostgreSQL RLS, cryptographic ballot separation
- Treasury Management — Assessment tracking, payment processing, delinquency workflows
- Document Vault — Upload, access tiers, embedding generation for semantic search
- Knowledge Search — pgvector legal document search via MCP server
- Meeting Management — Scheduling, ARC reviews, ICS generation
- Member Auth — Magic link login, role-based access (member, board, admin)

**Stack:** Python/Flask, PostgreSQL 17 with pgvector, Valkey 8, Leaflet.js, Tailwind, Alpine.js, Ollama, Docker Compose

---

## Contact Page (`/contact`)

Simple form:
- Name (text input)
- Email (email input)
- "What are you working on?" (textarea)
- Submit button

Form submission: POST to a simple endpoint. Options (in order of preference):
1. Formspree or similar free-tier service (no backend needed)
2. Mailto link fallback if form service is too much friction

Email address also displayed directly on the page for people who prefer that.

GA4 event fires on form submit.

Page is `noindex` — no SEO value, don't want it in search results.

---

## Design Language

### GrowDirect Identity

- **Base:** Warm off-white (#F8F7F4) background, near-black (#1A1A1A) text
- **GrowDirect accent:** Warm charcoal (#3D3D3D) as provisional. Iterate after seeing it in context.
- **Typography:** Inter (400, 500, 600) for body. Space Grotesk (500, 600, 700) for headings. Both already loaded on current site via Google Fonts.
- **No dark mode.** Clean, light, professional. Not a tech-bro portfolio.
- **No animations.** No scroll reveals, no parallax. Content loads and is readable immediately.
- **No stock imagery.** Architecture descriptions and capability breakdowns replace hero images. If we add visuals later, they'll be actual diagrams from the products.

### Pillar Brand Colors

Each pillar page uses CSS custom properties to swap accent colors:

| Pillar | Accent | Usage |
|--------|--------|-------|
| POS Platform | Canary gold (#FBBF24) | Headers, capability icons, CTAs |
| RE Toolkit | Angel coastal teal (#2DD4BF — provisional, warm teal) | Same |
| Membership | Cove deep blue (#1E3A5F — provisional, nautical) | Same |

### Responsive

Mobile-first. The site will be shared via link in Square partner applications, LinkedIn messages, and texts. Must look good on phone.

Breakpoints:
- Mobile: < 768px — single column, stacked cards
- Tablet: 768-1024px — two-column service cards
- Desktop: > 1024px — full layout

---

## SEO

### Per-Page Targets

| Page | Title Tag | Meta Description | Target Keywords |
|------|-----------|------------------|-----------------|
| Homepage | GrowDirect — Full-Stack Platform Development | Full-stack platform development for retail, real estate, and membership organizations. From prototype to production. | retail technology consulting, platform development |
| POS Platform | Retail & POS Intelligence — GrowDirect | Real-time loss prevention and analytics platform built on Square's API. Event pipelines, detection rules, merchant dashboards. | Square loss prevention, POS analytics, Square webhook integration, retail technology |
| RE Toolkit | Real Estate Agent Toolkit — GrowDirect | Neighborhood intelligence platform for real estate agents. MLS data, community content, conversational AI, and lead capture. | real estate agent website, Compass agent toolkit, MLS data platform, neighborhood content |
| Membership | Membership Framework — GrowDirect | Governance and operations platform for HOAs and membership organizations. GIS parcels, elections, treasury, document vault. | HOA management platform, membership governance, GIS parcel management |
| Contact | Contact — GrowDirect | (noindex — no description needed) | (noindex) |

### Technical SEO

- Unique `<title>` and `<meta name="description">` per page
- OG and Twitter Card meta per page with unique descriptions and (eventually) unique OG images
- `sitemap.xml` listing all 4 indexable pages (exclude `contact.html`)
- `robots.txt` allowing all (no Disallow rules — use `<meta name="robots" content="noindex">` on `contact.html` instead, since `robots.txt` only blocks crawling, not indexing)
- Canonical URLs on every page
- `<html lang="en">` on every page
- Semantic HTML (header, main, section, footer, nav)
- Alt text on any images added later

---

## Analytics

GA4 property (Measurement ID: `G-ELPTR2ZLP3` — create property in GA4 admin before launch, replace placeholder). Tag on all pages.

Events to track:
- `page_view` (automatic)
- `pillar_click` — which service line card was clicked from homepage
- `contact_form_submit` — form submission on contact page
- `email_click` — click on email address
- `cta_click` — any "have something to build?" or pillar page CTA click

No cookie banner needed for GA4 basic implementation (no advertising features, no remarketing).

---

## Deployment

### Infrastructure

- **Hosting:** GitHub Pages via `growdirectprez/growdirectprez.github.io` repo
- **Domain:** CNAME file already points to growdirect.io — do not change
- **SSL:** GitHub Pages provides automatic HTTPS
- **CI/CD:** Push to `main` branch = deploy. No build step needed.

### Deployment Steps

1. Clone `growdirectprez.github.io` as a subdirectory or work in a worktree
2. Replace all existing files (the old Bitcoin site)
3. Keep `CNAME` file unchanged
4. Push to `main`
5. Verify at growdirect.io

---

## Dependencies

| Dependency | Status | Blocks |
|------------|--------|--------|
| GRO-496 (Brain: manifesto distillation) | Backlog | About section text (can write placeholder now) |
| GRO-497 (Square blog one-pager) | Backlog | About section link (omit until ready) |
| Square partner waitlist application | Not started | POS page CTA refinement |
| GrowDirect brand color selection | Not started | CSS accent color (use placeholder, iterate) |
| OG images per page | Not started | Social sharing (text-only meta works without them) |

None of these block shipping the site. All can be iterated after launch.

---

## Out of Scope

- Blog / news section — not needed yet
- Client login / dashboard — this is a static portfolio
- Pricing page — too early, conversations happen via email
- Dark mode — not this design
- CMS — 5 HTML files don't need one
- RaaS subdomain — separate project, separate spec
- Framework migration (Astro/11ty) — graduate to this if the site grows

---

## Success Criteria

- Site live at growdirect.io with all 5 pages
- GA4 tracking events firing
- Contact form delivering to email
- Mobile-responsive, loads fast, no layout breaks
- Square partner waitlist submission references the site
- At least one Compass agent conversation uses the RE Toolkit page as collateral
