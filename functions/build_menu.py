import tkinter as tk

from PIL import ImageTk

from functions import tokens as t
from functions.build_footer import build_footer
from functions.build_hero import build_hero
from functions.build_menu_card import build_menu_card
from functions.grid_span import grid_span

# icon, title, description, action label
OPTIONS = (("device-desktop-analytics", "Testing mode",
            "Unattended: record every User Value 1 run to CSV, ready to re-analyse",
            "Enter testing mode  \u2192"),
           ("player-play", "Force run",
            "Start and stop one run from here, ignoring User Value 1",
            "Start recording  \u2192"),
           ("file-analytics", "Re-analyse data",
            "Re-cut the zones on a results file you already have",
            "Choose a file  \u2192"))
CARDS_Y, CARD_H = 236, 272


def build_menu(parent, backdrop, commands):
    """The branded front screen: the three things an operator can do, and the way out.

    A Canvas, so the masthead type can sit on the photograph; the cards are ordinary widgets
    placed on top, each composited against the backdrop so its shadow falls on the scene.
    """
    canvas = tk.Canvas(parent, width=t.WIDTH, height=t.HEIGHT, highlightthickness=0,
                       borderwidth=0, background=t.CANVAS)
    canvas.backdrop = ImageTk.PhotoImage(backdrop, master=canvas)
    canvas.create_image(0, 0, image=canvas.backdrop, anchor="nw")
    build_hero(canvas, backdrop)
    width = grid_span(4)
    for index, option in enumerate(OPTIONS):
        build_menu_card(canvas, backdrop,
                        (t.MARGIN + index * (width + t.GUTTER), CARDS_Y, width, CARD_H),
                        option, commands[index])
    build_footer(canvas, backdrop, commands[3])
    return canvas
