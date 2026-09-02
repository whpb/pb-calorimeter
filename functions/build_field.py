import tkinter as tk

from functions import tokens as t


def build_field(parent, label, hint, on_submit):
    """A labelled text box with its hint beneath. Returns the entry, for the caller to read.

    tk.Entry rather than ttk: the palette goes straight on, and the hairline is the widget's
    own highlight ring - the same way every other flat surface in the interface is drawn.
    """
    tk.Label(parent, text=label, font=t.H2, foreground=t.INK, background=t.WHITE,
             anchor="w").pack(fill="x")
    entry = tk.Entry(parent, font=t.TEXT, foreground=t.BODY, background=t.WHITE,
                     insertbackground=t.BRAND, relief="flat", highlightthickness=1,
                     highlightbackground=t.LINE, highlightcolor=t.ACCENT_1)
    entry.pack(fill="x", ipady=t.SPACE[2], pady=(t.SPACE[2], t.SPACE[1]))
    entry.bind("<Return>", lambda _: on_submit())  # typing a name and pressing enter is enough
    entry.invoke = on_submit  # mirrors build_button: the submit can be fired without an event
    tk.Label(parent, text=hint, font=t.SMALL, foreground=t.MUTED, background=t.WHITE,
             anchor="w").pack(fill="x")
    return entry
