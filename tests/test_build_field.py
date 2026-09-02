import tkinter as tk

from conftest import descendants, text_of

from functions.build_field import build_field


def _field(tk_root, on_submit=lambda: None):
    frame = tk.Frame(tk_root)
    return frame, build_field(frame, "Experiment name", "Leave it blank", on_submit)


def test_labels_the_box_and_explains_it(tk_root):
    frame, _ = _field(tk_root)
    assert text_of(frame) == ["Experiment name", "Leave it blank"]


def test_hands_back_an_entry_that_can_be_read(tk_root):
    _, entry = _field(tk_root)
    entry.insert(0, "Copper block")
    assert entry.get() == "Copper block"


def test_starts_empty(tk_root):
    """No prefilled name to delete: the operator is naming this run, not editing a default."""
    assert _field(tk_root)[1].get() == ""


def test_submitting_the_box_runs_the_command(tk_root):
    """Bound to Return, and hung on the widget as .invoke() the way the buttons are."""
    pressed = []
    _, entry = _field(tk_root, lambda: pressed.append(1))
    assert entry.bind("<Return>")  # the binding is registered
    entry.invoke()
    assert pressed == [1]


def test_the_entry_is_the_only_input(tk_root):
    frame, entry = _field(tk_root)
    assert [w for w in descendants(frame) if isinstance(w, tk.Entry)] == [entry]
