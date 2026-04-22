# Owl — AI Analysis Engine

**Service Type:** MCP Server (Canary)
**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]
**Architecture:** [[docs/sdds/canary/architecture|Canary Architecture SDD]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[Canary/docs/profiles/ops/Tom|Tom]] + [[Canary/docs/profiles/ops/Research|Research]] · **Operator role:** [[Canary/docs/profiles/ops/Owl|Owl]] + [[Canary/docs/profiles/ops/Jeremy|Jeremy]]

---

## Purpose

Owl is the AI intelligence layer for Canary LP. It provides personality-routed chat, context-aware health check reports, natural language data search, and an MCP tool registry that any client can discover and invoke. It is the merchant's primary interface to Canary's analytical capabilities -- every insight, report, and recommendation flows through Owl.

## Dependencies

| Dependency | Type | Required | Failure Impact |
|------------|------|:--------:|----------------|
| PostgreSQL (`canary` DB, `app` schema) | Database | Yes | Sessions, findings, memory not persisted; reports still generated but ephemeral |
| Ollama (`growdirect_ollama:11434`) | External AI | No | All paths degrade to deterministic fallback logic |
| Valkey (DB 0) | Cache | No | No caching; functionally identical, slightly slower |
| Chirp (detection engine) | Internal service | Yes | `score_payment` tool fails; heartbeat computation fails |
| Fox (case service) | Internal service | Yes | `case_create` / `follow_up` actions fail |
| ALX / Memory Bus (`growdirect_memory_bus:8003`) | MCP service | No | Window 0 (institutional knowledge) empty; prompts less context-rich |
| Dashboard service | Internal service | No | Dashboard tool returns empty; dashboard context not injected into prompts |

---

## Data Flow & PII Map

### What Enters

| Source | Data | Format |
|--------|------|--------|
| Mobile app / API clients | Merchant messages, alert lists, store stats | JSON via JWT-authenticated POST |
| PostgreSQL (alerts table) | Active alerts with employee IDs, amounts, rule IDs | Auto-fetched when client doesn't provide |
| Memory Bus MCP | Institutional knowledge (LP patterns, process expertise) | Semantic search results (pgvector) |
| Chirp engine | Stateless rule evaluations on payment payloads | Dict of fired rules |

### What's Stored (4 tables in `canary_app`)

| Table | Fields | PII Classification | Encryption |
|-------|--------|:------------------:|:----------:|
| `owl_sessions` | merchant_id, heartbeat_score, heartbeat_band, narrative_summary, lp/ops/analytics assessments, outlook | internal | plaintext |
| `owl_findings` | merchant_id, category, rule_ids, severity, finding_text, recommended_action, delta | internal | plaintext |
| `owl_merchant_memory` | merchant_id, running_summary, score_trend, recurring_categories, actions_taken | internal | plaintext |
| `owl_action_log` | merchant_id, action_type, action_detail (may contain alert_ids, drill filters) | internal | plaintext |

**PII exposure notes:**
- `narrative_summary` and `running_summary` are LLM-generated text that may reference employee names if present in alert data.
- `finding_text` may include employee names from upstream Chirp alerts.
- `action_detail` stores JSON with alert_ids and drill filter parameters -- no direct PII but links to PII-bearing records.
- No email, phone, SSN, or direct customer PII stored in Owl tables.
- Employee names flow through transiently in LLM prompts but are not independently stored by Owl (they come from Alert records).

### What Exits

| Destination | Data | Sensitivity |
|-------------|------|:-----------:|
| Mobile app / API clients | Chat responses, health reports, search results, dashboard data | internal |
| Fox case service | Alert IDs, transaction IDs, case metadata | internal |
| Ollama (external) | System prompts with merchant context, employee-linked alert summaries | **sensitive** -- prompts sent over Docker network contain employee-attributed alert data |
| `owl_action_log` | Action records | internal |

---

## API Contract

