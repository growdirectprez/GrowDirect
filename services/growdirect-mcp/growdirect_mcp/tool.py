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
