"""Build a spatial model from extraction JSON files using an Ollama text model.

Usage:
    from arc.model.builder import ModelBuilder
    builder = ModelBuilder()
    model_dict = builder.build(project_dir)          # synthesize from scratch
    model_dict = builder.build(project_dir,          # reconcile against existing
                               existing_model_path=...)
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Optional

import httpx

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("ARC_MODEL_MODEL", "llama3.1")

# ---------------------------------------------------------------------------
# Schema reference embedded in prompts
# ---------------------------------------------------------------------------

_SCHEMA_REFERENCE = """\
SPATIAL MODEL JSON SCHEMA (schema_version: 1)
=============================================
Coordinate system: X = east, Y = north, Z = up. Origin = SW corner of house.
All linear values are in FEET except fields ending in _in which are in INCHES.

Top-level structure:
{
  "schema_version": 1,
  "project": "<name>",
  "address": "<address>",
  "coordinate_system": {"x": "east", "y": "north", "z": "up", "origin": "SW corner of original house"},
  "lot": {
    "boundaries": [[x, y], ...],
    "setbacks": {"front": <ft>, "side": <ft>, "rear": <ft>},
    "apn": "<string or null>"
  },
  "structure": {
    "floors": [
      {
        "level": 0,
        "label": "Ground Floor",
        "plate_height": 8.0,
        "z_origin": 0.0,
        "rooms": [
          {
            "id": "living_room",
            "label": "Living Room",
            "polygon": [[x,y], [x,y], [x,y], [x,y]],
            "wall_refs": ["wall_id_1", "wall_id_2"],
            "sources": [{"ref": "<source_id>", "confidence": 0.8}]
          }
        ],
        "walls": [
          {
            "id": "wall_s_living",
            "type": "exterior",
            "from": [x, y],
            "to": [x, y],
            "thickness_in": 5.5,
            "rooms": {"interior": "living_room", "exterior": null},
            "openings": [
              {
                "type": "window",
                "position_along_wall": 2.0,
                "width": 4.0,
                "height": 4.0,
                "sill_height": 2.5
              }
            ],
            "sources": [{"ref": "<source_id>", "confidence": 0.8}]
          }
        ],
        "structural": {
          "posts": [{"position": [x, y], "size_in": 4.0, "material": "douglas_fir", "z_base": 0.0}],
          "beams": [{"from": [x, y], "to": [x, y], "width_in": 4.0, "depth_in": 8.0, "z": 8.0, "material": "douglas_fir"}]
        }
      }
    ]
  },
  "sources": [
    {"id": "<id>", "type": "blueprint", "file": "<filename>", "page": 1}
  ],
  "roof": {
    "planes": [
      {
        "label": "Main Roof",
        "type": "flat",
        "slope": 0.0,
        "overhang": 2.0,
        "boundary": [[x,y], [x,y], [x,y], [x,y]],
        "z_base": 8.0
      }
    ]
  }
}

WALL RULES:
- "from" and "to" are [x, y] in feet from the SW origin
- thickness_in: exterior walls = 5.5 in (2x6 framing) or 3.5 in (2x4); interior = 3.5 in
- Wall IDs should be descriptive: "wall_s_living", "wall_n_kitchen", etc.
- openings: position_along_wall = distance from wall's "from" point along its length
- Doors: sill_height = 0.0; Windows: sill_height typically 2.0–3.0 ft

ROOM RULES:
- polygon is a list of [x, y] corner points (counter-clockwise, SW corner first)
- wall_refs lists wall IDs that form the room's perimeter

FLOOR RULES:
- level 0 = ground floor, 1 = upper floor, -1 = basement
- z_origin = floor slab elevation in feet
- plate_height = wall height from slab to top of wall plate
"""

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

_SYNTHESIS_PROMPT_TEMPLATE = """\
You are an architectural draftsman converting extracted blueprint dimensions into a structured spatial model.

{schema}

EXTRACTED BLUEPRINT DATA
========================
{extractions_text}

TASK
====
Using the extracted dimensions above, produce a complete and valid spatial_model.json.

Rules:
1. Place the SW corner of the house at origin [0, 0].
2. Use the floor plan sheet as the primary source for room layout and wall coordinates.
3. Use elevation sheets for plate height, window sill heights, and roof geometry.
4. Use the foundation sheet for z_origin and foundation details.
5. Group wall IDs consistently (name them after their compass direction and room).
6. Set "sources" on walls and rooms referencing the sheet the dimension came from.
7. If a dimension is ambiguous or contradicts another, use the higher-confidence value and note the conflict in the wall's "conflicts" array.
8. Omit sections you have no data for (e.g., omit "roof" if no elevation data was extracted).

