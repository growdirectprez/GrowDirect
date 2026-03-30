# Owl Intelligence Brain

> **Status:** Complete — written from code
> **Namespace:** canary
> **Last updated:** 2026-03-30
> **Code location:** `Canary/canary/services/owl/`, `Canary/canary/services/owl/search/`

---

## 1. Overview

Owl is Canary's AI intelligence layer — the brain behind every merchant-facing insight. It sits between raw Chirp alert data and the merchant, converting detection signals into plain-English analysis, structured reports, and natural language search results.

Owl serves three distinct functions:

1. **Health intelligence** — Synthesizes all active alerts into a heartbeat score, McKinsey-style health check report, and "The One Thing" — the single most important insight for the merchant right now.
2. **Conversational chat** — A multi-personality chat interface (Chirp JPT) that routes merchant questions to the right analytical lens: Detection (LP instinct), Operations (process thinking), or Analytics (research and benchmarks).
3. **Natural language search** — Translates plain-English questions ("show me refunds over $50 this week") into parameterized PostgreSQL queries against the CRDM (Consolidated Retail Data Model), executing them with tenant isolation and returning results in closed-loop envelopes.

The Owl is designed to degrade gracefully: every intelligence path has a deterministic fallback that runs without the LLM. Merchants get meaningful output whether Ollama is online or not.

**LLM:** `qwen3:14b` via Ollama at `http://host.docker.internal:11434` (default). JSON mode disables thinking tokens, which consume response budget without producing structured output.

---

## 2. Architecture

### Component Diagram

```
                          Merchant / Mobile App
                                  |
                          owl_api.py (Flask Blueprint)
                         /        |          |        \
                 /chat      /health-check  /action  /owl/tools/<name>
                   |              |                        |
               router.py     report.py              tools.py (MCPRegistry)
                   |              |                  |    |    |    |
           personality.py   memory.py (assemble)  ask  search  heartbeat  ...
                   |              |                        |
           client.py (Ollama)  delta.py            search/facade.py
                   |                                   /       \
            ask_owl()                     deterministic.py   intent.py (LLM)
            owl_healthy()                               |         |
            fallback path                          validator.py  |
                                                   builder.py    |
                                                   executor.py   |
                                                   (PostgreSQL)  |
                                                                 |
                                              Institutional knowledge (Window 0)
                                              institutional.py → memory bus MCP
```

### Request / Data Flow

**Health Check Report (`POST /owl/health-check`)**

1. Fetch active alerts from DB (or accept from request body).
2. `compute_heartbeat(alerts)` — deterministic score (0-100), band, breakdown.
3. Load merchant memory: `get_merchant_memory()` + `get_previous_findings()`.
4. `assemble_context()` — builds four-window prompt block:
   - Window 0: Institutional knowledge from memory bus (if available).
   - Window 1: Running summary from `OwlMerchantMemory.running_summary`.
   - Window 2: Delta from previous session via `_format_delta_block()`.
   - Window 2b: Dashboard state via `build_dashboard_context()`.
   - Window 3: Current heartbeat formatted block.
5. `generate_health_report(context, alerts, ...)` — sends to Ollama; falls back to `_fallback_report()` if offline.
6. `_post_validate()` — patches any hallucinated scores/bands with correct deterministic values.
7. `create_owl_session()`, `create_owl_findings()`, `update_merchant_memory()` — persist to DB.
8. Return JSON report.

**Chat (`POST /owl/chat`)**

1. `route_message(message)` — deterministic: extracts named personality address or scores intent keywords.
2. `infer_output_type()` — picks `alert_set`, `memo`, `checklist`, or `number` from message signals.
3. Assemble system prompt: personality system prompt + memory context + alert summary.
4. `ask_owl(message, system_prompt, format_json=True)` — LLM call; fallback to `_chat_fallback()`.
5. `parse_owl_output()` — wraps LLM JSON into closed-loop envelope with `actions[]` and `closes_to`.
6. Attach routing metadata.

**Search (`POST /owl/tools/search` or via `owl_search()`)**

Pipeline runs in five stages. Deterministic parser runs first; LLM parser is fallback only.

```
Stage 1: Parse    — deterministic_parse() → LLM parse_intent() if no match
Stage 2: Validate — validate_intent() → field registry, operator type-check
Stage 3: Build    — build_query() → parameterized SQL, mandatory merchant_id
Stage 4: Execute  — execute_search() → PostgreSQL, 5s timeout, RLS context
Stage 5: Format   — _format_search_results() / _format_drill_results()
```

**Drill (`POST /drill` or `drill_search()`)**

Bypasses LLM entirely. The `drill_search()` facade handles entry (initial grouped view) and drill-down (tap on grouped row) modes. Breadcrumbs accumulate across levels. `drill_orders.py` defines five hierarchies for the GROUP BY cascade.

### Key Design Decisions

**Deterministic data, LLM interpretation.** Numbers (heartbeat scores, alert counts, delta directions) are computed by deterministic engines before the LLM sees them. The LLM interprets and recommends — it cannot invent or modify numbers. `_post_validate()` enforces this by patching any score references in LLM output.

**qwen3 thinking mode disabled for JSON.** The `think` flag is set to `False` whenever `format=json` is set. qwen3's thinking tokens consume the entire response budget and Ollama returns empty JSON when thinking is active.

