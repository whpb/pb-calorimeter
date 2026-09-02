from pathlib import Path

from functions.resolve_results_root import resolve_results_root


def test_auto_lands_under_documents(monkeypatch, settings, tmp_path):
    monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
    assert resolve_results_root(settings) == tmp_path / "Documents" / "PBCal"


def test_the_folder_is_created(monkeypatch, settings, tmp_path):
    monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
    assert resolve_results_root(settings).is_dir()


def test_an_explicit_path_is_used_as_given(settings, tmp_path):
    settings["SavePath"] = str(tmp_path / "nested" / "results")
    root = resolve_results_root(settings)
    assert root == tmp_path / "nested" / "results" and root.is_dir()


def test_asking_twice_is_harmless(settings, tmp_path):
    """It is called on every dispatch, and by the file dialog; it must not mind."""
    settings["SavePath"] = str(tmp_path / "results")
    assert resolve_results_root(settings) == resolve_results_root(settings)


def test_holds_no_run_folder_of_its_own(settings, tmp_path):
    """Resolving the root must never create a run folder - only resolve_save_path does that."""
    settings["SavePath"] = str(tmp_path / "results")
    assert list(resolve_results_root(settings).iterdir()) == []
