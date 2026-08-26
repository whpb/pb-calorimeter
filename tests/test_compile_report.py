import json

import pytest

from functions import compile_report as module
from functions.plot_work_curve import plot_work_curve

SUMMARY = {
    "samples": 3,
    "duration_min": 2.5,
    "baseline_w": 1.2,
    "peak_w": -30.0,
    "energy_j": 1234.5,
    "direction": "added to",
    "plot": "results.png",
    "finished": "2026-08-26T12:00:00",
}


@pytest.fixture
def run_folder(tmp_path):
    """A results folder holding the work-curve PNG the template expects to find."""
    save_path = tmp_path / "results.csv"
    plot_work_curve([(0.0, 0.0, 0.0), (1.0, 19.3, -0.5)], save_path)
    return save_path


def test_renders_the_repo_template_to_a_pdf(run_folder):
    """The real template must survive a real summary; a Typst error is silent otherwise."""
    pdf = module.compile_report(SUMMARY, run_folder)
    assert pdf == run_folder.with_suffix(".pdf")
    assert pdf.read_bytes().startswith(b"%PDF")


def test_copies_the_template_beside_the_results(run_folder):
    module.compile_report(SUMMARY, run_folder)
    template = module.Path(__file__).resolve().parent.parent / module.TEMPLATE
    assert run_folder.with_suffix(".typ").read_text() == template.read_text()


def test_writes_the_summary_as_json(run_folder):
    module.compile_report(SUMMARY, run_folder)
    assert json.loads(run_folder.with_suffix(".json").read_text(encoding="utf-8")) == SUMMARY


def test_reports_a_broken_template_without_raising(run_folder, tmp_path, monkeypatch, capsys):
    broken = tmp_path / "broken.typ"
    broken.write_text("#panic('nope')", encoding="utf-8")
    monkeypatch.setattr(module, "TEMPLATE", str(broken))
    assert module.compile_report(SUMMARY, run_folder) is None
    assert "Typst failed" in capsys.readouterr().out


def test_leaves_the_inputs_behind_when_typst_fails(run_folder, tmp_path, monkeypatch, capsys):
    """A failed render must not cost the operator the numbers from the run."""
    broken = tmp_path / "broken.typ"
    broken.write_text("#panic('nope')", encoding="utf-8")
    monkeypatch.setattr(module, "TEMPLATE", str(broken))
    module.compile_report(SUMMARY, run_folder)
    assert run_folder.with_suffix(".json").exists() and run_folder.with_suffix(".typ").exists()


def test_ships_the_repo_assets_with_the_report(run_folder):
    """The template can only read files under the Typst root, so assets/ has to travel."""
    module.compile_report(SUMMARY, run_folder)
    repo_assets = module.Path(__file__).resolve().parent.parent / module.ASSETS
    copied = run_folder.parent / module.ASSETS
    assert {path.name for path in copied.iterdir()} == {path.name for path in repo_assets.iterdir()}


def test_the_template_reads_its_data_by_relative_name(run_folder):
    """root is the results folder, so sys.inputs.data is a bare filename, not a path."""
    module.compile_report(SUMMARY, run_folder)
    assert "sys.inputs.data" in run_folder.with_suffix(".typ").read_text()