**Deterministic search first.** `deterministic_parse()` runs before the LLM on every search. Structured queries ("refunds over $100", "top employees by voids") are handled by regex pattern matching — faster, always correct, no LLM cost.

**Merchant isolation via mandatory filter.** `build_query()` always injects `WHERE primary_table.merchant_id = :merchant_id` as the first WHERE clause. This cannot be removed by the LLM or caller. The executor also sets the RLS context function `set_current_merchant()` before execution.

**Report assessments persisted to DB (GRO-158).** Owl reports survive Valkey TTL because `lp_assessment`, `ops_assessment`, `analytics_assessment`, `positive_notes`, and `outlook` are persisted directly on `OwlSession` rows.

---

## 3. Data Model

Four tables in the `app` schema of the `canary` database. All use string UUID primary keys with `generate_uuid` defaults (not PostgreSQL `uuid` type). No pgvector — Owl memory is structured, not vector-embedded.

### `owl_sessions`

One row per completed health check or Owl analysis session. Primary memory anchor.

```python
class OwlSession(AppBase, TenantMixin, AuditMixin):
    __tablename__ = "owl_sessions"

    id: Mapped[str]                      # UUID PK
    session_type: Mapped[str]            # health_check | chat | scheduled
    heartbeat_score: Mapped[int]         # 0-100
    heartbeat_band: Mapped[str]          # healthy | normal | warning | alert
    total_alerts: Mapped[int]
    alert_breakdown: Mapped[Optional[str]]  # JSON: {"critical": N, "high": N, ...}
    category_scores: Mapped[Optional[str]]  # JSON: {"payment": {"alerts": N, "deduction": N}, ...}
    narrative_summary: Mapped[Optional[str]]
    top_finding: Mapped[Optional[str]]
    top_finding_category: Mapped[Optional[str]]
    hc_session_id: Mapped[Optional[str]]    # FK to health check runner session
    previous_session_id: Mapped[Optional[str]]  # FK to owl_sessions.id (delta chain)
    relevance_weight: Mapped[float]         # time-decay; 1.0 = current
    lp_assessment: Mapped[Optional[str]]    # GRO-158: persisted report fields
    ops_assessment: Mapped[Optional[str]]
    analytics_assessment: Mapped[Optional[str]]
    positive_notes: Mapped[Optional[str]]
    outlook: Mapped[Optional[str]]
    # From TenantMixin: merchant_id
    # From AuditMixin: created_at, updated_at, created_by, modified_by
```

Indexes: `(merchant_id, created_at)`, `(merchant_id, session_type)`.

### `owl_findings`

One row per Chirp category that fired within a session. Granularity: one finding per category (payment, cash_drawer, order, timecard, void, gift_card, loyalty).

```python
class OwlFinding(AppBase, AuditMixin):
    __tablename__ = "owl_findings"

    id: Mapped[str]                      # UUID PK
    session_id: Mapped[str]              # FK → owl_sessions.id
    merchant_id: Mapped[str]             # FK → merchants.id (denormalized for querying)
    category: Mapped[str]                # Chirp category
    rule_ids: Mapped[str]                # JSON array: ["C-001", "C-007"]
    severity: Mapped[str]                # highest severity in category
    alert_count: Mapped[int]
    finding_text: Mapped[str]
    recommended_action: Mapped[Optional[str]]
    delta_direction: Mapped[Optional[str]]  # improved | worsened | new | unchanged | resolved
    delta_detail: Mapped[Optional[str]]     # JSON: {"prev_count": N, "curr_count": N, ...}
```

Indexes: `(session_id)`, `(merchant_id, category)`.

### `owl_merchant_memory`

One row per merchant — always-current running context. Updated after every session. One-to-one with merchants.

```python
class OwlMerchantMemory(AppBase, AuditMixin):
    __tablename__ = "owl_merchant_memory"

    id: Mapped[str]                          # UUID PK
    merchant_id: Mapped[str]                 # FK → merchants.id (unique)
    latest_session_id: Mapped[Optional[str]] # FK → owl_sessions.id
    latest_heartbeat_score: Mapped[Optional[int]]
    latest_heartbeat_band: Mapped[Optional[str]]
    session_count: Mapped[int]
    score_trend: Mapped[Optional[str]]       # JSON array (last 12): [{"date": "...", "score": N, "band": "..."}]
    recurring_categories: Mapped[Optional[str]]  # JSON: {"payment": {"streak": N, "first_seen": "...", "last_seen": "..."}}
    running_summary: Mapped[Optional[str]]   # rolling narrative, ~500 tokens max
    actions_taken: Mapped[Optional[str]]     # JSON array of merchant actions
    is_cold_start: Mapped[bool]              # True until first health check completes
```

### `owl_action_log`

Tracks what the merchant did about Owl findings. Outcome is evaluated at the start of the next session.

```python
class OwlActionLog(AppBase, AuditMixin):
    __tablename__ = "owl_action_log"

    id: Mapped[str]                       # UUID PK
    merchant_id: Mapped[str]              # FK → merchants.id
    finding_id: Mapped[Optional[str]]     # FK → owl_findings.id
    session_id: Mapped[Optional[str]]     # FK → owl_sessions.id
    action_type: Mapped[str]              # resolve | dismiss | case_create | follow_up | archive | drill_down
    action_detail: Mapped[Optional[str]]
    outcome: Mapped[Optional[str]]        # improved | no_change | worsened | pending
```

