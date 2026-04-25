# GrowDirect LLC — Confidential & Proprietary
# Copyright (c) 2026 GrowDirect LLC. All rights reserved.
import os


class Config:
    """Environment-based configuration for the memory bus."""

    def __init__(self):
        self.database_url: str = os.environ["DATABASE_URL"]
        self.ollama_url: str = os.environ.get(
            "OLLAMA_URL", "http://growdirect_ollama:11434"
        )
        self.embedding_model: str = os.environ.get(
            "EMBEDDING_MODEL", "qwen3-embedding:8b"
        )
        self.port: int = int(os.environ.get("PORT", "8003"))
        self.embedding_dimensions: int = 1024
        self.max_text_length: int = 6000
        self.mcp_api_key: str = os.environ.get("MCP_API_KEY", "")
