---
classification: confidential
owner: GrowDirect LLC
title: QA Agent Tier 0 — Unblock DB Context
date: 2026-04-21
project: Canary
linear:
  - GRO-326 (QA Agent — Claude-powered test assistant at /ops/qa)
  - GRO-388 (DB session factory returns None — duplicate of GRO-389)
  - GRO-389 (DB session factory returns None)
status: Design approved, ready for implementation plan
---

# QA Agent Tier 0 — Unblock DB Context

## Problem

The QA Agent sidecar (GRO-326) shipped Tier 0 MVP but is non-functional for its
stated purpose. Every data-backed tool call fails:

```
ERROR:canary.mcp.tool:MCP tool get_dashboard failed:
  'NoneType' object has no attribute 'query'
ERROR:canary.services.owl.search.executor:Search query failed after 0.0ms:
  'NoneType' object has no attribute 'execute'
```

Root cause: `canary.db.session_factory.db.get_session()` returns `None` inside
the sidecar container. The factory's `init_app()` requires a Flask app to
configure the engine and bind the RLS context bridge. The QA Agent runs as a
standalone Uvicorn ASGI service with no Flask app — so the factory is never
initialized, and `get_session()` returns the un-bound `None`.

Owl search, dashboard queries, transaction lookups, scenario polling, and
threshold reads all fail. The chat returns a generic "database connectivity
issue" message to the user.

GRO-388 and GRO-389 are duplicates filed seven seconds apart on 2026-04-01.

## Goal

Close GRO-388/389. Finish GRO-326 Tier 0 acceptance:

> Chat page loads, Claude responds with Canary context, can invoke atlas_figure
> and sandbox_fire tools, conversation persists across messages in session.

After this spec is implemented, every MCP tool exposed to the QA Agent can hit
the database from inside the sidecar, RLS tenant isolation is preserved, and
the Tier 0 demo path works end-to-end.

## Scope

**In scope:**

- Extend `canary/db/session_factory.py` with a standalone (Flask-free)
  initialization path and a ContextVar-based RLS merchant channel.
- Bootstrap the factory at sidecar startup.
- Parse merchant UUID from chat context and bind it per request.
- Integration tests that prove data flows end-to-end.
- Completeness gate per Canary CLAUDE.md (data in, data out, row counts, route
  responds).
- Linear housekeeping: close GRO-388 as duplicate, close GRO-389, mark GRO-326
  Tier 0 done.

**Out of scope (YAGNI — explicitly deferred):**

- Linear bug filing from chat (GRO-326 Tier 1)
- Atlas inline diagram rendering in chat (Tier 1)
- pgvector transcript memory and cross-session recall (Tier 2)
- Moving in-memory rate limits to Valkey
- Restructuring the tool dispatch loop
- Migrating from raw Anthropic SDK to Claude Agent SDK (SDK still needs
  headless-container support; sidecar architecture makes this a future swap)
- Observability / per-tool error metrics

## Architecture

The sidecar gets a Flask-free DB context. No Flask app is instantiated inside
the sidecar. The existing Flask app path through `init_app()` is untouched.
Two initialization paths coexist on the same `DatabaseSessionFactory`:

| Path | Caller | Merchant source |
|------|--------|-----------------|
| `init_app(flask_app)` | Canary Flask web app | `flask.g.merchant_id` |
| `init_standalone(db_url)` | QA Agent sidecar | `contextvars.ContextVar` |

`_set_rls_context` tries `flask.g` first, then falls back to the ContextVar.
If both are empty, the SQL `SELECT set_current_merchant(...)` call is skipped
and RLS sees NULL — queries fail closed, no data leaks.

## Component 1 — Session factory extension (guardian file)

**File:** `canary/db/session_factory.py`

**Additions (no removals, no behavior change for the Flask path):**

### 1. Module-level ContextVar + helpers

```python
from contextvars import ContextVar, Token

_merchant_ctx: ContextVar[str | None] = ContextVar(
    "canary_merchant_id", default=None
)

def set_merchant_context(merchant_id: str) -> Token:
    """Bind merchant for RLS in non-Flask contexts (QA Agent sidecar).

    Returns a Token — pass it to clear_merchant_context() in a finally block.
    """
    return _merchant_ctx.set(str(merchant_id))

def clear_merchant_context(token: Token) -> None:
    """Reset the merchant ContextVar using the Token from set_merchant_context."""
    _merchant_ctx.reset(token)
```

