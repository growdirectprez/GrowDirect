# MCP Consolidation Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish the official `mcp` Python SDK as the platform standard, extract ALX to platform level, and address all known MCP architectural findings from the SDD audit.

**Architecture:** Platform MCP package (`services/growdirect-mcp/`) wraps the official `mcp` SDK with GrowDirect conventions. Cove MCP refactored to use it as reference implementation. Memory Bus gets a full sweep (auth, Alembic, indexes, FK, cleanup). ALX entries removed from Canary server maps. All affected SDDs updated.

**Tech Stack:** Python 3.12, `mcp` SDK (>=1.0), SQLAlchemy 2.0, Alembic, pgvector, pytest, FastMCP

**Spec:** `docs/superpowers/specs/2026-03-30-mcp-consolidation-design.md`

---

## File Structure

### New Files

| File | Responsibility |
|------|---------------|
| `services/growdirect-mcp/pyproject.toml` | Package metadata, `mcp` SDK dependency |
| `services/growdirect-mcp/growdirect_mcp/__init__.py` | Public exports: `GrowDirectRegistry`, `GrowDirectTool` |
| `services/growdirect-mcp/growdirect_mcp/registry.py` | SDK `Server` wrapper with tool registration + context injection |
| `services/growdirect-mcp/growdirect_mcp/tool.py` | SDK `Tool` wrapper with response envelope + error handling |
| `services/growdirect-mcp/growdirect_mcp/auth.py` | API key + JWT auth middleware |
| `services/growdirect-mcp/growdirect_mcp/bridge.py` | Stdio-HTTP bridge for IDE integration |
| `services/growdirect-mcp/tests/test_tool.py` | GrowDirectTool unit tests |
| `services/growdirect-mcp/tests/test_registry.py` | GrowDirectRegistry unit tests |
| `services/growdirect-mcp/tests/test_auth.py` | Auth middleware unit tests |
| `services/growdirect-mcp/tests/test_bridge.py` | Bridge integration tests |
| `services/memory-bus/migrations/env.py` | Alembic environment config |
| `services/memory-bus/migrations/versions/001_baseline.py` | Baseline DDL migration |
| `services/memory-bus/migrations/versions/002_drop_seed_embeddings.py` | Drop unused table |
| `services/memory-bus/migrations/versions/003_hnsw_index.py` | Add vector index |
| `services/memory-bus/migrations/versions/004_session_fk.py` | Fix orphans + add FK |
| `services/memory-bus/tests/test_store.py` | Replacement tests for misplaced ones |
| `services/alx/__init__.py` | ALX platform service marker |
| `docs/decisions/2026-03-30-mcp-sdk-platform-standard.md` | ADR |

### Modified Files

| File | Change |
|------|--------|
| `Cove/cove/mcp/server.py` | Replace hardcoded TOOLS + if/elif with GrowDirectRegistry |
| `Cove/requirements.txt` | Add `growdirect-mcp` dependency |
| `Canary/canary/mcp/streamable_server.py` | Remove `"alx"` from SERVER_PREFIXES |
| `services/memory-bus/memory_bus/server.py` | Add auth middleware |
| `services/memory-bus/memory_bus/config.py` | Add `mcp_api_key` field |
| `services/memory-bus/memory_bus/store.py` | Add session existence check before memory writes |
| `services/memory-bus/scripts/seed_clean.py` | Create session before writing memories |
| `services/memory-bus/pyproject.toml` | Add `alembic` dependency |
| `devops/init-db/02-create-memory-db.sql` | Strip table DDL (keep DB + extensions only) |
| `devops/docker-compose.yml` | Add `MCP_API_KEY` env var to memory-bus service |

### Deleted Files

| File | Reason |
|------|--------|
| `services/memory-bus/tests/test_context_blocks.py` | Imports from `canary.services.alx.memory` — wrong codebase |
| `services/memory-bus/tests/test_rag_retrieval.py` | Imports from `canary.services.alx.memory` — wrong codebase |

### Moved Files

| From | To | Reason |
|------|----|--------|
| `docs/sdds/alx/qa-agent.md` | `docs/sdds/canary/qa-agent.md` | App-level, not ALX |

---

## Chunk 1: Platform MCP Package

Tasks 1–5 create `services/growdirect-mcp/` — the shared platform package wrapping the `mcp` SDK.

### Task 1: Package Skeleton

**Files:**
- Create: `services/growdirect-mcp/pyproject.toml`
- Create: `services/growdirect-mcp/growdirect_mcp/__init__.py`

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p services/growdirect-mcp/growdirect_mcp services/growdirect-mcp/tests
```

- [ ] **Step 2: Write pyproject.toml**

```toml
[project]
name = "growdirect-mcp"
version = "0.1.0"
description = "GrowDirect platform MCP SDK wrapper — shared conventions for all app MCP servers"
requires-python = ">=3.12"
dependencies = [
    "mcp>=1.0",
    "httpx>=0.27",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.24",
]

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"
```

- [ ] **Step 3: Write __init__.py**

```python
"""GrowDirect Platform MCP SDK — shared conventions for all app MCP servers."""

from growdirect_mcp.tool import GrowDirectTool
from growdirect_mcp.registry import GrowDirectRegistry

__all__ = ["GrowDirectTool", "GrowDirectRegistry"]
```

- [ ] **Step 4: Verify package installs**

```bash
cd services/growdirect-mcp && pip install -e ".[dev]"
```

Expected: Installs successfully (will fail on missing modules — that's fine, we just need the package metadata to resolve).

- [ ] **Step 5: Commit**

```bash
git add services/growdirect-mcp/pyproject.toml services/growdirect-mcp/growdirect_mcp/__init__.py
git commit -m "feat: scaffold growdirect-mcp platform package"
```

---

### Task 2: GrowDirectTool

**Files:**
- Create: `services/growdirect-mcp/tests/test_tool.py`
- Create: `services/growdirect-mcp/growdirect_mcp/tool.py`

- [ ] **Step 1: Write failing tests**

```python
"""Tests for GrowDirectTool — SDK Tool wrapper with response envelope."""

import json
import pytest
from growdirect_mcp.tool import GrowDirectTool


