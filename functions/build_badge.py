import tkinter as tk

from PIL import Image, ImageTk

from functions import tokens as t
from functions.icon_image import icon_image
from functions.panel_image import panel_image


def build_badge(parent, icon, size=54, fill=t.BRAND, ink=t.WHITE, ground=t.WHITE, glyph=28):
    """A Tabler icon in a filled disc, composited to one flat image so nothing can reflow."""
    disc = panel_image((size, size), size // 2, fill,
                       Image.new("RGB", (size, size), ground), blur=0, pad=0).convert("RGBA")
    disc.alpha_composite(icon_image(icon, glyph, ink), ((size - glyph) // 2,) * 2)
    image = ImageTk.PhotoImage(disc.convert("RGB"), master=parent)
    badge = tk.Label(parent, image=image, width=size, height=size, borderwidth=0,
                     highlightthickness=0, background=ground)
    badge.image = image  # Tk keeps no reference of its own
    return badge
