# Angel — Execution Plan

> **Type:** Planning Document
> **Status:** Active — Phase 0 complete (data loaded), Phase 1 in progress (content engine)
> **Namespace:** angel
> **Date:** 2026-04-06 (ops upgrade 2026-04-13)
> **Author:** ALX (COO) / Jeffe (CEO)
> **Linear Project:** [Angel — Real Estate Intelligence Platform](https://linear.app/growdirect/project/angel-real-estate-intelligence-platform-e2489e69f160)
> **Timeline:** April 7 - June 12, 2026 (10 weeks)
> **ADR:** `docs/decisions/2026-04-06-angel-as-cove-module.md`

**Wiki:** [[Brain/wiki/south-bay-wiki-architecture|South Bay Wiki Architecture]] · [[Brain/wiki/angel-architecture|Angel Architecture]] · [[Brain/projects/Angel|Angel MOC]]
**Parent:** [[docs/sdds/angel/angel-overview|Angel Overview]]

---

## Purpose

Execution timeline and Linear issue tracking for the Angel platform build.
Maps phases to GRO issues, tracks what's built vs planned, and defines
dependency chains. This is a planning document, not a service description.

---

## Architecture Summary

1. **Angel is a Cove module** — models, blueprints, migrations in Cove repo/DB
2. **LP is the flagship** — AngeliqueLyle.com stays on Luxury Presence
3. **TheHillPV.com is Flask** — data-driven content engine on Cove Flask
4. **We build the brain and plumbing** — data platform, chatbot, widget, content engine, lead pipeline

---

## Build Status (as of 2026-04-13)

### What's Built

| Component | GRO# | Status | Files |
|-----------|-------|--------|-------|
| Angel models (Listing, ListingEvent, MarketSnapshot) | GRO-458 | **Complete** | `Cove/cove/models/listing.py`, `market_snapshot.py` |
| CRMLS import pipeline (Top Producer, Hot Sheet, Lightning) | GRO-457 | **Complete** | `Cove/cove/angel/import_crmls.py`, `import_hotsheet.py`, `import_lightning.py` |
| Market snapshot computation (monthly/quarterly/annual) | GRO-457 | **Complete** | `Cove/cove/angel/market.py` |
| Community models (LocalEntity, CommunityEvent, LocalSource) | — | **Complete** | `Cove/cove/models/local_entity.py`, `community_event.py`, `local_source.py` |
| Community crawl pipeline | — | **Complete** | `Cove/cove/angel/crawl.py` |
| Content seeding (neighborhoods, schools) | — | **Complete** | `Cove/cove/angel/seed_content.py` |
| TheHillPV.com web routes (home, 7 neighborhoods, schools, ask) | GRO-465 | **Complete** | `Cove/cove/angel/web_routes.py` |
| Voice overlays (Angelique's voice per neighborhood) | — | **Complete** | `Cove/cove/angel/voice_overlays.py` |
| Chat proxy routes | — | **Complete** | `Cove/cove/angel/chat_routes.py` |
| SEO routes (sitemap.xml, robots.txt) | GRO-469 | **Complete** | `Cove/cove/angel/web_routes.py` (register_seo_routes) |
| CLI commands (flask crawl, flask market, flask crmls) | — | **Complete** | `Cove/cove/angel/cli.py` |

### What's Not Built

| Component | GRO# | Status | Blocked By |
|-----------|-------|--------|------------|
| Lead model (leads table) | GRO-458 | **Not started** | Design needed |
| Angel Agent sidecar | GRO-461 | **Not started** | Anthropic API key |
| Core MCP tools (parcel, listing, market) | GRO-462 | **Not started** | GRO-461 |
| Chat widget (JS embed) | GRO-463 | **Not started** | GRO-461 |
| Lead capture + SMS | GRO-464 | **Not started** | GRO-461 |
| ATTOM enrichment activation | GRO-459 | **Not started** | API key |
| Auto-generated market report pages | GRO-467 | **Not started** | GRO-465 (done), needs template |
| LP content refresh | GRO-470 | **Not started** | GRO-460 (pitch) |
| LP widget investigation | GRO-471 | **Not started** | GRO-463 |
| LP webhook receiver | GRO-474 | **Not started** | GRO-458 |
| LP API profile sync | GRO-475 | **Not started** | — |
| OwnPV spam cleanup | GRO-472 | **Not started** | — |
| Compass CRM sync | GRO-473 | **Not started** | GRO-464 |
| Brand pitch deck | GRO-460 | **Not started** | Jeffe's timeline |

---

## Phase Timeline

### Phase 0 — Foundation (Weeks 1-2, target April 18) — COMPLETE

| GRO# | Title | Status |
|-------|-------|--------|
| GRO-458 | Add Angel models and blueprints to Cove | **Done** |
| GRO-457 | Import CRMLS listings to Cove database | **Done** |
| GRO-459 | Activate ATTOM enrichment | **Pending** (needs API key) |
| GRO-460 | Brand pitch deck and voice calibration | **Pending** (Jeffe) |

### Phase 1 — Agent MVP (Weeks 3-6, target May 15)

| GRO# | Title | Status | Blocked By |
|-------|-------|--------|------------|
| GRO-461 | Build Angel Agent sidecar | Not started | GRO-458 (done) |
| GRO-462 | Implement core tools | Not started | GRO-457 (done) |
| GRO-463 | Build Angel chat widget | Not started | — |
| GRO-464 | Lead capture + SMS notification | Not started | GRO-458 (done) |

### Phase 2 — Content Engine & Integration (Weeks 7-10, target June 12)

| GRO# | Title | Status | Blocked By |
|-------|-------|--------|------------|
| GRO-465 | TheHillPV.com Flask skeleton | **Done** | — |
| GRO-466 | Neighborhood pages | **Done** (7 neighborhoods) | — |
| GRO-467 | Auto-generated market reports | Not started | GRO-465 (done) |
| GRO-468 | PVPUSD school guide | **Done** | — |
| GRO-469 | SEO technical setup | **Done** (sitemap, robots) | — |
| GRO-470 | Refresh AngeliqueLyle.com on LP | Not started | GRO-460 |
| GRO-471 | Investigate + embed Angel widget on LP | Not started | GRO-463 |
| GRO-474 | LP webhook receiver | Not started | GRO-458 (done) |
| GRO-475 | LP API profile sync | Not started | — |
| GRO-472 | Clean OwnPalosVerdes.com | Not started | — |
| GRO-473 | Compass CRM sync | Not started | GRO-464 |

---

## Dependency Graph

```
GRO-460 Brand Pitch ──────────────────── GATE (Jeffe)
    │
    └── GRO-470 LP Content Refresh

GRO-458 Cove Models (DONE) ──┬──────┬──────────────┐
    │                        │      │              │
    ▼                        ▼      ▼              ▼
GRO-457 Import (DONE)   GRO-461  GRO-474       GRO-465 (DONE)
    │                   Agent    LP Webhook     TheHillPV
    ├── GRO-459 ATTOM     │                       │
    │                   GRO-462 Tools          GRO-466 (DONE)
    │                        │                 GRO-467
    │                   GRO-463 Widget         GRO-468 (DONE)
    │                        │                 GRO-469 (DONE)
    │                        ├── GRO-471
    │                   GRO-464 Lead Capture
    │                        │
    │                        └── GRO-473 Compass Sync
    │
    └── GRO-466, GRO-467 (listing data dependency)
```

### Critical Path (Agent MVP)

```
GRO-461 → GRO-462 → GRO-463 → GRO-464
(sidecar)  (tools)   (widget)   (leads+SMS)
```

### Critical Path (Content Engine) — Largely Complete

```
GRO-465 (DONE) → GRO-466 (DONE) + GRO-467 + GRO-469 (DONE)
```

---

## SDD Cross-Reference

| SDD | Issues |
|-----|--------|
| [[docs/sdds/angel/data-platform|Data Platform]] | GRO-457, GRO-458, GRO-459 |
| [[docs/sdds/angel/angel-agent|Angel Agent]] | GRO-461, GRO-462, GRO-463, GRO-464 |
| [[docs/sdds/angel/web-strategy|Web Strategy]] | GRO-465, GRO-466, GRO-467, GRO-468, GRO-469, GRO-470, GRO-471, GRO-472, GRO-474, GRO-475 |
| [[docs/sdds/angel/brand-and-launch|Brand & Launch]] | GRO-460, GRO-470 |
| [[docs/sdds/angel/lp-integration|LP Integration]] | GRO-474, GRO-475 |
| [[docs/sdds/angel/angel-overview|Angel Overview]] | All (master reference) |

---

## Operations (Minimal — Planning Document)

This document tracks timeline and issues. No running service to operate.
Build progress tracked in Linear. Session discipline rules apply: each session
commits working code for one GRO issue.

---

## Code Review Findings

### P1 — Before GA

| # | Finding | Recommended Fix | Linear |
|---|---------|----------------|--------|
| 1 | Phase 0 data loading complete but lead model (GRO-458 partial) not yet designed | Design lead model with encrypted PII fields before starting GRO-464 | — |
| 2 | Content engine built ahead of Agent MVP — chat features still blocked on sidecar | Prioritize GRO-461 (sidecar) to unblock chat pipeline | — |

### P2 — Post-Launch

| # | Finding | Recommended Fix | Linear |
|---|---------|----------------|--------|
| 1 | 43 original OwnPV issues (GRO-405-447) canceled — cleanup in Linear may be needed | Verify canceled issues are properly archived | — |

---

## Production Readiness Checklist

N/A — planning document. Individual service SDDs have their own checklists.

---

*Angel Execution Plan v4 — GrowDirect Inc.*
