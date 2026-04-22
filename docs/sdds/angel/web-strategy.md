# Angel Web Strategy

> **Type:** App Service
> **Status:** Active — TheHillPV.com skeleton live, 7 neighborhood pages, schools page, SEO routes
> **Namespace:** angel
> **Date:** 2026-04-06 (ops upgrade 2026-04-13)
> **Author:** ALX (COO) / Jeffe (CEO)
> **Dependencies:** Angel data platform, Angel Agent sidecar, Cove Flask

**Wiki:** [[Brain/wiki/south-bay-wiki-architecture|South Bay Wiki Architecture]] · [[Brain/wiki/angel-content-engine|Angel Content Engine]] · [[Brain/wiki/angel-ninja-selling|Angel Ninja Selling]] · [[Brain/projects/Angel|Angel MOC]]
**Parent:** [[docs/sdds/angel/angel-overview|Angel Overview]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[Canary/docs/profiles/ops/Art|Art]] · **Operator role:** [[Canary/docs/profiles/ops/Jess|Jess]]

---

## Purpose

Angel's web strategy uses three domains with distinct roles that funnel traffic
toward a single outcome: a phone conversation between the visitor and Angelique
Lyle. TheHillPV.com is the data-driven content engine built on Flask.
AngeliqueLyle.com is the luxury flagship on Luxury Presence. OwnPalosVerdes.com
is a recovery project.

---

## Dependencies

| Dependency | Type | Required |
|------------|------|----------|
| Cove Flask (port 5002) | Host app — Angel web blueprints registered here | Yes |
| PostgreSQL (`cove` database) | Content queries (listings, entities, events, snapshots) | Yes |
| Angel Agent sidecar (port 8004) | Chat proxy for `/angel/chat` endpoints | For chat features |
| Cloudflare | DNS + CDN for TheHillPV.com | For production |
| Luxury Presence | AngeliqueLyle.com hosting (external) | External — not our infra |

---

## Data Flow & PII Map

### What Enters

| Source | Data | PII Content |
|--------|------|------------|
| Visitor HTTP request | URL, IP address, User-Agent, referrer | IP address (P1 — logged in access logs) |
| Angel chat widget (JS) | Visitor messages, conversation context | Phone number if lead captured (sensitive) |
| LP webhook (planned) | Lead contact info from AngeliqueLyle.com forms | Name, email, phone (sensitive) |

### What's Stored

| Field | Location | Classification | Encryption |
|-------|----------|---------------|------------|
| Visitor IP address | Web server access logs | **sensitive** | **Plaintext in logs (P1)** |
| Lead phone (via chat) | `leads` table (planned) | **sensitive** | **Not yet implemented (P0)** |
| Neighborhood content | `local_entities`, `community_events` | public | N/A |
| Voice overlay text | `voice_overlays.py` (hardcoded) | public | N/A |

### What Exits

| Destination | Data | Notes |
|-------------|------|-------|
| Visitor browser | Rendered HTML pages with market data, neighborhood info | Public — no PII |
| Angel Agent sidecar | Chat messages proxied to `/chat` endpoint | May contain visitor PII |
| Search engine crawlers | Sitemap.xml, robots.txt, structured data | Public |

---

## API Contract

### Web Routes (angel_web_bp, prefix: `/angel/web`)

| Route | Method | Auth | Purpose |
|-------|--------|------|---------|
| `/angel/web/` | GET | None | TheHillPV.com home page |
| `/angel/web/neighborhoods/` | GET | None | Neighborhood index |
| `/angel/web/neighborhoods/<slug>` | GET | None | Individual neighborhood page with DB data |
| `/angel/web/schools` | GET | None | PVPUSD school guide |
| `/angel/web/ask` | GET | None | Full-page Angel chat experience |

### Chat Routes (angel_chat_bp)

| Route | Method | Auth | Purpose |
|-------|--------|------|---------|
| `/angel/chat` | POST | None | Proxy to Angel Agent sidecar |
| `/angel/chat/health` | GET | None | Check sidecar reachability |

### SEO Routes (registered at app level)

| Route | Method | Purpose |
|-------|--------|---------|
| `/sitemap.xml` | GET | Auto-generated sitemap from route registry |
| `/robots.txt` | GET | Crawler directives with sitemap reference |

