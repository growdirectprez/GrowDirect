# Owl

## Overview

Owl is the AI intelligence layer for Canary LP. It provides personality-routed chat, context-aware health check reports, and an MCP tool registry that any client can discover and invoke.

**Chirp JPT Lenses.** Three frozen-dataclass lenses route merchant messages deterministically (no LLM in routing). jpt_detection (loss prevention) is the default -- LP is the product wedge. jpt_operations handles process and scheduling questions. jpt_analytics covers benchmarks, trends, and research. Each lens defines a system prompt, intent keywords, preferred output types, and an icon. Routing uses keyword intent scoring with sqrt normalization. Highest score wins; ties go to jpt_detection.

**4-Window Context Assembly.** Every Owl prompt is built from four context windows injected before the merchant's message: Window 0 (Institutional Knowledge, ~2,000 tokens) -- ALX pgvector semantic search filtered by JPT lens affinity (detection sees LP patterns, operations sees process architecture, analytics sees everything including foundation research); Window 1 (Running Summary, ~1,000 tokens) -- compressed merchant history from `owl_merchant_memory.running_summary`; Window 2 (Delta, ~1,000 tokens) -- what improved/worsened/appeared/resolved since last session via the deterministic delta engine; Window 3 (Heartbeat + Dashboard, ~700 tokens) -- current score, band, severity breakdown. Plus ~500 tokens of top-5 active alerts. Total prompt budget ~6,200 tokens with ~1,800 reserved for generation.

**Output Formatting.** Every Owl response is wrapped in a closed-loop envelope with one of four output types: `alert_set` (exit actions: Open case, Follow up, Resolve, Dismiss; closes to `resolved_or_case_opened`), `memo` (Archive, Share; `archived_or_shared`), `checklist` (Start checklist, Save as template; `completed_or_saved`), `number` (Dig deeper, Got it; `resolved_or_drilled`). No orphan outputs -- every response terminates in a one-tap merchant action.

**External dependency.** Ollama running qwen3:14b at `host.docker.internal:11434` (env vars `OWL_URL`, `OWL_MODEL`). Critical workaround: when `format_json=True`, the client sets `think=false` because qwen3's thinking mode with `format=json` returns empty `{}`.

**Fallbacks.** When Ollama is offline, all paths degrade gracefully to deterministic logic -- severity-based alert ranking for The One Thing (severity 60%, impact 40% when `impact_cents` available), template-based reports, and formatted envelopes with `source="fallback"`.

## API Contracts

**Blueprint:** `owl_api` at `/owl`. MCP server name: `canary-owl`, version `0.1.0`.

**Public endpoints (no auth):**
- `GET /owl/manifest` -- MCP protocol manifest with full tool list.
- `GET /owl/tools` -- All registered tools in MCP format.
- `GET /owl/health` -- Ollama status. Returns `{owl_status, url, model}`. 200 if healthy, 503 if offline.
- `GET /owl/personalities` -- Lists Chirp JPT lenses for chat UI picker.

**JWT-protected endpoints:**
- `POST /owl/tools/<name>` -- Generic MCP tool invocation. Params from JSON body, context from JWT.
- `POST /owl/one-thing` -- The single most important insight. Auto-fetches alerts from DB if not provided. Returns `{headline, detail, severity, confidence, category, source}`.
- `POST /owl/heartbeat` -- Store health score. Returns `{score, band, alert_counts, total_alerts}`.
- `POST /owl/chat` -- Full personality-routed chat. Request: `{message, alerts?, stats?}`. Response: closed-loop envelope plus routing metadata `{personality, display_name, domain, icon, explicit_address, intent_score, output_type_inferred}`.
- `POST /owl/health-check` -- McKinsey-style report. Seven-step pipeline: get alerts, compute heartbeat, load memory, assemble context, generate report (LLM or fallback), post-validate, persist. Output: `{executive_summary, findings[], lp_assessment, ops_assessment, analytics_assessment, top_priority, positive_notes, outlook}`. Chat timeout: 15s. Report timeout: 120s. Alert fetch limit: 50.
- `POST /owl/action` -- Closed-loop action dispatcher. 10 action codes: `case_create` (creates FoxCase + AlertHistory), `follow_up` (creates/appends to Fox case with RaaS evidence refs `raas:{merchant_id}:{source_table}:{source_id}`), `resolve`, `dismiss` (reason required), `archive`, `share`, `checklist_start`, `template_save`, `drill_down`. All successful actions logged to `owl_action_log` (best-effort, non-blocking).

