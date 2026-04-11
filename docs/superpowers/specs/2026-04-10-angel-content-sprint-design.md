# Angel Content Sprint — Design Spec

**Date:** 2026-04-10
**Issues:** GRO-491, GRO-492, GRO-468, GRO-469
**Milestone:** Phase 2 — Content Engine & Integration

---

## Overview

Four issues wired together: RSS crawl pipeline seeds the database, neighborhood
hub and school guide templates consume it, SEO ensures it's crawlable. All work
is in the Cove repo (Angel is a Cove module).

---

## 1. GRO-491 — RSS Crawl Pipeline

### What

Automated crawl pipeline that polls 8 Tier 1 RSS feeds daily and writes new
items to `community_events`.

### Implementation

**New file:** `Cove/cove/angel/crawl.py`

```python
# Core functions:
def seed_sources(db_session) -> int
    """Insert 8 Tier 1 RSS sources into local_sources table."""

def crawl_source(source: LocalSource) -> list[CommunityEvent]
    """Parse RSS feed, normalize entries, dedup by source_item_id."""

def crawl_all(db_session) -> dict
    """Iterate active sources, crawl each, return stats."""

def classify_item(entry) -> tuple[str, str, str]
    """Return (category, subcategory, neighborhood) for an RSS entry.
    Uses keyword matching against neighborhood taxonomy and category terms."""
```

**Dependencies:** `feedparser` (add to requirements.txt)

**Dedup strategy:** `source_item_id` = RSS `<guid>` or SHA-256 of entry URL.
Before INSERT, check if `source_item_id` already exists for that `source_id`.

**Geo-classification:** Keyword scan of title + description against neighborhood
taxonomy from `community-intelligence.md`. Default to `palos_verdes` if no match.

**Category classification:** Keyword matching:
- "hike|trail|canyon|bird|volunteer" → nature
- "restaurant|cafe|coffee|food|dining" → dining
- "school|student|pvpusd|enrollment" → schools
- "concert|art|gallery|film|theater" → arts
- "market|fair|festival|parade" → events
- Default → community

**8 Tier 1 Sources:**

| Name | URL | Schedule |
|------|-----|----------|
| Easy Reader News | easyreadernews.com/feed/ | daily |
| Patch PV | patch.com/california/palosverdes/feed | daily |
| Patch Manhattan Beach | patch.com/california/manhattanbeach/feed | daily |
| Patch Hermosa Beach | patch.com/california/hermosabeach/feed | daily |
| Patch Redondo Beach | patch.com/california/redondobeach/feed | daily |
| Patch Torrance | patch.com/california/torrance/feed | daily |
| Daily Breeze | dailybreeze.com/feed/ | daily |
| LAist | laist.com/rss-feed | daily |

**CLI entry point:** `flask crawl seed-sources` and `flask crawl run` via Click
CLI group registered in the app factory.

**No Valkey cron yet.** Phase 1 uses `flask crawl run` invoked by external cron
(Docker crontab or host crontab). Valkey-backed task queue is Phase 2.

### Files Changed

- `Cove/cove/angel/crawl.py` (new)
- `Cove/cove/angel/cli.py` (new — Click CLI group)
- `Cove/cove/__init__.py` (register CLI)
- `Cove/requirements.txt` (add feedparser)

---

## 2. GRO-492 — Neighborhood Hub Template + Lunada Bay Launch

### What

Wire the `neighborhood()` route to query DB for entities and events. Seed
Lunada Bay data. Replace template stubs with real content sections.

### Data Seeding

**New file:** `Cove/cove/angel/seed_lunada_bay.py`

Seeds from `lunada-bay-raw.md` content pool:

- **local_entities** (entity_type=restaurant): Java Wave, Black Bamboo Sushi,
  Salsa Verdes, Lunada Kitchen, Lunada Creamery, Lunada Market, Yellow Vase,
  Nelson's, mar'sel, Terra Mia, Neptune's Frozen Treats, Avenue Italy (~12 entities)
- **local_entities** (entity_type=business): Lunada Bay Hardware, Lunada Bay
  Barbers, PV Drugstore, Claydon Jewelers (~4 entities)
- **local_entities** (entity_type=school): Lunada Bay Elementary, PV Intermediate,
  PV High School (~3 entities)
