import tkinter as tk

from functions import tokens as t
from functions.build_card import build_card
from functions.panel_image import PAD

BOX = (48, 100, 300, 200)


def test_hands_back_a_frame_that_packs_like_any_other(tk_root, backdrop):
    inner = build_card(tk_root, backdrop, BOX)
    tk.Label(inner, text="content").pack()
    assert [w.cget("text") for w in inner.winfo_children()] == ["content"]


def test_the_panel_lands_where_it_was_asked_to(tk_root, backdrop):
    """The label is placed back by PAD, so the panel itself starts at the box."""
    inner = build_card(tk_root, backdrop, BOX)
    assert inner.master.place_info()["x"] == str(BOX[0] - PAD)


def test_the_content_is_inset_from_the_panel_edge(tk_root, backdrop):
    inner = build_card(tk_root, backdrop, BOX, inset=t.SPACE[4])
    assert int(inner.place_info()["width"]) == BOX[2] - t.SPACE[4] * 2


def test_a_nested_panel_can_sit_on_a_flat_colour(tk_root):
    """Inside a card the backdrop is already solid, so there is nothing to crop from."""
    inner = build_card(tk_root, t.WHITE, (0, 0, 120, 60))
    assert inner.winfo_exists()