Indexes: `(merchant_id, created_at)`, `(finding_id)`.

**Note on embedding dimension:** The Owl memory tables do not use pgvector. Memory is structured (scores, categories, JSON blobs), not vector-embedded. The platform standard of 1024-dimension embeddings (`qwen3-embedding:8b`) does not apply to this service. Institutional knowledge search uses the platform memory bus MCP at `growdirect_memory_bus:8003`, not a local vector column.

---

## 4. Interfaces

### HTTP Routes — `canary.blueprints.owl_api`

All routes except `/owl/manifest` and `/owl/tools` (GET) require `@jwt_required`. The `g.merchant_id` context variable is set by JWT middleware and used as the mandatory tenant scope.

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET`  | `/owl/manifest` | None | MCP server manifest |
| `GET`  | `/owl/tools` | None | List available MCP tools |
| `POST` | `/owl/tools/<name>` | JWT | Invoke a named MCP tool |
| `GET`  | `/owl/health` | JWT | Owl health check (Ollama status) |
| `POST` | `/owl/one-thing` | JWT | The One Thing — top insight right now |
| `POST` | `/owl/heartbeat` | JWT | Compute store heartbeat |
| `POST` | `/owl/chat` | JWT | Personality-routed chat |
| `GET`  | `/owl/personalities` | JWT | List available personalities |
| `POST` | `/owl/health-check` | JWT | Full McKinsey-style health check report |
| `POST` | `/owl/action` | JWT | Execute a closed-loop action |

### `/owl/chat` Request/Response

**Request:**
```json
{
  "message": "Who should I be coaching right now?",
  "alerts": [...],   // optional — fetched from DB if omitted
  "stats": {}        // optional store stats
}
```

**Response (closed-loop envelope):**
```json
{
  "ok": true,
  "personality": "jpt_detection",
  "message": "Sarah has the most voids this week — 12 against a team average of 3.",
  "output_type": "alert_set",
  "data": { "alerts": [...] },
  "severity": "high",
  "recommended_action": "Have a coaching conversation with Sarah about void procedures.",
  "actions": [
    {"label": "Open case", "action": "case_create", "icon": "folder-plus"},
    {"label": "Follow up", "action": "follow_up", "icon": "link"},
    {"label": "Resolve", "action": "resolve", "icon": "check-circle"},
    {"label": "Dismiss", "action": "dismiss", "icon": "x"}
  ],
  "closes_to": "resolved_or_case_opened",
  "source": "owl",
  "timestamp": "2026-03-30T...",
  "routing": {
    "personality": "jpt_detection",
    "display_name": "Chirp JPT",
    "domain": "loss_prevention",
    "icon": "shield",
    "explicit_address": false,
    "intent_score": 0.714,
    "output_type_inferred": "alert_set"
  }
}
```

### `/owl/health-check` Request/Response

**Request:**
```json
{
  "alerts": [...],    // optional
  "save": true        // persist to owl_sessions (default true)
}
```

**Response:**
```json
{
  "ok": true,
  "session_id": "<uuid>",
  "executive_summary": "Heartbeat score: 74/100 (normal). ...",
  "findings": [
    {
      "category": "payment",
      "severity": "high",
      "title": "3 high-severity refund alerts",
      "detail": "...",
      "trend": "worsened",
      "recommendation": "Review refund logs for unusual patterns."
    }
  ],
  "lp_assessment": "...",
  "ops_assessment": "...",
  "analytics_assessment": "...",
  "top_priority": "...",
  "positive_notes": "...",
  "outlook": "Needs attention",
  "source": "owl",
  "heartbeat_score": 74,
  "heartbeat_band": "normal"
}
```

### `/owl/action` Valid Action Codes

| Action | Output type | Description |
|--------|-------------|-------------|
| `case_create` | alert_set | Create a Fox investigation case |
| `follow_up` | alert_set | Seal alert context into Fox evidence locker |
| `resolve` | alert_set, number | Mark alert(s) resolved |
| `dismiss` | alert_set | Dismiss alert(s) |
| `archive` | memo | Archive a memo |
| `share` | memo | Share a memo |
| `checklist_start` | checklist | Start a checklist |
| `template_save` | checklist | Save checklist as template |
| `drill_down` | number | Drill into supporting data |
| `drill_row` | memo | Drill into a specific row |

### MCP Tools (`canary-owl` server)

Registered via `MCPRegistry` in `tools.py`. Seven tools:

| Tool | Category | LLM Required | Description |
|------|----------|--------------|-------------|
| `the_one_thing` | insights | Optional | Top insight from all active alerts |
| `ask` | query | Yes | Freeform question to Owl |
| `heartbeat` | health | No | Store health at a glance (deterministic) |
| `check_heartbeat` | health | Optional | Full health check with memory context + optional report |
| `score_payment` | scoring | No | Run stateless Chirp rules on a payment payload |
| `search` | search | Optional | Natural language CRDM query |
| `dashboard` | dashboard | No | Operational KPI dashboard |
| `knowledge_search` | knowledge | No | Search institutional knowledge base |

---

## 5. Service Layer

Modules are grouped by subsystem.

### Core: LLM Client (`client.py`)

**`owl_healthy() -> bool`**
Checks Ollama reachability via `GET /api/tags` with a 3-second timeout. Used as the gate before every LLM call.

**`ask_owl(prompt, system_prompt, format_json, timeout) -> Dict`**
Core Ollama request. Sets `format="json"` and `think=False` when `format_json=True` (qwen3 compatibility). Returns `{"response": ..., "ok": True}` on success or `{"ok": False, "error": "timeout|connection_refused|..."}` on failure.

**`get_the_one_thing(alerts, stats, merchant_context) -> Dict`**
Identifies the single most important insight from all active alerts. Passes top 20 alerts with a structured system prompt. Falls back to `_fallback_one_thing()` when Ollama is offline.

**`_fallback_one_thing(alerts) -> Dict`**
Deterministic ranking using `SEVERITY_RANK` (critical=0, high=1, medium=2, low=3, info=4). When `impact_cents` is present, uses `rank_by_impact()` with severity 60% / impact 40% weighting (GRO-141).

### Core: Memory Service (`memory.py`)

**`assemble_context(merchant_id, current_alerts, current_heartbeat, memory, previous_findings) -> str`**
Builds the four-window prompt injection block:
- Window 1: `MERCHANT HISTORY` from `OwlMerchantMemory.running_summary` or cold-start message.
- Window 2: `CHANGES SINCE LAST CHECK` via `_format_delta_block(previous_findings)`.
- Window 2b: `DASHBOARD STATE` via `build_dashboard_context(merchant_id)`.
- Window 3: `HEARTBEAT` block via `format_heartbeat_block(heartbeat)`.

**`build_heartbeat_context(alerts) -> str`**
Pure function. Computes heartbeat from alert list and formats the HEARTBEAT block.

**`build_dashboard_context(merchant_id) -> Optional[str]`**
Queries `get_dashboard_data()` and `get_top_risks_data()` to build a `DASHBOARD STATE` block. Returns `None` when no data is available.

**`create_owl_session(db_session, merchant_id, heartbeat, alerts, ...) -> OwlSession`**
Creates an `OwlSession` row, chains to previous session via `previous_session_id`. Persists all five report assessment fields.

**`create_owl_findings(db_session, session_id, merchant_id, alerts, previous_findings) -> List[OwlFinding]`**
Creates one `OwlFinding` per Chirp category. Computes delta vs previous findings (improved/worsened/new/resolved). Also creates resolved findings for categories that cleared since last session.

**`update_merchant_memory(db_session, merchant_id, session, findings) -> OwlMerchantMemory`**
Upserts `OwlMerchantMemory`. Updates `score_trend` (last 12 entries), `recurring_categories` (streak counter), flips `is_cold_start` after first session.

**`get_merchant_memory(db_session, merchant_id) -> Optional[Dict]`**
Loads `OwlMerchantMemory` as a plain dict.

**`get_previous_findings(db_session, merchant_id) -> List[Dict]`**
Loads findings from the most recent `OwlSession` for delta computation.

**`compute_relevance(created_at, now) -> float`**
Exponential decay with 14-day half-life. Returns value between 0.05 and 1.0.

### Core: Report Generator (`report.py`)

**`generate_health_report(context, alerts, heartbeat_score, heartbeat_band, alert_breakdown, findings_data, timeout) -> Dict`**
Sends assembled context + current alert summary to Ollama with `REPORT_SYSTEM_PROMPT` (McKinsey-style, professional tone, three-lens structure). 120-second timeout for `qwen3:14b`. Falls back to `_fallback_report()` if offline. Enriches prompt with institutional knowledge (analytics lens affinity) via `_get_institutional_context_for_report()`.

**`_post_validate(report, heartbeat_score, heartbeat_band, alert_breakdown, findings_data) -> Dict`**
Patches LLM output: fixes score/band references in `executive_summary` using regex replacement (tolerates ±15 point drift), aligns finding `trend` fields with delta engine output, migrates legacy field names (`jim_assessment` → `lp_assessment`, etc.), ensures all required fields exist.

**`_fallback_report(alerts, heartbeat_score, heartbeat_band, alert_breakdown, findings_data) -> Dict`**
Deterministic fallback. Generates executive summary, findings, and assessments from heartbeat data without any LLM involvement.

**`validate_report_structure(report) -> List[str]`**
Returns list of validation errors for required fields and correct types.

**`extract_narrative_summary(report) -> str`**
Extracts 2-3 sentence narrative from report for `OwlMerchantMemory.running_summary`. Caps at ~500 tokens (~2000 characters).

### Core: Delta Engine (`delta.py`)

**`compute_session_deltas(current_alerts, previous_findings) -> List[Dict]`**
Compares current alerts against previous session findings by Chirp category. Returns delta direction (improved/worsened/new/unchanged/resolved) with counts. Also generates resolved entries for categories that cleared.

**`format_delta_summary(deltas) -> str`**
Formats delta list as a human-readable text block for LLM prompt injection.

**`compute_recurring_updates(current_categories, recurring, now_str) -> Dict`**
Updates streak counters for recurring categories. Categories appearing 3+ consecutive sessions are flagged as recurring patterns, elevated in prompts.

**`get_recurring_summary(recurring, min_streak) -> str`**
Formats recurring categories (streak >= `min_streak`, default 3) for prompt injection.

### Chat: Router (`router.py`)

**`route_message(message) -> RoutedMessage`**
Two-phase deterministic routing:
1. Attempts to extract an explicit personality address via `_ADDRESS_PATTERNS` (e.g., "Hey JPT", "@detection:", "analytics:").
2. Falls back to intent keyword scoring: counts keyword matches, normalizes by `sqrt(len(keywords))` to prevent larger keyword sets from always winning.

Returns `RoutedMessage(personality, clean_message, raw_message, explicit_address, intent_score)`.

**`infer_output_type(message, personality) -> str`**
Counts signal words for each output type (`alert_set`, `memo`, `checklist`, `number`). Falls back to personality's `preferred_outputs[0]`.

### Chat: Personality Definitions (`personality.py`)

Three `OwlPersonality` instances (frozen dataclasses):

| Name | Display | Domain | Default outputs | Default route |
|------|---------|--------|-----------------|---------------|
| `jpt_detection` | Chirp JPT | loss_prevention | alert_set, number | Yes (LP is the wedge) |
| `jpt_operations` | Chirp JPT | operations | checklist, memo | No |
| `jpt_analytics` | Chirp JPT | analytics | number, memo | No |

All three personalities receive the same `HEARTBEAT_KNOWLEDGE` block appended to their system prompts. This defines the score/band system and seven Chirp detection categories.

`PERSONALITY_ALIASES` maps natural language terms to personality names (e.g., "lp" → `jpt_detection`, "process" → `jpt_operations`, "benchmark" → `jpt_analytics`).

### Chat: Output Formatter (`output_formatter.py`)

**`format_response(personality_name, message, output_type, data, ...) -> Dict`**
Builds the canonical closed-loop envelope. Attaches `EXIT_ACTIONS` and `CLOSES_TO` by output type:
- `alert_set` → Open case / Follow up / Resolve / Dismiss → `resolved_or_case_opened`
- `memo` → Drill into row / Archive / Share → `archived_or_shared`
- `checklist` → Start checklist / Save as template → `completed_or_saved`
- `number` → Dig deeper / Got it → `resolved_or_drilled`

**`parse_owl_output(personality_name, owl_response, fallback_output_type) -> Dict`**
Parses raw LLM JSON (expects `message`, `output_type`, `data`, `recommended_action`, `severity`) into a full envelope. Handles malformed output gracefully.

**`format_fallback_alert_set(personality_name, alerts, message) -> Dict`**
Deterministic alert_set envelope for when the LLM is offline.

**`format_fallback_number(personality_name, label, value, context, severity) -> Dict`**
Deterministic number envelope.

### Context: Context Gatherer (`context_gatherer.py`)

**`gather_alert_context(db_session, merchant_id, alert_id) -> Dict`**
Called when "Follow Up" or "Add to Case" is tapped. Gathers: alert fields, employee alert frequency (last 7 days), related transaction fields (if alert references a transaction). Returns partial context rather than raising on missing data.

**`gather_transaction_context(db_session_app, db_session_sales, merchant_id, txn_id) -> Dict`**
Gathers: full CRDM transaction fields, employee transaction patterns (last 7 days, by type), keyed-entry anomaly ratio. Used for Fox evidence locker sealing (GRO-305 Task 4).

### Context: Institutional Knowledge (`institutional.py`)

**`build_institutional_context(personality_name, user_message, token_budget, max_memories) -> str`**
Retrieves relevant institutional knowledge from the ALX memory bus MCP (`growdirect_memory_bus:8003`) for Window 0 injection. Enriches query with `PERSONALITY_AFFINITY` keywords (up to 4 terms). Formats results under token budget. Returns empty string if memory bus is unavailable.

**`knowledge_search(query, personality, limit) -> Dict`**
Exposed as `knowledge_search` MCP tool. Returns structured search results (not formatted for prompt injection). Strips embedding vectors from results.

Personality-domain affinity:
- `jpt_detection` → LP, detection, chirp, alert, employee, fox, coaching, refund, void, cash drawer
- `jpt_operations` → process, operations, architecture, analytics, pipeline, infrastructure
- `jpt_analytics` → research, benchmark, methodology, ontology, framework, academic, measurement

### Drill: Drill Builder (`drill.py`)

**`build_drill_intent(drill_context) -> StructuredIntent`**
Single-level drill. Reconstructs original filters from `drill_context`, adds group value as equality filter. Bypasses LLM — enters pipeline at stage 2 (Validate).

**`build_multilevel_drill_intent(drill_context) -> StructuredIntent`**
Multi-level drill (GRO-236). Accumulates filters from all breadcrumb levels, resolves next GROUP BY from drill order. Sets `aggregation="count"` when next level exists, `None` for detail level.

### Drill: Drill Orders (`drill_orders.py`)

Defines five GROUP BY hierarchies for the transaction drill path:

| Order | Level 1 | Level 2 | Level 3 |
|-------|---------|---------|---------|
| `default` | `transactions.transaction_date` | `employees.employee_name` | (detail) |
| `by_employee` | `employees.employee_name` | `transactions.transaction_date` | (detail) |
| `by_location` | `locations.location_name` | `transactions.transaction_date` | (detail) |
| `by_product` | `transaction_line_items.item_name` | `transactions.transaction_date` | `employees.employee_name` |
| `by_type` | `transactions.transaction_type` | `transactions.transaction_date` | (detail) |

**`next_group_by(order_name, current_group_by) -> Optional[str]`**
Returns next level in drill order, or `None` at detail level.

### Search: Facade (`search/facade.py`)

**`owl_search(question, merchant_id, personality, timeout) -> Dict`**
Primary search entry point. Runs deterministic parser first; falls through to LLM. For transaction result sets, returns the flat drill envelope (`_format_drill_results`) instead of the personality-wrapped format so `renderDrillView` gets consistent structure from both chat and drill paths (GRO-223/305).

**`drill_search(merchant_id, filters, tables, group_by, drill_order, label, limit, breadcrumbs, drill_field, drill_value) -> Dict`**
Unified drill entry point. All routes (`/drill`, `/owl/drill`, `/transactions`) call this function. Entry mode builds initial grouped query; drill-down mode accumulates breadcrumb filters and resolves next level.

### Search: Intent Parser (`search/intent.py`)

**`parse_intent(question, personality, merchant_id, timeout) -> StructuredIntent`**
Stage 1 (LLM). Sends the question and the full field registry context to Ollama with `INTENT_PARSER_SYSTEM` prompt. Returns empty low-confidence `StructuredIntent` when Ollama is offline. Strips schema prefixes from LLM-returned table names, clamps limit to 1-100.

`StructuredIntent` fields:
- `filters: List[FilterCondition]` — field + operator + value triples
- `tables: List[str]` — which CRDM tables to query
- `sort_by`, `sort_order`, `limit` — result ordering
- `aggregation`, `aggregation_field`, `group_by`, `having` — aggregate query support
- `confidence: float` — LLM self-assessed confidence (0.0-1.0)
- `raw_question: str`, `personality: str`

### Search: Deterministic Parser (`search/deterministic.py`)

Handles all structured queries without the LLM. Returns `None` when the question is ambiguous (facade then sends to LLM). Pattern families:

| Family | Examples | Key patterns |
|--------|---------|--------------|
| Transaction type | "refunds over $100", "voids this week" | `TXN_TYPES` dict, multi-word first |
| Amount | "over $50", "between $20 and $100", "exactly $75" | `_AMOUNT_PATTERNS` (5 operators) |
| Date range | "today", "last week", "last 30 days" | `DATE_RANGES` dict + hour-level windows |
| Aggregation | "how many", "total amount", "average" | `_AGG_PATTERNS` dict |
| Group by | "by employee", "top 10 employees by voids" | `_GROUP_BY_MAP` + `top_by` regex |
| HAVING | "more than 5 times", "having count > 3" | threshold detection (avoids $ ambiguity) |
| Top-N | "top 10", "first 5" | `_TOP_N_RE` regex |
| Alert | "critical alerts", "open alerts" | `SEVERITY_WORDS` + `ALERT_STATUS_WORDS` |
| Case | "open cases", "investigating" | `CASE_STATUS_WORDS` |
| Discount | "discounts today" | keyword signal → `transaction_line_items` |
| Gift card | "gift card loads", "gift card redeems" | `GIFT_CARD_ACTIVITY_WORDS` + bare "gift card" |
| Price override | "price overrides", "items sold above catalog price" | `_PRICE_OVERRIDE_SIGNALS` → products join |

### Search: Validator (`search/validator.py`)

**`validate_intent(intent) -> Tuple[bool, List[str]]`**
Stage 2. Validates: table names against `VALID_TABLES`, filter fields and operators against `FieldRegistry`, operator type-family compatibility, aggregation field type (sum/avg/min/max require numeric), group_by field existence, limit range (1-100). Returns `(is_valid, issues)`. Facade aborts if more than 3 issues.

### Search: Query Builder (`search/builder.py`)

**`build_query(intent, merchant_id) -> BuiltQuery`**
Stage 3. Builds parameterized PostgreSQL. Security invariants:
- `merchant_id` is always the first WHERE clause.
- All values are bind parameters (`:name` style, never string-interpolated).
- Column names are validated against `FieldRegistry` before use.
- Cross-schema tenant isolation: `(transaction_line_items, products)` JOIN includes `merchant_id = merchant_id` condition.

`TABLE_SCHEMA` maps 28+ tables across `sales`, `app`, and `metrics` schemas.

`JOIN_MAP` defines join paths for 25+ table pairs. Special handling for `alert_history`: uses `DISTINCT ON (alert_id)` subquery to return only the latest status per alert, preventing row duplication.

`TENANT_ISOLATED_JOINS` tracks cross-schema joins that need explicit merchant isolation.

Aggregate SELECT: datetime `group_by` fields are truncated to `DATE` and formatted as `YYYY-MM-DD` strings via `TO_CHAR` so they survive JSON serialization and can be passed back as drill filter values.

### Search: Executor (`search/executor.py`)

**`execute_search(query, merchant_id) -> Dict`**
Stage 4. Sets `statement_timeout = 5000ms` before execution. Calls `set_current_merchant(:mid)` for RLS context. Returns `{"ok": bool, "rows": [...], "row_count": int, "query_time_ms": float, ...}`.

**`execute_search_standalone(query, merchant_id, connection_string) -> Dict`**
Testing variant that accepts a connection string directly.

### Search: Operator Vocabulary (`search/operators.py`)

22 typed operators ported from `CRDMSearchableBuilder.CreateSearchable.cs`:

| Family | Operators |
|--------|-----------|
| All types | `equal`, `not_equal`, `is_null`, `is_not_null` |
| Text | `contains`, `not_contains`, `starts_with`, `ends_with`, `match` (PostgreSQL regex `~*`) |
| Numeric + datetime | `greater_than`, `less_than`, `greater_equal`, `less_equal`, `between` |
| Set membership | `in_list` (`= ANY(...)`), `not_in_list` (`!= ALL(...)`) |
| Boolean | `is_true`, `is_false` |
| Datetime | `within_days`, `on_date`, `before`, `after` |

### Search: Field Registry (`search/registry.py`)

`FieldRegistry` is a singleton built once at startup and cached. Maps every searchable CRDM column to its `SearchableField` metadata (table, column, display name, type family, schema, operator list).

`SearchableField.search_key` is the dot-notation key used by the LLM and deterministic parser (`table.column`).

`to_prompt_context()` serializes the full registry as a compact field listing for LLM injection. Groups fields by database and table.

Five type families: `text`, `numeric`, `datetime`, `boolean`, `guid`. Maps from PostgreSQL types via `_PG_TYPE_MAP`.

---

## 6. Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `OWL_URL` | `http://host.docker.internal:11434` | Ollama API base URL |
| `OWL_MODEL` | `qwen3:14b` | Model tag for all Owl inference |
| `QUERY_TIMEOUT_MS` | `5000` | PostgreSQL statement timeout for search queries |
| `MAX_RESULTS` | `100` | Hard cap on search result rows |

