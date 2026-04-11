---
type: project-moc
status: active
tags: [angel, real-estate, lead-generation, content-strategy, south-bay, compass]
---

# Angel

AI-powered real estate intelligence and lead generation platform for Compass agents. First deployment: Angelique Lyle, Palos Verdes Peninsula. Three components: data platform (CRMLS + county parcels via Cove), Angel Agent chatbot sidecar, and TheHillPV.com content engine. Angel is a Cove module — code lives in `Cove/cove/angel/`, knowledge lives in `Angel/knowledge/`.

## Status
Active as of April 2026. Content engine sprint shipped 2026-04-10. Foundation + Agent MVP phase. 16 Linear issues across Phase 0–2. SDDs at `docs/sdds/angel/`.

**What's live (localhost:5002):**
- 7 neighborhood hub pages with voice overlays, DB-backed entities/events, Schema.org markup
- PVPUSD school guide with feeder patterns, ratings, district stats
- RSS crawl pipeline (8 Tier 1 sources, daily via `flask crawl run`)
- SEO foundation: sitemap.xml, robots.txt, OG/Twitter meta, canonical URLs
- 43 entities + 14 events + 6 schools seeded in DB

---

## Wiki

| Article | What it covers |
|---------|---------------|
| [[Brain/wiki/south-bay-wiki-architecture|South Bay Wiki Architecture]] | Content spine, two-tier geography, voice definition, CMS strategy, seed data |

---

## Content Engine — Implementation Status (2026-04-10)

| Component | Status | Code |
|-----------|--------|------|
| RSS crawl pipeline | ✅ Running (10 items from first crawl) | `cove/angel/crawl.py`, `cli.py` |
| Neighborhood hub template | ✅ Live for all 7 neighborhoods | `templates/angel/neighborhood.html` |
| Voice overlays | ✅ All 7 neighborhoods written | `cove/angel/voice_overlays.py` |
| Seed data (entities/events) | ✅ 43 entities, 14 events seeded | `cove/angel/seed_content.py` |
| PVPUSD school guide | ✅ Full feeder patterns + ratings | `templates/angel/schools.html` |
| SEO (sitemap, robots, OG, schema) | ✅ At app root, Schema.org JSON-LD | `web_routes.py` + templates |
| GA4 + Search Console | ⏳ Waiting for domain routing | Placeholder in `base.html` |
| Valkey task queue for crawl | ⏳ Phase 2 — using CLI + external cron | — |
| CMS for voice overlays | ⏳ Future — Python dicts for now | — |

### Data Model (3 tables, migration `a7b8c9d0e1f2`)

| Table | Purpose | Records |
|-------|---------|---------|
| `local_sources` | RSS feed registry (8 Tier 1 feeds) | 8 |
| `community_events` | Events from crawl + seed | 24 (14 seeded + 10 crawled) |
| `local_entities` | Restaurants, businesses, schools | 49 (43 seeded + 6 schools) |

### CLI Commands

```bash
flask crawl seed-sources        # Insert 8 Tier 1 RSS sources
flask crawl run                 # Poll all active RSS feeds
flask crawl seed-content        # Seed all neighborhood entities/events
flask crawl seed-content -n lunada-bay  # Seed one neighborhood
flask crawl seed-schools        # Seed PVPUSD school data
```

---

## The Concept

Angelique handed us a two-page printed neighborhood guide (schools, neighborhoods, dining, coffee, shopping, golf, desserts). We're turning it into a living content platform:

- **Tier 1 — PV Peninsula (hyperlocal):** Neighborhoods, schools, events, parks/trails, community orgs
- **Tier 2 — South Bay (lifestyle):** Dining top lists, coffee, shopping districts, treats

Written in Angelique's voice — warm authority, insider knowledge, opinionated but generous. Not real estate brochure copy.

## Key People

- **Angelique Lyle** — Compass agent, 310.751.8335, angelique@compasshomes.com. The voice and brand.
- **Alejandro** — Building the content system and platform.

## Architecture

- **Cove module:** Models, blueprints, migrations, templates all live in `Cove/`
- **Knowledge repo:** Voice profiles, market knowledge, school guide in `Angel/knowledge/`
- **Agent sidecar:** Claude-powered chatbot on port 8004 (added to Cove compose)
- **TheHillPV.com:** Flask content engine served from `angel_web_bp` in Cove
- **APN bridge:** Same database as Cove — native JOINs between governance and real estate data

## Source Material

- Angel/knowledge/ — Agentic profile, compass platform, listing playbook, market knowledge, school guide, CRM pipeline, brand system
- Brain/raw/processed/angel/ — Transcribed screenshots of Angelique's printed neighborhood guide
- Angel/Top Producer - Residential*/ — CRMLS listing CSV exports
