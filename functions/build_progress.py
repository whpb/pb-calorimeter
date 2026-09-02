import tkinter as tk
from tkinter import ttk

from functions import tokens as t
from functions.build_button import build_button
from functions.build_card import build_card
from functions.build_screen import build_screen
from functions.build_shelf import build_shelf
from functions.grid_span import grid_span

PANEL = (t.MARGIN, 104, grid_span(12), 396)


def build_progress(parent, backdrop, heading, on_back, on_stop=None):
    """Holding screen: the latest status line, a live bar, and the run's output as it lands."""
    canvas = build_screen(parent, backdrop, heading)
    inner = build_card(canvas, PANEL)
    status = tk.Label(inner, text="Starting...", font=t.H2, foreground=t.BODY,
                      background=t.WHITE, anchor="w")
    status.pack(fill="x")
    bar = ttk.Progressbar(inner, mode="indeterminate", style="Brand.Horizontal.TProgressbar")
    bar.pack(fill="x", pady=(t.SPACE[2], t.SPACE[4]))
    bar.start(12)  # the animation says the interface is alive; the log says the rig is
    well = tk.Frame(inner, background=t.CANVAS, highlightthickness=1,
                    highlightbackground=t.LINE)
    well.pack(fill="both", expand=True)
    log = tk.Text(well, wrap="none", borderwidth=0, highlightthickness=0, font=t.LOG,
                  background=t.CANVAS, foreground=t.BODY, insertbackground=t.BODY,
                  padx=t.SPACE[3], pady=t.SPACE[2])
    log.pack(fill="both", expand=True)
    shelf = build_shelf(canvas)
    build_button(shelf, "Back to menu  (ends the run)", on_back, "quiet",
                 (232, 56)).pack(side="right")
    if on_stop is not None:  # only a forced run can be ended from here with its report intact
        build_button(shelf, "Stop and analyse", on_stop, size=(180, 56)).pack(
            side="right", padx=(0, t.SPACE[2]))
    return {"frame": canvas, "status": status, "log": log}
