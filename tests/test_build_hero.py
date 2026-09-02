from conftest import canvas_text

from functions.build_hero import LOGO, build_hero


def test_names_the_application_and_says_what_it_does(canvas):
    build_hero(canvas)
    assert canvas_text(canvas) == ["PB Calorimeter", "Indirect calorimetry on the Polar Bear"]


def test_carries_the_logo_and_nothing_else(canvas):
    """The equipment photograph was tried here and dropped; the masthead is logo and type."""
    build_hero(canvas)
    assert [canvas.type(i) for i in canvas.find_all()].count("image") == 1


def test_the_logo_is_resampled_rather_than_halved(canvas):
    """Tk's own subsample() only divides by whole numbers; 126 is not a factor of 164."""
    build_hero(canvas)
    assert (canvas.logo.width(), canvas.logo.height()) == (LOGO, LOGO)


def test_survives_missing_artwork(canvas, monkeypatch, tmp_path):
    """Branding is decoration; the masthead must still carry its words without it."""
    monkeypatch.setattr("functions.build_hero.ASSETS", tmp_path)
    build_hero(canvas)
    assert "PB Calorimeter" in canvas_text(canvas)
    assert not [i for i in canvas.find_all() if canvas.type(i) == "image"]
