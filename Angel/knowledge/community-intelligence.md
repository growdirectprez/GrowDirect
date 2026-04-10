# Community Intelligence System — South Bay Living Knowledge Base

## The Thesis

The relocating mom Googling at 11pm isn't searching "median home price RPV."
She's searching "things to do in Palos Verdes with kids" and "best farmers
market South Bay" and "is Lunada Bay walkable." The lifestyle intelligence
drives the neighborhood decision — the transaction data closes it.

Nobody has assembled the lifestyle layer into a structured, constantly-updated,
searchable dataset. We build that. TheHillPV.com becomes the community
intelligence platform that happens to be powered by a real estate agent.

Instead of: "Here are 5 homes for sale in Lunada Bay"

It becomes: "Here's what's happening on the Hill this week — the farmers market
has stone fruit back, PVPLC is running guided hikes Saturday, Terranea has a
new chef's table series, and by the way, here are the 3 new listings that
just hit."

That's a newsletter. That's a daily page visit. That's a reason to come back.
And every page is an SEO surface.

---

## Source Registry

### Tier 1: RSS Feeds (Automated — Daily Crawl)

These sources publish valid RSS/Atom feeds we can poll automatically.

| Source | Feed URL | Format | Update Freq | Coverage | Notes |
|--------|----------|--------|-------------|----------|-------|
| Easy Reader & Peninsula Magazine | `easyreadernews.com/feed/` | RSS 2.0 (WordPress) | Daily | MB, HB, RB, Peninsula | Confirmed active Apr 2026. Categories in feed: city + topic. Authors tagged. |
| Patch — Palos Verdes | `patch.com/california/palosverdes/feed` | RSS | Daily | RPV, PVE, RHE, RH | Events calendar + news. Structured event data. |
| Patch — Redondo Beach | `patch.com/california/redondobeach/feed` | RSS | Daily | Redondo Beach | Same Patch structure. |
| Patch — Manhattan Beach | `patch.com/california/manhattanbeach/feed` | RSS | Daily | Manhattan Beach | Same Patch structure. |
| Patch — Hermosa Beach | `patch.com/california/hermosabeach/feed` | RSS | Daily | Hermosa Beach | Same Patch structure. |
| Patch — Torrance | `patch.com/california/torrance/feed` | RSS | Daily | Torrance | Same Patch structure. |
| LAist | `laist.com/rss-feed` | RSS | Daily | LA County (filter to South Bay) | Regional news; filter by geo-tags. |
| Daily Breeze | `dailybreeze.com/feed/` | RSS | Daily | South Bay wide | Paywall on full articles; headlines + summaries are usable. |

### Tier 2: Structured Calendars (Automated — Weekly Scrape)

These sources have structured event pages (often CivicEngage, WordPress Events Calendar, or similar) that can be scraped or have iCal feeds.

| Source | URL | Platform | Coverage | Data Available |
|--------|-----|----------|----------|----------------|
| City of RPV | `rpvca.gov/Calendar.aspx` | CivicEngage | RPV city events, council meetings, rec programs | iCal subscription available. Structured: title, date, time, location, category. |
| City of Manhattan Beach | `manhattanbeach.gov/departments/parks-and-recreation/special-events/` | Custom | MB special events | Event listings with dates, descriptions. |
| City of Hermosa Beach | `hermosabeach.gov/our-community/what-s-new/calendar-of-events` | Custom | HB events | Sortable by category and department. |
| PVPUSD | `pvpusd.net/apps/events/` | SchoolWires | School events, board meetings, enrollment dates | Calendar with event details. Key dates: school year start, breaks, enrollment windows. |
| PV Peninsula Chamber of Commerce | `palosverdeschamber.com/events` + `business.palosverdeschamber.com/events/calendar` | ChamberMaster | Business events, networking, community | Searchable event list with categories. |
| South Coast Botanic Garden | `southcoastbotanicgarden.org/events` | Custom | Garden events, exhibits, classes | Major venue: DiscOasis, TROLLS exhibit, seasonal programs. |
| PVPLC (Land Conservancy) | `pvplc.org/events` | Custom | Hikes, nature walks, volunteer events, film festivals | Monthly event calendar. Active: Wild & Scenic Film Fest, guided hikes, kids programs. |
| Eventbrite — South Bay | `eventbrite.com/d/ca--rancho-palos-verdes/` | Eventbrite API | Ticketed events in the area | Eventbrite has a public API with structured event data. |
| PV Farmers Market | `palosverdesfarmersmarket` (Instagram/Facebook) | Social | Weekly Sunday market 8am-1pm, 27118 Silver Spur Rd | ~40 vendors. Est. 1994. Email: palosverdesfarmersmarket@gmail.com |
| Terranea Resort | `terranea.com/events` + `terranea.com/experiences` | Custom | Resort events, dining experiences, seasonal celebrations, wellness, kids programs | 102-acre luxury resort on former Marineland site. 9 restaurants (Mar'sel, Catalina Kitchen, Nelson's). Recurring: falconry, archery, kayaking, coastal hikes, art classes, tequila tasting, live music, yoga. Seasonal: holiday celebrations, summer programs, chef's table series. Eventbrite listings also available. Site blocks direct scraping (403) — use Eventbrite API + newsroom RSS at `terranea.com/newsroom/press-releases`. |

