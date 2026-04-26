# GrowDirect LLC — Confidential & Proprietary
# Copyright (c) 2026 GrowDirect LLC. All rights reserved.
"""Stdio-HTTP bridge — IDE tool discovery across platform MCP servers."""

import json
import logging
import os
from dataclasses import dataclass
from typing import Optional

import httpx

logger = logging.getLogger(__name__)


@dataclass
class ServerConfig:
    name: str
    base_url: str
    transport: str = "http"
    api_key: Optional[str] = None


def discover_servers() -> list[ServerConfig]:
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
