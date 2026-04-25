# GrowDirect LLC — Confidential & Proprietary
# Copyright (c) 2026 GrowDirect LLC. All rights reserved.
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
