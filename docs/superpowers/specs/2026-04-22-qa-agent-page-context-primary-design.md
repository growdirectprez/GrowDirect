---
title: QA Agent — Page Context as Primary Grounding
date: 2026-04-22
project: Canary
linear:
  - GRO-517 (QA Agent Tier 1 — Feature 1)
  - Parent GRO-326, predecessor GRO-389
status: Design approved, ready for implementation plan
---

# QA Agent — Page Context as Primary Grounding

## Problem

After GRO-389 unblocked the DB context, a live smoke test revealed a second
defect: the `/ops/qa` chat UI never sends the `[Page: ... | Merchant: <uuid>]`
prefix the sidecar's `_extract_merchant` regex looks for. So every real browser
chat request hits the short-circuit "No merchant context in request" path that
was added in GRO-389 Task B.

The SYSTEM_PROMPT in `canary/services/qa_agent/agent.py` already describes the
context header as if it exists, but nothing in the UI or Flask proxy actually
produces it. The result is a dead-on-arrival user experience: the agent
refuses to answer any question from the browser. The sidecar is reachable
only by hand-crafted curl that includes the prefix.

A secondary problem observed in the GRO-389 closing live trace: even when
merchant context *is* provided (via curl), the agent sometimes hedges about
entities the user is literally looking at — responding to a pasted
transaction UUID with "might be Square's system ID rather than Canary's" when
the Canary canonical UUID principle (CLAUDE.md) is clear that any UUID a user
sees is already a Canary UUID.

## Goal

Make the `/ops/qa` chat UI work end-to-end through the browser, grounded in
what the user was looking at on their previous ops page. Three sub-features,
all shipped together in one branch because they are coupled:

1. **1a. Baseline context wiring.** Every chat message carries
   `[Page: <path> | Merchant: <uuid>]` composed client-side from
   `sessionStorage` + a server-rendered merchant UUID. This makes the browser
   path work at all.

2. **1b. Per-page entity snapshot.** Four entity-detail pages write a small
   sessionStorage blob containing the IDs + titles of entities visible on
   that page. The QA page includes those in the context header so the agent
   can reason from what the user just saw.

3. **1c. Prompt + observability.** `SYSTEM_PROMPT` updated with the canonical
   UUID principle, a "reason from what the user can see first" ordering
   instruction, and a page-to-likely-tool mapping. Add structured logging
   when the dispatch loop ends without a tool call — gives data to decide if
   a guardrail (deferred) is actually needed.

After this ships, a user can navigate from `/chirps` to `/ops/qa`, ask "tell
me about the top alert", and the agent answers using the specific alert ID
that was on the screen, via the right tool, without hedging.

## Scope

**In scope:**

- Shared Jinja include (`templates/ops/_context_snapshot.html`) that writes
  `sessionStorage.opsContext = {path, snapshot, ts}` on every ops-page render.
- Four entity-page snapshot adapters: `/chirps`, `/alert/<uuid>`,
  `/fox/cases/<uuid>`, `/txn/<uuid>` each emit a `window.OPS_CONTEXT_ENTITIES`
  JSON blob for the include to serialize.
- QA page (`templates/ops/qa.html`) reads `sessionStorage.opsContext` at load
  and composes a `[Page: ... | Merchant: ... | Visible: {...}]` prefix per
  user turn.
- Server-side merchant UUID injection: the QA page template receives the
  internal merchant UUID (resolved via existing `_resolve_merchant` helper)
  as `window.OPS_MERCHANT_ID`. Not from sessionStorage — cannot be spoofed.
- `SYSTEM_PROMPT` update in `canary/services/qa_agent/agent.py`: canonical
  UUID principle, reasoning order, page→tool mapping.
- Structured `logger.info("qa_agent.no_tool_call", extra={...})` in
  `handle_chat` when the dispatch loop completes without tool dispatch.
- Integration + smoke tests covering the full browser-to-sidecar path.

**Explicitly out of scope (YAGNI — deferred):**

- Embedded/slideout chat widget on every ops page (architectural rework —
  separate design cycle)
- Explicit context selector UI (not needed if "last page" is accurate enough)
- `/owl/search` and `/dashboard` snapshots (different shape, lower entity
  density — separate iteration)
- Sidecar corrective re-prompt (Option B from brainstorm) — logging only
- Feature 2 (Linear bug filing from chat) and Feature 3 (Atlas inline
  rendering) — separate spec bundle
- Cross-tab session state (sessionStorage is per-tab by design; documented
  behaviour)

