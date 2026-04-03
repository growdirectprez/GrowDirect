"""Tests for the ARC ingest pipeline."""
import pytest
from pathlib import Path
from arc.ingest.blueprint_reader import extract_pages_from_pdf, normalize_image


@pytest.fixture
def arc_root():
    return Path(__file__).parent.parent


class TestBlueprintReader:
    def test_extract_pages_returns_images(self, tmp_path, arc_root):
        bp_dir = arc_root / "25 Seacove Blueprints"
        test_pdf = bp_dir / "25 Seacove Original Plan Page 3 - Floor Plan.pdf"
        if not test_pdf.exists():
            pytest.skip("Blueprint PDF not available")
        images = extract_pages_from_pdf(test_pdf, tmp_path)
        assert len(images) >= 1
        for img in images:
            assert img.exists()
            assert img.suffix == ".png"

    def test_normalize_image_resizes(self, tmp_path):
        from PIL import Image
        test_img = tmp_path / "test.png"
        Image.new("RGB", (4000, 3000)).save(test_img)
        result = normalize_image(test_img, tmp_path / "normalized.png")
        assert result.exists()
        img = Image.open(result)
        assert max(img.size) <= 2048
