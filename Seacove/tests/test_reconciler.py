"""Tests for arc.model.reconciler — deterministic diff of extractions vs model."""
from __future__ import annotations

from arc.model.reconciler import (
    TOLERANCE_FT,
    DimensionConflict,
    DimensionMatch,
    ReconciliationResult,
    _find_best_wall_match,
    _wall_length,
    reconcile_extractions,
)

# ---------------------------------------------------------------------------
# Test model fixture
# ---------------------------------------------------------------------------

MODEL_24x18 = {
    "structure": {
        "floors": [
            {
                "level": 0,
                "label": "Ground Floor",
                "plate_height": 8.0,
                "z_origin": 0.0,
                "rooms": [],
                "walls": [
                    {"id": "wall_s", "type": "exterior",
                     "from": [0, 0], "to": [24, 0], "thickness_in": 5.5,
                     "rooms": {"interior": "living", "exterior": None}},
                    {"id": "wall_n", "type": "exterior",
                     "from": [0, 18], "to": [24, 18], "thickness_in": 5.5,
                     "rooms": {"interior": "living", "exterior": None}},
                    {"id": "wall_w", "type": "exterior",
                     "from": [0, 0], "to": [0, 18], "thickness_in": 5.5,
                     "rooms": {"interior": "living", "exterior": None}},
                    {"id": "wall_e", "type": "exterior",
                     "from": [24, 0], "to": [24, 18], "thickness_in": 5.5,
                     "rooms": {"interior": "living", "exterior": None}},
                ],
            }
        ]
    }
}


# ---------------------------------------------------------------------------
# _wall_length
# ---------------------------------------------------------------------------

def test_wall_length_horizontal():
    wall = {"from": [0, 0], "to": [24, 0]}
    assert _wall_length(wall) == 24.0


def test_wall_length_vertical():
    wall = {"from": [0, 0], "to": [0, 18]}
    assert _wall_length(wall) == 18.0


def test_wall_length_diagonal():
    wall = {"from": [0, 0], "to": [3, 4]}
    assert abs(_wall_length(wall) - 5.0) < 0.001


# ---------------------------------------------------------------------------
# _find_best_wall_match
# ---------------------------------------------------------------------------

def test_find_best_wall_match_exact():
    walls = {
        "wall_s": {"from": [0, 0], "to": [24, 0]},
        "wall_w": {"from": [0, 0], "to": [0, 18]},
    }
    match = _find_best_wall_match(24.0, "south wall width", walls)
    assert match == "wall_s"


def test_find_best_wall_match_within_tolerance():
    walls = {"wall_s": {"from": [0, 0], "to": [24, 0]}}
    # 24.1 ft is within TOLERANCE_FT (0.25 ft) of 24.0
    match = _find_best_wall_match(24.1, "south wall", walls)
    assert match == "wall_s"


def test_find_best_wall_match_outside_tolerance():
    walls = {"wall_s": {"from": [0, 0], "to": [24, 0]}}
    # 25.5 ft is 1.5 ft off — outside tolerance
    match = _find_best_wall_match(25.5, "wall length", walls)
    assert match is None


def test_find_best_wall_match_empty_index():
    assert _find_best_wall_match(24.0, "south wall", {}) is None


# ---------------------------------------------------------------------------
# reconcile_extractions — plate height
# ---------------------------------------------------------------------------

def test_plate_height_match():
    extractions = [{
        "sheet_type": "elevation",
        "_source_file": "elev.json",
        "dimensions": [
            {"description": "plate height", "value_ft": 8.0, "confidence": 0.9},
        ],
        "notes": [],
    }]
    result = reconcile_extractions(extractions, MODEL_24x18)
    matches = [m for m in result.matches if m.field == "plate_height"]
    assert len(matches) == 1
    assert matches[0].model_value == 8.0
    assert matches[0].extracted_value == 8.0


