import csv

import pytest

from conftest import ScriptedClient
from functions import measure_calorimetry as module

SETTINGS = {"addresses": {"controllers": {"pb1": "x:502"}, "modbus": {"programmer": {
    "UserInput": ["pb1", str(ScriptedClient.USER_INPUT)],
    "PlateTemp": ["pb1", str(ScriptedClient.PLATE_TEMP)],
    "HeaterUtil": ["pb1", str(ScriptedClient.HEATER_UTIL)],
    "MasterTemp": ["pb1", None]}}}, "HeaterPower": 193}


@pytest.fixture
def rig(monkeypatch, curve, clock):
    """Run instantly, on the simple 1 C per % curve, with the operator's choices scripted."""
    monkeypatch.setattr(module, "load_cooling_curve", lambda: curve)
    chosen = {}

    def choose(samples, keep_alive_callback):
        keep_alive_callback()  # the pump the real window runs on a timer
        last = samples[-1]["Elapsed (min)"]
        return chosen.get("windows", {"baseline": (0.0, last / 2), "experiment": (last / 2, last)})

    monkeypatch.setattr(module, "select_windows", choose)
    return chosen


def _run(samples, tmp_path):
    clients = {"pb1": ScriptedClient(samples)}
    module.measure_calorimetry(clients, SETTINGS, tmp_path / "results.csv")
    return clients["pb1"]


def _rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def test_an_unloaded_run_integrates_to_nothing(rig, tmp_path):
    _run([(25.0, 25)] * 6, tmp_path)
    assert float(_rows(tmp_path / "results.csv")[-1]["Energy (J)"]) == pytest.approx(0.0)


def test_recovers_a_steady_source_as_energy(rig, tmp_path):
    """Samples land at 1..6 s; baseline over the unloaded pair, experiment over the loaded run."""
    rig["windows"] = {"baseline": (0.0, 2 / 60), "experiment": (3 / 60, 6 / 60)}
    _run([(25.0, 25)] * 3 + [(25.0, 15)] * 3, tmp_path)
    # the zone opens on a still-unloaded sample, then three 1 s steps at 19.3 W
    assert float(_rows(tmp_path / "results.csv")[-1]["Energy (J)"]) == pytest.approx(57.9)


def test_the_baseline_comes_from_the_zone_the_operator_picked(rig, tmp_path):
    """A drifted machine offsets every sample equally; the chosen zone cancels it."""
    rig["windows"] = {"baseline": (0.0, 2 / 60), "experiment": (3 / 60, 5 / 60)}
    _run([(25.0, 21)] * 3 + [(25.0, 11)] * 3, tmp_path)
    rows = _rows(tmp_path / "results.csv")
    assert float(rows[0]["Q_abs (W)"]) == pytest.approx(7.72)  # 7.72 W of drift in the raw signal
    assert float(rows[0]["Q_relative (W)"]) == pytest.approx(0.0)
    assert float(rows[-1]["Q_relative (W)"]) == pytest.approx(19.3)


def test_the_results_file_ends_up_with_one_row_per_sample(rig, tmp_path):
    _run([(25.0, 25)] * 6, tmp_path)
    assert len(_rows(tmp_path / "results.csv")) == 6


def test_the_rewritten_file_carries_the_derived_columns(rig, tmp_path):
    _run([(25.0, 25)] * 6, tmp_path)
    assert list(_rows(tmp_path / "results.csv")[0]) == [
        "Timestamp", "Elapsed (min)", "Plate temperature (C)", "Master temperature (C)",
        "Heater utilisation (%)", "Q_abs (W)", "Q_relative (W)",
        "Plate temperature change (C)", "Energy (J)", "Zone"]


def test_every_sample_is_labelled_with_its_zone(rig, tmp_path):
    rig["windows"] = {"baseline": (0.0, 2 / 60), "experiment": (3 / 60, 6 / 60)}
    _run([(25.0, 25)] * 6, tmp_path)
    zones = [row["Zone"] for row in _rows(tmp_path / "results.csv")]
    assert zones == ["baseline", "baseline"] + ["experiment"] * 4


def test_reports_and_plots_at_the_end(rig, tmp_path):
    _run([(25.0, 25)] * 6, tmp_path)
    assert (tmp_path / "results.pdf").exists() and (tmp_path / "results.png").exists()


def test_prints_the_baseline_the_operator_chose(rig, tmp_path, capsys):
    _run([(25.0, 25)] * 6, tmp_path)
    assert "Baseline: 25.00 C plate" in capsys.readouterr().out


def test_a_run_with_no_samples_stops_before_the_selector(rig, tmp_path, capsys):
    clients = {"pb1": ScriptedClient([(25.0, 25)], user_input=lambda: 0)}
    module.measure_calorimetry(clients, SETTINGS, tmp_path / "results.csv")
    assert "nothing to analyse" in capsys.readouterr().out
    assert not (tmp_path / "results.csv").exists()


def test_a_faulty_sample_never_reaches_the_results(rig, tmp_path):
    _run([(25.0, 25), None] + [(25.0, 25)] * 4, tmp_path)
    assert len(_rows(tmp_path / "results.csv")) == 5
