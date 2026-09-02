from tkinter import ttk

from functions import tokens as t

# The only ttk widget left in the interface is the progress bar; everything else is drawn.
# clam is the one theme on Windows that honours these options - vista draws from bitmaps.
STYLES = {"Brand.Horizontal.TProgressbar": {
    "troughcolor": t.ACCENT_3, "background": t.BRAND, "bordercolor": t.ACCENT_3,
    "lightcolor": t.BRAND, "darkcolor": t.BRAND, "thickness": 6, "borderwidth": 0}}


def apply_theme(root):
    """Point ttk at a theme that can be styled, and load the project's styles into it."""
    style = ttk.Style(root)
    style.theme_use("clam")
    for name, options in STYLES.items():
        style.configure(name, **options)
    return style
