from conftest import canvas_text

from functions import tokens as t
from functions.build_hero import EQUIPMENT, EQUIPMENT_Y, LOGO, build_hero
from functions.build_menu import CARDS_Y

TITLE = "Polar Bear Calorimeter"


def test_names_the_application_and_says_what_it_does(canvas):
    build_hero(canvas)
    assert canvas_text(canvas) == [TITLE, "Measures heat transfer to and from the Polar Bear plate."]


def test_carries_the_logo_and_the_equipment(canvas):
    """Both are cut-outs on a photograph; a boxed JPEG was tried here once and dropped."""
    build_hero(canvas)
    assert [canvas.type(i) for i in canvas.find_all()].count("image") == 2


def test_the_logo_is_resampled_rather_than_halved(canvas):
    """Tk's own subsample() only divides by whole numbers; 126 is not a factor of 164."""
    build_hero(canvas)
    assert (canvas.logo.width(), canvas.logo.height()) == (LOGO, LOGO)


def test_the_equipment_keeps_its_proportions(canvas):
    """Scaled by height, so a replacement photograph of any shape is not squashed."""
    build_hero(canvas)
    assert canvas.equipment.height() == EQUIPMENT
    assert abs(canvas.equipment.width() / EQUIPMENT - 1024 / 1536) < 0.01


def test_the_equipment_sits_in_the_corner_and_clears_the_cards(canvas):
    """It is drawn before them, so any overlap would be a card painting over its base."""
    build_hero(canvas)
    left, top, right, bottom = canvas.bbox(canvas.find_all()[-4])  # the equipment, then the type
    assert (right, top) == (t.WIDTH - t.MARGIN, EQUIPMENT_Y)
    assert bottom <= CARDS_Y and left > t.MARGIN + LOGO


def test_survives_missing_artwork(canvas, monkeypatch, tmp_path):
    """Branding is decoration; the masthead must still carry its words without it."""
    monkeypatch.setattr("functions.build_hero.ASSETS", tmp_path)
    build_hero(canvas)
    assert TITLE in canvas_text(canvas)
    assert not [i for i in canvas.find_all() if canvas.type(i) == "image"]
