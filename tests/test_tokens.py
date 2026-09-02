from functions import tokens as t


def test_the_grid_fills_the_window_exactly():
    """Twelve columns and eleven gutters, between two margins, must come to the full width."""
    assert t.CONTENT == t.COLUMN * 12 + t.GUTTER * 11
    assert t.CONTENT + t.MARGIN * 2 == t.WIDTH


def test_the_window_stays_inside_the_rig_s_screen():
    """The brief caps the outline at 720p; the frame Windows adds is about 16 by 40."""
    assert t.WIDTH + 16 < 1280 and t.HEIGHT + 40 < 720


def test_the_spacing_scale_is_a_scale():
    assert list(t.SPACE) == sorted(t.SPACE)
    assert all(step % 4 == 0 for step in t.SPACE)