## Architecture

```
┌──────────────────┐
│ /chirps page     │
│                  │──renders──► {% include "ops/_context_snapshot.html" %}
│ inline script    │              ↓
│ window.OPS_      │              sessionStorage.opsContext =
│   CONTEXT_       │                {path: "/chirps",
│   ENTITIES = {…} │                 snapshot: {...},
└──────────────────┘                 ts: 1738300000000}
                                     │
         (user clicks "QA" in nav)   │
                                     ▼
┌────────────────────────────────────────────────────┐
│ /ops/qa                                             │
│   Flask view sets g.merchant_id internal UUID       │
│   ↓                                                 │
│   qa.html renders with                              │
│     <script>window.OPS_MERCHANT_ID="..."</script>   │
│   ↓                                                 │
│   sendMessage() composes header from:               │
│     - window.OPS_MERCHANT_ID (server-side trust)    │
│     - sessionStorage.opsContext (staleness check)   │
│     - user text                                     │
│   ↓                                                 │
│   "[Page: /chirps | Merchant: <uuid>                │
│     | Visible: {alerts:[{id,title,...},…]}]        │
│                                                     │
│    <user text>"                                     │
└────────────────────────────────────────────────────┘
         │
         ▼ POST /ops/qa/chat
┌────────────────────────────────────────────────────┐
│ Flask proxy (ops_console.py) — unchanged            │
└────────────────────────────────────────────────────┘
         │
         ▼ POST qa-agent:8002/chat
┌────────────────────────────────────────────────────┐
│ sidecar server.py handle_chat                       │
│   _extract_merchant → parses Merchant UUID          │
│   set_merchant_context → ContextVar bound           │
│   Anthropic dispatch (SYSTEM_PROMPT updated)        │
│   Tool call with visible entity IDs as input        │
│   If no tool call: log structured event             │
└────────────────────────────────────────────────────┘
```

## Component 1 — Shared snapshot include (Jinja)

**File:** `templates/ops/_context_snapshot.html` (new)

A tiny Jinja partial included in `templates/ops/base_ops.html` (or the
specific entity pages — see Component 2 trade-off). The include emits one
`<script>` block that:

1. Reads an optional `window.OPS_CONTEXT_ENTITIES` JS object (set by the
   page's own inline script, if it's an entity page).
2. Writes `sessionStorage.opsContext` with `{path: window.location.pathname,
   snapshot: window.OPS_CONTEXT_ENTITIES || null, ts: Date.now()}`.
3. Runs once on page load; no navigation-unload hooks needed because every
   new page render refreshes the value.

```html
{# templates/ops/_context_snapshot.html
   GRO-517: writes sessionStorage.opsContext on every ops page render so the
   QA Agent chat UI can ground the agent in what the user just saw.
   Entity-specific pages set window.OPS_CONTEXT_ENTITIES before this runs. #}
<script nonce="{{ csp_nonce() }}">
  (function() {
    try {
      var snapshot = (typeof window.OPS_CONTEXT_ENTITIES === 'object')
        ? window.OPS_CONTEXT_ENTITIES : null;
      sessionStorage.setItem('opsContext', JSON.stringify({
        path: window.location.pathname,
        snapshot: snapshot,
        ts: Date.now()
      }));
    } catch (e) {
      // sessionStorage can throw in private mode / disabled storage —
      // silent fail is fine; QA chat will just lack "Visible" context.
    }
  })();
</script>
```

**Placement decision.** Include it once in `templates/ops/base_ops.html` at
the end of the body (or equivalent block) so it fires for every ops page,
not just the 4 entity pages. Non-entity pages simply write `snapshot: null`,
which is valid. Pages that want to contribute entity data set
`window.OPS_CONTEXT_ENTITIES` before the include runs.

## Component 2 — Per-page entity adapters

Each of the 4 entity pages adds a small `<script>` block near the top of
content (runs before the shared include at end of body) that sets
`window.OPS_CONTEXT_ENTITIES` to a JSON-serializable object.

The snapshots store entity IDs + a minimal set of display fields. No deep
joins, no role-protected fields. All data is already rendered into the page
by the backend, so this is pure DOM/template extraction.

### `/chirps` (alerts list)

**Template:** whichever template renders the chirps listing (verify during
implementation; likely `templates/app/chirps.html` or similar under the
existing `/chirps` blueprint).

Emit the top 5 visible alerts:

```jinja
<script nonce="{{ csp_nonce() }}">
  window.OPS_CONTEXT_ENTITIES = {
    type: "alerts_list",
    alerts: [
      {% for alert in alerts[:5] %}
      {
        id: "{{ alert.id }}",
        title: {{ alert.title | tojson }},
        rule_id: "{{ alert.rule_id }}",
        severity: "{{ alert.severity }}",
        status: "{{ alert.status }}"
      }{{ "," if not loop.last }}
      {% endfor %}
    ]
  };
</script>
```

### `/alert/<uuid>` (alert detail)

```jinja
<script nonce="{{ csp_nonce() }}">
  window.OPS_CONTEXT_ENTITIES = {
    type: "alert_detail",
    alert: {
      id: "{{ alert.id }}",
      title: {{ alert.title | tojson }},
      rule_id: "{{ alert.rule_id }}",
      severity: "{{ alert.severity }}",
      status: "{{ alert.status }}",
      linked_transaction_id: {{ (alert.transaction_id or None) | tojson }},
      triggered_at: "{{ alert.triggered_at.isoformat() if alert.triggered_at else '' }}"
    }
  };
</script>
```

### `/fox/cases/<uuid>` (case detail)

```jinja
<script nonce="{{ csp_nonce() }}">
  window.OPS_CONTEXT_ENTITIES = {
    type: "case_detail",
    case: {
      id: "{{ case.id }}",
      title: {{ case.title | tojson }},
      status: "{{ case.status }}",
      linked_alert_ids: {{ case.linked_alert_ids | tojson }},
      linked_transaction_ids: {{ case.linked_transaction_ids | tojson }}
    }
  };
</script>
```

### `/txn/<uuid>` (transaction detail)

```jinja
<script nonce="{{ csp_nonce() }}">
  window.OPS_CONTEXT_ENTITIES = {
    type: "transaction_detail",
    transaction: {
      id: "{{ txn.id }}",
      external_id: "{{ txn.external_id }}",
      amount_cents: {{ txn.amount_cents }},
      transaction_date: "{{ txn.transaction_date.isoformat() if txn.transaction_date else '' }}",
      transaction_type: "{{ txn.transaction_type }}",
      linked_alert_ids: {{ txn.linked_alert_ids | tojson }}
    }
  };
</script>
```

**Template paths (confirmed during spec review):**

- `/chirps` → `templates/app/chirps.html`
- `/alert/<uuid>` → `templates/app/alert_detail.html`
- `/fox/cases/<uuid>` → `templates/app/case_detail.html` (route prefix `/fox/cases`, template name `case_detail.html`)
- `/txn/<uuid>` → `templates/app/txn_detail.html`

The implementer verifies the exact template filenames and locates the
existing Jinja variables (`alert.id`, `case.title`, etc.) before adding the
entity-snapshot script block. If a linked-ID collection isn't already in
the template scope, the corresponding view function is extended to compute
it; any such backend change is captured in the implementation plan.

**Linked-ID truncation.** `linked_alert_ids` and `linked_transaction_ids`
arrays are capped at 20 items. If the case/txn has more, the snapshot
object includes `linked_alert_ids_truncated: true` (or equivalent). Keeps
the header size bounded and prevents Anthropic token waste on an edge case.

## Component 3 — QA page consumption

**File:** `templates/ops/qa.html`

Two changes:

### 3a. Inject server-side merchant UUID

Inside the `{% block content %}` or `{% block scripts_extra %}`, add:

```jinja
<script nonce="{{ csp_nonce() }}">
  window.OPS_MERCHANT_ID = {{ merchant_internal_uuid | tojson }};
</script>
```

The Flask view `qa_agent_page` in `canary/blueprints/ops_console.py` is
updated to pass the merchant UUID to the template. `g.merchant_id` is
already the internal UUID at this point — `canary/middleware/jwt_auth.py`
resolves it at the auth boundary via `_resolve_merchant_uuid`, so no
additional lookup is needed in the view:

```python
@ops_console_bp.route("/qa")
def qa_agent_page():
    merchant_internal_uuid = getattr(g, "merchant_id", None)
    return render_template(
        "ops/qa.html",
        merchant_internal_uuid=str(merchant_internal_uuid) if merchant_internal_uuid else None,
    )
```

(The existing `_resolve_merchant` helper in `views_wired.py` is defensively
idempotent — it accepts both Square IDs and internal UUIDs — but calling it
here would imply a resolution step that doesn't actually happen in the
modern auth flow. Skip it.)

### 3b. Compose the context header in `sendMessage()`

