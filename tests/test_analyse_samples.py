import csv

import pytest

from functions import analyse_samples as module

WINDOWS = {"baseline": (0.0, 0.05), "experiment": (0.1, 0.2)}


def _samples(probe=None):
    return [{"Timestamp": "x", "Elapsed (min)": i / 60, "Plate temperature (C)": 25.0,
             "Master temperature (C)": None if probe is None else probe[i],
             "Heater utilisation (%)": 25.0, "Q_abs (W)": 2.0 + i} for i in range(13)]


@pytest.fixture
def chosen(monkeypatch):
    """Script the operator's drag, and record the keep-alive callback it was handed."""
    seen = {}
    def choose(samples, keep_alive_callback):
        seen["callback"] = keep_alive_callback
        return seen.get("windows", WINDOWS)
    monkeypatch.setattr(module, "select_windows", choose)
    return seen


def _rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def test_writes_the_results_file_and_the_report(chosen, tmp_path):
    module.analyse_samples(_samples(), tmp_path / "results.csv", lambda: None)
    assert {p.suffix for p in tmp_path.iterdir() if p.is_file()} == {".csv", ".png", ".typ",
                                                                     ".json", ".pdf"}


def test_derives_the_columns_from_the_chosen_baseline(chosen, tmp_path):
    """Q_abs runs 2, 3, 4...; a baseline over the first four averages 3.5 W."""
    module.analyse_samples(_samples(), tmp_path / "results.csv", lambda: None)
    rows = _rows(tmp_path / "results.csv")
    assert float(rows[0]["Q_relative (W)"]) == pytest.approx(-1.5)
    assert rows[0]["Zone"] == "baseline"


def test_a_different_baseline_zone_shifts_every_sample(chosen, tmp_path):
    """The whole point of re-analysis: same data, re-cut baseline, different Q_relative."""
    module.analyse_samples(_samples(), tmp_path / "first.csv", lambda: None)
    chosen["windows"] = {"baseline": (0.15, 0.2), "experiment": (0.0, 0.05)}
    module.analyse_samples(_samples(), tmp_path / "second.csv", lambda: None)
    first = float(_rows(tmp_path / "first.csv")[0]["Q_relative (W)"])
    second = float(_rows(tmp_path / "second.csv")[0]["Q_relative (W)"])
    assert first != second


def test_hands_the_selector_the_keep_alive_callback(chosen, tmp_path):
    """Live runs pass keep_alive; re-analysis passes a no-op, and the selector cannot tell."""
    def pump():
        return "beat"
    module.analyse_samples(_samples(), tmp_path / "results.csv", pump)
    assert chosen["callback"] is pump


def test_uses_the_probe_baseline_when_the_probe_reported(chosen, tmp_path):
    module.analyse_samples(_samples(probe=[5.0] * 13), tmp_path / "results.csv", lambda: None)
    changes = [row["Master temperature change (C)"] for row in _rows(tmp_path / "results.csv")]
    assert changes == ["0.0"] * 13


def test_leaves_the_probe_column_blank_when_it_never_reported(chosen, tmp_path):
    module.analyse_samples(_samples(), tmp_path / "results.csv", lambda: None)
    changes = {row["Master temperature change (C)"] for row in _rows(tmp_path / "results.csv")}
    assert changes == {""}


def test_prints_the_baseline_it_settled_on(chosen, tmp_path, capsys):
    module.analyse_samples(_samples(), tmp_path / "results.csv", lambda: None)
    assert "Baseline: 25.00 C plate, Q_abs = 3.50 W" in capsys.readouterr().out
