import tkinter as tk
from pathlib import Path

from PIL import Image, ImageTk

from functions import tokens as t

ASSETS = Path(__file__).resolve().parent.parent / "assets"
LOGO, LOGO_Y = 126, 55
TITLE_X = t.MARGIN + LOGO + t.SPACE[4]


def build_hero(canvas):
    """The masthead, drawn straight onto the photograph so nothing is boxed in.

    Canvas items have no background of their own, which is the only way in Tk to put type
    over an image, and the canvas alpha-blends the logo's soft edge against the scene.
    """
    logo = ASSETS / "polarbear-logo.png"
    if logo.exists():
        canvas.logo = ImageTk.PhotoImage(
            Image.open(logo).convert("RGBA").resize((LOGO, LOGO), Image.LANCZOS), master=canvas)
        canvas.create_image(t.MARGIN, LOGO_Y, image=canvas.logo, anchor="nw")
    canvas.create_text(TITLE_X, 74, text="Polar Bear Calorimeter", font=t.DISPLAY, fill=t.INK, anchor="nw")
    canvas.create_rectangle(TITLE_X, 132, TITLE_X + 448, 135, fill=t.BRAND, width=0)
    canvas.create_text(TITLE_X, 146, text="Measures heat transfer to and from the Polar Bear plate.",
                       font=t.TEXT, fill=t.BODY, anchor="nw")
