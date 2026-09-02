from conftest import canvas_text

from functions import tokens as t
from functions.build_screen import build_screen


def test_fills_the_window(tk_root, backdrop):
    canvas = build_screen(tk_root, backdrop, "Force run")
    assert (int(canvas.cget("width")), int(canvas.cget("height"))) == (t.WIDTH, t.HEIGHT)


def test_the_heading_is_drawn_on_the_photograph(tk_root, backdrop):
    """A canvas item has no background of its own, which a label could never manage."""
    assert canvas_text(build_screen(tk_root, backdrop, "Re-analysis")) == ["Re-analysis"]


def test_the_rule_is_cut_to_the_heading(tk_root, backdrop):
    """A fixed width would sit wrong under "Force run" and under "Re-analysis" both."""
    canvas = build_screen(tk_root, backdrop, "Run complete")
    kinds = {canvas.type(item): canvas.bbox(item) for item in canvas.find_all()}
    width = lambda box: box[2] - box[0]
    assert abs(width(kinds["rectangle"]) - width(kinds["text"])) <= 2  # bbox adds a halo


def test_survives_a_missing_logo(tk_root, backdrop, monkeypatch, tmp_path):
    monkeypatch.setattr("functions.build_screen.ASSETS", tmp_path)
    assert canvas_text(build_screen(tk_root, backdrop, "Force run")) == ["Force run"]
