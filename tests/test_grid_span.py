from functions import tokens as t
from functions.grid_span import grid_span


def test_one_column_is_a_column():
    assert grid_span(1) == t.COLUMN


def test_a_span_swallows_the_gutters_it_crosses():
    assert grid_span(2) == t.COLUMN * 2 + t.GUTTER
    assert grid_span(4) == t.COLUMN * 4 + t.GUTTER * 3


def test_the_full_span_is_the_content_width():
    """Three four-column cards and their two gutters must equal one twelve-column card."""
    assert grid_span(12) == t.CONTENT
    assert grid_span(4) * 3 + t.GUTTER * 2 == grid_span(12)
