from PIL import Image, ImageDraw, ImageFilter

SHADOW_DROP = 5
SHADOW_BLUR = 12
SHADOW_RGBA = (27, 5, 77, 58)  # the dark accent at low alpha - a blue shade, never black
PAD = SHADOW_BLUR * 2 + SHADOW_DROP


def panel_image(size, radius, fill, backdrop=None, outline=None, blur=SHADOW_BLUR, pad=PAD):
    """A rounded panel with a soft shadow, flattened onto whatever sits behind it.

    The result is `pad` larger than `size` on every edge so the blur has room, so place it at
    (x - pad, y - pad) to land the panel itself at (x, y). Pass `backdrop` - whatever is
    behind, at exactly that padded size - to composite against it; omit it for a bare RGBA.
    """
    width, height = size
    panel = Image.new("RGBA", (width + pad * 2, height + pad * 2), (0, 0, 0, 0))
    box = [pad, pad, pad + width - 1, pad + height - 1]
    if blur:
        cast = Image.new("RGBA", panel.size, (0, 0, 0, 0))
        ImageDraw.Draw(cast).rounded_rectangle(
            [box[0], box[1] + SHADOW_DROP, box[2], box[3] + SHADOW_DROP], radius,
            fill=SHADOW_RGBA)
        panel = Image.alpha_composite(panel, cast.filter(ImageFilter.GaussianBlur(blur)))
    ImageDraw.Draw(panel).rounded_rectangle(box, radius, fill=fill, outline=outline,
                                            width=1 if outline else 0)
    if backdrop is None:
        return panel
    plate = backdrop.convert("RGBA")
    plate.alpha_composite(panel)
    return plate.convert("RGB")
