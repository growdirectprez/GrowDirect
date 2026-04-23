# QA Agent Page-Context Primary Grounding Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the `/ops/qa` chat UI actually usable through the browser by having every chat message carry a `[Page: ... | Merchant: <uuid> | Visible: {...}]` context header composed client-side. Ground the agent in what the user was looking at on the page they came from.

**Architecture:** Shared Jinja snapshot include writes `sessionStorage.opsContext` on every app/ops page render. Four entity-detail templates (`/chirps`, `/alert/<uuid>`, `/fox/cases/<uuid>`, `/txn/<uuid>`) contribute visible-entity hints via `window.OPS_CONTEXT_ENTITIES`. The QA page reads the snapshot at chat time, composes the header with a server-rendered merchant UUID (safe from client tampering), and prepends it to each user turn. Sidecar SYSTEM_PROMPT is rewritten to reason from visible entities first. Structured log line fires when the dispatch loop ends without a tool call.

**Tech Stack:** Jinja2 templates, vanilla JS (sessionStorage API), Flask, Anthropic Python SDK (prompt change only), pytest, pytest-playwright for smoke.

**Spec:** [docs/superpowers/specs/2026-04-22-qa-agent-page-context-primary-design.md](../specs/2026-04-22-qa-agent-page-context-primary-design.md)

**Linear:** GRO-517 (Feature 1); builds on GRO-389 merged at commit `4951dc6`.

---

## File Structure

**Modified:**
- `Canary/templates/app/base_app.html` — include snapshot partial
- `Canary/templates/ops/base_ops.html` — include snapshot partial
- `Canary/templates/app/chirps.html` — emit alerts-list entity snapshot
- `Canary/templates/app/alert_detail.html` — emit alert-detail snapshot
- `Canary/templates/app/case_detail.html` — emit case-detail snapshot
- `Canary/templates/app/txn_detail.html` — emit transaction-detail snapshot
- `Canary/templates/ops/qa.html` — inject merchant UUID + compose header in sendMessage
- `Canary/canary/blueprints/ops_console.py` — `qa_agent_page` passes `merchant_internal_uuid`
- `Canary/canary/services/qa_agent/agent.py` — SYSTEM_PROMPT rewrite
- `Canary/canary/services/qa_agent/server.py` — structured log in handle_chat

**Created:**
- `Canary/templates/ops/_context_snapshot.html` — shared snapshot-write partial
- `Canary/tests/unit/test_qa_agent_context_header.py` — regex compatibility tests
- `Canary/tests/integration/test_qa_agent_chat_with_context.py` — header-routes-tool-call tests
- `Canary/tests/smoke/test_qa_page_context_header.py` — Playwright end-to-end

**Unchanged (confirmed during planning):**
- `Canary/canary/db/session_factory.py` — GRO-389 work, nothing to touch
- The view functions for `/chirps`, `/alert/<uuid>`, `/fox/cases/<uuid>`, `/txn/<uuid>` — existing Jinja variables (`alert.id`, `case.title`, etc.) already in scope; no backend additions unless Task 2 step discovers otherwise

---

## Chunk 1: Snapshot pipeline (client side, browser-facing)

This chunk delivers the end-to-end header wiring: the shared include, the four entity-page adapters, the QA page composition, and the Flask view change to pass the merchant UUID. After this chunk, the browser sends a properly-formed context header and the sidecar receives it. No sidecar changes yet — the existing `_extract_merchant` regex handles the new header shape (verified during spec review pass).

### Task 1.1: Shared snapshot include

**Files:**
- Create: `Canary/templates/ops/_context_snapshot.html`

- [ ] **Step 1: Create the partial**

```html
{#
  templates/ops/_context_snapshot.html

  GRO-517: writes sessionStorage.opsContext on every app/ops page render.
  The QA Agent chat UI reads it to ground the agent in what the user was
  just looking at. Entity-specific pages set window.OPS_CONTEXT_ENTITIES
  before this runs; other pages produce {path, snapshot: null, ts}.
#}
<script nonce="{{ csp_nonce() }}">
  (function() {
    try {
      var snapshot = (typeof window.OPS_CONTEXT_ENTITIES === 'object'
                      && window.OPS_CONTEXT_ENTITIES !== null)
        ? window.OPS_CONTEXT_ENTITIES
        : null;
      sessionStorage.setItem('opsContext', JSON.stringify({
        path: window.location.pathname,
        snapshot: snapshot,
        ts: Date.now()
      }));
    } catch (e) {
      // sessionStorage can throw in private mode / disabled storage.
      // Silent fail is fine — QA chat will just lack "Visible" context.
    }
  })();
</script>
```

- [ ] **Step 2: Commit**

```bash
cd ~/GrowDirect/Canary
git add templates/ops/_context_snapshot.html
git commit -m "feat(qa-agent): shared ops context snapshot partial [GRO-517]

Writes sessionStorage.opsContext on every app/ops page render so the
QA Agent chat UI can ground the agent in what the user just saw.
Entity pages contribute via window.OPS_CONTEXT_ENTITIES before the
partial runs. Silent fail on private-mode sessionStorage errors."
```

---

### Task 1.2: Wire the include into both base templates

