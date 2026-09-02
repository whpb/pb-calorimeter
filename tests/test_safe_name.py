from functions.safe_name import safe_name


def test_keeps_an_ordinary_name_untouched():
    assert safe_name("Copper block 20 W") == "Copper block 20 W"


def test_replaces_characters_windows_will_not_take_in_a_folder_name():
    assert safe_name('Sample A: 20/09 <2>') == "Sample A 20 09 2"


def test_collapses_the_whitespace_it_leaves_behind():
    assert safe_name("  Copper   block  ") == "Copper block"


def test_strips_trailing_dots_and_spaces():
    """Legal to type, illegal to store: Windows silently drops them and the path moves."""
    assert safe_name("Run 1. ") == "Run 1"


def test_truncates_a_very_long_name():
    assert len(safe_name("x" * 200)) == 60


def test_gives_nothing_back_when_nothing_usable_survives():
    """The caller's cue to fall back to the FileName pattern, rather than refuse to record."""
    assert safe_name("///") == "" and safe_name("") == "" and safe_name(None) == ""
