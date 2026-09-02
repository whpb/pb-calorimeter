from functions import window_icon as module


def test_gives_the_title_bar_the_logo(tk_root):
    icon = module.window_icon(tk_root)
    assert (icon.width(), icon.height()) == (module.SIZE,) * 2


def test_a_missing_logo_is_not_fatal(tk_root, monkeypatch, tmp_path):
    """Branding is decoration; the window must still open without it."""
    monkeypatch.setattr(module, "LOGO", tmp_path / "gone.png")
    assert module.window_icon(tk_root) is None