**Files:**
- Modify: `Canary/templates/app/base_app.html`
- Modify: `Canary/templates/ops/base_ops.html`

- [ ] **Step 1: Read both base templates to find the insertion point**

Use the Read tool on both files. Look for the `{% block scripts_extra %}` block (confirmed present at the bottom of `base_ops.html`). Insert the include IMMEDIATELY AFTER `{% block scripts_extra %}{% endblock %}` but still inside `</body>`. In `base_app.html`, find the equivalent block.

If a page does not define `window.OPS_CONTEXT_ENTITIES` before the partial fires, the partial writes `snapshot: null` — that's intentional.

- [ ] **Step 2: Add include to `base_ops.html`**

Insert the line immediately before `</body>`, after the existing `{% block scripts_extra %}{% endblock %}`:

```jinja
{% include "ops/_context_snapshot.html" %}
```

- [ ] **Step 3: Add include to `base_app.html`**

Find the equivalent location (end of body, after whatever scripts_extra-style block exists). Add the same line.

- [ ] **Step 4: Smoke-verify both pages render without JS errors**

```bash
cd ~/GrowDirect/Canary/devops
docker compose -f docker-compose.localhost.yml up -d flask
# Hit a known page and view-source to confirm the snapshot script is present
curl -s http://localhost:5001/chirps | grep -c "opsContext" 2>&1
# Expected: at least 1 (the script is in the rendered page)
```

If the curl returns 0, the include didn't land or the template inheritance isn't finding it — re-check the location of `{% include %}` in base_app.html.

- [ ] **Step 5: Commit**

```bash
cd ~/GrowDirect/Canary
git add templates/app/base_app.html templates/ops/base_ops.html
git commit -m "feat(qa-agent): include ops context snapshot in app+ops bases [GRO-517]

Every page rendered under base_app.html or base_ops.html now writes
sessionStorage.opsContext on load. Entity pages will contribute visible
entity hints via window.OPS_CONTEXT_ENTITIES in subsequent commits."
```

---

### Task 1.3: Entity snapshot — `/chirps`

**Files:**
- Modify: `Canary/templates/app/chirps.html`

- [ ] **Step 1: Read the template**

Use Read on `templates/app/chirps.html`. Identify:
- Whether `alerts` (plural) is the Jinja variable name for the list
- What fields are available on each alert (look for `alert.id`, `alert.title`, `alert.rule_id`, `alert.severity`, `alert.status` in the existing template markup)
- Where to insert the snapshot `<script>` — before `{% block scripts_extra %}` end, or at the top of `{% block content %}` — either works; pick whichever is earlier in the page body so the global var is set before the base template's snapshot-write runs.

If any of the 5 fields isn't available in the template scope (e.g., `status` is not exposed), EITHER drop it from the snapshot shape OR update the view function to pass it. Prefer dropping — the snapshot is best-effort, not a contract for downstream data fidelity.

- [ ] **Step 2: Add the snapshot script**

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

Insert at the top of `{% block content %}` (or equivalent).

- [ ] **Step 3: Verify the snapshot shape at runtime**

With the flask container running:
```bash
curl -s http://localhost:5001/chirps -b "$(get-admin-cookie)" | grep -A 20 "OPS_CONTEXT_ENTITIES"
```
If you don't have `get-admin-cookie`, open `/chirps` in the browser (logged in), open DevTools console, run:
```javascript
JSON.parse(sessionStorage.getItem('opsContext'))
```
Expected: `{path: "/chirps", snapshot: {type: "alerts_list", alerts: [...]}, ts: <number>}` with up to 5 alerts.

If the Jinja loop produces `SyntaxError` in JS (usually from an unescaped quote in a title), the `| tojson` filter should handle it — but if not, wrap the whole `window.OPS_CONTEXT_ENTITIES = {...};` assignment in a `try/catch` that falls back to `null`.

- [ ] **Step 4: Commit**

```bash
cd ~/GrowDirect/Canary
git add templates/app/chirps.html
git commit -m "feat(qa-agent): /chirps entity snapshot [GRO-517]

Top 5 visible alerts emitted via window.OPS_CONTEXT_ENTITIES for the
shared snapshot include. Agent can now reason about the alerts the
user just saw when chatting at /ops/qa."
```

---

### Task 1.4: Entity snapshot — `/alert/<uuid>`

**Files:**
- Modify: `Canary/templates/app/alert_detail.html`

- [ ] **Step 1: Read the template**

Identify the Jinja variable for the single alert (probably `alert`) and verify these fields are in scope: `id`, `title`, `rule_id`, `severity`, `status`, `transaction_id` (or `alert.transaction.id` — depends on model), `triggered_at`.

- [ ] **Step 2: Add the snapshot script**

At the top of `{% block content %}`:

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

If the model exposes `linked_transaction_id` under a different attribute name (e.g., nested `alert.transaction.id`), adapt accordingly. If absent, emit `linked_transaction_id: null`.

- [ ] **Step 3: Verify runtime**

Open `/alert/<any-visible-alert-uuid>` in browser, DevTools console:
```javascript
JSON.parse(sessionStorage.getItem('opsContext'))
```
Expected: `{path: "/alert/...", snapshot: {type: "alert_detail", alert: {id, title, ...}}, ts: ...}`

