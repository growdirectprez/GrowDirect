"""Unit tests for ALX Context Blocks — SDD-058 Domain Memories.

Tests recall_context_blocks(), assemble_domain_context(), _pick_best_workflow(),
and the domain_context MCP tool registration.

Layer 1: pure functions, no database. All DB calls mocked.
"""

import json
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone

pytestmark = [pytest.mark.unit, pytest.mark.alx]


# ======================================================================
# Fixtures — mock context block rows
# ======================================================================

def _make_row(memory_id, memory_type, content, metadata, created_at=None):
    """Build a mock row tuple matching the SELECT column order."""
    return (
        memory_id,
        memory_type,
        content,
        json.dumps(metadata) if isinstance(metadata, dict) else metadata,
        created_at or datetime(2026, 3, 9, tzinfo=timezone.utc),
    )


CHIRP_OVERVIEW = _make_row(
    "ov-chirp-001",
    "context_block",
    "## Chirp Domain Overview\n\n### SDDs\n- SDD-005, SDD-006, SDD-025\n\n### Blueprints\n- chirp_wired (/api/chirp)\n\n### Services\n- rule_engine.py, stateless_engine.py",
    {
        "block_type": "domain_overview",
        "domain": "chirp",
        "sdd_refs": ["SDD-005", "SDD-006", "SDD-025"],
        "token_estimate": 1200,
    },
)

CHIRP_API = _make_row(
    "api-chirp-001",
    "context_block",
    "## Chirp API Contract\n\n### POST /webhooks/square\nHMAC auth. Receives Square webhook.\n\n### GET /api/chirp/rules\nJWT auth. List detection rules.",
    {
        "block_type": "api_contract",
        "domain": "chirp",
        "api_paths": ["/webhooks/square", "/api/chirp/rules"],
        "token_estimate": 1200,
    },
)

ALERT_LIFECYCLE_WORKFLOW = _make_row(
    "wf-alert-001",
    "context_block",
    "## Alert Lifecycle Workflow\n\nSquare webhook → TSP → Chirp → Alert (new)\n  ├── Resolve → done\n  ├── Dismiss → dismissed\n  └── Open case → Fox",
    {
        "block_type": "workflow",
        "domain": "alert",
        "domains": ["tsp", "chirp", "alert", "owl", "fox"],
        "token_estimate": 2000,
    },
)

HEALTH_CHECK_WORKFLOW = _make_row(
    "wf-health-001",
    "context_block",
    "## Health Check Pipeline\n\nPOST /ops/api/health-check/start → stages → report",
    {
        "block_type": "workflow",
        "domain": "ops",
        "domains": ["ops", "chirp", "owl", "alert"],
        "token_estimate": 2000,
    },
)

CANARY_APP_DATA_MODEL = _make_row(
    "dm-app-001",
    "context_block",
    "## canary_app Data Model\n\n38 tables. Mixed patterns: CRUD, APPEND-ONLY, soft delete.",
    {
        "block_type": "data_model",
        "domain": "chirp",
        "database": "canary_app",
        "token_estimate": 1500,
    },
)


# ======================================================================
# recall_context_blocks
# ======================================================================

class TestRecallContextBlocks:

    @patch("canary.services.alx.memory._get_session")
    def test_recall_returns_blocks(self, mock_session):
        from canary.services.alx.memory import recall_context_blocks

        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_db.execute.return_value.fetchall.return_value = [CHIRP_OVERVIEW, CHIRP_API]

        results = recall_context_blocks("chirp")

        assert len(results) == 2
        assert results[0]["memory_id"] == "ov-chirp-001"
        assert results[1]["memory_id"] == "api-chirp-001"
        assert "Chirp Domain Overview" in results[0]["content"]
        mock_db.close.assert_called_once()

    @patch("canary.services.alx.memory._get_session")
    def test_recall_with_block_type_filter(self, mock_session):
        from canary.services.alx.memory import recall_context_blocks

        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_db.execute.return_value.fetchall.return_value = [CHIRP_OVERVIEW]

        results = recall_context_blocks("chirp", block_type="domain_overview")

        assert len(results) == 1
        # Verify block_type was passed in query params
        call_args = mock_db.execute.call_args
        params = call_args[0][1]
        assert params["block_type"] == "domain_overview"
        mock_db.close.assert_called_once()

    @patch("canary.services.alx.memory._get_session")
    def test_recall_empty_result(self, mock_session):
        from canary.services.alx.memory import recall_context_blocks

        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_db.execute.return_value.fetchall.return_value = []

        results = recall_context_blocks("raas")

        assert results == []
        mock_db.close.assert_called_once()

    def test_recall_invalid_domain(self):
        from canary.services.alx.memory import recall_context_blocks

        with pytest.raises(ValueError, match="Unknown domain"):
            recall_context_blocks("nonexistent")

    def test_recall_invalid_block_type(self):
        from canary.services.alx.memory import recall_context_blocks

        with pytest.raises(ValueError, match="Unknown block_type"):
            recall_context_blocks("chirp", block_type="invalid_type")

    @patch("canary.services.alx.memory._get_session")
    def test_recall_parses_metadata(self, mock_session):
        from canary.services.alx.memory import recall_context_blocks

        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_db.execute.return_value.fetchall.return_value = [CHIRP_OVERVIEW]

        results = recall_context_blocks("chirp")

        meta = results[0]["metadata"]
        assert meta["block_type"] == "domain_overview"
        assert meta["domain"] == "chirp"
        assert "SDD-005" in meta["sdd_refs"]

    @patch("canary.services.alx.memory._get_session")
    def test_recall_handles_dict_metadata(self, mock_session):
        """If metadata comes back as already-parsed dict (not JSON string)."""
        from canary.services.alx.memory import recall_context_blocks

        row_with_dict_meta = (
            "test-001",
            "context_block",
            "content here",
            {"block_type": "domain_overview", "domain": "chirp"},
            datetime(2026, 3, 9, tzinfo=timezone.utc),
        )
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_db.execute.return_value.fetchall.return_value = [row_with_dict_meta]

        results = recall_context_blocks("chirp")

        assert results[0]["metadata"]["domain"] == "chirp"


