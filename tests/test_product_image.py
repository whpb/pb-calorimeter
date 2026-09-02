from PIL import Image

from functions.product_image import product_image

BACKDROP = "#CDECE9"


def _shot(tmp_path):
    """A studio photograph: a grey object on white, with white margin to be trimmed away."""
    photo = Image.new("RGB", (400, 800), "#FFFFFF")
    photo.paste(Image.new("RGB", (200, 400), "#606060"), (100, 300))
    photo.save(tmp_path / "equipment.jpg")
    return tmp_path / "equipment.jpg"


def _backdrop():
    return Image.new("RGB", (600, 400), BACKDROP)


def test_stands_the_height_it_was_asked_for(tmp_path):
    assert product_image(_shot(tmp_path), 200, _backdrop(), 500, 40).height == 200


def test_the_white_studio_ground_is_multiplied_away(tmp_path):
    """Multiply is what removes the backing: white leaves the backdrop exactly as it was.

    Two corners of object, so white survives the trim in between and can be checked.
    """
    photo = Image.new("RGB", (100, 100), "#FFFFFF")
    for corner in ((10, 10), (70, 70)):
        photo.paste(Image.new("RGB", (20, 20), "#606060"), corner)
    photo.save(tmp_path / "e.jpg")
    blended = product_image(tmp_path / "e.jpg", 60, _backdrop(), 400, 0)
    assert blended.getpixel((30, 20)) == (205, 236, 233)


def test_the_object_darkens_the_scene(tmp_path):
    blended = product_image(_shot(tmp_path), 200, _backdrop(), 500, 40)
    assert sum(blended.getpixel((blended.width // 2, 60))) < sum((205, 236, 233))


def test_the_base_fades_out_rather_than_being_cut_off(tmp_path):
    blended = product_image(_shot(tmp_path), 200, _backdrop(), 500, 40)
    middle = sum(blended.getpixel((blended.width // 2, 100)))
    bottom = sum(blended.getpixel((blended.width // 2, 199)))
    assert middle < bottom <= sum((205, 236, 233))
