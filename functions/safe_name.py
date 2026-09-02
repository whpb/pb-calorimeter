ILLEGAL = '<>:"/|?*' + chr(92)  # everything Windows refuses in a folder name, backslash last
LIMIT = 60


def safe_name(name):
    """Reduce a typed experiment name to something Windows will accept as a folder name.

    Returns "" when nothing usable survives, which is the caller's cue to fall back to the
    FileName pattern - an operator typing only punctuation must not stop a run starting.
    """
    kept = "".join(" " if character in ILLEGAL or ord(character) < 32 else character
                   for character in (name or ""))
    # trailing dots and spaces are legal to type and illegal to store, so they go last
    return " ".join(kept.split())[:LIMIT].rstrip(". ")
