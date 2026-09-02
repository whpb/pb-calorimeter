from PIL import Image

from functions import tokens as t
from functions.window_backdrop import window_backdrop

SIZE = (400, 200)


def _photograph(tmp_path, colour="#1050A0"):
    path = tmp_path / "background.png"
    Image.new("RGB", (1536, 1024), colour).save(path)
    return path


def test_covers_the_window_exactly(tmp_path):
    assert window_backdrop(_photograph(tmp_path), SIZE).size == SIZE


def test_a_missing_photograph_leaves_a_flat_ground(tmp_path):
    """Branding is decoration; every screen must still build without it."""
    backdrop = window_backdrop(tmp_path / "gone.png", SIZE)
    assert backdrop.size == SIZE and backdrop.getpixel((0, 0)) == (242, 248, 250)


def test_the_veil_is_heaviest_where_the_type_sits(tmp_path):
    """The masthead is at the top, so that is where the photograph is whitened most."""
    backdrop = window_backdrop(_photograph(tmp_path), SIZE)
    top, middle = backdrop.getpixel((200, 0)), backdrop.getpixel((200, int(200 * 0.47)))
    assert sum(top) > sum(middle)


def test_a_tall_photograph_is_cropped_rather_than_squashed(tmp_path):
    """Cover, not stretch: an aspect change must not distort the mountains."""
    path = tmp_path / "background.png"
    Image.new("RGB", (200, 800), "#1050A0").save(path)
    assert window_backdrop(path, (t.WIDTH, t.HEIGHT)).size == (t.WIDTH, t.HEIGHT)