def test_plate_height_conflict():
    extractions = [{
        "sheet_type": "elevation",
        "_source_file": "elev.json",
        "dimensions": [
            {"description": "wall height", "value_ft": 9.0, "confidence": 0.9},
        ],
        "notes": [],
    }]
    result = reconcile_extractions(extractions, MODEL_24x18)
    conflicts = [c for c in result.conflicts if c.field == "plate_height"]
    assert len(conflicts) == 1
    assert conflicts[0].model_value == 8.0
    assert conflicts[0].extracted_value == 9.0
    assert conflicts[0].severity == "high"  # 1.0 ft delta


def test_plate_height_medium_severity():
    extractions = [{
        "sheet_type": "elevation",
        "_source_file": "elev.json",
        "dimensions": [
            {"description": "ceiling height", "value_ft": 8.5, "confidence": 0.9},
        ],
        "notes": [],
    }]
    result = reconcile_extractions(extractions, MODEL_24x18)
    conflicts = [c for c in result.conflicts if c.field == "plate_height"]
    assert len(conflicts) == 1
    assert conflicts[0].severity == "medium"  # 0.5 ft delta


# ---------------------------------------------------------------------------
# reconcile_extractions — wall length
# ---------------------------------------------------------------------------

def test_wall_length_match():
    extractions = [{
        "sheet_type": "floor_plan",
        "_source_file": "fp.json",
        "dimensions": [
            {"description": "south wall width", "value_ft": 24.0, "confidence": 0.9},
        ],
        "notes": [],
    }]
    result = reconcile_extractions(extractions, MODEL_24x18)
    matches = [m for m in result.matches if m.field == "length_ft"]
    assert len(matches) == 1
    assert matches[0].entity_id == "wall_s"


def test_wall_length_conflict():
    extractions = [{
        "sheet_type": "floor_plan",
        "_source_file": "fp.json",
        "dimensions": [
            # 26 ft for south wall when model has 24 ft — 2 ft off, high severity
            {"description": "south wall length", "value_ft": 26.0, "confidence": 0.85},
        ],
        "notes": [],
    }]
    result = reconcile_extractions(extractions, MODEL_24x18)
    conflicts = [c for c in result.conflicts if c.field == "length_ft"]
    assert len(conflicts) == 1
    assert conflicts[0].entity_id == "wall_s"
    assert conflicts[0].severity == "high"


def test_unmatched_wall_dimension_becomes_addition():
    extractions = [{
        "sheet_type": "floor_plan",
        "_source_file": "fp.json",
        "dimensions": [
            # 50 ft — doesn't match any wall, goes to additions
            {"description": "overall building length", "value_ft": 50.0, "confidence": 0.8},
        ],
        "notes": [],
    }]
    result = reconcile_extractions(extractions, MODEL_24x18)
    assert len(result.additions) >= 1


# ---------------------------------------------------------------------------
# reconcile_extractions — low-confidence dimensions filtered
# ---------------------------------------------------------------------------

def test_low_confidence_dimension_ignored():
    extractions = [{
        "sheet_type": "floor_plan",
        "_source_file": "fp.json",
        "dimensions": [
            {"description": "some measurement", "value_ft": 99.0, "confidence": 0.3},
        ],
        "notes": [],
    }]
    result = reconcile_extractions(extractions, MODEL_24x18)
    # Low confidence unclassified dimension should not appear
    assert all(a.extracted_value != 99.0 for a in result.additions)


# ---------------------------------------------------------------------------
# ReconciliationResult.to_dict and _summary
# ---------------------------------------------------------------------------

def test_result_to_dict_structure():
    result = ReconciliationResult(
        matches=[DimensionMatch("floor_0", "plate_height", 8.0, 8.0, 0.9, "elev.json")],
        conflicts=[],
        additions=[],
    )
    d = result.to_dict()
    assert "matches" in d
    assert "conflicts" in d
    assert "additions" in d
    assert "summary" in d
    assert d["matches"][0]["entity"] == "floor_0"


def test_result_summary_with_conflicts():
    result = ReconciliationResult(
        matches=[],
        conflicts=[
            DimensionConflict("wall_s", "length_ft", 24.0, 26.0, 2.0, 0.9, "high",
                              "Update wall.", "fp.json")
        ],
        additions=[],
    )
    summary = result._summary()
    assert "conflict" in summary.lower()
    assert "high" in summary.lower()
