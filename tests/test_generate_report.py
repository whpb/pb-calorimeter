import pytest

from functions import generate_report as module

HISTORY = [(0.0, 0.0, 0.0), (1.0, 19.3, -0.5), (2.5, 12.0, -1.25)]


@pytest.fixture
def quiet_plot(monkeypatch):
    """Skip the real render; plotting is covered by test_plot_work_curve."""
    monkeypatch.setattr(module, "plot_work_curve", lambda history, path: path.with_suffix(".png"))


def test_says_nothing_useful_without_samples(tmp_path, capsys):
    module.generate_report([], 0.0, 0.0, tmp_path / "results.csv")
    assert "No samples recorded" in capsys.readouterr().out
    assert not (tmp_path / "results.txt").exists()


def test_writes_a_report_beside_the_results(quiet_plot, tmp_path, capsys):
    module.generate_report(HISTORY, 1234.5, 1.2, tmp_path / "results.csv")
    report = (tmp_path / "results.txt").read_text(encoding="utf-8")
    assert report == capsys.readouterr().out.rsplit("Report written", 1)[0]


def test_summarises_the_run(quiet_plot, tmp_path):
    module.generate_report(HISTORY, 1234.5, 1.2, tmp_path / "results.csv")
    report = (tmp_path / "results.txt").read_text(encoding="utf-8")
    assert "Samples:         3" in report
    assert "Duration:        2.50 min" in report  # last elapsed minus first, not sample count
    assert "Baseline Q_abs:  1.20 W" in report


def test_reports_energy_as_the_headline_with_its_direction(quiet_plot, tmp_path):
    module.generate_report(HISTORY, 1234.5, 0.0, tmp_path / "results.csv")
    assert "1234.5 J (1.234 kJ added to the plate)" in (tmp_path / "results.txt").read_text()
    module.generate_report(HISTORY, -2000.0, 0.0, tmp_path / "other.csv")
    assert "2.000 kJ removed from the plate" in (tmp_path / "other.txt").read_text()


def test_peak_keeps_the_sign_of_the_largest_excursion(quiet_plot, tmp_path):
    history = [(0.0, 5.0, 0.0), (1.0, -30.0, 0.0), (2.0, 12.0, 0.0)]
    module.generate_report(history, 0.0, 0.0, tmp_path / "results.csv")
    assert "Peak Q_relative: -30.00 W" in (tmp_path / "results.txt").read_text()


def test_plots_the_work_curve(tmp_path):
    module.generate_report(HISTORY, 100.0, 0.0, tmp_path / "results.csv")
    assert (tmp_path / "results.png").exists()
    assert "Work curve:      results.png" in (tmp_path / "results.txt").read_text()
