import tkinter as tk

from PIL import Image, ImageTk

from functions import tokens as t
from functions.bundled_path import bundled_path

ASSETS = bundled_path("assets")
LOGO, LOGO_Y = 126, 55
TITLE_X = t.MARGIN + LOGO + t.SPACE[4]
# tall enough to hold the corner, short enough that its base clears the cards at y=236
EQUIPMENT, EQUIPMENT_Y = 212, 12


def build_hero(canvas):
    """The masthead, drawn straight onto the photograph so nothing is boxed in.

    Canvas items have no background of their own, which is the only way in Tk to put type
    over an image, and the canvas alpha-blends each cut-out's soft edge against the scene.
    """
    logo = ASSETS / "polarbear-logo.png"
    if logo.exists():
        canvas.logo = ImageTk.PhotoImage(
            Image.open(logo).convert("RGBA").resize((LOGO, LOGO), Image.LANCZOS), master=canvas)
        canvas.create_image(t.MARGIN, LOGO_Y, image=canvas.logo, anchor="nw")
    equipment = ASSETS / "equipment.png"
    if equipment.exists():
        photo = Image.open(equipment).convert("RGBA")  # scaled by height; the width follows
        canvas.equipment = ImageTk.PhotoImage(
            photo.resize((round(photo.width * EQUIPMENT / photo.height), EQUIPMENT),
                         Image.LANCZOS), master=canvas)
        canvas.create_image(t.WIDTH - t.MARGIN, EQUIPMENT_Y, image=canvas.equipment, anchor="ne")
    canvas.create_text(TITLE_X, 74, text="Polar Bear Calorimeter", font=t.DISPLAY, fill=t.INK, anchor="nw")
    canvas.create_rectangle(TITLE_X, 132, TITLE_X + 448, 135, fill=t.BRAND, width=0)
    canvas.create_text(TITLE_X, 146, text="Measures heat transfer to and from the Polar Bear plate.",
                       font=t.TEXT, fill=t.BODY, anchor="nw")
