# Angel Agent

> **Type:** MCP Server (Angel)
> **Status:** Active — early production, 4 of 12 tools implemented
> **Namespace:** `cove.services.angel_agent`
> **Port:** 8004 (uvicorn ASGI sidecar)
> **Owner:** ALX (COO) / Jeffe (CEO)
> **Last reviewed:** 2026-04-13

**Wiki:** [[Brain/wiki/angel-architecture|Angel Architecture]] · [[Brain/wiki/south-bay-wiki-architecture|South Bay Wiki Architecture]] · [[Brain/projects/Angel|Angel MOC]]
**Parent:** [[docs/sdds/angel/angel-overview|Angel Overview]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[docs/team/Architect|Architect]] · **Operator role:** [[docs/team/ALX|ALX]]

---

## Purpose

Angel Agent is a Claude-powered conversational sidecar that answers questions about every property on the Palos Verdes peninsula. It runs as a standalone ASGI container (port 8004), accepts chat requests proxied from Cove Flask (port 5002), dispatches tool calls against the Cove database for parcel and listing data, and returns natural-language responses to a JavaScript chat widget. When a conversation reaches a decision point, the `capture_lead` tool (stub, not yet implemented) will collect visitor contact info and route it to Angelique Lyle via SMS.

**What makes it different from generic real estate chatbots:** proprietary APN-level data for 5,500+ parcels, 2,368 MLS listing records with transaction history, Cove community governance data, and Angelique's actual voice via personality-first prompting.

---

## Dependencies

| Dependency | Type | Required | Notes |
|-----------|------|:--------:|-------|
| Cove Flask (port 5002) | Upstream proxy | Yes | `angel_chat_bp` proxies `/chat` and `/health` to sidecar |
| PostgreSQL (`cove` database) | Data store | Yes | Read-only access to `parcels`, `listings`, `listing_events`, `market_snapshots` |
| Anthropic API | External API | Yes | `claude-sonnet-4-20250514`, `ANTHROPIC_API_KEY` env var |
| `growdirect` Docker network | Infrastructure | Yes | Shared network for DB connectivity |

**Not currently required (future):** Valkey (visitor session tracking), ATTOM API (deed/ownership enrichment), Twilio/SMS provider (lead notification), Compass CRM API (lead sync).

---

## Data Flow & PII Map

### What Enters

| Source | Data | Format | Contains PII |
|--------|------|--------|:------------:|
| Chat widget (browser) | Conversation messages, session_id | JSON POST to Cove Flask `/chat` | No (currently) |
| Widget context (planned) | page_url, referrer, session_id, turn_count | JSON fields in payload | session_id is pseudonymous |
| Cove Flask proxy | Forwarded request body | JSON POST to sidecar `/chat` | No |

### What's Stored

| Store | Data | Encryption | PII Classification |
|-------|------|:----------:|:------------------:|
| PostgreSQL `parcels` table | APN, address, city, beds/baths/sqft, year built | Plaintext | **public** — property records |
| PostgreSQL `listings` table | MLS#, prices, DOM, agent names, remarks | Plaintext | **public** — MLS data |
| PostgreSQL `market_snapshots` table | Median prices, DOM, inventory by area/period | Plaintext | **public** — aggregate stats |
| In-memory `_session_counts` / `_daily_counts` (server.py) | session_id -> message count | None (RAM only) | **internal** — usage tracking |
| ~~Lead records~~ (planned, not built) | ~~name, phone, email, interest, notes~~ | ~~Plaintext~~ | ~~**sensitive** — visitor PII~~ |

### What Exits

| Destination | Data | Contains PII |
|-------------|------|:------------:|
| Chat widget (browser) | Natural language response, tool call metadata, usage stats | No (property data is public) |
| Anthropic API | System prompt + conversation history + tool results | No (currently — no visitor PII in messages) |
| ~~SMS notification~~ (planned) | ~~Lead name, phone, interest~~ | ~~Yes~~ |
| ~~Compass CRM~~ (planned) | ~~Lead contact info, property interest~~ | ~~Yes~~ |

### PII Classification Summary

