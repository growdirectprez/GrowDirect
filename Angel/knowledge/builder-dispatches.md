# Angel Builder Dispatches — First Sessions

> **Created:** 2026-04-06 by ALX
> **Purpose:** Copy-paste each dispatch into a Claude Code session for the Angel builder.
> **Rules:** One GRO issue per session. Builder reads CLAUDE.md first, then executes factory pipeline.

---

## Dispatch 1: GRO-457 — Import CRMLS Listings to Angel Database

**Priority:** Urgent | **Phase:** 0 — Foundation | **Blocks:** GRO-462, GRO-466, GRO-467
**Branch:** `gro-457-import-crmls-listings-to-angel-database`

```
You are the Angel builder. Read these files first, in order:
1. ~/GrowDirect/CLAUDE.md (platform standards)
2. ~/GrowDirect/Cove/CLAUDE.md (Cove app context — Angel lives here)
3. ~/GrowDirect/Angel/CLAUDE.md (Angel domain context)
4. ~/GrowDirect/docs/sdds/angel/data-platform.md §4 and §5

ISSUE: GRO-457 — Import CRMLS listings to Angel database
LINEAR: https://linear.app/growdirect/issue/GRO-457
BRANCH: gro-457-import-crmls-listings-to-angel-database

CONTEXT:
Angel is a Cove module. All code goes in ~/GrowDirect/Cove/. All models,
migrations, blueprints live there. Angel/ is a knowledge + data repo only.

GRO-458 (Add Angel models and blueprints to Cove) is DONE. The listings,
listing_events, leads, and market_snapshots models already exist in
Cove/cove/models/. Verify they're there before writing migrations.

SOURCE DATA (6 Top Producer CSV batches — 2,368 listings total):
  ~/GrowDirect/Angel/Top Producer - Residential/Top Producer - Residential.tp
  ~/GrowDirect/Angel/Top Producer - Residential-2/Top Producer - Residential.tp
  ~/GrowDirect/Angel/Top Producer - Residential-3/Top Producer - Residential.tp
  ~/GrowDirect/Angel/Top Producer - Residential-4/Top Producer - Residential.tp
  ~/GrowDirect/Angel/Top Producer - Residential-5/Top Producer - Residential.tp
  ~/GrowDirect/Angel/Top Producer - Residential-6/Top Producer - Residential.tp

HOT SHEET DATA (Agent Hot Sheet CSVs → listing_events):
  ~/GrowDirect/Angel/Agent Hot Sheet.csv
  ~/GrowDirect/Angel/Agent Hot Sheet-2.csv
  ~/GrowDirect/Angel/Agent Hot Sheet-3.csv
  ~/GrowDirect/Angel/Agent Hot Sheet-4.csv
  ~/GrowDirect/Angel/Agent Hot Sheet-5.csv

SCOPE:
1. Check if Alembic migration for listings + listing_events tables exists.
   If not, create it. Schema is in docs/sdds/angel/data-platform.md §4.1, §4.2.
2. Write Cove/scripts/import_crmls.py:
   - Read .tp files (they're CSVs with 214 columns)
   - Normalize APNs to dashed format (XXXX-XXX-XXX)
   - Deduplicate by MLS# (upsert on conflict)
   - Parse dates, prices, coordinates
   - Store full raw row in raw_data JSONB column
   - Track batch_id per import run
3. Write Cove/scripts/import_hot_sheet.py:
   - Hot Sheet CSVs → listing_events table
   - Link to listings by MLS#
4. Run both scripts against all batches
5. Write pytest tests for models + import scripts

ACCEPTANCE CRITERIA:
- listings table has ~2,368 rows with unique MLS numbers
- listing_events table populated from hot sheet data
- All APNs in dashed format (XXXX-XXX-XXX)
- pytest passes for model + import script
- Batch provenance tracked (batch_id on every row)

FACTORY PIPELINE: Run all 9 stages. Start with preflight.
Update GRO-457 status to In Progress when you start, Done when complete.
```

---

## Dispatch 2: GRO-461 — Build Angel Agent Sidecar

**Priority:** Urgent | **Phase:** 1 — Agent MVP | **Blocked by:** GRO-458 (Done)
**Branch:** `gro-461-build-angel-agent-sidecar-serverpy-tool-dispatch`

