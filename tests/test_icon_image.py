from functions.icon_image import icon_image


def test_fills_the_box_it_was_asked_for():
    assert icon_image("flask", 40, "#135892").size == (40, 40)


def test_the_ink_is_centred_on_the_box():
    """The icon font declares an absurd ascent, so the ink is measured, never trusted."""
    left, top, right, bottom = icon_image("flask", 64, "#000000").getbbox()
    assert abs(left - (64 - right)) <= 2 and abs(top - (64 - bottom)) <= 2


def test_the_ink_takes_the_colour_it_was_given():
    tile = icon_image("flask", 48, "#135892")
    inked = [p for p in tile.convert("RGBA").get_flattened_data() if p[3] > 250]
    assert inked and all(p[:3] == (19, 88, 146) for p in inked)


def test_the_rest_of_the_tile_is_transparent():
    assert icon_image("flask", 48, "#135892").getpixel((0, 0))[3] == 0