| Field | Classification | Current State | Required State |
|-------|:-------------:|:-------------:|:--------------:|
| Property addresses, APNs | public | Plaintext | Plaintext (OK) |
| MLS listing data, agent names | public | Plaintext | Plaintext (OK) |
| Visitor session_id | internal | In-memory only | In-memory only (OK) |
| Lead name (planned) | sensitive | Not built | AES-256-GCM at rest |
| Lead phone (planned) | sensitive | Not built | AES-256-GCM at rest |
| Lead email (planned) | sensitive | Not built | AES-256-GCM at rest |
| Conversation history | internal | Not stored server-side | Keep stateless (OK) |

---

## API Contract

### Cove Flask Proxy (angel_chat_bp)

Registered in Cove app at `cove/angel/chat_routes.py`.

| Route | Method | Auth | Rate Limit | Description |
|-------|--------|:----:|:----------:|-------------|
| `/chat` | POST | None (public) | 10 req/min per IP (SDD spec, **not yet enforced in code**) | Proxy to sidecar, 120s timeout |
| `/health` | GET | None | None | Check sidecar health, returns `{"status": "ok"}` or `{"status": "degraded"}` |

### Angel Agent Sidecar (ASGI, port 8004)

Raw ASGI app at `cove/services/angel_agent/server.py`. No framework, no middleware.

| Route | Method | Auth | Rate Limit | Description |
|-------|--------|:----:|:----------:|-------------|
| `/chat` | POST | None | 30/session, 150/day (in-memory) | Tool dispatch loop, returns `{text, tool_calls, model, usage}` |
| `/health` | GET | None | None | Returns `{service, status, tools_loaded, uptime_seconds, daily_usage}` |

**POST `/chat` request body:**
```json
{
  "messages": [{"role": "user", "content": "What's active in Lunada Bay?"}],
  "session_id": "abc123"
}
```

**POST `/chat` response:**
```json
{
  "text": "There are 5 active listings in Lunada Bay...",
  "tool_calls": [{"tool": "listing_search", "input": {"area": "lunada bay"}}],
  "model": "claude-sonnet-4-20250514",
  "usage": {"session_remaining": 29, "daily_remaining": 149}
}
```

---

## MCP Tool Registry

12 tools defined in `cove/services/angel_agent/tools.py`. 4 implemented, 8 stubs.

| Tool | Auth | PII Access | Rate Limit | Status | Description |
|------|:----:|:----------:|:----------:|:------:|-------------|
| `parcel_lookup` | None | public (address, APN) | Sidecar session/daily | **Live** | Look up property by APN, address, or MLS# |
| `listing_search` | None | public (MLS data) | Sidecar session/daily | **Live** | Search listings by area, price, beds, status |
| `market_stats` | None | public (aggregate stats) | Sidecar session/daily | **Live** | Market statistics by area and period |
| `listing_detail` | None | public (MLS data, agent names) | Sidecar session/daily | **Live** | Full listing detail with events/history |
| `parcel_history` | None | public (ownership records) | Sidecar session/daily | **Stub** | Ownership and transaction history |
| `nearby_parcels` | None | public (addresses) | Sidecar session/daily | **Stub** | Properties within radius of APN |
| `neighborhood_profile` | None | none | Sidecar session/daily | **Stub** | Neighborhood character and amenities |
| `school_info` | None | none | Sidecar session/daily | **Stub** | School ratings and feeder patterns |
| `commute_estimate` | None | none | Sidecar session/daily | **Stub** | Drive time to common destinations |
| `cma_summary` | None | public (listing comps) | Sidecar session/daily | **Stub** | Quick comparative market analysis |
| `listing_strategy` | None | public (market data) | Sidecar session/daily | **Stub** | Pricing and timeline recommendations |
| `capture_lead` | None | **sensitive** (name, phone, email) | Sidecar session/daily | **Stub** | Collect visitor contact info for follow-up |

**Tool dispatch flow:** Claude returns `tool_use` blocks -> `execute_tool()` routes to handler or returns stub error -> result serialized to JSON (truncated at 8KB) -> fed back to Claude as `tool_result` -> loop up to 10 iterations.

---

## Cross-App Data Access

### What the agent reads