**Blueprint:** `owl_api` at `/owl`. MCP server name: `canary-owl`, version `0.1.0`.

### Public Endpoints (no auth)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/owl/manifest` | MCP protocol manifest with full tool list |
| GET | `/owl/tools` | All registered tools in MCP format |
| GET | `/owl/health` | Ollama status. Returns `{owl_status, url, model}`. 200 if healthy, 503 if offline |

### JWT-Protected Endpoints

| Method | Path | Timeout | Description |
|--------|------|:-------:|-------------|
| POST | `/owl/tools/<name>` | varies | Generic MCP tool invocation. Params from JSON body, context from JWT |
| POST | `/owl/one-thing` | 15s | Single most important insight. Auto-fetches alerts from DB if not provided |
| POST | `/owl/heartbeat` | -- | Store health score. Returns `{score, band, alert_counts, total_alerts}` |
| POST | `/owl/chat` | 15s | Full personality-routed chat. Closed-loop envelope response |
| GET | `/owl/personalities` | -- | Lists Chirp JPT lenses for chat UI picker |
| POST | `/owl/health-check` | 120s | McKinsey-style health report. Seven-step pipeline |
| POST | `/owl/action` | -- | Closed-loop action dispatcher. 11 action codes |

### Action Codes

`case_create`, `follow_up`, `resolve`, `dismiss` (reason required), `archive`, `share`, `checklist_start`, `template_save`, `drill_down`, `drill_row`.

### Python Service API (internal)

`owl_healthy()`, `ask_owl(prompt, system_prompt, format_json, timeout)`, `get_the_one_thing(alerts, stats, merchant_context)`, `route_message(message)`, `infer_output_type(message, personality)`, `get_personality(name)`, `list_personalities()`, `format_response(...)`, `parse_owl_output(...)`.

---

## MCP Tool Registry

| Tool | Auth Required | PII Access | Rate Limit | Description |
|------|:---:|:---:|:---:|-------------|
| `the_one_thing` | JWT | Reads alerts (employee-linked) | None | Single most important insight. LLM with deterministic fallback. Category: insights |
| `ask` | JWT | Reads merchant context | None | Freeform plain-English question. LLM required (returns error if offline). Category: query |
| `heartbeat` | JWT | Reads alerts (counts only) | None | Store health score 0-100. Pure computation, no LLM. Category: health |
| `check_heartbeat` | JWT | Reads alerts, memory, previous findings | None | Full health check with memory context and optional McKinsey report. Category: health |
| `score_payment` | JWT | Reads payment payload (card_last4, employee, amounts) | None | Stateless Chirp rule evaluation on a parsed Square payment. Category: scoring |
| `search` | JWT | Reads transactions, alerts, cases, employees | None | Natural language query translated to structured PostgreSQL query. Category: search |
| `dashboard` | JWT | Reads merchant KPIs, employee risk scores | None | Health score, top concern, anomaly count, metric bands. Deterministic. Category: dashboard |
| `knowledge_search` | JWT | None (searches institutional knowledge only) | None | ALX institutional knowledge via pgvector semantic similarity. Category: knowledge |

---

## Cross-App Data Access

Owl operates entirely within the Canary application boundary. It does not access Cove, Angel, or platform databases directly.

| Data Source | Access Type | Tenant Isolation |
|-------------|:-----------:|------------------|
| `canary.app` schema (alerts, cases, owl tables) | Read/Write | All queries filter by `merchant_id` from JWT context |
| `canary.sales` schema (transactions) | Read | Filtered by `merchant_id` via search executor |
| `canary.metrics` schema | Read (via dashboard service) | Filtered by `merchant_id` |
| Memory Bus MCP (port 8003) | Read | No tenant filter -- institutional knowledge is shared across merchants |

**Tenant isolation model:** Every database query in Owl filters by `merchant_id` extracted from the JWT token (via `g.merchant_id`). The `TenantMixin` on `OwlSession` and the explicit `merchant_id` FK on all other Owl tables enforce this at the model level. There is no cross-tenant query path in the current code.

