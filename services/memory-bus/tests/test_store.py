"""Tests for MemoryStore — exercises actual memory_bus service operations."""

import json
import os
import pytest
from unittest.mock import patch, MagicMock

from memory_bus.config import Config
from memory_bus.store import MemoryStore


@pytest.fixture
def mock_config():
    """Config with test database URL."""
    config = Config.__new__(Config)
    config.database_url = os.environ.get(
        "DATABASE_URL",
        "postgresql://growdirect:growdirect_dev@localhost:5432/growdirect_memory_test",
    )
    config.ollama_url = "http://localhost:11434"
    config.embedding_model = "qwen3-embedding:8b"
    config.port = 8003
    config.embedding_dimensions = 1024
    config.max_text_length = 6000
    config.mcp_api_key = ""
    return config


@pytest.fixture
def store(mock_config):
    """MemoryStore instance for testing."""
    return MemoryStore(mock_config)


class TestSessionLifecycle:
    """Test session_start and session_close."""

    @pytest.mark.postgres
    def test_session_start_returns_session_id(self, store):
        result = store.session_start(gro_issues=["GRO-999"])
        assert "session_id" in result
        assert result["status"] == "active"

    @pytest.mark.postgres
    def test_session_close_sets_summary(self, store):
        start = store.session_start()
        sid = start["session_id"]
        result = store.session_close(sid, summary="Test session done")
        assert result["status"] == "closed"
        assert result["summary"] == "Test session done"


class TestMemoryStore:
    """Test memory_store and memory_recall."""

    @pytest.mark.postgres
    def test_store_memory_returns_id(self, store):
        start = store.session_start()
        sid = start["session_id"]
        with patch("memory_bus.store.get_embedding", return_value=None):
            result = store.memory_store(
                session_id=sid,
                content="Test memory content",
                memory_type="context",
                layer="shared",
            )
        assert "memory_id" in result

    @pytest.mark.postgres
    def test_store_rejects_invalid_type(self, store):
        start = store.session_start()
        sid = start["session_id"]
        result = store.memory_store(
            session_id=sid,
            content="Test",
            memory_type="invalid_type",
        )
        assert "error" in result

    @pytest.mark.postgres
    def test_recall_returns_results(self, store):
        start = store.session_start()
        sid = start["session_id"]
        with patch("memory_bus.store.get_embedding", return_value=None):
            store.memory_store(session_id=sid, content="Unique recall test content xyz123")
        result = store.memory_recall(query="xyz123", limit=5)
        assert "matches" in result


class TestContextAssemble:
    """Test context_assemble."""

    @pytest.mark.postgres
    def test_context_assemble_returns_dict(self, store):
        result = store.context_assemble(topic="test")
        assert isinstance(result, dict)
