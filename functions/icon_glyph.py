import json

from functions.bundled_path import bundled_path

CODEPOINTS = bundled_path("assets") / "tabler-codepoints.json"
# The whole Tabler set, name -> hex codepoint, so a new icon costs a string and nothing else.
# Read behind .exists() like every other asset: unguarded, a missing file killed the program
# at import, before Tk opened and before anything could report why.
TABLE = json.loads(CODEPOINTS.read_text(encoding="utf-8")) if CODEPOINTS.exists() else {}


def icon_glyph(name):
    """The character for a Tabler icon name, to be drawn in the tabler-icons font."""
    if not TABLE:
        raise FileNotFoundError(f"Tabler codepoints not found at {CODEPOINTS}")
    try:
        return chr(int(TABLE[name], 16))
    except KeyError:
        raise KeyError(f"no Tabler icon named {name!r}") from None
