from tkinter import ttk

import pytest

from functions import build_results as module


@pytest.fixture
def report(tmp_path):
    """A finished run: everything except the Typst source, so the panel has to skip one."""
    for suffix in (".pdf", ".csv", ".png", ".json"):
        (tmp_path / "Run 1").with_suffix(suffix).write_text("x")
    return tmp_path / "Run 1.csv"


def _buttons(frame):
    found = []
    for widget in frame.winfo_children():
        found.extend([widget] if isinstance(widget, ttk.Button) else
                     [w for w in widget.winfo_children() if isinstance(w, ttk.Button)])
    return [b.cget("text") for b in found]


def test_links_every_file_the_run_produced(tk_root, report):
    labels = " ".join(_buttons(module.build_results(tk_root, report, lambda: None)))
    for name in ("Run 1.pdf", "Run 1.csv", "Run 1.png", "Run 1.json"):
        assert name in labels


def test_omits_a_file_that_was_never_written(tk_root, report):
    """A failed Typst render leaves no PDF; the panel must not offer a dead link."""
    labels = " ".join(_buttons(module.build_results(tk_root, report, lambda: None)))
    assert "Run 1.typ" not in labels


def test_opens_a_file_through_the_shell(tk_root, report, monkeypatch):
    opened = []
    monkeypatch.setattr(module, "open_path", opened.append)
    frame = module.build_results(tk_root, report, lambda: None)
    [w for w in frame.winfo_children()
     if isinstance(w, ttk.Button) and "Report" in w.cget("text")][0].invoke()
    assert opened == [report.with_suffix(".pdf")]


def test_offers_the_containing_folder(tk_root, report, monkeypatch):
    opened = []
    monkeypatch.setattr(module, "open_path", opened.append)
    frame = module.build_results(tk_root, report, lambda: None)
    [w for w in frame.winfo_children()
     if isinstance(w, ttk.Button) and "folder" in w.cget("text")][0].invoke()
    assert opened == [report.parent]


def test_always_offers_the_way_back(tk_root, report):
    assert "Back to menu" in _buttons(module.build_results(tk_root, report, lambda: None))


def test_offers_to_carry_on_only_while_testing_mode_is_alive(tk_root, report):
    """Re-analysis exits after one report, so there is nothing to continue."""
    alone = _buttons(module.build_results(tk_root, report, lambda: None))
    both = _buttons(module.build_results(tk_root, report, lambda: None, lambda: None))
    assert "Continue testing" not in alone and "Continue testing" in both
