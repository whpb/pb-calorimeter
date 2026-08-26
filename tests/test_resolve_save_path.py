from datetime import datetime
from pathlib import Path

from functions import resolve_save_path as module


def test_auto_savepath_lands_under_documents(monkeypatch, settings, tmp_path):
    monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
    path = module.resolve_save_path(settings)
    assert path.parent == tmp_path / "Documents" / "PBCal"
    assert path.parent.is_dir()  # created for us, not assumed to exist


def test_auto_filename_is_a_timestamp(monkeypatch, settings, tmp_path):
    monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
    path = module.resolve_save_path(settings)
    assert path.suffix == ".csv"
    datetime.strptime(path.stem, module.DEFAULT_FILENAME_PATTERN)  # raises if malformed


def test_explicit_folder_is_created(settings, tmp_path):
    settings["SavePath"] = str(tmp_path / "nested" / "results")
    assert module.resolve_save_path(settings).parent.is_dir()


def test_a_plain_filename_is_numbered_sequentially(settings, tmp_path):
    settings["SavePath"], settings["FileName"] = str(tmp_path), "Run"
    assert module.resolve_save_path(settings).name == "Run 1.csv"
    (tmp_path / "Run 1.csv").touch()
    assert module.resolve_save_path(settings).name == "Run 2.csv"