---

## Three-Domain Strategy

### TheHillPV.com — Silent SEO Engine (Flask)

**Built and live.** Blueprint on Cove Flask (port 5002). Serves data-driven
neighborhood pages, school guide, and chat experience.

**Current routes:**
- Home, 7 neighborhood pages (Lunada Bay, Malaga Cove, Valmonte, Miraleste, RPV, Rolling Hills, Rolling Hills Estates)
- Schools page with PVPUSD data
- Ask page (full-page chat)
- Sitemap.xml and robots.txt

**Content sources:** `local_entities` table (restaurants, businesses, schools),
`community_events` table (RSS-sourced), `voice_overlays.py` (Angelique's voice text),
`seed_content.py` (PVPUSD school data).

**Planned routes (not yet built):**
- `/market/{area}/{month}` — auto-generated market reports from `market_snapshots`
- `/streets/{slug}` — street-level profiles from listing data
- `/guides/{slug}` — relocation guides
- `/blog/{slug}` — editorial content

### AngeliqueLyle.com — Flagship (Luxury Presence)

External platform. Content refresh needed. Angel widget integration TBD
(requires LP script injection investigation).

### OwnPalosVerdes.com — Reclamation

Domain compromised with spam content. Recovery plan: cleanup, reconsideration
request, evaluate after 90 days.

---

## SEO Architecture

**Target keyword clusters:**
- "Palos Verdes homes for sale" / "Rancho Palos Verdes real estate"
- "PV peninsula neighborhoods" / "Lunada Bay homes"
- "PVPUSD schools ranking" / "Palos Verdes schools"
- "Palos Verdes market report" / "RPV home prices"

**Technical SEO (implemented):**
- Server-rendered HTML (Flask + Jinja2, not SPA) — fully crawlable
- Sitemap.xml auto-generated from content routes
- robots.txt with sitemap reference
- Minimal JS (Alpine.js only for interactivity), Tailwind CSS

**Technical SEO (planned):**
- Schema.org structured data (RealEstateListing, Place, School)
- Meta descriptions auto-generated from data summaries
- Canonical URLs, proper heading hierarchy

---

## Lead Flow

```
Visitor lands on any domain
    │
    ├── Reads content (page views, time on page)
    │
    ├── Engages with Angel chatbot
    │   ├── Asks about property → parcel_lookup tool
    │   ├── Asks about market → market_stats tool
    │   └── Ready to act → capture_lead tool
    │       │
    │       ▼
    │   Lead captured: phone, interest, property context
    │       │
    │       ├── SMS to Angelique (planned)
    │       ├── Lead → Angel DB (with source attribution)
    │       └── Async: Compass CRM sync (planned)
    │
    └── Clicks CTA → AngeliqueLyle.com (tracked referral)
```

**Attribution fields (planned):**
- `source_domain` — thehillpv.com, angeliquelyle.com, ownpalosverdes.com
- `source_page` — specific URL when visitor engaged
- `source_referrer` — organic, social, direct, email
- `conversation_turns` — chat depth before capture

---

## Operations

### Startup Sequence

No separate startup — web routes are part of Cove Flask app factory.
Angel blueprints registered in `cove/__init__.py`.

### Health Checks

- `GET /health` — Cove-level health (DB + Valkey)
- `GET /angel/chat/health` — Angel Agent sidecar reachability
- `GET /sitemap.xml` — confirms route registry is functional

### Failure Modes

| Failure | Behavior | Recovery |
|---------|----------|----------|
| DB down | Neighborhood pages fail (500), home page may fail | Restart PostgreSQL |
| Sidecar down | Chat returns 503; all other pages unaffected | Restart angel-agent container |
| Empty DB tables | Pages render with empty data sections (no crash) | Run seed commands: `flask crawl seed-content` |
| Missing voice overlay | Page renders without voice section (graceful) | Add overlay to `voice_overlays.py` |

### Monitoring

| Metric | Alert Threshold |
|--------|----------------|
| Page response time | > 2 seconds (server-rendered, should be < 500ms) |
| 5xx error rate | > 1% of requests |
| Sitemap generation | Fails to return valid XML |
| Chat proxy latency | > 30 seconds per request |

### Configuration

| Env Var | Purpose | Default |
|---------|---------|---------|
| `ANGEL_AGENT_URL` | Sidecar URL for chat proxy | `http://localhost:8004` |
| `SERVER_NAME` | Flask server name for url_for `_external=True` | Not set (uses request host) |

---

## Deployment

### Docker

Angel web routes are part of the `cove-flask` container:

```yaml
cove_flask:
  image: cove-flask
  ports:
    - "5002:5000"
  # Angel templates in cove/angel/templates/
  # Angel static in cove/static/images/angel/
```

### AWS Target

| Component | AWS Service |
|-----------|------------|
| Cove Flask + Angel web | ECS Fargate |
| CDN | Cloudflare (DNS + CDN + SSL for TheHillPV.com) |
| Static assets | S3 + CloudFront (optional, Cloudflare may handle) |

### DNS Configuration (Planned)

| Domain | Points To | Purpose |
|--------|----------|---------|
| thehillpv.com | Cloudflare → ALB → ECS | Primary SEO engine |
| angeliquelyle.com | Luxury Presence | Flagship |
| ownpalosverdes.com | TBD | Secondary/redirect |
| chat.angeliquelyle.com | Cloudflare → ALB → ECS (optional) | Angel widget API subdomain |

---

## Code Review Findings

### P0 — Blocks Production

| # | Finding | Recommended Fix | Linear |
|---|---------|----------------|--------|
| 1 | No rate limiting on any public-facing routes — web pages, chat proxy, sitemap | Add Flask-Limiter: page routes 60/min, chat 20/min, sitemap 5/min | — |
| 2 | Chat proxy at `/angel/chat` has no input validation beyond checking `messages` is a list — could forward malicious payloads to sidecar | Validate message structure, enforce max message count and length | — |
| 3 | No CSRF protection on chat POST endpoint (it's a JSON API, not a form, but should have origin checking) | Add origin/referer validation or API key for chat endpoint | — |

### P1 — Before GA

| # | Finding | Recommended Fix | Linear |
|---|---------|----------------|--------|
| 1 | Visitor IP addresses logged in plaintext by web server | Hash or mask IPs in production access logs | — |
| 2 | No visitor analytics tracking implemented — no way to measure SEO success | Integrate Google Analytics 4 or Plausible Analytics | — |
| 3 | Neighborhood data (7 items) hardcoded as Python dict in `web_routes.py` — won't scale | Migrate to DB table or JSON config file when adding more neighborhoods | — |
| 4 | Voice overlay content hardcoded in `voice_overlays.py` — 100+ lines of content in code | Migrate to DB-backed CMS or JSON content files | — |
| 5 | Error responses from chat proxy could expose sidecar URL (`ANGEL_AGENT_URL`) in logs | Ensure error responses return generic messages, not internal URLs | — |
| 6 | Schema.org structured data not yet implemented | Add JSON-LD structured data to neighborhood and listing pages | — |

### P2 — Post-Launch

| # | Finding | Recommended Fix | Linear |
|---|---------|----------------|--------|
| 1 | No page caching — every request hits DB | Add Valkey page cache with 5-minute TTL for neighborhood pages | — |
| 2 | No image optimization pipeline — hero images served as-is | Implement responsive images with srcset, WebP format | — |
| 3 | `register_seo_routes()` registers routes at app level, bypassing blueprint prefix — works but unconventional | Consider using a separate SEO blueprint at root prefix | — |
| 4 | No A/B testing or CTA optimization framework | Implement after baseline traffic is established | — |

---

## Production Readiness Checklist

- [ ] Rate limiting on all public endpoints (pages, chat, sitemap)
- [ ] Chat proxy input validation (message structure, length limits)
- [ ] Origin/referer checking on chat POST endpoint
- [ ] IP address hashing/masking in production logs
- [ ] Analytics integration (GA4 or Plausible)
- [ ] Schema.org structured data on content pages
- [ ] Secrets in AWS Secrets Manager (not .env)
- [ ] Health check endpoints respond correctly
- [ ] Error responses don't leak internal URLs or stack traces
- [ ] Page cache implemented for data-driven content
- [ ] Cloudflare DNS configured for TheHillPV.com
- [ ] SSL certificate active (via Cloudflare)

---

*Angel Web Strategy SDD — GrowDirect Inc.*