Return ONLY valid JSON — no explanation, no markdown fences, no preamble.
"""

_RECONCILE_PROMPT_TEMPLATE = """\
You are an architectural draftsman reviewing new blueprint extractions against an existing spatial model.

{schema}

EXISTING SPATIAL MODEL
======================
{existing_model_text}

NEW EXTRACTION DATA
===================
{extractions_text}

TASK
====
Compare the extraction data against the existing model. Produce a reconciliation report as JSON:

{{
  "matches": [
    {{"entity": "<wall_id or room_id>", "field": "<field>", "model_value": ..., "extracted_value": ..., "notes": "..."}}
  ],
  "conflicts": [
    {{"entity": "<wall_id or room_id>", "field": "<field>", "model_value": ..., "extracted_value": ..., "severity": "low|medium|high", "recommendation": "..."}}
  ],
  "additions": [
    {{"description": "...", "suggested_json": {{...}}}}
  ],
  "summary": "Brief plain-English summary of findings."
}}

Return ONLY valid JSON — no explanation, no markdown fences.
"""


# ---------------------------------------------------------------------------
# Ollama text API
# ---------------------------------------------------------------------------

def _call_ollama_text(prompt: str, model: str = DEFAULT_MODEL, timeout: float = 180.0) -> str:
    """Send a text prompt to Ollama. Returns the response string."""
    payload = {"model": model, "prompt": prompt, "stream": False}
    with httpx.Client(timeout=timeout) as client:
        resp = client.post(f"{OLLAMA_URL}/api/generate", json=payload)
        resp.raise_for_status()
        return resp.json().get("response", "")


def _extract_json(text: str) -> dict:
    """Pull the first JSON object out of a text response."""
    # Strip markdown code fences if present
    text = re.sub(r"```(?:json)?\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return json.loads(text[start:end])
    except (ValueError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not parse JSON from LLM response: {exc}\n---\n{text[:500]}") from exc


# ---------------------------------------------------------------------------
# Extraction loading helpers
# ---------------------------------------------------------------------------

def load_extractions(extract_dir: Path) -> list[dict]:
    """Load all *_extraction.json files from extract_dir, sorted by name."""
    files = sorted(extract_dir.glob("*_extraction.json"))
    results = []
    for f in files:
        data = json.loads(f.read_text())
        data["_source_file"] = f.name
        results.append(data)
    return results


def group_by_sheet_type(extractions: list[dict]) -> dict[str, list[dict]]:
    """Group extraction dicts by their sheet_type field."""
    groups: dict[str, list[dict]] = {}
    for ext in extractions:
        sheet_type = ext.get("sheet_type", "unknown")
        groups.setdefault(sheet_type, []).append(ext)
    return groups


def _format_extractions_text(extractions: list[dict]) -> str:
    """Format extractions into a readable text block for LLM prompts."""
    grouped = group_by_sheet_type(extractions)
    lines = []
    for sheet_type, exts in sorted(grouped.items()):
        lines.append(f"\n## Sheet type: {sheet_type.upper()}")
        for ext in exts:
            src = ext.get("_source_file", "unknown")
            scale = ext.get("scale", "unknown")
            lines.append(f"\nSource: {src}  Scale: {scale}")
            dims = ext.get("dimensions", [])
            if not dims:
                lines.append("  (no dimensions extracted)")
                continue
            for d in dims:
                conf = d.get("confidence", 0.0)
                conf_str = f"{conf:.2f}"
                raw = d.get("value_raw", "")
                val_ft = d.get("value_ft", "?")
                desc = d.get("description", "")
                loc = d.get("location", "")
                lines.append(f"  [{conf_str}] {desc}: {raw} ({val_ft} ft)  @ {loc}")
            for note in ext.get("notes", []):
                lines.append(f"  NOTE: {note}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# ModelBuilder
# ---------------------------------------------------------------------------

class ModelBuilder:
    """Orchestrate extraction → spatial model synthesis via Ollama."""

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build(
        self,
        project_dir: Path,
        existing_model_path: Optional[Path] = None,
        dry_run: bool = False,
    ) -> dict:
        """Synthesize or reconcile spatial model from extractions.

        Args:
            project_dir:         Path to the project directory (contains extractions/).
            existing_model_path: If provided, run in reconciliation mode.
            dry_run:             If True, return the result dict without writing.

        Returns:
            dict — the synthesized spatial_model dict (synthesis mode)
                   or the reconciliation report dict (reconcile mode).
        """
        extract_dir = project_dir / "extractions"
        if not extract_dir.exists():
            raise FileNotFoundError(
                f"No extractions directory at {extract_dir}. "
                "Run 'arc extract <project>' first."
            )

        extractions = load_extractions(extract_dir)
        if not extractions:
            raise ValueError(f"No extraction files found in {extract_dir}.")

        if existing_model_path and existing_model_path.exists():
            result = self._reconcile(extractions, existing_model_path)
        else:
            result = self._synthesize(extractions, project_dir)

        if not dry_run:
            model_dir = project_dir / "model"
            model_dir.mkdir(parents=True, exist_ok=True)
            if existing_model_path and existing_model_path.exists():
                out_path = project_dir / "model" / "reconciliation_report.json"
            else:
                out_path = project_dir / "model" / "spatial_model.json"
            out_path.write_text(json.dumps(result, indent=2) + "\n")

        return result

    def synthesize_from_extractions(self, extractions: list[dict]) -> dict:
        """Call LLM to synthesize a spatial model dict from extraction data.
        Exposed for testing (inject mock extractions).
        """
        return self._synthesize_raw(extractions)

    def reconcile(self, extractions: list[dict], existing_model: dict) -> dict:
        """Call LLM to produce a reconciliation report.
        Exposed for testing.
        """
        return self._reconcile_raw(extractions, existing_model)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _synthesize(self, extractions: list[dict], project_dir: Path) -> dict:
        result = self._synthesize_raw(extractions)
        # Inject source records for each extraction file found
        sources = result.setdefault("sources", [])
        existing_ids = {s.get("id") for s in sources}
        for ext in extractions:
            src_file = ext.get("_source_file", "")
            src_id = src_file.replace("_extraction.json", "")
            if src_id and src_id not in existing_ids:
                sources.append({
                    "id": src_id,
                    "type": "blueprint",
                    "file": src_file,
                })
                existing_ids.add(src_id)
        return result

    def _synthesize_raw(self, extractions: list[dict]) -> dict:
        extractions_text = _format_extractions_text(extractions)
        prompt = _SYNTHESIS_PROMPT_TEMPLATE.format(
            schema=_SCHEMA_REFERENCE,
            extractions_text=extractions_text,
        )
        response = _call_ollama_text(prompt, model=self.model)
        return _extract_json(response)

    def _reconcile(self, extractions: list[dict], existing_model_path: Path) -> dict:
        existing_model = json.loads(existing_model_path.read_text())
        return self._reconcile_raw(extractions, existing_model)

    def _reconcile_raw(self, extractions: list[dict], existing_model: dict) -> dict:
        extractions_text = _format_extractions_text(extractions)
        existing_model_text = json.dumps(existing_model, indent=2)
        prompt = _RECONCILE_PROMPT_TEMPLATE.format(
            schema=_SCHEMA_REFERENCE,
            existing_model_text=existing_model_text,
            extractions_text=extractions_text,
        )
        response = _call_ollama_text(prompt, model=self.model)
        return _extract_json(response)


# ---------------------------------------------------------------------------
# Convenience function for CLI
# ---------------------------------------------------------------------------

def build_model(
    project_dir: Path,
    model: str = DEFAULT_MODEL,
    reconcile: bool = False,
    dry_run: bool = False,
) -> tuple[dict, Path | None]:
    """High-level entry point used by the CLI.

    Returns:
        (result_dict, output_path) — output_path is None when dry_run=True.
    """
    builder = ModelBuilder(model=model)
    model_dir = project_dir / "model"
    existing_path = model_dir / "spatial_model.json"

    if reconcile:
        if not existing_path.exists():
            raise FileNotFoundError(
                f"No existing model at {existing_path}. "
                "Cannot reconcile — run without --reconcile first to synthesize."
            )
        result = builder.build(project_dir, existing_model_path=existing_path, dry_run=dry_run)
        out_path = None if dry_run else model_dir / "reconciliation_report.json"
    else:
        result = builder.build(project_dir, dry_run=dry_run)
        out_path = None if dry_run else model_dir / "spatial_model.json"

    return result, out_path