Angel Agent creates its own SQLAlchemy engine (not Flask's) from `DATABASE_URL` pointing to the `cove` database. It imports Cove models and queries them directly.

| Cove Table | Access | What's Queried | Isolation |
|-----------|:------:|---------------|-----------|
| `parcels` | Read | APN, address, city, beds/baths/sqft, lot_size, year_built, property_type, mls_area, architectural_style | Shared engine, no tenant isolation (single-org) |
| `listings` | Read | mls_number, status, list_price, close_price, dom, dates, remarks, agent names, hoa_fee, virtual_tour_url | Same |
| `listing_events` | Read | event_type, event_date, old_value, new_value for a given MLS# | Same |
| `market_snapshots` | Read | Aggregate stats by area, period_type, property_type | Same |

### What the agent does NOT access

- Member tables (no `members`, `roles`, `member_roles`)
- Governance tables (no `ballots`, `ballot_envelopes`, `proposals`, `elections`)
- Vault documents, treasury, meetings
- No write access to any table

### Tenant isolation

Single-organization deployment (WPBCA/Angel). No multi-tenant isolation needed currently. The sidecar's DB pool (`pool_size=5`) is independent of Flask's connection pool.

---

## Tool Dispatch Security

### Authentication model

**None.** The sidecar has no authentication layer. Any process that can reach port 8004 on the Docker network can call `/chat`. The Cove Flask proxy is the only intended caller.

### Privilege escalation

- All 4 live tools are read-only SELECT queries against public property data
- No tool can write to the database (no INSERT/UPDATE/DELETE)
- The `capture_lead` stub returns a "coming soon" error without executing
- Tool results are truncated to 8KB before being fed to Claude
- `execute_tool()` catches all exceptions and returns a safe error message

### Compromise scenario

If the sidecar container is compromised:
- **Read exposure:** All parcel, listing, and market data in the `cove` database (public property records)
- **No write exposure:** The DB user has write permissions but no tool code issues writes; a compromised process could issue raw SQL
- **Anthropic API key:** Exposed via environment variable; attacker could make API calls on the account
- **No member PII exposure:** Agent does not query member tables
- **Lateral movement:** Container is on the `growdirect` Docker network and could reach PostgreSQL, Valkey, and other containers

---

## System Prompt Architecture

Three-layer prompt assembled in `system_prompt.py`:

| Layer | Content | Tokens (approx) |
|-------|---------|:----------------:|
| Identity | Angel persona, voice rules, compliance disclaimers | ~200 |
| Knowledge Context | Peninsula geography, 17 MLS area mappings, market overview | ~400 |
| Tool Instructions | When to use each tool, citation requirements | ~150 |
| Fair Housing | Federal FHA + California FEHA compliance rules | ~200 |

**Total system prompt:** ~950 tokens. Static (not injected per-request). No visitor context injection is implemented yet.

---

## Operations

### Startup Sequence

1. `uvicorn cove.services.angel_agent.server:app` starts on port 8004
2. First `/chat` request triggers lazy initialization:
   - `db.py._init_engine()` creates SQLAlchemy engine from `DATABASE_URL`
   - `anthropic.Anthropic()` client created per-request (not pooled)
   - `build_system_prompt()` assembles static prompt
3. Health check immediately available at `/health`

### Health Check

`GET /health` on port 8004 — no dependencies checked (does not verify DB or Anthropic connectivity).

```json
{
  "service": "angel-agent",
  "status": "healthy",
  "tools_loaded": 12,
  "uptime_seconds": 86400,
  "daily_usage": 42,
  "daily_limit": 150
}
```

### Failure Modes

| Failure | Impact | Recovery | Detection |
|---------|--------|----------|-----------|
| Anthropic API unreachable | Chat returns "trouble connecting" | Auto-retry on next request | User-visible error message |
| Anthropic API key missing | Chat returns config error message | Set env var, restart container | `/health` still returns "healthy" (gap) |
| PostgreSQL unreachable | Tool calls return "database unavailable" | DB connection pool auto-reconnects (`pool_pre_ping=True`) | Tool error in response |
| Sidecar container down | Cove Flask proxy returns 503 | Docker restart policy (`unless-stopped`) | Flask logs "sidecar unreachable" |
| Rate limit hit (30/session) | User told to start new conversation | Reset by new session_id | Usage stats in response |
| Rate limit hit (150/day) | User told to try tomorrow | Daily counter resets at midnight UTC | Usage stats in response |

### Monitoring

**Currently implemented:**
- In-memory counters: `_session_counts`, `_daily_counts` (lost on container restart)
- Uvicorn access logs (stdout)
- Tool dispatch logging (`logger.info("Angel -> tool: ...")`)

**Not implemented (see findings):**
- No persistent metrics (Valkey counters described in SDD are aspirational)
- No alerting
- No conversation-level logging or analytics
- No Anthropic API cost tracking

### Configuration

| Env Var | Default | Description |
|---------|---------|-------------|
| `ANTHROPIC_API_KEY` | (none, required) | Claude API authentication |
| `DATABASE_URL` | (none, required) | PostgreSQL connection string |
| `ANGEL_AGENT_MODEL` | `claude-sonnet-4-20250514` | Claude model for inference |
| `ANGEL_AGENT_PORT` | `8004` | Sidecar listen port |

**Hardcoded constants in server.py:**
- `MAX_TOKENS = 4096`
- `MAX_TOOL_ITERATIONS = 10`
- `MAX_TOOL_RESULT_BYTES = 8000`
- `MAX_MESSAGES_PER_SESSION = 30`
- `MAX_MESSAGES_PER_DAY = 150`

---

## Deployment

### Docker Service Definition

```yaml
# Cove/devops/docker-compose.yml
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

**Dockerfile** (`Cove/Dockerfile.angel-agent`): Python 3.12-slim, installs uvicorn + anthropic + sqlalchemy + psycopg2-binary. Copies only model files and `services/angel_agent/` — no Flask app, no templates, no static assets.

### AWS Target

| Component | AWS Service | Notes |
|-----------|-------------|-------|
| Sidecar container | ECS Fargate | 0.5 vCPU, 1 GB RAM |
| Database | RDS PostgreSQL 17 | Shared with Cove |
| Secrets | Secrets Manager | `ANTHROPIC_API_KEY`, `DATABASE_URL` |
| Networking | VPC private subnet | Sidecar not internet-facing; Cove ALB proxies |

### CI/CD Requirements

- Build `Dockerfile.angel-agent` on push to `main` (when `cove/services/angel_agent/` or `cove/models/` change)
- Run `tests/angel_agent/` test suite before deploy
- No database migrations owned by the sidecar (it reads Cove's schema)

---

## Code Review Findings

### F-001: No rate limiting on Flask proxy endpoint

| | |
|---|---|
| **Severity** | **P1** — before GA |
| **File** | `cove/angel/chat_routes.py` |
| **Description** | The SDD specifies "10 req/min per IP" on the Flask proxy, but no rate limiting middleware is applied. The sidecar has in-memory session/daily limits but the proxy has none. An attacker can flood the proxy, which forwards every request to the sidecar and Anthropic API. |
| **Recommended fix** | Add Flask-Limiter to `angel_chat_bp` with `10/minute` per remote IP on the `/chat` route. |
| **Linear** | — |

### F-002: No authentication between Flask proxy and sidecar

| | |
|---|---|
| **Severity** | **P1** — before GA |
| **File** | `cove/angel/chat_routes.py`, `cove/services/angel_agent/server.py` |
| **Description** | Any container on the `growdirect` Docker network can call `POST /chat` on port 8004. There is no shared secret, API key, or mTLS between the proxy and sidecar. In production, the sidecar will be on a private subnet, but defense-in-depth requires authentication. |
| **Recommended fix** | Add a `X-Angel-Internal-Key` header check — shared secret from Secrets Manager, validated in the ASGI app before processing. |
| **Linear** | — |

### F-003: Anthropic API key in environment variable, not Secrets Manager

| | |
|---|---|
| **Severity** | **P0** — blocks production |
| **File** | `Cove/devops/docker-compose.yml`, `cove/services/angel_agent/server.py` |
| **Description** | `ANTHROPIC_API_KEY` is passed via Docker Compose environment from `.env` file. In production, this must be in AWS Secrets Manager with `boto3` retrieval at startup. Current pattern risks key exposure in container inspection, ECS task definitions, and CloudWatch logs. |
| **Recommended fix** | Retrieve from Secrets Manager at startup (same pattern as Canary's `crypto.py` for encryption keys). |
| **Linear** | — |

### F-004: Database credentials in environment variable, not Secrets Manager

| | |
|---|---|
| **Severity** | **P0** — blocks production |
| **File** | `Cove/devops/docker-compose.yml`, `cove/services/angel_agent/db.py` |
| **Description** | `DATABASE_URL` with plaintext credentials is passed via Docker Compose environment. The sidecar has full read/write DB access (PostgreSQL user `growdirect` is not read-only). |
| **Recommended fix** | 1) Create a read-only PostgreSQL user for the sidecar. 2) Retrieve connection string from Secrets Manager. |
| **Linear** | — |

### F-005: Health check does not verify dependencies

| | |
|---|---|
| **Severity** | **P2** — post-launch |
| **File** | `cove/services/angel_agent/server.py` |
| **Description** | `/health` returns "healthy" without checking DB connectivity or Anthropic API key presence. A container with a missing API key or unreachable database will report healthy. |
| **Recommended fix** | Health check should test DB connection (`pool.connect()`) and verify `ANTHROPIC_API_KEY` is set. Return "degraded" with specifics if either fails. |
| **Linear** | — |

### F-006: In-memory rate limiting lost on container restart

| | |
|---|---|
| **Severity** | **P2** — post-launch |
| **File** | `cove/services/angel_agent/server.py` |
| **Description** | `_session_counts` and `_daily_counts` are Python dicts in process memory. Container restart resets all limits. Multiple container replicas (ECS) would each have independent counters, allowing N-times-limit abuse. |
| **Recommended fix** | Move rate limit counters to Valkey (DB 1) with TTL-based expiry. Allows shared state across replicas. |
| **Linear** | — |

### F-007: Anthropic client created per-request, not pooled

| | |
|---|---|
| **Severity** | **P2** — post-launch |
| **File** | `cove/services/angel_agent/server.py` line 86 |
| **Description** | `Anthropic(api_key=api_key)` is instantiated on every chat request via lazy import. This creates a new HTTP connection pool per request. Under load, this wastes connections and adds latency. |
| **Recommended fix** | Initialize the Anthropic client once at module level or on first use, and reuse it across requests. |
| **Linear** | — |

### F-008: DB connection string logged at startup

| | |
|---|---|
| **Severity** | **P1** — before GA |
| **File** | `cove/services/angel_agent/db.py` line 41 |
| **Description** | `logger.info("Angel Agent DB engine initialized: %s", url.split("@")[-1])` logs the host/port/database portion of the connection string. While it strips the password, this still leaks infrastructure topology to logs. In production with CloudWatch, this is acceptable but should be reviewed. |
| **Recommended fix** | Log only "Angel Agent DB engine initialized" without any URL fragment, or use a sanitized alias. |
| **Linear** | — |

### F-009: No CORS headers on sidecar endpoints

| | |
|---|---|
| **Severity** | **P1** — before GA |
| **File** | `cove/services/angel_agent/server.py` |
| **Description** | The sidecar raw ASGI app sets no CORS headers. Currently, the widget calls the Cove Flask proxy (which handles CORS), but if the widget ever calls the sidecar directly, all requests would fail. More critically, the lack of CORS on the sidecar means any origin can call it if port 8004 is exposed. |
| **Recommended fix** | The sidecar should never be internet-exposed. Add a comment documenting this constraint. If direct widget access is ever needed, add strict CORS with allowed origins. |
| **Linear** | — |

### F-010: Error responses may leak internal details

| | |
|---|---|
| **Severity** | **P1** — before GA |
| **File** | `cove/services/angel_agent/server.py` |
| **Description** | Exception handling in `handle_chat()` catches broadly and returns generic messages, which is good. However, the Flask proxy in `chat_routes.py` forwards the sidecar's full JSON response body including any `error` field values, which could contain internal details from future tool implementations. |
| **Recommended fix** | Flask proxy should sanitize error responses — only forward `text` and `usage` fields, never raw error details from the sidecar. |
| **Linear** | — |

### F-011: capture_lead tool has no PII encryption plan

| | |
|---|---|
| **Severity** | **P0** — blocks production (when implemented) |
| **File** | `cove/services/angel_agent/tools.py` |
| **Description** | The `capture_lead` tool stub accepts name, phone, and email. When implemented, this will create Lead records. The current SDD design stores these fields plaintext. No encryption layer, no audit logging, and no data retention policy exists for lead data. |
| **Recommended fix** | Before implementing `capture_lead`: 1) Create Lead model with AES-256-GCM encrypted fields (extend Canary's `crypto.py` pattern). 2) Add audit log entries for lead creation and status changes. 3) Define retention policy (leads older than 12 months auto-purged). |
| **Linear** | — |

### F-012: SMS notification for leads has no implementation path

| | |
|---|---|
| **Severity** | **P1** — before GA (when lead capture ships) |
| **File** | SDD design only — no code exists |
| **Description** | The SDD describes SMS notification to Angelique when a lead is captured. No SMS provider is configured (Twilio, AWS SNS, etc.). No phone number validation. No opt-in consent mechanism for the visitor. California law (CCPA) requires disclosure before collecting contact info. |
| **Recommended fix** | 1) Select SMS provider and add to infrastructure. 2) Add phone number validation before storage. 3) Add disclosure text to the widget before lead capture form. 4) Consider email notification as MVP alternative to SMS. |
| **Linear** | — |

### F-013: No request size limit on sidecar

| | |
|---|---|
| **Severity** | **P1** — before GA |
| **File** | `cove/services/angel_agent/server.py` lines 183-189 |
| **Description** | The raw ASGI body reader accumulates `body += message.get("body", b"")` without any size limit. An attacker could send a multi-GB payload and exhaust container memory. |
| **Recommended fix** | Add a `MAX_REQUEST_BYTES` constant (e.g., 64KB) and reject requests exceeding it. |
| **Linear** | — |

### F-014: SQL injection surface via string interpolation in area resolution

| | |
|---|---|
| **Severity** | **P2** — post-launch (mitigated by SQLAlchemy ORM) |
| **File** | `cove/services/angel_agent/tools.py` |
| **Description** | Tool handlers use SQLAlchemy ORM with `.filter()` and `.ilike()`, which parameterize queries. The area resolver in `areas.py` returns user input as `{"type": "unknown", "value": area}` which is then used in `MarketSnapshot.area.ilike(f"%{area_input}%")`. SQLAlchemy parameterizes this, but the pattern of embedding user input in LIKE patterns could cause unexpected results (e.g., `%` in input matches everything). |
| **Recommended fix** | Escape `%` and `_` characters in user input before passing to `.ilike()`. |
| **Linear** | — |

---

## Production Readiness Checklist

- [ ] **PII encrypted at rest** — No PII stored currently. P0 blocker when `capture_lead` is implemented (F-011).
- [ ] **Secrets in AWS Secrets Manager** — `ANTHROPIC_API_KEY` and `DATABASE_URL` currently in `.env` / Docker env (F-003, F-004).
- [x] **Health check endpoint responds** — `/health` returns JSON. Does not verify dependencies (F-005).
- [ ] **Audit logging for sensitive operations** — No audit trail for tool calls or lead captures. In-memory counters only.
- [ ] **Data retention policy implemented** — No retention policy for any data. Lead data retention TBD.
- [x] **Rate limiting on public endpoints** — Sidecar has in-memory 30/session + 150/day limits. Flask proxy has no rate limiting (F-001).
- [ ] **Error responses don't leak internals** — Mostly safe but proxy forwards raw sidecar errors (F-010).
- [ ] **Internal service authentication** — No auth between Flask proxy and sidecar (F-002).
- [ ] **Request size limits** — No request body size limit on sidecar (F-013).
- [x] **Read-only database access** — All live tools are read-only. DB user has write permissions but no tool code writes (F-004 recommends read-only user).
- [x] **Fair Housing compliance in system prompt** — FHA + FEHA guardrails in system prompt, demographic steering prohibited.
- [x] **AI disclosure in widget** — Footer discloses Angel is AI with DRE# and Compass branding.

---

## Key Source Files

| File | Purpose |
|------|---------|
| `Cove/cove/angel/chat_routes.py` | Flask proxy blueprint (angel_chat_bp) |
| `Cove/cove/services/angel_agent/server.py` | ASGI sidecar app, rate limiting, tool dispatch loop |
| `Cove/cove/services/angel_agent/tools.py` | Tool definitions (12) and handlers (4 live, 8 stubs) |
| `Cove/cove/services/angel_agent/db.py` | Standalone SQLAlchemy engine for sidecar |
| `Cove/cove/services/angel_agent/system_prompt.py` | Three-layer system prompt assembly |
| `Cove/cove/services/angel_agent/areas.py` | Area name resolution (city aliases, neighborhood mappings) |
| `Cove/Dockerfile.angel-agent` | Sidecar container definition |
| `Cove/devops/docker-compose.yml` | Service definition (angel-agent service) |
| `Cove/tests/angel_agent/` | Test suite (test_tools.py, test_server.py, conftest.py) |

---

*Angel Agent SDD — GrowDirect Inc. — Last updated 2026-04-13*