Replace the current `conversationHistory.push({role:'user', content: text})`
block with context-prefixed composition:

```javascript
function buildContextHeader(userText) {
  var merchant = window.OPS_MERCHANT_ID || null;
  var ctx = null;
  try {
    var raw = sessionStorage.getItem('opsContext');
    if (raw) ctx = JSON.parse(raw);
  } catch (e) { /* ignore */ }

  var parts = [];
  // Page: default to /ops/qa if no prior context
  parts.push('Page: ' + ((ctx && ctx.path) || '/ops/qa'));
  if (merchant) parts.push('Merchant: ' + merchant);

  // Staleness: skip snapshot if older than 30 minutes
  var STALE_MS = 30 * 60 * 1000;
  if (ctx && ctx.snapshot && ctx.ts && (Date.now() - ctx.ts) < STALE_MS) {
    parts.push('Visible: ' + JSON.stringify(ctx.snapshot));
  }

  var header = '[' + parts.join(' | ') + ']';
  return header + '\n\n' + userText;
}

function sendMessage() {
  var text = inputEl.value.trim();
  if (!text) return;
  // ... existing clear + UI-update code ...
  var composed = buildContextHeader(text);
  addMessage('user', escapeHtml(text));  // show the raw text in the UI
  conversationHistory.push({ role: 'user', content: composed });
  // ... existing fetch code ...
}
```

**Note on what the user sees.** The chat bubble in the UI shows the raw user
text. Only the payload sent to the server has the prefix. Keeps the UX
clean.

## Component 4 — SYSTEM_PROMPT updates

**File:** `canary/services/qa_agent/agent.py`

Revised `SYSTEM_PROMPT` (full replacement):

```python
SYSTEM_PROMPT = """You are the Canary QA Agent — an interactive test assistant for the Canary loss prevention platform.

## Canonical UUID principle (Canary, GRO-237)

Every UUID the user pastes or references is a Canary UUID — `Transaction.id`, `Alert.id`, `FoxCase.id`, or a merchant id. Never hedge that a UUID "might be Square's system ID rather than Canary's" — our UUID is always the primary identifier. Square's `external_id` is for source reconciliation only; the user never sees it.

## Reasoning order — ground in what the user can see first

Every user message starts with a context header:
`[Page: <path> | Merchant: <uuid> | Visible: <json>]`

Always reason from this header before answering:

1. What page is the user on? Parse `Page: <path>`.
2. What entities are visible? Parse `Visible: ...`. On `/chirps` you'll see up to 5 recent alerts; on `/alert/<uuid>` you'll see one alert with its linked transaction; on `/fox/cases/<uuid>` you'll see one case with linked alerts and transactions; on `/txn/<uuid>` you'll see one transaction with linked alerts.
3. Map the user's question to the right tool. If they paste a UUID, look it up first. If they ask "this alert" / "this case" / "this transaction", operate on the one in `Visible`.
4. Only then synthesize. Don't guess what an ID could be — run a tool.

## Page → likely-tool mapping

- `/chirps` — alerts list. Use `list_alerts` / `rank_alerts` for listing, `get_alert` for a specific ID.
- `/alert/<uuid>` — single alert. Use `get_alert`, `lifecycle_summary`, `get_timeline`. If the user asks about "the transaction", operate on `alert.linked_transaction_id`.
- `/fox/cases/<uuid>` — single case. Use `get_case`, `get_timeline`, `verify_chain`. If they ask "the alerts" or "the transactions", operate on the linked IDs.
- `/txn/<uuid>` — single transaction. Use search or `get_alert` against `linked_alert_ids` to find associated alerts.
- `/ops/qa` (no referrer) — the user came to chat without prior context. Ask what they want to do, or run `list_scenarios` if they seem to want to test the pipeline.

## Available tool categories (all prefixed with mcp__canary__):

- Atlas: atlas_figure, atlas_search, atlas_validate, atlas_index
- Alerts: list_alerts, get_alert, lifecycle_summary, rank_alerts
- Analytics: get_dashboard, get_trends, get_top_risks, score_metrics
- Chirp: get_rules, get_rule, get_config_summary, validate_thresholds
- Fox: list_cases, get_case, get_timeline, verify_chain
- Identity: get_merchant, list_employees, list_locations
- Owl: search, ask, knowledge_search, score_payment
- TSP: get_stream_health, get_ingestion_stats, get_dead_letters
- Scenarios: fire_scenario, poll_scenario, list_scenarios, get_thresholds

## Response style

- Prefer tool calls over explanations. "I don't know what this ID is" is not an acceptable first response — run a tool.
- Chain tools when needed.
- Keep responses concise — 2-3 paragraphs max.
- If a tool fails, say what failed and suggest an alternative.
- Include clickable links to Canary app pages when referencing entities:
  - Alerts: `[Alert title](/alert/<uuid>)` or `[View alerts](/chirps)`
  - Cases: `[Case title](/fox/cases/<uuid>)`
  - Transactions: `[Transaction](/txn/<uuid>)`
  - Search: `[Search results](/owl/search?q=<query>)`
- Don't repeat the context header back to the user — just use it silently.

Environment: Square Sandbox — no real merchant data at risk.
"""
```

