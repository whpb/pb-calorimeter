from PIL import Image, ImageTk

from functions.bundled_path import bundled_path

LOGO = bundled_path("assets") / "polarbear-logo.png"
SIZE = 64


def window_icon(root):
    """The logo, sized for the title bar and the task bar; None if the asset is missing.

    Tk's own PhotoImage would do, but only Pillow resamples smoothly - subsample() halves.
    """
    if not LOGO.exists():
        return None
    return ImageTk.PhotoImage(Image.open(LOGO).convert("RGBA").resize((SIZE, SIZE),
                                                                     Image.LANCZOS), master=root)
