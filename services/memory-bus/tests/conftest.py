# GrowDirect LLC — Confidential & Proprietary
# Copyright (c) 2026 GrowDirect LLC. All rights reserved.
import os

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/growdirect_memory_test",
)
os.environ.setdefault("OLLAMA_URL", "http://growdirect_ollama:11434")
os.environ.setdefault("EMBEDDING_MODEL", "qwen3-embedding:8b")
