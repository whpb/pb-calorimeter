import tkinter as tk

from conftest import canvas_text

from functions.build_hero import build_hero


def _canvas(tk_root):
    return tk.Canvas(tk_root, width=1180, height=640)


def test_names_the_application_and_says_what_it_does(tk_root, backdrop):
    canvas = _canvas(tk_root)
    build_hero(canvas, backdrop)
    assert canvas_text(canvas) == ["PB Calorimeter", "Indirect calorimetry on the Polar Bear"]


def test_places_both_photographs(tk_root, backdrop):
    canvas = _canvas(tk_root)
    build_hero(canvas, backdrop)
    assert len([i for i in canvas.find_all() if canvas.type(i) == "image"]) == 2


def test_survives_missing_artwork(tk_root, backdrop, monkeypatch, tmp_path):
    """Branding is decoration; the masthead must still carry its words without it."""
    monkeypatch.setattr("functions.build_hero.ASSETS", tmp_path)
    canvas = _canvas(tk_root)
    build_hero(canvas, backdrop)
    assert "PB Calorimeter" in canvas_text(canvas)
    assert not [i for i in canvas.find_all() if canvas.type(i) == "image"]