## Component 5 — Dispatch-loop observability

**File:** `canary/services/qa_agent/server.py`

Inside `handle_chat`, at the point where `text_parts` is finalized (right
before the return), add one structured log line if `all_tool_calls` is
empty:

```python
if not all_tool_calls:
    # GRO-517 observability — are we still seeing no-tool-call answers
    # after the context header + prompt update? If this fires often enough
    # to be painful, consider Option B (corrective re-prompt) from the
    # design spec.
    # Redact the header to avoid logging merchant UUIDs at INFO level.
    first_user = next(
        (m.get("content", "") for m in messages if m.get("role") == "user"
         and isinstance(m.get("content"), str)),
        ""
    )
    # Strip the context header if present
    if first_user.startswith("["):
        idx = first_user.find("]\n")
        first_user = first_user[idx + 2:] if idx != -1 else first_user
    logger.info(
        "qa_agent.no_tool_call session=%s text=%r",
        session_id, first_user[:200]
    )
```

No behaviour change — just a log line for later analysis.

## Data flow after fix

```
User on /chirps
  → page renders with 10 visible alerts
  → inline <script> sets window.OPS_CONTEXT_ENTITIES = {type:"alerts_list", alerts:[top 5]}
  → shared include writes sessionStorage.opsContext = {path:"/chirps", snapshot:{...}, ts:...}
  → user clicks "QA Agent" nav link
  → navigates to /ops/qa
  → Flask view resolves merchant internal UUID via _resolve_merchant
  → qa.html renders with window.OPS_MERCHANT_ID = "<uuid>"
  → user types "tell me about the top alert"
  → sendMessage reads sessionStorage + window.OPS_MERCHANT_ID
  → composes: "[Page: /chirps | Merchant: <uuid> | Visible: {type:alerts_list, alerts:[...]}]\n\ntell me about the top alert"
  → POST to /ops/qa/chat → Flask proxy → sidecar
  → sidecar _extract_merchant parses merchant → set_merchant_context
  → SYSTEM_PROMPT instructs agent to reason from Visible first
  → agent calls get_alert({alert_id: <first id from Visible>})
  → real DB row returned via the GRO-389 session factory path
  → agent synthesizes "The top alert is ..."
  → ui shows raw user text ("tell me about the top alert"), not the prefix
  → assistant response rendered normally
```

## Testing

All tests under `Canary/tests/`.

### Unit — `tests/unit/test_qa_agent_context_header.py` (new)

Tests the sidecar's existing `_extract_merchant` still works with the new
richer header shape. No JS test; sidecar-side only.

- `test_extract_merchant_with_visible_block` — header contains `Visible: {...}`
  with nested braces; regex still finds the Merchant UUID
- `test_extract_merchant_header_with_tojson_escaped_strings` — `Visible`
  payload includes escaped quotes in titles; regex doesn't break
- `test_extract_merchant_missing_visible` — header is just
  `[Page: /x | Merchant: <uuid>]` (no Visible); still matches
- `test_extract_merchant_position_independent` — regex matches even if
  `Visible: {...}` appears before `Merchant: <uuid>` (future-proofs the
  contract against header-ordering changes)

### Integration — `tests/integration/test_qa_agent_chat_with_context.py` (new, `@pytest.mark.postgres`)

Extends the Tier 0 chat-handler tests with context-header scenarios.

- `test_chat_with_chirps_context_routes_to_alerts_tool` — mock Anthropic so
  the first tool call is `get_alert`, payload has a `[Page: /chirps |
  Merchant: ... | Visible: {alerts:[...]}]` header, assert `get_alert` is
  called with an ID from the visible list
- `test_no_tool_call_logs_structured_event` — mock Anthropic to return a
  plain text response (no tool_use), assert `logger.info` emits
  `qa_agent.no_tool_call` with the session_id and redacted text (no header
  leak)

