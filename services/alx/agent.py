# GrowDirect LLC — Confidential & Proprietary
# Copyright (c) 2026 GrowDirect LLC. All rights reserved.
"""ALX — Canary Go VSM and Delivery Manager.

Mercury Astronaut role. Receives imprint dispatches, recalls from
CRB/Canary Go/NCR corpus, emits findings and audit events.
"""

import os
from pathlib import Path

from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams

_PROMPT = (Path(__file__).parent / "prompts" / "vsm.md").read_text()

root_agent = Agent(
    model="claude-sonnet-4-6",
    name="alx",
    description="ALX — Canary Go VSM and Delivery Manager (Mercury Astronaut)",
    instruction=_PROMPT,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=os.environ["MEMORY_BUS_URL"] + "/mcp",
                headers={"X-API-Key": os.environ["MEMORY_BUS_API_KEY"]},
            )
        )
    ],
)
