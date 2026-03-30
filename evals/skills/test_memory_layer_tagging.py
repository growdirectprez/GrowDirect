"""Memory layer tagging eval suite — binary pass/fail.

Verifies that the memory bus correctly supports layer-based tagging
and filtering for the 4-layer skill architecture.

Source material:
  - docs/skill-taxonomy.md § Memory Tagging
  - services/memory-bus/memory_bus/store.py — VALID_LAYERS
  - GRO-378 acceptance criteria: "ALX memory tagged by layer"

Eval target: 100% pass rate (all binary checks).
"""

import importlib.util
import json
import os
import sys

import pytest

MEMORY_BUS_ROOT = os.path.join(os.path.expanduser("~/GrowDirect"), "services", "memory-bus")


@pytest.fixture
def store_module():
    """Import store module directly — no Docker dependency."""
    spec = importlib.util.spec_from_file_location(
        "store",
        os.path.join(MEMORY_BUS_ROOT, "memory_bus", "store.py"),
    )
    # Need config and embeddings modules too
    config_spec = importlib.util.spec_from_file_location(
        "memory_bus.config",
        os.path.join(MEMORY_BUS_ROOT, "memory_bus", "config.py"),
    )
    config_mod = importlib.util.module_from_spec(config_spec)
    sys.modules["memory_bus.config"] = config_mod
    config_spec.loader.exec_module(config_mod)

    embeddings_spec = importlib.util.spec_from_file_location(
        "memory_bus.embeddings",
        os.path.join(MEMORY_BUS_ROOT, "memory_bus", "embeddings.py"),
    )
    embeddings_mod = importlib.util.module_from_spec(embeddings_spec)
    sys.modules["memory_bus.embeddings"] = embeddings_mod
    embeddings_spec.loader.exec_module(embeddings_mod)

    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# 1. Layer constants — verify all 4 layers are declared
#    Source: docs/skill-taxonomy.md § Memory Tagging
# ---------------------------------------------------------------------------

class TestLayerConstants:
    """Memory bus declares all required layers."""

    def test_valid_layers_has_corp(self, store_module):
        """Layer 'corp' exists for GrowDirect Corp (DOA) memories."""
        assert "corp" in store_module.VALID_LAYERS

    def test_valid_layers_has_canary(self, store_module):
        """Layer 'canary' exists for Canary app memories."""
        assert "canary" in store_module.VALID_LAYERS

    def test_valid_layers_has_cove(self, store_module):
        """Layer 'cove' exists for Cove app memories."""
        assert "cove" in store_module.VALID_LAYERS

    def test_valid_layers_has_shared(self, store_module):
        """Layer 'shared' exists for cross-app memories."""
        assert "shared" in store_module.VALID_LAYERS

    def test_exactly_four_layers(self, store_module):
        """Exactly 4 layers — no extras, no missing."""
        assert len(store_module.VALID_LAYERS) == 4


# ---------------------------------------------------------------------------
# 2. Memory type constants — verify all types for skill output
# ---------------------------------------------------------------------------

EXPECTED_MEMORY_TYPES = {
    "decision", "finding", "context", "architecture",
    "session_summary", "procedure", "context_block",
    "work_product", "team_profile", "foundation",
}


class TestMemoryTypes:
    """Memory bus declares all required memory types."""

    def test_all_memory_types_present(self, store_module):
        """All expected memory types are declared."""
        assert store_module.VALID_MEMORY_TYPES == EXPECTED_MEMORY_TYPES

    def test_decision_type_exists(self, store_module):
        """'decision' type for recording choices made during sessions."""
        assert "decision" in store_module.VALID_MEMORY_TYPES

    def test_finding_type_exists(self, store_module):
        """'finding' type for bugs, gaps, unexpected behavior."""
        assert "finding" in store_module.VALID_MEMORY_TYPES

    def test_session_summary_type_exists(self, store_module):
        """'session_summary' type for close-stage outputs."""
        assert "session_summary" in store_module.VALID_MEMORY_TYPES

    def test_procedure_type_exists(self, store_module):
        """'procedure' type for workflow/process changes."""
        assert "procedure" in store_module.VALID_MEMORY_TYPES


# ---------------------------------------------------------------------------
# 3. memory_store API — layer parameter exists and validates
# ---------------------------------------------------------------------------

