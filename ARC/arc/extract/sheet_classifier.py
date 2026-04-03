"""Classify blueprint sheet type using vision AI."""
from __future__ import annotations
from pathlib import Path
from arc.llm.vision import analyze_image

CLASSIFY_PROMPT = """Look at this architectural drawing and classify it.
Return ONLY one of: floor_plan, foundation_plan, elevation, section, site_plan, interior_elevation, detail, hvac, electrical, schedule"""


def classify_sheet(image_path: Path, model: str | None = None) -> str:
    kwargs = {"image_path": image_path, "prompt": CLASSIFY_PROMPT}
    if model:
        kwargs["model"] = model
    result = analyze_image(**kwargs)
    response = result.get("response", "").strip().lower()
    valid = {"floor_plan", "foundation_plan", "elevation", "section", "site_plan",
             "interior_elevation", "detail", "hvac", "electrical", "schedule"}
    return response if response in valid else "unknown"
