"""Generates MSIX tile logos from assets/polarbear-logo.png into the Nuitka dist folder."""
from pathlib import Path

from PIL import Image

REPO_ROOT = Path(__file__).parent.parent
SOURCE = REPO_ROOT / "assets" / "polarbear-logo.png"
OUTPUT = REPO_ROOT / "build" / "launcher.dist" / "AppxAssets"

SIZES = {
    "Square44x44Logo.png": 44,
    "Square150x150Logo.png": 150,
    "StoreLogo.png": 50,
}

PADDING = 0.8  # fraction of the canvas the logo occupies, per MSIX tile guidelines


def make_logo(source: Image.Image, size: int) -> Image.Image:
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    scaled = source.copy()
    scaled.thumbnail((int(size * PADDING), int(size * PADDING)), Image.LANCZOS)
    offset = ((size - scaled.width) // 2, (size - scaled.height) // 2)
    canvas.paste(scaled, offset, scaled)
    return canvas


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    source = Image.open(SOURCE).convert("RGBA")
    for filename, size in SIZES.items():
        make_logo(source, size).save(OUTPUT / filename)
        print(f"Wrote {filename} ({size}x{size})")


if __name__ == "__main__":
    main()
