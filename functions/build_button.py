import tkinter as tk

from PIL import Image, ImageTk

from functions import tokens as t
from functions.panel_image import panel_image

EDGE = 8  # room inside the widget for the shadow, so `size` is the footprint on screen
# name -> (fill, ink, hovered fill, outline, shadow blur)
VARIANTS = {"primary": (t.BRAND, t.WHITE, t.BRAND_DEEP, None, 5),
            "secondary": (t.WHITE, t.BRAND, t.ACCENT_3, t.ACCENT_1, 0),
            "quiet": (t.WHITE, t.BODY, t.ACCENT_3, t.LINE, 0)}


def build_button(parent, text, command, variant="primary", size=(200, 40), ground=t.WHITE):
    """A rounded button drawn as an image, because ttk cannot round a corner.

    `size` is the widget's footprint; the pill inside it is inset by EDGE to leave the
    shadow room. `ground` is the flat colour behind, which the soft edges are baked against.
    Hover swaps the image; Return and Space activate it like a click. The command is also
    hung on the widget as .invoke(), mirroring ttk.Button, so callers need no event to fire it.
    """
    fill, ink, hovered, outline, blur = VARIANTS[variant]
    pill = (size[0] - EDGE * 2, size[1] - EDGE * 2)
    plate = Image.new("RGB", size, ground)
    faces = [ImageTk.PhotoImage(panel_image(pill, pill[1] // 2, colour, plate, outline,
                                            blur, EDGE), master=parent)
             for colour in (fill, hovered)]
    button = tk.Label(parent, image=faces[0], text=text, compound="center", font=t.BUTTON,
                      foreground=ink, background=ground, borderwidth=0, highlightthickness=0,
                      cursor="hand2", takefocus=True)
    button.faces, button.invoke = faces, command
    button.bind("<Enter>", lambda _: button.configure(image=faces[1]))
    button.bind("<Leave>", lambda _: button.configure(image=faces[0]))
    for sequence in ("<Button-1>", "<Return>", "<space>"):
        button.bind(sequence, lambda _: command())
    return button
