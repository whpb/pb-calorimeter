from functions import tokens as t


def grid_span(columns):
    """The pixel width of N columns of the Swiss grid, inner gutters included."""
    return columns * t.COLUMN + (columns - 1) * t.GUTTER
