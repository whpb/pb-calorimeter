import tkinter as tk

from PIL import ImageTk

from functions import tokens as t
from functions.build_footer import build_footer
from functions.build_hero import build_hero
from functions.build_menu_card import build_menu_card
from functions.grid_span import grid_span

# icon, title, description, action label
OPTIONS = (("device-desktop-analytics", "Automated Sequence",
            "Run successive experiments controlled by the Polar Bear Programmer.",
            "Enter testing mode  \u2192"),
           ("flask", "Run an Experiment",
            "Perform a single calorimetry experiment and view the results.",
            "Start recording  \u2192"),
           ("file-analytics", "Analyse Data",
            "Open a results file and calculate calorimetry data.",
            "Choose a file  \u2192"))
CARDS_Y, CARD_H = 236, 272


def build_menu(parent, backdrop, commands):
    """The branded front screen: the three things an operator can do, and the way out.

    A Canvas, so the masthead type can sit on the photograph and the cards' shadows can blend
    into it and into one another; only each card's content is a widget placed on top.
    """
    canvas = tk.Canvas(parent, width=t.WIDTH, height=t.HEIGHT, highlightthickness=0,
                       borderwidth=0, background=t.CANVAS)
    canvas.backdrop = ImageTk.PhotoImage(backdrop, master=canvas)
    canvas.create_image(0, 0, image=canvas.backdrop, anchor="nw")
    build_hero(canvas)
    width = grid_span(4)
    for index, option in enumerate(OPTIONS):
        build_menu_card(canvas, (t.MARGIN + index * (width + t.GUTTER), CARDS_Y, width, CARD_H),
                        option, commands[index])
    build_footer(canvas, commands[3])
    return canvas
