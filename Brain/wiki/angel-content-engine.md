---
date: 2026-04-13
type: wiki
status: active
tags: [angel, content-engine, voice, crawl, wiki, seo, kanban, open-house]
sources: [docs/sdds/angel/web-strategy.md, Brain/wiki/south-bay-wiki-architecture.md, Cove/cove/angel/crawl.py, Cove/cove/angel/voice_overlays.py, Cove/cove/angel/seed_content.py]
last-compiled: 2026-04-13
needs-review: 2026-04-27
---

# Angel Content Engine

## Summary

The content engine is the system that turns raw data (CRMLS listings, web crawls, RSS feeds) and qualitative knowledge (this wiki) into Angelique's online presence — neighborhood guides, market reports, school guides, blog posts, and eventually an open house iPad experience. The wiki is the data warehouse for qualitative knowledge. The Cove database is the warehouse for structured data. Content reads from both.

The operating metaphor is a **support desk for an agent's online persona** — a kanban-style workflow where content freshness is tracked, stale items are flagged, and the system produces outputs that make Angelique's digital presence feel as current and natural as an in-person open house conversation.

## The Content Operations Problem

Most agents create content episodically — they write a blog post when they remember, update their bio once a year, post a just-sold photo when they feel like it. The result: an online presence that feels stale within weeks.

Angel treats content as an operations problem with a queue:

**Incoming signals (the backlog):**
- Weekly CRMLS export → new listings, price changes, closings, expirations
- RSS crawl (daily) → local news, community events, new restaurant openings
- Firecrawl (periodic) → deep scrapes of Yelp, school sites, city calendars
- Market shifts → median price changes, inventory swings, seasonal patterns
- Life events → school enrollment opens, community calendar changes

**Processing (the sprint):**
- Parse CRMLS data → update wiki market snapshots + DB listings table
- Crawl results → enrich wiki neighborhood articles + seed DB entities/events
- Stale content detection → flag wiki articles that need refresh
- Voice synthesis → take raw data and write it in Angelique's voice

**Outputs (the deliverables):**
- TheHillPV.com pages (auto-generated from DB + wiki)
- Blog posts in Angelique's voice (from wiki content briefs)
- Market reports (auto-generated monthly from market snapshots)
- Social media content (excerpted from wiki articles)
- Open house iPad app (self-contained, offline-first, feeds CRM)
- Angel Agent knowledge (chatbot reads wiki + DB)

The wiki IS the kanban board. Each article has a freshness state. Each weekly CRMLS import is a sprint that moves items through the queue.

## Weekly Operating Rhythm

The real estate calendar drives the content cadence. Broker caravan is Tuesday. Open houses are weekends. The Hot Sheet (daily CRMLS alerts — new listings, price changes, status changes) is the daily pulse. Everything rolls up into a weekly cycle.

### The Weekly Sprint

| Day | What Happens | Angel Produces |
|-----|-------------|---------------|
| **Monday** | CRMLS weekly data closes. Hot Sheet shows weekend activity (offers accepted, price reductions, new listings from weekend showings). | Import CRMLS data. Run diff vs. last week. Flag what changed. |
| **Tuesday** | Broker caravan — agents tour new listings. This is the industry's "news day." Afternoon/evening is when agents digest what they saw. | **"What's New This Week"** — summary of new listings, price changes, status updates, notable closings. Publish to TheHillPV.com + social. |
| **Wednesday** | Market analysis day. Process the week's data into intelligence. | Update wiki market snapshot articles. Refresh neighborhood stats if significant shifts. Draft market trend commentary in Angelique's voice. |
| **Thursday** | Content production day. Turn intelligence into published content. | Blog post or neighborhood guide update. Social media content batch. Update school/community articles if new info from crawls. |
| **Friday** | Outbound day. Angelique's direct engagement. | Newsletter send (bi-weekly). Sphere-of-influence touches. Weekend open house promotion — where she'll be, what's worth seeing. |
| **Weekend** | Open houses. In-person engagement. | Open house iPad captures leads → sync to CRM Monday. Social posts from open house (just-listed, neighborhood moments). |

### Daily Pulse (Hot Sheet)

The CRMLS Hot Sheet is a daily feed of listing events — not the full weekly export, but the changes:

| Event Type | What It Means | Content Signal |
|------------|--------------|----------------|
| New Listing | Property just hit the market | Immediate: social post, add to "What's New" queue |
| Price Change | Seller adjusted (usually down) | Tuesday rollup: "X homes reduced this week" |
| Back on Market | Deal fell through | Alert: opportunity for buyers in Angelique's pipeline |
| Status Change | Active → Pending, Pending → Closed | Tuesday rollup + market snapshot update |
| Expired/Withdrawn | Listing didn't sell | Lead signal: seller may need new representation |

