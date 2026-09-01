import tkinter as tk
from tkinter import ttk


def build_progress(parent, heading, on_back, on_stop=None):
    """Holding screen: an animated bar, the latest status line, and the run's output as it lands."""
    frame = ttk.Frame(parent, padding=28)
    ttk.Label(frame, text=heading, font=("Segoe UI", 20, "bold")).pack(anchor="w")
    status = ttk.Label(frame, text="Starting...", foreground="#555555")
    status.pack(anchor="w", pady=(6, 14))
    bar = ttk.Progressbar(frame, mode="indeterminate")
    bar.pack(fill="x")
    bar.start(12)  # the animation says the interface is alive; the log says the rig is
    log = tk.Text(frame, height=16, wrap="none", borderwidth=0, font=("Consolas", 9),
                  background="#1E1E1E", foreground="#D4D4D4", insertbackground="#D4D4D4")
    log.pack(fill="both", expand=True, pady=(18, 18))
    buttons = ttk.Frame(frame)
    buttons.pack(anchor="w")
    if on_stop is not None:  # only a forced run can be ended from here with its report intact
        ttk.Button(buttons, text="Stop and analyse", command=on_stop).pack(side="left", padx=(0, 8))
    ttk.Button(buttons, text="Back to menu  (ends the run)",
               command=on_back).pack(side="left")
    return {"frame": frame, "status": status, "log": log}
