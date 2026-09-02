import pytest
from conftest import drawn, packed_height, text_of

from functions.build_menu import CARDS_Y, CARD_H, OPTIONS
from functions.build_menu_card import build_menu_card
from functions.grid_span import grid_span

BOX = (48, CARDS_Y, grid_span(4), CARD_H)
OPTION = ("player-play", "Force run", "Start and stop one run from here", "Start recording")


def test_shows_the_heading_and_the_sentence(canvas):
    inner = build_menu_card(canvas, BOX, OPTION, lambda: None)
    assert OPTION[1] in text_of(inner) and OPTION[2] in text_of(inner)


def test_the_action_is_the_only_thing_to_press(canvas):
    pressed = []
    inner = build_menu_card(canvas, BOX, OPTION, lambda: pressed.append(1))
    buttons = drawn(inner)
    assert [b.cget("text") for b in buttons] == [OPTION[3]]
    buttons[0].invoke()
    assert pressed == [1]


@pytest.mark.parametrize("option", OPTIONS, ids=[title for _, title, _, _ in OPTIONS])
def test_the_real_content_fits_inside_the_card(canvas, option):
    """Every sentence is packed into a fixed panel, so the longest one sets the card height."""
    inner = build_menu_card(canvas, BOX, option, lambda: None)
    inner.update_idletasks()
    assert packed_height(inner) <= int(inner.place_info()["height"])