**8 MCP Tools:**
1. `the_one_thing` (insights) -- Single most important insight. LLM with deterministic fallback.
2. `ask` (query) -- Freeform plain-English question. LLM required.
3. `heartbeat` (health) -- Store health score 0-100. Pure computation, no LLM.
4. `check_heartbeat` (health) -- Full health check with memory context and optional McKinsey report.
5. `score_payment` (scoring) -- Stateless Chirp rule evaluation on a parsed Square payment.
6. `search` (search) -- Natural language CDM query translated to structured PostgreSQL query.
7. `dashboard` (insights) -- Health score, top concern, anomaly count, metric bands. Deterministic.
8. `knowledge_search` (search) -- ALX institutional knowledge via pgvector semantic similarity.

**Python service API (internal):** `owl_healthy() -> bool`, `ask_owl(prompt, system_prompt, format_json, timeout) -> Dict`, `get_the_one_thing(alerts, stats, merchant_context) -> Dict`, `route_message(message) -> RoutedMessage`, `infer_output_type(message, personality) -> str`, `get_personality(name) -> OwlPersonality`, `list_personalities() -> List[Dict]`, `format_response(...)` / `parse_owl_output(...)` / `format_fallback_alert_set(...)` / `format_fallback_number(...)`.

## Data Model

Four tables in `app` schema (`canary_app`). All extend `AppBase` + `AuditMixin` (created_at/modified_at/created_by/modified_by). Access pattern: append-only (sessions and findings are never updated after creation; merchant memory is upserted).

**`owl_sessions`** -- One row per completed analysis run.
Columns: `id` (String(36) PK), `merchant_id` (String(36), TenantMixin), `session_type` (String(20): health_check/chat/scheduled), `heartbeat_score` (Integer 0-100), `heartbeat_band` (String(20): healthy/normal/warning/alert), `total_alerts` (Integer), `alert_breakdown` (Text JSON: `{critical: N, high: N, ...}`), `category_scores` (Text JSON per Chirp category with alerts count and deduction), `narrative_summary` (Text, LLM-generated 2-3 sentences), `top_finding` (Text), `top_finding_category` (String(50)), `hc_session_id` (String(36)), `previous_session_id` (String(36) FK to self for delta chain), `relevance_weight` (Float, time-decay: 1.0 current, 0.05 floor).
Indexes: `(merchant_id, created_at)`, `(merchant_id, session_type)`.

**`owl_findings`** -- One row per Chirp category that fired within a session.
Columns: `id` (PK), `session_id` (FK to owl_sessions), `merchant_id`, `category` (String(50): payment/cash_drawer/order/timecard/void/gift_card/loyalty), `rule_ids` (Text JSON array), `severity` (String(20), highest in category), `alert_count` (Integer), `finding_text` (Text), `recommended_action` (Text), `delta_direction` (String(20): improved/worsened/new/unchanged/resolved), `delta_detail` (Text JSON with prev_count/curr_count/prev_severity).
Indexes: `(session_id)`, `(merchant_id, category)`.

**`owl_merchant_memory`** -- One row per merchant, always-current. This is what gets injected into prompts.
Columns: `id` (PK), `merchant_id` (UNIQUE), `latest_session_id` (FK), `latest_heartbeat_score` (Integer), `latest_heartbeat_band` (String(20)), `session_count` (Integer), `score_trend` (Text JSON array, last 12 entries: `[{date, score, band}]`), `recurring_categories` (Text JSON: `{payment: {streak, first_seen, last_seen}}`), `running_summary` (Text, rolling narrative ~500 tokens), `actions_taken` (Text JSON array), `is_cold_start` (Boolean, true until first health check).

**`owl_action_log`** -- Tracks merchant actions on findings. Outcome evaluated next session.
Columns: `id` (PK), `merchant_id`, `finding_id` (FK to owl_findings, optional), `session_id` (FK, optional), `action_type` (String(50): resolve/dismiss/case_create/follow_up/archive/drill_down), `action_detail` (Text JSON), `outcome` (String(50): improved/no_change/worsened/pending).
Indexes: `(merchant_id, created_at)`, `(finding_id)`.

**Time decay.** Exponential decay with 14-day half-life, floor 0.05: `max(0.05, pow(2, -days_old / 14.0))`. At 7 days: 0.71, 14 days: 0.50, 28 days: 0.25, 60+ days: 0.05.

