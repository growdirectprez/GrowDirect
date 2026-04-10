"""Tests for extraction accuracy against Seacove ground truth.
These tests require Ollama running with a vision model. Skip if not available.
"""
import json
import pytest
from pathlib import Path
from arc.llm.vision import check_model_available

ARC_ROOT = Path(__file__).parent.parent
GROUND_TRUTH_PATH = ARC_ROOT / "projects/seacove/ground_truth/dimensions.json"
BLUEPRINT_DIR = ARC_ROOT / "25 Seacove Blueprints"


@pytest.fixture
def ground_truth():
    if not GROUND_TRUTH_PATH.exists():
        pytest.skip("Ground truth file not found")
    return json.loads(GROUND_TRUTH_PATH.read_text())


@pytest.mark.skipif(not check_model_available(), reason="Ollama vision model not available")
class TestExtractionAccuracy:
    def test_floor_plan_dimensions_within_tolerance(self, ground_truth, tmp_path):
        from arc.ingest.blueprint_reader import extract_pages_from_pdf
        from arc.extract.dimension_extractor import extract_dimensions

        floor_plan = BLUEPRINT_DIR / "25 Seacove Original Plan Page 3 - Floor Plan.pdf"
        if not floor_plan.exists():
            pytest.skip("Floor plan PDF not found")

        images = extract_pages_from_pdf(floor_plan, tmp_path)
        assert len(images) >= 1
        result = extract_dimensions(images[0])
        extracted_dims = {d["description"]: d["value_ft"] for d in result.get("dimensions", [])}

        gt_floor = [d for d in ground_truth["dimensions"] if d["sheet"] == "floor_plan"]
        matches = 0
        for gt_dim in gt_floor:
            for desc, value in extracted_dims.items():
                if abs(value - gt_dim["value_ft"]) <= 0.5:
                    matches += 1
                    break

        print(f"Matched {matches}/{len(gt_floor)} floor plan dimensions within 6 inches")
        assert matches > 0, f"No dimensions matched within 6 inches. Extracted: {list(extracted_dims.keys())}"
