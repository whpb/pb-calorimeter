from tkinter import ttk

from functions.apply_theme import STYLES, apply_theme


def test_switches_to_the_theme_that_can_be_styled(tk_root):
    """vista draws its widgets from bitmaps and ignores configure; clam does not."""
    assert str(apply_theme(tk_root).theme_use()) == "clam"


def test_the_progress_bar_wears_the_brand(tk_root):
    style = apply_theme(tk_root)
    assert style.lookup("Brand.Horizontal.TProgressbar", "background") == "#135892"


def test_every_style_it_declares_is_loaded(tk_root):
    style = apply_theme(tk_root)
    for name, options in STYLES.items():
        for option, value in options.items():
            assert str(style.lookup(name, option)) == str(value)
