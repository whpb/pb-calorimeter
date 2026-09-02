import pytest

from functions.build_button import EDGE, VARIANTS, build_button

# A withdrawn root delivers no events, so the wiring is checked by the bindings it registers
# and the behaviour by .invoke(); the appearance is checked by eye against a screenshot.
# Tk normalises the key names it was given: <Return> is stored as <Key-Return>.
WIRED = {"<Button-1>", "<Key-Return>", "<Key-space>", "<Enter>", "<Leave>"}


def test_the_command_can_be_fired_without_an_event(tk_root):
    pressed = []
    build_button(tk_root, "Go", lambda: pressed.append(1)).invoke()
    assert pressed == [1]


def test_the_mouse_and_the_keyboard_both_reach_it(tk_root):
    """A drawn label is not a button, so focus, click and Return have to be wired by hand."""
    button = build_button(tk_root, "Go", lambda: None)
    assert WIRED <= set(button.bind())
    assert str(button.cget("takefocus")) == "1"  # Tk 9 returns an int, not a str


def test_the_size_is_the_footprint_shadow_included(tk_root):
    button = build_button(tk_root, "Go", lambda: None, size=(200, 52))
    assert (button.faces[0].width(), button.faces[0].height()) == (200, 52)
    assert EDGE * 2 < 52  # the pill still has room inside it


def test_it_carries_a_second_face_to_hover_with(tk_root):
    button = build_button(tk_root, "Go", lambda: None)
    assert len(button.faces) == 2 and button.cget("image") == str(button.faces[0])


def test_every_variant_names_a_real_set_of_colours(tk_root):
    for variant in VARIANTS:
        button = build_button(tk_root, "Go", lambda: None, variant)
        assert button.cget("foreground") == VARIANTS[variant][1]


def test_an_unknown_variant_says_so(tk_root):
    with pytest.raises(KeyError):
        build_button(tk_root, "Go", lambda: None, "flamboyant")
