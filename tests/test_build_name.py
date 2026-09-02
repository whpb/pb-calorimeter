import tkinter as tk

from conftest import canvas_text, descendants, drawn, find, packed_height, text_of

from functions.build_name import HINT, LABEL, build_name


def _screen(tk_root, backdrop, on_start=lambda name: None, on_back=lambda: None):
    return build_name(tk_root, backdrop, on_start, on_back)


def _entry(canvas):
    """The one text box on the screen, which is what the operator came here to fill in."""
    return [w for w in descendants(canvas) if isinstance(w, tk.Entry)][0]


def test_asks_for_the_name_before_recording(tk_root, backdrop):
    canvas = _screen(tk_root, backdrop)
    assert "Run an Experiment" in canvas_text(canvas)
    assert LABEL in text_of(canvas) and HINT in text_of(canvas)


def test_starting_passes_the_typed_name_on(tk_root, backdrop):
    names = []
    canvas = _screen(tk_root, backdrop, names.append)
    _entry(canvas).insert(0, "Copper block")
    find(canvas, "Start recording").invoke()
    assert names == ["Copper block"]


def test_a_blank_name_still_starts_the_run(tk_root, backdrop):
    """The fallback is the date and time; being at the rig must never mean being blocked."""
    names = []
    find(_screen(tk_root, backdrop, names.append), "Start recording").invoke()
    assert names == [""]


def test_submitting_the_box_starts_the_run_too(tk_root, backdrop):
    """Return in the box does what the button does, so a name can be typed and entered."""
    names = []
    canvas = _screen(tk_root, backdrop, names.append)
    entry = _entry(canvas)
    entry.insert(0, "Nickel block")
    entry.invoke()
    assert names == ["Nickel block"]


def test_backing_out_starts_nothing(tk_root, backdrop):
    started, backed = [], []
    canvas = _screen(tk_root, backdrop, started.append, lambda: backed.append(1))
    find(canvas, "Back to menu").invoke()
    assert (started, backed) == ([], [1])


def test_offers_only_the_two_ways_on(tk_root, backdrop):
    canvas = _screen(tk_root, backdrop)
    assert [w.cget("text") for w in drawn(canvas) if "text" in w.keys()] == [
        "Back to menu", "Start recording  →"]


def test_the_field_fits_inside_the_panel(tk_root, backdrop):
    """The panel is a fixed size, so a hint that wrapped to a second line would be clipped."""
    canvas = _screen(tk_root, backdrop)
    inner = [w for w in descendants(canvas) if w.winfo_class() == "Frame"
             and w.place_info().get("height")][0]
    inner.update_idletasks()
    assert packed_height(inner) <= int(inner.place_info()["height"])
