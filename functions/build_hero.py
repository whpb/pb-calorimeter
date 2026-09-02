import tkinter as tk
from pathlib import Path

from PIL import Image, ImageTk

from functions import tokens as t
from functions.product_image import product_image

ASSETS = Path(__file__).resolve().parent.parent / "assets"
LOGO, LOGO_Y = 84, 77
MACHINE = 210  # the machine stands the height of the masthead, clear of the cards
TITLE_X = t.MARGIN + LOGO + t.SPACE[4]


def build_hero(canvas, backdrop):
    """The masthead, drawn straight onto the photograph as canvas items so nothing is boxed in.

    Text on a Canvas has no background of its own, which is the only way in Tk to put type
    over an image. Both photographs are composited into the backdrop by Pillow first, so
    their soft edges blend against the real pixels rather than against a flat fill.
    """
    keep = []
    logo = ASSETS / "polarbear-logo.png"
    if logo.exists():
        plate = backdrop.crop((t.MARGIN, LOGO_Y, t.MARGIN + LOGO, LOGO_Y + LOGO)).convert("RGBA")
        plate.alpha_composite(Image.open(logo).convert("RGBA").resize((LOGO, LOGO), Image.LANCZOS))
        keep.append(ImageTk.PhotoImage(plate.convert("RGB"), master=canvas))
        canvas.create_image(t.MARGIN, LOGO_Y, image=keep[-1], anchor="nw")
    equipment = ASSETS / "equipment.jpg"
    if equipment.exists():
        keep.append(ImageTk.PhotoImage(product_image(equipment, MACHINE, backdrop,
                                                     t.WIDTH - t.MARGIN, 8), master=canvas))
        canvas.create_image(t.WIDTH - t.MARGIN, 8, image=keep[-1], anchor="ne")
    canvas.create_text(TITLE_X, 74, text="PB Calorimeter", font=t.DISPLAY, fill=t.INK, anchor="nw")
    canvas.create_rectangle(TITLE_X, 132, TITLE_X + 248, 135, fill=t.BRAND, width=0)
    canvas.create_text(TITLE_X, 146, text="Indirect calorimetry on the Polar Bear",
                       font=t.TEXT, fill=t.BODY, anchor="nw")
    canvas.hero_images = keep  # Tk keeps no reference of its own
