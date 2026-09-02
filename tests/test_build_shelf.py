from functions import tokens as t
from functions.build_shelf import SHELF, build_shelf
from functions.grid_span import grid_span


def test_spans_the_full_grid(tk_root, backdrop):
    assert SHELF[2] == grid_span(12)
    assert SHELF[0] == t.MARGIN


def test_leaves_room_for_a_button(tk_root, backdrop):
    """The shelf carries 52px buttons; its inner frame has to be at least that tall."""
    shelf = build_shelf(tk_root, backdrop)
    assert int(shelf.place_info()["height"]) >= 52


def test_sits_inside_the_window(tk_root, backdrop):
    assert SHELF[1] + SHELF[3] < t.HEIGHT