The platform embedding model (`qwen3-embedding:8b`, 1024 dimensions) is accessed via the shared memory bus at `http://growdirect_memory_bus:8003`. Owl itself does not call Ollama for embeddings — only for generation.

`OWL_URL` defaults to `host.docker.internal:11434` in the service module (read from environment via `os.getenv`). In the Canary Docker Compose stack, the container should have `OWL_URL=http://growdirect_ollama:11434` to use the shared Ollama service on the `growdirect` network.

---

## 7. Security & Compliance

**Tenant isolation — mandatory filter pattern.** Every search query built by `build_query()` includes `WHERE primary_table.merchant_id = :merchant_id` as the first WHERE clause. This is injected from the authenticated `g.merchant_id` context and cannot be overridden by LLM output. The executor additionally calls `set_current_merchant()` to set the RLS context function.

**Cross-schema tenant isolation.** The `transaction_line_items → products` JOIN (GRO-244) is a cross-schema join where both tables have independent `merchant_id` columns. The builder adds an explicit `AND primary_table.merchant_id = joined_table.merchant_id` condition for all joins in `TENANT_ISOLATED_JOINS`.

**Parameterized queries — no SQL injection.** All user-controlled values, LLM-generated values, and drill filter values go through bind parameters. Column and table names are validated against `FieldRegistry` and `VALID_TABLES` before use in SQL.