**In-memory structures.** `OwlPersonality` (frozen dataclass: name, display_name, domain, system_prompt, preferred_outputs, intent_keywords, icon), `RoutedMessage` (dataclass: personality, clean_message, raw_message, explicit_address, intent_score), closed-loop envelope dict (personality, message, output_type, data, severity, recommended_action, actions[], closes_to, source, timestamp).

## Workflows

**Chat Flow.** (1) Merchant sends message via `POST /owl/chat`. (2) Router extracts explicit address via regex; if no match, scores intent keywords against all three personalities using `matches / sqrt(keywords)` normalization. Produces `RoutedMessage` with selected personality and cleaned message. (3) `infer_output_type()` counts signal words to classify expected output (alert_set/memo/checklist/number), falling back to personality's first preferred output. (4) `_get_memory_context()` assembles the 4-window context: Window 0 via `build_institutional_context()` (pgvector search filtered by personality affinity), Windows 1-3 via `assemble_context()` (running summary, delta, heartbeat). All best-effort -- returns empty string on failure. (5) System prompt built: personality definition + HEARTBEAT_KNOWLEDGE + institutional context + merchant context + top 5 alerts + stats. (6) `ask_owl(clean_message, system_prompt, format_json=True, timeout=15)` posts to Ollama `/api/generate`. (7) `parse_owl_output()` extracts message/output_type/data/severity from LLM JSON, wraps in closed-loop envelope with exit actions and `closes_to` terminal state. (8) If LLM fails at any point, `_chat_fallback()` produces a deterministic envelope with `source="fallback"`. (9) Routing metadata attached to response. Merchant sees response with action buttons.

**Closed-Loop Action Flow.** Merchant taps an action button. `POST /owl/action` dispatches to handler by action code. `case_create`: loads alerts from DB, creates FoxCase via FoxCaseService, links alerts via FoxCaseAlert, writes AlertHistory(case_opened). `follow_up`: checks if alerts already link to an open Fox case -- if yes, appends evidence; if no, creates new case. Builds GUID evidence refs (`raas:{merchant_id}:{source_table}:{source_id}`). `resolve`/`dismiss`: writes AlertHistory with corresponding status (dismiss requires reason). `archive`/`share`/`checklist_start`/`template_save`/`drill_down`: lightweight actions with no DB writes (or stubs for future). All actions logged to `owl_action_log` non-blocking. Terminal state reached -- loop closed.

**Health Check Report Flow.** (1) Ops triggers `POST /owl/health-check`. (2) Alerts fetched from DB (auto-fetch if not provided, limit 50). (3) `compute_heartbeat(alerts)` produces deterministic score 0-100 and band. (4) Load merchant memory + previous findings (best-effort). (5) `assemble_context()` builds 4-window prompt block. (6) `generate_health_report()` sends to LLM with `REPORT_SYSTEM_PROMPT` (timeout 120s). If offline, `_fallback_report()` generates deterministic report. (7) `_post_validate()` patches hallucinated numbers (corrects scores within +/-15 of actual via regex), migrates legacy field names, validates finding trends against delta engine. (8) Persist: `create_owl_session()` (links to previous via `previous_session_id`), `create_owl_findings()` (one per Chirp category with delta direction, plus "resolved" findings for disappeared categories), `update_merchant_memory()` (appends to score_trend capped at 12, updates recurring_categories streaks, flips `is_cold_start` to false). Persistence is non-fatal -- report returns to merchant even if DB write fails.

**The One Thing Flow.** App load or pull-to-refresh triggers `POST /owl/one-thing`. If Owl healthy: builds JSON prompt from up to 20 alerts + stats + context, calls `ask_owl()` with jpt_detection lens, parses JSON response (headline/detail/severity/confidence/category), tags `source="owl"`. If offline: falls back to `_fallback_one_thing()` using composite ranking (severity 60%, impact_cents 40% when available) or simple severity+recency sort. Tags `source="fallback"`.

**Delta Engine.** `compute_session_deltas()` compares current alerts (grouped by Chirp category) against previous session's findings. For each category: count decreased = improved, count increased = worsened, same count but severity changed = direction follows severity, not in previous = new, in previous but not current = resolved. Categories firing 3+ consecutive sessions flagged as "recurring" with elevated prompt prominence. Severity comparison uses `{critical: 0, high: 1, medium: 2, low: 3, info: 4}` ranking.
