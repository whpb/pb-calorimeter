from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from functions.icon_glyph import icon_glyph

TTF = Path(__file__).resolve().parent.parent / "assets" / "tabler-icons.ttf"


def icon_image(name, size, colour):
    """A Tabler glyph rendered to a transparent square, its ink centred on the box.

    Drawn by Pillow rather than shown in a Tk label because the icon font declares an ascent
    eleven times its point size - a webfont habit, harmless under CSS line-height - which no
    Tk widget can undo. Centring the measured ink sidesteps the font's metrics entirely.
    """
    font = ImageFont.truetype(str(TTF), size)
    tile = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(tile)
    left, top, right, bottom = draw.textbbox((0, 0), icon_glyph(name), font=font)
    draw.text(((size - right + left) / 2 - left, (size - bottom + top) / 2 - top),
              icon_glyph(name), font=font, fill=colour)
    return tile
