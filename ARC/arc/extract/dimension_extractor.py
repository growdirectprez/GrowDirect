"""Extract dimensions from blueprint images using Ollama vision."""
from __future__ import annotations
import json
from pathlib import Path
from arc.llm.vision import analyze_image

DIMENSION_PROMPT = """You are an architectural draftsman reading a blueprint scan.

Analyze this architectural drawing and extract ALL dimensions you can read.
For each dimension, provide:
- description: what the dimension measures
- value_ft: the dimension in feet (convert from feet-inches notation)
- value_raw: the original notation as written on the drawing
- confidence: 0.0-1.0 how confident you are in the reading
- location: where on the drawing

Return ONLY valid JSON:
{
  "sheet_type": "floor_plan" | "elevation" | "section" | "site_plan" | "foundation",
  "scale": "1/4 inch = 1 foot" or similar,
  "dimensions": [
    {"description": "...", "value_ft": 41.58, "value_raw": "41'-7\\"", "confidence": 0.7, "location": "..."}
  ],
  "notes": ["any observations about scan quality"]
}
"""


def extract_dimensions(image_path: Path, model: str | None = None) -> dict:
    kwargs = {"image_path": image_path, "prompt": DIMENSION_PROMPT}
    if model:
        kwargs["model"] = model
    result = analyze_image(**kwargs)
    response_text = result.get("response", "")
    try:
        start = response_text.index("{")
        end = response_text.rindex("}") + 1
        return json.loads(response_text[start:end])
    except (ValueError, json.JSONDecodeError):
        return {
            "sheet_type": "unknown", "scale": "unknown", "dimensions": [],
            "notes": [f"Failed to parse: {response_text[:200]}"],
            "raw_response": response_text,
        }


def save_extraction(data: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, indent=2) + "\n")