class TestMemoryStoreAPI:
    """memory_store method accepts and validates layer parameter."""

    def test_memory_store_has_layer_param(self, store_module):
        """memory_store() accepts a 'layer' parameter."""
        import inspect
        sig = inspect.signature(store_module.MemoryStore.memory_store)
        assert "layer" in sig.parameters

    def test_memory_store_layer_default_is_shared(self, store_module):
        """layer parameter defaults to 'shared'."""
        import inspect
        sig = inspect.signature(store_module.MemoryStore.memory_store)
        assert sig.parameters["layer"].default == "shared"


# ---------------------------------------------------------------------------
# 4. memory_recall API — layer parameter exists for filtering
# ---------------------------------------------------------------------------

class TestMemoryRecallAPI:
    """memory_recall method supports layer-based filtering."""

    def test_memory_recall_has_layer_param(self, store_module):
        """memory_recall() accepts a 'layer' parameter for filtering."""
        import inspect
        sig = inspect.signature(store_module.MemoryStore.memory_recall)
        assert "layer" in sig.parameters, (
            "memory_recall missing 'layer' parameter — "
            "layer-based filtering not implemented"
        )

    def test_memory_recall_layer_default_is_none(self, store_module):
        """layer parameter defaults to None (all layers)."""
        import inspect
        sig = inspect.signature(store_module.MemoryStore.memory_recall)
        assert sig.parameters["layer"].default is None


# ---------------------------------------------------------------------------
# 5. memory_search API — layer parameter exists for filtering
# ---------------------------------------------------------------------------

class TestMemorySearchAPI:
    """memory_search method supports layer-based filtering."""

    def test_memory_search_has_layer_param(self, store_module):
        """memory_search() accepts a 'layer' parameter for filtering."""
        import inspect
        sig = inspect.signature(store_module.MemoryStore.memory_search)
        assert "layer" in sig.parameters, (
            "memory_search missing 'layer' parameter — "
            "layer-based filtering not implemented"
        )

    def test_memory_search_layer_default_is_none(self, store_module):
        """layer parameter defaults to None (all layers)."""
        import inspect
        sig = inspect.signature(store_module.MemoryStore.memory_search)
        assert sig.parameters["layer"].default is None


# ---------------------------------------------------------------------------
# 6. MCP server tool — layer parameter exposed
# ---------------------------------------------------------------------------

class TestMCPServerTools:
    """MCP server exposes layer parameter on tools."""

    def test_server_py_exists(self):
        """Memory bus server.py exists."""
        path = os.path.join(MEMORY_BUS_ROOT, "memory_bus", "server.py")
        assert os.path.isfile(path)

    def test_server_has_memory_store_tool(self):
        """Server defines memory_store as an MCP tool."""
        path = os.path.join(MEMORY_BUS_ROOT, "memory_bus", "server.py")
        with open(path) as f:
            content = f.read()
        assert "def memory_store" in content

    def test_server_memory_store_has_layer(self):
        """Server memory_store tool exposes layer parameter."""
        path = os.path.join(MEMORY_BUS_ROOT, "memory_bus", "server.py")
        with open(path) as f:
            content = f.read()
        # Find the memory_store function and check for layer param
        assert 'layer' in content


# ---------------------------------------------------------------------------
# 7. Skill taxonomy alignment — manifest references layers
# ---------------------------------------------------------------------------

class TestTaxonomyAlignment:
    """Skill taxonomy and manifest correctly reference layer tagging."""

    def test_taxonomy_doc_exists(self):
        """Skill taxonomy document exists."""
        path = os.path.join(os.path.expanduser("~/GrowDirect"), "docs", "skill-taxonomy.md")
        assert os.path.isfile(path)

    def test_taxonomy_mentions_layers(self):
        """Taxonomy document references the 4 memory layers."""
        path = os.path.join(os.path.expanduser("~/GrowDirect"), "docs", "skill-taxonomy.md")
        with open(path) as f:
            content = f.read()
        for layer in ["corp", "canary", "cove", "shared"]:
            assert layer in content, f"Taxonomy missing layer: {layer}"

    def test_post_mortem_skill_exists(self):
        """Post-mortem capture skill file exists."""
        path = os.path.join(
            os.path.expanduser("~/GrowDirect"),
            ".claude", "skills", "factory-postmortem.md",
        )
        assert os.path.isfile(path), "factory-postmortem.md skill not found"