```
You are the Angel builder. Read these files first, in order:
1. ~/GrowDirect/CLAUDE.md (platform standards)
2. ~/GrowDirect/Cove/CLAUDE.md (Cove app context — Angel lives here)
3. ~/GrowDirect/Angel/CLAUDE.md (Angel domain context)
4. ~/GrowDirect/docs/sdds/angel/angel-agent.md (full agent spec)
5. ~/GrowDirect/Angel/knowledge/agentic-profile.md (Angelique's voice)

PATTERN REFERENCE — read the Canary QA Agent you're copying from:
6. ~/GrowDirect/Canary/canary/services/qa_agent/ (all files)

ISSUE: GRO-461 — Build Angel Agent sidecar (server.py + tool dispatch)
LINEAR: https://linear.app/growdirect/issue/GRO-461
BRANCH: gro-461-build-angel-agent-sidecar-serverpy-tool-dispatch

CONTEXT:
Angel Agent is a Claude-powered chatbot sidecar on port 8004. It follows
the exact same pattern as Canary's QA Agent (GRO-326) but is consumer-facing
(read-only tools, no operator context, Fair Housing guardrails).

The sidecar is a separate container added to Cove/devops/docker-compose.yml.
It does NOT run inside the Cove Flask process. It's an ASGI server (uvicorn)
that Cove's angel_chat_bp proxies to via HTTP.

SCOPE:
1. Create Cove/cove/services/angel_agent/server.py
   - uvicorn ASGI app
   - POST /chat — accepts messages, returns Claude response
   - GET /health — returns tool count, uptime
2. Create Cove/cove/services/angel_agent/agent.py
   - Flask-side HTTP proxy to sidecar
   - Used by angel_chat_bp to forward chat requests
3. Create Cove/cove/services/angel_agent/tools.py
   - Tool registry and dispatch
   - Stub tool definitions (actual implementations come in GRO-462)
4. Create Cove/Dockerfile.angel-agent (Python 3.12, port 8004)
5. Add angel-agent service to Cove/devops/docker-compose.yml
   - image: angel-agent (follows Docker image naming rule)
   - Port 8004
   - Joins growdirect network
   - Reads from cove database
6. System prompt with 3-layer architecture:
   Layer 1 — Identity: "You are Angel, Angelique Lyle's AI assistant..."
   Layer 2 — Knowledge context: loaded from Angel/knowledge/ files
   Layer 3 — Tool instructions: when/how to use each tool
   Include: Fair Housing Act compliance, CA DRE# 01475592 disclosure
7. Rate limiting: 30 messages/session, 150/day per IP

ACCEPTANCE CRITERIA:
- angel-agent container starts on port 8004
- Health check returns tool count and uptime
- POST /chat with test messages returns Claude response
- Tool dispatch loop works (max 10 iterations)
- System prompt includes Fair Housing + DRE disclosure
- Rate limiting enforced (Valkey-backed counters)
- pytest coverage for server, agent proxy, tool dispatch

FACTORY PIPELINE: Run all 9 stages. Start with preflight.
Update GRO-461 status to In Progress when you start, Done when complete.
```

---

## Dispatch 3: GRO-462 — Implement Core Agent Tools

**Priority:** Urgent | **Phase:** 1 — Agent MVP | **Blocked by:** GRO-457 + GRO-458 (both must be Done)
**Branch:** `gro-462-implement-core-agent-tools-parcel_lookup-listing_search`

```
You are the Angel builder. Read these files first, in order:
1. ~/GrowDirect/CLAUDE.md (platform standards)
2. ~/GrowDirect/Cove/CLAUDE.md (Cove app context)
3. ~/GrowDirect/Angel/CLAUDE.md (Angel domain context)
4. ~/GrowDirect/docs/sdds/angel/angel-agent.md §4.1, §4.2 (tool specs)
5. ~/GrowDirect/docs/sdds/angel/data-platform.md (data model)
6. ~/GrowDirect/Angel/knowledge/market-knowledge.md (neighborhoods)

PREREQUISITE CHECK:
- GRO-457 must be Done (listings table populated with ~2,368 rows)
- GRO-461 must be Done (agent sidecar running with stub tools)
If either is not done, STOP and report back. Do not proceed.

ISSUE: GRO-462 — Implement core Agent tools: parcel_lookup, listing_search, market_stats
LINEAR: https://linear.app/growdirect/issue/GRO-462
BRANCH: gro-462-implement-core-agent-tools-parcel_lookup-listing_search

SCOPE:

### Tool 1: parcel_lookup
- Input: APN, address fragment, or MLS#
- Query: Angel listings table + Cove parcels (native JOIN, same DB)
- Output: Summarized property card:
  address, beds/baths/sqft, year built, lot size, status, last sale price,
  days on market, listing agent, APN
- Fallback order: try APN match → address ILIKE → MLS# exact

### Tool 2: listing_search
- Input: area (RPV/PVE/RHE/RH/peninsula), status, price range, beds, property type
- Query: Angel listings with filters
- Output: Up to 25 matching listings, sorted by relevance (status > recency)
- Areas map to city/community values in the data

### Tool 3: market_stats
- Input: area, time period (month/quarter/year)
- Query: Aggregate from listings where status = Closed
- Output: active count, closed count, median sold price, median DOM,
  months of inventory, list-to-close price ratio, YoY change

IMPLEMENTATION:
- Tools go in Cove/cove/services/angel_agent/tools.py
- Each tool is a function registered in the tool_definitions dict
- Tool outputs are SUMMARIZED text, not raw JSON dumps
- The agent presents data conversationally, not as tables

ACCEPTANCE CRITERIA:
- All 3 tools registered in tool_definitions
- parcel_lookup resolves APN, address, and MLS# queries
- listing_search filters work for all parameter combinations
- market_stats returns accurate aggregations (verify against raw SQL)
- Tool outputs are human-readable summaries
- pytest coverage for each tool function

FACTORY PIPELINE: Run all 9 stages. Start with preflight.
Update GRO-462 status to In Progress when you start, Done when complete.
```

