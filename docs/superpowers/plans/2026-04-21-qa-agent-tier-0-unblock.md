# QA Agent Tier 0 — Unblock DB Context Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wire a Flask-free DB session into the QA Agent sidecar so every MCP tool exposed to the agent can hit the database with RLS tenant isolation preserved. Closes GRO-388/389 and finishes GRO-326 Tier 0 acceptance.

**Architecture:** Extend `canary/db/session_factory.py` (guardian file) with a ContextVar-based RLS merchant channel and a Flask-free `init_standalone(db_url)` method. The QA Agent sidecar (uvicorn ASGI) bootstraps the factory at lifespan startup, parses the `Merchant: <uuid>` prefix from the incoming chat message, binds it to the ContextVar before tool dispatch, and clears it in `finally`. The existing Flask app path (`init_app` + `flask.g`) is untouched. `_set_rls_context` tries `flask.g` first, falls back to the ContextVar — so both callers work without branching at the call site.

**Tech Stack:** Python 3.12, SQLAlchemy 2.0 (`scoped_session` with custom `scopefunc`), `contextvars.ContextVar`, uvicorn (ASGI lifespan protocol), pytest with `@pytest.mark.postgres` for integration tests, httpx.AsyncClient + ASGITransport for in-process sidecar testing, Anthropic SDK (mocked in tests).

**Spec:** [docs/superpowers/specs/2026-04-21-qa-agent-tier-0-unblock-design.md](../specs/2026-04-21-qa-agent-tier-0-unblock-design.md)

**Linear:** GRO-326 (parent), GRO-388/389 (blocking bug)

---

## File Structure

**Modified:**
- `Canary/canary/db/session_factory.py` (guardian file — ~30 LOC added, zero removed)
- `Canary/canary/services/qa_agent/server.py` (ASGI lifespan + merchant binding in handle_chat)
- `Canary/.guardian-manifest` (SHA256 bump + entry for the change)

**Created:**
- `Canary/tests/unit/test_session_factory_standalone.py` (5 unit tests)
- `Canary/tests/integration/test_qa_agent_db.py` (4 integration tests)
- `Canary/tests/integration/test_qa_agent_chat.py` (1 integration test)

**Unchanged (verified during planning):**
- `Canary/canary/services/qa_agent/agent.py` (HTTP proxy stays dumb)
- `Canary/canary/services/qa_agent/tools.py` (tool handlers already call `get_session()` correctly; they just need the factory actually initialized)
- `Canary/devops/docker-compose.localhost.yml` (`CANARY_DB_URL` already present at line 433)
- `Canary/Dockerfile.qa-agent` (workers=1 default, no change)

---

## Chunk 1: Session factory extension + unit tests

This chunk extends the guardian file with the ContextVar channel and standalone init path, guarded by unit tests. Unit tests go first (TDD). After this chunk, the factory supports both Flask and standalone initialization; nothing in the sidecar uses it yet.

### Task 1.1: Unit test file scaffolding

**Files:**
- Create: `Canary/tests/unit/test_session_factory_standalone.py`

- [ ] **Step 1: Create the test file with imports and a docstring**

```python
"""Unit tests for session_factory standalone (Flask-free) init path.

Covers the ContextVar-based RLS channel added for the QA Agent sidecar
(GRO-389). Tests run without a Flask app context to exercise the fallback
path in _set_rls_context.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy import create_engine, text


# ---------------------------------------------------------------------------
# These imports will FAIL on the first run — the symbols don't exist yet.
# That's the point of TDD: RED first, then GREEN.
# ---------------------------------------------------------------------------
from canary.db.session_factory import (
    DatabaseSessionFactory,
    _merchant_ctx,
    set_merchant_context,
    clear_merchant_context,
)
```

- [ ] **Step 2: Run the empty test file to confirm imports fail**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/unit/test_session_factory_standalone.py -v`

Expected: `ImportError: cannot import name '_merchant_ctx' from 'canary.db.session_factory'` (RED — the symbols don't exist yet; that's correct for this step)

- [ ] **Step 3: Commit scaffold**

```bash
cd ~/GrowDirect/Canary
git add tests/unit/test_session_factory_standalone.py
git commit -m "test(session-factory): scaffold standalone unit tests [GRO-389]"
```

---

### Task 1.2: Write failing unit tests

**Files:**
- Modify: `Canary/tests/unit/test_session_factory_standalone.py`

- [ ] **Step 1: Add all five unit tests**

Append to the file:

```python
# ---------------------------------------------------------------------------
# Test 1: init_standalone creates engine and session
# ---------------------------------------------------------------------------

def test_init_standalone_creates_engine_and_session():
    """init_standalone should leave factory.engine and factory.session non-None."""
    factory = DatabaseSessionFactory()
    # Use SQLite in-memory for this unit test — we're only checking the
    # factory wiring, not RLS SQL execution (that's integration territory).
    factory.init_standalone("sqlite:///:memory:")
    assert factory.engine is not None
    assert factory.session is not None
    assert str(factory.engine.url) == "sqlite:///:memory:"


# ---------------------------------------------------------------------------
# Test 2: ContextVar round-trip via public helpers
# ---------------------------------------------------------------------------

def test_context_var_round_trip():
    """set_merchant_context stores the value; clear_merchant_context resets it."""
    # Default is None
    assert _merchant_ctx.get() is None

    token = set_merchant_context("merchant-abc-123")
    try:
        assert _merchant_ctx.get() == "merchant-abc-123"
    finally:
        clear_merchant_context(token)

    assert _merchant_ctx.get() is None


# ---------------------------------------------------------------------------
# Test 3: _set_rls_context uses ContextVar when no Flask g is present
# ---------------------------------------------------------------------------