### Tier 3: Community Content Sites (Weekly Crawl + NLP)

These are editorial sites that aggregate and curate local events. They don't
have clean feeds but have structured HTML we can parse.

| Source | URL | What They Cover | Why It Matters |
|--------|-----|-----------------|----------------|
| South Bay by Jackie | `southbaybyjackie.com` | **The gold standard.** Daily blog, weekend guide (every Thursday), special events, recurring events, farmers markets, live music, dining. Covers El Segundo to PV. Has RSS feed + newsletter. | Most comprehensive South Bay event aggregator. If we could only watch one source, this is it. |
| Palos Verdes Pulse | `palosverdespulse.com` | Art, culture, events, lifestyle, wellness, local business profiles. PV Peninsula + South Bay focus. Multiple posts per week. Newsletter + podcast. | Peninsula-specific lifestyle content. Our direct editorial competitor for "life on the Hill." |
| Rachel Ezra (Sotheby's) | `rachelezra.com/south-bay-calendar` | Monthly events calendar for South Bay. Curated, clean, organized by date. Newsletter with market trends + events. | **Competitor agent doing exactly what we want to do.** She's a Sotheby's agent using community events as a lead-gen strategy. Proof of concept. |
| Palos Verdes Magazine | `palosverdesmagazine.com/community-calendar/` | Community events calendar. Broader lifestyle coverage. | Local print magazine with digital calendar. Established brand. |
| OurSouthBay / Southbay Magazine | `oursouthbay.com` | Events, dining, travel, real estate, arts, homes, people. High-production lifestyle content. | Premium lifestyle brand. 35K+ Instagram followers. The aspirational voice of the South Bay. |
| LocalAnchor — South Bay | `localanchor.com/south-bay-events` | Monthly event roundups | Newer aggregator; less depth but structured format. |

### Tier 4: Social/Influencer Accounts (Monitor — Weekly)

| Account | Platform | Followers | Focus | Value to Us |
|---------|----------|-----------|-------|-------------|
| @oursouthbay (Southbay Magazine) | Instagram | 35K+ | Lifestyle, events, dining, culture | Premium voice; tracks what's trending locally |
| @thesouthbayclub | Instagram | 104K | "Born & raised South Bay tour guide." Columnist for Southbay Magazine | Largest local lifestyle account. Tracks events, restaurants, hidden gems |
| @palosverdesfarmersmarket | Instagram | — | Weekly market updates, vendor features | Direct community pulse for PV |
| @dailybreezenews | Instagram | — | South Bay news, breaking stories | News layer |
| @southcoastbotanicgarden | Instagram | — | Garden events, exhibits, seasonal programs | Major PV venue |
| @pvplc | Instagram | — | Hikes, nature, conservation, volunteer events | Outdoor/family activity layer |
| South Bay Babes | Instagram/Community | — | Women's community group | Referenced by PV Pulse; community connector |

### Tier 5: Local History & Archives

| Source | URL | What They Have | Why It Matters |
|--------|-----|----------------|----------------|
| Palos Verdes Community Archives | `palosverdeshistory.org` | 7,560 items: 3,614 historical photos, 287 publications, 50 videos, 120 documents, 60 curated collections. Topics: aerial views, coastal areas, architectural heritage, historic buildings, Malaga Cove, La Venta Inn, PV Golf Club, community portraits. Interactive geomap. Run by PV Library District + Peninsula Friends of the Library. | **Content gold mine.** Every neighborhood page on TheHillPV.com gets a "History" section pulling from this archive. "Lunada Bay was originally..." with a 1940s photo = authority content nobody else has. Acknowledges Gabrielino/Tongva peoples as traditional land caretakers — we should too. No RSS/blog, but the collection is browsable and linkable. |
| Terranea / Marineland History | `terranea.com/resort/history` + `palosverdesmagazine.com/marineland-of-the-pacific/` + `palosverdespulse.com` (Phil Wahba article) | Marineland of the Pacific opened 1954 (one year before Disneyland), architect William Pereira, world's largest oceanarium. Closed 1987 (SeaWorld acquisition). Site abandoned ~20 years. Lowe Enterprises developed 1998-2009. Terranea opened June 2009. 102 acres, Mediterranean architecture by Hill Glazier + Scheurer Architects. Vanderlip connection: Frank Vanderlip purchased 16,000 acres in 1913, first homes 1924. | Marineland → Terranea transformation is one of the best stories on the Peninsula. Content for neighborhood pages (RPV/Portuguese Bend), "From the Archives" features, and the community intelligence layer. Connects to Vanderlip history which also feeds Malaga Cove Plaza narrative. |

### Tier 6: Competitor Agent Blogs (Monitor — Weekly via RSS)

LP supports RSS feed **consumption** — agents can pull external RSS into their
LP blog. LP does **NOT** provide outgoing RSS feeds from agent blogs.

**Workaround for monitoring competitors:** Scrape their blog listing pages
weekly. Most LP sites follow predictable URL patterns:
`{agent-domain}.com/blog/` with article links.

| Agent/Team | Domain | Brokerage | Why Monitor |
|------------|--------|-----------|-------------|
| Accardo Real Estate Associates | `accardorealestate.com/blog` | Compass | Angelique's own team. See what they publish. |
| Rachel Ezra | `rachelezra.com` | Sotheby's | Actively doing the community calendar play. |
| Top PVE agents | TBD — pull from Compass directory | Various | Content gap analysis: what are they writing? What are they missing? |
| Top RPV agents | TBD — pull from Compass directory | Various | Same. |
| Top MB/HB/RB agents | TBD | Various | Beach cities comparison content gaps. |

---

## LP RSS: What's Actually Possible

Based on Luxury Presence documentation:

**Inbound RSS (LP consumes external feeds):**
- LP sites CAN pull in external RSS feeds to auto-populate a blog section
- This means: TheHillPV.com content → RSS feed → AngeliqueLyle.com (LP) auto-publishes summaries
- Format: standard RSS 2.0 feed URL pasted into LP dashboard settings
- Use case: Write once on TheHillPV.com, syndicate to LP flagship via RSS

**Outbound RSS (LP produces feeds):**
- LP does **NOT** provide outgoing RSS feeds from agent blogs
- Their help article "How to Share Blog Content Without an Outgoing RSS Feed" confirms this limitation
- Workaround: manual scraping of competitor LP sites, or using LP's suggested sharing methods

**The play:** TheHillPV.com (Flask) generates its own RSS feed (trivial — it's
our code). That feed gets consumed by AngeliqueLyle.com (LP) via their RSS
blog integration. Content written once, published on both domains.
Community intelligence content from our crawler → TheHillPV.com → RSS →
AngeliqueLyle.com. One content engine, two distribution points.

---

## System Architecture

### Data Model

```
local_sources
├── id (UUID)
├── name ("Easy Reader News")
├── source_type (rss | ical | scrape | api | social)
├── url ("easyreadernews.com/feed/")
├── scrape_config (JSONB — CSS selectors, pagination rules)
├── schedule (cron expression — "0 6 * * *" = daily 6am)
├── last_crawled_at (timestamp)
├── last_success_at (timestamp)
├── items_found (integer — running count)
├── coverage_area (text[] — ["manhattan_beach", "hermosa_beach"])
├── categories (text[] — ["news", "events", "dining"])
├── is_active (boolean)
├── created_at / updated_at

community_events
├── id (UUID)
├── source_id (FK → local_sources)
├── source_url (original URL of the event/article)
├── source_item_id (guid from RSS, or hash of URL for dedup)
├── title
├── description (text)
├── event_date (date — NULL for evergreen content)
├── event_end_date (date — NULL for single-day)
├── event_time (time)
├── recurrence (text — "weekly_sunday", "monthly_first_saturday", NULL)
├── location_name ("South Coast Botanic Garden")
├── location_address
├── location_lat / location_lng
├── neighborhood (text — mapped to our neighborhood taxonomy)
├── city (text)
├── category (text — events, dining, schools, nature, arts, sports, community)
├── subcategory (text — farmers_market, hike, concert, fundraiser, etc.)
├── tags (text[])
├── image_url (text)
├── is_recurring (boolean)
├── is_featured (boolean — editorial pick)
├── embedding (Vector(1024) — for semantic search via Angel chatbot)
├── expires_at (timestamp — auto-hide after event passes)
├── created_at / updated_at

content_opportunities
├── id (UUID)
├── detected_from (FK → local_sources — which competitor/source revealed the gap)
├── opportunity_type (keyword_gap | event_coverage | seasonal | trending)
├── title ("Nobody's covering Portuguese Bend trail opening")
├── keyword (text — the SEO target)
├── search_volume (integer)
├── neighborhood (text)
├── our_coverage_status (none | partial | published)
├── our_content_url (text — TheHillPV.com URL if we've covered it)
├── priority_score (decimal — from authority matrix)
├── notes (text)
├── created_at / updated_at

local_entities
├── id (UUID)
├── entity_type (restaurant | park | school | venue | business | trail)
├── name
├── address
├── neighborhood
├── city
├── lat / lng
├── category (text)
├── tags (text[])
├── description (text)
├── website (text)
├── phone (text)
├── hours (JSONB)
├── source_url (text — where we learned about it)
├── embedding (Vector(1024))
├── is_active (boolean)
├── first_seen_at / last_seen_at
├── created_at / updated_at
```

### Crawl Pipeline

```
┌─────────────────────────────────────────────────────┐
│                  CRAWL SCHEDULER                     │
│  Valkey-backed cron (reuses Cove task queue)         │
│  Reads local_sources.schedule for each source        │
│  Dispatches crawl jobs to workers                    │
└──────────────┬──────────────────────────────────────┘
               │
    ┌──────────┼──────────────┐
    ▼          ▼              ▼
┌────────┐ ┌────────┐ ┌────────────┐
│  RSS   │ │ Scrape │ │    API     │
│ Parser │ │ Worker │ │  Client    │
│        │ │        │ │            │
│feedparser│ │BeautifulSoup│ │Eventbrite │
│ stdlib │ │ + rules│ │ Google Cal │
└───┬────┘ └───┬────┘ └─────┬──────┘
    │          │             │
    ▼          ▼             ▼
┌─────────────────────────────────────────────────────┐
│              NORMALIZE + CLASSIFY                    │
│                                                      │
│  1. Dedup (source_item_id or URL hash)              │
│  2. Geo-classify (map to neighborhood taxonomy)      │
│  3. Category classify (event type, topic)            │
│  4. Extract entities (venue → local_entities)        │
│  5. Generate embedding (Ollama qwen3-embedding:8b)   │
│  6. Detect opportunities (gap analysis vs our content)│
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│              COMMUNITY INTELLIGENCE DB               │
│  community_events + local_entities +                 │
│  content_opportunities                               │
│  (tables in cove database — Angel is a Cove module)  │
└──────────────┬──────────────────────────────────────┘
               │
    ┌──────────┼───────────────┬────────────────┐
    ▼          ▼               ▼                ▼
┌────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
│TheHill │ │  Angel   │ │ Weekly   │ │  Content     │
│PV.com  │ │ Chatbot  │ │Newsletter│ │ Opportunity  │
│        │ │          │ │          │ │  Alerts      │
│/events │ │community_│ │ Auto-gen │ │              │
│/this-  │ │search    │ │ "This    │ │ "Nobody is   │
│ week   │ │tool      │ │  Week on │ │  writing     │
│/calendar│ │          │ │  the     │ │  about X"    │
│        │ │"What's   │ │  Hill"   │ │              │
│RSS feed│ │happening │ │          │ │ → content    │
│ → LP   │ │this wknd"│ │ → email  │ │   brief      │
└────────┘ └──────────┘ └──────────┘ └──────────────┘
```

### Angel Chatbot: New Tool

```
community_search
  Input: query (text), date_range (optional), neighborhood (optional),
         category (optional)
  Method: semantic search on community_events.embedding +
          filters on date/neighborhood/category
  Output: top 5-10 matching events with details

  Example queries:
  - "What's happening this weekend in PVE?"
  - "Any farmers markets near Lunada Bay?"
  - "Family activities in Palos Verdes this month"
  - "New restaurants in the South Bay"
  - "When does school start for PVPUSD?"
```

### Content Auto-Generation

The system generates three types of content automatically:

**1. Weekly Roundup — "This Week on the Hill"**
- Pulls community_events for next 7 days
- Groups by: outdoors, dining, arts, schools, community
- Generates in Angelique's voice (warm, local, first-person)
- Publishes to TheHillPV.com/this-week
- RSS → AngeliqueLyle.com blog auto-update
- Email newsletter version

**2. Monthly Event Calendar**
- TheHillPV.com/events/2026/04
- Structured calendar view with category filters
- schema.org Event markup on every item
- SEO target: "Palos Verdes events [month] [year]"

**3. Seasonal Content Triggers**
- System knows recurring patterns from historical data:
  - Jan-Mar: school enrollment content (PVPUSD registration)
  - Apr: Earth Day events, spring hiking (PVPLC)
  - May: graduation content, summer planning
  - Jun-Aug: beach events, surf festivals, summer camps
  - Sep: back to school, fall hiking
  - Oct: Halloween (trick-or-treating guides by neighborhood)
  - Nov-Dec: holiday events, Terranea holiday programs, light displays
- Triggers content_opportunity records 4-6 weeks before each season

---

## Neighborhood Taxonomy

Events and entities map to this controlled vocabulary:

```
peninsula:
  - lunada_bay
  - malaga_cove
  - valmonte
  - montemalaga
  - portuguese_bend
  - point_vicente
  - miraleste
  - rolling_hills
  - rolling_hills_estates
  - peninsula_center    # shopping/dining hub

beach_cities:
  - manhattan_beach
  - hermosa_beach
  - redondo_beach_north
  - redondo_beach_south  # Riviera Village
  - riviera_village

torrance:
  - hollywood_riviera
  - old_torrance
  - south_torrance

harbor:
  - san_pedro
  - wilmington

# Special zones (span multiple neighborhoods)
the_strand          # MB → HB → RB coastal path
south_coast_botanic_garden
terranea_resort
trump_national
point_fermin
```

---

## Competitor Content Gap Analysis

### How It Works

1. Crawl competitor agent blogs weekly (scrape listing pages)
2. Extract: title, topic, neighborhood, publish date
3. Compare to our content index (TheHillPV.com published pages)
4. Flag gaps: topics they cover that we don't
5. Flag opportunities: topics NOBODY covers (detected from event data)
6. Generate content_opportunity records with priority scores

### Rachel Ezra (Sotheby's) — Case Study

She's already doing a version of this play:
- Monthly South Bay events calendar on her agent site
- Newsletter with "local events + market trends + featured properties"
- She's a Sotheby's agent using community events as lead-gen

**What she's doing right:** Combining lifestyle content with real estate
**What she's missing:** It's manual curation, not data-driven. No chatbot.
No structured data. No SEO infrastructure. No auto-generation.

We build the automated, data-driven version of what she does by hand.

---

## Rolling Window + Campaign History

### The Rolling Window

The system maintains a **6-month rolling window** of community intelligence:

- **Past 3 months:** What happened. Performance data on our content about those
  events (traffic, leads generated, time-on-page). Which event-driven content
  converted? What seasonal patterns emerged?

- **Current month:** What's happening now. Active events calendar. "This Week"
  roundup. Real-time chatbot answers.

- **Next 2 months:** What's coming. Seasonal triggers firing content briefs.
  Events we know about from advance listings. Content planned and in production.

### Campaign History

Every piece of content generated from community intelligence gets tracked:

```
content_campaigns
├── id (UUID)
├── content_opportunity_id (FK — what triggered this)
├── title ("Palos Verdes Farmers Market — Your Sunday Morning Guide")
├── content_type (blog | event_page | newsletter | social_post)
├── published_url
├── published_at
├── source_events (UUID[] — which community_events fed this)
├── target_keywords (text[])
├── neighborhood (text)
├── season (text — "spring_2026", "back_to_school_2026")
│
│ — Performance (updated by analytics pipeline) —
├── page_views (integer)
├── avg_time_on_page (interval)
├── leads_generated (integer)
├── leads_captured (UUID[] — FK to leads table)
├── search_rank (JSONB — {keyword: rank} snapshots)
├── backlinks_earned (integer)
│
│ — Learning —
├── what_worked (text — editorial notes after performance review)
├── reuse_template (boolean — flag if this is a repeatable format)
├── next_refresh_date (date — when to update/republish)
├── created_at / updated_at
```

### The Learning Loop

Monthly review process (automated report, human review):

1. **What content performed?** Top 10 pages by traffic + leads from community
   intelligence content
2. **What events drove engagement?** Cross-reference community_events with
   page views and chatbot queries
3. **What gaps remain?** Content opportunities that went unaddressed
4. **What's seasonal?** Flag content that should be refreshed for next year
   (trick-or-treat guide, school enrollment guide, summer camp roundup)
5. **What should we double down on?** Categories or neighborhoods where
   community content → leads conversion is highest

This creates a flywheel: crawl → publish → measure → learn → crawl smarter.

---

## Implementation Priority

### Phase 0.5 (Before Agent MVP — build during data import week)

1. **Set up RSS polling for Tier 1 sources** — 8 feeds, daily cron, write to
   community_events. This is the cheapest win: ~2 hours of work, immediately
   populates the events database.

2. **Scrape South Bay by Jackie recurring events** — one-time parse of their
   ongoing events page to seed the farmers markets, live music, weekly events.

3. **Create neighborhood taxonomy** — controlled vocabulary above, used as
   classification target for all crawled content.

4. **Add `community_search` tool to Angel Agent** — even before TheHillPV.com
   exists, the chatbot can answer "what's happening this weekend" from RSS data.

### Phase 1.5 (During Content Engine build)

5. **TheHillPV.com /events and /this-week pages** — auto-generated from
   community_events table. Schema.org Event markup. Calendar view.

6. **RSS output feed from TheHillPV.com** — consumed by LP to auto-populate
   AngeliqueLyle.com blog section.

7. **Weekly newsletter generation** — "This Week on the Hill" from same data.

8. **Competitor blog monitoring** — scrape 10-15 agent blog listing pages,
   feed into content_opportunities.

### Phase 2.5 (Post-launch optimization)

9. **Eventbrite API integration** — structured ticketed events.

10. **Social monitoring** — Instagram scraping for @oursouthbay,
    @thesouthbayclub, @palosverdesfarmersmarket to detect trending topics.

11. **Campaign tracking + learning loop** — connect GA4 to content_campaigns,
    build monthly performance reports.

12. **Seasonal content automation** — trigger content briefs 4-6 weeks before
    recurring seasonal events based on prior year data.

---

## What This Changes About the Pitch

**Before (current pitch):** "I'll build you an AI chatbot that answers
questions about PV real estate."

**After (community intelligence pitch):** "I'll make you the information hub
for life on the Peninsula. When someone Googles 'what's happening in Palos
Verdes this weekend' or 'best farmers market South Bay' or 'PVPUSD school
calendar' — they find you. Not Patch, not Sotheby's, not South Bay by Jackie.
You. And when they're ready to buy, you're already the person they trust."

The chatbot is just the interface. The community intelligence engine is the moat.

---

*Community Intelligence System v1 — Angel / GrowDirect Inc. — 2026-04-06*