---

## Tool Dispatch Security

**Authentication:** All tool invocations go through `@jwt_required`, which extracts `merchant_id` and `user_id` from the JWT and sets them on Flask's `g` object. The generic `/owl/tools/<name>` endpoint and all convenience endpoints enforce this.

**Authorization:** No role-based access control within Owl. Any authenticated merchant user can invoke any tool. The `case_create` and `follow_up` actions write to Fox (case management) using the JWT-provided `user_id`.

**Privilege escalation risk:** Low. Owl tools read data scoped to the merchant and write only to Owl's own tables plus Fox cases (through FoxCaseService). The `search` tool constructs SQL queries from natural language, but the query builder validates intent and the executor filters by `merchant_id`. SQL injection risk is mitigated by parameterized queries in the search builder/executor.

**Compromise scenario:** If the MCP server is compromised, an attacker could:
- Read all alerts, transactions, and cases for any merchant (if JWT auth is bypassed)
- Generate Fox cases with arbitrary data
- Send arbitrary prompts to Ollama (no sensitive data in model weights)
- Read institutional knowledge (non-sensitive)

The blast radius is limited to Canary data. No cross-app access exists.

---

## Chirp JPT Lenses

Three frozen-dataclass lenses route merchant messages deterministically (no LLM in routing):

| Lens | Domain | Default | Preferred Outputs | Routing |
|------|--------|:-------:|-------------------|---------|
| `jpt_detection` | Loss prevention | Yes | alert_set, number | Employee patterns, void/refund anomalies, coaching |
| `jpt_operations` | Operations | No | checklist, memo | Process optimization, scheduling, workflow |
| `jpt_analytics` | Analytics | No | number, memo | Benchmarks, trends, cohort comparisons |

Routing uses keyword intent scoring with `matches / sqrt(keywords)` normalization. Highest score wins; ties go to `jpt_detection`. Explicit address (e.g., "@lp" prefix) overrides intent scoring with 0.8 minimum confidence.

---

## 4-Window Context Assembly

Every Owl prompt is built from four context windows injected before the merchant's message:

| Window | Source | Budget | Fallback |
|:------:|--------|:------:|----------|
| 0 | Institutional Knowledge -- ALX pgvector semantic search filtered by JPT lens affinity | ~2,000 tokens | Empty string (best-effort) |
| 1 | Running Summary -- compressed merchant history from `owl_merchant_memory.running_summary` | ~1,000 tokens | Cold start baseline message |
| 2 | Delta -- what improved/worsened/appeared/resolved since last session via deterministic delta engine | ~1,000 tokens | Empty (no prior session) |
| 3 | Heartbeat + Dashboard -- current score, band, severity breakdown, plus top-5 active alerts. Dashboard state (3b) injected when available | ~700 tokens | Heartbeat only |

Total prompt budget: ~6,200 tokens with ~1,800 reserved for generation.

---

## Output Formatting

Every Owl response is wrapped in a closed-loop envelope with one of four output types:

| Output Type | Exit Actions | Terminal State |
|-------------|-------------|----------------|
| `alert_set` | Open case, Follow up, Resolve, Dismiss | `resolved_or_case_opened` |
| `memo` | Archive, Share | `archived_or_shared` |
| `checklist` | Start checklist, Save as template | `completed_or_saved` |
| `number` | Dig deeper, Got it | `resolved_or_drilled` |

No orphan outputs -- every response terminates in a one-tap merchant action.

---

## Data Model

Four tables in `app` schema (`canary_app`). All extend `AppBase` + `AuditMixin` (created_at/modified_at/created_by/modified_by). Access pattern: append-only (sessions and findings are never updated after creation; merchant memory is upserted).

