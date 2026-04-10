"""Ollama vision API client for blueprint analysis."""
from __future__ import annotations

import base64
import os
import httpx
from pathlib import Path

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
DEFAULT_VISION_MODEL = os.environ.get("ARC_VISION_MODEL", "llava:34b")


def analyze_image(
    image_path: Path,
    prompt: str,
    model: str = DEFAULT_VISION_MODEL,
    timeout: float = 120.0,
) -> dict:
    """Send an image to Ollama vision model with a prompt.
    Returns: {"response": str, "model": str, "done": bool}
    """
    image_data = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    payload = {
        "model": model,
        "prompt": prompt,
        "images": [image_data],
        "stream": False,
    }
    with httpx.Client(timeout=timeout) as client:
        resp = client.post(f"{OLLAMA_URL}/api/generate", json=payload)
        resp.raise_for_status()
        return resp.json()


def check_model_available(model: str = DEFAULT_VISION_MODEL) -> bool:
    """Check if the vision model is available in Ollama."""
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(f"{OLLAMA_URL}/api/tags")
            resp.raise_for_status()
            models = [m["name"] for m in resp.json().get("models", [])]
            return any(model in m for m in models)
    except httpx.HTTPError:
        return False
