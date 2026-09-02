import tkinter as tk

from functions import tokens as t
from functions.build_badge import build_badge
from functions.build_button import build_button
from functions.build_card import build_card

INSET = t.SPACE[4]


def build_menu_card(parent, backdrop, box, option, command):
    """One of the operator's choices: a badge, a heading, a sentence and the way in.

    `option` is (icon, title, description, action) - see OPTIONS in build_menu.
    """
    icon, title, description, action = option
    width = box[2] - INSET * 2
    inner = build_card(parent, backdrop, box, INSET)
    build_badge(inner, icon).pack(pady=(t.SPACE[0], t.SPACE[2]))
    tk.Label(inner, text=title, font=t.H2, foreground=t.INK, background=t.WHITE).pack()
    tk.Frame(inner, height=2, width=28, background=t.ACCENT_1).pack(pady=(t.SPACE[1], t.SPACE[2]))
    tk.Label(inner, text=description, font=t.SMALL, foreground=t.BODY, background=t.WHITE,
             wraplength=width - t.SPACE[2], justify="center").pack()
    build_button(inner, action, command, size=(width, 54)).pack(side="bottom")
    return inner
