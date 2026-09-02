from conftest import drawn, text_of

from functions.build_footer import build_footer


def test_names_the_application(tk_root, backdrop):
    assert "PB Calorimeter" in text_of(build_footer(tk_root, backdrop, lambda: None))


def test_quit_is_the_only_control_on_the_shelf(tk_root, backdrop):
    pressed = []
    shelf = build_footer(tk_root, backdrop, lambda: pressed.append(1))
    assert [b.cget("text") for b in drawn(shelf)] == ["Quit"]
    drawn(shelf)[0].invoke()
    assert pressed == [1]
