from PIL import Image, ImageChops

WHITE_POINT = 238  # studio grey above this is lifted to pure white before the blend
FADE = 34          # pixels of soft bottom edge, so the machine is not cut off by a hard line


def product_image(path, height, backdrop, right, top):
    """The equipment shot, its white studio background multiplied away into the scene.

    Multiply is what removes the backing: white leaves the backdrop untouched, so only the
    machine darkens it. Place the result with anchor="ne" at (right, top) - the caller never
    needs to know how wide it came out.
    """
    photo = Image.open(path).convert("RGB").point(lambda v: min(255, round(v * 255 / WHITE_POINT)))
    photo = photo.crop(photo.convert("L").point(lambda v: 255 if v < 250 else 0).getbbox())
    photo = photo.resize((round(photo.width * height / photo.height), height), Image.LANCZOS)
    plate = backdrop.crop((right - photo.width, top, right, top + height)).convert("RGB")
    mask = Image.new("L", photo.size, 255)
    mask.paste(Image.linear_gradient("L").resize((photo.width, FADE)).transpose(
        Image.Transpose.FLIP_TOP_BOTTOM), (0, height - FADE))
    plate.paste(ImageChops.multiply(plate, photo), (0, 0), mask)
    return plate
