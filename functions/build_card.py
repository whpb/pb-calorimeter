import tkinter as tk

from PIL import ImageTk

from functions import tokens as t
from functions.panel_image import PAD, panel_image


def build_card(canvas, box, inset=t.SPACE[4], fill=t.WHITE, radius=t.RADIUS):
    """A rounded panel drawn on the canvas; returns the frame to put the content in.

    `box` is (x, y, width, height). The panel is a transparent-cornered canvas image rather
    than a widget, so a neighbour's shadow blends into it and into the photograph - as an
    opaque label the last card drawn would paint over the one beside it. Only the content is
    a real widget, inset well inside the rounded corners, where pack() works as normal.
    """
    x, y, width, height = box
    image = ImageTk.PhotoImage(panel_image((width, height), radius, fill), master=canvas)
    canvas.create_image(x - PAD, y - PAD, image=image, anchor="nw")
    canvas.panels = [*getattr(canvas, "panels", []), image]  # Tk keeps no reference of its own
    inner = tk.Frame(canvas, background=fill)
    inner.place(x=x + inset, y=y + inset, width=width - inset * 2, height=height - inset * 2)
    return inner