**Query timeout enforcement.** `SET LOCAL statement_timeout = '5000'` runs before every search query. Combined with `LIMIT :query_limit` (max 100), this prevents expensive merchant queries from consuming database resources.

**No external data leakage between tenants.** The LLM receives only the merchant's own alert data and anonymized institutional knowledge from the memory bus. The Owl prompt never contains PII or data from other merchants.

**Evidence locker pattern.** When a merchant taps "Follow Up," `gather_alert_context()` and `gather_transaction_context()` collect structured context for sealing into Fox. Canary is a lens, not a database — evidence GUIDs point back to RaaS raw data.

---

## 8. Error Handling

**LLM failures (timeout, connection error, bad JSON):**
Every LLM call path has a deterministic fallback:
- `get_the_one_thing()` → `_fallback_one_thing()` (severity × impact ranking)
- `generate_health_report()` → `_fallback_report()` (deterministic per-category summaries)
- `owl_search()` → returns low-confidence memo envelope
- `/owl/chat` → `_chat_fallback()` (alert count summary or deterministic alert list)

**qwen3 thinking mode conflict.** `think=False` is set whenever `format=json` is used. Without this, qwen3's chain-of-thought tokens consume the full response budget and Ollama returns empty JSON.

**Post-validation hallucination correction.** `_post_validate()` runs after every LLM report generation. It patches score references in `executive_summary` (tolerating ±15 point drift), aligns finding trends with the delta engine, and ensures all required fields exist.

