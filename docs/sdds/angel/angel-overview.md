# Angel — System Overview

> **Status:** Proposed — master spec, all components in design phase
> **Namespace:** angel
> **Date:** 2026-04-06
> **Author:** ALX (COO) / Jeffe (CEO)
> **Client:** Angelique Lyle, Compass, Palos Verdes Peninsula

---

## What Is Angel

Angel is a real estate intelligence platform that turns 20 years of local
expertise and a proprietary property dataset into a 24/7 AI-powered lead
generation engine for Angelique Lyle, a top 1.5% Compass agent on the
Palos Verdes peninsula.

The system has four layers:

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

## The Thesis

Every agent on the Palos Verdes peninsula has a website showing the same MLS
data through the same IDX feed. They compete on headshots and taglines.

Angel competes on **data depth**. We have APN-level records for every parcel
on the Hill — county assessor data, transaction history, MLS listing records,
ATTOM enrichment, Cove community governance data, school assignments — tied
together by a single key. No other agent has this dataset. No other agent has
an AI that can query it in natural language and answer in their voice.

The flywheel: proprietary data → data-driven content (TheHillPV.com) → SEO
authority → organic traffic → Angel chatbot engagement → lead capture →
Angelique's phone → listing appointments → closed transactions → more data
(transaction records feed back into the dataset).

---

## Component SDDs

| Document | What It Covers |
|----------|---------------|
| [data-platform.md](data-platform.md) | Database schema, ingestion pipeline, APN enrichment, Cove bridge, data sources |
| [angel-agent.md](angel-agent.md) | Chatbot architecture, MCP tools, system prompt, widget, deployment |
| [web-strategy.md](web-strategy.md) | Three-domain strategy, SEO, content engine, LP integration, lead flow |
| [brand-and-launch.md](brand-and-launch.md) | Brand concept, pitch to Angelique, phased rollout, budget, risks |

---

## Architecture Summary

### Infrastructure (Shared GrowDirect Stack)

| Component | Detail |
|-----------|--------|
| Database | `cove` on `growdirect_postgres:5432` (Angel tables coexist with Cove) |
| Cache | Valkey DB 1 on `growdirect_valkey:6379` (shared with Cove) |
| Embeddings | `growdirect_ollama:11434` (future — semantic search on listings) |
| Network | `growdirect` Docker network (shared with Canary, Cove) |

### Angel Services

| Service | Port | Container | Purpose |
|---------|------|-----------|---------|
| Cove Flask | 5002 | `cove-flask` | Hosts Cove + Angel blueprints. TheHillPV.com content engine (angel_web_bp) + Angel chat proxy (angel_chat_bp) |
| Angel Agent | 8004 | `angel-agent` | Claude-powered chat sidecar |

### External Services