---

## Dispatch 4: GRO-459 — Activate ATTOM Enrichment (Parallel Track)

**Priority:** High | **Phase:** 0 — Foundation | **Can run parallel to Dispatch 1**
**Branch:** `gro-459-activate-attom-enrichment-for-angel-parcels`

```
You are the Angel builder. Read these files first, in order:
1. ~/GrowDirect/CLAUDE.md (platform standards)
2. ~/GrowDirect/Cove/CLAUDE.md (Cove app context)
3. ~/GrowDirect/Angel/CLAUDE.md (Angel domain context)
4. ~/GrowDirect/docs/sdds/angel/data-platform.md §2, §5.2

EXISTING CODE — read the Cove enrichment script you're extending:
5. ~/GrowDirect/Cove/scripts/enrich_attom.py

ISSUE: GRO-459 — Activate ATTOM enrichment for Angel parcels
LINEAR: https://linear.app/growdirect/issue/GRO-459
BRANCH: gro-459-activate-attom-enrichment-for-angel-parcels

CONTEXT:
Cove already has 5,514 parcels in research_parcels. The ATTOM enrichment
script exists at Cove/scripts/enrich_attom.py. This issue activates the
ATTOM API trial and runs enrichment against the 379 APNs that overlap
between CRMLS listings and Cove parcels.

NOTE: This issue requires an ATTOM API key. If the key is not yet in .env,
STOP after writing the code and report that the key is needed. Do not
attempt to fabricate or skip the API integration.

SCOPE:
1. Verify ATTOM API key exists in Cove/.env (ATTOM_API_KEY)
   - If missing, write the code but skip the run step. Report back.
2. Identify the 379 overlap APNs:
   - Query: APNs that exist in BOTH Cove research_parcels AND Angel listings
   - This requires GRO-457 to be done (listings populated)
   - If listings table is empty, write code but report dependency.
3. Extend enrich_attom.py (or create angel-specific wrapper):
   - Property detail endpoint
   - Sale detail endpoint (deed history)
   - Assessment detail endpoint (AVM)
   - School detail endpoint
4. Enrichment writes to Cove's research_parcels table (shared benefit)
   - Angel reads via native JOIN (same database, per ADR)
5. Respect rate limits: 1,000 calls/day on free trial
   - Batch in groups, track progress, support resume on failure

ACCEPTANCE CRITERIA:
- ATTOM API key configured in .env (or documented as needed)
- Overlap APN query works (returns ~379 APNs)
- Enrichment script handles all 4 endpoints
- Writes to research_parcels with ATTOM data columns
- Script is resumable (tracks last enriched APN)
- Rate limiting respected
- pytest for enrichment logic (mock API responses)

FACTORY PIPELINE: Run all 9 stages. Start with preflight.
Update GRO-459 status to In Progress when you start, Done when complete.
```

---

## Execution Order

```
Session 1: GRO-457 (CRMLS import)        ← START HERE, unblocked
Session 2: GRO-461 (Agent sidecar)       ← parallel to Session 1, unblocked
Session 3: GRO-459 (ATTOM enrichment)    ← parallel, needs API key
Session 4: GRO-462 (Core agent tools)    ← blocked by 457 + 461
```

Sessions 1 and 2 can run simultaneously — no dependency between them.
Session 3 can run parallel but may pause waiting for ATTOM API key.
Session 4 must wait for both 1 and 2 to complete.

---

## Notes for Jeffe

- Each dispatch is self-contained. Copy the text inside the ``` block and paste into a fresh Claude Code session.
- The builder will read CLAUDE.md files, then execute the factory pipeline (preflight → research → blueprint → TDD → assembly → verify → QA → ship → close).
- Builder updates Linear status automatically at start (In Progress) and end (Done).
- If a builder hits a blocker, it reports back. Don't force past blockers — create a new GRO issue for the blocker.
- Two new GRO issues to create when ready:
  1. **Newsletter OCR pipeline** — extend Cove archive pipeline to OCR Compass Marketing Center newsletter images for voice training data
  2. **Gmail alert ingestion** — import Compass listing alert emails (reply-to-agent@compass.com) into listing_events as status change signals
