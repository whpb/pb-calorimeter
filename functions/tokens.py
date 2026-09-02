"""The design system: every colour, size and rhythm the interface uses, in one place.

No functions - this is the stylesheet. Change a value here and it changes everywhere.
"""

# Brand palette, as supplied.
BRAND = "#135892"
ACCENT_1 = "#4E97B3"
ACCENT_2 = "#8CCBD1"
ACCENT_3 = "#CDECE9"
DARK = "#1B054D"
WHITE = "#FFFFFF"

# Derived tones. Not supplied - mixed from the palette so text and hairlines have somewhere
# to sit between BRAND and WHITE. Flagged for review.
BRAND_DEEP = "#0F4676"   # BRAND darkened, for the pressed/hover state of a filled button
INK = DARK               # headings
BODY = "#3D5566"         # running text
MUTED = "#6E8798"        # captions and secondary labels
LINE = "#DCE9EF"         # hairlines and card borders
CANVAS = "#F2F8FA"       # page ground where no photograph shows

# Type. Lato throughout, with the Tabler icon font for glyphs.
FONT = "Lato"
MONO = "Consolas"
DISPLAY = (FONT, 32, "bold")
H1 = (FONT, 19, "bold")
H2 = (FONT, 13, "bold")
FIGURE = (FONT, 26, "bold")
TEXT = (FONT, 10)
SMALL = (FONT, 9)
CAPTION = (FONT, 8)
BUTTON = (FONT, 10, "bold")
LOG = (MONO, 9)

# Spacing scale. Everything is a multiple of 4; nothing is chosen ad hoc.
SPACE = (4, 8, 12, 16, 24, 32, 48)

# Swiss grid. Twelve columns of 72 with 20 gutters fill 1084, leaving 48 margins in 1180.
WIDTH = 1180
HEIGHT = 640
MARGIN = 48
GUTTER = 20
COLUMN = 72
CONTENT = COLUMN * 12 + GUTTER * 11
RADIUS = 10
