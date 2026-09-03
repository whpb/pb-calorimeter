from pathlib import Path

from functions import bundled_path as module


def test_finds_the_files_shipped_with_the_program():
    """From source that is the repo; the real files must be where it says they are."""
    assert module.bundled_path("settings.default.json").is_file()
    assert module.bundled_path("assets").is_dir()


def test_the_anchor_is_the_repo_root_when_running_from_source():
    assert module.ROOT == Path(__file__).resolve().parent.parent
    assert not module.FROZEN  # the suite never runs against a compiled build


def test_the_seeded_files_are_all_present_to_ship():
    """Nuitka copies these into the dist folder; a missing one is a broken install."""
    from functions.resolve_docs_folder import SEEDED

    for source in SEEDED.values():
        assert module.bundled_path(source).is_file(), source


def test_a_moved_anchor_moves_every_lookup(monkeypatch, tmp_path):
    """ROOT is read on each call, which is what lets a compiled build point elsewhere."""
    monkeypatch.setattr(module, "ROOT", tmp_path)
    assert module.bundled_path("assets") == tmp_path / "assets"
    assert module.bundled_path() == tmp_path  # no name: the bundle folder itself
