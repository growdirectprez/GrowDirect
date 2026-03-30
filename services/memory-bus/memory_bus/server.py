"""GrowDirect Memory Bus — MCP server for organizational knowledge."""
import json
import logging
from typing import Optional

from mcp.server.fastmcp import FastMCP

from memory_bus.config import Config
from memory_bus.store import MemoryStore

logger = logging.getLogger(__name__)

config = Config()
store = MemoryStore(config)

mcp = FastMCP(
    "GrowDirect Memory Bus",
    description="Platform-level organizational knowledge store",
)


@mcp.tool()
def session_start(gro_issues: Optional[list[str]] = None) -> str:
    """Start a new ALX session. Optionally associate GRO issues."""
    result = store.session_start(gro_issues=gro_issues)
    return json.dumps(result, default=str)


@mcp.tool()
def session_close(
    session_id: str,
    summary: str,
    decisions: Optional[list[str]] = None,
    unresolved: Optional[list[str]] = None,
) -> str:
    """Close a session with summary, decisions, and unresolved items."""
    result = store.session_close(
        session_id=session_id,
        summary=summary,
        decisions=decisions,
        unresolved=unresolved,
    )
    return json.dumps(result, default=str)


@mcp.tool()
def memory_store(
    content: str,
    memory_type: str = "context",
    session_id: Optional[str] = None,
    metadata: Optional[dict] = None,
    layer: str = "shared",
) -> str:
    """Store a memory with embedding, layer tag, and type classification."""
    result = store.memory_store(
        session_id=session_id or "unattached",
        content=content,
        memory_type=memory_type,
        metadata=metadata,
        layer=layer,
    )
    return json.dumps(result, default=str)


@mcp.tool()
def memory_recall(
    query: str,
    limit: int = 10,
    memory_type: Optional[str] = None,
    layer: Optional[str] = None,
) -> str:
    """Semantic search over memories. Falls back: vector -> full-text -> ILIKE.

    Use layer to scope results: corp, canary, cove, or shared.
    """
    result = store.memory_recall(
        query=query, limit=limit, memory_type=memory_type, layer=layer
    )
    return json.dumps(result, default=str)


@mcp.tool()
def memory_search(
    session_id: Optional[str] = None,
    memory_type: Optional[str] = None,
    since: Optional[str] = None,
    layer: Optional[str] = None,
    limit: int = 20,
) -> str:
    """Structured search by session, type, date, or layer.

    Use layer to scope results: corp, canary, cove, or shared.
    """
    result = store.memory_search(
        session_id=session_id,
        memory_type=memory_type,
        since=since,
        layer=layer,
        limit=limit,
    )
    return json.dumps(result, default=str)


@mcp.tool()
def context_assemble(
    topic: Optional[str] = None,
    gro_issue: Optional[str] = None,
    limit: int = 15,
) -> str:
    """Assemble a context window for a topic or GRO issue."""
    result = store.context_assemble(
        topic=topic, gro_issue=gro_issue, limit=limit
    )
    return json.dumps(result, default=str)


@mcp.tool()
def domain_context(
    domain: str,
    topic: Optional[str] = None,
    token_budget: int = 4000,
) -> str:
    """Full domain context assembly with token budget."""
    result = store.domain_context(
        domain=domain, topic=topic, token_budget=token_budget
    )
    return json.dumps(result, default=str)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=config.port)
