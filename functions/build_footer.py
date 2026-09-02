import tkinter as tk

from functions import tokens as t
from functions.build_button import build_button
from functions.build_shelf import build_shelf


def build_footer(canvas, on_quit):
    """The front screen's shelf: whose it is, and the way out."""
    shelf = build_shelf(canvas)
    tk.Label(shelf, text="PB Calorimeter", font=t.H2, foreground=t.INK,
             background=t.WHITE).pack(side="left", padx=(t.SPACE[2], 0))
    tk.Label(shelf, text="Cambridge Reactor Design Ltd", font=t.SMALL, foreground=t.MUTED,
             background=t.WHITE).pack(side="left", padx=(t.SPACE[2], 0))
    build_button(shelf, "Quit", on_quit, "quiet", (124, 56)).pack(side="right")
    return shelf
