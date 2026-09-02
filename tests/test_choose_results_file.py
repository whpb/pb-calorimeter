from pathlib import Path

from functions import choose_results_file as module


def _quiet_dialog(monkeypatch, chosen, seen=None):
    """Stand in for Tk so nothing is ever drawn during the suite."""
    recorded = {} if seen is None else seen  # an empty dict is falsy, so `or` would discard it
    monkeypatch.setattr(module, "Tk", lambda: type("R", (), {"withdraw": lambda s: None,
                                                             "destroy": lambda s: None})())
    monkeypatch.setattr(module.filedialog, "askopenfilename",
                        lambda **kwargs: recorded.update(kwargs) or chosen)


def test_prefers_a_path_passed_on_the_command_line(monkeypatch, settings):
    """Which is how a CSV dragged onto the .bat arrives."""
    _quiet_dialog(monkeypatch, "should not be used")
    assert module.choose_results_file([r"C:\runs\Run 1.csv"], settings) == Path(r"C:\runs\Run 1.csv")


def test_asks_when_double_clicked_with_no_argument(monkeypatch, settings, tmp_path):
    monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
    _quiet_dialog(monkeypatch, str(tmp_path / "chosen.csv"))
    assert module.choose_results_file([], settings) == tmp_path / "chosen.csv"


def test_starts_the_dialog_in_the_results_folder(monkeypatch, settings, tmp_path):
    monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
    seen = {}
    _quiet_dialog(monkeypatch, "", seen)
    module.choose_results_file([], settings)
    assert seen["initialdir"] == tmp_path / "Documents" / "PBCal"
    assert seen["filetypes"] == [("Results CSV", "*.csv")]


def test_asking_creates_no_run_folder(monkeypatch, settings, tmp_path):
    """resolve_save_path would make one; opening a file dialog must not litter the root."""
    monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
    _quiet_dialog(monkeypatch, "")
    module.choose_results_file([], settings)
    assert list((tmp_path / "Documents" / "PBCal").iterdir()) == []


def test_returns_nothing_when_the_dialog_is_cancelled(monkeypatch, settings, tmp_path):
    monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
    _quiet_dialog(monkeypatch, "")
    assert module.choose_results_file([], settings) is None