### 2. `_set_rls_context` fallback

```python
def _set_rls_context(self, connection):
    """Set RLS merchant context at the start of each transaction.

    Order: flask.g first (existing behavior), then ContextVar (sidecar path).
    """
    try:
        from flask import g
        merchant_id = g.get("merchant_id", None)
    except RuntimeError:
        merchant_id = None

    if merchant_id is None:
        merchant_id = _merchant_ctx.get()

    if merchant_id:
        connection.execute(
            text("SELECT set_current_merchant(:mid)"),
            {"mid": merchant_id},
        )
        logger.debug("RLS context set for merchant_id=%s", merchant_id)
```

### 3. `DatabaseSessionFactory.init_standalone(db_url)`

```python
def init_standalone(self, db_url: str) -> None:
    """Initialize engine and session without a Flask app.

    scopefunc is bound to the ContextVar identity so each async task /
    chat request gets its own session under asyncio. Caller is responsible
    for session cleanup (no teardown_appcontext) — use db.session.remove()
    in a finally block at the end of each request.
    """
    self.engine = create_engine(
        db_url,
        pool_size=15,
        max_overflow=25,
        pool_pre_ping=True,
    )
    # scopefunc returns a per-request id so concurrent asyncio tasks don't
    # share one session (default scoped_session is thread-local, which under
    # asyncio = all coroutines on one event loop share one session — a race).
    self.session = scoped_session(
        sessionmaker(bind=self.engine),
        scopefunc=lambda: _merchant_ctx.get() or "__no_merchant__",
    )
    event.listen(self.engine, "begin", self._set_rls_context)
    logger.info(
        "DatabaseSessionFactory initialized (standalone mode, no Flask app)"
    )
```

**Note on scoping:** the scopefunc uses the ContextVar value as the session
identity key. Since each chat request sets a unique merchant UUID (and
ContextVars are per-asyncio-task), this gives per-request session isolation
for concurrent chats from different merchants. Two concurrent requests for the
*same* merchant will share a session — acceptable for the QA Agent's
read-heavy workload; none of the exposed tools write cross-merchant state.

**Net change:** ~30 lines added, zero lines modified in existing paths.

**Guardian:** manifest SHA256 is bumped after edit. User has granted edit
permission for this session; no approval cycle needed. Implementer re-hashes
and updates `.guardian-manifest` as part of the commit.

## Component 2 — Sidecar integration

**File:** `canary/services/qa_agent/server.py`

### 1. Startup bootstrap — ASGI lifespan

Use the ASGI lifespan protocol instead of module-level init so the engine is
created after uvicorn's event loop starts (module-level init runs at import
time, which is pre-fork if workers > 1 — SQLAlchemy connection pools don't
survive `fork()`):

```python
from canary.db.session_factory import (
    db,
    set_merchant_context,
    clear_merchant_context,
)

async def _lifespan(scope, receive, send):
    while True:
        message = await receive()
        if message["type"] == "lifespan.startup":
            db_url = os.getenv("CANARY_DB_URL")
            if db_url:
                db.init_standalone(db_url)
                logger.info(
                    "QA Agent: DB session factory initialized (standalone)"
                )
            else:
                logger.error(
                    "QA Agent: CANARY_DB_URL not set — DB tools will fail"
                )
            await send({"type": "lifespan.startup.complete"})
        elif message["type"] == "lifespan.shutdown":
            if db.session is not None:
                db.session.remove()
            if db.engine is not None:
                db.engine.dispose()
            await send({"type": "lifespan.shutdown.complete"})
            return
```

Update the top-level `app` ASGI callable to dispatch by scope type. Final
shape:

```python
async def app(scope, receive, send):
    if scope["type"] == "lifespan":
        await _lifespan(scope, receive, send)
        return
    if scope["type"] != "http":
        return
    # ... existing http branch unchanged
```

**Deployment constraint:** the sidecar runs with `workers=1` (default in
current Dockerfile). If that ever changes, revisit — connection pooling and
the in-memory rate-limit counters both assume single-worker.

### 2. Per-request merchant binding in `handle_chat`

Parse the `Merchant: <uuid>` prefix from the earliest user message whose
content is a string (tool-result turns are also `role=user` but their content
is a list of dicts — the string check skips them). Set the ContextVar before
tool dispatch, reset in `finally`:

```python
import re

_MERCHANT_RE = re.compile(r"Merchant:\s*([0-9a-f-]{36})", re.IGNORECASE)

def _extract_merchant(messages: list[dict]) -> str | None:
    """Return the first Merchant: <uuid> found in a string-content user
    message. Tool-result messages (role=user, content=list) are skipped."""
    for m in messages:
        if m.get("role") != "user":
            continue
        content = m.get("content")
        if not isinstance(content, str):
            continue
        match = _MERCHANT_RE.search(content)
        if match:
            return match.group(1)
    return None

# Inside handle_chat, short-circuit when no merchant context is available —
# every DB-backed tool would fail closed anyway, and entering the dispatch
# loop would share the "no-merchant" session bucket across concurrent
# unauthenticated requests (session.remove() would yank it mid-query).
merchant_id = _extract_merchant(messages)
if merchant_id is None:
    return {
        "text": "No merchant context in request. The QA Agent needs a "
                "Merchant: <uuid> prefix to answer data questions.",
        "tool_calls": [],
        "model": DEFAULT_MODEL,
    }

ctx_token = set_merchant_context(merchant_id)
try:
    # existing tool dispatch loop (unchanged)
    ...
finally:
    clear_merchant_context(ctx_token)
    if db.session is not None:
        # scopefunc keys on ContextVar, so this only removes the session for
        # THIS merchant's scope — other concurrent merchant requests have
        # their own session buckets and are unaffected
        db.session.remove()
```

### 3. No changes to `agent.py`

The HTTP proxy stays dumb — it forwards JSON to the sidecar and returns the
response envelope.

### 4. Docker compose

Verified during spec authoring: `CANARY_DB_URL` is already present in the
qa-agent service environment at `Canary/devops/docker-compose.localhost.yml`
(line 433), pointing at the shared `growdirect_postgres:5432/canary`
database. No compose changes required. The dev compose override at
`docker-compose.dev.yml` only patches `volumes` — it does not redefine env.

## Data flow after fix

```
POST /ops/qa/chat {messages: [{role: "user",
                                content: "[Page: /chirps | Merchant: <uuid>] ..."}]}
    ↓
Flask ops_console blueprint → qa_agent.agent.chat() → HTTP sidecar
    ↓
Sidecar server.py handle_chat():
    1. Parse Merchant: <uuid> from message
    2. set_merchant_context(uuid) → ContextVar.set()
    3. Claude API call with tool definitions
    4. Claude returns tool_use: get_dashboard({merchant_id: uuid})
    5. execute_tool("get_dashboard", ...) → calls get_session()
    6. get_session() returns the scoped session (real, not None)
    7. session.query(...) fires; SQLAlchemy "begin" event triggers
       _set_rls_context
    8. _set_rls_context reads ContextVar → SELECT set_current_merchant(uuid)
    9. Query executes with RLS enforced → rows returned
    10. Tool result returned to Claude → synthesis → final text
    11. finally: clear_merchant_context(token); db.session.remove()
    ↓
Response envelope with text + tool_calls + usage
```

## Testing

All tests live under `Canary/tests/`.

### Unit — `tests/unit/test_session_factory_standalone.py` (new)

- `test_init_standalone_creates_engine_and_session` — after init, `db.engine`
  and `db.session` are non-None; engine URL matches input
- `test_context_var_round_trip` — `set_merchant_context("abc")`,
  `_merchant_ctx.get()` returns `"abc"`, `clear_merchant_context(token)`
  resets to default None
- `test_rls_listener_uses_context_var_when_no_flask_g` — mock connection,
  set ContextVar, trigger `_set_rls_context`, assert
  `SELECT set_current_merchant` fires with ContextVar value
- `test_rls_listener_still_uses_flask_g_when_present` — regression guard; in a
  Flask app context with `g.merchant_id`, ContextVar value is ignored
- `test_rls_listener_skips_sql_when_both_sources_empty` — no ContextVar, no
  Flask g, no SQL call

### Integration — `tests/integration/test_qa_agent_db.py` (new, `@pytest.mark.postgres`)

All tests in this file run **without** a Flask app context so the ContextVar
fallback path in `_set_rls_context` is actually exercised. If the shared
`conftest.py` auto-pushes a Flask app context for all tests, this file needs a
local fixture that pops it (or uses a fresh SQLAlchemy connection outside any
app context).

- `test_standalone_factory_executes_sql` — init against `canary_test`,
  `get_session().execute(text("SELECT 1"))` returns 1
- `test_db_tool_via_execute_tool` — seed a transaction row for merchant A,
  set merchant context A, call `execute_tool("get_dashboard", {...})`, assert
  row data returned (not a NoneType error envelope)