### Smoke — `tests/smoke/test_qa_page_context_header.py` (new, Playwright)

End-to-end browser test:

- Log in as an admin, navigate to `/chirps`, wait for page load, verify
  `sessionStorage.opsContext.path === '/chirps'` and `.snapshot.alerts` is
  populated
- Click through to `/ops/qa`, verify `window.OPS_MERCHANT_ID` is set
- Send a chat message, inspect the network request to `/ops/qa/chat`,
  assert the `messages[0].content` starts with `[Page: /chirps | Merchant:
  <uuid> | Visible:`

**Pre-flight:** check `tests/smoke/conftest.py` for an existing admin-login
fixture. If one exists (likely — Canary has admin-only routes covered by
smoke tests), reuse it. If not, adding an `admin_logged_in_page` fixture is
part of commit 6; call this out explicitly in the implementation plan so
the extra scope doesn't surprise anyone.

## Completeness gate (end-of-session verification)

Per Canary CLAUDE.md "No Lazy Pipes":

1. **Data in** — log into `/ops/qa` through the browser, navigate to
   `/chirps`, then click QA Agent, send "tell me about the top alert".
   Response calls `get_alert` with a real alert ID and returns a non-error
   answer.
2. **Data out** — the ID in the `tool_calls` matches an ID from the
   `sessionStorage.opsContext.snapshot.alerts` at the moment the chat was
   sent.
3. **Row reads** — sidecar log shows `QA Agent → MCP: get_alert(...)` with
   the right merchant_id and no NoneType errors.
4. **UX check** — the user sees only their original text in the chat
   bubble, not the prefix. The prefix is invisible to the user.

## Linear closeout

- Update GRO-517 description / comment: Feature 1 done, Feature 2 and
  Feature 3 still open on this GRO. Consider splitting them into new issues
  (GRO-518, GRO-519) or keeping under GRO-517 — implementer's call at
  closeout.

## Risks and non-goals

- **sessionStorage is per-tab.** User opens `/chirps` in tab A, `/ops/qa`
  in tab B → tab B has no context. Documented; acceptable for Tier 1.
- **Private browsing / disabled storage.** The include silently
  `try/catch`es. Falls back to `[Page: /ops/qa | Merchant: ...]` with no
  Visible section. Agent handles this gracefully (explicit instruction in
  prompt for "/ops/qa with no referrer" case).
- **Snapshot staleness.** 30-minute TTL. If the user lingers an hour on a
  page and then chats, the snapshot is stale but not misleading — we drop
  it. Header still has Page + Merchant.
- **Merchant UUID is trusted from server.** `window.OPS_MERCHANT_ID` is
  rendered server-side via `_resolve_merchant`, not taken from
  sessionStorage. Client-side mutation cannot impersonate.
- **Prompt update may regress existing flows.** The UUID principle + page
  mapping is new — existing integration tests (`test_qa_agent_chat.py` from
  GRO-389) should still pass because the mocked Anthropic ignores the
  prompt. Real Anthropic behaviour is covered by the smoke test.
- **No guardrail.** If Claude still answers without a tool call despite the
  richer context, the `qa_agent.no_tool_call` log line is our only signal.
  Guardrail is deferred to a future iteration if the log volume warrants.

## Commit strategy

1. `feat(qa-agent): shared ops context snapshot include [GRO-517]` — the
   Jinja include + base_ops.html integration
2. `feat(qa-agent): per-page entity snapshots for chirps/alert/case/txn [GRO-517]`
   — the 4 adapter scripts
3. `feat(qa-agent): QA page reads context + injects merchant [GRO-517]`
   — qa.html + ops_console.py view update
4. `feat(qa-agent): SYSTEM_PROMPT update — UUID principle + reasoning order [GRO-517]`
   — agent.py. Behaviour verified by the smoke test in commit 6; no
   standalone unit test (mocked Anthropic ignores the prompt).
5. `feat(qa-agent): structured log for no-tool-call responses [GRO-517]`
   — server.py
6. `test(qa-agent): context header unit + integration + smoke [GRO-517]`
   — three test files
7. (if needed) `fix(qa-agent): address review findings [GRO-517]`

Each commit is bisectable. Tests land last because most of them require the
header to exist end-to-end. If a future bisect implicates "agent started
hedging about UUIDs again," the suspect is commit 4 — commit 6 tests will
be where the regression surfaces, but the fix belongs in the prompt.
