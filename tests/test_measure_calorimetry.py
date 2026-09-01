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
    """Run instantly, on the simple 1 C per % curve."""
    monkeypatch.setattr(module, "load_cooling_curve", lambda: curve)


def _run(samples, tmp_path):
    clients = {"pb1": ScriptedClient(samples)}
    module.measure_calorimetry(clients, SETTINGS, tmp_path / "results.csv")
    return clients["pb1"]


def _rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def test_records_every_sample(rig, tmp_path):
    _run([(25.0, 25)] * 6, tmp_path)
    assert len(_rows(tmp_path / "results.csv")) == 6


def test_stops_when_user_value_one_clears(rig, tmp_path):
    """Unattended mode still ends where it always did: at the nanodac."""
    client = _run([(25.0, 25)] * 3, tmp_path)
    assert len(_rows(tmp_path / "results.csv")) == 3
    assert any(address == ScriptedClient.USER_INPUT for address, _, _ in client.reads)


def test_writes_the_raw_columns_only(rig, tmp_path):
    """The derived columns need a baseline, and nobody is here to draw one."""
    _run([(25.0, 25)] * 4, tmp_path)
    assert list(_rows(tmp_path / "results.csv")[0]) == [
        "Timestamp", "Elapsed (min)", "Plate temperature (C)", "Master temperature (C)",
        "Heater utilisation (%)", "Q_abs (W)"]


def test_produces_no_report_and_no_window(rig, tmp_path):
    """A blocking selection window would hang the rig until somebody came back to it."""
    _run([(25.0, 25)] * 4, tmp_path)
    assert [path.name for path in tmp_path.iterdir()] == ["results.csv"]


def test_computes_net_power_while_recording(rig, tmp_path):
    """Q_abs needs no baseline, so it is still worth having in the file."""
    _run([(25.0, 15)] * 3, tmp_path)
    assert float(_rows(tmp_path / "results.csv")[0]["Q_abs (W)"]) == pytest.approx(19.3)


def test_points_the_operator_at_re_analysis(rig, tmp_path, capsys):
    _run([(25.0, 25)] * 4, tmp_path)
    out = capsys.readouterr().out
    assert "Recorded 4 samples to results.csv" in out and "Re-analyse" in out


def test_a_run_with_no_samples_says_so(rig, tmp_path, capsys):
    clients = {"pb1": ScriptedClient([(25.0, 25)], user_input=lambda: 0)}
    module.measure_calorimetry(clients, SETTINGS, tmp_path / "results.csv")
    assert "No samples recorded" in capsys.readouterr().out
    assert not (tmp_path / "results.csv").exists()


def test_a_faulty_sample_never_reaches_the_results(rig, tmp_path):
    _run([(25.0, 25), None] + [(25.0, 25)] * 4, tmp_path)
    assert len(_rows(tmp_path / "results.csv")) == 5
