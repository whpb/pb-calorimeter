import tkinter as tk
from pathlib import Path

from PIL import Image, ImageTk

from functions import tokens as t

ASSETS = Path(__file__).resolve().parent.parent / "assets"
LOGO, LOGO_Y = 48, 34
TITLE_X = t.MARGIN + LOGO + t.SPACE[3]


def build_screen(parent, backdrop, heading):
    """The shell every screen after the menu shares: the photograph, a compact masthead.

    Returns the canvas, so the caller can place its own cards on it.
    """
    canvas = tk.Canvas(parent, width=t.WIDTH, height=t.HEIGHT, highlightthickness=0,
                       borderwidth=0, background=t.CANVAS)
    canvas.backdrop = ImageTk.PhotoImage(backdrop, master=canvas)
    canvas.create_image(0, 0, image=canvas.backdrop, anchor="nw")
    logo = ASSETS / "polarbear-logo.png"
    if logo.exists():
        plate = backdrop.crop((t.MARGIN, LOGO_Y, t.MARGIN + LOGO, LOGO_Y + LOGO)).convert("RGBA")
        plate.alpha_composite(Image.open(logo).convert("RGBA").resize((LOGO, LOGO), Image.LANCZOS))
        canvas.logo = ImageTk.PhotoImage(plate.convert("RGB"), master=canvas)
        canvas.create_image(t.MARGIN, LOGO_Y, image=canvas.logo, anchor="nw")
    title = canvas.create_text(TITLE_X, 36, text=heading, font=t.H1, fill=t.INK, anchor="nw")
    left, _, right, bottom = canvas.bbox(title)  # the rule is cut to the heading it underlines
    canvas.create_rectangle(left, bottom + 6, right, bottom + 9, fill=t.BRAND, width=0)
    return canvas
