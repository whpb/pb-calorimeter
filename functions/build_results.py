import tkinter as tk

from functions import tokens as t
from functions.build_button import build_button
from functions.build_card import build_card
from functions.build_file_row import build_file_row
from functions.build_screen import build_screen
from functions.build_shelf import build_shelf
from functions.grid_span import grid_span
from functions.open_path import open_path

PANEL = (t.MARGIN, 104, grid_span(12), 396)
FILES = ((".pdf", "Report", "file-text"), (".csv", "Results data", "table"),
         (".png", "Work curve", "chart-line"), (".json", "Summary data", "braces"),
         (".typ", "Typst source", "file-code"))


def build_results(parent, backdrop, report, on_menu, on_continue=None):
    """Links to everything a finished run produced, and the way back."""
    canvas = build_screen(parent, backdrop, "Run complete")
    inner = build_card(canvas, PANEL)
    tk.Label(inner, text=report.stem, font=t.TEXT, foreground=t.MUTED, background=t.WHITE,
             anchor="w").pack(fill="x", pady=(0, t.SPACE[3]))
    for suffix, description, icon in FILES:
        path = report.with_suffix(suffix)
        if path.exists():
            build_file_row(inner, icon, description, path,
                           lambda chosen=path: open_path(chosen)).pack(fill="x", pady=t.SPACE[1])
    build_file_row(inner, "folder-open", "Containing folder", report.parent,
                   lambda: open_path(report.parent)).pack(fill="x", pady=(t.SPACE[2], 0))
    shelf = build_shelf(canvas)
    build_button(shelf, "Back to menu", on_menu, "quiet", (150, 56)).pack(side="right")
    if on_continue is not None:
        build_button(shelf, "Continue testing", on_continue, size=(176, 56)).pack(
            side="right", padx=(0, t.SPACE[2]))
    return canvas