- **community_events**: Whale of a Day, PVPLC volunteer days, Trolls exhibit,
  Earth Day, Farmers Market (recurring), Summer Concert Series (~10 events)

All entities get `neighborhood = "lunada_bay"`. Schools get additional
structured data in a new `ratings` JSONB column (or in `tags` array as
`greatschools:8`, `niche:A-`).

**School ratings approach:** Store in `description` field as structured text, or
add metadata to `tags` array. No schema change needed — use existing columns.

**Voice overlay content:** Stored as a Python dict in the route module keyed by
neighborhood slug. Contains intro paragraphs, section commentary, closing.
Moves to a `neighborhood_content` table later when we have a CMS.

### Route Changes (`web_routes.py`)

```python
@angel_web_bp.route("/neighborhoods/<slug>")
def neighborhood(slug: str):
    nbhd = _NEIGHBORHOODS_BY_SLUG.get(slug)
    if not nbhd:
        abort(404)

    # Query DB for this neighborhood's data
    restaurants = LocalEntity.query.filter_by(
        neighborhood=slug.replace("-", "_"), entity_type="restaurant", is_active=True
    ).all()
    businesses = LocalEntity.query.filter_by(
        neighborhood=slug.replace("-", "_"), entity_type="business", is_active=True
    ).all()
    schools = LocalEntity.query.filter_by(
        neighborhood=slug.replace("-", "_"), entity_type="school", is_active=True
    ).all()
    events = CommunityEvent.query.filter(
        CommunityEvent.neighborhood == slug.replace("-", "_"),
        or_(
            CommunityEvent.event_date >= date.today(),
            CommunityEvent.is_recurring == True,
        ),
    ).order_by(CommunityEvent.event_date).limit(10).all()

    voice = VOICE_OVERLAYS.get(slug, {})

    return render_template(
        "angel/neighborhood.html",
        neighborhood=nbhd,
        neighborhoods=NEIGHBORHOODS,
        restaurants=restaurants,
        businesses=businesses,
        schools=schools,
        events=events,
        voice=voice,
    )
```

### Template Changes (`neighborhood.html`)

Replace each stub section:

- **Intro:** Voice overlay paragraphs (from `voice.intro`)
- **Real Estate:** Market stats from voice overlay (static for now, moves to
  `market_snapshots` table later)
- **Schools:** Loop `schools` list, show ratings from tags/description
- **Dining:** Loop `restaurants`, show name/cuisine/description/hours
- **Events:** Loop `events`, show title/date/location/description
- **Community News:** Voice overlay section (static text)
- **Further Reading:** Voice overlay links list

### Slug-to-Taxonomy Mapping

URL slugs use hyphens (`lunada-bay`), DB taxonomy uses underscores (`lunada_bay`).
Conversion: `slug.replace("-", "_")` in route, reverse in template URL generation.

### Files Changed

- `Cove/cove/angel/seed_lunada_bay.py` (new)
- `Cove/cove/angel/web_routes.py` (modified — add DB queries, voice overlays)
- `Cove/templates/angel/neighborhood.html` (modified — replace stubs)

---

## 3. GRO-468 — PVPUSD School Guide

### What

Build out `schools.html` with real data: feeder patterns, ratings, enrollment,
neighborhood cross-reference.

### Data Approach

School data structured as dicts in the route, with Schema.org `School` markup
in the template. Schools also seeded into `local_entities` (entity_type=school)
for the neighborhood pages.

### Route Changes

```python
PVPUSD_SCHOOLS = {
    "high_schools": [
        {
            "name": "Palos Verdes High School",
            "mascot": "Sea Kings",
            "grades": "9-12",
            "greatschools": 10,
            "niche": "A+",
            "graduation_rate": 97,
            "avg_sat": 1330,
            "avg_act": 29,
            "neighborhoods": ["lunada_bay", "malaga_cove"],
            "feeders": {
                "intermediate": "Palos Verdes Intermediate",
                "elementary": ["Lunada Bay Elementary", "Malaga Cove Intermediate feeder schools"],
            },
        },
        # ... PVPHS, Rancho del Mar
    ],
    "intermediate": [...],
    "elementary": [...],
    "district": {
        "total_schools": 19,
        "total_students": 10300,
        "ca_ranking": "top 5%",
        "enrollment_note": "2026-27 Virtual Line opened Feb 2, 2026",
    },
}
```

