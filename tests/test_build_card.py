import tkinter as tk

from functions import tokens as t
from functions.build_card import build_card
from functions.panel_image import PAD

BOX = (48, 100, 300, 200)


def _canvas(tk_root):
    return tk.Canvas(tk_root, width=t.WIDTH, height=t.HEIGHT)


def test_hands_back_a_frame_that_packs_like_any_other(tk_root):
    inner = build_card(_canvas(tk_root), BOX)
    tk.Label(inner, text="content").pack()
    assert [w.cget("text") for w in inner.winfo_children()] == ["content"]


def test_the_panel_is_drawn_not_placed(tk_root):
    """As an opaque widget, the card beside it would paint over this one's shadow."""
    canvas = _canvas(tk_root)
    build_card(canvas, BOX)
    assert [canvas.type(i) for i in canvas.find_all()] == ["image"]


def test_the_panel_lands_where_it_was_asked_to(tk_root):
    canvas = _canvas(tk_root)
    build_card(canvas, BOX)
    assert canvas.coords(canvas.find_all()[0]) == [BOX[0] - PAD, BOX[1] - PAD]


def test_the_content_is_inset_from_the_panel_edge(tk_root):
    inner = build_card(_canvas(tk_root), BOX, inset=t.SPACE[4])
    assert int(inner.place_info()["width"]) == BOX[2] - t.SPACE[4] * 2
    assert int(inner.place_info()["x"]) == BOX[0] + t.SPACE[4]


def test_the_content_never_squares_off_the_rounded_corners(tk_root):
    """The inner frame is opaque, so its corner has to fall inside the panel's arc."""
    for inset in (t.SPACE[1], t.SPACE[4]):
        assert inset >= t.RADIUS * (1 - 2 ** -0.5)


def test_neighbouring_cards_both_survive(tk_root):
    canvas = _canvas(tk_root)
    build_card(canvas, (48, 236, 348, 272))
    build_card(canvas, (416, 236, 348, 272))
    assert len(canvas.panels) == 2  # both images are kept, or Tk would collect one
