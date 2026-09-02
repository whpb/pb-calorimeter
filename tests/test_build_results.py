import pytest
from conftest import canvas_text, descendants, drawn, find, packed_height, text_of

from functions import build_results as module


@pytest.fixture
def report(tmp_path):
    """A finished run: everything except the Typst source, so the panel has to skip one."""
    for suffix in (".pdf", ".csv", ".png", ".json"):
        (tmp_path / "Run 1").with_suffix(suffix).write_text("x")
    return tmp_path / "Run 1.csv"


def test_links_every_file_the_run_produced(tk_root, backdrop, report):
    shown = " ".join(text_of(module.build_results(tk_root, backdrop, report, lambda: None)))
    for name in ("Run 1.pdf", "Run 1.csv", "Run 1.png", "Run 1.json"):
        assert name in shown


def test_omits_a_file_that_was_never_written(tk_root, backdrop, report):
    """A failed Typst render leaves no PDF; the panel must not offer a dead link."""
    shown = " ".join(text_of(module.build_results(tk_root, backdrop, report, lambda: None)))
    assert "Run 1.typ" not in shown


def test_opens_a_file_through_the_shell(tk_root, backdrop, report, monkeypatch):
    opened = []
    monkeypatch.setattr(module, "open_path", opened.append)
    find(module.build_results(tk_root, backdrop, report, lambda: None), "Run 1.pdf").invoke()
    assert opened == [report.with_suffix(".pdf")]


def test_offers_the_containing_folder(tk_root, backdrop, report, monkeypatch):
    opened = []
    monkeypatch.setattr(module, "open_path", opened.append)
    find(module.build_results(tk_root, backdrop, report, lambda: None),
         "Containing folder").invoke()
    assert opened == [report.parent]


def test_names_the_run_it_finished(tk_root, backdrop, report):
    canvas = module.build_results(tk_root, backdrop, report, lambda: None)
    assert "Run complete" in canvas_text(canvas)
    assert report.stem in text_of(canvas)


def test_always_offers_the_way_back(tk_root, backdrop, report):
    pressed = []
    canvas = module.build_results(tk_root, backdrop, report, lambda: pressed.append(1))
    find(canvas, "Back to menu").invoke()
    assert pressed == [1]


def test_offers_to_carry_on_only_while_testing_mode_is_alive(tk_root, backdrop, report):
    """Re-analysis exits after one report, so there is nothing to continue."""
    alone = drawn(module.build_results(tk_root, backdrop, report, lambda: None))
    both = drawn(module.build_results(tk_root, backdrop, report, lambda: None, lambda: None))
    texts = lambda widgets: [w.cget("text") for w in widgets if "text" in w.keys()]
    assert "Continue testing" not in texts(alone) and "Continue testing" in texts(both)


def test_every_row_fits_inside_the_panel(tk_root, backdrop, report, tmp_path):
    """Six rows are packed into a fixed panel; one too many would be clipped, not scrolled."""
    (tmp_path / "Run 1.typ").write_text("x")  # the fullest case: every file present
    canvas = module.build_results(tk_root, backdrop, report, lambda: None)
    inner = [w for w in descendants(canvas) if w.winfo_class() == "Frame"
             and w.place_info().get("height")][0]
    inner.update_idletasks()
    assert packed_height(inner) <= int(inner.place_info()["height"])