The Hot Sheet feeds the `listing_events` table (GRO-483 will automate ingestion from Compass Gmail alerts). For now, it's a manual awareness layer that shapes the Tuesday "What's New" summary.

### Monthly Rollups

At month-end, the weekly data accumulates into monthly deliverables:

| Deliverable | When | What |
|-------------|------|------|
| Market Trend Report | 1st week of month | Auto-generated from `market_snapshots` — median prices, DOM, inventory, YoY comparison per area |
| Neighborhood Guide Refresh | 1st week of month | Update any neighborhood articles where market data shifted > 5% |
| Content Calendar | Last week of month | Plan next month's blog topics, social themes, event coverage based on upcoming calendar |
| School Guide Check | Quarterly (Jan, Apr, Jul, Oct) | GreatSchools ratings update, enrollment changes, program updates |

### Angelique's Personal Kanban

The weekly sprint produces a short checklist Angelique (or her content assistant) acts on:

**Tuesday:**
- [ ] Review "What's New This Week" draft → approve for publish
- [ ] Note any open houses she wants to highlight (hers or notable ones to attend)
- [ ] Flag any listings she has insider context on (for voice overlay)

**Thursday:**
- [ ] Review blog post draft → approve or add personal anecdote
- [ ] Approve social media batch for the week

**Friday:**
- [ ] Review newsletter draft (bi-weekly) → approve for send
- [ ] Add personal touches to sphere-of-influence messages
- [ ] Confirm weekend open house schedule → publish "Where I'll Be"

**Monday:**
- [ ] Download CRMLS export → hand off to pipeline
- [ ] Review weekend open house lead captures → follow up

The system does the heavy lifting (data processing, drafting, scheduling). Angelique's role is editorial — approve, add personal touches, and show up in person.

## Three Content Surfaces

### 1. TheHillPV.com (Web — SEO Engine)

Flask content engine served from Cove (`angel_web_bp`). Server-rendered, fully crawlable, full SEO control.

```
TheHillPV.com
├── / (home) — "Life Above the Pacific"
├── /neighborhoods/{slug} — 10+ neighborhood guides
├── /schools — PVPUSD guide, feeder patterns, ratings
├── /market — Monthly market report (auto-generated)
├── /market/{area}/{month} — Granular snapshots
├── /streets/{slug} — Notable street profiles (future)
├── /guides/{slug} — Relocation, first-time buyer, downsizer
├── /blog/{slug} — Editorial in Angelique's voice
├── /ask — Full-page Angel chat
└── /api/chat — Agent endpoint
```

**Content velocity target:** 60+ market reports/year (monthly × 5 areas), 50+ street profiles (batch-generated), 2-4 blog posts/month, 10+ neighborhood pages.

**SEO architecture:** Server-rendered HTML (not SPA), Schema.org on every page (RealEstateListing, Place, School, FAQPage), auto-generated sitemap.xml, canonical URLs, proper heading hierarchy, minimal JS (Alpine.js only).

**What's built:** 7 neighborhood hub pages, school guide, RSS pipeline, sitemap, robots.txt, OG/Twitter meta, Schema.org JSON-LD.

### 2. Angel Agent (Conversational — Chat Widget)

The chatbot reads from both the database and the wiki to answer questions. When a visitor asks about Lunada Bay, the agent pulls listing stats from the DB AND neighborhood character from the wiki. This is what makes Angel different from a generic IDX chatbot — it has qualitative knowledge, not just data.

**Knowledge sources for the agent:**
- DB: listings (pricing, DOM, inventory), parcels (APN, geometry), events
- Wiki: neighborhood narratives, school insights, restaurant picks, market analysis
- `Angel/knowledge/`: voice profile, listing playbook, market knowledge

### 3. Open House iPad App (In-Person — Future)

A self-contained tablet experience for open houses that mirrors the Angel chat experience but optimized for in-person engagement. The visitor browses the same neighborhood knowledge, school data, and market insights that live on TheHillPV.com — but in a touch-friendly format designed for the open house table.

**Key design principles:**
- **Offline-first** — works without WiFi (open houses have unreliable connectivity)
- **Lead capture native** — visitor enters name/email/phone, syncs to CRM when back online
- **Same data, same voice** — reads from the same wiki + DB that powers the website
- **Non-intrusive** — sits on the table, visitors browse at their own pace (not a pushy sign-in sheet)
- **Contextual** — pre-loaded with the listing's neighborhood, nearby schools, recent comps