- [ ] **Step 4: Commit**

```bash
cd ~/GrowDirect/Canary
git add templates/app/alert_detail.html
git commit -m "feat(qa-agent): /alert/<uuid> entity snapshot [GRO-517]"
```

---

### Task 1.5: Entity snapshot — `/fox/cases/<uuid>`

**Files:**
- Modify: `Canary/templates/app/case_detail.html`

- [ ] **Step 1: Read the template and identify linked-ID collections**

The spec emits `linked_alert_ids` and `linked_transaction_ids`, both capped at 20. Check whether these are already in the Jinja scope (`case.linked_alert_ids`, `case.alerts`, `case.alert_ids`, etc.). If not, note what IS in scope (e.g., `case.alerts` might be a list of Alert objects rather than IDs) and either:

a. Derive the IDs inline with a Jinja list-comprehension: `[{% for a in case.alerts[:20] %}"{{ a.id }}"{{ "," if not loop.last }}{% endfor %}]`
b. Update the view in `canary/blueprints/views_wired.py` to pass `linked_alert_ids=[str(a.id) for a in case.alerts[:20]]` to the template. Only do this if option (a) produces messy Jinja.

Cap at 20; include `linked_alert_ids_truncated: true` when the full list was longer (see spec).

- [ ] **Step 2: Add the snapshot script**

