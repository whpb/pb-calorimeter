from conftest import canvas_text, drawn, find, text_of

from functions.build_menu import OPTIONS, build_menu


def test_offers_exactly_the_three_operator_actions(tk_root, backdrop):
    """Quit is the fourth command, but it lives on the shelf rather than in a card."""
    canvas = build_menu(tk_root, backdrop, (lambda: None,) * 4)
    for _, title, _, _ in OPTIONS:
        assert title in text_of(canvas)
    assert len(drawn(canvas)) == len(OPTIONS) + 1


def test_each_button_runs_its_own_command(tk_root, backdrop):
    pressed = []
    commands = [*(lambda name=title: pressed.append(name) for _, title, _, _ in OPTIONS),
                lambda: pressed.append("Quit")]
    canvas = build_menu(tk_root, backdrop, commands)
    for _, title, _, action in OPTIONS:
        find(canvas, action).invoke()
    find(canvas, "Quit").invoke()
    assert pressed == [title for _, title, _, _ in OPTIONS] + ["Quit"]


def test_every_action_is_explained(tk_root, backdrop):
    canvas = build_menu(tk_root, backdrop, (lambda: None,) * 4)
    for _, _, description, _ in OPTIONS:
        assert description in text_of(canvas)


def test_the_masthead_names_the_application(tk_root, backdrop):
    """The title is drawn on the canvas, not in a label, so that it can sit on the photograph."""
    assert "Polar Bear Calorimeter" in canvas_text(
        build_menu(tk_root, backdrop, (lambda: None,) * 4))


def test_survives_missing_artwork(tk_root, backdrop, monkeypatch, tmp_path):
    """Branding is decoration; the menu must still work if the assets are gone."""
    monkeypatch.setattr("functions.build_hero.ASSETS", tmp_path)
    assert len(drawn(build_menu(tk_root, backdrop, (lambda: None,) * 4))) == len(OPTIONS) + 1
