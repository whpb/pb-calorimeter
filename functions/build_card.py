import tkinter as tk

from PIL import Image, ImageTk

from functions import tokens as t
from functions.panel_image import PAD, panel_image


def build_card(parent, backdrop, box, inset=t.SPACE[4], fill=t.WHITE, radius=t.RADIUS):
    """A rounded panel on the window's backdrop; returns the frame to put the content in.

    `box` is (x, y, width, height) in the parent's coordinates. The panel is a label carrying
    a pre-rendered image - Tk has no rounded corners and no alpha - so the shadow is baked
    against what sits behind it, and the content goes in a plain frame placed on top, where
    ordinary pack() and grid() work as normal. `backdrop` is the window's background image,
    or a flat colour when the panel is nested inside something already solid.
    """
    x, y, width, height = box
    plate = (backdrop.crop((x - PAD, y - PAD, x + width + PAD, y + height + PAD))
             if hasattr(backdrop, "crop")
             else Image.new("RGB", (width + PAD * 2, height + PAD * 2), backdrop))
    image = ImageTk.PhotoImage(panel_image((width, height), radius, fill, plate))
    card = tk.Label(parent, image=image, borderwidth=0, highlightthickness=0)
    card.image = image  # Tk keeps no reference of its own, and the image would be collected
    card.place(x=x - PAD, y=y - PAD)
    inner = tk.Frame(card, background=fill)
    inner.place(x=PAD + inset, y=PAD + inset,
                width=width - inset * 2, height=height - inset * 2)
    return inner