**`owl_sessions`** -- One row per completed analysis run.
Columns: `id` (String(36) PK), `merchant_id` (String(36), TenantMixin), `session_type` (String(20): health_check/chat/scheduled), `heartbeat_score` (Integer 0-100), `heartbeat_band` (String(20)), `total_alerts` (Integer), `alert_breakdown` (Text JSON), `category_scores` (Text JSON), `narrative_summary` (Text, LLM-generated), `top_finding` (Text), `top_finding_category` (String(50)), `hc_session_id` (String(36)), `previous_session_id` (String(36) FK to self), `relevance_weight` (Float, time-decay), `lp_assessment` (Text), `ops_assessment` (Text), `analytics_assessment` (Text), `positive_notes` (Text), `outlook` (Text).
Indexes: `(merchant_id, created_at)`, `(merchant_id, session_type)`.

**`owl_findings`** -- One row per Chirp category that fired within a session.
Columns: `id` (PK), `session_id` (FK), `merchant_id`, `category` (String(50)), `rule_ids` (Text JSON array), `severity` (String(20)), `alert_count` (Integer), `finding_text` (Text), `recommended_action` (Text), `delta_direction` (String(20)), `delta_detail` (Text JSON).
Indexes: `(session_id)`, `(merchant_id, category)`.

**`owl_merchant_memory`** -- One row per merchant, always-current.
Columns: `id` (PK), `merchant_id` (UNIQUE), `latest_session_id` (FK), `latest_heartbeat_score` (Integer), `latest_heartbeat_band` (String(20)), `session_count` (Integer), `score_trend` (Text JSON array, last 12), `recurring_categories` (Text JSON), `running_summary` (Text, ~500 tokens), `actions_taken` (Text JSON array), `is_cold_start` (Boolean).

**`owl_action_log`** -- Tracks merchant actions on findings.
Columns: `id` (PK), `merchant_id`, `finding_id` (FK, optional), `session_id` (FK, optional), `action_type` (String(50)), `action_detail` (Text JSON), `outcome` (String(50)).
Indexes: `(merchant_id, created_at)`, `(finding_id)`.

**Time decay:** Exponential with 14-day half-life, floor 0.05: `max(0.05, pow(2, -days_old / 14.0))`.

---

## Workflows

### Chat Flow

1. Merchant sends message via `POST /owl/chat`.
2. Router extracts explicit address via regex; if no match, scores intent keywords against all three personalities using `matches / sqrt(keywords)` normalization. Produces `RoutedMessage`.
3. `infer_output_type()` counts signal words to classify expected output, falling back to personality's first preferred output.
4. `_get_memory_context()` assembles the 4-window context (all best-effort -- returns empty string on failure).
5. System prompt built: personality definition + HEARTBEAT_KNOWLEDGE + institutional context + merchant context + top 5 alerts + stats.
6. `ask_owl(clean_message, system_prompt, format_json=True, timeout=15)` posts to Ollama `/api/generate`.
7. `parse_owl_output()` extracts message/output_type/data/severity from LLM JSON, wraps in closed-loop envelope.
8. If LLM fails, `_chat_fallback()` produces a deterministic envelope with `source="fallback"`.
9. Routing metadata attached to response.

### Closed-Loop Action Flow

Merchant taps an action button. `POST /owl/action` dispatches by action code. `case_create`: routes through `FoxCaseService.create_case_from_context()` (supports alerts, transactions, and drill paths). `follow_up`: checks existing Fox case linkage, creates or appends evidence with GUID refs (`raas:{merchant_id}:{source_table}:{source_id}`). `resolve`/`dismiss`: writes AlertHistory. All actions logged to `owl_action_log` non-blocking.

### Health Check Report Flow

1. Ops triggers `POST /owl/health-check`. Alerts fetched (auto if not provided, limit 50).
2. `compute_heartbeat(alerts)` produces deterministic score and band.
3. Load merchant memory + previous findings (best-effort).
4. `assemble_context()` builds 4-window prompt block.
5. `generate_health_report()` sends to LLM with `REPORT_SYSTEM_PROMPT` (timeout 120s). Fallback if offline.
6. `_post_validate()` patches hallucinated numbers (corrects scores within +/-15 via regex), migrates legacy field names, validates finding trends against delta engine.
7. Persist: `create_owl_session()`, `create_owl_findings()` (one per Chirp category with delta direction plus "resolved" findings), `update_merchant_memory()`. Persistence is non-fatal.