**Memory context failures.** `assemble_context()` and memory loading are wrapped in try/except with logger.debug fallthrough. A missing memory context results in a cold-start message rather than an error — the report still runs.

**Institutional knowledge (Window 0) failures.** `build_institutional_context()` returns empty string on any failure. The Owl proceeds without institutional context rather than blocking.

**DB persistence failures.** In `/owl/health-check`, session/findings persistence is wrapped in a try/except with `finally: db.close()`. Persistence failure is logged but non-fatal — the report is still returned to the merchant. `db.rollback()` is called on exception to avoid transaction leaks.

**Search validation failures.** Up to 3 validation issues are tolerated (query proceeds with a warning). More than 3 issues triggers a user-facing "trouble parsing" message. Intent confidence < 0.3 with no filters returns an "I'm not sure what you're looking for" message.

---

## 9. Testing

**Integration tests** (require PostgreSQL):

| File | Description |
|------|-------------|
| `tests/integration/test_owl_memory_integration.py` | OwlSession, OwlFinding, OwlMerchantMemory CRUD; delta computation; memory update cycle |
| `tests/integration/test_owl_search_db.py` | Search pipeline end-to-end: intent parsing → SQL build → PostgreSQL execution; tenant isolation; aggregates |

**Live tests** (require Ollama running):