def test_tool_creates_with_required_fields():
    tool = GrowDirectTool(
        name="test_tool",
        description="A test tool",
        handler=lambda params, context: {"result": "ok"},
        input_schema={
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    )
    assert tool.name == "test_tool"
    assert tool.description == "A test tool"
    assert tool.category == "general"


def test_tool_creates_with_category():
    tool = GrowDirectTool(
        name="test_tool",
        description="A test tool",
        handler=lambda params, context: {"result": "ok"},
        input_schema={"type": "object", "properties": {}},
        category="search",
    )
    assert tool.category == "search"


@pytest.mark.asyncio
async def test_invoke_returns_envelope_on_success():
    def handler(params, context):
        return {"data": params["query"]}

    tool = GrowDirectTool(
        name="test_tool",
        description="A test tool",
        handler=handler,
        input_schema={"type": "object", "properties": {"query": {"type": "string"}}},
    )
    result = await tool.invoke({"query": "hello"}, {"user_id": "u1"})
    assert result["ok"] is True
    assert result["result"]["data"] == "hello"
    assert result["tool"] == "test_tool"
    assert "timestamp" in result


@pytest.mark.asyncio
async def test_invoke_returns_envelope_on_handler_error_key():
    def handler(params, context):
        return {"error": "not found"}

    tool = GrowDirectTool(
        name="test_tool",
        description="A test tool",
        handler=handler,
        input_schema={"type": "object", "properties": {}},
    )
    result = await tool.invoke({}, {})
    assert result["ok"] is False
    assert result["error"] == "not found"


@pytest.mark.asyncio
async def test_invoke_returns_envelope_on_exception():
    def handler(params, context):
        raise ValueError("boom")

    tool = GrowDirectTool(
        name="test_tool",
        description="A test tool",
        handler=handler,
        input_schema={"type": "object", "properties": {}},
    )
    result = await tool.invoke({}, {})
    assert result["ok"] is False
    assert "boom" in result["error"]


def test_to_mcp_returns_sdk_tool():
    tool = GrowDirectTool(
        name="test_tool",
        description="A test tool",
        handler=lambda p, c: {"result": "ok"},
        input_schema={"type": "object", "properties": {"q": {"type": "string"}}},
    )
    mcp_tool = tool.to_mcp()
    assert mcp_tool.name == "test_tool"
    assert mcp_tool.description == "A test tool"
    assert mcp_tool.inputSchema["properties"]["q"]["type"] == "string"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd services/growdirect-mcp && python3 -m pytest tests/test_tool.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'growdirect_mcp.tool'`

- [ ] **Step 3: Implement GrowDirectTool**

```python
"""GrowDirectTool — SDK Tool wrapper with response envelope and error handling."""

import asyncio
import logging
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Any, Callable

from mcp.types import Tool

logger = logging.getLogger(__name__)


@dataclass
class GrowDirectTool:
    """Wraps the MCP SDK Tool with GrowDirect conventions.

    Handler signature: def handler(params: dict, context: dict) -> dict
    - Return {"error": "msg"} for logical failures (ok=False)
    - Return any other dict for success (ok=True, wrapped in result)
    - Exceptions are caught and wrapped as ok=False
    """

    name: str
    description: str
    handler: Callable[[dict, dict], dict]
    input_schema: dict
    category: str = "general"

    async def invoke(
        self, params: dict[str, Any], context: dict[str, Any]
    ) -> dict[str, Any]:
        """Execute handler and wrap in standard response envelope."""
        try:
            result = self.handler(params, context)
            if asyncio.iscoroutine(result):
                result = await result

            if isinstance(result, dict) and "error" in result:
                return {
                    "tool": self.name,
                    "ok": False,
                    "error": result["error"],
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }

            return {
                "tool": self.name,
                "ok": True,
                "result": result,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            logger.exception("Tool %s raised exception", self.name)
            return {
                "tool": self.name,
                "ok": False,
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    def to_mcp(self) -> Tool:
        """Convert to SDK Tool for MCP protocol registration."""
        return Tool(
            name=self.name,
            description=self.description,
            inputSchema=self.input_schema,
        )
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd services/growdirect-mcp && python3 -m pytest tests/test_tool.py -v
```

Expected: All 6 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add services/growdirect-mcp/growdirect_mcp/tool.py services/growdirect-mcp/tests/test_tool.py
git commit -m "feat: GrowDirectTool — SDK Tool wrapper with response envelope"
```

---

### Task 3: GrowDirectRegistry

**Files:**
- Create: `services/growdirect-mcp/tests/test_registry.py`
- Create: `services/growdirect-mcp/growdirect_mcp/registry.py`

- [ ] **Step 1: Write failing tests**

```python
"""Tests for GrowDirectRegistry — SDK Server wrapper with tool registration."""

import json
import pytest
from mcp.types import TextContent
from growdirect_mcp.registry import GrowDirectRegistry
from growdirect_mcp.tool import GrowDirectTool


@pytest.fixture
def registry():
    reg = GrowDirectRegistry(
        server_name="test-server",
        version="0.1.0",
        description="Test server",
    )
    reg.register(GrowDirectTool(
        name="echo",
        description="Echo back the input",
        handler=lambda params, context: {"echo": params.get("msg", "")},
        input_schema={
            "type": "object",
            "properties": {"msg": {"type": "string"}},
        },
    ))
    reg.register(GrowDirectTool(
        name="fail",
        description="Always fails",
        handler=lambda params, context: {"error": "nope"},
        input_schema={"type": "object", "properties": {}},
    ))
    return reg


def test_register_and_list_tools(registry):
    names = registry.tool_names()
    assert "echo" in names
    assert "fail" in names
    assert len(names) == 2


def test_get_tool(registry):
    tool = registry.get("echo")
    assert tool is not None
    assert tool.name == "echo"


def test_get_nonexistent_returns_none(registry):
    assert registry.get("nonexistent") is None


def test_list_tools_returns_mcp_format(registry):
    tools = registry.list_tools()
    assert len(tools) == 2
    assert all(t.name in ("echo", "fail") for t in tools)


def test_manifest(registry):
    manifest = registry.get_manifest()
    assert manifest["server_name"] == "test-server"
    assert manifest["version"] == "0.1.0"
    assert len(manifest["tools"]) == 2


@pytest.mark.asyncio
async def test_dispatch_calls_tool(registry):
    result = await registry.dispatch("echo", {"msg": "hello"}, {"user_id": "u1"})
    parsed = json.loads(result[0].text)
    assert parsed["ok"] is True
    assert parsed["result"]["echo"] == "hello"


@pytest.mark.asyncio
async def test_dispatch_unknown_tool(registry):
    result = await registry.dispatch("nope", {}, {})
    parsed = json.loads(result[0].text)
    assert parsed["ok"] is False
    assert "Unknown tool" in parsed["error"]


def test_contains(registry):
    assert "echo" in registry
    assert "nope" not in registry


def test_len(registry):
    assert len(registry) == 2
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd services/growdirect-mcp && python3 -m pytest tests/test_registry.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'growdirect_mcp.registry'`

- [ ] **Step 3: Implement GrowDirectRegistry**

```python
"""GrowDirectRegistry — SDK Server wrapper with tool registration and dispatch."""

import json
import logging
from typing import Any, Optional

from mcp.server import Server
from mcp.types import TextContent, Tool

from growdirect_mcp.tool import GrowDirectTool

logger = logging.getLogger(__name__)


class GrowDirectRegistry:
    """Registry of MCP tools for a single server.

    Wraps the SDK Server class with:
    - Tool registration via GrowDirectTool instances
    - Context injection (merchant_id, org_id, user_id)
    - Standard dispatch with response envelope
    - Manifest generation for discovery
    """

    def __init__(self, server_name: str, version: str, description: str):
        self.server_name = server_name
        self.version = version
        self.description = description
        self._tools: dict[str, GrowDirectTool] = {}

    def register(self, tool: GrowDirectTool) -> None:
        """Register a tool. Raises ValueError on duplicate name."""
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' already registered")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[GrowDirectTool]:
        """Look up a tool by name."""
        return self._tools.get(name)

    def tool_names(self) -> list[str]:
        """List all registered tool names."""
        return list(self._tools.keys())

    def list_tools(self) -> list[Tool]:
        """Return SDK Tool objects for MCP protocol."""
        return [t.to_mcp() for t in self._tools.values()]

    def get_manifest(self) -> dict[str, Any]:
        """Full server manifest for discovery."""
        return {
            "server_name": self.server_name,
            "version": self.version,
            "description": self.description,
            "tools": [
                {
                    "name": t.name,
                    "description": t.description,
                    "category": t.category,
                    "input_schema": t.input_schema,
                }
                for t in self._tools.values()
            ],
        }

    async def dispatch(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        context: dict[str, Any],
    ) -> list[TextContent]:
        """Dispatch a tool call and return MCP TextContent response."""
        tool = self.get(tool_name)
        if tool is None:
            error_envelope = {
                "tool": tool_name,
                "ok": False,
                "error": f"Unknown tool: {tool_name}",
            }
            return [TextContent(type="text", text=json.dumps(error_envelope))]

        result = await tool.invoke(arguments, context)
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2, default=str),
        )]

    def build_server(self) -> Server:
        """Create an MCP Server wired to this registry's tools.

        Returns a Server instance with list_tools and call_tool handlers
        registered. The caller is responsible for running the server
        with the appropriate transport (stdio, HTTP, etc).
        """
        server = Server(self.server_name)
        registry = self  # capture for closures

        @server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            return registry.list_tools()

        @server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict
        ) -> list[TextContent]:
            return await registry.dispatch(name, arguments, {})

        return server

    def __contains__(self, name: str) -> bool:
        return name in self._tools

    def __len__(self) -> int:
        return len(self._tools)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd services/growdirect-mcp && python3 -m pytest tests/test_registry.py -v
```

Expected: All 9 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add services/growdirect-mcp/growdirect_mcp/registry.py services/growdirect-mcp/tests/test_registry.py
git commit -m "feat: GrowDirectRegistry — SDK Server wrapper with tool registration"
```

---

### Task 4: Auth Middleware

**Files:**
- Create: `services/growdirect-mcp/tests/test_auth.py`
- Create: `services/growdirect-mcp/growdirect_mcp/auth.py`

- [ ] **Step 1: Write failing tests**

```python
"""Tests for auth middleware — API key, JWT validation, and no-auth opt-in."""

import os
import pytest
from growdirect_mcp.auth import validate_api_key, validate_jwt, AuthError


# --- API key tests ---

def test_validate_api_key_passes_with_correct_key(monkeypatch):
    monkeypatch.setenv("MCP_API_KEY", "test-secret-key")
    assert validate_api_key("test-secret-key") is True


def test_validate_api_key_raises_on_wrong_key(monkeypatch):
    monkeypatch.setenv("MCP_API_KEY", "test-secret-key")
    with pytest.raises(AuthError, match="Invalid API key"):
        validate_api_key("wrong-key")


def test_validate_api_key_raises_on_missing_key(monkeypatch):
    monkeypatch.setenv("MCP_API_KEY", "test-secret-key")
    with pytest.raises(AuthError, match="API key required"):
        validate_api_key(None)


def test_validate_api_key_raises_on_empty_key(monkeypatch):
    monkeypatch.setenv("MCP_API_KEY", "test-secret-key")
    with pytest.raises(AuthError, match="API key required"):
        validate_api_key("")


# --- No-auth opt-in (must be explicit) ---

def test_validate_api_key_rejects_when_no_env_key(monkeypatch):
    """Default is secure: if MCP_API_KEY is not set, reject all calls."""
    monkeypatch.delenv("MCP_API_KEY", raising=False)
    monkeypatch.delenv("MCP_AUTH_DISABLED", raising=False)
    with pytest.raises(AuthError, match="MCP_API_KEY not configured"):
        validate_api_key("any-key")


def test_validate_api_key_allows_when_auth_explicitly_disabled(monkeypatch):
    """No-auth mode requires explicit opt-in via MCP_AUTH_DISABLED=1."""
    monkeypatch.delenv("MCP_API_KEY", raising=False)
    monkeypatch.setenv("MCP_AUTH_DISABLED", "1")
    assert validate_api_key(None) is True


# --- JWT tests ---

def test_validate_jwt_passes_with_valid_token(monkeypatch):
    monkeypatch.setenv("MCP_JWT_SECRET", "test-jwt-secret")
    import jwt
    token = jwt.encode({"sub": "service-a", "iss": "growdirect"}, "test-jwt-secret", algorithm="HS256")
    claims = validate_jwt(token)
    assert claims["sub"] == "service-a"


def test_validate_jwt_raises_on_invalid_token(monkeypatch):
    monkeypatch.setenv("MCP_JWT_SECRET", "test-jwt-secret")
    with pytest.raises(AuthError, match="Invalid JWT"):
        validate_jwt("garbage-token")


def test_validate_jwt_raises_when_no_secret(monkeypatch):
    monkeypatch.delenv("MCP_JWT_SECRET", raising=False)
    with pytest.raises(AuthError, match="JWT validation not configured"):
        validate_jwt("any-token")
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd services/growdirect-mcp && python3 -m pytest tests/test_auth.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'growdirect_mcp.auth'`

- [ ] **Step 3: Implement auth middleware**

```python
"""Auth middleware — API key and JWT validation for MCP transports.

Security model:
- Default is SECURE: if MCP_API_KEY is not set, all calls are rejected.
- No-auth mode requires explicit opt-in via MCP_AUTH_DISABLED=1 (trusted Docker network only).
- JWT validation for inter-service calls (optional, requires MCP_JWT_SECRET).
"""

import os
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class AuthError(Exception):
    """Raised when authentication fails."""
    pass


def validate_api_key(provided_key: Optional[str]) -> bool:
    """Validate an API key against MCP_API_KEY env var.

    If MCP_AUTH_DISABLED=1, auth is bypassed (explicit opt-in for trusted networks).
    If MCP_API_KEY is not set and auth is not disabled, reject all calls.
    If MCP_API_KEY is set, the provided key must match exactly.
    """
    # Explicit no-auth opt-in for trusted Docker network
    if os.environ.get("MCP_AUTH_DISABLED", "").strip() == "1":
        return True

    expected_key = os.environ.get("MCP_API_KEY", "").strip()

    if not expected_key:
        raise AuthError("MCP_API_KEY not configured — set it or use MCP_AUTH_DISABLED=1 for trusted networks")

    if not provided_key:
        raise AuthError("API key required — set X-API-Key header or MCP_API_KEY param")

    if provided_key != expected_key:
        raise AuthError("Invalid API key")

    return True


def validate_jwt(token: str) -> dict[str, Any]:
    """Validate a JWT for inter-service calls.

    Requires MCP_JWT_SECRET env var. Returns decoded claims on success.
    """
    import jwt as pyjwt

    secret = os.environ.get("MCP_JWT_SECRET", "").strip()
    if not secret:
        raise AuthError("JWT validation not configured — set MCP_JWT_SECRET")

    try:
        claims = pyjwt.decode(token, secret, algorithms=["HS256"])
        return claims
    except pyjwt.InvalidTokenError as e:
        raise AuthError(f"Invalid JWT: {e}") from e
```

Note: Add `"PyJWT>=2.8"` to `[project].dependencies` in `pyproject.toml` (runtime dependency, not dev-only).

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd services/growdirect-mcp && python3 -m pytest tests/test_auth.py -v
```

Expected: All 9 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add services/growdirect-mcp/growdirect_mcp/auth.py services/growdirect-mcp/tests/test_auth.py
git commit -m "feat: auth middleware — API key validation for MCP transports"
```

---

### Task 5: Stdio-HTTP Bridge

**Files:**
- Create: `services/growdirect-mcp/growdirect_mcp/bridge.py`
- Create: `services/growdirect-mcp/tests/test_bridge.py`

**Context:** This replaces `Canary/canary/mcp/streamable_server.py`. It discovers tools from SDK-based servers only (Memory Bus, Cove). Uses the SDK's native stdio transport.

- [ ] **Step 1: Write failing tests**

```python
"""Tests for the stdio-HTTP bridge — IDE tool discovery across platform servers."""

import json
import pytest
from unittest.mock import patch, MagicMock
from growdirect_mcp.bridge import ServerConfig, discover_servers, build_bridge_registry


def test_server_config_creation():
    config = ServerConfig(
        name="memory-bus",
        base_url="http://localhost:8003",
        transport="http",
    )
    assert config.name == "memory-bus"
    assert config.base_url == "http://localhost:8003"


def test_discover_servers_reads_from_env(monkeypatch):
    monkeypatch.setenv(
        "MCP_BRIDGE_SERVERS",
        json.dumps([
            {"name": "memory-bus", "base_url": "http://localhost:8003", "transport": "http"},
            {"name": "cove-knowledge", "base_url": "stdio://cove.mcp.server", "transport": "stdio"},
        ]),
    )
    servers = discover_servers()
    assert len(servers) == 2
    assert servers[0].name == "memory-bus"
    assert servers[1].name == "cove-knowledge"


def test_discover_servers_returns_empty_when_no_env(monkeypatch):
    monkeypatch.delenv("MCP_BRIDGE_SERVERS", raising=False)
    servers = discover_servers()
    assert servers == []


def test_build_bridge_registry_discovers_http_tools(monkeypatch):
    """Bridge fetches /manifest from HTTP servers and registers proxy tools."""
    from unittest.mock import MagicMock, patch
    manifest = {
        "server_name": "memory-bus",
        "tools": [
            {"name": "memory_store", "description": "Store a memory", "input_schema": {"type": "object", "properties": {}}, "category": "memory"},
            {"name": "memory_recall", "description": "Recall memories", "input_schema": {"type": "object", "properties": {}}, "category": "memory"},
        ],
    }
    mock_resp = MagicMock()
    mock_resp.json.return_value = manifest
    mock_resp.raise_for_status = MagicMock()

    with patch("growdirect_mcp.bridge.httpx") as mock_httpx:
        mock_httpx.get.return_value = mock_resp
        servers = [ServerConfig(name="memory-bus", base_url="http://localhost:8003", transport="http")]
        bridge = build_bridge_registry(servers)
        assert len(bridge) == 2
        assert "memory-bus:memory_store" in bridge
        assert "memory-bus:memory_recall" in bridge
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd services/growdirect-mcp && python3 -m pytest tests/test_bridge.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'growdirect_mcp.bridge'`

- [ ] **Step 3: Implement bridge**

```python
"""Stdio-HTTP bridge — IDE tool discovery across platform MCP servers.

Replaces Canary's streamable_server.py. Discovers tools from SDK-based
servers only (Memory Bus, Cove Knowledge). Canary's custom framework
servers are not discoverable until Canary is retrofitted to the SDK.

Usage:
    python3 -m growdirect_mcp.bridge

    Or via MCP_BRIDGE_SERVERS env var:
    MCP_BRIDGE_SERVERS='[{"name":"memory-bus","base_url":"http://localhost:8003","transport":"http"}]'
"""

import json
import logging
import os
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ServerConfig:
    """Configuration for a discoverable MCP server."""
    name: str
    base_url: str
    transport: str = "http"
    api_key: Optional[str] = None


def discover_servers() -> list[ServerConfig]:
    """Read server configurations from MCP_BRIDGE_SERVERS env var.

    Returns empty list if env var is not set.

    Format: JSON array of objects with name, base_url, transport, api_key (optional).
    """
    raw = os.environ.get("MCP_BRIDGE_SERVERS", "").strip()
    if not raw:
        return []

    try:
        configs = json.loads(raw)
        return [ServerConfig(**c) for c in configs]
    except (json.JSONDecodeError, TypeError) as e:
        logger.error("Failed to parse MCP_BRIDGE_SERVERS: %s", e)
        return []


def build_bridge_registry(servers: list[ServerConfig]):
    """Build a unified registry from multiple server configs.

    For HTTP servers: fetches manifest endpoint and creates proxy tools.
    For stdio servers: registers server metadata for subprocess dispatch.

    Discovery is real — each HTTP server's /manifest endpoint is queried
    and its tools are registered as proxy entries in the bridge registry.
    Full proxied invocation (forwarding tool calls to the origin server)
    will be expanded during the Canary retrofit spec.
    """
    import httpx
    from growdirect_mcp.registry import GrowDirectRegistry
    from growdirect_mcp.tool import GrowDirectTool

    bridge = GrowDirectRegistry(
        server_name="growdirect-bridge",
        version="0.1.0",
        description="Platform MCP bridge — unified tool discovery across all servers",
    )

    for server in servers:
        if server.transport == "http":
            try:
                headers = {"X-API-Key": server.api_key} if server.api_key else {}
                resp = httpx.get(f"{server.base_url}/manifest", headers=headers, timeout=5.0)
                resp.raise_for_status()
                manifest = resp.json()
                for tool_info in manifest.get("tools", []):
                    bridge.register(GrowDirectTool(
                        name=f"{server.name}:{tool_info['name']}",
                        description=f"[{server.name}] {tool_info.get('description', '')}",
                        handler=lambda p, c, _url=server.base_url, _name=tool_info["name"]: {
                            "proxy": True, "server": _url, "tool": _name,
                        },
                        input_schema=tool_info.get("input_schema", {"type": "object", "properties": {}}),
                        category=tool_info.get("category", "general"),
                    ))
                logger.info("Discovered %d tools from %s", len(manifest.get("tools", [])), server.name)
            except Exception as e:
                logger.warning("Failed to discover tools from %s: %s", server.name, e)
        else:
            logger.info("Registered stdio server: %s (discovery deferred to runtime)", server.name)

    return bridge
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd services/growdirect-mcp && python3 -m pytest tests/test_bridge.py -v
```

Expected: All 3 tests PASS.

- [ ] **Step 5: Run full test suite**

```bash
cd services/growdirect-mcp && python3 -m pytest tests/ -v
```

Expected: All 28 tests PASS (6 tool + 9 registry + 9 auth + 4 bridge).

- [ ] **Step 6: Commit**

```bash
git add services/growdirect-mcp/growdirect_mcp/bridge.py services/growdirect-mcp/tests/test_bridge.py
git commit -m "feat: stdio-HTTP bridge — IDE tool discovery across platform servers"
```

---

## Chunk 2: Memory Bus Full Sweep

Tasks 6–12 address all Section 11 findings for `services/memory-bus/`.

### Task 6: Alembic Init + Baseline Migration

**Files:**
- Create: `services/memory-bus/alembic.ini`
- Create: `services/memory-bus/migrations/env.py`
- Create: `services/memory-bus/migrations/script.py.mako`
- Create: `services/memory-bus/migrations/versions/001_baseline.py`
- Modify: `services/memory-bus/pyproject.toml`

**Context:** Currently `growdirect_memory` tables are created by raw SQL in `devops/init-db/02-create-memory-db.sql`. We're bringing it under Alembic. The baseline migration captures the current DDL (pre-fix state).

- [ ] **Step 1: Add alembic dependency**

In `services/memory-bus/pyproject.toml`, add `"alembic>=1.13"` to the dependencies list.

- [ ] **Step 2: Initialize Alembic**

```bash
cd services/memory-bus && python3 -m alembic init migrations
```

- [ ] **Step 3: Configure alembic.ini**

Set `sqlalchemy.url` to empty (will be overridden by env.py):

```ini
[alembic]
script_location = migrations
sqlalchemy.url =
```

- [ ] **Step 4: Write env.py**

```python
"""Alembic environment for growdirect_memory database."""

import os
from alembic import context
from sqlalchemy import create_engine

config = context.config
database_url = os.environ.get(
    "DATABASE_URL",
    "postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/growdirect_memory",
)


def run_migrations_online():
    engine = create_engine(database_url)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=None)
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
```

- [ ] **Step 5: Write baseline migration**

This captures the current DDL from `02-create-memory-db.sql` — the 3 tables as they exist today (including `seed_embeddings`). This is the stamp point for existing dev environments.

```python
"""001 — baseline: capture current growdirect_memory DDL.

Revision ID: 001_baseline
Create Date: 2026-03-30
"""

from alembic import op

revision = "001_baseline"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    CREATE TABLE IF NOT EXISTS alx_sessions (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        session_id TEXT UNIQUE NOT NULL,
        started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        closed_at TIMESTAMPTZ,
        status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'closed', 'abandoned')),
        gro_issues JSONB DEFAULT '[]',
        summary TEXT,
        decisions JSONB DEFAULT '[]',
        unresolved JSONB DEFAULT '[]',
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
    CREATE INDEX IF NOT EXISTS idx_sessions_status ON alx_sessions(status);
    CREATE INDEX IF NOT EXISTS idx_sessions_started ON alx_sessions(started_at DESC);

    CREATE TABLE IF NOT EXISTS alx_memories (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        session_id TEXT NOT NULL,
        memory_type TEXT NOT NULL CHECK (memory_type IN (
            'decision', 'finding', 'context', 'architecture',
            'session_summary', 'procedure', 'context_block',
            'work_product', 'team_profile'
        )),
        content TEXT NOT NULL,
        metadata JSONB DEFAULT '{}',
        embedding vector(1024),
        layer TEXT NOT NULL DEFAULT 'shared' CHECK (layer IN ('corp', 'canary', 'cove', 'shared')),
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
    CREATE INDEX IF NOT EXISTS idx_memories_session ON alx_memories(session_id);
    CREATE INDEX IF NOT EXISTS idx_memories_type ON alx_memories(memory_type);
    CREATE INDEX IF NOT EXISTS idx_memories_created ON alx_memories(created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_memories_layer ON alx_memories(layer);

    CREATE TABLE IF NOT EXISTS seed_embeddings (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        source_file TEXT NOT NULL,
        section_path TEXT,
        content TEXT NOT NULL,
        embedding vector(1024) NOT NULL,
        metadata JSONB DEFAULT '{}',
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
    CREATE INDEX IF NOT EXISTS idx_seed_source ON seed_embeddings(source_file);
    CREATE INDEX IF NOT EXISTS idx_seed_embedding_hnsw
        ON seed_embeddings USING hnsw (embedding vector_cosine_ops);
    """)


def downgrade():
    op.execute("DROP TABLE IF EXISTS seed_embeddings CASCADE")
    op.execute("DROP TABLE IF EXISTS alx_memories CASCADE")
    op.execute("DROP TABLE IF EXISTS alx_sessions CASCADE")
```

- [ ] **Step 6: Document stamp procedure for existing environments**

Add a comment at the top of the baseline migration and a note in `alembic.ini`:

For existing dev environments (tables already created by `02-create-memory-db.sql`):
```bash
cd services/memory-bus && alembic stamp 001_baseline
# Then apply fixes:
alembic upgrade head
```

For fresh installs (no tables yet):
```bash
cd services/memory-bus && alembic upgrade head
```

Add this to the plan's README or as a comment block at the top of `001_baseline.py`:
```python
# STAMP PROCEDURE — existing environments:
#   cd services/memory-bus && alembic stamp 001_baseline && alembic upgrade head
# FRESH INSTALLS:
#   cd services/memory-bus && alembic upgrade head
```

- [ ] **Step 7: Commit**

```bash
git add services/memory-bus/alembic.ini services/memory-bus/migrations/ services/memory-bus/pyproject.toml
git commit -m "feat: Alembic init for growdirect_memory — baseline migration"
```

---

### Task 7: Drop seed_embeddings Table

**Files:**
- Create: `services/memory-bus/migrations/versions/002_drop_seed_embeddings.py`

- [ ] **Step 1: Write migration**

```python
"""002 — drop seed_embeddings table (unused, not queried by any code).

Revision ID: 002_drop_seed_embeddings
Create Date: 2026-03-30
"""

from alembic import op

revision = "002_drop_seed_embeddings"
down_revision = "001_baseline"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("DROP TABLE IF EXISTS seed_embeddings CASCADE")


def downgrade():
    op.execute("""
    CREATE TABLE seed_embeddings (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        source_file TEXT NOT NULL,
        section_path TEXT,
        content TEXT NOT NULL,
        embedding vector(1024) NOT NULL,
        metadata JSONB DEFAULT '{}',
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
    CREATE INDEX idx_seed_source ON seed_embeddings(source_file);
    CREATE INDEX idx_seed_embedding_hnsw
        ON seed_embeddings USING hnsw (embedding vector_cosine_ops);
    """)
```

- [ ] **Step 2: Commit**

```bash
git add services/memory-bus/migrations/versions/002_drop_seed_embeddings.py
git commit -m "fix: drop unused seed_embeddings table (memory bus sweep)"
```

---

### Task 8: HNSW Index on alx_memories

**Files:**
- Create: `services/memory-bus/migrations/versions/003_hnsw_index.py`

- [ ] **Step 1: Write migration**

```python
"""003 — add HNSW index on alx_memories.embedding for vector search performance.

Revision ID: 003_hnsw_index
Create Date: 2026-03-30
"""

from alembic import op

revision = "003_hnsw_index"
down_revision = "002_drop_seed_embeddings"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    CREATE INDEX IF NOT EXISTS idx_alx_memories_embedding_hnsw
    ON alx_memories USING hnsw (embedding vector_cosine_ops);
    """)


def downgrade():
    op.execute("DROP INDEX IF EXISTS idx_alx_memories_embedding_hnsw")
```

- [ ] **Step 2: Commit**

```bash
git add services/memory-bus/migrations/versions/003_hnsw_index.py
git commit -m "fix: add HNSW index on alx_memories.embedding (memory bus sweep)"
```

---

### Task 9: Session FK + Orphan Fix

**Files:**
- Create: `services/memory-bus/migrations/versions/004_session_fk.py`

- [ ] **Step 1: Write migration**

```python
"""004 — backfill orphan session records + add session_id FK to alx_memories.

Revision ID: 004_session_fk
Create Date: 2026-03-30
"""

from alembic import op

revision = "004_session_fk"
down_revision = "003_hnsw_index"
branch_labels = None
depends_on = None


def upgrade():
    # Step 1: Create session records for any orphan session_ids
    op.execute("""
    INSERT INTO alx_sessions (session_id, status, started_at, closed_at, summary)
    SELECT
        m.session_id,
        'closed',
        MIN(m.created_at),
        MAX(m.created_at),
        'Backfilled session for orphan memories (migration 004)'
    FROM alx_memories m
    WHERE m.session_id NOT IN (SELECT session_id FROM alx_sessions)
    GROUP BY m.session_id;
    """)

    # Step 2: Add foreign key constraint
    op.execute("""
    ALTER TABLE alx_memories
    ADD CONSTRAINT fk_memories_session
    FOREIGN KEY (session_id) REFERENCES alx_sessions(session_id);
    """)


def downgrade():
    op.execute("""
    ALTER TABLE alx_memories DROP CONSTRAINT IF EXISTS fk_memories_session;
    """)
    # Note: does NOT delete backfilled sessions — they're harmless
```

- [ ] **Step 2: Commit**

```bash
git add services/memory-bus/migrations/versions/004_session_fk.py
git commit -m "fix: backfill orphan sessions + add session_id FK (memory bus sweep)"
```

---

### Task 10: Auth on Memory Bus

**Files:**
- Modify: `services/memory-bus/memory_bus/config.py`
- Modify: `services/memory-bus/memory_bus/server.py`
- Modify: `devops/docker-compose.yml`

**Context:** Add `MCP_API_KEY` check to all tool calls. Uses `growdirect_mcp.auth.validate_api_key`.

- [ ] **Step 1: Add mcp_api_key to config**

In `services/memory-bus/memory_bus/config.py`, add:

```python
self.mcp_api_key: str = os.environ.get("MCP_API_KEY", "")
```

- [ ] **Step 2: Add auth check to server.py**

Add an auth guard to each `@mcp.tool()` decorated function. The Memory Bus uses FastMCP which doesn't have request headers access in the same way. Instead, add `api_key: Optional[str] = None` parameter to each tool and validate it:

At the top of `server.py`, add:

```python
from growdirect_mcp.auth import validate_api_key, AuthError
```

Then wrap each tool function body with:

```python
try:
    validate_api_key(api_key)
except AuthError as e:
    return json.dumps({"error": str(e)})
```

Add `api_key: Optional[str] = None` to each tool function signature.

- [ ] **Step 3: Add MCP_API_KEY to docker-compose.yml**

In `devops/docker-compose.yml`, add to the memory-bus service environment:

```yaml
MCP_API_KEY: ${MCP_API_KEY:-growdirect-memory-dev-key}
```

- [ ] **Step 4: Add growdirect-mcp as dependency**

In `services/memory-bus/pyproject.toml`, the auth module comes from the platform package. For now, since the memory-bus and growdirect-mcp are in the same monorepo, add to the dev dependencies or copy the auth module. Since the memory-bus Dockerfile will need to install it:

Add to `services/memory-bus/pyproject.toml` dependencies:

```toml
"growdirect-mcp>=0.1.0",
```

- [ ] **Step 5: Commit**

```bash
git add services/memory-bus/memory_bus/config.py services/memory-bus/memory_bus/server.py devops/docker-compose.yml services/memory-bus/pyproject.toml
git commit -m "feat: add API key auth to Memory Bus (memory bus sweep)"
```

---

### Task 11: Remove Misplaced Tests + Write Replacements

**Files:**
- Delete: `services/memory-bus/tests/test_context_blocks.py`
- Delete: `services/memory-bus/tests/test_rag_retrieval.py`
- Create: `services/memory-bus/tests/test_store.py`

- [ ] **Step 1: Remove misplaced tests**

```bash
rm services/memory-bus/tests/test_context_blocks.py services/memory-bus/tests/test_rag_retrieval.py
```

- [ ] **Step 2: Write replacement tests**

```python
"""Tests for MemoryStore — exercises actual memory_bus service operations."""

import json
import os
import pytest
from unittest.mock import patch, MagicMock

from memory_bus.config import Config
from memory_bus.store import MemoryStore


@pytest.fixture
def mock_config():
    """Config with test database URL."""
    config = Config.__new__(Config)
    config.database_url = os.environ.get(
        "DATABASE_URL",
        "postgresql://growdirect:growdirect_dev@localhost:5432/growdirect_memory_test",
    )
    config.ollama_url = "http://localhost:11434"
    config.embedding_model = "qwen3-embedding:8b"
    config.port = 8003
    config.embedding_dimensions = 1024
    config.max_text_length = 6000
    config.mcp_api_key = ""
    return config


@pytest.fixture
def store(mock_config):
    """MemoryStore instance for testing."""
    return MemoryStore(mock_config)


class TestSessionLifecycle:
    """Test session_start and session_close."""

    @pytest.mark.postgres
    def test_session_start_returns_session_id(self, store):
        result = store.session_start(gro_issues=["GRO-999"])
        assert "session_id" in result
        assert result["status"] == "active"

    @pytest.mark.postgres
    def test_session_close_sets_summary(self, store):
        start = store.session_start()
        sid = start["session_id"]
        result = store.session_close(sid, summary="Test session done")
        assert result["status"] == "closed"
        assert result["summary"] == "Test session done"


class TestMemoryStore:
    """Test memory_store and memory_recall."""

    @pytest.mark.postgres
    def test_store_memory_returns_id(self, store):
        start = store.session_start()
        sid = start["session_id"]
        with patch("memory_bus.store.get_embedding", return_value=None):
            result = store.memory_store(
                session_id=sid,
                content="Test memory content",
                memory_type="context",
                layer="shared",
            )
        assert "memory_id" in result

    @pytest.mark.postgres
    def test_store_rejects_invalid_type(self, store):
        start = store.session_start()
        sid = start["session_id"]
        result = store.memory_store(
            session_id=sid,
            content="Test",
            memory_type="invalid_type",
        )
        assert "error" in result

    @pytest.mark.postgres
    def test_recall_returns_results(self, store):
        start = store.session_start()
        sid = start["session_id"]
        with patch("memory_bus.store.get_embedding", return_value=None):
            store.memory_store(session_id=sid, content="Unique recall test content xyz123")
        result = store.memory_recall(query="xyz123", limit=5)
        assert "memories" in result


class TestContextAssemble:
    """Test context_assemble."""

    @pytest.mark.postgres
    def test_context_assemble_returns_dict(self, store):
        result = store.context_assemble(topic="test")
        assert isinstance(result, dict)
```

- [ ] **Step 3: Verify tests are importable**

```bash
cd services/memory-bus && python3 -m pytest tests/test_store.py --collect-only
```

Expected: Tests collected (may not pass without live DB — that's ok for this step).

- [ ] **Step 4: Commit**

```bash
git add -A services/memory-bus/tests/
git commit -m "fix: replace misplaced tests with actual memory_bus service tests"
```

---

### Task 12: Update seed_clean.py + Strip DDL from Init SQL

**Files:**
- Modify: `services/memory-bus/scripts/seed_clean.py`
- Modify: `devops/init-db/02-create-memory-db.sql`

- [ ] **Step 1: Update seed_clean.py to create a session**

At the start of the `seed_memories()` function (or equivalent), before any `insert_memory()` calls, add session creation:

```python
# Create a session for seeded memories
session_id = "seed-clean"
now = datetime.now(timezone.utc).isoformat()
with engine.connect() as conn:
    # Check if session already exists (idempotent)
    existing = conn.execute(
        text("SELECT 1 FROM alx_sessions WHERE session_id = :sid"),
        {"sid": session_id},
    ).fetchone()
    if not existing:
        conn.execute(
            text("""
            INSERT INTO alx_sessions (session_id, status, started_at, summary)
            VALUES (:sid, 'active', :now, 'Seed script session')
            """),
            {"sid": session_id, "now": now},
        )
        conn.commit()
```

And at the end of the function, close the session:

```python
with engine.connect() as conn:
    conn.execute(
        text("""
        UPDATE alx_sessions
        SET status = 'closed', closed_at = :now, summary = 'Seed complete'
        WHERE session_id = :sid
        """),
        {"sid": session_id, "now": now},
    )
    conn.commit()
```

- [ ] **Step 2: Add session validation to store.py**

In `services/memory-bus/memory_bus/store.py`, in the `memory_store()` method, add a session existence check before inserting a memory:

```python
# Validate session exists (enforces FK integrity at application level)
session_check = conn.execute(
    text("SELECT 1 FROM alx_sessions WHERE session_id = :sid"),
    {"sid": session_id},
).fetchone()
if not session_check:
    return {"error": f"Session '{session_id}' does not exist — call session_start first"}
```

Add this check before the `INSERT INTO alx_memories` statement.

- [ ] **Step 3: Strip table DDL from 02-create-memory-db.sql**

Keep only the database creation, extension installation, and role grants. Remove all `CREATE TABLE`, `CREATE INDEX`, and trigger DDL. Add a comment pointing to Alembic:

```sql
-- growdirect_memory database bootstrap
-- Tables are managed by Alembic (services/memory-bus/migrations/)
-- Run: cd services/memory-bus && alembic upgrade head

-- Create database (only runs on first boot)
-- (keep existing CREATE DATABASE block)

-- Extensions
\c growdirect_memory
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Same for test database
\c growdirect_memory_test
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

- [ ] **Step 4: Commit**

```bash
git add services/memory-bus/scripts/seed_clean.py services/memory-bus/memory_bus/store.py devops/init-db/02-create-memory-db.sql
git commit -m "fix: seed_clean creates session, store validates session, DDL moved to Alembic (memory bus sweep)"
```

---

## Chunk 3: Cove Polish, ALX Extraction, SDDs

Tasks 13–18 complete the Cove MCP refactor, clean up Canary server maps, and update all affected documentation.

### Task 13: Cove MCP — Registry Refactor

**Files:**
- Modify: `Cove/cove/mcp/server.py`
- Modify: `Cove/requirements.txt`

**Context:** Replace the hardcoded `TOOLS` list and if/elif dispatch in `server.py` with `GrowDirectRegistry`. The 10 tool handler functions in `tools/search.py`, `tools/retrieval.py`, `tools/ingest.py` stay unchanged. Resources stay unchanged.

- [ ] **Step 1: Add growdirect-mcp to Cove requirements**

Add to `Cove/requirements.txt`:

```
growdirect-mcp>=0.1.0
```

- [ ] **Step 2: Refactor server.py**

Replace the `TOOLS` list (lines ~41-222) and `call_tool` dispatcher (lines ~236-267) with:

```python
from growdirect_mcp import GrowDirectRegistry, GrowDirectTool
from cove.mcp.tools import search, retrieval, ingest

# Build registry
registry = GrowDirectRegistry(
    server_name="cove-knowledge",
    version="1.0.0",
    description="Cove legal/governance knowledge base — CC&Rs, bylaws, property records",
)

# Search tools
registry.register(GrowDirectTool(
    name="knowledge_search",
    description="Semantic similarity search across the knowledge base",
    handler=search.knowledge_search,
    input_schema=<COPY FROM EXISTING TOOLS LIST — read the Tool(name="knowledge_search", ...) entry in current server.py and copy its inputSchema dict verbatim>,
    category="search",
))
# Register all 10 tools. For each: read its Tool(...) entry from the current
# TOOLS list in server.py, copy name/description/inputSchema exactly, map
# handler to the correct function in tools/search.py, tools/retrieval.py,
# or tools/ingest.py, and assign a category ("search", "retrieval", or "ingest").
```

Replace the `@server.call_tool()` handler with:

```python
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    return await registry.dispatch(name, arguments, {})
```

Replace the `@server.list_tools()` handler with:

```python
@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    return registry.list_tools()
```

Keep the `@server.list_resources()` and `@server.read_resource()` handlers unchanged.

- [ ] **Step 3: Write smoke test for registry dispatch**

Before modifying `server.py`, write a test that verifies the tool dispatch produces the same behavior:

```python
"""Smoke test: Cove MCP registry produces same tool list as before refactor."""

def test_cove_registry_has_all_tools():
    from cove.mcp.server import registry
    expected_tools = [
        "knowledge_search", "knowledge_get_chunk", "knowledge_list_documents",
        "knowledge_ingest", "knowledge_reingest", "knowledge_delete_document",
        "knowledge_stats", "knowledge_get_document", "knowledge_search_parcels",
        "knowledge_get_parcel",
    ]
    actual = registry.tool_names()
    assert sorted(actual) == sorted(expected_tools), f"Missing: {set(expected_tools) - set(actual)}"
    assert len(registry) == 10
```

- [ ] **Step 4: Test Cove MCP starts and tool count matches**

```bash
cd Cove && python3 -c "from cove.mcp.server import registry; print(f'{len(registry)} tools registered')"
```

Expected: `10 tools registered`

- [ ] **Step 5: Commit**

```bash
git add -f Cove/cove/mcp/server.py Cove/requirements.txt
git commit -m "refactor: Cove MCP uses GrowDirectRegistry — reference implementation"
```

---

### Task 14: Clean Canary Server Maps

**Files:**
- Modify: `Canary/canary/mcp/streamable_server.py`

**Context:** Remove `"alx"` from `SERVER_PREFIXES` (line ~48). The `"alx"` entry was already removed from `SERVER_BLUEPRINTS` and `SERVER_DEPS` per GRO-172, but the prefix remains as a ghost entry.

- [ ] **Step 1: Remove alx from SERVER_PREFIXES**

Remove the line `"alx": "/alx",` from the `SERVER_PREFIXES` dict in `streamable_server.py`.

- [ ] **Step 2: Verify no broken references**

```bash
cd Canary && grep -r '"alx"' canary/mcp/ --include="*.py"
```

Expected: No references to `"alx"` in the MCP module (beyond comments).

- [ ] **Step 3: Commit**

```bash
git add -f Canary/canary/mcp/streamable_server.py
git commit -m "fix: remove alx ghost entry from Canary SERVER_PREFIXES"
```

---

### Task 15: ALX Platform Skeleton

**Files:**
- Create: `services/alx/__init__.py`

- [ ] **Step 1: Create ALX platform marker**

```python
"""ALX — GrowDirect COO platform service.

Responsibilities:
- Platform coordination (dispatch, monitoring, status rollups) — future specs
- Memory bus integration — primary consumer of services/memory-bus/
- Consumes services/growdirect-mcp/ for MCP infrastructure

This is a platform service, NOT an app-level agent. App-level agents
(like Canary's QA Agent) belong in their respective app repos.
"""
```

- [ ] **Step 2: Commit**

```bash
git add services/alx/__init__.py
git commit -m "feat: ALX platform service skeleton"
```

---

### Task 16: ADR — MCP SDK Platform Standard

**Files:**
- Create: `docs/decisions/2026-03-30-mcp-sdk-platform-standard.md`

- [ ] **Step 1: Write ADR**

```markdown
# ADR: Official MCP Python SDK as Platform Standard

> **Date:** 2026-03-30
> **Status:** Accepted
> **Context:** SDD audit revealed Canary built a custom MCP framework without knowing the official SDK existed. Cove uses the SDK correctly.

## Decision

The official `mcp` Python SDK (`mcp>=1.0`) is the platform standard for all MCP servers going forward.

- All new MCP servers must use the SDK (via `growdirect-mcp` platform package)
- Cove's implementation is the reference pattern
- Canary's custom framework (`MCPTool`/`MCPRegistry`/`create_mcp_blueprint`) is tech debt to be retrofitted
- Both FastMCP (high-level) and `mcp.server.Server` (low-level) are valid API surfaces within the SDK
- The platform package at `services/growdirect-mcp/` wraps the SDK with GrowDirect conventions

## Consequences

- New MCP servers are faster to build (shared registry, auth, bridge)
- IDE integration works across all SDK-based servers via platform bridge
- Canary retrofit is a separate spec — 12 domain servers continue on the custom framework until then
- Memory Bus stays on FastMCP (it IS the SDK, high-level API)
```

- [ ] **Step 2: Commit**

```bash
git add docs/decisions/2026-03-30-mcp-sdk-platform-standard.md
git commit -m "docs: ADR — MCP Python SDK as platform standard"
```

---

### Task 17: Reclassify QA Agent SDD

**Files:**
- Move: `docs/sdds/alx/qa-agent.md` → `docs/sdds/canary/qa-agent.md`

- [ ] **Step 1: Move the file**

```bash
git mv docs/sdds/alx/qa-agent.md docs/sdds/canary/qa-agent.md
```

Note: `docs/sdds/canary/` may be gitignored by the `Canary/` rule. Use `git add -f` if needed.

- [ ] **Step 2: Update namespace in header**

Change `> **Namespace:** alx` to `> **Namespace:** canary` in the moved file.

- [ ] **Step 3: Commit**

```bash
git add -f docs/sdds/canary/qa-agent.md
git commit -m "docs: reclassify QA Agent SDD from alx/ to canary/ (app-level)"
```

---

### Task 18: Update SDDs

**Files:**
- Rewrite: `docs/sdds/alx/mcp-service-layer.md`
- Modify: `docs/sdds/platform/memory-bus.md`
- Modify: `docs/sdds/cove/archive-system.md` (update S4/S5 to reflect new import path and registry pattern for knowledge chunk ingestion)
- Modify: `docs/sdds/platform/shared-infrastructure.md` (S4 — add port allocation for any new platform services)

**Context:** SDDs describe what exists after the code changes.

- [ ] **Step 1: Rewrite MCP Service Layer SDD**

The SDD now documents `services/growdirect-mcp/` (the platform MCP SDK package), not Canary's custom framework. Key changes:
- Code location: `services/growdirect-mcp/`
- Architecture: SDK wrapper with GrowDirectRegistry, GrowDirectTool, bridge, auth
- Data model: N/A (no database)
- Interfaces: GrowDirectRegistry API, GrowDirectTool API, bridge config
- Section 11: Canary retrofit deferred (separate spec), `ops` ghost prefix remains as Canary tech debt

- [ ] **Step 2: Update Memory Bus SDD**

Update these sections to reflect the sweep:
- S2: Add dual-codebase boundary clarification
- S3: Remove seed_embeddings, add HNSW index, add session_id FK
- S7: Add auth (MCP_API_KEY)
- S9: New test file list
- S11: Mark all findings as resolved with this spec reference

- [ ] **Step 3: Commit**

```bash
git add -f docs/sdds/alx/mcp-service-layer.md docs/sdds/platform/memory-bus.md docs/sdds/cove/archive-system.md docs/sdds/platform/shared-infrastructure.md
git commit -m "docs: update SDDs for MCP consolidation — platform package, memory bus sweep"
```

---

## Verification

After all tasks complete, verify all success criteria:

```bash
# Positive assertions
ls services/growdirect-mcp/pyproject.toml                    # 1. Package exists
python3 -c "from growdirect_mcp import GrowDirectRegistry"   # 1. Importable
python3 -c "from growdirect_mcp.bridge import discover_servers" # 2. Bridge exists
cd Cove && python3 -c "from cove.mcp.server import registry; print(len(registry))"  # 3. Cove uses registry
ls services/memory-bus/alembic.ini                           # 4. Alembic exists
ls docs/decisions/2026-03-30-mcp-sdk-platform-standard.md    # 8. ADR exists
ls docs/sdds/canary/qa-agent.md                              # 7. QA Agent moved

# Negative assertions
grep -r "seed_embeddings" devops/init-db/02-create-memory-db.sql  # 10. Should be empty
grep -r "canary.services.alx" services/memory-bus/tests/          # 11. Should be empty
grep '"alx"' Canary/canary/mcp/streamable_server.py               # 12. Should be empty (or comments only)
```

---

## Execution Order

| Phase | Tasks | Parallelism | Blocks On |
|-------|-------|-------------|-----------|
| 1 | Tasks 1–5 (Platform MCP Package) | Sequential (each builds on previous) | Nothing |
| 2 | Tasks 6–12 (Memory Bus Sweep) | Sequential (migrations depend on each other) | Phase 1 (Task 10 needs growdirect-mcp) |
| 3 | Tasks 13–18 (Cove + ALX + SDDs) | Tasks 13, 14, 15 can parallel; 16, 17, 18 sequential after | Phase 1 (Task 13 needs growdirect-mcp) |

**Wall-clock phases: 3** (Phase 2 and 3 can start after Phase 1, but not parallel with each other due to Task 10 and Task 13 both modifying package dependencies).
