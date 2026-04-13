# Angel Agent Sidecar + Core Tools

**Date:** 2026-04-13
**Linear:** GRO-461 (sidecar) + GRO-462 (tools)
**Status:** Design approved, pending implementation plan

---

## Goal

Build the Angel Agent sidecar and its first 4 tools so that a user can have a
data-backed conversation about Palos Verdes real estate. The sidecar runs as a
standalone container on port 8004, receives chat messages proxied from Cove
Flask, dispatches tools against the Cove database, and returns conversational
responses powered by Claude.

**First use case:** Angelique and team testing locally — "I'm looking at homes
in Lunada Bay under $3M" triggers listing_search; "What's the market like?"
triggers market_stats; "Tell me about 1234 Granvia Altamira" triggers
parcel_lookup.

---

## Architecture

```
Browser / curl
    → POST /angel/chat (Cove Flask, port 5002)
        → POST http://angel-agent:8004/chat (httpx proxy, 120s timeout)
            → Anthropic API (claude-sonnet-4-20250514, 4096 max_tokens)
            → Tool dispatch loop (max 10 iterations)
                → SQLAlchemy queries against cove DB (read-only)
            → Response dict
        ← JSON response
    ← JSON to client
```

**Pattern donor:** Canary QA Agent (`Canary/canary/services/qa_agent/`). Raw
ASGI app, no web framework in the sidecar. Adapted for consumer-facing
constraints (read-only, Fair Housing guardrails).

**Database access:** Standalone SQLAlchemy engine from `DATABASE_URL` env var.
Imports model classes from `cove.models` (which use `db.Model` from
Flask-SQLAlchemy). This requires `flask-sqlalchemy` as a dependency even though
the sidecar doesn't run Flask — the model metadata must be initialized. The
`db.py` module creates a standalone engine and binds it to the existing model
metadata. Read-only — no commits, no writes.

**Data model note:** Property characteristics (bedrooms, bathrooms, sqft,
year_built, address, city, mls_area, property_type, architectural_style) live
on the `Parcel` model (`parcels` table), NOT on `Listing`. Transaction data
(mls_number, status, prices, dates, DOM, agents) lives on `Listing`. All tools
that return property data must JOIN through `listing.parcel` (via the
`listings.apn` → `parcels.apn` FK). Listings with NULL APN will return partial
data (transaction only, no property characteristics).

---

## Deliverables

### 1. Sidecar Server

**File:** `Cove/cove/services/angel_agent/server.py`

Raw ASGI app with two endpoints:

- `POST /chat` — accepts `{"messages": [...], "session_id": "optional"}`,
  returns `{"text": "...", "tool_calls": [...], "model": "...", "usage": {...}}`
- `GET /health` — returns `{"service": "angel-agent", "status": "healthy",
  "tools_loaded": N, "daily_usage": N, "daily_limit": N}`

**Tool dispatch loop:**
1. Call `client.messages.create()` with system prompt + tool definitions +
   messages.
2. If response contains `tool_use` blocks, execute each tool via
   `execute_tool()`, collect results.
3. Append assistant response + tool results to message history.
4. Re-call Claude. Repeat up to 10 iterations.
5. On final text response (no tool_use), extract text and return.
6. Truncate tool results at 8KB to prevent token bloat.

**Rate limiting:** In-memory dicts. 30 messages/session, 150/day per IP.
Returns early with a friendly message when exceeded. Resets on container
restart — acceptable for testing phase.

**Model:** `claude-sonnet-4-20250514`, max_tokens 4096.

**Entry point:** `uvicorn cove.services.angel_agent.server:app --host 0.0.0.0 --port 8004`

### 2. System Prompt

Three layers concatenated into one system string:

