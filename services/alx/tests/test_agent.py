# services/alx-agent/tests/test_agent.py
"""Unit tests for ALX agent — prompt validation and ADK wiring."""

import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))


def test_vsm_prompt_file_exists():
    """vsm.md must exist and be non-empty."""
    prompt_path = Path(__file__).parent.parent / "prompts" / "vsm.md"
    assert prompt_path.exists(), "prompts/vsm.md not found"
    content = prompt_path.read_text()
    assert len(content) > 100, "vsm.md appears empty or too short"
    assert "Canary Go" in content
    assert "memory_recall" in content
    assert "audit_event" in content


def test_vsm_prompt_scope_exclusions():
    """vsm.md must explicitly exclude out-of-scope projects."""
    prompt_path = Path(__file__).parent.parent / "prompts" / "vsm.md"
    content = prompt_path.read_text()
    assert "Cove" in content, "prompt must name Cove as out of scope"
    assert "Angel" in content, "prompt must name Angel as out of scope"


def test_agent_module_imports():
    """agent.py must be importable and define root_agent."""
    with patch.dict(os.environ, {
        "MEMORY_BUS_URL": "http://localhost:8003",
        "MEMORY_BUS_API_KEY": "test-key",
    }):
        with patch("google.adk.tools.mcp_tool.mcp_toolset.MCPToolset") as mock_mcp, \
             patch("google.adk.tools.mcp_tool.mcp_toolset.StreamableHTTPConnectionParams"):
            mock_mcp.return_value = MagicMock()
            import agent
            assert hasattr(agent, "root_agent"), "agent.py must define root_agent"
            assert agent.root_agent is not None


def test_root_agent_has_mcp_toolset():
    """root_agent must be configured with at least one toolset."""
    with patch.dict(os.environ, {
        "MEMORY_BUS_URL": "http://localhost:8003",
        "MEMORY_BUS_API_KEY": "test-key",
    }):
        with patch("google.adk.tools.mcp_tool.mcp_toolset.MCPToolset") as mock_mcp, \
             patch("google.adk.tools.mcp_tool.mcp_toolset.StreamableHTTPConnectionParams"):
            mock_toolset = MagicMock()
            mock_mcp.return_value = mock_toolset
            import importlib
            import agent as _agent_mod
            importlib.reload(_agent_mod)
            assert mock_mcp.called, "MCPToolset must be instantiated in agent.py"