# ======================================================================
# _pick_best_workflow
# ======================================================================

class TestPickBestWorkflow:

    def test_picks_matching_workflow(self):
        from canary.services.alx.memory import _pick_best_workflow

        workflows = [
            {"content": "Health check pipeline with ops monitoring and chirp sweep"},
            {"content": "Alert lifecycle from webhook through resolution and case management"},
        ]

        result = _pick_best_workflow(workflows, "alert lifecycle")
        assert "Alert lifecycle" in result["content"]

    def test_picks_first_when_no_match(self):
        from canary.services.alx.memory import _pick_best_workflow

        workflows = [
            {"content": "First workflow about topic A"},
            {"content": "Second workflow about topic B"},
        ]

        result = _pick_best_workflow(workflows, "completely unrelated query")
        assert result["content"] == "First workflow about topic A"

    def test_empty_workflows_returns_none(self):
        from canary.services.alx.memory import _pick_best_workflow

        result = _pick_best_workflow([], "any topic")
        assert result is None

    def test_empty_topic_returns_first(self):
        from canary.services.alx.memory import _pick_best_workflow

        workflows = [{"content": "First"}, {"content": "Second"}]
        result = _pick_best_workflow(workflows, "")
        assert result["content"] == "First"


# ======================================================================
# assemble_domain_context
# ======================================================================

class TestAssembleDomainContext:

    @patch("canary.services.alx.memory.recall_context_blocks")
    def test_assembles_overview_and_api(self, mock_recall):
        from canary.services.alx.memory import assemble_domain_context

        def side_effect(domain, block_type=None):
            if block_type == "domain_overview":
                return [{"content": "Chirp overview content", "metadata": {}}]
            if block_type == "api_contract":
                return [{"content": "Chirp API contract", "metadata": {}}]
            return []

        mock_recall.side_effect = side_effect

        result = assemble_domain_context("chirp")

        assert "Chirp Domain Context" in result["context"]
        assert "### Overview" in result["context"]
        assert "### API Contract" in result["context"]
        assert "domain_overview" in result["blocks_used"]
        assert "api_contract" in result["blocks_used"]
        assert result["domain"] == "chirp"
        assert result["topic"] is None
        assert result["token_estimate"] > 0

    @patch("canary.services.alx.memory.recall_context_blocks")
    def test_includes_workflow_when_topic_given(self, mock_recall):
        from canary.services.alx.memory import assemble_domain_context

        def side_effect(domain, block_type=None):
            if block_type == "domain_overview":
                return [{"content": "Alert overview", "metadata": {}}]
            if block_type == "api_contract":
                return [{"content": "Alert API", "metadata": {}}]
            if block_type == "workflow":
                return [{"content": "Alert lifecycle workflow from webhook to resolution", "metadata": {}}]
            return []

        mock_recall.side_effect = side_effect

        result = assemble_domain_context("alert", topic="alert lifecycle")

        assert "### Workflow" in result["context"]
        assert "workflow" in result["blocks_used"]
        assert result["topic"] == "alert lifecycle"

    @patch("canary.services.alx.memory.recall_context_blocks")
    def test_no_workflow_without_topic(self, mock_recall):
        from canary.services.alx.memory import assemble_domain_context

        def side_effect(domain, block_type=None):
            if block_type == "domain_overview":
                return [{"content": "Overview", "metadata": {}}]
            if block_type == "api_contract":
                return [{"content": "API", "metadata": {}}]
            return []

        mock_recall.side_effect = side_effect

        result = assemble_domain_context("owl")

        assert "### Workflow" not in result["context"]
        assert "workflow" not in result["blocks_used"]

    @patch("canary.services.alx.memory.recall_context_blocks")
    def test_empty_domain_shows_seed_message(self, mock_recall):
        from canary.services.alx.memory import assemble_domain_context

        mock_recall.return_value = []

        result = assemble_domain_context("raas")

        assert "seed_context_blocks.py" in result["context"]
        assert result["blocks_used"] == []

    def test_invalid_domain_raises(self):
        from canary.services.alx.memory import assemble_domain_context

        with pytest.raises(ValueError, match="Unknown domain"):
            assemble_domain_context("invalid_domain")

    @patch("canary.services.alx.memory.recall_context_blocks")
    def test_token_budget_enforced(self, mock_recall):
        from canary.services.alx.memory import assemble_domain_context

        # Large content that exceeds a small budget
        big_content = "x" * 5000

        def side_effect(domain, block_type=None):
            if block_type == "domain_overview":
                return [{"content": big_content, "metadata": {}}]
            if block_type == "api_contract":
                return [{"content": big_content, "metadata": {}}]
            if block_type == "workflow":
                return [{"content": big_content, "metadata": {}}]
            return []

        mock_recall.side_effect = side_effect

        # With a 3000-token budget (~12000 chars), the workflow should be truncated
        result = assemble_domain_context("chirp", topic="test", token_budget=3000)

        # Should have overview + api + possibly truncated workflow
        assert result["token_estimate"] > 0
        assert "domain_overview" in result["blocks_used"]

    @patch("canary.services.alx.memory.recall_context_blocks")
    def test_includes_data_model_when_space(self, mock_recall):
        from canary.services.alx.memory import assemble_domain_context

        def side_effect(domain, block_type=None):
            if block_type == "domain_overview":
                return [{"content": "Short overview", "metadata": {}}]
            if block_type == "api_contract":
                return [{"content": "Short API", "metadata": {}}]
            if block_type == "data_model":
                return [{"content": "Data model tables list", "metadata": {}}]
            return []

        mock_recall.side_effect = side_effect

        result = assemble_domain_context("chirp")

        assert "### Data Model" in result["context"]
        assert "data_model" in result["blocks_used"]