def test_rls_listener_uses_context_var_when_no_flask_g():
    """In a non-Flask context, _set_rls_context should fire SQL from ContextVar."""
    factory = DatabaseSessionFactory()
    mock_conn = MagicMock()

    token = set_merchant_context("merchant-from-ctxvar")
    try:
        # Call the listener directly — no Flask app context active, so the
        # `from flask import g` try inside will hit RuntimeError and fall
        # back to the ContextVar.
        factory._set_rls_context(mock_conn)
    finally:
        clear_merchant_context(token)

    # Assert SQL was executed with the ContextVar value
    assert mock_conn.execute.call_count == 1
    args, kwargs = mock_conn.execute.call_args
    # args[0] is a TextClause; args[1] is the params dict
    assert str(args[0]) == "SELECT set_current_merchant(:mid)"
    assert args[1] == {"mid": "merchant-from-ctxvar"}


# ---------------------------------------------------------------------------
# Test 4: _set_rls_context prefers flask.g when both are set (regression guard)
# ---------------------------------------------------------------------------

def test_rls_listener_still_uses_flask_g_when_present():
    """Flask path must be unchanged: flask.g.merchant_id wins over ContextVar."""
    from flask import Flask

    factory = DatabaseSessionFactory()
    mock_conn = MagicMock()
    app = Flask(__name__)

    ctx_token = set_merchant_context("merchant-from-ctxvar")
    try:
        with app.app_context():
            from flask import g
            g.merchant_id = "merchant-from-flask-g"
            factory._set_rls_context(mock_conn)
    finally:
        clear_merchant_context(ctx_token)

    assert mock_conn.execute.call_count == 1
    args, _ = mock_conn.execute.call_args
    # Flask g wins — ContextVar value must NOT appear
    assert args[1] == {"mid": "merchant-from-flask-g"}


# ---------------------------------------------------------------------------
# Test 5: No SQL when both sources empty (fail-closed at the listener level)
# ---------------------------------------------------------------------------

def test_rls_listener_skips_sql_when_both_sources_empty():
    """No Flask g, no ContextVar → no SELECT set_current_merchant call."""
    factory = DatabaseSessionFactory()
    mock_conn = MagicMock()

    # Sanity: ContextVar is at default
    assert _merchant_ctx.get() is None

    factory._set_rls_context(mock_conn)

    assert mock_conn.execute.call_count == 0
```

- [ ] **Step 2: Run the tests to confirm they all fail for the right reason**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/unit/test_session_factory_standalone.py -v`

