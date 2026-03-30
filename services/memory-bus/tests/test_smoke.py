"""End-to-end smoke test for memory bus MCP server.

Requires: growdirect_memory_test database, Ollama running.
"""
import pytest


class TestSmoke:
    @pytest.mark.asyncio
    async def test_store_recall_roundtrip(self):
        """Acceptance criterion: memory_store -> memory_recall returns content."""
        from mcp import ClientSession
        from memory_bus.server import mcp

        async with ClientSession(*await mcp.get_streamable_http_transport()) as session:
            await session.initialize()

            # Start session
            await session.call_tool("session_start", arguments={"gro_issues": ["GRO-SMOKE"]})

            # Store with layer
            await session.call_tool("memory_store", arguments={
                "content": "Secret ballot separation is required by Davis-Stirling Civil Code 5100",
                "memory_type": "decision",
                "layer": "cove",
            })

            # Recall
            result = await session.call_tool("memory_recall", arguments={
                "query": "secret ballot separation",
            })

            content_str = str(result.content)
            assert "ballot" in content_str.lower() or "separation" in content_str.lower()
