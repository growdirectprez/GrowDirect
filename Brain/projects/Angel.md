---
type: project-moc
status: active
tags: [angel, real-estate, compass]
---

# Angel

Real estate intelligence + lead gen for Compass agents. First deployment: Angelique Lyle, Palos Verdes Peninsula. Angel is a Cove module.

**The thesis:** Compete on data depth (APN-level records) + qualitative knowledge (this wiki) + conversational AI. Flywheel: data → content → SEO → traffic → chat → leads → transactions → more data.

**Linear:** [Angel project](https://linear.app/growdirect/project/angel-real-estate-intelligence-platform-e2489e69f160) — check here for status, priorities, and issue details.

---

## Where Things Live

| What | Where |
|------|-------|
| Angel blueprints + web routes | `Cove/cove/angel/` |
| Agent sidecar (server, tools, areas) | `Cove/cove/services/angel_agent/` |
| Models (Listing, MarketSnapshot, etc.) | `Cove/cove/models/` |
| Tests | `Cove/tests/angel_agent/` |
| Sidecar Dockerfile | `Cove/Dockerfile.angel-agent` |
| Voice profiles, market knowledge | `Angel/knowledge/` |
| CRMLS CSV exports | `Angel/Top Producer - Residential*/` |
| Content pools (crawled + synthesized) | `Angel/knowledge/content-pools/` |

---

## Architecture Decisions

These are settled — don't revisit without a reason.

- **Cove module, not standalone** — shared DB, shared APN key, native JOINs (`docs/decisions/2026-04-06-angel-as-cove-module.md`)
- **Sidecar pattern for AI** — raw ASGI on port 8004, Flask proxies via `chat_routes.py`, no Anthropic SDK in Flask
- **APN is the universal key** — dashed format canonical (`XXXX-XXX-XXX`), Parcel is the property record, Listing is the transaction record
- **LP stays as flagship** — AngeliqueLyle.com on Luxury Presence, TheHillPV.com is our Flask content engine
- **Voice overlays as Python dicts** — moves to DB when we outgrow 7 neighborhoods
- **Fair Housing in system prompt** — Federal FHA + California FEHA, non-negotiable

---

## How Data Flows

```
CRMLS (weekly CSV) → scripts/import_crmls.py → listings table (upsert by MLS#)
                                               → flask market snapshot (recompute)

Parcel data → parcels table (APN PK) ←→ listings table (APN FK)
                                      ←→ market_snapshots (area aggregations)

RSS feeds (daily) → flask crawl run → community_events table

Angel Agent sidecar → reads parcels + listings + market_snapshots via tools
                    → Anthropic API for LLM inference
                    → Flask proxy on /api/chat
```

**Known gap:** Many CRMLS listings reference APNs without a `parcels` row. The original full-peninsula GIS pull was lost during schema consolidation. Backfill needed — either re-pull from LA County GIS or create Parcel rows from CRMLS data.

---

## CRMLS Import — Operational Knowledge

This matters for every data session. Top Producer limits exports to 500 records.

**Weekly cadence:** Jeffe exports → CSV to `Angel/Top Producer*/` → `scripts/import_crmls.py` upserts → `flask market snapshot` recomputes.

**Sparse fields to watch:** agent names (MISSING in most exports), zip codes (MISSING in some), school assignments (empty), DOM (MISSING — calculate from dates), lot size (MISSING in some).

**Expansion planned:** Current exports are PV-only. Beach Cities (90266, 90254, 90277, 90278) + Torrance (90501-90505) need a one-time historical bulk export, then fold into weekly cadence.

See [[Brain/wiki/angel-weekly-crmls-pull|Weekly CRMLS Pull]] for full export definitions and field mappings.

---

## Wiki — Domain Knowledge

DB holds facts (APN, price, DOM). Wiki holds intelligence (neighborhood character, school insights, market narratives, community context). Use `mcp__obsidian__obsidian_simple_search` to find relevant articles.

### How Angel Works
- [[Brain/wiki/angel-architecture|Architecture]] — system layers, sidecar, infrastructure
- [[Brain/wiki/angel-data-platform|Data Platform]] — schema, ingestion, APN bridge, data quality rules
- [[Brain/wiki/angel-content-engine|Content Engine]] — voice system, crawl pipeline, content ops

### Domain Knowledge for Agent + Content
- [[Brain/wiki/angel-market-intelligence|Market Intelligence]] — trend analysis, area rankings, seasonal patterns
- [[Brain/wiki/angel-ninja-selling|Ninja Selling]] — sales methodology mapped to Angel tools
- [[Brain/wiki/angel-voice-training|Voice Training]] — Angelique's voice, profile, testimonials
- [[Brain/wiki/angel-buyer-process|Buyer Process]] — 9-step journey, Compass tools
- [[Brain/wiki/angel-listing-process|Listing Process]] — pricing strategy, marketing timeline
- [[Brain/wiki/angel-transaction-timeline|Transaction Timeline]] — escrow roadmaps, checklists
- [[Brain/wiki/angel-compass-concierge|Compass Concierge]] — pre-sale renovation financing
- [[Brain/wiki/angel-brand-and-team|Brand & Team]] — AREA roster, credentials, marketing
- [[Brain/wiki/angel-client-reviews|Client Reviews]] — Google/Zillow testimonials (voice calibration source)

### Neighborhood Profiles (19 articles)

Each covers: character, price positioning, DOM, schools, lifestyle, key selling angles. Named `angel-{neighborhood}-raw` in `Brain/wiki/`.

PVE: [[Brain/wiki/angel-valmonte-raw|Valmonte]], [[Brain/wiki/angel-malaga-cove-raw|Malaga Cove]], [[Brain/wiki/angel-montemalaga-raw|Montemalaga]]
RPV: [[Brain/wiki/angel-pv-dr-north-raw|PV Dr North]], [[Brain/wiki/angel-pv-dr-east-raw|PV Dr East]], [[Brain/wiki/angel-pv-dr-south-raw|PV Dr South]], [[Brain/wiki/angel-eastview-raw|Eastview]], [[Brain/wiki/angel-silver-spur-raw|Silver Spur]], [[Brain/wiki/angel-los-verdes-raw|Los Verdes]], [[Brain/wiki/angel-country-club-raw|Country Club]], [[Brain/wiki/angel-la-cresta-raw|La Cresta]], [[Brain/wiki/angel-peninsula-center-raw|Peninsula Center]], [[Brain/wiki/angel-west-palos-verdes-raw|West PV]], [[Brain/wiki/angel-the-crest-raw|The Crest]], [[Brain/wiki/angel-mira-catalina-raw|Mira Catalina]], [[Brain/wiki/angel-south-shores-raw|South Shores]]
Other: [[Brain/wiki/angel-rolling-hills-raw|Rolling Hills]], [[Brain/wiki/angel-rolling-hills-estates-raw|Rolling Hills Estates]], [[Brain/wiki/angel-riviera-village-raw|Riviera Village]]

### Cross-Cutting Lifestyle Guides
- [[Brain/wiki/angel-peninsula-golf-guide|Golf]]
- [[Brain/wiki/angel-peninsula-equestrian-guide|Equestrian]]
- [[Brain/wiki/angel-peninsula-sports-guide|Sports]]
- [[Brain/wiki/angel-peninsula-school-guide|Schools]]
- [[Brain/wiki/peninsula-tennis-pickleball|Tennis & Pickleball]]
- [[Brain/wiki/peninsula-ice-cream|Ice Cream & Frozen Treats]]
- [[Brain/wiki/peninsula-gyms-fitness|Gyms & Fitness]]
- [[Brain/wiki/peninsula-kids-water|Kids Water Activities]]
- [[Brain/wiki/peninsula-youth-sports-summer|Youth Sports, Summer & Enrichment]]

### Heritage & Source Documents
- 1926 PV Estates Sales Brochure — PDF + OCR at `Angel/knowledge/heritage/1926-pv-estates-sales-brochure.*` (historical artifact, no wiki treatment)

### Content Operations
- [[Brain/wiki/angel-content-archive-index|Content Archive — Index & Catalog]]
- [[Brain/wiki/angel-weekly-crmls-pull|Weekly CRMLS Pull]]

---

## Key People

- **Angelique Lyle** — Compass, DRE# 01475592, 310.751.8335. The voice and brand.
- **Jeffe** — CEO. Runs CRMLS exports, manages Angelique relationship.
- **ALX** — COO. Builds platform and content system.

## Related
- [[Brain/projects/Cove]] — Parent platform
- [[Brain/wiki/south-bay-wiki-architecture]] — Content geography and voice
