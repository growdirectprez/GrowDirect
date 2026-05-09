# GrowDirect LLC — Confidential & Proprietary
# Copyright (c) 2026 GrowDirect LLC. All rights reserved.
"""ALX — Canary Go VSM and Delivery Manager.

Mercury Astronaut role. Receives imprint dispatches, recalls from
CRB/Canary Go/NCR corpus, emits findings and audit events.

Secrets are pulled from Secret Manager (project: growdirect-mercury) at
module load via Application Default Credentials. No .env files, no
shell exports. Run `gcloud auth application-default login` once on
the local dev machine; Cloud Run uses the runtime SA automatically.
"""

import os
from pathlib import Path

from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
from google.cloud import secretmanager

_PROJECT = "growdirect-mercury"
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", _PROJECT)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "true")


def _sm(name: str) -> str:
    """Fetch latest version of a Mercury Secret Manager secret."""
    client = secretmanager.SecretManagerServiceClient()
    resp = client.access_secret_version(
        name=f"projects/{_PROJECT}/secrets/{name}/versions/latest"
    )
    return resp.payload.data.decode().strip()


_MEMORY_BUS_URL = _sm("memory-bus-url")
_MEMORY_BUS_API_KEY = _sm("memory-bus-api-key")
_PROMPT = (Path(__file__).parent / "prompts" / "vsm.md").read_text()

# TODO(2026-05-06): swap back to claude-sonnet-4-6 once Vertex AI Anthropic
# subscription is fully active in growdirect-mercury. Bridge for tonight.
root_agent = Agent(
    model="gemini-2.5-flash",
    name="alx",
    description="ALX — Canary Go VSM and Delivery Manager (Mercury Astronaut)",
    instruction=_PROMPT,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=_MEMORY_BUS_URL + "/mcp",
                headers={"X-API-Key": _MEMORY_BUS_API_KEY},
            )
        )
    ],
)
