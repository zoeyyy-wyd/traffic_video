"""Turning frames into what a VLM actually receives.

Claude downsamples so the long edge is ~1568 px. Rendering larger is paid for
in upload time and discarded; rendering smaller wastes the budget. A contact
sheet divides that budget by its column count, which is why separate
full-resolution frames are preferred wherever small objects matter.
"""
import base64
import io
import os
from typing import Sequence, Tuple

from PIL import Image, ImageDraw, ImageFont

LONG_EDGE = 1568

_FONT_PATHS = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
)


def _font(size: int):
    """Bold sans face for burnt-in labels, with a bitmap fallback."""
    for path in _FONT_PATHS:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def stamp(img: Image.Image, text: str) -> Image.Image:
    """Burn a caption into the top-left corner."""
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)
    size = max(16, img.width // 40)
    font = _font(size)
    pad = size // 3
    box = draw.textbbox((0, 0), text, font=font)
    draw.rectangle([0, 0, box[2] + 2 * pad, box[3] + 2 * pad], fill=(0, 0, 0))
    draw.text((pad, pad), text, fill=(255, 255, 0), font=font)
    return img


def fit(img: Image.Image, long_edge: int = LONG_EDGE) -> Image.Image:
    if max(img.size) <= long_edge:
        return img
    ratio = long_edge / max(img.size)
    return img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)


def contact_sheet(frames: Sequence[Tuple[float, Image.Image]], cols: int) -> Image.Image:
    """Tile frames into a grid: cheaper in tokens and easier to read motion
    across, at the cost of dividing linear resolution by `cols`."""
    rows = (len(frames) + cols - 1) // cols
    cell_w = LONG_EDGE // cols
    cells = []
    for t, img in frames:
        img = stamp(img, f"t={t:.2f}s")
        ratio = cell_w / img.width
        cells.append(img.resize((cell_w, int(img.height * ratio)), Image.LANCZOS))
    cell_h = max(c.height for c in cells)
    sheet = Image.new("RGB", (cell_w * cols, cell_h * rows), (20, 20, 20))
    for i, cell in enumerate(cells):
        sheet.paste(cell, ((i % cols) * cell_w, (i // cols) * cell_h))
    return sheet


def to_b64(img: Image.Image, quality: int = 88) -> str:
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return base64.b64encode(buf.getvalue()).decode()


def save_window(frames, out_dir, tag: str, mode: str, cols: int) -> None:
    """Persist exactly what the model is shown.

    When a scan misses an event the first question is whether the evidence was
    legible at all, so this is written unconditionally, dry run or not.
    """
    from pathlib import Path

    out_dir = Path(out_dir)
    if mode == "sheet":
        contact_sheet(frames, cols).save(out_dir / f"{tag}.jpg", quality=88)
    else:
        cell_dir = out_dir / tag
        cell_dir.mkdir(parents=True, exist_ok=True)
        for t, img in frames:
            fit(stamp(img, f"t={t:.2f}s")).save(cell_dir / f"{t:08.2f}.jpg", quality=88)


def overview_grid(thumbs, cols: int = 10, cell_w: int = 320) -> Image.Image:
    """Tile one thumbnail per sampled moment into a single scannable image.

    Half an hour of footage becomes one picture a person can read in seconds.
    Its main job is practical: a look at an actual frame beats stepping
    through a player when you need to know what the camera covers.
    """
    cells = []
    for t, img in thumbs:
        img = img.convert("RGB")
        ratio = cell_w / img.width
        cells.append(stamp(img.resize((cell_w, max(1, int(img.height * ratio))),
                                      Image.LANCZOS),
                           f"{int(t) // 60:02d}:{int(t) % 60:02d}"))
    rows = (len(cells) + cols - 1) // cols
    ch = max(c.height for c in cells)
    grid = Image.new("RGB", (cell_w * cols, ch * rows), (20, 20, 20))
    for i, c in enumerate(cells):
        grid.paste(c, ((i % cols) * cell_w, (i // cols) * ch))
    return grid
