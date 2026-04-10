# Angel — Execution Plan (Final)

> **Status:** Active — build plan
> **Namespace:** angel
> **Date:** 2026-04-06 (v4 — hybrid: LP flagship + Flask content engine)
> **Author:** ALX (COO) / Jeffe (CEO)
> **Linear Project:** [Angel — Real Estate Intelligence Platform](https://linear.app/growdirect/project/angel-real-estate-intelligence-platform-e2489e69f160)
> **Timeline:** April 7 – June 12, 2026 (10 weeks)
> **ADR:** `docs/decisions/2026-04-06-angel-as-cove-module.md`

---

## Architecture (Final)

Three rounds of simplification plus one course correction:

1. **Angel is a Cove module** — models, blueprints, and migrations live in Cove's repo and database. No separate Flask app, no separate database.
2. **LP is the flagship** — AngeliqueLyle.com stays on Luxury Presence (IDX, managed hosting, brochure site). Content refresh and widget embed via LP dashboard.
3. **TheHillPV.com is our Flask content engine** — data-driven pages (neighborhoods, market reports, school guide, street profiles) served from Cove Flask. Full programmatic control over content, SEO, and chat integration. This is where our proprietary dataset becomes visible.
4. **We build the brain and the plumbing** — data platform (Cove tables + import scripts), Angel Agent chatbot (sidecar container), chat widget (JS embed), content engine (TheHillPV Flask blueprints), lead pipeline (LP webhook + SMS + Compass CRM sync).

```
AngeliqueLyle.com (LP — flagship)
    │  Angel chat widget embedded via LP dashboard
    │  LP forms → Custom Webhook → Cove
    │
TheHillPV.com (Flask — content engine)
    │  Server-rendered pages from Cove data
    │  Angel chat widget native
    │  Full SEO control
    │
    ▼
Cove Flask (port 5002)
    │  angel_chat_bp — proxies to sidecar
    │  angel_web_bp — TheHillPV content pages
    │  angel_webhook_bp — receives LP lead events
    │
    ├──► Angel Agent Sidecar (port 8004)
    │    Claude-powered, 12 MCP tools
    │    Reads from Cove DB directly
    │
    ├──► Cove DB (listings, leads, market_snapshots + existing parcels)
    │
    ├──► Twilio SMS → Angelique's phone
    │
    └──► Compass CRM (async sync)
```

---

## Live Issues (16 total)

### Phase 0 — Foundation (Weeks 1–2, target April 18)

| GRO# | Title | Priority | Owner | Blocked By |
|-------|-------|----------|-------|------------|
| **GRO-458** | Add Angel models and blueprints to Cove | Urgent | Builder | — |
| **GRO-457** | Import CRMLS listings to Cove database | Urgent | Builder | GRO-458 |
| **GRO-459** | Activate ATTOM enrichment for Angel parcels | High | ALX | GRO-458 |
| **GRO-460** | Brand pitch deck and voice calibration | Urgent | Jeffe | — |

**Exit criteria:** Angelique says yes. 2,368 listings in Cove DB. Angel
blueprints registered in Cove app. ATTOM enrichment running.

### Phase 1 — Agent MVP (Weeks 3–6, target May 15)

| GRO# | Title | Priority | Owner | Blocked By |
|-------|-------|----------|-------|------------|
| **GRO-461** | Build Angel Agent sidecar | Urgent | Builder | GRO-458 |
| **GRO-462** | Implement core tools (parcel, listing, market) | Urgent | Builder | GRO-457 |
| **GRO-463** | Build Angel chat widget (JS embed) | High | Builder | — |
| **GRO-464** | Implement lead capture + SMS notification | High | Builder | GRO-458 |

**Exit criteria:** Angel Agent answers questions about PV properties using
real Cove data. Lead capture → SMS to Angelique works end-to-end.

### Phase 2 — Content Engine & Integration (Weeks 7–10, target June 12)

| GRO# | Title | Priority | Owner | Blocked By |
|-------|-------|----------|-------|------------|
| **GRO-465** | TheHillPV.com Flask skeleton (Angel web blueprints) | Urgent | Builder | GRO-458 |
| **GRO-466** | Neighborhood pages (data-driven, server-rendered) | High | Builder | GRO-465, GRO-457 |
| **GRO-467** | Auto-generated market reports | High | Builder | GRO-465, GRO-457 |
| **GRO-468** | PVPUSD school guide | Medium | Builder | GRO-465 |
| **GRO-469** | SEO technical setup (sitemap, schema.org, meta) | High | Builder | GRO-465 |
| **GRO-470** | Refresh AngeliqueLyle.com content on LP | High | Jeffe + Angelique | GRO-460 |
| **GRO-471** | Investigate + embed Angel widget on LP | High | Builder | GRO-463 |
| **GRO-474** | Set up LP Custom Webhook → Cove leads | High | Builder | GRO-458 |
| **GRO-475** | Build LP API agent profile sync | Medium | Builder | — |
| **GRO-472** | Clean OwnPalosVerdes.com spam | Medium | ALX | — |
| **GRO-473** | Build Compass CRM async lead sync | Medium | Builder | GRO-464 |

**Exit criteria:** TheHillPV.com live with neighborhood pages, market reports,
and native Angel widget. AngeliqueLyle.com refreshed on LP with widget embed.
LP leads and Angel chat leads flowing into same Cove pipeline. Compass CRM sync operational.

---

## Dependency Graph

```
GRO-460 Brand Pitch ──────────────────────── GATE (Jeffe)
    │
    └── GRO-470 LP Content Refresh

GRO-458 Cove Models ──┬─────────────┬───────────────┐
    │                  │             │               │
    ▼                  ▼             ▼               ▼
GRO-457 Import    GRO-461 Agent  GRO-474 LP      GRO-465 TheHillPV
    │             Sidecar        Webhook          Flask Skeleton
    │                  │                              │
    ├──► GRO-459      GRO-462 Tools              ┌───┼───────┐
    │    ATTOM              │                     ▼   ▼       ▼
    │                  GRO-463 Widget          GRO-466 GRO-467 GRO-468
    │                       │                  Nbhds  Reports  Schools
    │                       ├──► GRO-471          │
    │                       │    LP Widget     GRO-469 SEO
    │                       │
    │                  GRO-464 Lead Capture
    │                       │
    │                       └──► GRO-473 Compass Sync
    │
    └──► GRO-466 (also needs listing data)
         GRO-467 (also needs listing data)
```

### Critical Path (Agent MVP)

```
GRO-458 → GRO-457 → GRO-462 → GRO-461 → GRO-463 → GRO-464
(models)   (data)    (tools)   (sidecar)  (widget)   (leads+SMS)
```

### Critical Path (Content Engine)

```
GRO-458 → GRO-465 → GRO-466 + GRO-467 + GRO-469
(models)   (skeleton)  (neighborhood pages, market reports, SEO)
```

Both paths start from GRO-458 and can run in parallel after that.

---

## Canceled Issues

| GRO# | Title | Reason |
|-------|-------|--------|
| GRO-405–447 | Original OwnPV Relaunch plan (43 issues) | Superseded by Angel system |
| GRO-476 | Create TheHillPV.com as second LP site | TheHillPV is Flask, not LP |

---

## What We Build vs What LP Does

| We Build | LP Does |
|----------|---------|
| TheHillPV.com content engine (Flask, Cove blueprints) | AngeliqueLyle.com flagship (design, hosting, SSL, IDX) |
| Data models in Cove (listings, leads, snapshots) | AngeliqueLyle.com content pages (bio, testimonials) |
| CRMLS import scripts | Template design, responsive layout |
| Neighborhood pages, market reports, school guide (data-driven) | IDX listing search |
| Angel Agent sidecar (Claude chatbot) | Lead forms (LP native, alongside Angel widget) |
| Chat widget JS (embedded on both sites) | Agent profile hosting |
| LP webhook receiver (leads → Cove) | |
| LP API sync (agent profiles) | |
| SEO infrastructure for TheHillPV (sitemap, schema.org, meta) | |
| SMS notifications (Twilio) | |
| Compass CRM sync | |

### Why TheHillPV.com Is Flask, Not LP

LP excels at the flagship brochure site — IDX, managed hosting, responsive
templates. But a content engine that auto-generates 60+ market reports/year
and 50+ street profiles from a live database needs programmatic control that
LP's CMS can't provide (no content publishing API).

TheHillPV.com is Flask because:
- Pages are generated from Cove data, not manually authored
- Monthly market reports self-publish without human intervention
- SEO needs full control (schema.org, structured data, sitemap generation)
- Angel widget is native, not injected
- Content velocity (50+ pages at launch, growing monthly) requires automation

AngeliqueLyle.com stays on LP because:
- IDX listing search is table stakes and LP does it well
- Flagship brochure content changes infrequently
- LP's design quality matches Compass luxury brand expectations
- Angelique already pays for it

---

## Build Order for Angel Builder

1. **Read** `~/GrowDirect/CLAUDE.md` then `~/GrowDirect/Cove/CLAUDE.md`
2. **GRO-458** — Add models to `Cove/cove/models/` (listing.py, lead.py, market_snapshot.py). Register angel blueprints in Cove's app factory. Alembic migration.
3. **GRO-457** — Write `Cove/scripts/import_crmls.py`. Load CSVs from `Angel/Top Producer - Residential*/`. Run against Cove DB.
4. **GRO-461** — Build sidecar. Pattern: `Canary/canary/services/qa_agent/`. Add to `Cove/devops/docker-compose.yml`.
5. **GRO-462** — Implement tools. They query Cove DB directly (listings + research_parcels = native JOIN).
6. **GRO-463** — Chat widget. Self-contained JS file served from Cove static.
7. **GRO-464** — Lead capture tool + Twilio SMS.
8. **GRO-465** — TheHillPV Flask skeleton. Angel web blueprints in Cove (angel_web_bp). Routes: /, /neighborhoods, /market, /schools, /streets, /ask. Tailwind + Alpine.js. Cloudflare DNS.
9. **GRO-466** — Neighborhood pages. Data-driven from parcels + listings. Server-rendered Jinja2.
10. **GRO-467** — Market reports. Auto-generated from market_snapshots. Monthly cron or on-demand.
11. **GRO-469** — SEO setup. Sitemap.xml, schema.org structured data, meta tags, canonical URLs.
12. **GRO-474** — LP webhook endpoint in Cove.

GRO-460 (pitch) runs on Jeffe's timeline. Builder infrastructure work
doesn't wait on it.

---

## SDD Cross-Reference

| SDD | Issues |
|-----|--------|
| `data-platform.md` | GRO-457, GRO-458, GRO-459 |
| `angel-agent.md` | GRO-461, GRO-462, GRO-463, GRO-464 |
| `web-strategy.md` | GRO-465, GRO-466, GRO-467, GRO-468, GRO-469, GRO-470, GRO-471, GRO-472, GRO-474, GRO-475 |
| `brand-and-launch.md` | GRO-460, GRO-470 |
| `angel-overview.md` | All (master reference) |
| ADR: `2026-04-06-angel-as-cove-module.md` | Architecture decision |

---

*Angel Execution Plan v4 — GrowDirect Inc.*
