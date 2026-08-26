import pytest

from functions import generate_report as module

HISTORY = [(0.0, 0.0, 0.0), (1.0, 19.3, -0.5), (2.5, 12.0, -1.25)]


@pytest.fixture
def summary(monkeypatch):
    """Capture what generate_report hands to Typst, without rendering a PDF."""
    captured = []
    monkeypatch.setattr(module, "compile_report",
                        lambda summary, path: captured.append(summary) or path.with_suffix(".pdf"))
    monkeypatch.setattr(module, "plot_work_curve", lambda history, path: path.with_suffix(".png"))
    return captured


def test_says_nothing_useful_without_samples(tmp_path, capsys):
    module.generate_report([], 0.0, 0.0, tmp_path / "results.csv")
    assert "No samples recorded" in capsys.readouterr().out
    assert not any(tmp_path.iterdir())


def test_summarises_the_run(summary, tmp_path):
    module.generate_report(HISTORY, 1234.5, 1.2, tmp_path / "results.csv")
    assert summary[0]["samples"] == 3
    assert summary[0]["duration_min"] == 2.5  # last elapsed minus first, not sample count
    assert summary[0]["baseline_w"] == 1.2
    assert summary[0]["energy_j"] == 1234.5


def test_peak_keeps_the_sign_of_the_largest_excursion(summary, tmp_path):
    module.generate_report([(0.0, 5.0, 0.0), (1.0, -30.0, 0.0)], 0.0, 0.0, tmp_path / "results.csv")
    assert summary[0]["peak_w"] == -30.0


def test_direction_follows_the_sign_of_the_energy(summary, tmp_path):
    module.generate_report(HISTORY, 10.0, 0.0, tmp_path / "results.csv")
    module.generate_report(HISTORY, -10.0, 0.0, tmp_path / "results.csv")
    assert [entry["direction"] for entry in summary] == ["added to", "removed from"]


def test_passes_the_plot_by_name_not_path(summary, tmp_path):
    module.generate_report(HISTORY, 0.0, 0.0, tmp_path / "results.csv")
    assert summary[0]["plot"] == "results.png"  # relative to the Typst root


def test_prints_the_headline_energy_to_the_console_log(summary, tmp_path, capsys):
    module.generate_report(HISTORY, 1234.5, 1.2, tmp_path / "results.csv")
    out = capsys.readouterr().out
    assert "3 samples over 2.50 min" in out
    assert "1234.5 J (1.234 kJ added to the plate)" in out


def test_announces_the_pdf(summary, tmp_path, capsys):
    module.generate_report(HISTORY, 0.0, 0.0, tmp_path / "results.csv")
    assert "results.pdf" in capsys.readouterr().out


def test_stays_quiet_about_a_report_that_failed_to_render(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(module, "compile_report", lambda summary, path: None)
    module.generate_report(HISTORY, 0.0, 0.0, tmp_path / "results.csv")
    assert "Report written" not in capsys.readouterr().out


def test_renders_a_real_pdf_end_to_end(tmp_path):
    module.generate_report(HISTORY, 1234.5, 1.2, tmp_path / "results.csv")
    rendered = {path.suffix for path in tmp_path.iterdir() if path.is_file()}
    assert rendered == {".png", ".typ", ".json", ".pdf"}