Rough shape (adapt to whatever's in scope):

```jinja
<script nonce="{{ csp_nonce() }}">
  (function() {
    var allAlertIds = [{% for a in case.alerts %}"{{ a.id }}"{{ "," if not loop.last }}{% endfor %}];
    var allTxnIds = [{% for t in case.transactions %}"{{ t.id }}"{{ "," if not loop.last }}{% endfor %}];
    window.OPS_CONTEXT_ENTITIES = {
      type: "case_detail",
      case: {
        id: "{{ case.id }}",
        title: {{ case.title | tojson }},
        status: "{{ case.status }}",
        linked_alert_ids: allAlertIds.slice(0, 20),
        linked_alert_ids_truncated: allAlertIds.length > 20,
        linked_transaction_ids: allTxnIds.slice(0, 20),
        linked_transaction_ids_truncated: allTxnIds.length > 20
      }
    };
  })();
</script>
```

Wrap in an IIFE so the truncation logic doesn't leak vars into the global scope.

- [ ] **Step 3: Verify runtime**

Open `/fox/cases/<any-case-uuid>` in browser, DevTools:
```javascript
JSON.parse(sessionStorage.getItem('opsContext'))
```
Expected: snapshot has `case.id`, `case.title`, capped linked arrays.

- [ ] **Step 4: Commit**

```bash
cd ~/GrowDirect/Canary
git add templates/app/case_detail.html
# If view update needed:
# git add canary/blueprints/views_wired.py
git commit -m "feat(qa-agent): /fox/cases/<uuid> entity snapshot [GRO-517]"
```

---

### Task 1.6: Entity snapshot — `/txn/<uuid>`

**Files:**
- Modify: `Canary/templates/app/txn_detail.html`

- [ ] **Step 1: Read the template**

Check for `txn` or `transaction` as the Jinja variable. Verify `id`, `external_id`, `amount_cents`, `transaction_date`, `transaction_type` are accessible. `linked_alert_ids` is the derived list — may require the same inline derivation or view change as Task 1.5.

- [ ] **Step 2: Add the snapshot script**

```jinja
<script nonce="{{ csp_nonce() }}">
  (function() {
    var allAlertIds = [{% for a in txn.alerts %}"{{ a.id }}"{{ "," if not loop.last }}{% endfor %}];
    window.OPS_CONTEXT_ENTITIES = {
      type: "transaction_detail",
      transaction: {
        id: "{{ txn.id }}",
        external_id: "{{ txn.external_id }}",
        amount_cents: {{ txn.amount_cents }},
        transaction_date: "{{ txn.transaction_date.isoformat() if txn.transaction_date else '' }}",
        transaction_type: "{{ txn.transaction_type }}",
        linked_alert_ids: allAlertIds.slice(0, 20),
        linked_alert_ids_truncated: allAlertIds.length > 20
      }
    };
  })();
</script>
```

- [ ] **Step 3: Verify runtime**

DevTools: `JSON.parse(sessionStorage.getItem('opsContext'))` — check the shape.

- [ ] **Step 4: Commit**

```bash
cd ~/GrowDirect/Canary
git add templates/app/txn_detail.html
git commit -m "feat(qa-agent): /txn/<uuid> entity snapshot [GRO-517]"
```

---

### Task 1.7: QA page consumption — `qa.html` + Flask view

**Files:**
- Modify: `Canary/templates/ops/qa.html`
- Modify: `Canary/canary/blueprints/ops_console.py`

- [ ] **Step 1: Update the Flask view**

In `ops_console.py`, find `qa_agent_page` (around line 176):

```python
@ops_console_bp.route("/qa")
def qa_agent_page():
    """QA Agent — Claude-powered interactive test assistant."""
    return render_template("ops/qa.html")
```

Replace with:

```python
@ops_console_bp.route("/qa")
def qa_agent_page():
    """QA Agent — Claude-powered interactive test assistant.

    Passes the current merchant's internal UUID to the template as
    `merchant_internal_uuid` so the chat client can embed it in the
    [Page | Merchant] header sent to the sidecar. g.merchant_id is
    already resolved to the internal UUID by the auth middleware
    (canary/middleware/jwt_auth.py), so no lookup needed here.
    """
    merchant_internal_uuid = getattr(g, "merchant_id", None)
    return render_template(
        "ops/qa.html",
        merchant_internal_uuid=str(merchant_internal_uuid) if merchant_internal_uuid else None,
    )
```

Make sure `g` is imported in the file (`from flask import g`); it already should be.

- [ ] **Step 2: Inject `window.OPS_MERCHANT_ID` in `qa.html`**

At the top of `{% block scripts_extra %}` in `templates/ops/qa.html`, BEFORE the existing `mermaid.initialize(...)` line (around line 261), add:

```jinja
<script nonce="{{ csp_nonce() }}">
  window.OPS_MERCHANT_ID = {{ merchant_internal_uuid | tojson }};
</script>
```

- [ ] **Step 3: Add `buildContextHeader` helper and modify `sendMessage`**

In the existing `<script>` block in `qa.html`, ADD a new helper function immediately before `function sendMessage()`:

```javascript
function buildContextHeader(userText) {
  var merchant = window.OPS_MERCHANT_ID || null;
  var ctx = null;
  try {
    var raw = sessionStorage.getItem('opsContext');
    if (raw) ctx = JSON.parse(raw);
  } catch (e) { /* ignore */ }

  var parts = [];
  parts.push('Page: ' + ((ctx && ctx.path) || '/ops/qa'));
  if (merchant) parts.push('Merchant: ' + merchant);

  // 30-minute staleness window
  var STALE_MS = 30 * 60 * 1000;
  if (ctx && ctx.snapshot && ctx.ts && (Date.now() - ctx.ts) < STALE_MS) {
    parts.push('Visible: ' + JSON.stringify(ctx.snapshot));
  }

  return '[' + parts.join(' | ') + ']\n\n' + userText;
}
```

Then MODIFY `function sendMessage()` — find the line `conversationHistory.push({ role: 'user', content: text });` and change it to:

```javascript
conversationHistory.push({ role: 'user', content: buildContextHeader(text) });
```

IMPORTANT: do NOT change the `addMessage('user', escapeHtml(text))` line immediately above it — the UI displays the raw user text, not the prefix.

- [ ] **Step 4: Reload and smoke-test**

```bash
cd ~/GrowDirect/Canary/devops
docker compose -f docker-compose.localhost.yml restart flask
```

Open `/chirps` in browser, wait for load, click through to `/ops/qa`. Open DevTools Network tab. Type "test" and send. Inspect the POST to `/ops/qa/chat`. The `messages[0].content` should look like:
```
[Page: /chirps | Merchant: <uuid> | Visible: {"type":"alerts_list","alerts":[...]}]

test
```

The chat bubble in the UI should show just "test".

- [ ] **Step 5: Verify the sidecar responds without the short-circuit error**

The response from `/ops/qa/chat` should NOT be `"No merchant context in request..."`. It should be a real agent response (possibly invoking a tool). If you get the short-circuit text, inspect the request body — the regex may not be matching. Most common cause: `window.OPS_MERCHANT_ID` is `null` because `g.merchant_id` wasn't set in the view (auth middleware config issue outside this scope).

- [ ] **Step 6: Commit**

```bash
cd ~/GrowDirect/Canary
git add templates/ops/qa.html canary/blueprints/ops_console.py
git commit -m "feat(qa-agent): QA page composes context header per turn [GRO-517]

qa_agent_page view now passes merchant_internal_uuid from g.merchant_id
(already resolved by auth middleware — no lookup needed). qa.html reads
sessionStorage.opsContext + window.OPS_MERCHANT_ID and composes a
[Page: ... | Merchant: ... | Visible: ...] header for each user turn.
UI shows only the raw user text; the prefix is invisible to the user.

Fixes the dead-on-arrival UX from GRO-389 where the sidecar short-
circuited every browser request for lack of a Merchant prefix."
```

---

## Chunk 2: Sidecar prompt + observability + tests

This chunk delivers the agent-side behaviour change (prompt rewrite + no-tool-call log) and the full test coverage. After this chunk, the pipeline is not just wired but also exercised end-to-end in tests and carries observability for future iteration.

### Task 2.1: SYSTEM_PROMPT update

**Files:**
- Modify: `Canary/canary/services/qa_agent/agent.py`

- [ ] **Step 1: Read the current SYSTEM_PROMPT**

In `canary/services/qa_agent/agent.py`, find the `SYSTEM_PROMPT = """..."""` assignment (starts around line 19 per the spec). Read the full current value.

- [ ] **Step 2: Replace the SYSTEM_PROMPT wholesale**

Replace the entire `SYSTEM_PROMPT = """..."""` block with:

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

Verify the file still parses:
```bash
cd ~/GrowDirect/Canary
python3 -c "from canary.services.qa_agent.agent import SYSTEM_PROMPT; print(len(SYSTEM_PROMPT))"
# Expected: some large positive integer (no SyntaxError)
```

- [ ] **Step 3: Commit**

```bash
cd ~/GrowDirect/Canary
git add canary/services/qa_agent/agent.py
git commit -m "feat(qa-agent): SYSTEM_PROMPT — UUID principle + reasoning order [GRO-517]

Rewrites the system prompt to:
- bake in the canonical UUID principle (CLAUDE.md, GRO-237) — any UUID
  the user sees is a Canary UUID, no hedging about Square IDs
- instruct reasoning order: parse Page, parse Visible, run a tool before
  answering
- give page-to-likely-tool mapping for the 4 entity pages

Behaviour verified by the smoke test added in commit Task 2.4.
No standalone unit test — mocked Anthropic ignores the prompt.
If a future bisect implicates 'agent hedging about UUIDs' or 'agent
answered without calling a tool', suspect this commit."
```

---

### Task 2.2: Structured no-tool-call log

**Files:**
- Modify: `Canary/canary/services/qa_agent/server.py`

- [ ] **Step 1: Read the current `handle_chat` return path**

Find the block that returns the final response (around lines 195-206 per the GRO-389 landed state). Locate where `text_parts` is finalized and `all_tool_calls` is known.

- [ ] **Step 2: Insert the structured log**

IMMEDIATELY BEFORE the final `return {...}` inside the `try` block (after rate-limit updates, inside the try), add:

```python
        if not all_tool_calls:
            # GRO-517 observability — no-tool-call responses are the pattern
            # the SYSTEM_PROMPT rewrite is trying to eliminate. Log them for
            # later analysis to decide whether a corrective re-prompt
            # guardrail is warranted. Strip the context header from the
            # first user message so merchant UUIDs don't leak at INFO level.
            first_user = next(
                (m.get("content", "") for m in messages
                 if m.get("role") == "user" and isinstance(m.get("content"), str)),
                ""
            )
            if first_user.startswith("["):
                idx = first_user.find("]\n")
                first_user = first_user[idx + 2:] if idx != -1 else first_user
            logger.info(
                "qa_agent.no_tool_call session=%s text=%r",
                session_id, first_user[:200]
            )
```

- [ ] **Step 3: Verify module imports**

```bash
cd ~/GrowDirect/Canary
python3 -c "from canary.services.qa_agent.server import handle_chat, app; print('ok')"
```
Expected: `ok`.

- [ ] **Step 4: Commit**

```bash
cd ~/GrowDirect/Canary
git add canary/services/qa_agent/server.py
git commit -m "feat(qa-agent): structured log for no-tool-call responses [GRO-517]

Logs qa_agent.no_tool_call at INFO level when the dispatch loop ends
without invoking any tool. Context header stripped from the logged
text so merchant UUIDs don't land in INFO-level logs. Gives us data
to decide whether a corrective re-prompt guardrail is needed — not
adding one speculatively."
```

---

### Task 2.3: Unit tests — header regex compatibility

**Files:**
- Create: `Canary/tests/unit/test_qa_agent_context_header.py`

- [ ] **Step 1: Create the test file**

```python
"""Unit tests: _extract_merchant regex handles the new context header shape.

GRO-517: the header added to chat messages from the browser goes from
`[Page: X | Merchant: <uuid>]` (Tier 0 crudely described) to
`[Page: X | Merchant: <uuid> | Visible: {...}]`. This file proves the
existing regex in canary/services/qa_agent/server.py still finds the
Merchant UUID under the new layout, including edge cases (nested JSON
braces, embedded quotes, ordering changes).
"""

from __future__ import annotations

from canary.services.qa_agent.server import _extract_merchant


MERCHANT_UUID = "12345678-1234-1234-1234-1234567890ab"


def test_extract_merchant_with_visible_block():
    """Visible JSON object with nested braces shouldn't confuse the regex."""
    header = (
        f"[Page: /chirps | Merchant: {MERCHANT_UUID} | "
        'Visible: {"type":"alerts_list","alerts":[{"id":"a","title":"x"}]}]'
    )
    msgs = [{"role": "user", "content": header + "\n\nhi"}]
    assert _extract_merchant(msgs) == MERCHANT_UUID


def test_extract_merchant_header_with_tojson_escaped_strings():
    """Escaped quotes in Visible.alerts[].title shouldn't break extraction."""
    header = (
        f"[Page: /alert/abc | Merchant: {MERCHANT_UUID} | "
        'Visible: {"type":"alert_detail","alert":{"title":"he said \\"hi\\""}}]'
    )
    msgs = [{"role": "user", "content": header + "\n\nok"}]
    assert _extract_merchant(msgs) == MERCHANT_UUID


def test_extract_merchant_missing_visible():
    """Header without Visible still matches — this is the fallback shape
    when sessionStorage is stale or unavailable."""
    header = f"[Page: /ops/qa | Merchant: {MERCHANT_UUID}]"
    msgs = [{"role": "user", "content": header + "\n\nhello"}]
    assert _extract_merchant(msgs) == MERCHANT_UUID


def test_extract_merchant_position_independent():
    """Future-proof: regex should match even if Visible precedes Merchant.
    Current client emits Merchant before Visible, but changing that
    shouldn't regress extraction."""
    header = (
        f"[Visible: {{}} | Page: /chirps | Merchant: {MERCHANT_UUID}]"
    )
    msgs = [{"role": "user", "content": header + "\n\nquery"}]
    assert _extract_merchant(msgs) == MERCHANT_UUID
```

- [ ] **Step 2: Run the tests**

```bash
cd ~/GrowDirect/Canary
python3 -m pytest tests/unit/test_qa_agent_context_header.py -v
```

Expected: 4 passed.

If any test fails with "merchant not extracted", the regex in `server.py` may be anchored differently than expected — inspect and either adjust the regex (minor) or adjust the test (if the test's implicit assumption was wrong).

- [ ] **Step 3: Commit**

```bash
cd ~/GrowDirect/Canary
git add tests/unit/test_qa_agent_context_header.py
git commit -m "test(qa-agent): unit tests — context header regex compatibility [GRO-517]

Four tests pinning _extract_merchant behaviour under the GRO-517 header
shape: with Visible block, with escaped quotes in Visible, without
Visible (stale/missing case), and with position-independent ordering."
```

---

### Task 2.4: Integration test — header routes tool call + no-tool-call log

**Files:**
- Create: `Canary/tests/integration/test_qa_agent_chat_with_context.py`

- [ ] **Step 1: Read `tests/integration/test_qa_agent_chat.py` for the existing mock pattern**

The bootstrapped_sidecar + anthropic_two_turn_dashboard fixtures from GRO-389 are reusable. You'll want the same pattern (sys.modules injection for `anthropic`, DB factory rebind).

- [ ] **Step 2: Create the test file**

```python
"""Integration tests for QA Agent chat handler with context header.

GRO-517: proves handle_chat(), given a header that includes a visible
entity list, routes the agent's tool call to an alert/case/txn ID from
that list; and that the no-tool-call structured log fires when the
agent answers without calling a tool.
"""

from __future__ import annotations

import logging
import os
from unittest.mock import MagicMock, patch

import pytest
import sys

from canary.db.session_factory import DatabaseSessionFactory

pytestmark = pytest.mark.postgres


CANARY_DB_URL = os.getenv(
    "CANARY_DB_URL",
    "postgresql://canary:canary_dev_2026@localhost:5432/canary",
)


@pytest.fixture
def bootstrapped_sidecar(monkeypatch):
    """Mirror the GRO-389 fixture: rebind module-level db + set ANTHROPIC_API_KEY."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-mock")

    import canary.db.session_factory as sf_module
    original_db = sf_module.db

    factory = DatabaseSessionFactory()
    factory.init_standalone(CANARY_DB_URL)
    sf_module.db = factory

    yield factory

    sf_module.db = original_db
    if factory.session is not None:
        factory.session.remove()
    if factory.engine is not None:
        factory.engine.dispose()


@pytest.fixture
def anthropic_mock():
    """Installable mock — caller sets .side_effect on mock_client.messages.create."""
    fake_mod = MagicMock()
    mock_client = MagicMock()
    fake_mod.Anthropic = MagicMock(return_value=mock_client)

    original = sys.modules.get("anthropic")
    sys.modules["anthropic"] = fake_mod
    try:
        yield mock_client
    finally:
        if original is None:
            del sys.modules["anthropic"]
        else:
            sys.modules["anthropic"] = original


@pytest.mark.asyncio
async def test_chat_with_chirps_context_routes_to_get_alert(
    bootstrapped_sidecar, anthropic_mock, test_merchant,
):
    """When Visible has an alerts_list, agent's tool call should reference
    one of the visible alert IDs."""
    visible_alert_id = "11111111-2222-3333-4444-555555555555"

    tool_use = MagicMock()
    tool_use.type = "tool_use"
    tool_use.name = "get_alert"
    tool_use.id = "toolu_1"
    tool_use.input = {"alert_id": visible_alert_id}

    r1 = MagicMock(); r1.content = [tool_use]
    text_block = MagicMock(); text_block.type = "text"; text_block.text = "Here's the alert"
    r2 = MagicMock(); r2.content = [text_block]
    anthropic_mock.messages.create.side_effect = [r1, r2]

    from canary.services.qa_agent.server import handle_chat

    header = (
        f"[Page: /chirps | Merchant: {test_merchant.id} | "
        f'Visible: {{"type":"alerts_list","alerts":[{{"id":"{visible_alert_id}","title":"t"}}]}}]'
    )
    result = await handle_chat({
        "messages": [{"role": "user", "content": header + "\n\ntell me about the top alert"}],
        "session_id": "ctx-test-1",
    })

    tool_names = [tc["tool"] for tc in result.get("tool_calls", [])]
    assert "get_alert" in tool_names

    # Confirm the agent used the visible ID (not a random one)
    call_inputs = [tc["input"] for tc in result["tool_calls"] if tc["tool"] == "get_alert"]
    assert any(ci.get("alert_id") == visible_alert_id for ci in call_inputs)


@pytest.mark.asyncio
async def test_no_tool_call_logs_structured_event(
    bootstrapped_sidecar, anthropic_mock, test_merchant, caplog,
):
    """When Anthropic returns only text (no tool_use), handle_chat must
    emit a qa_agent.no_tool_call log entry with the user text redacted
    of the header prefix."""
    text_block = MagicMock()
    text_block.type = "text"
    text_block.text = "I don't know what that is."
    r1 = MagicMock(); r1.content = [text_block]
    anthropic_mock.messages.create.side_effect = [r1]

    from canary.services.qa_agent.server import handle_chat

    header = f"[Page: /ops/qa | Merchant: {test_merchant.id}]"
    user_question = "what is this mystery id"

    with caplog.at_level(logging.INFO, logger="canary.services.qa_agent.server"):
        await handle_chat({
            "messages": [{"role": "user", "content": header + "\n\n" + user_question}],
            "session_id": "no-tool-test",
        })

    assert any(
        "qa_agent.no_tool_call" in r.getMessage() and user_question in r.getMessage()
        for r in caplog.records
    ), f"Expected qa_agent.no_tool_call log with '{user_question}' — got: {[r.getMessage() for r in caplog.records]}"

    # Merchant UUID should NOT appear in the log line (header was stripped)
    assert not any(str(test_merchant.id) in r.getMessage() for r in caplog.records)
```

- [ ] **Step 3: Run the tests**

```bash
cd ~/GrowDirect/Canary
python3 -m pytest tests/integration/test_qa_agent_chat_with_context.py -v -m postgres
```
Expected: 2 passed.

Likely snag: the `caplog.at_level` assertion may miss the log if `propagate=False` is set on the canary logger. If so, use `caplog.set_level(logging.INFO)` at the top of the test and remove the `logger=` parameter.

- [ ] **Step 4: Commit**

```bash
cd ~/GrowDirect/Canary
git add tests/integration/test_qa_agent_chat_with_context.py
git commit -m "test(qa-agent): integration — header routes tool call + logs [GRO-517]

Two tests:
- visible alerts list with 1 ID → mock Anthropic calls get_alert with
  that exact ID (proves the agent is grounding in Visible)
- text-only Anthropic response → qa_agent.no_tool_call INFO log fires
  with the user question but WITHOUT the merchant UUID (redaction works)"
```

---

### Task 2.5: Playwright smoke test (end-to-end)

**Files:**
- Create: `Canary/tests/smoke/test_qa_page_context_header.py`

- [ ] **Step 1: Check for an existing admin-login fixture**

```bash
cd ~/GrowDirect/Canary
grep -n "admin\|logged_in\|login" tests/smoke/conftest.py | head -20
```

If you find a fixture like `admin_page` or `logged_in_admin_page`, REUSE it. If you find only merchant-user login fixtures, you'll need to write a new `admin_logged_in_page` fixture — that's fine, add it to `conftest.py` as part of this task (note it in the commit message).

If there's no login fixture at all, STOP and report back — the gate is going to need manual verification and this test belongs in a follow-up issue.

- [ ] **Step 2: Create the smoke test**

Template (adapt fixture name to what exists):

```python
"""Smoke test: end-to-end browser flow verifying the context header lands
in the POST payload to /ops/qa/chat.

GRO-517: proves the full pipeline works in a real browser:
- Visiting /chirps writes sessionStorage.opsContext with alert snapshot
- Clicking through to /ops/qa loads window.OPS_MERCHANT_ID
- Sending a chat message POSTs a payload whose first user message
  starts with `[Page: /chirps | Merchant: <uuid> | Visible: ...]`
"""

from __future__ import annotations

import json
import pytest


pytestmark = pytest.mark.smoke


def test_qa_chat_carries_context_header(admin_page):
    """admin_page is a fixture providing a Playwright page logged in as
    an ops admin. Navigates /chirps → /ops/qa, sends a message, inspects
    the network request."""
    page = admin_page

    # Visit /chirps and wait for alerts to load
    page.goto("http://localhost:5001/chirps")
    page.wait_for_load_state("networkidle")

    # Verify the snapshot landed in sessionStorage
    ctx_raw = page.evaluate("() => sessionStorage.getItem('opsContext')")
    assert ctx_raw, "sessionStorage.opsContext not set on /chirps"
    ctx = json.loads(ctx_raw)
    assert ctx["path"] == "/chirps"
    assert ctx["snapshot"] is not None, "Expected alerts_list snapshot on /chirps"
    assert ctx["snapshot"]["type"] == "alerts_list"

    # Click through to /ops/qa
    page.goto("http://localhost:5001/ops/qa")
    page.wait_for_load_state("networkidle")

    # Verify merchant UUID is present
    merchant = page.evaluate("() => window.OPS_MERCHANT_ID")
    assert merchant, "window.OPS_MERCHANT_ID not set on /ops/qa"

    # Intercept the next POST to /ops/qa/chat
    with page.expect_request("**/ops/qa/chat") as req_info:
        page.fill("#input", "tell me about the top alert")
        page.click("#send")

    request = req_info.value
    body = request.post_data_json
    assert body, "Chat POST had no JSON body"

    first_msg = body["messages"][0]["content"]
    assert first_msg.startswith("[Page: /chirps | Merchant: "), (
        f"Expected context header prefix, got: {first_msg[:200]!r}"
    )
    assert "Visible:" in first_msg, "Expected Visible: block in the header"
    assert "\n\ntell me about the top alert" in first_msg
```

- [ ] **Step 3: Run the smoke test**

```bash
cd ~/GrowDirect/Canary
# Ensure full stack is up
cd devops && docker compose -f docker-compose.localhost.yml up -d && cd ..
python3 -m pytest tests/smoke/test_qa_page_context_header.py -v -m smoke
```

Expected: 1 passed.

Likely snags:
- If `admin_page` fixture doesn't exist in smoke conftest, adapt to whatever fixture name DOES exist. The test's role-check requirement is "logged in, can view /chirps and /ops/qa."
- If `input` / `send` IDs in `qa.html` don't match the test's selectors, check the template and adjust.
- If the test times out waiting for the alerts list, the test merchant needs seeded alerts — use a merchant with known data (maybe the Sandbox Merchant `67584298-7494-43a0-a54e-4d3eb11f86c9`).

- [ ] **Step 4: Commit**

```bash
cd ~/GrowDirect/Canary
git add tests/smoke/test_qa_page_context_header.py
# Add conftest.py if you added a new fixture
git commit -m "test(qa-agent): smoke — end-to-end context header pipeline [GRO-517]

Full browser flow: visit /chirps → snapshot writes to sessionStorage →
navigate /ops/qa → window.OPS_MERCHANT_ID present → send chat →
intercept POST → assert messages[0].content starts with
'[Page: /chirps | Merchant: ... | Visible:'. Proves the complete
pipeline the earlier commits added."
```

---

## Verification Checklist (end of session)

Before declaring the plan complete:

- [ ] 4 unit tests pass (`pytest tests/unit/test_qa_agent_context_header.py`)
- [ ] 2 integration tests pass (`pytest tests/integration/test_qa_agent_chat_with_context.py -m postgres`)
- [ ] 1 smoke test passes (`pytest tests/smoke/test_qa_page_context_header.py -m smoke`)
- [ ] Existing GRO-389 tests still pass (`pytest tests/unit/test_session_factory_standalone.py tests/integration/test_qa_agent_chat.py tests/integration/test_qa_agent_db.py`)
- [ ] Manual browser check: `/chirps` → `/ops/qa` → send "tell me about the top alert" → response references a real alert ID (no hedging)
- [ ] Sidecar log shows `QA Agent → MCP: get_alert(...)` on that request
- [ ] Rebuild + restart qa-agent container to pick up server.py + agent.py changes: `cd ~/GrowDirect/Canary/devops && docker compose -f docker-compose.localhost.yml up -d --build qa-agent`

## Commit Trail Expected

From Chunk 1:
1. `feat(qa-agent): shared ops context snapshot partial [GRO-517]`
2. `feat(qa-agent): include ops context snapshot in app+ops bases [GRO-517]`
3. `feat(qa-agent): /chirps entity snapshot [GRO-517]`
4. `feat(qa-agent): /alert/<uuid> entity snapshot [GRO-517]`
5. `feat(qa-agent): /fox/cases/<uuid> entity snapshot [GRO-517]`
6. `feat(qa-agent): /txn/<uuid> entity snapshot [GRO-517]`
7. `feat(qa-agent): QA page composes context header per turn [GRO-517]`

From Chunk 2:
8. `feat(qa-agent): SYSTEM_PROMPT — UUID principle + reasoning order [GRO-517]`
9. `feat(qa-agent): structured log for no-tool-call responses [GRO-517]`
10. `test(qa-agent): unit tests — context header regex compatibility [GRO-517]`
11. `test(qa-agent): integration — header routes tool call + logs [GRO-517]`
12. `test(qa-agent): smoke — end-to-end context header pipeline [GRO-517]`

Each commit is bisectable. Commits 1–7 build the pipeline incrementally; 8 changes agent behaviour; 9 adds observability; 10–12 are tests.

## Skills to Invoke During Execution

- `@superpowers:test-driven-development` — Tasks 2.3–2.5 are test-first; the earlier tasks are template changes verified by eyeball + curl because JS template work is hard to TDD meaningfully
- `@superpowers:verification-before-completion` — run the verification checklist before declaring done
- `@superpowers:receiving-code-review` — if a reviewer flags issues, apply rigorously

## Risks Called Out in Spec (for implementer awareness)

- SessionStorage is per-tab by design — document, don't fix
- Private-mode browsers silently fail — agent has a "/ops/qa no referrer" case in the prompt
- `/chirps`-view variable names may differ from `alerts` — inspect and adapt in Task 1.3
- `case.linked_alert_ids` / `linked_transaction_ids` may require view-function updates if not already in template scope — inspect and adapt in Tasks 1.5/1.6
- Sidecar rebuild needed after Chunk 2 — Dockerfile hasn't changed, but server.py and agent.py are baked into the image; `docker compose up -d --build qa-agent` is mandatory for changes to land