### The One Thing Flow

App load or pull-to-refresh triggers `POST /owl/one-thing`. If Owl healthy: builds JSON prompt from up to 20 alerts + stats + context, calls `ask_owl()` with `jpt_detection` lens, parses JSON. If offline: falls back to composite ranking (severity 60%, impact_cents 40% when available). Dashboard override: if any metric is in "investigate" band and alert severity < critical, dashboard concern takes priority.

### Delta Engine

`compute_session_deltas()` compares current alerts (grouped by Chirp category) against previous session's findings. Count decreased = improved, increased = worsened, same count but severity changed = follows severity, not in previous = new, in previous but not current = resolved. Categories firing 3+ consecutive sessions flagged as "recurring" with elevated prompt prominence.

---

## Operations

### Startup Sequence

1. Flask app loads, registers `owl_api` blueprint at `/owl`
2. `_create_owl_blueprint()` calls `create_mcp_blueprint()` which registers all 8 tools from `owl/tools.py`
3. Ollama connectivity checked lazily on first tool invocation (not at startup)
4. No database migration or seed required -- tables created by Alembic

### Health Check

`GET /owl/health` returns:
```json
{
  "service": "canary-owl",
  "healthy": true,
  "owl_status": "online",
  "url": "http://host.docker.internal:11434",
  "model": "qwen3:14b",
  "tools": 8
}
```
Returns 200 if Ollama is reachable (GET `/api/tags` with 3s timeout), 503 if offline.

### Failure Modes

| Component | Failure | Impact | Degradation |
|-----------|---------|--------|-------------|
| Ollama down | `owl_healthy()` returns false | No LLM-generated insights | All tools degrade to deterministic logic: severity-based ranking for The One Thing, template-based reports, formatted envelopes with `source="fallback"` |
| Ollama timeout | 15s (chat), 120s (report) | LLM response lost | Same deterministic fallback path |
| Ollama returns `{}` | qwen3 thinking mode + `format=json` | Empty LLM response | Workaround in place: `think=false` set when `format_json=True` |
| PostgreSQL down | DB queries fail | Sessions/findings not persisted, memory not loaded | Reports still generated and returned; persistence failure is non-fatal (logged, not raised) |
| Memory Bus down | `_memory_recall_via_mcp()` fails | Window 0 empty | 5s timeout, returns empty string, prompt proceeds without institutional context |
| Dashboard service down | `get_dashboard_data()` fails | Dashboard tool returns empty, Window 3b empty | Try/except returns None, context assembly continues |

### Monitoring

| Metric | Alert Threshold | Notes |
|--------|:-----------:|-------|
| `/owl/health` status | 503 for > 5 min | Ollama is down -- all AI features degraded |
| Report generation time | > 120s (timeout) | LLM overloaded or model too large |
| `_post_validate` score corrections | Logged as DEBUG | Frequent corrections suggest prompt quality issues |
| `owl_sessions` creation failures | Any ERROR log | Database connectivity or schema issues |
| Action dispatch failures | Any 500 response | Fox/Alert service issues |

### Configuration

| Env Var | Default | Description |
|---------|---------|-------------|
| `OWL_URL` | `http://host.docker.internal:11434` | Ollama API base URL |
| `OWL_MODEL` | `qwen3:14b` | Ollama model tag |
| `CANARY_DEV_JWT_SECRET` | (none) | Dev-mode JWT validation secret |
| `SECRET_KEY` | (none) | Flask secret key (standalone MCP mode) |
| `MCP_SERVER_NAME` | (none) | Set to `owl` for standalone extraction |

---

## Deployment

### Docker Service Definition

Owl runs in two modes:

**Mode 1: Monolith (primary).** Owl is a Flask blueprint inside the Canary monolith at `:5001/owl/*`. No separate container.

**Mode 2: Standalone MCP (proof of concept).** Defined in `docker-compose.localhost.yml` as `owl-mcp` service at `:8001/owl/*`. Same code, separate container. Uses `MCP_SERVER_NAME=owl`.

```yaml
owl-mcp:
  image: canary-owl-mcp
  container_name: canary_localhost_owl_mcp
  environment:
    MCP_SERVER_NAME: owl
    OWL_URL: http://growdirect_ollama:11434
    OWL_MODEL: qwen3:14b
  networks:
    - growdirect
```

### AWS Target

- **Compute:** ECS/Fargate (monolith) -- Owl deploys as part of the Canary Flask container
- **Database:** RDS PostgreSQL 17 (shared `canary` database)
- **AI:** Ollama on a GPU-enabled EC2 instance or SageMaker endpoint (qwen3:14b requires ~10GB VRAM)
- **Secrets:** AWS Secrets Manager for JWT secrets, DB credentials

### CI/CD Requirements

- Owl has no independent deploy -- ships with Canary monolith
- Ollama model must be pre-pulled on the inference host (`ollama pull qwen3:14b`)
- Health check endpoint (`/owl/health`) used for readiness probe

---

## Code Review Findings

### P0 -- Blocks Production

**P0-1: Error responses may leak internal details.**
The action dispatcher catches exceptions and returns `str(e)` directly in the JSON response body (`return jsonify({"ok": False, "error": str(e)}), 500`). This can leak stack traces, internal service names, and database error messages to the client.
*Recommended fix:* Sanitize error responses to return generic messages to clients. Log full errors server-side. Applies to `execute_action()`, `_action_case_create_unified()`, and other action handlers.
*Linear:* --

**P0-2: No input validation on search tool.**
The `search` tool accepts arbitrary natural language and translates it to SQL via `owl_search()`. While the query builder uses parameterized queries, there is no validation of result set size, no query complexity limit, and no timeout on the database query itself. A crafted question could trigger expensive full-table scans.
*Recommended fix:* Add query timeout at the database level (statement_timeout), enforce result row limits in the executor, and validate that translated queries don't touch unauthorized tables.
*Linear:* --

**P0-3: Public endpoints expose service topology.**
`GET /owl/health` returns the internal Ollama URL (`host.docker.internal:11434`) and model name. `GET /owl/manifest` and `/owl/tools` list all tool schemas without authentication. While MCP convention allows public discovery, the health endpoint should not expose internal infrastructure details in production.
*Recommended fix:* Redact `url` field from health response in production. Consider adding auth to manifest/tools endpoints or making them opt-in.
*Linear:* --

### P1 -- Before GA

**P1-1: No rate limiting on any endpoint.**
All Owl endpoints (including public manifest/tools/health) lack rate limiting. A malicious client could flood the chat or health-check endpoints, consuming Ollama GPU resources and database connections.
*Recommended fix:* Add Flask-Limiter to all Owl endpoints. Suggested limits: 60/min for chat, 10/min for health-check reports, 120/min for heartbeat/one-thing, 30/min for search.
*Linear:* --

**P1-2: No audit logging for tool invocations.**
Tool invocations through the generic `/owl/tools/<name>` endpoint are not logged. Only action dispatches are logged to `owl_action_log`. There is no record of who searched what, who generated reports, or who asked the Owl questions.
*Recommended fix:* Add structured audit logging for all tool invocations: who (merchant_id, user_id), what (tool name, params hash), when, and result status.
*Linear:* --

**P1-3: No data retention policy for Owl tables.**
`owl_sessions`, `owl_findings`, and `owl_action_log` grow indefinitely. No purge or archival mechanism exists. `owl_merchant_memory.score_trend` is capped at 12 entries, but all other tables are unbounded.
*Recommended fix:* Implement automated retention: archive sessions older than 12 months, purge action logs older than 24 months. Add relevance_weight decay job to down-weight old sessions.
*Linear:* --