- `test_rls_isolation_across_merchants` — seed rows for merchants A and B,
  set context A → query returns only A's rows; set context B → only B's rows
- `test_rls_fails_closed_without_merchant_context` — seed rows for merchant A,
  set **no** context (neither Flask g nor ContextVar), query
  `sales.transactions` → returns zero rows. Proves the fail-closed claim; a
  regression in the RLS policy ("allow all when current_merchant is null")
  would surface here.

### Integration — `tests/integration/test_qa_agent_chat.py` (new, `@pytest.mark.postgres`)

- `test_sidecar_chat_endpoint_routes_dashboard_query` — POST directly to the
  **sidecar** `http://qa-agent:8002/chat` (or test client equivalent) with a
  merchant-prefixed message; assert 200, `tool_calls` contains
  `get_dashboard`, response text doesn't match the failure pattern. This test
  covers the sidecar in isolation from the Flask proxy.

**Test data:** reuse existing fixtures in `conftest.py`. No new sandbox payment
creation for tests — that's the completeness gate's job.

## Completeness gate (end-of-session verification)

Per Canary CLAUDE.md "No Lazy Pipes" delivery standard. The gate runs against
the **Flask ops-console endpoint** (port 5001), not the sidecar directly —
this proves the full user-facing path works, not just the sidecar in
isolation. The sidecar-only path is covered by the integration tests.

1. **Data in:** fire a scenario through the Flask `/ops/qa/chat` endpoint →
   `fire_scenario({scenario: "high_velocity_refunds"})` → row lands in
   `sales.transactions` for the test merchant.
2. **Data out:** same session, call `get_dashboard` → returns the row just
   written.
3. **Row counts:** `SELECT count(*) FROM sales.transactions WHERE
   merchant_id = :test_merchant_id` before and after; delta matches exactly
   one.
4. **Route responds:** `curl -XPOST http://localhost:5001/ops/qa/chat -d
   '{...merchant-prefixed message...}'` returns 200 with real data, not the
   "database connectivity issue" message.

All four must pass before the session is declared done.

## Linear closeout

- **GRO-388** → close as duplicate of GRO-389 (no commit link needed)
- **GRO-389** → close with commit link and one-line verification note
- **GRO-326** → update description: check off Tier 0 acceptance criteria;
  note Tier 1 (Linear bug filing, Atlas inline rendering) as next cycle

## Risks and non-goals

- **Sidecar restart wipes rate-limit counters.** Pre-existing (lives in module
  globals). GRO-326 Tier 2+ territory. Not addressed here.
- **No transcript persistence.** Pre-existing. Tier 2.
- **ContextVar is per-async-task.** If any tool handler spawns a thread or
  uses a separate event loop, the merchant binding won't propagate. Current
  tool code is sync and in-process; fine today, worth re-checking if tool
  dispatch ever goes multi-threaded.
- **QA_AGENT_PORT discrepancy.** GRO-326 ticket and the platform CLAUDE.md port
  table mention 8004; `Dockerfile.qa-agent` and `server.py` both use 8002.
  Not addressed here — out of scope for the DB fix. File a separate Linear
  issue during closeout.
- **Tier 0 acceptance names `sandbox_fire`, tool is `fire_scenario`.** GRO-326
  acceptance copy is stale. Update the ticket description when marking Tier 0
  done to match the actual tool names exposed by `tools.py`.
- **Single-worker constraint.** Sidecar must run `workers=1` under uvicorn.
  Module-level rate-limit dicts and the factory's connection pool both
  assume it. Documented; not enforced in code.
- **Silent tool failures look like the old bug.** Today's symptom ("database
  connectivity issue") is a tool-level error surfaced as a synth. After this
  fix, DB tools return real data — but any non-DB tool failure still gets
  swallowed into a generic response. Observability (per-tool error metrics,
  structured tool_calls with status) is deferred to Tier 1/2. Mitigation
  during verification: watch sidecar logs for `MCP tool ... failed` lines
  while testing.

## Commit strategy

- One bisectable commit for the factory extension (guardian file)
- One commit for the sidecar integration
- One commit per test file
- One trailing commit for Linear closeout notes (if any code touches Linear
  state; otherwise Linear is closed via the MCP tool and not captured in git)

Commit message pattern: `fix(qa-agent): wire standalone DB session factory —
closes GRO-389 [Tier 0]`
