from functions import tokens as t
from functions.build_card import build_card
from functions.grid_span import grid_span

SHELF = (t.MARGIN, 520, grid_span(12), 68)


def build_shelf(canvas):
    """The strip along the foot of every screen; returns the frame to pack buttons into."""
    return build_card(canvas, SHELF, t.SPACE[1])
