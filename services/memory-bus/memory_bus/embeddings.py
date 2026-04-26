# GrowDirect LLC — Confidential & Proprietary
# Copyright (c) 2026 GrowDirect LLC. All rights reserved.
import logging
from typing import Optional

import httpx

from memory_bus.config import Config

logger = logging.getLogger(__name__)


def get_embedding(text: str, config: Config) -> Optional[list[float]]:
    """Generate embedding vector via Ollama. Returns None if unavailable."""
    truncated = text[: config.max_text_length]
    try:
        response = httpx.post(
            f"{config.ollama_url}/api/embed",
            json={"model": config.embedding_model, "input": truncated},
            timeout=120.0,
        )
        response.raise_for_status()
        data = response.json()
        # Ollama /api/embed returns "embeddings" (array of arrays)
        embedding = data["embeddings"][0]
        # Matryoshka truncation: native 4096d -> 1024d
        return [float(v) for v in embedding[: config.embedding_dimensions]]
    except Exception:
        logger.warning("Embedding generation failed — storing without vector")
        return None
