# GrowDirect LLC — Confidential & Proprietary
# Copyright (c) 2026 GrowDirect LLC. All rights reserved.
import pytest
from memory_bus.config import Config


class TestConfig:
    def test_database_url_from_env(self, monkeypatch):
        monkeypatch.setenv("DATABASE_URL", "postgresql://test:test@localhost/test_db")
        config = Config()
        assert config.database_url == "postgresql://test:test@localhost/test_db"

    def test_database_url_missing_raises(self, monkeypatch):
        monkeypatch.delenv("DATABASE_URL", raising=False)
        with pytest.raises(KeyError):
            Config()

    def test_ollama_url_default(self, monkeypatch):
        monkeypatch.setenv("DATABASE_URL", "postgresql://test:test@localhost/test_db")
        monkeypatch.delenv("OLLAMA_URL", raising=False)
        config = Config()
        assert config.ollama_url == "http://growdirect_ollama:11434"

    def test_embedding_model_default(self, monkeypatch):
        monkeypatch.setenv("DATABASE_URL", "postgresql://test:test@localhost/test_db")
        config = Config()
        assert config.embedding_model == "qwen3-embedding:8b"

    def test_port_default(self, monkeypatch):
        monkeypatch.setenv("DATABASE_URL", "postgresql://test:test@localhost/test_db")
        config = Config()
        assert config.port == 8003
