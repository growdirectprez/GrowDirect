"""Reconcile extraction data against an existing spatial model.

This module does a deterministic (no-LLM) structural diff between extracted
dimensions and the current spatial_model.json. It is used as a pre-pass
before calling the LLM reconciler in builder.py — the output gives the LLM
a tighter, more focused context to reason about.

Public API:
    reconcile_extractions(extractions, model_dict) -> ReconciliationResult
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

@dataclass
class DimensionMatch:
    """An extracted dimension that agrees with the model."""
    entity_id: str
    field: str
    model_value: Any
    extracted_value: Any
    confidence: float
    source_file: str


@dataclass
class DimensionConflict:
    """An extracted dimension that contradicts the model."""
    entity_id: str
    field: str
    model_value: Any
    extracted_value: Any
    delta: Optional[float]       # absolute difference (ft), None if non-numeric
    confidence: float
    severity: str                # "low" | "medium" | "high"
    recommendation: str
    source_file: str


@dataclass
class DimensionAddition:
    """An extracted dimension with no corresponding model entry."""
    description: str
    extracted_value: Any
    sheet_type: str
    confidence: float
    source_file: str


@dataclass
class ReconciliationResult:
    matches: list[DimensionMatch] = field(default_factory=list)
    conflicts: list[DimensionConflict] = field(default_factory=list)
    additions: list[DimensionAddition] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "matches": [
                {
                    "entity": m.entity_id,
                    "field": m.field,
                    "model_value": m.model_value,
                    "extracted_value": m.extracted_value,
                    "confidence": m.confidence,
                    "source_file": m.source_file,
                }
                for m in self.matches
            ],
            "conflicts": [
                {
                    "entity": c.entity_id,
                    "field": c.field,
                    "model_value": c.model_value,
                    "extracted_value": c.extracted_value,
                    "delta_ft": c.delta,
                    "confidence": c.confidence,
                    "severity": c.severity,
                    "recommendation": c.recommendation,
                    "source_file": c.source_file,
                }
                for c in self.conflicts
            ],
            "additions": [
                {
                    "description": a.description,
                    "extracted_value": a.extracted_value,
                    "sheet_type": a.sheet_type,
                    "confidence": a.confidence,
                    "source_file": a.source_file,
                }
                for a in self.additions
            ],
            "summary": self._summary(),
        }

    def _summary(self) -> str:
        n_m = len(self.matches)
        n_c = len(self.conflicts)
        n_a = len(self.additions)
        high = sum(1 for c in self.conflicts if c.severity == "high")
        parts = [f"{n_m} dimension(s) confirmed by extractions"]
        if n_c:
            parts.append(f"{n_c} conflict(s) ({high} high-severity)")
        if n_a:
            parts.append(f"{n_a} extracted value(s) not yet in model")
        return "; ".join(parts) + "."


# ---------------------------------------------------------------------------
# Tolerances
# ---------------------------------------------------------------------------

TOLERANCE_FT = 0.25       # within 3 inches → match
HIGH_SEVERITY_FT = 1.0    # more than 1 ft off → high severity


def _severity(delta: float) -> str:
    if delta <= TOLERANCE_FT:
        return "low"
    if delta < HIGH_SEVERITY_FT:
        return "medium"
    return "high"


# ---------------------------------------------------------------------------
# Wall length index from model
# ---------------------------------------------------------------------------

def _wall_length(wall: dict) -> float:
    from_pt = wall.get("from", [0, 0])
    to_pt = wall.get("to", [0, 0])
    dx = to_pt[0] - from_pt[0]
    dy = to_pt[1] - from_pt[1]
    return math.hypot(dx, dy)


def _build_wall_index(model_dict: dict) -> dict[str, dict]:
    """Return {wall_id: wall_dict} for all walls in the model."""
    index = {}
    floors = model_dict.get("structure", {}).get("floors", [])
    for fl in floors:
        for wall in fl.get("walls", []):
            wid = wall.get("id")
            if wid:
                index[wid] = {**wall, "_plate_height": fl.get("plate_height", 8.0)}
    return index


def _build_floor_index(model_dict: dict) -> dict[int, dict]:
    """Return {level: floor_dict}."""
    index = {}
    floors = model_dict.get("structure", {}).get("floors", [])
    for fl in floors:
        index[fl.get("level", 0)] = fl
    return index


# ---------------------------------------------------------------------------
# Dimension matching heuristics
# ---------------------------------------------------------------------------

# Keywords that suggest a dimension describes a wall length
_WALL_LENGTH_KEYWORDS = {
    "south wall", "north wall", "east wall", "west wall",
    "wall length", "wall width", "room width", "room length",
    "living room", "bedroom", "kitchen", "hallway", "bathroom",
}

# Keywords for plate / wall height
_HEIGHT_KEYWORDS = {"plate height", "wall height", "ceiling height", "floor to ceiling"}

# Keywords for overall building dimensions
_OVERALL_KEYWORDS = {"overall", "total", "building width", "building length", "house width", "house length"}


def _keyword_match(description: str, keyword_set: set[str]) -> bool:
    desc_lower = description.lower()
    return any(kw in desc_lower for kw in keyword_set)


def _find_best_wall_match(
    value_ft: float,
    description: str,
    wall_index: dict[str, dict],
    tolerance: float = TOLERANCE_FT,
) -> Optional[str]:
    """Find the wall ID whose length is closest to value_ft, within tolerance.

    Used for match/conflict classification after association has already been done.
    """
    return _find_closest_wall(value_ft, description, wall_index, max_delta=tolerance)


def _find_closest_wall(
    value_ft: float,
    description: str,
    wall_index: dict[str, dict],
    max_delta: float = TOLERANCE_FT,
) -> Optional[str]:
    """Find the wall ID most plausibly described by value_ft + description.

    Uses compass-direction hints from the description to break ties.
    max_delta caps the search radius (in feet).
    """
    best_id = None
    best_delta = float("inf")

    desc_lower = description.lower()
    for wid, wall in wall_index.items():
        length = _wall_length(wall)
        delta = abs(length - value_ft)
        if delta > max_delta:
            continue
        # Compass bonus: prefer walls whose id contains the compass hint
        compass_bonus = 0.0
        for direction in ("south", "north", "east", "west"):
            if direction in desc_lower and direction[:1] in wid.lower():
                compass_bonus = max_delta * 0.4

        effective_delta = delta - compass_bonus
        if effective_delta < best_delta:
            best_delta = effective_delta
            best_id = wid

    return best_id


# ---------------------------------------------------------------------------
# Main reconciliation function
# ---------------------------------------------------------------------------

def reconcile_extractions(
    extractions: list[dict],
    model_dict: dict,
) -> ReconciliationResult:
    """Deterministic diff of extracted dimensions against the spatial model.

    Args:
        extractions: list of extraction dicts (from load_extractions).
        model_dict:  parsed spatial_model.json as a dict.

    Returns:
        ReconciliationResult with matches, conflicts, additions.
    """
    result = ReconciliationResult()
    wall_index = _build_wall_index(model_dict)
    floor_index = _build_floor_index(model_dict)

    for ext in extractions:
        sheet_type = ext.get("sheet_type", "unknown")
        source_file = ext.get("_source_file", "unknown")

        for dim in ext.get("dimensions", []):
            desc = dim.get("description", "")
            value_ft = dim.get("value_ft")
            confidence = dim.get("confidence", 0.0)

            if value_ft is None:
                continue

            # --- Plate / wall height ---
            if _keyword_match(desc, _HEIGHT_KEYWORDS):
                floor_0 = floor_index.get(0)
                if floor_0:
                    model_ph = floor_0.get("plate_height", 8.0)
                    delta = abs(model_ph - value_ft)
                    if delta <= TOLERANCE_FT:
                        result.matches.append(DimensionMatch(
                            entity_id="floor_0",
                            field="plate_height",
                            model_value=model_ph,
                            extracted_value=value_ft,
                            confidence=confidence,
                            source_file=source_file,
                        ))
                    else:
                        result.conflicts.append(DimensionConflict(
                            entity_id="floor_0",
                            field="plate_height",
                            model_value=model_ph,
                            extracted_value=value_ft,
                            delta=delta,
                            confidence=confidence,
                            severity=_severity(delta),
                            recommendation=(
                                f"Update floor 0 plate_height from {model_ph} to {value_ft} ft "
                                f"(extracted from {source_file})."
                            ),
                            source_file=source_file,
                        ))
                else:
                    result.additions.append(DimensionAddition(
                        description=f"plate_height: {desc}",
                        extracted_value=value_ft,
                        sheet_type=sheet_type,
                        confidence=confidence,
                        source_file=source_file,
                    ))
                continue

            # --- Wall length ---
            if _keyword_match(desc, _WALL_LENGTH_KEYWORDS):
                # Two-step: first associate (generous 5 ft radius), then classify.
                ASSOC_TOLERANCE = 5.0
                wall_id = _find_closest_wall(value_ft, desc, wall_index, max_delta=ASSOC_TOLERANCE)
                if wall_id:
                    model_len = _wall_length(wall_index[wall_id])
                    delta = abs(model_len - value_ft)
                    if delta <= TOLERANCE_FT:
                        result.matches.append(DimensionMatch(
                            entity_id=wall_id,
                            field="length_ft",
                            model_value=round(model_len, 3),
                            extracted_value=value_ft,
                            confidence=confidence,
                            source_file=source_file,
                        ))
                    else:
                        result.conflicts.append(DimensionConflict(
                            entity_id=wall_id,
                            field="length_ft",
                            model_value=round(model_len, 3),
                            extracted_value=value_ft,
                            delta=delta,
                            confidence=confidence,
                            severity=_severity(delta),
                            recommendation=(
                                f"Wall '{wall_id}' model length {model_len:.2f} ft differs "
                                f"from extraction {value_ft} ft by {delta:.2f} ft. "
                                f"Review wall endpoints."
                            ),
                            source_file=source_file,
                        ))
                else:
                    # No wall in model near this value — likely a new element
                    result.additions.append(DimensionAddition(
                        description=desc,
                        extracted_value=value_ft,
                        sheet_type=sheet_type,
                        confidence=confidence,
                        source_file=source_file,
                    ))
                continue

            # --- Overall building dimensions (no single wall match expected) ---
            if _keyword_match(desc, _OVERALL_KEYWORDS):
                result.additions.append(DimensionAddition(
                    description=f"overall: {desc}",
                    extracted_value=value_ft,
                    sheet_type=sheet_type,
                    confidence=confidence,
                    source_file=source_file,
                ))
                continue

            # --- Unclassified dimension — record as addition ---
            if confidence >= 0.7:
                result.additions.append(DimensionAddition(
                    description=desc,
                    extracted_value=value_ft,
                    sheet_type=sheet_type,
                    confidence=confidence,
                    source_file=source_file,
                ))

    return result
