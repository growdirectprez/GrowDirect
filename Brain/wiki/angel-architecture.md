---
date: 2026-04-13
type: wiki
status: active
tags: [angel, architecture, cove-module, sidecar, infrastructure]
sources: [docs/sdds/angel/angel-overview.md, docs/sdds/angel/angel-agent.md, docs/sdds/angel/execution-plan.md, Cove/cove/angel/, docs/decisions/2026-04-06-angel-as-cove-module.md]
last-compiled: 2026-04-13
---

# Angel Architecture

## Summary

Angel is a real estate intelligence platform built as a Cove module — not a standalone app. It shares Cove's Flask app, database, cache, and Docker network, extending them with MLS listing data, a Claude-powered chatbot sidecar, and a data-driven content engine served as TheHillPV.com. The architecture has five layers: websites, agent, data platform, brain (Obsidian wiki), and brand. Everything resolves to APN (Assessor's Parcel Number) as the universal key.

## Design Principles

**Cove module, not standalone.** Angel blueprints register in Cove's Flask app factory. Angel models share Cove's Alembic migration path. Angel tables coexist with Cove tables in the same `cove` PostgreSQL database. This was an explicit architecture decision (ADR: `docs/decisions/2026-04-06-angel-as-cove-module.md`) — the shared APN key means Angel and Cove data JOINs are native queries, not cross-database bridges.

**Sidecar pattern for AI.** The Angel Agent chatbot runs as a separate container (port 8004), communicating with Flask via HTTP. Flask has no Anthropic SDK dependency. The sidecar is stateless — conversation history lives in the browser widget. This mirrors Canary's QA Agent pattern (GRO-326).

**Two websites, one pipeline.** AngeliqueLyle.com stays on Luxury Presence (managed hosting, IDX feed, brochure site). TheHillPV.com is a Flask content engine with full programmatic control. Both embed the same Angel chat widget, both feed leads into the same Cove pipeline. LP handles the flagship; we handle the content engine.

**Database for facts, wiki for intelligence.** The Cove database stores structured data — APNs, prices, DOM, listing status, agent names. The Brain wiki (Obsidian) stores qualitative knowledge — neighborhood character, school insights, market narratives, restaurant picks, community context. Content generation reads from both.

## System Layers

### Layer 1: Websites

Two domains with distinct roles converging on one outcome: a phone conversation between visitor and Angelique.

| Domain | Platform | Role | Control |
|--------|----------|------|---------|
| AngeliqueLyle.com | Luxury Presence | Flagship brochure + IDX | LP manages hosting/design; we refresh content + embed widget |
| TheHillPV.com | Flask (Cove `angel_web_bp`) | Silent SEO content engine | Full programmatic control — auto-generated pages, SEO, analytics |
| OwnPalosVerdes.com | TBD | Secondary SEO (spam cleanup needed) | Parked; redirects to TheHillPV after recovery assessment |

TheHillPV.com reads like an independent local guide, not an agent marketing site. "The Hill" is what PV locals call the peninsula. Angelique's association is subtle until the visitor engages with Angel.

### Layer 2: Angel Agent (Chatbot Sidecar)

Claude-powered conversational AI that knows every property on the peninsula. Runs as `angel-agent` container on port 8004.

**Architecture:**
```
Chat Widget (JS embed, any website)
    → POST /api/chat
    → Cove Flask (angel_chat_bp, port 5002)
        → POST http://angel-agent:8004/chat (120s timeout)
        → Anthropic API (claude-sonnet, 4096 max tokens)
        → Tool dispatch (12 MCP tools, read-only)
    → Response to widget
    + Lead capture → SMS to Angelique + Compass CRM
```

**12 MCP tools across 5 domains:**

| Domain | Tools | Data Source |
|--------|-------|------------|
| Parcel | parcel_lookup, parcel_history, nearby_parcels | Cove parcels + Angel listings |
| Listing | listing_search, listing_detail, market_stats, transaction_history | Angel listings table |
| Community | neighborhood_profile, school_info, commute_estimate | Brain wiki + GreatSchools |
| Strategy | cma_summary, listing_strategy, concierge_calc | Market data + knowledge |
| Lead | capture_lead, schedule_callback | Creates Lead record + SMS |

**Safety model (consumer-facing, not operator-facing):**
- All tools read-only (no writes except capture_lead)
- Fair Housing compliant — never steers based on protected classes
- PII collected only through explicit capture_lead tool
- Rate limited: 30 messages/session, 150/day per IP
- Conversation bounded: max 20 turns per session
- DRE# 01475592 disclosure in widget footer

### Layer 3: Data Platform

Three data domains sharing the `cove` database:

| Domain | Tables | Source |
|--------|--------|--------|
| Parcels (Cove core) | `parcels` | LA County GIS + WPBCA seed |
| Listings (Angel) | `listings`, `listing_events` | CRMLS Top Producer |
| Community Intelligence (Angel) | `local_sources`, `community_events`, `local_entities` | RSS feeds + manual seeds |
| Market snapshots (Angel) | `market_snapshots` | Computed aggregations (monthly/quarterly/annual) |
| Leads (Angel, not yet built) | `leads` | Agent capture + signals |

The APN is the join key across everything. See [[Brain/wiki/angel-data-platform|Angel Data Platform]] for schema details and ingestion pipeline.

### Layer 4: Brain (This Wiki)

