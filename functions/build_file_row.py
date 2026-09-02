import tkinter as tk

from functions import tokens as t
from functions.build_badge import build_badge

TINT = {False: (t.INK, t.MUTED), True: (t.BRAND, t.BRAND)}


def build_file_row(parent, icon, description, path, command):
    """One line of the results panel: what the file is, what it is called, and a way to open it."""
    row = tk.Frame(parent, background=t.WHITE, cursor="hand2")
    build_badge(row, icon, 34, t.ACCENT_3, t.BRAND, t.WHITE, 18).pack(side="left")
    name = tk.Label(row, text=description, font=t.H2, foreground=t.INK, background=t.WHITE)
    name.pack(side="left", padx=(t.SPACE[2], 0))
    detail = tk.Label(row, text=path.name, font=t.SMALL, foreground=t.MUTED,
                      background=t.WHITE)
    detail.pack(side="left", padx=(t.SPACE[2], 0))
    arrow = tk.Label(row, text="\u2192", font=t.H2, foreground=t.ACCENT_1, background=t.WHITE)
    arrow.pack(side="right", padx=(0, t.SPACE[2]))
    row.invoke = command  # mirrors ttk.Button, so the row can be fired without an event
    for widget in (row, name, detail, arrow):
        widget.bind("<Button-1>", lambda _: command())
        for entering in (True, False):  # hover tints the type, never the badge's baked ground
            widget.bind("<Enter>" if entering else "<Leave>",
                        lambda _, on=entering: [name.configure(foreground=TINT[on][0]),
                                                detail.configure(foreground=TINT[on][1])])
    return row
