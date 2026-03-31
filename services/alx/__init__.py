"""ALX — GrowDirect COO platform service.

Responsibilities:
- Platform coordination (dispatch, monitoring, status rollups) — future specs
- Memory bus integration — primary consumer of services/memory-bus/
- Consumes services/growdirect-mcp/ for MCP infrastructure

This is a platform service, NOT an app-level agent. App-level agents
(like Canary's QA Agent) belong in their respective app repos.
"""
