from datetime import datetime
from pathlib import Path

from functions import resolve_save_path as module


def test_the_run_gets_its_own_folder_inside_the_results_root(settings, tmp_path):
    """Everything a run produces shares a stem, so one folder holds the lot."""
    settings["SavePath"] = str(tmp_path)
    path = module.resolve_save_path(settings, "Copper block")
    assert path == tmp_path / "Copper block" / "Copper block.csv"
    assert path.parent.is_dir()


def test_the_typed_name_is_made_safe_to_store(settings, tmp_path):
    settings["SavePath"] = str(tmp_path)
    assert module.resolve_save_path(settings, "Sample A: 20/09").parent.name == "Sample A 20 09"


def test_a_repeated_name_takes_the_next_number(settings, tmp_path):
    """A second run of the same experiment must never land in the first one's folder."""
    settings["SavePath"] = str(tmp_path)
    first = module.resolve_save_path(settings, "Copper block")
    second = module.resolve_save_path(settings, "Copper block")
    assert second == tmp_path / "Copper block 1" / "Copper block 1.csv"
    assert first.parent != second.parent


def test_auto_savepath_lands_under_documents(monkeypatch, settings, tmp_path):
    monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
    path = module.resolve_save_path(settings)
    assert path.parent.parent == tmp_path / "Documents" / "PBCal"


def test_no_name_falls_back_to_a_timestamp(monkeypatch, settings, tmp_path):
    monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
    path = module.resolve_save_path(settings)
    assert path.suffix == ".csv" and path.stem == path.parent.name
    datetime.strptime(path.stem, module.DEFAULT_FILENAME_PATTERN)  # raises if malformed


def test_an_unusable_name_falls_back_the_same_way(monkeypatch, settings, tmp_path):
    monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
    datetime.strptime(module.resolve_save_path(settings, "///").stem,
                      module.DEFAULT_FILENAME_PATTERN)


def test_explicit_folder_is_created(settings, tmp_path):
    settings["SavePath"] = str(tmp_path / "nested" / "results")
    assert module.resolve_save_path(settings).parent.parent.is_dir()


def test_a_plain_filename_is_numbered_sequentially(settings, tmp_path):
    settings["SavePath"], settings["FileName"] = str(tmp_path), "Run"
    assert module.resolve_save_path(settings).parent.name == "Run 1"
    assert module.resolve_save_path(settings).parent.name == "Run 2"


def test_never_reuses_a_folder_that_already_holds_results(settings, tmp_path):
    """Each run resolves its own folder, so a second run cannot overwrite the first."""
    settings["SavePath"] = str(tmp_path)
    first = module.resolve_save_path(settings)
    first.touch()
    assert module.resolve_save_path(settings) != first


def test_a_same_second_collision_falls_back_to_a_number(settings, tmp_path):
    settings["SavePath"], settings["FileName"] = str(tmp_path), "Run"
    (tmp_path / "Run").mkdir()  # a plain pattern with no % and no room to move
    assert module.resolve_save_path(settings).parent.name == "Run 1"
