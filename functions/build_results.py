from tkinter import ttk

from functions.open_path import open_path

FILES = ((".pdf", "Report"), (".csv", "Results data"), (".png", "Work curve"),
         (".json", "Summary data"), (".typ", "Typst source"))


def build_results(parent, report, on_menu, on_continue=None):
    """Links to everything a finished run produced, and the way back."""
    frame = ttk.Frame(parent, padding=28)
    ttk.Label(frame, text="Run complete", font=("Segoe UI", 20, "bold")).pack(anchor="w")
    ttk.Label(frame, text=report.stem, foreground="#555555").pack(anchor="w", pady=(6, 20))
    for suffix, description in FILES:
        path = report.with_suffix(suffix)
        if path.exists():
            ttk.Button(frame, text=f"{description}  -  {path.name}", width=52,
                       command=lambda chosen=path: open_path(chosen)).pack(anchor="w", pady=2)
    ttk.Button(frame, text="Open containing folder", width=52,
               command=lambda: open_path(report.parent)).pack(anchor="w", pady=(14, 0))
    buttons = ttk.Frame(frame)
    buttons.pack(anchor="w", pady=(28, 0))
    if on_continue is not None:
        ttk.Button(buttons, text="Continue testing", command=on_continue).pack(side="left")
    ttk.Button(buttons, text="Back to menu", command=on_menu).pack(side="left", padx=(8, 0))
    return frame
