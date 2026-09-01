import csv

import pytest

from conftest import ScriptedClient
from functions import record_samples as module


def _settings(master_address=None):
    return {"addresses": {"controllers": {"pb1": "x:502"}, "modbus": {"programmer": {
        "UserInput": ["pb1", str(ScriptedClient.USER_INPUT)],
        "PlateTemp": ["pb1", str(ScriptedClient.PLATE_TEMP)],
        "HeaterUtil": ["pb1", str(ScriptedClient.HEATER_UTIL)],
        "MasterTemp": ["pb1", master_address]}}}, "HeaterPower": 193}


def _run(samples, curve, tmp_path, master_address=None, user_input=None):
    clients = {"pb1": ScriptedClient(samples, user_input=user_input)}
    return module.record_samples(clients, _settings(master_address), curve, tmp_path / "results.csv")


def _rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def test_records_one_row_per_sample(clock, curve, tmp_path):
    samples = _run([(25.0, 25), (25.0, 15), (25.0, 20)], curve, tmp_path)
    assert len(samples) == 3  # every reading is a row now; nothing is spent on baselining
    assert len(_rows(tmp_path / "results.csv")) == 3


def test_writes_each_row_as_it_lands(clock, curve, tmp_path):
    """Appending live is what makes a killed run keep everything it had already sampled."""
    _run([(25.0, 25)] * 4, curve, tmp_path)
    assert list(_rows(tmp_path / "results.csv")[0]) == [
        "Timestamp", "Elapsed (min)", "Plate temperature (C)", "Master temperature (C)",
        "Heater utilisation (%)", "Q_abs (W)"]


def test_holds_no_derived_columns_yet(clock, curve, tmp_path):
    """Q_relative and Energy need a baseline, which does not exist until the operator picks one."""
    samples = _run([(25.0, 25), (25.0, 15)], curve, tmp_path)
    assert "Q_relative (W)" not in samples[0] and "Energy (J)" not in samples[0]


def test_elapsed_starts_at_the_first_sample(clock, curve, tmp_path):
    clock.now = 900.0
    samples = _run([(25.0, 25), (25.0, 15)], curve, tmp_path)
    assert samples[0]["Elapsed (min)"] == pytest.approx(1 / 60, abs=1e-3)


def test_computes_net_power_from_the_curve(clock, curve, tmp_path):
    samples = _run([(25.0, 15), (25.0, 25)], curve, tmp_path)
    # the curve wants 25 % at 25 C; the heater using only 15 % means 19.3 W is arriving
    assert samples[0]["Q_abs (W)"] == pytest.approx(19.3)
    assert samples[1]["Q_abs (W)"] == pytest.approx(0.0)


def test_leaves_the_probe_blank_until_it_is_configured(clock, curve, tmp_path):
    samples = _run([(25.0, 25), (25.0, 15)], curve, tmp_path)
    assert samples[0]["Master temperature (C)"] is None
    assert _rows(tmp_path / "results.csv")[0]["Master temperature (C)"] == ""


def test_records_the_probe_once_it_has_an_address(clock, curve, tmp_path):
    samples = _run([(25.0, 25, 5.0), (25.0, 15, 6.5)], curve, tmp_path,
                   master_address=str(ScriptedClient.MASTER_TEMP))
    assert [row["Master temperature (C)"] for row in samples] == [pytest.approx(5.0),
                                                                  pytest.approx(6.5)]


def test_a_faulty_sample_is_skipped_not_fatal(clock, curve, tmp_path, capsys):
    samples = _run([(25.0, 25), None, (25.0, 15)], curve, tmp_path)
    assert "Sample skipped" in capsys.readouterr().out
    assert len(samples) == 2


def test_returns_nothing_if_the_trigger_clears_immediately(clock, curve, tmp_path):
    assert _run([(25.0, 25)], curve, tmp_path, user_input=lambda: 0) == []
    assert not (tmp_path / "results.csv").exists()
