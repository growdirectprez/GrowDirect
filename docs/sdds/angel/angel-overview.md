# Angel — System Overview

> **Type:** Platform Service (Angel Index SDD)
> **Status:** Active — Phase 0 complete, Phase 1 in progress
> **Namespace:** angel
> **Date:** 2026-04-06 (ops upgrade 2026-04-13)
> **Author:** ALX (COO) / Jeffe (CEO)
> **Client:** Angelique Lyle, Compass, Palos Verdes Peninsula

**Wiki:** [[Brain/wiki/south-bay-wiki-architecture|South Bay Wiki Architecture]] · [[Brain/projects/Angel|Angel MOC]]

---

## Purpose

Angel is a real estate intelligence platform that turns 20 years of local
expertise and a proprietary property dataset into a 24/7 AI-powered lead
generation engine for Angelique Lyle, a top 1.5% Compass agent on the
Palos Verdes Peninsula. It is deployed as a module inside Cove (shared Flask
app, shared database, shared Docker network).

---

## Dependencies

| Dependency | Type | Required |
|------------|------|----------|
| Cove Flask (port 5002) | Host app — Angel blueprints registered here | Yes |
| PostgreSQL (`cove` database) | Angel tables coexist with Cove tables | Yes |
| Valkey DB 1 | Sessions, page cache (shared with Cove) | Yes |
| Angel Agent sidecar (port 8004) | Claude-powered chat — separate container | For chat features |
| Anthropic API | LLM inference for Angel Agent | For chat features |
| Ollama (`growdirect_ollama:11434`) | Future — semantic search on listings | No (planned) |
| ATTOM API | Property enrichment | No (script ready, needs key) |
| Twilio | SMS lead notifications | No (planned) |
| Cloudflare | DNS + CDN for TheHillPV.com | For production |
| Luxury Presence | AngeliqueLyle.com hosting | External (Angelique's account) |

---

## Component SDDs

| Document | Type | What It Covers |
|----------|------|---------------|
| [data-platform.md](data-platform.md) | App Service | Database schema, CRMLS ingestion, APN enrichment, market analysis |
| [angel-agent.md](angel-agent.md) | App Service | Chatbot architecture, MCP tools, system prompt, widget, sidecar deployment |
| [web-strategy.md](web-strategy.md) | App Service | Three-domain strategy, SEO, Flask content engine, LP integration, lead flow |
| [brand-and-launch.md](brand-and-launch.md) | Reference | Brand concept, voice definition, pitch to Angelique, budget |
| [execution-plan.md](execution-plan.md) | Planning | Timeline, phases, Linear issues, dependency graph |
| [lp-integration.md](lp-integration.md) | External Integration | LP webhook receiver, lead sync, agent profile API |

---

## Architecture — 4-Layer Stack

```
┌─────────────────────────────────────────────────────────┐
│                    WEBSITES                              │
│  AngeliqueLyle.com (LP)    TheHillPV.com (Flask)        │
│  Flagship brochure/IDX     Data-driven content engine   │
│           ↓                    ↓              ↓          │
│              Angel Chat Widget (embedded)                │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                  ANGEL AGENT                             │
│  Claude-powered sidecar · Angelique's voice             │
│  12 MCP tools · Lead capture → SMS + Compass CRM       │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                  DATA PLATFORM                           │
│  2,368 MLS listings · 5,514 county parcels (Cove)      │
│  ATTOM enrichment · APN as universal key                │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                     BRAND                                │
│  "Angel" identity · Angelique's voice · PV local brand  │
│  Portable — moves with her, not tied to Compass         │
└─────────────────────────────────────────────────────────┘
```

---

## Data Flow & PII Map

### What Enters

| Source | Data | Format |
|--------|------|--------|
| CRMLS Top Producer exports | MLS listings with agent names/emails | CSV (.tp files) |
| CRMLS Agent Hot Sheet | Listing status change events | CSV |
| CRMLS Lightning v2 | Enriched listing data (zip, schools, remarks) | Tab-delimited |
| Angel chat widget | Visitor conversations, phone numbers | JSON via sidecar |
| LP custom webhook | Lead contact info from AngeliqueLyle.com | JSON POST |
| Community crawl (RSS) | Local events, entity data | RSS/Atom feeds |

### What's Stored (PII Classification)

| Field | Table | Classification | Encryption |
|-------|-------|---------------|------------|
| Listing agent name | `listings` | **internal** | Plaintext |
| Listing agent email | `listings` | **sensitive** | Plaintext (P0) |
| Buyer agent name | `listings` | **internal** | Plaintext |
| Buyer agent email | `listings` | **sensitive** | Plaintext (P0) |
| Lead owner name | `leads` (planned) | **sensitive** | Plaintext (P0) |
| Lead owner email | `leads` (planned) | **sensitive** | Plaintext (P0) |
| Lead owner phone | `leads` (planned) | **sensitive** | Plaintext (P0) |
| Visitor phone (chat capture) | `leads` (planned) | **sensitive** | Plaintext (P0) |
| Property address | `listings` | **public** | N/A |
| APN | `listings`, `parcels` | **public** | N/A |
| List/close prices | `listings` | **public** | N/A |
| Raw CSV data | `listings.raw_data` | **internal** | Plaintext JSON (contains agent PII) |
| Market snapshots | `market_snapshots` | **public** | N/A |

### What Exits

| Destination | Data | Notes |
|-------------|------|-------|
| TheHillPV.com pages | Market stats, neighborhood data, school info | Public — no PII |
| Angel Agent sidecar | Listing data, parcel data for chat queries | Internal network |
| SMS (Twilio, planned) | Lead phone + context → Angelique's phone | Sensitive |
| Compass CRM (planned) | Lead name, phone, email, property interest | Sensitive |

---

## Infrastructure

### Services

| Service | Port | Container | Purpose |
|---------|------|-----------|---------|
| Cove Flask | 5002 | `cove-flask` | Hosts Angel blueprints (angel_web_bp, angel_chat_bp) |
| Angel Agent | 8004 | `angel-agent` | Claude-powered chat sidecar |

### Shared Infrastructure

| Component | Detail |
|-----------|--------|
| Database | `cove` on `growdirect_postgres:5432` |
| Cache | Valkey DB 1 on `growdirect_valkey:6379` |
| Embeddings | `growdirect_ollama:11434` (future) |
| Network | `growdirect` Docker network |

### Multi-Tenant Isolation

Angel is NOT multi-tenant. It serves one agent (Angelique Lyle) on one peninsula.
Angel tables coexist with Cove tables in the same database — no schema isolation.
If Angel were to serve multiple agents in the future, tenant isolation would be
required at the database schema level (separate schemas per agent or row-level
tenant_id filtering).

### Startup Order

1. `growdirect_postgres` — database must be available
2. `growdirect_valkey` — sessions and cache
3. `cove-flask` — Angel blueprints registered during app factory
4. `angel-agent` — sidecar starts independently, Cove proxies to it

### Blast Radius

| If This Goes Down | Impact |
|-------------------|--------|
| `cove-flask` | All Angel web pages down, chat proxy down, LP webhook receiver down |
| `angel-agent` sidecar | Chat unavailable; web pages and data pipeline unaffected |
| PostgreSQL | All Angel features down (pages, chat, import) |
| Valkey | Sessions lost, page cache cold; pages still render from DB |
| Anthropic API | Chat responses fail; everything else unaffected |

---

## Operations

### Startup & Health Checks

- Cove Flask: `GET /health` returns 200 with DB and Valkey status
- Angel chat proxy: `GET /angel/chat/health` checks sidecar reachability
- Angel Agent sidecar: `GET /health` on port 8004

### Failure Modes

| Failure | Behavior | Recovery |
|---------|----------|----------|
| Sidecar down | Chat returns 503; web pages unaffected | Restart `angel-agent` container |
| DB connection lost | All routes return 500 | Check PostgreSQL, restart Flask |
| CRMLS import error | Per-row rollback, continues next row | Check error log, re-import failed batch |
| Anthropic API timeout | Chat returns timeout error to user | Automatic — next request retries |

### Configuration

| Env Var | Purpose | Default |
|---------|---------|---------|
| `ANGEL_AGENT_URL` | Sidecar URL | `http://localhost:8004` |
| `DATABASE_URL` | PostgreSQL connection | (from Cove .env) |
| `VALKEY_URL` | Cache/sessions | (from Cove .env) |
| `ANTHROPIC_API_KEY` | LLM for Angel Agent | Required for chat |
| `TWILIO_*` | SMS configuration | Not yet configured |

---

## Deployment

### Docker

Angel is part of the Cove Docker Compose stack:
- `cove-flask`: Gunicorn on 5002:5000, mounts Cove code including `cove/angel/`
- `angel-agent`: Separate container on 8004, Claude sidecar pattern from Canary QA Agent

### AWS Target

| Component | AWS Service |
|-----------|------------|
| Cove Flask + Angel | ECS Fargate (single task, shared with Cove) |
| Angel Agent sidecar | ECS Fargate (separate task in same cluster) |
| PostgreSQL | RDS PostgreSQL 17 |
| Valkey | ElastiCache (Valkey-compatible) |
| Secrets | AWS Secrets Manager |
| DNS | Cloudflare (TheHillPV.com) → ALB |

### CI/CD

Not yet configured. Target: GitHub Actions → Docker build → ECR push → ECS deploy.

---

## Data Inventory

| Dataset | Records | Source | Status |
|---------|---------|--------|--------|
| County parcels (APN, geometry, assessed values) | 5,514 | LA County GIS via Cove | LIVE |
| MLS listings (Top Producer + Lightning exports) | 2,368 | CRMLS member export | Loaded |
| Closed transactions with prices | 1,489 | Subset of MLS listings | Loaded |
| APN overlap (Cove parcels intersect CRMLS) | 379 | Computed | Mapped |
| ATTOM enrichment (deed, AVM, schools) | 0 | ATTOM API | Script ready, needs activation |
| Listing events (price changes, status) | ~400 | Agent Hot Sheet exports | Loaded |
| Market snapshots (monthly/quarterly/annual) | ~1,500 | Computed from listings | Computed |
| Community events (RSS crawl) | ~50 | Local RSS feeds | Seeded |
| Local entities (restaurants, businesses, schools) | ~100 | Content pools | Seeded |

---

## Lead Flow

```
Organic Search / Social / Referral / Direct
         │
         ▼
    ┌─── Website (any of 3 domains) ───┐
    │    Content consumed               │
    │    Angel Chat Widget              │
    │    3-10 turns of conversation     │
    │    Phone number captured          │
    └────────┬───────────────────────────┘
             │
     ┌───────┼───────────┐
     ▼       ▼           ▼
   SMS    Angel DB    Compass CRM
   to     (lead       (async sync)
 Angelique record)
```

---

## Relationship to Other GrowDirect Apps

| App | Relationship |
|-----|-------------|
| **Cove** | Angel is a Cove module. Models, blueprints, migrations coexist in Cove repo and DB. ADR: `docs/decisions/2026-04-06-angel-as-cove-module.md` |
| **Canary** | Architecture pattern donor. Angel Agent follows Canary's QA Agent sidecar pattern (GRO-326). |
| **Memory Bus** | Future — Angel sessions logged to platform memory for cross-app learning. |

---

## Code Review Findings

### P0 — Blocks Production

| # | Finding | Recommended Fix | Linear |
|---|---------|----------------|--------|
| 1 | Agent emails in `listings` stored plaintext (`listing_agent_email`, `buyer_agent_email`) | Field-level AES-256-GCM encryption using Canary's `crypto.py` pattern | — |
| 2 | `raw_data` JSON column preserves full CSV rows including agent PII (names, emails, office affiliations) | Redact sensitive fields from `raw_data` before storage, or encrypt the JSON blob | — |
| 3 | `leads` table (planned) will store owner name/email/phone — no encryption pattern established | Design lead model with encrypted PII fields from day one | — |
| 4 | Secrets (API keys, DB credentials) in `.env` files | AWS Secrets Manager + `boto3` retrieval at startup | — |
| 5 | No authentication on Angel web routes — public pages serve data from DB queries without rate limiting | Add rate limiting (Flask-Limiter) on all public-facing routes | — |

### P1 — Before GA

| # | Finding | Recommended Fix | Linear |
|---|---------|----------------|--------|
| 1 | No audit trail for lead pipeline stage transitions | Add audit log entries for lead creation, stage changes, CRM sync events | — |
| 2 | No data retention policy for listings, leads, or chat conversations | Define retention: leads >12mo archived, chat logs >6mo purged, listings retained indefinitely (public data) | — |
| 3 | CRMLS import commits per-row (`db.session.commit()` in loop) — slow and no batch atomicity | Refactor to batch commits (every N rows) with rollback on batch failure | — |
| 4 | No rate limiting on `/angel/chat` proxy endpoint | Flask-Limiter on chat endpoint (e.g., 20 req/min per IP) | — |
| 5 | Chat proxy passes raw sidecar JSON to client — error responses could leak internal URLs | Sanitize sidecar error responses before returning to client | — |

### P2 — Post-Launch

| # | Finding | Recommended Fix | Linear |
|---|---------|----------------|--------|
| 1 | `Listing.id` uses `String(36)` UUID — inconsistent with platform `Mapped[uuid.UUID]` standard | Migrate to native UUID column type | — |
| 2 | No monitoring dashboard for Angel-specific metrics (chat volume, lead capture rate, import health) | Build Grafana dashboard or add to Cove ops | — |
| 3 | Voice overlay content hardcoded in `voice_overlays.py` — won't scale past 7 neighborhoods | Migrate to DB or CMS table when content exceeds 10 neighborhoods | — |
| 4 | Market snapshot computation runs synchronously in CLI — no scheduling | Add cron job or Valkey-based task queue for periodic recomputation | — |

---

## Production Readiness Checklist

- [ ] PII encrypted at rest (agent emails, lead contact info)
- [ ] Secrets in AWS Secrets Manager (not .env)
- [ ] Health check endpoint responds (`/health`, `/angel/chat/health`)
- [ ] Audit logging for sensitive operations (lead stage changes, data imports)
- [ ] Data retention policy implemented
- [ ] Rate limiting on public endpoints (web pages, chat, webhook)
- [ ] Error responses don't leak internals (sidecar URLs, stack traces)
- [ ] `raw_data` JSON column scrubbed of PII before storage
- [ ] CRMLS import batch tracking with error reporting
- [ ] Angel Agent sidecar health monitored and alerted

---

## Open Questions

1. **LP widget injection** — Can Luxury Presence sites accept custom `<script>` tags?
2. **CRMLS API access** — RESO Web API requires license agreement through broker.
3. **Compass CRM API** — Does Compass expose a CRM API for contact/pipeline sync?
4. **ATTOM pricing post-trial** — Free trial gives 1,000 calls/day for 30 days. Post-trial tier TBD.
5. **Angelique's response** — Everything depends on her saying yes.

---

*Angel System Overview — GrowDirect Inc.*