### Template Sections

1. **District Overview** — 19 schools, 10,300 students, top 5% in CA
2. **Feeder Patterns** — Visual flow: Elementary → Intermediate → High School
   (two tracks: PVHS Sea Kings / PVPHS Panthers). CSS-based flow diagram, not
   SVG — Tailwind flexbox with connecting lines.
3. **School Cards** — Grid of all schools with level badge, ratings, key stats
4. **Schools by Neighborhood** — Cross-reference linking to neighborhood hub pages
5. **Enrollment Info** — Current enrollment cycle, Virtual Line link
6. **Voice Overlay** — Angelique's school commentary from hub page
7. **CTA** — Ask Angelique

### Files Changed

- `Cove/cove/angel/web_routes.py` (modified — add school data, pass to template)
- `Cove/templates/angel/schools.html` (modified — replace stubs with data)

---

## 4. GRO-469 — SEO Technical Setup

### What

Technical SEO foundation: sitemap, robots.txt, meta tags, structured data,
canonical URLs.

### Implementation

**Sitemap (`/sitemap.xml`):**
New route in `angel_web_bp` that auto-generates XML sitemap from all content
routes. Uses `url_for()` to enumerate pages. Sets `Content-Type: application/xml`.

```python
@angel_web_bp.route("/sitemap.xml")
def sitemap():
    pages = []
    # Static pages
    for rule in ["home", "neighborhoods", "schools", "ask"]:
        pages.append(url_for(f"angel_web.{rule}", _external=True))
    # Dynamic pages
    for nbhd in NEIGHBORHOODS:
        pages.append(url_for("angel_web.neighborhood", slug=nbhd["slug"], _external=True))
    return render_template("angel/sitemap.xml", pages=pages), 200, {"Content-Type": "application/xml"}
```

**robots.txt (`/robots.txt`):**
```
User-agent: *
Allow: /
Sitemap: https://thehillpv.com/sitemap.xml
```

**Meta tags (base.html changes):**
- Add `{% block og_tags %}` with Open Graph (og:title, og:description, og:image, og:url, og:type)
- Add Twitter Card meta tags (twitter:card, twitter:title, twitter:description)
- Add canonical URL: `<link rel="canonical" href="{% block canonical %}{{ request.url }}{% endblock %}">`

**Schema.org structured data:**
- `neighborhood.html`: `LocalBusiness` for each restaurant, `School` for schools,
  `Event` for events
- `schools.html`: `School` for each school, `EducationalOrganization` for PVPUSD
- `home.html`: `RealEstateAgent` for Angelique

Rendered as `<script type="application/ld+json">` blocks.

**GA4 + Search Console:**
- GA4: Add measurement ID slot in base.html (`{% block analytics %}`)
- Search Console: DNS TXT verification (Cloudflare) — manual step, flagged for user

### Files Changed

- `Cove/templates/angel/base.html` (modified — OG tags, canonical, analytics slot)
- `Cove/templates/angel/sitemap.xml` (new)
- `Cove/templates/angel/robots.txt` (new)
- `Cove/templates/angel/neighborhood.html` (modified — Schema.org JSON-LD)
- `Cove/templates/angel/schools.html` (modified — Schema.org JSON-LD)
- `Cove/cove/angel/web_routes.py` (modified — sitemap + robots routes)

---

## Execution Order

1. **GRO-491** first — creates crawl infrastructure and seeds sources
2. **GRO-492** second — seeds Lunada Bay data, wires neighborhood template
3. **GRO-468** third — builds school guide (uses same entity data)
4. **GRO-469** last — adds SEO layer on top of all content pages

Steps 1-2 can be partially parallelized (crawl pipeline is independent of
template work). Step 4 depends on 2-3 being complete (needs content pages to
add structured data to).

---

## Dependencies

- `feedparser` package (GRO-491)
- Database must be up with community intelligence tables migrated
- No new migrations needed — all three tables already exist

## Out of Scope

- Valkey-backed task queue (future — use CLI + external cron for now)
- CMS for voice overlays (future — use Python dicts for now)
- GA4 measurement ID and Search Console verification (manual config steps)
- Phase 2/3 scrapers for Tier 2/3 sources
- Embedding generation for events
