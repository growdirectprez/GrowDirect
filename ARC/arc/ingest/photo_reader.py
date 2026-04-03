"""Process site photos — normalize and tag for reference."""
from __future__ import annotations
from pathlib import Path
from arc.ingest.blueprint_reader import normalize_image

def process_photos(photo_dir: Path, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for photo in sorted(photo_dir.iterdir()):
        if photo.suffix.lower() in (".jpg", ".jpeg", ".png"):
            out = output_dir / f"photo_{photo.stem}.png"
            normalize_image(photo, out)
            results.append(out)
    return results
