from tkinter import ttk

from functions.build_menu import build_menu, OPTIONS


def _buttons(frame):
    return [w for w in frame.winfo_children() if isinstance(w, ttk.Button)]


def test_offers_exactly_the_three_operator_actions(tk_root):
    frame = build_menu(tk_root, None, (lambda: None,) * 3)
    assert [b.cget("text") for b in _buttons(frame)] == ["Testing mode", "Re-analyse data", "Quit"]


def test_each_button_runs_its_own_command(tk_root):
    pressed = []
    commands = tuple(lambda name=name: pressed.append(name)
                     for name, _ in OPTIONS)
    frame = build_menu(tk_root, None, commands)
    for button in _buttons(frame):
        button.invoke()
    assert pressed == ["Testing mode", "Re-analyse data", "Quit"]


def test_every_action_is_explained(tk_root):
    frame = build_menu(tk_root, None, (lambda: None,) * 3)
    labels = [w.cget("text") for w in frame.winfo_children() if isinstance(w, ttk.Label)]
    for _, description in OPTIONS:
        assert description in labels


def test_survives_a_missing_logo(tk_root):
    """Branding is decoration; the menu must still work if the asset is gone."""
    assert build_menu(tk_root, None, (lambda: None,) * 3).winfo_children()
