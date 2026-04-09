"""GrowDirectRegistry — SDK Server wrapper with tool registration and dispatch."""

import json
import logging
from typing import Any, Optional

from mcp.server import Server
from mcp.types import TextContent, Tool

from growdirect_mcp.tool import GrowDirectTool

logger = logging.getLogger(__name__)


class GrowDirectRegistry:
    """Registry of MCP tools for a single server."""

    def __init__(self, server_name: str, version: str, description: str):
        self.server_name = server_name
        self.version = version
        self.description = description
        self._tools: dict[str, GrowDirectTool] = {}

    def register(self, tool: GrowDirectTool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' already registered")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[GrowDirectTool]:
        return self._tools.get(name)

    def tool_names(self) -> list[str]:
        return list(self._tools.keys())

    def list_tools(self) -> list[Tool]:
        return [t.to_mcp() for t in self._tools.values()]

    def get_manifest(self) -> dict[str, Any]:
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
        self, tool_name: str, arguments: dict[str, Any], context: dict[str, Any],
    ) -> list[TextContent]:
        tool = self.get(tool_name)
        if tool is None:
            error_envelope = {"tool": tool_name, "ok": False, "error": f"Unknown tool: {tool_name}"}
            return [TextContent(type="text", text=json.dumps(error_envelope))]
        result = await tool.invoke(arguments, context)
        return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

    def build_server(self) -> Server:
        server = Server(self.server_name)
        registry = self

        @server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            return registry.list_tools()

        @server.call_tool()
        async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
            return await registry.dispatch(name, arguments, {})

        return server

    def __contains__(self, name: str) -> bool:
        return name in self._tools

    def __len__(self) -> int:
        return len(self._tools)
