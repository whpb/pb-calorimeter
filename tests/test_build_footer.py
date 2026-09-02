from conftest import drawn, text_of

from functions.build_footer import build_footer


def test_names_the_application(canvas):
    assert "PB Calorimeter" in text_of(build_footer(canvas, lambda: None))


def test_quit_is_the_only_control_on_the_shelf(canvas):
    pressed = []
    shelf = build_footer(canvas, lambda: pressed.append(1))
    assert [b.cget("text") for b in drawn(shelf)] == ["Quit"]
    drawn(shelf)[0].invoke()
    assert pressed == [1]