**Layer 1 — Identity:**
> You are Angel, Angelique Lyle's AI real estate assistant for the Palos Verdes
> peninsula. Angelique is a Compass agent (DRE# 01475592, 310.751.8335).
> You help prospective buyers and sellers understand the peninsula's
> neighborhoods, pricing, and market conditions using real MLS data.

**Layer 2 — Knowledge context:**
Static string with peninsula geography (RPV, PVE, RHE, RH, San Pedro),
neighborhood names mapped to MLS areas, and a one-paragraph market overview.
Not generated per-request — keeps latency low.

**Layer 3 — Tool instructions:**
When to use each tool, what they return. Explicit instruction to lead with
specific data (not vague qualifiers), cite sources ("based on 61 closings in
2025"), and never fabricate numbers.

**Fair Housing guardrails (embedded in system prompt):**
- Never steer based on race, color, religion, sex, national origin, familial
  status, or disability.
- Never characterize a neighborhood as "safe," "good," "family-friendly,"
  "up-and-coming," or any demographic descriptor.
- Answer questions about schools, parks, walkability with factual data only.
- If asked about neighborhood demographics, decline and redirect to census.gov.

**DRE disclosure:** Include `CA DRE# 01475592` in every response that
discusses pricing, market conditions, or property recommendations.

### 3. Tool Registry and Dispatch

**File:** `Cove/cove/services/angel_agent/tools.py`

**Registry:** `TOOL_DEFINITIONS` list in Anthropic tool schema format.
`get_tool_definitions()` returns the list. `execute_tool(name, params)`
dispatches to handler functions.

**DB session pattern:** Each `execute_tool()` call creates a session from the
standalone engine, uses it in a try/finally, closes on exit. Read-only.

**4 implemented tools + 8 stubs:**

#### parcel_lookup

- **Purpose:** Look up a property by APN, address, or MLS number.
- **Input:** `{"query": "string"}`
- **Query type detection:**
  - Matches `^\d{4}-\d{3}-\d{3}$` or `^\d{10}$` → APN lookup (normalize to
    dashed format, query `parcels.apn` joined to `listings`)
  - Matches `^\d{2}-\d+$` or all digits 5-9 chars → MLS# lookup on
    `listings.mls_number` (joined to `parcels` for property data)
  - Otherwise → address fragment `ILIKE '%query%'` on
    `parcels.address || ' ' || parcels.city` (joined to `listings` for
    transaction data)
- **Output:**
  ```json
  {
    "summary": "3 bed / 2 bath, 1,850 sqft ranch in Lunada Bay — closed at $2.5M in Sep 2025",
    "address": "1234 Granvia Altamira, Rancho Palos Verdes",
    "apn": "7573-006-008",
    "mls_number": "SB25-12345",
    "status": "Closed",
    "list_price": 2595000,
    "close_price": 2500000,
    "bedrooms": 3,
    "bathrooms": 2,
    "sqft": 1850,
    "lot_sqft": 7500,
    "year_built": 1965,
    "dom": 25,
    "property_type": "Single Family Residence",
    "last_sale_date": "2025-09-15",
    "has_parcel_record": true
  }
  ```
- **Multiple matches:** If address fragment returns multiple results, return up
  to 5 with a note: "Multiple properties match — here are the closest."
- **No match:** Return `{"summary": "No property found matching 'query'", "results": []}`

#### listing_search

- **Purpose:** Search active/recent listings by area, price, beds, status, type.
- **Input:**
  ```json
  {
    "area": "string — city name, MLS area name, or 'peninsula'",
    "status": "Active | Closed | Pending | all (default: Active)",
    "min_price": "integer | null",
    "max_price": "integer | null",
    "min_beds": "integer | null",
    "property_type": "SFR | Condo | all (default: all)",
    "limit": "integer (default: 10, max: 25)"
  }
  ```
- **Area resolution:** JOIN `listings` to `parcels` via APN. Match `area`
  against `parcels.city` (case-insensitive) first. If no match, try
  `parcels.mls_area` (ILIKE). "peninsula" or "PV" or "palos verdes" matches
  all. Recognized city aliases: RPV → Rancho Palos Verdes, PVE → Palos Verdes
  Estates, RHE → Rolling Hills Estates, RH → Rolling Hills.
- **Property type mapping:** "SFR" matches `parcels.property_type ILIKE '%Single Family%'`.
  "Condo" matches `parcels.property_type ILIKE '%Condo%'`. V1 only supports
  SFR, Condo, and "all". Other types (Townhouse, Land/Lot) are included in
  "all" results but not filterable individually.
- **Price filter:** Uses `list_price` for Active/Pending, `close_price` for
  Closed.
- **Sort:** Active/Pending by `list_date DESC`, Closed by `close_date DESC`.
- **Output:**
  ```json
  {
    "summary": "8 active listings in Lunada Bay under $3M",
    "total_matches": 8,
    "results": [
      {
        "address": "1234 Via Coronel",
        "mls_number": "SB26-001",
        "status": "Active",
        "list_price": 2795000,
        "bedrooms": 4,
        "bathrooms": 3,
        "sqft": 2400,
        "dom": 12,
        "property_type": "Single Family Residence"
      }
    ]
  }
  ```

#### market_stats

- **Purpose:** Market statistics for an area over a time period.
- **Input:**
  ```json
  {
    "area": "string — city, MLS area, or 'peninsula'",
    "period_type": "monthly | quarterly | annual (default: monthly)"
  }
  ```
- **Query:** Fetch the most recent `market_snapshots` row matching area +
  period_type + area_type. Use pre-computed `yoy_median_price_change` and
  `yoy_closed_count_change` columns directly — do NOT fetch a second row.
- **Area resolution:** Same alias mapping as listing_search. The
  `market_snapshots.area` field stores city names and MLS area names. The
  `area_type` column (`mls_area`, `city`, `peninsula`) must also be filtered:
  city names → `area_type='city'`, MLS area names → `area_type='mls_area'`,
  "peninsula" → `area_type='peninsula'`.
- **Property type filter:** Default to `property_type='All'` in the snapshot
  query. The unique constraint is `(period_type, period_start, area, area_type,
  property_type)` — omitting property_type could return multiple rows.
- **Output:**
  ```json
  {
    "summary": "Lunada Bay (Mar 2026): median $2.56M, 7 days on market, 6 closings",
    "area": "Lunada Bay",
    "period": "Mar 2026",
    "period_type": "monthly",
    "active_count": 12,
    "closed_count": 6,
    "median_list_price": 2795000,
    "median_close_price": 2560000,
    "median_dom": 7,
    "median_ppsf": 1027,
    "inventory_months": 2.0,
    "list_to_close_ratio": 1.018,
    "yoy_median_price_change_pct": -15.4,
    "yoy_closed_count_change_pct": 0.0
  }
  ```

#### listing_detail

- **Purpose:** Full detail for a specific MLS number.
- **Input:** `{"mls_number": "string"}`
- **Query:** Single-row lookup on `listings.mls_number`. Also fetch
  `listing_events` for this MLS number.
- **Output:** Everything in parcel_lookup output plus: `remarks`,
  `architectural_style`, `hoa_fee`, `virtual_tour_url`, `listing_agent_name`,
  `listing_office`, `buyer_agent_name`, `buyer_office`, `events` (list of
  `{event_type, event_date, old_value, new_value}`).

#### Stub tools (8 remaining)

These return `{"error": "not_implemented", "message": "This tool is coming soon."}`:

- parcel_history, nearby_parcels (need ATTOM — GRO-459)
- neighborhood_profile, school_info, commute_estimate (need structured wiki access)
- cma_summary, listing_strategy (Phase 2)
- capture_lead (need leads table — GRO-464)

Stubs are registered in `TOOL_DEFINITIONS` with full schemas so Claude knows
they exist and can tell the user "I can't do that yet, but I will be able to
soon."

### 4. Docker Setup

**`Cove/Dockerfile.angel-agent`:**
- Base: `python:3.12-slim`
- Install: `uvicorn`, `anthropic`, `sqlalchemy`, `flask-sqlalchemy`,
  `psycopg2-binary` (flask-sqlalchemy required for model metadata, not for HTTP)
- Copy: `cove/models/`, `cove/services/angel_agent/`, `cove/__init__.py`,
  `cove/extensions.py` (needed for `db.Model` base class)
- Entry: `uvicorn cove.services.angel_agent.server:app --host 0.0.0.0 --port 8004`
- Port: 8004

**`Cove/devops/docker-compose.yml` addition:**
```yaml
angel-agent:
  image: cove-angel-agent
  build:
    context: ../
    dockerfile: Dockerfile.angel-agent
  container_name: cove_angel_agent
  ports:
    - "8004:8004"
  environment:
    - DATABASE_URL=postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/cove
    - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    - ANGEL_AGENT_PORT=8004
  networks:
    - growdirect
  restart: unless-stopped
```

**Flask env var:** Set `ANGEL_AGENT_URL=http://angel-agent:8004` in Cove Flask
service environment so the proxy knows where to reach the sidecar on the Docker
network.

### 5. Proxy Update (`chat_routes.py`)

The existing Flask proxy needs 3 changes to match the sidecar contract:

1. **Payload:** Accept `messages` (plural array) + `session_id`, not `message`
   (singular string). Validate `messages` is a non-empty list.
2. **Timeout:** Increase from 30s to 120s (tool dispatch loop can take 10+
   iterations of Claude API calls).
3. **Response passthrough:** Forward the sidecar's `{"text", "tool_calls",
   "model", "usage"}` response shape directly.

### 6. Error Handling

Tool handlers return a standard error shape when things go wrong:
```json
{"error": "database_unavailable", "message": "I'm having trouble looking that up right now."}
```

Error categories:
- `not_found` — query returned no results (not an error for Claude, just empty data)
- `database_unavailable` — DB connection failed
- `invalid_input` — missing or malformed parameters
- `not_implemented` — stub tools

Claude sees the error dict as a tool result and responds conversationally
("I wasn't able to find that property" or "Let me try a different search").

### 7. Tests

**`Cove/tests/angel_agent/test_tools.py`:**
- Fixtures: seed 5-10 listings with linked parcels (mixed areas, statuses,
  prices), 2-3 market snapshots (with area_type set), 1-2 standalone parcels
  without listings for APN-only lookup testing.
- `test_parcel_lookup_by_apn` — dashed APN returns property card
- `test_parcel_lookup_by_mls` — MLS# returns correct listing
- `test_parcel_lookup_by_address` — partial address returns matches
- `test_parcel_lookup_no_match` — unknown query returns empty
- `test_listing_search_by_area` — filters by city correctly
- `test_listing_search_by_price_range` — min/max filters work
- `test_listing_search_peninsula_wide` — "peninsula" returns all areas
- `test_listing_search_limit` — respects limit parameter
- `test_market_stats_monthly` — returns most recent snapshot
- `test_market_stats_yoy` — includes YoY comparison
- `test_listing_detail` — returns full record + events
- `test_listing_detail_not_found` — unknown MLS# returns error
- `test_listing_search_alias_rpv` — "RPV" resolves to Rancho Palos Verdes
- `test_market_stats_area_type` — city vs mls_area resolution works
- `test_parcel_lookup_no_listing` — APN with parcel but no listing returns parcel data only
- `test_listing_no_parcel` — listing with NULL APN returns transaction data only

**`Cove/tests/angel_agent/test_server.py`:**
- Uses httpx `AsyncClient` against the ASGI app directly.
- `test_health_check` — 200, correct shape
- `test_chat_returns_response` — mock Anthropic to return text, verify shape
- `test_tool_dispatch` — mock Anthropic to return tool_use, verify tool
  executes and result is returned
- `test_rate_limit_session` — exceed session limit, verify 200 with limit
  message
- `test_rate_limit_daily` — exceed daily limit, verify 200 with limit message

**No live Anthropic API calls in CI.** All Claude responses mocked. A separate
`scripts/smoke_test_angel.py` hits the real API for manual verification.

---

## File Layout

```
Cove/cove/services/angel_agent/
├── __init__.py
├── server.py          — ASGI app, /chat + /health, dispatch loop
├── tools.py           — tool definitions, execute_tool(), 4 handlers + 8 stubs
├── system_prompt.py   — 3-layer prompt builder (identity, knowledge, tools)
└── db.py              — standalone engine + sessionmaker from DATABASE_URL

Cove/tests/angel_agent/
├── conftest.py        — DB fixtures (listings, snapshots, parcels)
├── test_tools.py      — unit tests for each tool handler
└── test_server.py     — integration tests for ASGI app

Cove/Dockerfile.angel-agent
Cove/devops/docker-compose.yml  (modified — add angel-agent service)
```

---

## Out of Scope

- Chat widget JS embed (GRO-463)
- Lead capture / leads table (GRO-464)
- ATTOM enrichment tools (GRO-459)
- Community/strategy tools (Phase 2)
- Valkey-backed rate limiting (production concern)
- Production deployment / Cloudflare / SSL
- Conversation persistence (stateless — history lives in the client)

---

## Dependencies

| Dependency | Status | Required for |
|---|---|---|
| `listings` table populated | Done (2,368 rows) | parcel_lookup, listing_search, listing_detail |
| `market_snapshots` table populated | Done (1,250 rows) | market_stats |
| `parcels` table populated | Done (5,514 rows) | parcel_lookup APN bridge, property data |
| `listing_events` table | Done (schema exists) | listing_detail events |
| Anthropic API key | Available | Claude calls |
| Docker shared network (`growdirect`) | Done | Container networking |
| Flask proxy (`chat_routes.py`) | Done (needs update) | Proxying to sidecar (payload + timeout changes) |

---

## Success Criteria

1. `docker compose up angel-agent` starts and `/health` returns 200.
2. `POST /chat {"messages": [{"role": "user", "content": "What homes are active in Lunada Bay under $3M?"}]}` returns a response with real listing data.
3. `POST /chat` with "What's the market like in Valmonte?" returns real market stats with median prices and DOM.
4. `POST /chat` with "Tell me about MLS# SB25-12345" returns a property card.
5. All pytest tests pass against `cove_test` database.
6. Rate limiting triggers at configured thresholds.
7. Fair Housing guardrails prevent demographic steering in responses.
