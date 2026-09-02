from functions import tokens as t
from functions.build_badge import build_badge


def test_is_exactly_the_disc_it_was_asked_for(tk_root):
    badge = build_badge(tk_root, "flask", size=48)
    assert (badge.cget("width"), badge.cget("height")) == (48, 48)


def test_the_icon_is_baked_in_so_nothing_can_reflow(tk_root):
    """The icon font's ascent is eleven times its size; as an image it cannot push anything."""
    badge = build_badge(tk_root, "flask", size=54)
    assert badge.image.width() == 54 and badge.image.height() == 54
    assert badge.cget("text") == ""


def test_takes_the_colours_it_was_given(tk_root):
    badge = build_badge(tk_root, "flask", 40, t.ACCENT_3, t.BRAND, t.WHITE, 20)
    assert badge.cget("background") == t.WHITE
