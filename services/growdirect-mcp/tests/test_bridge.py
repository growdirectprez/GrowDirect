# GrowDirect LLC — Confidential & Proprietary
# Copyright (c) 2026 GrowDirect LLC. All rights reserved.
"""Tests for the stdio-HTTP bridge — IDE tool discovery across platform servers."""

import json
import pytest
from unittest.mock import MagicMock, patch
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
