"""Parse natural language descriptions into structured intent."""
from __future__ import annotations

def parse_description(text: str) -> dict:
    return {"raw_text": text, "rooms": [], "modifications": []}