The Obsidian knowledge graph holds everything a database can't — neighborhood narratives, school insights, market analysis, community context, voice overlays. Content generation reads from both DB and wiki.

Knowledge flows in, content flows out:
```
CRMLS (weekly) ──→ DB ──→ market analysis ──→ wiki snapshots ──→ market reports
Firecrawl ──→ wiki (entities, context) ──→ voice overlays ──→ neighborhood pages
RSS feeds ──→ DB (events) ──→ wiki enrichment ──→ event calendars
```

See [[Brain/wiki/angel-content-engine|Angel Content Engine]] for the knowledge workflow.

### Layer 5: Brand

"Angel" is the AI assistant identity. Angelique Lyle is the human brand. The brand is portable — it moves with Angelique, not tied to Compass or any brokerage.

Voice rules (from `Angel/knowledge/agentic-profile.md`):
- First person, warm, confident, grounded
- Specific local knowledge — street names, school campuses, neighborhood character
- Lead with empathy — real estate decisions are personal
- Never: "stunning," "luxury lifestyle," "dream home," "act fast"
- Always: Fair Housing compliant

## Infrastructure

### Shared GrowDirect Stack

| Component | Port | Container |
|-----------|------|-----------|
| PostgreSQL 17 | 5432 | `growdirect_postgres` |
| Valkey 8 | 6379 | `growdirect_valkey` |
| Ollama | 11434 | `growdirect_ollama` |
| pgAdmin | 5050 | `growdirect_pgadmin` |

### Angel Services (in Cove compose)

| Service | Port | Container | Purpose |
|---------|------|-----------|---------|
| Cove Flask | 5002 | `cove-flask` | Hosts Cove + Angel blueprints, TheHillPV.com |
| Angel Agent | 8004 | `angel-agent` | Claude chatbot sidecar |
| MailHog | 1026/8026 | `cove-mailhog` | Dev email testing |

### Database

| Database | Purpose |
|----------|---------|
| `cove` | Production — Cove governance + Angel real estate (shared) |
| `cove_test` | Test database |

Credentials: `growdirect / growdirect_dev`. Valkey DB 1 (shared Cove + Angel). Extensions: `vector`, `pgcrypto`, `uuid-ossp`.

### External Services

| Service | Purpose | Status |
|---------|---------|--------|
| Anthropic API | Angel Agent LLM | Ready (needs API key) |
| ATTOM API | Property enrichment | Script ready, needs activation |
| Twilio | SMS lead notifications | Needs setup |
| Cloudflare | DNS + CDN for TheHillPV.com | Needs setup |
| Luxury Presence | AngeliqueLyle.com hosting | Active |

## Lead Flow

```
Organic Search / Social / Referral
    → Website (any of 3 domains)
    → Content consumed (neighborhood, market, school)
    → Angel Chat Widget ("Ask me anything about PV")
    → 3-10 turns of conversation (parcel lookups, market data)
    → "I'd love to connect you with Angelique directly"
    → Phone number captured
    ├── SMS to Angelique (Twilio)
    ├── Lead record in Cove DB (with source attribution)
    └── Compass CRM sync (async)
```

Lead stages: identified → engaged → captured → contacted → showing → offer → escrow → closed → archived.

Attribution fields: source_domain, source_page, source_referrer, conversation_turns.

## What Makes Angel Different

| Dimension | Typical Agent Tech | Angel |
|-----------|-------------------|-------|
| Data | IDX feed (same as everyone) | Proprietary APN-level dataset (parcels + listings + market snapshots) |
| Website | Template (LP, kvCORE) | LP flagship + Flask content engine |
| AI | Generic chatbot | Conversational AI with local knowledge + 12 tools |
| Voice | Corporate boilerplate | Angelique's actual voice and expertise |
| Lead capture | Form fill → email | Natural conversation → SMS to phone |
| Content | Manual blog posts | Auto-generated from data + wiki + editorial review |
| Moat | None (same tools, same data) | Dataset + wiki compound over time |

## Code Organization

```
Cove/cove/angel/           — Blueprints, routes, crawl pipeline, voice overlays, CLI
Cove/cove/models/          — Listing, ListingEvent, LocalSource, CommunityEvent, LocalEntity
Cove/templates/angel/      — Jinja2 templates (home, neighborhood, schools)
Cove/static/css/angel/     — Tailwind styles
Cove/scripts/              — import_crmls.py, import_hot_sheet.py
Angel/knowledge/           — Voice profiles, market knowledge, school guide, brand
Angel/Top Producer*/       — CRMLS CSV exports (6 batches, ~2,368 listings)
Angel/knowledge/content-pools/  — Crawled + synthesized neighborhood content
```

## Related

- [[Brain/wiki/angel-data-platform|Angel Data Platform]] — Schema, ingestion, APN bridge, data sources
- [[Brain/wiki/angel-content-engine|Angel Content Engine]] — Voice system, crawl pipeline, knowledge workflow
- [[Brain/wiki/south-bay-wiki-architecture|South Bay Wiki Architecture]] — Content spine and geography
- [[Brain/projects/Angel|Angel MOC]] — Project hub with Linear issues and full inventory
- [[Brain/projects/Cove|Cove]] — Parent platform
- [[Brain/wiki/canary-architecture|Canary Architecture]] — Pattern donor for sidecar + MCP approach
