import tkinter as tk
from tkinter import ttk

BRAND = "#D71921"  # sampled from the logo, so the rule under the title matches it
OPTIONS = (("Testing mode", "Unattended: record every User Value 1 run to CSV, ready to re-analyse"),
           ("Force run", "Start and stop one run from here, ignoring User Value 1"),
           ("Re-analyse data", "Re-cut the zones on a results file you already have"),
           ("Quit", "Close the application"))


def build_menu(parent, logo, commands):
    """The branded front screen: the three things an operator can do."""
    frame = ttk.Frame(parent, padding=32)
    if logo is not None:
        ttk.Label(frame, image=logo).pack(anchor="w", pady=(0, 12))
    ttk.Label(frame, text="PB Calorimeter", font=("Segoe UI", 24, "bold")).pack(anchor="w")
    tk.Frame(frame, height=3, background=BRAND).pack(fill="x", pady=(6, 6))
    ttk.Label(frame, text="Indirect calorimetry on the Polar Bear",
              foreground="#555555").pack(anchor="w", pady=(0, 30))
    for (text, description), command in zip(OPTIONS, commands):
        ttk.Button(frame, text=text, width=26, command=command).pack(anchor="w")
        ttk.Label(frame, text=description, foreground="#777777").pack(anchor="w", pady=(2, 16))
    return frame
