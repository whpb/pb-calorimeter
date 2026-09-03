import ctypes

from functions.bundled_path import bundled_path

FR_PRIVATE = 0x10  # available to this process only, so nothing is installed on the rig
BUNDLED = ("Lato-Regular.ttf", "Lato-Bold.ttf", "Lato-Black.ttf")


def load_fonts():
    """Register the bundled font files with Windows, and report which families arrived.

    The Tabler icons are NOT here: Pillow reads that .ttf straight off disk in icon_image,
    so it never needs to be a Tk font family.

    Must be called before tkinter.Tk() exists: Tk enumerates the font families once, when
    the interpreter's Tcl is initialised, and will not see anything added afterwards.
    """
    assets = bundled_path("assets")
    loaded = []
    for name in BUNDLED:
        path = assets / name
        if path.exists() and ctypes.windll.gdi32.AddFontResourceExW(str(path), FR_PRIVATE, 0):
            loaded.append(name)
    return loaded
