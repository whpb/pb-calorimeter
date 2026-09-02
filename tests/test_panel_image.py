from PIL import Image

from functions.panel_image import PAD, SHADOW_BLUR, SHADOW_DROP, panel_image


def test_leaves_the_blur_room_on_every_edge():
    assert panel_image((100, 40), 8, "#FFFFFF").size == (100 + PAD * 2, 40 + PAD * 2)


def test_the_pad_can_be_tightened_for_a_small_shadow():
    assert panel_image((54, 54), 27, "#135892", blur=0, pad=0).size == (54, 54)


def test_the_panel_is_the_fill_and_the_corners_are_not():
    panel = panel_image((100, 100), 20, "#135892", blur=0, pad=0)
    assert panel.getpixel((50, 50)) == (19, 88, 146, 255)
    assert panel.getpixel((0, 0))[3] == 0  # rounded away


def test_a_backdrop_is_composited_and_comes_back_opaque():
    plate = Image.new("RGB", (100 + PAD * 2, 40 + PAD * 2), "#CDECE9")
    panel = panel_image((100, 40), 8, "#FFFFFF", plate)
    assert panel.mode == "RGB"
    assert panel.getpixel((PAD + 50, PAD + 20)) == (255, 255, 255)
    assert panel.getpixel((0, 0)) == (205, 236, 233)  # untouched backdrop, beyond the blur


def test_the_shadow_darkens_below_the_panel():
    """It falls downward, in the dark accent - a blue shade, never black."""
    plate = Image.new("RGB", (100 + PAD * 2, 40 + PAD * 2), "#FFFFFF")
    panel = panel_image((100, 40), 8, "#FFFFFF", plate)
    below = panel.getpixel((PAD + 50, PAD + 40 + 6))
    above = panel.getpixel((PAD + 50, PAD - 6))
    assert sum(below) < sum(above) < 765


def test_the_shadow_is_not_cropped_by_the_padding():
    """PAD has to cover the blur's reach plus its drop, or the panel gets a hard bottom line."""
    assert PAD >= SHADOW_BLUR * 2 + SHADOW_DROP


def test_a_tighter_pad_still_holds_the_whole_shadow():
    """The buttons pass their own smaller pad; the edge row must be clear of the blur."""
    panel = panel_image((80, 30), 15, "#135892", blur=3, pad=3 * 2 + SHADOW_DROP)
    assert panel.getpixel((0, panel.height - 1))[3] == 0