**CRM integration:** Captured leads sync to Cove DB → Compass CRM when the device reconnects. Source attribution: `source_domain: open_house`, `source_page: {address}`.

This is the bridge between digital and in-person. The online experience should feel as natural as the open house conversation, and the open house should feel as data-rich as the website.

## The Voice System

All client-facing content follows Angelique's voice (defined in `Angel/knowledge/agentic-profile.md`).

**Voice characteristics:**
- Warm authority — she knows, she doesn't guess
- Insider language — neighborhood names locals use, specific intersections not zip codes
- Opinionated but generous — clear favorites, explains why, doesn't trash competitors
- Lifestyle framing — schools aren't just rated, restaurants aren't just good
- Casual elegance — reads like a personal email, not a brochure

**Voice don'ts:** No "nestled," "boasts," "vibrant community," passive voice, generic superlatives, listicle voice.

**Current implementation:** Voice overlays stored as Python dicts in `cove/angel/voice_overlays.py` — 7 neighborhoods written. Will move to DB-backed CMS when we outgrow 7 neighborhoods.

**Future:** Voice synthesis pipeline where raw wiki content (facts, data, crawled material) gets transformed into Angelique's voice via LLM with the agentic profile as system prompt. The wiki holds the raw intelligence; the voice layer produces the published content.

## Knowledge Flow

### Weekly CRMLS Cycle

```
Week N: Jeffe exports CRMLS Top Producer CSV
    → scripts/import_crmls.py upserts to listings table
    → Compare to Week N-1: new listings, status changes, price changes, closings
    → Update wiki market snapshot articles with fresh numbers
    → Flag stale neighborhood articles if market data has shifted significantly
    → Generate monthly market report if it's a new month
```

Each weekly import is additive. The historical record only grows. A listing that was Active in Week 1 and Closed in Week 4 now has both data points — we can compute DOM, list-to-close ratio, and pricing trajectory.

### Firecrawl Enrichment Cycle

```
Periodic: Firecrawl MCP scrapes target sites
    → Yelp: restaurant ratings, hours, reviews (neighborhood entities)
    → GreatSchools: school ratings, test scores (school articles)
    → City calendars: RPV, PVE events (community events)
    → Local blogs: PV Pulse, Easy Reader (community intelligence)
    → Results parsed → wiki articles enriched → DB entities updated
```

Firecrawl is the deep web research layer. RSS handles daily news flow. Firecrawl handles periodic deep dives that update the foundational knowledge.

### RSS Daily Flow

```
Daily: flask crawl run
    → 8 Tier 1 RSS sources polled
    → New items classified by neighborhood + category
    → Stored in community_events table
    → Available for neighborhood pages and Angel Agent
```

### Content Production Flow

```
Wiki article (raw intelligence) 
    → Voice synthesis (apply Angelique's voice)
    → Editorial review (human check)
    → Published content (TheHillPV.com page, blog post, social excerpt)
    → SEO indexed → organic traffic → Angel chat → lead capture
```

## Crawl Pipeline (Implemented)

### RSS Sources (8 Tier 1)

| Source | Coverage | Categories |
|--------|----------|-----------|
| Easy Reader News | South Bay | Community, events, dining |
| Patch PV | Palos Verdes | Community, events, schools |
| Patch Manhattan Beach | Manhattan Beach | Community, events |
| Patch Hermosa Beach | Hermosa Beach | Community, events |
| Patch Redondo Beach | Redondo Beach | Community, events |
| Patch Torrance | Torrance | Community, events |
| Daily Breeze | South Bay | News, community |
| LAist | LA-wide | News, events, arts |

### Crawl Architecture

```python
# cove/angel/crawl.py
seed_sources()     # Idempotent insert of TIER_1_SOURCES
crawl_source(src)  # Parse RSS, extract fields, classify, dedup, store
crawl_all()        # Iterate all active sources, return stats
```

Classification: keyword matching against `NEIGHBORHOOD_KEYWORDS` dict (7 neighborhoods) and `CATEGORY_KEYWORDS` dict (6 categories: nature, dining, schools, arts, events, community).

Dedup: SHA-256 hash of RSS entry guid or link → stored as `source_item_id`.

### CLI Commands

```bash
flask crawl seed-sources              # Insert 8 RSS feeds
flask crawl run                       # Poll all active feeds
flask crawl seed-content              # Seed neighborhood entities/events
flask crawl seed-content -n lunada-bay  # Seed one neighborhood
flask crawl seed-schools              # Seed PVPUSD school data
```

## Content Freshness Model

Every piece of content in the system has a freshness state:

| State | Meaning | Action |
|-------|---------|--------|
| **Current** | Data verified within refresh window | None |
| **Aging** | Approaching refresh deadline | Queue for next sprint |
| **Stale** | Past refresh deadline or data contradicted | Flag for immediate update |
| **Dead** | Source gone (restaurant closed, event past) | Remove or archive |

**Refresh cadences by content type:**

| Content Type | Refresh Window | Signal Source |
|-------------|---------------|--------------|
| Market prices/stats | Monthly | CRMLS weekly import |
| Neighborhood narrative | Quarterly | Manual review + crawl |
| School ratings | Annually | GreatSchools + PVPUSD |
| Restaurant/business | Quarterly | Yelp "Permanently Closed" flag |
| Community events | Monthly | RSS + city calendars |
| Blog posts | None (evergreen unless data changes) | — |

**Stale detection signals:**
- Median price change > 5% from published figure → flag neighborhood article
- GreatSchools rating differs from published → flag school article
- Yelp "Permanently Closed" → remove from lists immediately
- RSS event date passed → archive event
- New community event not in wiki → flag for addition

## SEO Strategy

### Target Keyword Clusters

**Tier 1 — Neighborhood + Intent (highest conversion):**
"homes for sale in Lunada Bay," "Rancho Palos Verdes real estate agent," "buy a home in Rolling Hills Estates"

**Tier 2 — Neighborhood + Life Decision (relocation families):**
"best schools Palos Verdes," "moving to Palos Verdes with kids," "Palos Verdes vs Manhattan Beach families"

**Tier 3 — Local Knowledge (long-tail authority):**
"Lunada Bay neighborhood review," "PVPHS vs PVHS which is better," "Portuguese Bend horse property"

**Tier 4 — Market Intelligence (newsletter/social):**
"Palos Verdes home prices 2026," "how long do homes take to sell in PVE"

### Authority Formula

Every piece of content embeds transaction proof from the CRMLS data:
- Number of deals Angelique has closed in the area
- Median close price from her transactions
- Average DOM vs. peninsula average
- Price-per-sqft trends from historical data

This is the difference between commodity content ("Lunada Bay is beautiful") and authority content ("I've helped 12 families find their home here, median close at $3.1M, average 28 days on market").

### Technical SEO (Implemented)

- Server-rendered HTML (Flask + Jinja2, fully crawlable)
- Schema.org: RealEstateListing, Place, School, FAQPage
- Auto-generated sitemap.xml from Flask routes
- Canonical URLs, proper heading hierarchy
- Minimal JS (Alpine.js for interactivity only)
- Tailwind CSS with PostCSS build

## Content Pools (Raw Material)

### Legacy (Angel/knowledge/content-pools/)
| File | Contents | Status |
|------|----------|--------|
| `lunada-bay-raw.md` | Full web crawl — RE, schools, dining, events | Complete |
| `lunada-bay-hub.md` | Polished synthesis in Angelique's voice | Complete |
| `rpv-seed-data.py` | Structured entities/events for RPV | Complete |
| `miraleste-hub-data.py` | Structured entities/events for Miraleste | Partial |

### Brain Wiki Content Pools (19 articles, crawled 2026-04-13)
All neighborhood content pools now live in `Brain/wiki/angel-{slug}-raw.md` with 8-section structure (facts, schools, dining, shopping, events, community news, lifestyle, annual events) plus our CRMLS market data injected. Coverage: 3 PVE neighborhoods, 13 RPV neighborhoods, 2 other PV cities, 1 South Bay Tier 2 (Riviera Village). See [[Brain/projects/Angel|Angel MOC]] for full listing with links.

## Distribution Strategy

Content written once, distributed everywhere:

| Channel | Format | Cadence |
|---------|--------|---------|
| TheHillPV.com | Full articles, market reports | Continuous |
| AngeliqueLyle.com | Syndicated highlights (if LP allows) | Monthly |
| Instagram | Carousel excerpts, just-sold photos | 3-5/week |
| Email newsletter | Curated highlights + 1 deep article | Bi-weekly |
| Google Business Profile | Posts linking to articles | Weekly |
| Open house iPad | Self-contained neighborhood experience | Per event |
| Angel chatbot | Knowledge base for conversational answers | Always current |

## Related

- [[Brain/wiki/angel-architecture|Angel Architecture]] — System design, 5 layers
- [[Brain/wiki/angel-data-platform|Angel Data Platform]] — Schema, CRMLS data, APN bridge
- [[Brain/wiki/south-bay-wiki-architecture|South Bay Wiki Architecture]] — Content geography, voice definition
- [[Brain/projects/Angel|Angel MOC]] — Project hub with Linear issues
