"""Generate placeholder product-image PNG tiles using Pillow.

Each tile is a 600×600 solid-color PNG with the SKU centered in white text.
Colors are deterministically derived from the SKU string so they are stable
across re-runs.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

# Warm, brand-adjacent palette — 12 distinct hues
_PALETTE: list[tuple[int, int, int]] = [
    (74, 153, 148),   # solex teal
    (183, 141, 78),   # solex gold
    (95, 148, 95),    # solex leaf
    (200, 100, 80),   # terracotta
    (120, 80, 160),   # violet
    (60, 130, 180),   # sky blue
    (200, 130, 60),   # amber
    (160, 90, 120),   # mauve
    (80, 150, 130),   # sea-green
    (190, 100, 100),  # salmon
    (100, 120, 160),  # slate blue
    (150, 160, 80),   # olive
]


def _color_for_sku(sku: str) -> tuple[int, int, int]:
    digest = hashlib.md5(sku.encode()).hexdigest()
    index = int(digest[:4], 16) % len(_PALETTE)
    return _PALETTE[index]


def generate(skus: list[str], out_dir: Path) -> int:
    """Generate one 600×600 PNG per SKU into *out_dir*.

    Returns the number of files written.
    """
    from PIL import Image, ImageDraw, ImageFont

    out_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for sku in skus:
        color = _color_for_sku(sku)
        img = Image.new("RGB", (600, 600), color=color)
        draw = ImageDraw.Draw(img)

        # Render SKU label — fallback to default font if truetype not available
        label = sku.upper()
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        except (IOError, OSError):
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), label, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (600 - text_w) // 2 - bbox[0]
        y = (600 - text_h) // 2 - bbox[1]
        draw.text((x, y), label, fill=(255, 255, 255), font=font)

        slug = sku.lower()
        img.save(out_dir / f"{slug}.png", "PNG")
        count += 1
    return count