| Service | Purpose | Status |
|---------|---------|--------|
| Anthropic API | Angel Agent LLM | Ready (API key required) |
| ATTOM API | Property enrichment | Script exists, needs key activation |
| Twilio | SMS lead notifications | Needs account setup |
| Cloudflare | DNS + CDN for TheHillPV.com | Needs setup |
| Luxury Presence | AngeliqueLyle.com hosting | Active (Angelique's account) |

---

## Data Inventory

| Dataset | Records | Source | Status |
|---------|---------|--------|--------|
| County parcels (APN, geometry, assessed values) | 5,514 | LA County GIS via Cove | LIVE |
| MLS listings (Top Producer export) | 2,368 | CRMLS member export | Loaded (CSV) |
| Closed transactions with prices | 1,489 | Subset of MLS listings | Loaded |
| APN overlap (Cove ∩ CRMLS) | 379 | Computed | Mapped |
| ATTOM enrichment (deed, AVM, schools) | 0 | ATTOM API | Script ready, needs activation |
| Listing events (price changes, status) | ~400 | Agent Hot Sheet exports | Loaded (CSV) |

---

## Lead Flow

```
Organic Search / Social / Referral / Direct
         │
         ▼
    ┌─── Website (any of 3 domains) ───┐
    │                                    │
    │    Content consumed                │
    │    (neighborhood, market, school)  │
    │         │                          │
    │         ▼                          │
    │    Angel Chat Widget               │
    │    "Ask me anything about PV"      │
    │         │                          │
    │    3-10 turns of conversation      │
    │    (parcel lookups, market data)   │
    │         │                          │
    │    "I'd love to connect you        │
    │     with Angelique directly"       │
    │         │                          │
    │    Phone number captured           │
    │         │                          │
    └────────┬───────────────────────────┘
             │
     ┌───────┼───────────┐
     ▼       ▼           ▼
   SMS    Angel DB    Compass CRM
   to     (lead       (async sync)
 Angelique record)
     │
     ▼
  Callback within 4 hours
     │
     ▼
  Listing appointment / Buyer consultation
     │
     ▼
  Transaction
```

---

## Phased Timeline

| Phase | Weeks | Goal | Exit Criteria |
|-------|-------|------|---------------|
| **0 — Foundation** | 1–2 | Data loaded, brand approved | Angelique says yes. Listings in DB. |
| **1 — Agent MVP** | 3–6 | Working chatbot on TheHillPV | Visitor → Angel → SMS to Angelique |
| **2 — Content & Integration** | 7–10 | TheHillPV live + LP integrated | 20+ pages indexed, LP refreshed, widget on both, CRM sync |
| **4 — Optimization** | Ongoing | Growth and refinement | Leads/month growing, SEO ranking |

---

## What Makes This Different

| Dimension | Typical Agent Tech | Angel |
|-----------|-------------------|-------|
| Data | IDX feed (same as everyone) | Proprietary APN-level dataset |
| Website | Template (LP, kvCORE, Chime) | LP flagship + Flask content engine (TheHillPV) |
| AI | Generic chatbot ("an agent will call you") | Conversational AI with local knowledge |
| Voice | Corporate boilerplate | Angelique's actual voice and expertise |
| Lead capture | Form fill → email to agent | Natural conversation → SMS to phone |
| Brand | Brokerage-dependent | Portable — moves with the agent |
| Content | Manual blog posts | Auto-generated from data + editorial review |
| Moat | None (same tools, same data) | Dataset compounds over time |

---

## Relationship to Other GrowDirect Apps

| App | Relationship to Angel |
|-----|----------------------|
| **Cove** | Angel is now a Cove module. Models, blueprints, migrations, and data tables coexist in the Cove repository and database. Angel blueprints are registered in Cove's Flask app. See ADR: docs/decisions/2026-04-06-angel-as-cove-module.md |
| **Canary** | Architecture pattern donor. Angel Agent follows Canary's QA Agent sidecar pattern (GRO-326). Same Anthropic SDK wrapper, same tool dispatch loop, same stateless design. |
| **Memory Bus** | Future — Angel shipping sessions logged to platform memory for cross-app learning. |

---

## Open Questions

1. **LP widget injection** — Can Luxury Presence sites accept custom `<script>` tags? Needs investigation with LP support or Angelique's account settings.

2. **CRMLS API access** — Jeffe has member access for manual exports. Getting RESO Web API access requires a license agreement through the broker. Timeline and process TBD.

3. **Compass CRM API** — Does Compass expose a CRM API for contact/pipeline sync? Or do we use their import tools (CSV, email forwarding)? Needs investigation.

4. **ATTOM pricing post-trial** — Free trial gives 1,000 calls/day for 30 days. After trial, what tier do we need for ongoing enrichment of ~5,500 parcels?

5. **OwnPalosVerdes.com recovery** — How badly is the domain penalized? Need to audit with Google Search Console after cleanup to assess if SEO investment is worth it.

6. **Angelique's response** — Everything depends on her saying yes. The pitch strategy is in brand-and-launch.md, but we don't know until we present.

---

*Angel System Overview — GrowDirect Inc.*