**P1-4: Ollama prompts contain employee-attributed alert data.**
System prompts sent to Ollama include employee names and their associated alert patterns (e.g., "Maria: 3 refunds over $50"). While Ollama runs locally (Docker network), in a production deployment with a remote inference endpoint, this data would transit the network. No encryption or PII redaction is applied to prompts.
*Recommended fix:* For remote Ollama deployments, either (a) use employee IDs instead of names in prompts, (b) add TLS between Canary and Ollama, or (c) run Ollama on the same host/VPC with private networking.
*Linear:* --

**P1-5: `owl_action_log` writes are best-effort with swallowed exceptions.**
`_log_owl_action()` catches all exceptions and logs them at DEBUG level. A persistent database issue could silently lose all action audit records without anyone noticing.
*Recommended fix:* Elevate logging to WARNING for action log failures. Add a monitoring alert for repeated failures. Consider a fallback write path (e.g., write to a local file or Valkey queue).
*Linear:* --

### P2 -- Post-Launch

**P2-1: LLM post-validation is regex-based and fragile.**
`_post_validate()` uses regex to find and correct hallucinated scores in executive summaries. The +/-15 tolerance means scores that are exactly 15 points off pass through uncorrected. The regex patterns are English-specific.
*Recommended fix:* Validate score references more strictly by parsing the executive_summary as structured text. Consider having the LLM output scores in a separate structured field rather than embedded in prose.
*Linear:* --

**P2-2: No circuit breaker for Ollama.**
Every request checks `owl_healthy()` which makes a fresh HTTP call to Ollama. Under high load, this creates N+1 health checks. If Ollama is slow but not down, each request incurs a 3s timeout penalty before falling back.
*Recommended fix:* Implement a circuit breaker pattern: cache Ollama health status for 30s, open circuit after 3 consecutive failures, half-open after 60s.
*Linear:* --

**P2-3: Legacy field name migration in reports.**
`_post_validate()` still maps legacy field names (`jim_assessment` -> `lp_assessment`, etc.) from older LLM outputs. This adds complexity and suggests the system prompt may still occasionally produce legacy names.
*Recommended fix:* Update the system prompt to strictly enforce new field names. Remove legacy mapping after confirming no recent occurrences.
*Linear:* --

**P2-4: `ask` tool timeout at 90s is aggressive for freeform questions.**
The `ask` tool uses a 90s timeout for Ollama, which is much higher than the 15s chat timeout. For freeform questions, this could hold a connection open for 90s on a slow inference.
*Recommended fix:* Reduce `ask` timeout to 30s (matching SDD's documented timeout), or implement streaming responses.
*Linear:* --

---

## Production Readiness Checklist

- [ ] PII encrypted at rest -- N/A for Owl tables (no direct PII stored; employee names transit through LLM prompts but are not persisted by Owl)
- [ ] Secrets in AWS Secrets Manager (not .env) -- JWT secrets, DB credentials still in .env
- [x] Health check endpoint responds -- `GET /owl/health` returns 200/503 with Ollama status
- [ ] Audit logging for sensitive operations -- tool invocations not logged; only action dispatches logged (best-effort)
- [ ] Data retention policy implemented -- no automated purge for sessions, findings, or action logs
- [ ] Rate limiting on public endpoints -- no rate limiting on any Owl endpoint
- [ ] Error responses don't leak internals -- action dispatcher returns raw exception messages to client
- [x] Graceful degradation when Ollama is down -- all paths fall back to deterministic logic
- [x] Tenant isolation via merchant_id -- all queries scoped by JWT-extracted merchant_id
- [ ] Prompt PII redaction for remote inference -- employee names sent to Ollama unredacted
- [x] Post-validation of LLM output -- `_post_validate()` corrects hallucinated numbers
- [x] Non-fatal persistence -- report generation continues even if DB write fails
