"""Tests for arc.model.builder — model synthesis via Ollama text model.

Ollama calls are mocked so these tests run offline.
"""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from arc.model.builder import (
    ModelBuilder,
    _extract_json,
    _format_extractions_text,
    group_by_sheet_type,
    load_extractions,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

MINIMAL_EXTRACTIONS = [
    {
        "sheet_type": "floor_plan",
        "scale": "1/4 inch = 1 foot",
        "_source_file": "page_01_extraction.json",
        "dimensions": [
            {
                "description": "south wall width",
                "value_ft": 24.0,
                "value_raw": "24'-0\"",
                "confidence": 0.9,
                "location": "bottom",
            },
            {
                "description": "west wall depth",
                "value_ft": 18.0,
                "value_raw": "18'-0\"",
                "confidence": 0.85,
                "location": "left",
            },
        ],
        "notes": [],
    },
    {
        "sheet_type": "elevation",
        "scale": "1/4 inch = 1 foot",
        "_source_file": "page_04_extraction.json",
        "dimensions": [
            {
                "description": "plate height",
                "value_ft": 8.0,
                "value_raw": "8'-0\"",
                "confidence": 0.95,
                "location": "left margin",
            }
        ],
        "notes": [],
    },
]

MINIMAL_SPATIAL_MODEL = {
    "schema_version": 1,
    "project": "test_house",
    "address": "1 Test St",
    "coordinate_system": {"x": "east", "y": "north", "z": "up", "origin": "SW corner"},
    "lot": {"boundaries": [], "setbacks": {"front": 20.0, "side": 5.0, "rear": 15.0}},
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
                        "polygon": [[0, 0], [24, 0], [24, 18], [0, 18]],
                        "wall_refs": ["wall_s", "wall_e", "wall_n", "wall_w"],
                    }
                ],
                "walls": [
                    {"id": "wall_s", "type": "exterior", "from": [0, 0], "to": [24, 0],
                     "thickness_in": 5.5, "rooms": {"interior": "living_room", "exterior": None}},
                    {"id": "wall_n", "type": "exterior", "from": [0, 18], "to": [24, 18],
                     "thickness_in": 5.5, "rooms": {"interior": "living_room", "exterior": None}},
                    {"id": "wall_w", "type": "exterior", "from": [0, 0], "to": [0, 18],
                     "thickness_in": 5.5, "rooms": {"interior": "living_room", "exterior": None}},
                    {"id": "wall_e", "type": "exterior", "from": [24, 0], "to": [24, 18],
                     "thickness_in": 5.5, "rooms": {"interior": "living_room", "exterior": None}},
                ],
            }
        ]
    },
    "sources": [{"id": "blueprint_1", "type": "blueprint", "file": "test.pdf", "page": 1}],
}


# ---------------------------------------------------------------------------
# _extract_json
# ---------------------------------------------------------------------------

def test_extract_json_plain():
    raw = '{"a": 1, "b": [1, 2]}'
    assert _extract_json(raw) == {"a": 1, "b": [1, 2]}


def test_extract_json_strips_markdown_fences():
    raw = "```json\n{\"x\": 42}\n```"
    assert _extract_json(raw) == {"x": 42}


def test_extract_json_with_preamble():
    raw = "Here is the JSON:\n{\"key\": \"value\"}\nEnd."
    assert _extract_json(raw) == {"key": "value"}


def test_extract_json_raises_on_garbage():
    with pytest.raises(ValueError, match="Could not parse JSON"):
        _extract_json("No JSON here at all.")


# ---------------------------------------------------------------------------
# group_by_sheet_type
# ---------------------------------------------------------------------------

def test_group_by_sheet_type():
    exts = [
        {"sheet_type": "floor_plan"},
        {"sheet_type": "elevation"},
        {"sheet_type": "floor_plan"},
    ]
    groups = group_by_sheet_type(exts)
    assert set(groups.keys()) == {"floor_plan", "elevation"}
    assert len(groups["floor_plan"]) == 2
    assert len(groups["elevation"]) == 1


def test_group_by_sheet_type_unknown_fallback():
    exts = [{"other_field": "x"}]   # no sheet_type key
    groups = group_by_sheet_type(exts)
    assert "unknown" in groups


# ---------------------------------------------------------------------------
# _format_extractions_text
# ---------------------------------------------------------------------------

def test_format_extractions_text_contains_descriptions():
    text = _format_extractions_text(MINIMAL_EXTRACTIONS)
    assert "south wall width" in text
    assert "plate height" in text
    assert "FLOOR_PLAN" in text
    assert "ELEVATION" in text


def test_format_extractions_text_shows_confidence():
    text = _format_extractions_text(MINIMAL_EXTRACTIONS)
    assert "0.90" in text or "0.9" in text


# ---------------------------------------------------------------------------
# load_extractions
# ---------------------------------------------------------------------------

