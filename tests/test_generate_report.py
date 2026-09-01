import pytest

from functions import generate_report as module

WINDOWS = {"baseline": (0.0, 0.2), "experiment": (0.3, 0.5)}
BASELINE = {"start_min": 0.0, "end_min": 0.2, "duration_min": 0.2, "samples": 3,
            "mean": 1.2, "sd": 0.4, "spread": 1.1}


def _samples():
    rows = []
    for i in range(6):
        zone = "baseline" if i <= 2 else ("experiment" if i >= 3 else "")
        rows.append({"Elapsed (min)": i / 10, "Q_relative (W)": [1.0, 2.0, 1.5, 19.3, -30.0, 12.0][i],
                     "Plate temperature change (C)": -0.5 * i,
                     "Master temperature change (C)": 0.25 * i, "Zone": zone})
    return rows


@pytest.fixture
def summary(monkeypatch):
    """Capture what generate_report hands to Typst, without rendering a PDF."""
    captured = []
    monkeypatch.setattr(module, "compile_report",
                        lambda summary, path: captured.append(summary) or path.with_suffix(".pdf"))
    monkeypatch.setattr(module, "plot_work_curve",
                        lambda samples, windows, path: path.with_suffix(".png"))
    return captured


def test_summarises_the_whole_recording(summary, tmp_path):
    module.generate_report(_samples(), WINDOWS, BASELINE, 1234.5, tmp_path / "results.csv")
    assert summary[0]["samples"] == 6
    assert summary[0]["duration_min"] == 0.5  # the run, not the selected experiment
    assert summary[0]["energy_j"] == 1234.5


def test_carries_both_zones_through_to_the_template(summary, tmp_path):
    module.generate_report(_samples(), WINDOWS, BASELINE, 0.0, tmp_path / "results.csv")
    assert summary[0]["baseline"] == BASELINE
    assert summary[0]["experiment"]["samples"] == 3
    assert summary[0]["experiment"]["duration_min"] == pytest.approx(0.2)


def test_keeps_the_field_names_the_existing_template_uses(summary, tmp_path):
    """The template is the author's; adding zones must not rename what it already reads."""
    module.generate_report(_samples(), WINDOWS, BASELINE, 1234.5, tmp_path / "results.csv")
    assert {"samples", "duration_min", "baseline_w", "peak_w", "energy_j",
            "direction", "plot", "finished"} <= set(summary[0])


def test_peak_is_the_largest_excursion_inside_the_experiment(summary, tmp_path):
    module.generate_report(_samples(), WINDOWS, BASELINE, 0.0, tmp_path / "results.csv")
    assert summary[0]["peak_w"] == -30.0  # sign preserved, and the 19.3 W outside it ignored


def test_baseline_w_is_the_mean_of_the_selected_zone(summary, tmp_path):
    module.generate_report(_samples(), WINDOWS, BASELINE, 0.0, tmp_path / "results.csv")
    assert summary[0]["baseline_w"] == BASELINE["mean"]


def test_direction_follows_the_sign_of_the_energy(summary, tmp_path):
    module.generate_report(_samples(), WINDOWS, BASELINE, 10.0, tmp_path / "results.csv")
    module.generate_report(_samples(), WINDOWS, BASELINE, -10.0, tmp_path / "results.csv")
    assert [entry["direction"] for entry in summary] == ["added to", "removed from"]


def test_prints_both_zones_and_the_headline_energy(summary, tmp_path, capsys):
    module.generate_report(_samples(), WINDOWS, BASELINE, 1234.5, tmp_path / "results.csv")
    out = capsys.readouterr().out
    assert "Baseline zone 0.00-0.20 min" in out and "experiment zone 0.30-0.50 min" in out
    assert "1234.5 J (1.234 kJ added to the plate)" in out


def test_stays_quiet_about_a_report_that_failed_to_render(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(module, "compile_report", lambda summary, path: None)
    monkeypatch.setattr(module, "plot_work_curve", lambda samples, windows, path: path)
    module.generate_report(_samples(), WINDOWS, BASELINE, 0.0, tmp_path / "results.csv")
    assert "Report written" not in capsys.readouterr().out


def test_renders_a_real_pdf_end_to_end(tmp_path):
    module.generate_report(_samples(), WINDOWS, BASELINE, 1234.5, tmp_path / "results.csv")
    rendered = {path.suffix for path in tmp_path.iterdir() if path.is_file()}
    assert rendered == {".png", ".typ", ".json", ".pdf"}