# ======================================================================
# domain_context MCP tool registration
# ======================================================================

class TestDomainContextTool:

    def test_tool_is_registered(self):
        from canary.services.alx.tools import get_tool

        tool = get_tool("domain_context")
        assert tool is not None
        assert tool.name == "domain_context"

    def test_tool_in_manifest(self):
        from canary.services.alx.tools import get_manifest

        manifest = get_manifest()
        tool_names = [t["name"] for t in manifest["tools"]]
        assert "domain_context" in tool_names

    def test_tool_has_domain_enum(self):
        from canary.services.alx.tools import get_tool

        tool = get_tool("domain_context")
        schema = tool.input_schema
        assert "domain" in schema
        assert "enum" in schema["domain"]
        assert "chirp" in schema["domain"]["enum"]
        assert "owl" in schema["domain"]["enum"]
        assert len(schema["domain"]["enum"]) == 11

    def test_tool_has_topic_param(self):
        from canary.services.alx.tools import get_tool

        tool = get_tool("domain_context")
        assert "topic" in tool.input_schema

    @patch("canary.services.alx.memory.assemble_domain_context")
    def test_tool_invocation(self, mock_assemble):
        from canary.services.alx.tools import get_tool

        mock_assemble.return_value = {
            "context": "## Chirp Domain Context\n...",
            "domain": "chirp",
            "topic": None,
            "blocks_used": ["domain_overview", "api_contract"],
            "token_estimate": 600,
        }

        tool = get_tool("domain_context")
        result = tool.invoke({"domain": "chirp"})

        assert result["ok"] is True
        assert result["result"]["domain"] == "chirp"
        mock_assemble.assert_called_once()

    @patch("canary.services.alx.memory.assemble_domain_context")
    def test_tool_with_topic(self, mock_assemble):
        from canary.services.alx.tools import get_tool

        mock_assemble.return_value = {
            "context": "## Alert Domain Context\n...",
            "domain": "alert",
            "topic": "lifecycle",
            "blocks_used": ["domain_overview", "api_contract", "workflow"],
            "token_estimate": 1200,
        }

        tool = get_tool("domain_context")
        result = tool.invoke({"domain": "alert", "topic": "lifecycle"})

        assert result["ok"] is True
        assert result["result"]["topic"] == "lifecycle"

    def test_tool_missing_domain(self):
        from canary.services.alx.tools import get_tool

        tool = get_tool("domain_context")
        result = tool.invoke({"domain": ""})

        assert result["ok"] is False
        assert "error" in result["result"]


# ======================================================================
# Valid domain constants
# ======================================================================

class TestDomainConstants:

    def test_valid_domains_count(self):
        from canary.services.alx.memory import _VALID_DOMAINS

        assert len(_VALID_DOMAINS) == 11

    def test_all_domains_present(self):
        from canary.services.alx.memory import _VALID_DOMAINS

        expected = {
            "identity", "tsp", "chirp", "alert", "owl",
            "fox", "analytics", "alx", "raas", "ops", "ui_bff",
        }
        assert _VALID_DOMAINS == expected

    def test_valid_block_types(self):
        from canary.services.alx.memory import _VALID_BLOCK_TYPES

        expected = {"domain_overview", "workflow", "data_model", "api_contract"}
        assert _VALID_BLOCK_TYPES == expected
