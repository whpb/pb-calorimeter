import pytest

from functions.icon_glyph import TABLE, icon_glyph


def test_returns_a_single_character():
    glyph = icon_glyph("flask")
    assert len(glyph) == 1 and ord(glyph) > 0xE000  # the private use area, where icons live


def test_every_icon_the_interface_asks_for_exists():
    from functions.build_menu import OPTIONS
    from functions.build_results import FILES

    for icon, *_ in OPTIONS:
        assert icon in TABLE
    for _, _, icon in FILES:
        assert icon in TABLE
    assert "folder-open" in TABLE


def test_an_unknown_name_says_so(): 
    with pytest.raises(KeyError, match="no Tabler icon named 'not-an-icon'"):
        icon_glyph("not-an-icon")
