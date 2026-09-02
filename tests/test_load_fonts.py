from functions import load_fonts as module


def test_reports_nothing_when_the_files_are_not_bundled(monkeypatch, tmp_path):
    """Lato may be installed on the machine instead; a missing bundle is not an error."""
    monkeypatch.setattr(module, "BUNDLED", ("Nothing-Regular.ttf",))
    monkeypatch.setattr(module.Path, "resolve", lambda self: tmp_path / "functions" / "x.py")
    assert module.load_fonts() == []


def test_the_icon_font_is_not_registered_here():
    """Pillow reads that .ttf straight off disk, so it never needs to be a Tk family."""
    assert not any("tabler" in name for name in module.BUNDLED)


def test_registers_privately(): 
    """A private registration is visible to this process only - the rig is left untouched."""
    assert module.FR_PRIVATE == 0x10
