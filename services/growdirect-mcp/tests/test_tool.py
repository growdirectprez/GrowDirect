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
