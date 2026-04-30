# GrowDirect LLC — Confidential & Proprietary
# Copyright (c) 2026 GrowDirect LLC. All rights reserved.
"""GrowDirect Memory Bus — MCP server for organizational knowledge."""
import json
import logging
from typing import Optional

from mcp.server.fastmcp import FastMCP

from memory_bus.config import Config
from memory_bus.store import MemoryStore
from growdirect_mcp.auth import validate_api_key, AuthError

logger = logging.getLogger(__name__)

config = Config()
store = MemoryStore(config)

mcp = FastMCP(
    "GrowDirect Memory Bus",
    host="0.0.0.0",
    port=config.port,
)


@mcp.tool()
def session_start(gro_issues: Optional[list[str]] = None, api_key: Optional[str] = None) -> str:
    """Start a new ALX session. Optionally associate GRO issues."""
    try:
        validate_api_key(api_key)
    except AuthError as e:
        return json.dumps({"error": str(e)})
    result = store.session_start(gro_issues=gro_issues)
    return json.dumps(result, default=str)


@mcp.tool()
def session_close(
    session_id: str,
    summary: str,
    decisions: Optional[list[str]] = None,
    unresolved: Optional[list[str]] = None,
    api_key: Optional[str] = None,
) -> str:
    """Close a session with summary, decisions, and unresolved items."""
    try:
        validate_api_key(api_key)
    except AuthError as e:
        return json.dumps({"error": str(e)})
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
    engines: Optional[list[str]] = None,
    api_key: Optional[str] = None,
) -> str:
    """Store a memory with embedding, layer tag, engine applicability, and type classification.

    engines: list of engine primitives this memory applies to. Defaults to
    ['platform']. Valid values: loyalty, voting, store-ops, web-store,
    operations, geospatial, platform.
    """
    try:
        validate_api_key(api_key)
    except AuthError as e:
        return json.dumps({"error": str(e)})
    result = store.memory_store(
        session_id=session_id or "unattached",
        content=content,
        memory_type=memory_type,
        metadata=metadata,
        layer=layer,
        engines=engines,
    )
    return json.dumps(result, default=str)


@mcp.tool()
def memory_recall(
    query: str,
    limit: int = 10,
    memory_type: Optional[str] = None,
    layer: Optional[str] = None,
    engines: Optional[list[str]] = None,
    api_key: Optional[str] = None,
) -> str:
    """Semantic search over memories. Falls back: vector -> full-text -> ILIKE.

    Use layer to scope results: corp, canary, cove, or shared (legacy partition).
    Use engines to scope by engine applicability (overlap semantics): loyalty,
    voting, store-ops, web-store, operations, geospatial, platform.
    """
    try:
        validate_api_key(api_key)
    except AuthError as e:
        return json.dumps({"error": str(e)})
    result = store.memory_recall(
        query=query, limit=limit, memory_type=memory_type, layer=layer, engines=engines
    )
    return json.dumps(result, default=str)


@mcp.tool()
def memory_search(
    session_id: Optional[str] = None,
    memory_type: Optional[str] = None,
    since: Optional[str] = None,
    layer: Optional[str] = None,
    limit: int = 20,
    engines: Optional[list[str]] = None,
    api_key: Optional[str] = None,
) -> str:
    """Structured search by session, type, date, layer, or engine applicability.

    Use layer to scope results: corp, canary, cove, or shared (legacy partition).
    Use engines to scope by engine applicability (overlap semantics).
    """
    try:
        validate_api_key(api_key)
    except AuthError as e:
        return json.dumps({"error": str(e)})
    result = store.memory_search(
        session_id=session_id,
        memory_type=memory_type,
        since=since,
        layer=layer,
        limit=limit,
        engines=engines,
    )
    return json.dumps(result, default=str)


@mcp.tool()
def context_assemble(
    topic: Optional[str] = None,
    gro_issue: Optional[str] = None,
    limit: int = 15,
    api_key: Optional[str] = None,
) -> str:
    """Assemble a context window for a topic or GRO issue."""
    try:
        validate_api_key(api_key)
    except AuthError as e:
        return json.dumps({"error": str(e)})
    result = store.context_assemble(
        topic=topic, gro_issue=gro_issue, limit=limit
    )
    return json.dumps(result, default=str)


@mcp.tool()
def domain_context(
    domain: str,
    topic: Optional[str] = None,
    token_budget: int = 4000,
    api_key: Optional[str] = None,
) -> str:
    """Full domain context assembly with token budget."""
    try:
        validate_api_key(api_key)
    except AuthError as e:
        return json.dumps({"error": str(e)})
    result = store.domain_context(
        domain=domain, topic=topic, token_budget=token_budget
    )
    return json.dumps(result, default=str)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