Expected: Still `ImportError` (symbols still don't exist). This is the RED phase. Do NOT proceed to implementation until you see the ImportError.

- [ ] **Step 3: Commit failing tests**

```bash
cd ~/GrowDirect/Canary
git add tests/unit/test_session_factory_standalone.py
git commit -m "test(session-factory): add 5 failing standalone tests [GRO-389]"
```

---

### Task 1.3: Extend session_factory.py to make tests pass

**Files:**
- Modify: `Canary/canary/db/session_factory.py` (guardian-protected — user granted edit permission for this session)

- [ ] **Step 1: Read the current file to establish exact insertion points**

Run: `cd ~/GrowDirect/Canary && wc -l canary/db/session_factory.py`

Expected: file is short (under 100 lines). Re-read it with the Read tool so the exact existing content is fresh in context. Key existing symbols: `class DatabaseSessionFactory`, `def init_app`, `def _set_rls_context`, `def get_session`, `db = DatabaseSessionFactory()` singleton at module bottom.

- [ ] **Step 2: Add ContextVar + public helpers at module top (after existing imports)**

Insert immediately after the existing `logger = logging.getLogger(__name__)` line:

```python
from contextvars import ContextVar, Token

# ---------------------------------------------------------------------------
# Merchant context channel for non-Flask callers (QA Agent sidecar, GRO-389).
# Flask callers continue to use flask.g; this ContextVar is the fallback
# read by _set_rls_context when no Flask app context is active.
# ---------------------------------------------------------------------------
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

- [ ] **Step 3: Update `_set_rls_context` to fall back to the ContextVar**

Replace the existing `_set_rls_context` method body. The only change is adding one fallback line before the `if merchant_id:` block:

```python
def _set_rls_context(self, connection):
    """Set the RLS merchant context at the start of each transaction.

    Order: flask.g first (existing behavior), then ContextVar (sidecar path).
    """
    try:
        from flask import g
        merchant_id = g.get("merchant_id", None)
    except RuntimeError:
        merchant_id = None

    # NEW: fall back to the sidecar ContextVar when no Flask g is available
    if merchant_id is None:
        merchant_id = _merchant_ctx.get()

    if merchant_id:
        connection.execute(
            text("SELECT set_current_merchant(:mid)"),
            {"mid": merchant_id},
        )
        logger.debug("RLS context set for merchant_id=%s", merchant_id)
```

- [ ] **Step 4: Add `init_standalone` method to `DatabaseSessionFactory`**

Insert this method inside the `DatabaseSessionFactory` class, immediately after the existing `init_app` method:

```python
def init_standalone(self, db_url: str) -> None:
    """Initialize engine and session without a Flask app (QA Agent sidecar).

    scopefunc is bound to the ContextVar value so each async task / chat
    request gets its own session under asyncio. Default scoped_session is
    thread-local, which under asyncio means all coroutines on one event
    loop share one session — a race on session.remove().

    Caller is responsible for session cleanup (no teardown_appcontext).
    Use db.session.remove() in a finally block at the end of each request.
    """
    self.engine = create_engine(
        db_url,
        pool_size=15,
        max_overflow=25,
        pool_pre_ping=True,
    )
    self.session = scoped_session(
        sessionmaker(bind=self.engine),
        scopefunc=lambda: _merchant_ctx.get() or "__no_merchant__",
    )
    event.listen(self.engine, "begin", self._set_rls_context)
    logger.info(
        "DatabaseSessionFactory initialized (standalone mode, no Flask app)"
    )
```

- [ ] **Step 5: Run the unit tests to confirm they pass**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/unit/test_session_factory_standalone.py -v`

Expected: all 5 tests PASS. If test 3 fails on `str(args[0])` assertion (SQLAlchemy TextClause repr can vary), change the assertion to:
```python
assert "set_current_merchant" in str(args[0])
```

- [ ] **Step 6: Run the full unit test suite to verify no regressions in Flask path**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/unit/ -v --ignore=tests/unit/test_session_factory_standalone.py`

Expected: same pass/fail counts as before this change. If anything that was passing is now failing, investigate — the Flask path `_set_rls_context` read order should be unchanged.

- [ ] **Step 7: Update the guardian manifest**

Compute the new SHA256:
```bash
cd ~/GrowDirect/Canary
shasum -a 256 canary/db/session_factory.py
```

Edit `.guardian-manifest`: update the `canary/db/session_factory.py` entry's `sha256`, set `last_guardian_edit` to the current UTC ISO-8601 timestamp, update `updated_at` at the top of the manifest, and set `reason` to `"GRO-389: Add ContextVar RLS channel + init_standalone for QA Agent sidecar"`.

- [ ] **Step 8: Commit the factory change + manifest bump as one bisectable commit**

```bash
cd ~/GrowDirect/Canary
git add canary/db/session_factory.py .guardian-manifest
git commit -m "fix(db): add ContextVar RLS channel + init_standalone [GRO-389]

Extends DatabaseSessionFactory with a Flask-free initialization path for
the QA Agent sidecar. ContextVar-based merchant channel falls through in
_set_rls_context when no Flask app context is active; existing Flask path
is unchanged.

Guardian manifest: SHA256 bumped for canary/db/session_factory.py."
```

---

## Chunk 2: Sidecar integration

This chunk wires the sidecar to bootstrap the factory at ASGI lifespan startup and to bind/clear the merchant ContextVar around each chat request. No new files — `server.py` is the only edit.

### Task 2.1: Add ASGI lifespan handler

**Files:**
- Modify: `Canary/canary/services/qa_agent/server.py`

- [ ] **Step 1: Re-read the current server.py to confirm existing structure**

Use the Read tool on `Canary/canary/services/qa_agent/server.py`. Key landmarks:
- Module-level imports (lines 17-27)
- Rate limiting globals (lines 29-34)
- `async def handle_chat(data)` (lines 37-156)
- `async def app(scope, receive, send)` top-level ASGI callable (lines 161-209)
- `if __name__ == "__main__"` uvicorn boot (lines 212-222)

- [ ] **Step 2: Add lifespan handler and session_factory imports**

After the existing `from canary.services.qa_agent.agent import SYSTEM_PROMPT, DEFAULT_MODEL` line, add:

```python
from canary.db.session_factory import (
    db,
    set_merchant_context,
    clear_merchant_context,
)
```

Immediately before the `async def app` definition (around line 161), insert the lifespan handler:

```python
# ---------------------------------------------------------------------------
# ASGI lifespan — bootstrap DB factory at startup, dispose on shutdown.
# Uvicorn emits lifespan events after the event loop starts, so engine
# creation happens post-fork (if workers>1 is ever used). See spec for the
# single-worker constraint.
# ---------------------------------------------------------------------------

async def _lifespan(scope: dict, receive, send) -> None:
    while True:
        message = await receive()
        if message["type"] == "lifespan.startup":
            db_url = os.getenv("CANARY_DB_URL")
            if db_url:
                db.init_standalone(db_url)
                logger.info(
                    "QA Agent: DB session factory initialized (standalone mode)"
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

- [ ] **Step 3: Update the top-level `app` callable to dispatch lifespan events**

Find the existing:
```python
async def app(scope: dict, receive, send) -> None:
    """Minimal ASGI app — two routes: POST /chat and GET /health."""
    if scope["type"] != "http":
        return
```

Replace those three lines with:
```python
async def app(scope: dict, receive, send) -> None:
    """Minimal ASGI app — lifespan + two HTTP routes: POST /chat, GET /health."""
    if scope["type"] == "lifespan":
        await _lifespan(scope, receive, send)
        return
    if scope["type"] != "http":
        return
```

- [ ] **Step 4: Verify the file still parses**

Run: `cd ~/GrowDirect/Canary && python3 -c "from canary.services.qa_agent import server; print(server.app)"`

Expected: prints the ASGI callable, no import errors. If it errors on missing `canary.db.session_factory.set_merchant_context`, the Chunk 1 commit didn't land — go back.

- [ ] **Step 5: Commit the lifespan hookup**

```bash
cd ~/GrowDirect/Canary
git add canary/services/qa_agent/server.py
git commit -m "feat(qa-agent): bootstrap DB factory via ASGI lifespan [GRO-389]

Sidecar now initializes DatabaseSessionFactory in standalone mode when
CANARY_DB_URL is set. Engine disposed on shutdown. Single-worker
deployment required (see spec)."
```

---

### Task 2.2: Add merchant extraction + bind/clear in handle_chat

**Files:**
- Modify: `Canary/canary/services/qa_agent/server.py`

- [ ] **Step 1: Add the merchant regex and extractor at module top**

After the rate-limiting globals block (around line 34), add:

```python
import re

# ---------------------------------------------------------------------------
# Merchant extraction — the ops-console chat template prepends a context
# header like "[Page: /chirps | Merchant: <uuid>] <user message>". We parse
# the UUID out and bind it as RLS context for the duration of the request.
# ---------------------------------------------------------------------------

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
```

- [ ] **Step 2: Wrap the existing tool dispatch loop in `handle_chat` with merchant binding**

Find the existing block inside `handle_chat` (starts with the `client = Anthropic(api_key=api_key)` line around line 89). Before that line, insert the merchant check — AFTER the rate-limit checks but BEFORE the Anthropic client construction:

```python
    # Merchant context required for any DB-backed tool. Without it, every
    # tool that hits RLS would fail closed — and entering the dispatch loop
    # would share the "__no_merchant__" session bucket across concurrent
    # requests, creating a session.remove() race. Short-circuit cleanly.
    merchant_id = _extract_merchant(messages)
    if merchant_id is None:
        return {
            "text": (
                "No merchant context in request. The QA Agent needs a "
                "[Page: ... | Merchant: <uuid>] prefix to answer data "
                "questions."
            ),
            "tool_calls": [],
            "model": DEFAULT_MODEL,
        }

    ctx_token = set_merchant_context(merchant_id)
```

Then wrap the existing dispatch loop (the `for _ in range(10):` block through `_daily_count += 1`) in a `try` / `finally`:

```python
    try:
        # ... existing dispatch loop, unchanged ...
        for _ in range(10):
            # ... existing body ...
        # ... existing rate-limit updates ...
        _session_counts[session_id] = session_count + 1
        _daily_count += 1

        return {
            "text": "\n".join(text_parts),
            "tool_calls": all_tool_calls,
            "model": DEFAULT_MODEL,
            "usage": {
                "session_remaining": MAX_MESSAGES_PER_SESSION - session_count - 1,
                "daily_remaining": MAX_MESSAGES_PER_DAY - _daily_count,
            },
        }
    finally:
        clear_merchant_context(ctx_token)
        if db.session is not None:
            # scopefunc keys on the ContextVar, so this only removes the
            # session for THIS merchant's bucket — concurrent requests for
            # other merchants have their own sessions and are unaffected.
            db.session.remove()
```

**Note on existing structure:** the original `for` loop has a `break` for final responses and a `else:` (on the `for`) for max-depth. Both paths must end up inside the `try`. Double-check the indentation after editing — Python will silently accept misaligned `finally` blocks that behave differently than intended.

- [ ] **Step 3: Verify imports & syntax**

Run: `cd ~/GrowDirect/Canary && python3 -c "from canary.services.qa_agent import server; print('ok')"`

Expected: prints `ok`.

- [ ] **Step 4: Smoke-test the extraction function from the REPL**

Run: 
```bash
cd ~/GrowDirect/Canary && python3 -c "
from canary.services.qa_agent.server import _extract_merchant
# Valid case
msgs = [{'role': 'user', 'content': '[Page: /chirps | Merchant: 12345678-1234-1234-1234-1234567890ab] how many alerts'}]
print('case1:', _extract_merchant(msgs))

# Tool result case (should be skipped)
msgs = [{'role': 'user', 'content': [{'type': 'tool_result', 'tool_use_id': 'x', 'content': 'data'}]}]
print('case2:', _extract_merchant(msgs))

# No merchant
msgs = [{'role': 'user', 'content': 'hello'}]
print('case3:', _extract_merchant(msgs))
"
```

Expected:
```
case1: 12345678-1234-1234-1234-1234567890ab
case2: None
case3: None
```

- [ ] **Step 5: Commit**

```bash
cd ~/GrowDirect/Canary
git add canary/services/qa_agent/server.py
git commit -m "feat(qa-agent): bind merchant RLS context per chat request [GRO-389]

Parses Merchant: <uuid> from the earliest string-content user message
(tool-result messages are skipped) and sets the ContextVar before the
tool dispatch loop. Session cleanup and context reset happen in finally.
Short-circuits with a clear error when no merchant is present —
avoids the shared __no_merchant__ session bucket race."
```

---

## Chunk 3: Integration tests, completeness gate, Linear closeout

This chunk proves the fix end-to-end and cleans up Linear. Integration tests require a running `growdirect_postgres` container. Completeness gate requires the full stack (`docker compose up` in `~/GrowDirect/Canary/devops`).

### Task 3.1: DB integration tests

**Files:**
- Create: `Canary/tests/integration/test_qa_agent_db.py`

- [ ] **Step 1: Read existing integration fixtures to understand conventions**

Use the Read tool on `Canary/tests/integration/conftest.py` — key fixtures already available: `canary_engine` (session-scoped), `app_session` / `sales_session` (per-test rollback), `test_merchant` (seeds a merchant row).

Confirm: the conftest does NOT auto-push a Flask app context — tests use raw `Session` bindings. This means the ContextVar fallback path will be exercised without extra fixtures.

- [ ] **Step 2: Create the test file**

```python
"""Integration tests for QA Agent DB session factory wiring.

GRO-389: proves the standalone factory can execute SQL, tools can reach
the DB, RLS isolates across merchants, and queries fail closed when no
merchant context is bound.

All tests run without a Flask app context — the ContextVar fallback in
_set_rls_context is what we're exercising.

SCHEMA NAMES: the database has three schemas named `app`, `sales`, and
`metrics` (confirmed via canary/models/base.py — MetaData(schema="app")
etc.). No `canary_` prefix. Use `app.merchants`, `sales.transactions`.

RLS POLICIES: policies are applied by devops/seeds/level_b_demo.py, NOT
by devops/init-db/*. Tests 3 and 4 check for policy presence and skip if
absent — a clean test DB without the seed run is expected to lack policies.
"""

from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone

import pytest
from sqlalchemy import text

from canary.db.session_factory import (
    DatabaseSessionFactory,
    set_merchant_context,
    clear_merchant_context,
)

pytestmark = pytest.mark.postgres


CANARY_DB_URL = os.getenv(
    "CANARY_DB_URL",
    "postgresql://canary:canary_dev_2026@localhost:5432/canary",
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def standalone_factory():
    """Fresh factory per test — avoids cross-test pool/listener bleed.

    CONTRACT: do not call factory.init_standalone() twice on the same
    factory instance. SQLAlchemy registers event listeners cumulatively
    and a double-init would fire _set_rls_context twice per begin event.
    """
    factory = DatabaseSessionFactory()
    factory.init_standalone(CANARY_DB_URL)
    yield factory
    if factory.session is not None:
        factory.session.remove()
    if factory.engine is not None:
        factory.engine.dispose()


@pytest.fixture
def rls_policy_present(committed_app_session):
    """Skip the test unless the RLS policy we depend on is actually applied.

    Policies are applied by devops/seeds/level_b_demo.py, not init-db. A fresh
    test DB without the seed run has no RLS — and our fail-closed / isolation
    tests would fail for environmental reasons, masking real regressions.
    """
    result = committed_app_session.execute(
        text(
            "SELECT policyname FROM pg_policies "
            "WHERE schemaname = 'sales' AND tablename = 'transactions'"
        )
    ).fetchall()
    if not result:
        pytest.skip(
            "RLS policy on sales.transactions not applied in test DB. "
            "Run devops/seeds/level_b_demo.py to enable RLS-dependent tests."
        )


# ---------------------------------------------------------------------------
# Test 1: standalone factory can execute SQL
# ---------------------------------------------------------------------------

def test_standalone_factory_executes_sql(standalone_factory):
    """Baseline: the factory returns a real session that runs a SELECT 1."""
    sess = standalone_factory.get_session()
    assert sess is not None

    result = sess.execute(text("SELECT 1 AS one"))
    assert result.scalar() == 1


# ---------------------------------------------------------------------------
# Test 2: a DB-backed MCP tool runs via execute_tool without a NoneType crash
# ---------------------------------------------------------------------------

def test_db_tool_via_execute_tool(standalone_factory, test_merchant):
    """execute_tool('get_dashboard', ...) must not return the NoneType error
    envelope that was the GRO-389 symptom.

    Monkey-patch works because analytics/alerts/owl/tsp tools call
    `from canary.db.session_factory import get_session` and the `get_session()`
    function resolves `db.get_session()` at call time through the module-level
    `db` name — which we rebind here. Any tool that does `from ... import db`
    directly would bypass the patch; grep confirms none do today.
    """
    import canary.db.session_factory as sf_module
    original_db = sf_module.db
    sf_module.db = standalone_factory
    try:
        token = set_merchant_context(str(test_merchant.id))
        try:
            from canary.services.qa_agent.tools import execute_tool
            result = execute_tool(
                "get_dashboard", {"merchant_id": str(test_merchant.id)}
            )
        finally:
            clear_merchant_context(token)
    finally:
        sf_module.db = original_db

    # The bug surfaced as {"error": "... 'NoneType' object has no attribute 'query'"}.
    # We don't care what get_dashboard returns in detail — we care that it's
    # NOT that specific error.
    if isinstance(result, dict) and "error" in result:
        assert "NoneType" not in result["error"], (
            f"get_dashboard still returning the GRO-389 symptom: {result['error']}"
        )


# ---------------------------------------------------------------------------
# Test 3: RLS isolation across merchants (positive case)
# ---------------------------------------------------------------------------

def test_rls_isolation_across_merchants(
    standalone_factory, committed_app_session, committed_sales_session,
    rls_policy_present,
):
    """Seed a transaction for merchant A and one for merchant B; each
    merchant context sees only its own rows."""
    from canary.models.app.merchants import Merchant

    merchant_a = Merchant(
        source_merchant_id=f"test-rls-a-{uuid.uuid4().hex[:8]}",
        merchant_name="RLS Test A",
        currency="USD",
    )
    merchant_b = Merchant(
        source_merchant_id=f"test-rls-b-{uuid.uuid4().hex[:8]}",
        merchant_name="RLS Test B",
        currency="USD",
    )
    committed_app_session.add_all([merchant_a, merchant_b])
    committed_app_session.commit()

    txn_a_id = str(uuid.uuid4())
    txn_b_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)

    # Seed one transaction per merchant. See canary/models/sales/transactions.py
    # for the NOT NULL column set — we populate only what's required.
    for txn_id, mid in [(txn_a_id, merchant_a.id), (txn_b_id, merchant_b.id)]:
        committed_sales_session.execute(
            text(
                "INSERT INTO sales.transactions "
                "(id, merchant_id, external_id, source_type, location_id, "
                " transaction_type, transaction_date, amount_cents, currency) "
                "VALUES (:id, :mid, :ext, 'square', :loc, 'payment', "
                "        :tdate, 1234, 'USD')"
            ),
            {
                "id": txn_id,
                "mid": str(mid),
                "ext": f"ext-{txn_id[:8]}",
                "loc": f"loc-{txn_id[:8]}",
                "tdate": now,
            },
        )
    committed_sales_session.commit()

    try:
        sess = standalone_factory.get_session()

        # As merchant A: see A's txn, NOT B's
        token = set_merchant_context(str(merchant_a.id))
        try:
            ids_seen = [
                r[0] for r in sess.execute(
                    text(
                        "SELECT id FROM sales.transactions "
                        "WHERE id IN (:a, :b)"
                    ),
                    {"a": txn_a_id, "b": txn_b_id},
                ).fetchall()
            ]
            assert txn_a_id in [str(x) for x in ids_seen]
            assert txn_b_id not in [str(x) for x in ids_seen]
        finally:
            clear_merchant_context(token)
            sess.close()

        # As merchant B: see B's txn, NOT A's
        token = set_merchant_context(str(merchant_b.id))
        try:
            sess2 = standalone_factory.get_session()
            ids_seen = [
                r[0] for r in sess2.execute(
                    text(
                        "SELECT id FROM sales.transactions "
                        "WHERE id IN (:a, :b)"
                    ),
                    {"a": txn_a_id, "b": txn_b_id},
                ).fetchall()
            ]
            assert txn_b_id in [str(x) for x in ids_seen]
            assert txn_a_id not in [str(x) for x in ids_seen]
            sess2.close()
        finally:
            clear_merchant_context(token)

    finally:
        committed_sales_session.execute(
            text("DELETE FROM sales.transactions WHERE id IN (:a, :b)"),
            {"a": txn_a_id, "b": txn_b_id},
        )
        committed_sales_session.commit()
        committed_app_session.execute(
            text("DELETE FROM app.merchants WHERE id IN (:a, :b)"),
            {"a": str(merchant_a.id), "b": str(merchant_b.id)},
        )
        committed_app_session.commit()


# ---------------------------------------------------------------------------
# Test 4: Fail-closed when no merchant context is set
# ---------------------------------------------------------------------------

def test_rls_fails_closed_without_merchant_context(
    standalone_factory, committed_app_session, committed_sales_session,
    rls_policy_present,
):
    """Seed a row, bind NO merchant context, read sales.transactions →
    expect zero rows under RLS. A regression that defaults RLS to 'allow
    all when current_merchant is null' would surface here."""
    from canary.models.app.merchants import Merchant

    merchant = Merchant(
        source_merchant_id=f"test-failclosed-{uuid.uuid4().hex[:8]}",
        merchant_name="Fail-Closed Test",
        currency="USD",
    )
    committed_app_session.add(merchant)
    committed_app_session.commit()

    txn_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)

    committed_sales_session.execute(
        text(
            "INSERT INTO sales.transactions "
            "(id, merchant_id, external_id, source_type, location_id, "
            " transaction_type, transaction_date, amount_cents, currency) "
            "VALUES (:id, :mid, :ext, 'square', :loc, 'payment', "
            "        :tdate, 1234, 'USD')"
        ),
        {
            "id": txn_id,
            "mid": str(merchant.id),
            "ext": f"ext-{txn_id[:8]}",
            "loc": f"loc-{txn_id[:8]}",
            "tdate": now,
        },
    )
    committed_sales_session.commit()

    try:
        sess = standalone_factory.get_session()

        # Explicitly DO NOT set merchant context
        rows = sess.execute(
            text("SELECT id FROM sales.transactions WHERE id = :id"),
            {"id": txn_id},
        ).fetchall()

        assert len(rows) == 0, (
            "RLS fail-closed regression: query returned rows without "
            "a merchant context. The RLS policy may have changed to "
            "'allow all when current_merchant is null'."
        )

        sess.close()

    finally:
        committed_sales_session.execute(
            text("DELETE FROM sales.transactions WHERE id = :id"),
            {"id": txn_id},
        )
        committed_sales_session.commit()
        committed_app_session.execute(
            text("DELETE FROM app.merchants WHERE id = :id"),
            {"id": str(merchant.id)},
        )
        committed_app_session.commit()
```

- [ ] **Step 3: Run the integration tests**

Ensure the shared infra is up first:
```bash
cd ~/GrowDirect/devops && docker compose up -d
cd ~/GrowDirect/Canary
python3 -m pytest tests/integration/test_qa_agent_db.py -v -m postgres
```

Expected: all 4 tests PASS.

**If test 2 fails with an error other than NoneType** (e.g., `get_dashboard` demands a different input shape): inspect `canary/services/analytics/tools.py` for the actual required params and adjust the call. The test's job is to confirm NoneType is gone, not to assert a full dashboard payload.

**If test 4 fails** (rows returned when no merchant set): RLS policy on `canary_sales.transactions` is configured to allow reads when `current_merchant` is null. Verify the policy via `\d+ canary_sales.transactions` in psql. If the policy is intentionally permissive in the test database, the fix is to adjust the policy — this is a real security gap and should be filed as a new Linear issue before merging this chunk.

- [ ] **Step 4: Commit**

```bash
cd ~/GrowDirect/Canary
git add tests/integration/test_qa_agent_db.py
git commit -m "test(qa-agent): DB integration tests for standalone factory [GRO-389]

Covers: SELECT 1 via standalone session, get_dashboard via execute_tool
(no NoneType), cross-merchant RLS isolation, fail-closed on missing
merchant context."
```

---

### Task 3.2: Sidecar chat handler integration test

**Files:**
- Create: `Canary/tests/integration/test_qa_agent_chat.py`

We test `handle_chat()` directly instead of going through httpx's `ASGITransport`. `ASGITransport` (httpx 0.28+) does not drive ASGI lifespan events — `db.engine` would stay `None` and reproduce the GRO-389 symptom the test is trying to rule out. Calling `handle_chat` directly with an explicitly bootstrapped factory is cleaner, needs no new dependencies, and proves the same property (merchant extraction → set_merchant_context → tool dispatch → real DB data).

- [ ] **Step 1: Create the test file**

```python
"""Integration test for the QA Agent sidecar chat handler.

GRO-389: proves handle_chat(), with a bootstrapped standalone factory and
a merchant-prefixed message, routes a user question through Anthropic
(mocked) and dispatches a DB-backed tool against the real test database.

We call handle_chat directly — not through httpx's ASGITransport, which
does not drive ASGI lifespan events (so db.engine would stay None and
reproduce the bug we're testing the fix for).
"""

from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest

from canary.db.session_factory import DatabaseSessionFactory

pytestmark = pytest.mark.postgres


CANARY_DB_URL = os.getenv(
    "CANARY_DB_URL",
    "postgresql://canary:canary_dev_2026@localhost:5432/canary",
)


@pytest.fixture
def bootstrapped_sidecar(monkeypatch):
    """Set env and point the sidecar's module-level `db` at a fresh
    standalone factory. Mirrors what the ASGI lifespan handler does at
    container startup."""
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
def anthropic_two_turn_dashboard():
    """Mock anthropic.Anthropic: first turn returns a tool_use for
    get_dashboard; second turn returns a text final answer."""
    tool_use_block = MagicMock()
    tool_use_block.type = "tool_use"
    tool_use_block.name = "get_dashboard"
    tool_use_block.id = "toolu_test_1"
    tool_use_block.input = {}

    response_1 = MagicMock()
    response_1.content = [tool_use_block]

    text_block = MagicMock()
    text_block.type = "text"
    text_block.text = "Here's your dashboard summary from live data."

    response_2 = MagicMock()
    response_2.content = [text_block]

    mock_client = MagicMock()
    mock_client.messages.create.side_effect = [response_1, response_2]

    with patch("anthropic.Anthropic", return_value=mock_client) as mocked:
        yield mocked, mock_client


@pytest.mark.asyncio
async def test_sidecar_chat_handler_routes_dashboard_query(
    bootstrapped_sidecar, anthropic_two_turn_dashboard, test_merchant,
):
    """handle_chat with a merchant-prefixed message must:
      1. Extract the merchant UUID and bind ContextVar
      2. Call Anthropic (mocked — returns tool_use)
      3. Dispatch get_dashboard via execute_tool
      4. Call Anthropic again (mocked — returns final text)
      5. Return the synth text and populated tool_calls

    Failure path the GRO-389 bug produced: text contains "database
    connectivity issue" because execute_tool returned a NoneType error.
    """
    from canary.services.qa_agent.server import handle_chat

    payload = {
        "messages": [
            {
                "role": "user",
                "content": (
                    f"[Page: /chirps | Merchant: {test_merchant.id}] "
                    "how many alerts fired today?"
                ),
            }
        ],
        "session_id": "test-sidecar-handle-chat",
    }

    result = await handle_chat(payload)

    # Tool dispatch ran
    tool_names = [tc["tool"] for tc in result.get("tool_calls", [])]
    assert "get_dashboard" in tool_names, (
        f"Expected get_dashboard in tool_calls, got: {result.get('tool_calls')}"
    )

    # Final text came from the second Anthropic response, not the failure path
    text = result.get("text", "")
    assert "database connectivity issue" not in text.lower()
    assert "sidecar is not running" not in text.lower()
    assert "no merchant context" not in text.lower()


@pytest.mark.asyncio
async def test_sidecar_chat_handler_short_circuits_without_merchant(
    bootstrapped_sidecar, anthropic_two_turn_dashboard,
):
    """Without a Merchant: <uuid> prefix, handle_chat must short-circuit
    before calling Anthropic — no API tokens burned, no tool dispatch,
    no shared __no_merchant__ session bucket race."""
    from canary.services.qa_agent.server import handle_chat

    _, mock_client = anthropic_two_turn_dashboard

    result = await handle_chat({
        "messages": [{"role": "user", "content": "no merchant here"}],
        "session_id": "test-no-merchant",
    })

    assert "no merchant context" in result.get("text", "").lower()
    assert result.get("tool_calls") == []
    mock_client.messages.create.assert_not_called()
```

- [ ] **Step 2: Verify pytest-asyncio is available and configured**

Run: `cd ~/GrowDirect/Canary && python3 -c "import pytest_asyncio; print(pytest_asyncio.__version__)"`

If `ModuleNotFoundError`: **flag to the user before installing** — adding to `requirements-dev.txt` requires approval (per memory: "Flag dependency changes"). Approved addition:
```
pytest-asyncio>=0.23
```

Then check `pytest.ini` — it currently has no `asyncio_mode` setting. pytest-asyncio 1.x defaults to strict mode, which means explicit `@pytest.mark.asyncio` per test is required (already present in the tests above). No config change needed if using strict mode.

**If asyncio_mode needs setting** (you see "coroutine was never awaited" warnings): add to `pytest.ini`:
```
asyncio_mode = strict
```

- [ ] **Step 3: Run the tests**

```bash
cd ~/GrowDirect/Canary
python3 -m pytest tests/integration/test_qa_agent_chat.py -v -m postgres
```

Expected: 2 tests PASS.

**If the first test fails with the NoneType error**: the `bootstrapped_sidecar` fixture didn't rebind `sf_module.db` correctly, or `handle_chat` grabs `db.session` before the fixture's `init_standalone` runs. Verify the fixture's `sf_module.db = factory` assignment lands BEFORE handle_chat is imported in the test body.

**If the mock doesn't intercept `anthropic.Anthropic`**: the sidecar imports `Anthropic` inside `handle_chat` (see server.py:79 — `from anthropic import Anthropic`). Patching `anthropic.Anthropic` at the module level works because Python resolves the attribute at call time. If it breaks in future refactors that do `from anthropic import Anthropic` at module top, change the patch target to `canary.services.qa_agent.server.Anthropic`.

- [ ] **Step 4: Commit**

```bash
cd ~/GrowDirect/Canary
git add tests/integration/test_qa_agent_chat.py
git commit -m "test(qa-agent): handle_chat integration tests [GRO-389]

Two tests: happy-path tool dispatch through a mocked Anthropic client
(proves GRO-389 NoneType bug is gone), and missing-merchant short
circuit (proves no Anthropic call + clear error). Calls handle_chat
directly to sidestep httpx ASGITransport lack of lifespan support."
```

---

### Task 3.3: Completeness gate — end-to-end verification

This is per Canary CLAUDE.md "No Lazy Pipes" standard. Run before declaring the session done. No code changes — verification only.

- [ ] **Step 1: Start the full Canary stack**

```bash
cd ~/GrowDirect/devops && docker compose up -d
cd ~/GrowDirect/Canary/devops && docker compose up -d --build qa-agent flask
```

Wait for health: `docker ps` should show `canary_localhost_flask` and `canary_localhost_qa_agent` both healthy.

- [ ] **Step 2: Pre-count rows in sales.transactions for the test merchant**

Replace `<TEST_MERCHANT_UUID>` with a known sandbox merchant UUID (pull from `app.merchants`):

```bash
docker exec growdirect_postgres psql -U growdirect -d canary -c \
  "SELECT id, merchant_name FROM app.merchants ORDER BY created_at DESC LIMIT 5;"
```

Pick one; use its `id` for the rest of the gate. Record the pre-count:

```bash
docker exec growdirect_postgres psql -U growdirect -d canary -c \
  "SELECT count(*) FROM sales.transactions WHERE merchant_id = '<TEST_MERCHANT_UUID>';"
```

Record the count as `PRE_COUNT`.

- [ ] **Step 3: Data in — fire a scenario through the Flask chat endpoint**

Log into the ops console as an admin (magic link) and navigate to `/ops/qa`. Send the message:

```
[Page: /ops/qa | Merchant: <TEST_MERCHANT_UUID>] fire the high_velocity_refunds scenario
```

Expected: chat response confirms `fire_scenario` was called and returns a Square payment_id. Watch sidecar logs:
```bash
docker logs -f canary_localhost_qa_agent
```
Look for `QA Agent → MCP: fire_scenario(...)` — not a failure.

- [ ] **Step 4: Data out — ask for the dashboard**

Same chat session, send:
```
what's today's dashboard?
```

Expected: response contains real numbers (not "database connectivity issue"). `tool_calls` in the network response includes `get_dashboard`.

- [ ] **Step 5: Row count delta**

```bash
docker exec growdirect_postgres psql -U growdirect -d canary -c \
  "SELECT count(*) FROM sales.transactions WHERE merchant_id = '<TEST_MERCHANT_UUID>';"
```

Expected: count is `PRE_COUNT + 1` (one new transaction from the scenario fire). If zero delta, the scenario fired but ingestion didn't land — this is a separate pipeline issue, not a QA Agent DB fix regression. File separately.

- [ ] **Step 6: Route-level curl verification — sidecar directly**

Hitting the Flask endpoint requires a login cookie (admin-gated). Easier: hit the sidecar directly on port 8002. This proves the DB fix end-to-end without auth plumbing.

```bash
curl -s -X POST http://localhost:8002/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{
      "role": "user",
      "content": "[Page: /ops/qa | Merchant: <TEST_MERCHANT_UUID>] what are my top risks?"
    }],
    "session_id": "gate-verification"
  }' | python3 -m json.tool
```

Expected: 200 response with `text` containing real analysis, `tool_calls` populated. `"database connectivity issue"` must NOT appear in the text. `"no merchant context"` must NOT appear (the Merchant: prefix is present).

Then confirm the Flask path is wired — log into `/ops/qa` in a browser and send one message with the same merchant prefix. Response should match the curl output pattern.

- [ ] **Step 7: Log the gate results in Linear**

Post a comment on GRO-389 with:
- The PRE_COUNT and POST_COUNT with delta
- The sidecar log line showing `QA Agent → MCP: fire_scenario`
- The `tool_calls` content from step 6 (redact merchant UUID if sharing publicly)

---

### Task 3.4: Linear closeout

No code changes — use the Linear MCP.

- [ ] **Step 1: Close GRO-388 as duplicate of GRO-389**

Use the Linear MCP `save_issue` tool (or Linear UI) to set GRO-388 status → Canceled, add comment: "Duplicate of GRO-389 — filed 7s apart on 2026-04-01. Fix landed on main; see GRO-389 for the closing commit."

- [ ] **Step 2: Close GRO-389**

Set status → Done. Post closing comment linking to the commits from Chunks 1–3 and a one-liner from the completeness gate (row count delta). Include git commit SHAs.

- [ ] **Step 3: Update GRO-326 description**

Edit the description to check off the Tier 0 acceptance list:
- [x] Chat page loads — was already working
- [x] Claude responds with Canary context — was already working
- [x] Can invoke tools (fix_scenario, atlas_figure, get_dashboard, etc.) — **now working after GRO-389**
- [x] Conversation persists across messages in session — was already working

Add a note: "Tier 0 complete as of <date>. Tier 1 (Linear bug filing, Atlas inline rendering) queued as follow-up." Correct the `sandbox_fire` → `fire_scenario` naming in the acceptance copy while you're there.

- [ ] **Step 4: File two follow-up issues**

New Linear issue: **"QA Agent port discrepancy — CLAUDE.md says 8004, Dockerfile/server use 8002"** (P3). One-line repro: `grep QA_AGENT_PORT devops/docker-compose.localhost.yml` vs root CLAUDE.md port table. Fix is a doc/config reconciliation, not code.

New Linear issue: **"QA Agent Tier 1 — Linear bug filing + Atlas inline rendering"** (P2), link parent GRO-326. This is the next logical chunk after Tier 0.

---

## Verification Checklist (end of session)

Before claiming this plan is done, confirm:

- [ ] All 5 unit tests pass (`pytest tests/unit/test_session_factory_standalone.py`)
- [ ] All 4 DB integration tests pass (`pytest tests/integration/test_qa_agent_db.py -m postgres`)
- [ ] The 1 chat integration test passes (`pytest tests/integration/test_qa_agent_chat.py -m postgres`)
- [ ] Full unit suite has no regressions (`pytest tests/unit/`)
- [ ] Completeness gate 4 points all pass (data in, data out, row count delta, route responds)
- [ ] `.guardian-manifest` updated with new SHA256 for `canary/db/session_factory.py`
- [ ] GRO-388 closed as duplicate; GRO-389 closed with commit links; GRO-326 description updated
- [ ] Two follow-up Linear issues filed (port discrepancy, Tier 1 scope)

## Commit Trail Expected

1. `test(session-factory): scaffold standalone unit tests [GRO-389]`
2. `test(session-factory): add 5 failing standalone tests [GRO-389]`
3. `fix(db): add ContextVar RLS channel + init_standalone [GRO-389]`
4. `feat(qa-agent): bootstrap DB factory via ASGI lifespan [GRO-389]`
5. `feat(qa-agent): bind merchant RLS context per chat request [GRO-389]`
6. `test(qa-agent): DB integration tests for standalone factory [GRO-389]`
7. `test(qa-agent): sidecar /chat endpoint integration test [GRO-389]`

All seven commits should land bisectably — each commit compiles, each test commit fails only for the symbol it's exercising that's added in the next commit, each fix commit makes its target test pass without breaking earlier tests.

## Skills to Invoke During Execution

- `@superpowers:test-driven-development` — each test task writes the failing test first, then the implementation
- `@superpowers:verification-before-completion` — run the verification checklist before claiming done
- `@superpowers:receiving-code-review` — if a reviewer flags issues, follow this skill's rigor

## Risks Called Out in Spec (for implementer awareness)

- Silent non-DB tool failures still look like the old bug — watch sidecar logs for `MCP tool ... failed` during the gate
- Single-worker uvicorn constraint — documented; if anyone changes `Dockerfile.qa-agent` to add `--workers N`, the fix breaks
- ContextVar per-asyncio-task — if tool handlers ever spawn threads, merchant binding won't propagate
