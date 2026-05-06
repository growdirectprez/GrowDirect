# GrowDirect LLC — Confidential & Proprietary
# Copyright (c) 2026 GrowDirect LLC. All rights reserved.
import logging
import os
from typing import Optional

import httpx

from memory_bus.config import Config

logger = logging.getLogger(__name__)

_vertex_credentials = None


def _vertex_token() -> str:
    global _vertex_credentials
    import google.auth
    import google.auth.transport.requests
    if _vertex_credentials is None:
        _vertex_credentials, _ = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
    req = google.auth.transport.requests.Request()
    _vertex_credentials.refresh(req)
    return _vertex_credentials.token


def get_embedding(text: str, config: Config) -> Optional[list[float]]:
    """Generate embedding vector. Uses Vertex AI REST when EMBED_BACKEND=vertex, else Ollama."""
    truncated = text[: config.max_text_length]
    backend = os.environ.get("EMBED_BACKEND", "ollama")
    try:
        if backend == "vertex":
            project = os.environ.get("GOOGLE_CLOUD_PROJECT", "growdirect-mercury")
            region = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")
            token = _vertex_token()
            url = (
                f"https://{region}-aiplatform.googleapis.com/v1"
                f"/projects/{project}/locations/{region}"
                f"/publishers/google/models/{config.embedding_model}:predict"
            )
            r = httpx.post(
                url,
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                json={"instances": [{"content": truncated}]},
                timeout=60.0,
            )
            r.raise_for_status()
            values = r.json()["predictions"][0]["embeddings"]["values"]
            return [float(v) for v in values[: config.embedding_dimensions]]
        else:
            response = httpx.post(
                f"{config.ollama_url}/api/embed",
                json={"model": config.embedding_model, "input": truncated},
                timeout=120.0,
            )
            response.raise_for_status()
            data = response.json()
            embedding = data["embeddings"][0]
            return [float(v) for v in embedding[: config.embedding_dimensions]]
    except Exception:
        logger.warning("Embedding generation failed — storing without vector")
        return None
