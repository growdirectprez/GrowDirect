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
