# Angel Web Strategy

> **Status:** Proposed — design spec, not yet built
> **Namespace:** angel
> **Date:** 2026-04-06
> **Author:** ALX (COO) / Jeffe (CEO)
> **Dependencies:** Angel Agent, Angel data platform

---

## 1. Overview

Angel's web strategy uses three domains with distinct roles that funnel
traffic toward a single outcome: a phone conversation between the visitor
and Angelique Lyle.

| Domain | Role | Platform | Owner |
|--------|------|----------|-------|
| **AngeliqueLyle.com** | Flagship luxury presence | Luxury Presence (LP) | Angelique |
| **TheHillPV.com** | Silent SEO content engine | GrowDirect Flask stack | GrowDirect |
| **OwnPalosVerdes.com** | Secondary SEO (reclamation) | TBD — needs spam cleanup | Angelique |

The Angel chatbot widget is the connective tissue — embedded on all three
sites, it provides the same proprietary data experience regardless of entry
point and captures leads into a single pipeline.

---

## 2. AngeliqueLyle.com — Flagship Refresh

### Current State

- Hosted on **Luxury Presence** (LP) — a managed platform powering 50K+ agent sites
- LP handles IDX integration, responsive design, hosting, SSL
- Content is outdated — existing brand materials are disjointed (Abalone Shore,
  various themes that don't cohese)
- Domain is Angelique's primary professional identity

### Strategy: Refresh, Don't Rebuild

Rebuilding on our stack would mean losing LP's IDX feed, managed hosting, and
the 50K-agent network effects. Instead, we refresh the content and integrate
Angel where LP allows.

**Phase 1 — Content refresh (no code required):**
- Update bio, headshot, and brand messaging to new Angel brand identity
- Rewrite neighborhood pages with data-backed market insights
- Add testimonials and transaction highlights
- Update property descriptions with Angelique's authentic voice
- Remove all "Abalone Shore" branding and disjointed legacy material

**Phase 2 — Chat widget integration (needs LP investigation):**

LP integration options (in order of preference):
1. **Custom script injection** — if LP allows `<script>` tags in custom HTML
   sections, embed the Angel chat widget directly. This is the cleanest path.
2. **LP API / webhook** — LP may offer an API for adding custom features.
   Requires API key or partner relationship.
3. **Subdomain redirect** — `chat.angeliquelyle.com` points to our stack,
   linked from LP site via buttons/CTAs. Visitor leaves LP momentarily to
   interact with Angel, then returns.
4. **Bridge CTA** — LP site includes prominent "Ask Angel" buttons that
   link to TheHillPV.com chat. LP handles the brochure; our stack handles
   the conversation.

**Phase 3 — Content syndication (future):**

If LP supports custom page content via API or embed, Angel can generate
and publish data-driven content (market reports, neighborhood guides) to
AngeliqueLyle.com automatically. This would give the LP site the depth of
a custom site without rebuilding it.

### What LP Keeps Owning

- IDX listing search (MLS-compliant, already integrated)
- Responsive templates and design system
- SSL, hosting, CDN
- SEO baseline (domain authority, sitemap, meta tags)
- Mobile responsiveness

### What Angel Adds

- Conversational AI (chat widget, if injection is possible)
- Data-backed content (market reports written from Angel's dataset)
- Brand consistency (new Angel identity applied to LP's template)
- Lead capture that feeds into Angel's pipeline (not just LP's default form)

---

## 3. TheHillPV.com — Silent SEO Engine

### Purpose

TheHillPV.com is a data-driven local content site that builds SEO authority
for Palos Verdes real estate search terms. It is NOT obviously an agent
marketing site — it reads like an independent local guide. Angelique's
association is subtle (author bylines, "About" page) until the visitor
engages with Angel and is routed to her.

"The Hill" is PV locals' own name for the peninsula. The domain speaks to
insiders and curious outsiders alike.

### Platform

Blueprint on Cove Flask app (port 5002). Full control over content, SEO, analytics,
and chat integration through Angel blueprints registered in Cove.

```
TheHillPV.com
├── / (home) — "Life Above the Pacific" — editorial landing
├── /neighborhoods/{slug} — RPV, PVE, RHE, RH, Lunada Bay, etc.
├── /schools — PVPUSD guide, feeder patterns, ratings
├── /market — Monthly market report (auto-generated from data)
├── /market/{area}/{month} — Granular market snapshots
├── /streets/{slug} — Notable streets / micro-neighborhoods
├── /guides/{slug} — Relocation guide, first-time buyer, downsizer
├── /blog/{slug} — Editorial content in Angelique's voice
├── /ask — Full-page Angel chat experience
└── /api/chat — Angel Agent endpoint (proxied to sidecar)
```

### Content Strategy

Content is generated from Angel's proprietary dataset, not scraped or
generic. Every page has data that no competitor can replicate because it
comes from our APN-level database.

**Neighborhood pages** (`/neighborhoods/lunada-bay`):
- Boundaries and character description (from knowledge base)
- Current active listings count and median price (from Angel listings)
- Recent sales with price-per-sqft trends (from Angel listings, Closed)
- School assignments (from GreatSchools + knowledge)
- Walk score, commute estimates (future integration)
- Angel chat widget pre-loaded with neighborhood context

**Market reports** (`/market/rpv/2026-03`):
- Auto-generated monthly from Angel market_snapshots table
- Active inventory, closings, median prices, DOM, inventory months
- MoM and YoY comparisons
- Price-per-sqft by area
- "What this means" summary (LLM-generated, editorially reviewed)

**School guide** (`/schools`):
- PVPUSD overview with all campuses
- Feeder pattern visualization
- Ratings from GreatSchools
- Enrollment and demographic trends (public data)
- "Schools by neighborhood" cross-reference

**Street profiles** (`/streets/via-del-monte`):
- Micro-neighborhood character from knowledge base
- Historical transaction data for properties on the street
- Average home values and recent sales

### SEO Architecture

**Target keyword clusters:**
- "Palos Verdes homes for sale" / "Rancho Palos Verdes real estate"
- "PV peninsula neighborhoods" / "Lunada Bay homes"
- "PVPUSD schools ranking" / "Palos Verdes schools"
- "Palos Verdes market report" / "RPV home prices"
- "{Street name} Palos Verdes" — long-tail, low competition
- "Moving to Palos Verdes" / "Palos Verdes relocation guide"

**Technical SEO:**
- Server-rendered HTML (Flask + Jinja2, not SPA) — fully crawlable
- Schema.org structured data on every page (RealEstateListing, Place, School)
- Sitemap.xml auto-generated from content routes
- Meta descriptions auto-generated from data summaries
- Canonical URLs, proper heading hierarchy
- Page speed: minimal JS (Alpine.js only for interactivity), Tailwind CSS
- Mobile-first responsive design

**Content velocity:**
- Market reports: auto-generated monthly (12/year × 5 areas = 60 pages/year)
- Neighborhood pages: manually curated, updated quarterly with fresh data
- Blog posts: 2–4/month, written with Angel Voice skill, editorially reviewed
- Street profiles: batch-generated from data, ~50 notable streets

### Analytics and Lead Attribution

```
Visitor lands on TheHillPV.com
    │  (organic search, social, referral)
    │
    ├── Reads content (page views, time on page, scroll depth)
    │
    ├── Engages with Angel chatbot
    │   ├── Asks about a property → parcel_lookup tool
    │   ├── Asks about market → market_stats tool
    │   └── Ready to act → capture_lead tool
    │       │
    │       ▼
    │   Lead captured: phone, interest, property context
    │       │
    │       ├── SMS to Angelique
    │       ├── Lead → Angel DB (with source: "thehillpv", page: "/neighborhoods/rpv")
    │       └── Async: Compass CRM sync
    │
    └── Clicks CTA → AngeliqueLyle.com (tracked referral)
```

**Attribution fields on every lead:**
- `source_domain` — thehillpv.com, angeliquelyle.com, ownpalosverdes.com
- `source_page` — the specific URL they were on when they engaged
- `source_referrer` — how they found the site (organic, social, direct, email)
- `conversation_turns` — how deep the chat went before capture

---

## 4. OwnPalosVerdes.com — Reclamation

### Current State

The domain has been compromised with spam content ("Best Chicken Road Game
Accessories," "Ideal Casinos That Accept Mastercard Deposits"). The SEO
authority is likely damaged. The domain may be flagged by Google.

### Recovery Plan

**Phase 1 — Cleanup (immediate):**
1. Remove all spam content
2. Audit for malware, unauthorized redirects, injected scripts
3. Change all credentials (hosting, DNS, CMS admin)
4. Submit Google Search Console reconsideration request if penalized
5. Set up basic holding page with Angelique's branding

**Phase 2 — Repurpose (after authority recovers):**

If Google penalty is lifted and domain authority recovers:
- Use as a secondary content site (mirrors select content from TheHillPV)
- Target "Own Palos Verdes" keyword cluster (buyer-intent)
- NOT obviously tied to Angelique — positioned as community resource
- Angel widget embedded for lead capture
- Redirect strategy: any residual traffic from old spam pages → 301 to
  relevant TheHillPV content

If domain authority is irreparably damaged:
- Park the domain (prevent competitor acquisition)
- Redirect all traffic to TheHillPV.com via 301
- Do not invest further content effort

**Phase 3 — Evaluation (90 days after cleanup):**
- Check Google Search Console for impressions recovery
- Monitor organic traffic trend
- Decision: invest in content or permanent redirect

---

## 5. Lead Flow — All Sites

Regardless of which domain a visitor enters through, the lead flow converges:

```
                    AngeliqueLyle.com (LP)
                         │
                    Angel Widget (if embedded)
                    or CTA → TheHillPV
                         │
TheHillPV.com ──────────►│◄──────────── OwnPalosVerdes.com
    │                    │                    │
    ▼                    ▼                    ▼
   Cove Flask (port 5002, hosts Angel blueprints)
            │
            ▼
    Angel Agent Sidecar (port 8004)
            │
       Lead captured
       (phone, interest, property, source)
            │
   ┌────────┼────────┐
   ▼        ▼        ▼
  SMS    Cove DB   Compass CRM
  to     (leads    (async sync)
Angelique table)
```

### Lead Stages

1. **Identified** — APN-based signal (transfer, expiration, equity), no visitor interaction yet
2. **Engaged** — Visitor started Angel conversation (3+ turns)
3. **Captured** — Phone number collected via Angel widget
4. **Contacted** — Angelique has called/texted back
5. **Showing** — Property tour scheduled
6. **Offer** — Offer submitted
7. **Escrow** — Under contract
8. **Closed** — Transaction closed
9. **Archived** — Not pursuing, with reason

---

## 6. Infrastructure

### TheHillPV.com Stack

| Component | Detail |
|-----------|--------|
| App | Cove Flask 3+ on port 5002 (Angel blueprints registered here) |
| Agent | Angel Agent sidecar on port 8004 |
| Database | `cove` on shared PostgreSQL (Angel tables alongside Cove) |
| Cache | Valkey DB 1 (sessions, page cache, rate limits) (shared with Cove) |
| CSS | Tailwind 3.x with PostCSS build |
| JS | Alpine.js 3.x (minimal interactivity) |
| Maps | Leaflet.js (neighborhood boundaries, property pins) |
| Hosting | Docker container on GrowDirect infrastructure |
| DNS | Cloudflare (DNS + CDN + SSL) |

### Domain DNS

| Domain | Points To | Purpose |
|--------|----------|---------|
| thehillpv.com | GrowDirect infra (Cloudflare → Docker) | Primary SEO engine |
| angeliquelyle.com | Luxury Presence | Flagship (managed by LP) |
| ownpalosverdes.com | TBD — cleanup first | Secondary SEO or redirect |
| chat.angeliquelyle.com | GrowDirect infra (optional) | Angel widget API subdomain |

---

## 7. Competitive Positioning

### What Angelique Has That Others Don't

Every agent on the Hill has a website. Most are templated IDX sites from
KVCore, Chime, Sierra, or Luxury Presence. They all show the same MLS data
through the same IDX feeds.

Angel's web strategy is different because:

1. **Proprietary dataset** — 5,514 parcels + 2,368 listings + ATTOM enrichment,
   not just the IDX feed
2. **Conversational interface** — Angel answers questions in natural language,
   not just search filters
3. **Content depth** — street-level profiles, school feeder patterns, market
   snapshots by micro-neighborhood
4. **Silent lead capture** — visitor gets value (answers, data, insights) before
   being asked for contact info
5. **Unified pipeline** — every interaction, regardless of entry point, feeds the
   same lead funnel to Compass CRM

### Marketing Tool Landscape

Angel replaces or complements several tools agents typically pay for:

| Tool | What It Does | Angel Equivalent |
|------|-------------|-----------------|
| Ylopo | Paid lead generation (PPC → IDX → lead) | Organic SEO + Angel chat → lead |
| Adwerx | Retargeting ads | Future: retarget TheHillPV visitors |
| Curaytor | Done-for-you content marketing | Angel Voice skill + auto-generated content |
| Lofty/Sierra/kvCORE | All-in-one CRM + website + leads | Angel data + TheHillPV + Compass CRM |
| Luxury Presence | Premium agent website | Keep for flagship; TheHillPV supplements |

### LP Custom Webhook Integration

Luxury Presence sites can integrate with external systems via custom webhooks.
Angel leverages this to sync lead profiles from AngeliqueLyle.com into the
unified pipeline. When LP widget or forms capture contact info, the data is
POSTed to Angel's `/webhook/lp` endpoint, merged with any Angel chat context,
and routed to Compass CRM alongside TheHillPV.com leads.

---

*Angel Web Strategy SDD — GrowDirect Inc.*
