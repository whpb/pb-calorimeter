from PIL import Image

from functions import tokens as t

# White veil over the photograph, as (fraction down the window, opacity). Strong at the top
# so the title reads, thinnest at the horizon, half-strength behind the cards.
SCRIM = ((0.00, 0.93), (0.26, 0.60), (0.47, 0.14), (1.00, 0.46))


def window_backdrop(path, size):
    """The photograph, cropped to cover the window and veiled in white so text can sit on it."""
    width, height = size
    if not path.exists():
        return Image.new("RGB", size, t.CANVAS)  # branding is decoration; the app still runs
    photo = Image.open(path).convert("RGB")
    scale = max(width / photo.width, height / photo.height)
    photo = photo.resize((round(photo.width * scale), round(photo.height * scale)),
                         Image.LANCZOS)
    left, top = (photo.width - width) // 2, (photo.height - height) // 2
    photo = photo.crop((left, top, left + width, top + height))
    veil = Image.new("L", (1, height))
    veil.putdata([next(round(255 * (a0 + (a1 - a0) * (y / (height - 1) - f0) / (f1 - f0)))
                       for (f0, a0), (f1, a1) in zip(SCRIM, SCRIM[1:])
                       if f0 <= y / (height - 1) <= f1) for y in range(height)])
    photo.paste(Image.new("RGB", size, t.WHITE), (0, 0), veil.resize(size))
    return photo