def test_load_extractions(tmp_path):
    ext = {"sheet_type": "floor_plan", "dimensions": [], "notes": []}
    (tmp_path / "sheet1_extraction.json").write_text(json.dumps(ext))
    (tmp_path / "sheet2_extraction.json").write_text(json.dumps(ext))
    # Non-extraction file should be ignored
    (tmp_path / "spatial_model.json").write_text("{}")

    result = load_extractions(tmp_path)
    assert len(result) == 2
    assert all("_source_file" in r for r in result)
    names = {r["_source_file"] for r in result}
    assert "sheet1_extraction.json" in names


def test_load_extractions_empty_dir(tmp_path):
    result = load_extractions(tmp_path)
    assert result == []


# ---------------------------------------------------------------------------
# ModelBuilder.synthesize_from_extractions (mocked LLM)
# ---------------------------------------------------------------------------

MOCK_SYNTHESIS_RESPONSE = json.dumps(MINIMAL_SPATIAL_MODEL)


@patch("arc.model.builder._call_ollama_text", return_value=MOCK_SYNTHESIS_RESPONSE)
def test_synthesize_returns_dict(mock_llm):
    builder = ModelBuilder(model="llama3.1")
    result = builder.synthesize_from_extractions(MINIMAL_EXTRACTIONS)
    assert result["schema_version"] == 1
    assert "structure" in result
    mock_llm.assert_called_once()


@patch("arc.model.builder._call_ollama_text", return_value=MOCK_SYNTHESIS_RESPONSE)
def test_synthesize_prompt_includes_extractions(mock_llm):
    builder = ModelBuilder()
    builder.synthesize_from_extractions(MINIMAL_EXTRACTIONS)
    prompt_used = mock_llm.call_args[0][0]
    assert "south wall width" in prompt_used
    assert "plate height" in prompt_used


@patch("arc.model.builder._call_ollama_text", return_value=MOCK_SYNTHESIS_RESPONSE)
def test_synthesize_prompt_includes_schema(mock_llm):
    builder = ModelBuilder()
    builder.synthesize_from_extractions(MINIMAL_EXTRACTIONS)
    prompt_used = mock_llm.call_args[0][0]
    assert "schema_version" in prompt_used
    assert "plate_height" in prompt_used


# ---------------------------------------------------------------------------
# ModelBuilder.reconcile (mocked LLM)
# ---------------------------------------------------------------------------

MOCK_RECONCILE_RESPONSE = json.dumps({
    "matches": [{"entity": "floor_0", "field": "plate_height", "model_value": 8.0,
                 "extracted_value": 8.0, "notes": "exact match"}],
    "conflicts": [],
    "additions": [],
    "summary": "All extracted dimensions match the existing model.",
})


@patch("arc.model.builder._call_ollama_text", return_value=MOCK_RECONCILE_RESPONSE)
def test_reconcile_returns_report(mock_llm):
    builder = ModelBuilder()
    report = builder.reconcile(MINIMAL_EXTRACTIONS, MINIMAL_SPATIAL_MODEL)
    assert "matches" in report
    assert "conflicts" in report
    assert "additions" in report
    assert "summary" in report


@patch("arc.model.builder._call_ollama_text", return_value=MOCK_RECONCILE_RESPONSE)
def test_reconcile_prompt_includes_existing_model(mock_llm):
    builder = ModelBuilder()
    builder.reconcile(MINIMAL_EXTRACTIONS, MINIMAL_SPATIAL_MODEL)
    prompt_used = mock_llm.call_args[0][0]
    assert "wall_s" in prompt_used or "living_room" in prompt_used


# ---------------------------------------------------------------------------
# ModelBuilder.build — file I/O (mocked LLM)
# ---------------------------------------------------------------------------

@patch("arc.model.builder._call_ollama_text", return_value=MOCK_SYNTHESIS_RESPONSE)
def test_build_writes_spatial_model(mock_llm, tmp_path):
    extract_dir = tmp_path / "extractions"
    extract_dir.mkdir()
    ext = {
        "sheet_type": "floor_plan",
        "scale": "1/4\" = 1'",
        "dimensions": [{"description": "south wall", "value_ft": 24.0,
                        "value_raw": "24'", "confidence": 0.9, "location": "bottom"}],
        "notes": [],
    }
    (extract_dir / "page01_extraction.json").write_text(json.dumps(ext))

    builder = ModelBuilder()
    builder.build(tmp_path)

    out = tmp_path / "model" / "spatial_model.json"
    assert out.exists()
    data = json.loads(out.read_text())
    assert data["schema_version"] == 1


@patch("arc.model.builder._call_ollama_text", return_value=MOCK_SYNTHESIS_RESPONSE)
def test_build_dry_run_does_not_write(mock_llm, tmp_path):
    extract_dir = tmp_path / "extractions"
    extract_dir.mkdir()
    (extract_dir / "x_extraction.json").write_text(json.dumps({
        "sheet_type": "floor_plan", "scale": "?", "dimensions": [], "notes": []}))

    builder = ModelBuilder()
    builder.build(tmp_path, dry_run=True)

    assert not (tmp_path / "model" / "spatial_model.json").exists()


def test_build_raises_if_no_extractions_dir(tmp_path):
    builder = ModelBuilder()
    with pytest.raises(FileNotFoundError, match="extractions"):
        builder.build(tmp_path)
