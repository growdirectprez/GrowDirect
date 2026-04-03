"""Read blueprint PDFs and normalize images for vision AI extraction."""
from __future__ import annotations
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image


def extract_pages_from_pdf(pdf_path: Path, output_dir: Path, dpi: int = 300) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(pdf_path))
    images: list[Path] = []
    for i, page in enumerate(doc):
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        stem = pdf_path.stem.replace(" ", "_")
        out_path = output_dir / f"{stem}_page{i + 1}.png"
        pix.save(str(out_path))
        images.append(out_path)
    doc.close()
    return images


def normalize_image(image_path: Path, output_path: Path, max_dim: int = 2048) -> Path:
    img = Image.open(image_path)
    w, h = img.size
    if max(w, h) > max_dim:
        scale = max_dim / max(w, h)
        new_size = (int(w * scale), int(h * scale))
        img = img.resize(new_size, Image.LANCZOS)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
    return output_path