| File | Description |
|------|-------------|
| `tests/integration/test_owl_chat_live.py` | Chat route with real Ollama; personality routing; fallback behavior |
| `tests/integration/test_owl_search_live.py` | Natural language questions through full LLM parse → SQL → results pipeline |

**Key test scenarios for each layer:**
- `client.py`: `owl_healthy()` with Ollama up/down; `ask_owl()` timeout and JSON parse failure.
- `memory.py`: Cold start creates OwlMerchantMemory; second session flips `is_cold_start`, increments `session_count`; score trend capped at 12 entries; recurring category streak increment and decay.
- `delta.py`: All four delta directions (improved, worsened, new, resolved) from category count changes.
- `deterministic.py`: Dollar-to-cents conversion; date range calculation; group-by resolution; HAVING threshold detection without triggering amount pattern false-positive.
- `validator.py`: Unknown field rejection; operator/type-family mismatch; limit clamping.
- `builder.py`: merchant_id always present; JOIN paths for all table combinations; aggregate SELECT format.

---

## 10. Dependencies

### Upstream

| Dependency | What Owl needs |
|------------|---------------|
| **Chirp detection engine** | Active alert list with `rule_id`, `severity`, `category`, `employee_id`, `amount_cents`, `impact_cents` |
| **Heartbeat engine** (`canary.services.health_check.heartbeat`) | `compute_heartbeat(alerts) -> HeartbeatResult` — score, band, breakdown |
| **Impact scoring** (`canary.services.impact_scoring`) | `rank_by_impact(alerts)` — used in fallback One Thing when `impact_cents` is available |
| **Dashboard service** (`canary.services.dashboard`) | `get_dashboard_data()`, `get_top_risks_data()` — KPI bands for Window 2b and the dashboard MCP tool |
| **Fox** (`canary.services.fox`) | `create_case_from_context()` — unified case creation from Owl action dispatcher |
| **Chirp stateless engine** | `evaluate_stateless(payment)` — used by `score_payment` MCP tool |

