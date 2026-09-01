import os
from pathlib import Path

from functions.open_path import open_path


def test_hands_the_path_to_windows(monkeypatch, tmp_path):
    """The results panel has no viewers of its own; it defers to whatever opens a PDF."""
    opened = []
    monkeypatch.setattr(os, "startfile", opened.append, raising=False)
    target = tmp_path / "Run 1.pdf"
    open_path(target)
    assert opened == [target]


def test_works_for_a_folder_too(monkeypatch, tmp_path):
    opened = []
    monkeypatch.setattr(os, "startfile", opened.append, raising=False)
    open_path(tmp_path)
    assert opened == [Path(tmp_path)]
