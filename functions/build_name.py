from functions import tokens as t
from functions.build_button import build_button
from functions.build_card import build_card
from functions.build_field import build_field
from functions.build_screen import build_screen
from functions.build_shelf import build_shelf
from functions.grid_span import grid_span

PANEL = (t.MARGIN, 104, grid_span(8), 160)  # hugs the field; the shelf carries the rest
LABEL = "Experiment name"
HINT = "Names this run's folder and every file in it. Leave it blank to use the date and time."


def build_name(parent, backdrop, on_start, on_back):
    """Ask what the experiment is called, before a forced run starts recording."""
    canvas = build_screen(parent, backdrop, "Run an Experiment")
    inner = build_card(canvas, PANEL)

    def start():
        on_start(entry.get())

    entry = build_field(inner, LABEL, HINT, start)
    entry.focus_set()  # the operator is at the rig to record, not to hunt for the box
    shelf = build_shelf(canvas)
    build_button(shelf, "Back to menu", on_back, "quiet", (150, 56)).pack(side="right")
    build_button(shelf, "Start recording  \u2192", start, size=(200, 56)).pack(
        side="right", padx=(0, t.SPACE[2]))
    return canvas