### Downstream

| Consumer | How it uses Owl |
|----------|----------------|
| **Mobile app** | Calls `/owl/chat`, `/owl/health-check`, `/owl/one-thing`, `/owl/action` for all merchant-facing intelligence |
| **Fox** | Receives structured context from `gather_alert_context()` / `gather_transaction_context()` for evidence sealing |
| **MCP clients** | Access all tools via the `canary-owl` MCP server at port 8001 |

### Shared Infrastructure

| Service | Usage |
|---------|-------|
| **Ollama** (`growdirect_ollama:11434`) | LLM inference — `qwen3:14b` for report, chat, and search intent |
| **PostgreSQL** (`growdirect_postgres:5432`, `canary` database) | All Owl memory tables (`owl_sessions`, `owl_findings`, `owl_merchant_memory`, `owl_action_log`) in `app` schema; CRDM search tables across `app`, `sales`, `metrics` schemas |
| **Memory Bus MCP** (`growdirect_memory_bus:8003`) | Institutional knowledge retrieval for Window 0 injection and `knowledge_search` tool |
| **Valkey** | Session/auth only — Owl does not use Valkey directly (GRO-158: report data persisted to DB to survive TTL) |

---

## 11. Known Issues & Reconciliation

### Embedding Dimension — Not Applicable to Owl Memory

**Platform standard:** `qwen3-embedding:8b`, 1024 dimensions, `Vector(1024)` column.

**Owl Memory:** Does not use pgvector. All four `owl_*` tables store structured data (integers, JSON text, timestamps). There is no embedding column in any Owl table. Semantic search for institutional knowledge is delegated to the platform memory bus MCP — Owl does not maintain its own vector store.

**Verdict:** No reconciliation needed. The embedding standard applies to other Canary services (e.g., any future semantic alert similarity). Owl's memory architecture is intentionally deterministic and structured.

### OWL_URL Default — Docker Networking Mismatch

The default `OWL_URL = "http://host.docker.internal:11434"` in `client.py` works on macOS Docker Desktop (which resolves `host.docker.internal` to the host machine) but will fail on Linux-based Docker hosts without explicit host mapping. Production and QA deployments must set `OWL_URL=http://growdirect_ollama:11434` in the app's `.env` file to use the shared Ollama container on the `growdirect` network.

### qwen3:14b Timeout Budget

The report generator uses a 120-second timeout for `qwen3:14b`. This is required because the McKinsey-style report prompt is long (context + 25 alerts + full schema). Chat uses 15 seconds, search intent uses 30 seconds. If qwen3 is replaced with a slower model, these timeouts may need adjustment.

### Legacy Field Names in Report Output

`_post_validate()` includes a `_LEGACY_FIELD_MAP` migration (`jim_assessment` → `lp_assessment`, `tom_assessment` → `ops_assessment`, `phd_assessment` → `analytics_assessment`). This migration exists because earlier Owl sessions used persona names instead of role names. Any `OwlSession` rows written before GRO-158 may have legacy field names in their `lp_assessment` column. The migrator is safe to remove once all legacy sessions have aged out of active use.

### Single-Level vs. Multi-Level Drill

`build_drill_intent()` (single-level, `drill.py`) and `build_multilevel_drill_intent()` (multi-level, `drill.py`) are two separate functions with slightly different `drill_context` schemas. The `drill_search()` facade in `facade.py` is the canonical entry point for all drill paths and handles breadcrumb accumulation directly — new callers should use `drill_search()` rather than either drill intent builder directly.
