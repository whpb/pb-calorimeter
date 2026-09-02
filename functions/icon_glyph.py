import json
from pathlib import Path

# The whole Tabler set, name -> hex codepoint, so a new icon costs a string and nothing else.
TABLE = json.loads((Path(__file__).resolve().parent.parent / "assets" /
                    "tabler-codepoints.json").read_text(encoding="utf-8"))


def icon_glyph(name):
    """The character for a Tabler icon name, to be drawn in the tabler-icons font."""
    try:
        return chr(int(TABLE[name], 16))
    except KeyError:
        raise KeyError(f"no Tabler icon named {name!r}") from None
