from conftest import text_of

from functions.build_file_row import TINT, build_file_row

WIRED = {"<Button-1>", "<Enter>", "<Leave>"}


def _row(tk_root, tmp_path, command=lambda: None):
    path = tmp_path / "Run 1.pdf"
    path.write_text("x")
    return build_file_row(tk_root, "file-text", "Report", path, command)


def test_names_the_file_and_what_it_is(tk_root, tmp_path):
    shown = text_of(_row(tk_root, tmp_path))
    assert "Report" in shown and "Run 1.pdf" in shown


def test_the_whole_row_is_the_target_not_just_the_text(tk_root, tmp_path):
    """Every part of the row carries the bindings, so there is no dead space to click on."""
    row = _row(tk_root, tmp_path)
    assert WIRED <= set(row.bind())
    for child in row.winfo_children():
        assert WIRED <= set(child.bind()) or child.cget("text") == ""


def test_the_command_can_be_fired_without_an_event(tk_root, tmp_path):
    opened = []
    _row(tk_root, tmp_path, lambda: opened.append(1)).invoke()
    assert opened == [1]


def test_hovering_has_a_tint_to_move_to(tk_root, tmp_path):
    """Type only: the badge's ground is baked into its image and could not follow."""
    assert TINT[True] != TINT[False]
