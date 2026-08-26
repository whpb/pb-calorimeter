import csv
import time

import pytest

from conftest import FakeClient, FakeResult, DATATYPE
from functions import measure_calorimetry as module
from pymodbus.client.mixin import ModbusClientMixin

USER_INPUT, PLATE_TEMP, HEATER_UTIL = 14954, 33280, 43874


class ScriptedClient(FakeClient):
    """Replays a list of (plate C, heater %) samples; None stages a MODBUS fault."""

    def __init__(self, samples):
        super().__init__()
        self.samples, self.index, self.current = samples, 0, None

    def read_holding_registers(self, address, count=1, device_id=None):
        self.reads.append((address, count, device_id))
        if address == USER_INPUT:  # the run ends once the script is exhausted
            return self._encode(1 if self.index < len(self.samples) else 0, DATATYPE.INT16)
        if address == PLATE_TEMP:
            self.current, self.index = self.samples[self.index], self.index + 1
            return FakeResult(error=True) if self.current is None else self._encode(
                self.current[0], DATATYPE.FLOAT32)
        return FakeResult(error=True) if self.current is None else self._encode(
            self.current[1], DATATYPE.INT16)

    @staticmethod
    def _encode(value, datatype):
        return FakeResult(ModbusClientMixin.convert_to_registers(value, datatype))


class Clock:
    """A fake clock that only sleep advances, so a skipped sample still costs its second."""

    def __init__(self):
        self.now = 0.0

    def sleep(self, seconds):
        self.now += seconds

    def monotonic(self):
        return self.now


@pytest.fixture
def rig(monkeypatch, curve):
    """Run instantly on the fake clock, against the simple 1 C per % curve."""
    clock = Clock()
    monkeypatch.setattr(module, "load_cooling_curve", lambda: curve)
    monkeypatch.setattr(time, "sleep", clock.sleep)
    monkeypatch.setattr(time, "monotonic", clock.monotonic)
    return clock


def _run(samples, tmp_path):
    clients = {"pb1": ScriptedClient(samples)}
    module.measure_calorimetry(clients, _settings(), tmp_path / "results.csv", 0.0)
    return clients["pb1"]


def _settings():
    return {
        "addresses": {"controllers": {"pb1": "x:502"},
                      "modbus": {"programmer": {"UserInput": ["pb1", str(USER_INPUT)],
                                                "PlateTemp": ["pb1", str(PLATE_TEMP)],
                                                "HeaterUtil": ["pb1", str(HEATER_UTIL)]}}},
        "HeaterPower": 193,
    }


def _rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def test_an_unloaded_run_integrates_to_nothing(rig, tmp_path):
    _run([(25.0, 25)] * 4, tmp_path)
    assert float(_rows(tmp_path / "results.csv")[-1]["Energy (J)"]) == pytest.approx(0.0)


def test_recovers_a_steady_source_as_energy(rig, tmp_path):
    # baseline then three 1 s samples with the heater 10 points down: 3 x 19.3 W x 1 s
    _run([(25.0, 25)] + [(25.0, 15)] * 3, tmp_path)
    rows = _rows(tmp_path / "results.csv")
    assert [float(row["Q_relative (W)"]) for row in rows] == [pytest.approx(19.3)] * 3
    assert float(rows[-1]["Energy (J)"]) == pytest.approx(57.9)


def test_baseline_offset_is_subtracted_out(rig, tmp_path):
    """A stale curve shifts every sample equally, so Q_relative still reads the source."""
    _run([(25.0, 21)] + [(25.0, 11)] * 2, tmp_path)
    rows = _rows(tmp_path / "results.csv")
    assert float(rows[0]["Q_abs (W)"]) == pytest.approx(27.02)  # 7.72 W of drift included
    assert float(rows[0]["Q_relative (W)"]) == pytest.approx(19.3)


def test_a_faulty_sample_is_skipped_without_losing_the_run(rig, tmp_path, capsys):
    _run([(25.0, 25), (25.0, 15), None, (25.0, 15)], tmp_path)
    rows = _rows(tmp_path / "results.csv")
    assert "Sample skipped" in capsys.readouterr().out
    assert len(rows) == 2  # the fault produced no row...
    # ...and the next step spans the whole gap, so its second is not lost from the integral
    assert float(rows[-1]["Energy (J)"]) == pytest.approx(19.3 * 3)


def test_logs_every_sample_with_its_units(rig, tmp_path):
    _run([(25.0, 25), (24.0, 15)], tmp_path)
    row = _rows(tmp_path / "results.csv")[0]
    assert list(row) == ["Timestamp", "Elapsed (min)", "Plate temperature (C)",
                         "Heater utilisation (%)", "Q_abs (W)", "Q_relative (W)", "Energy (J)"]
    assert float(row["Plate temperature (C)"]) == pytest.approx(24.0)


def test_records_temperature_change_from_baseline_for_the_plot(rig, tmp_path, monkeypatch):
    captured = []
    monkeypatch.setattr(module, "generate_report",
                        lambda history, *args: captured.append(history))
    _run([(25.0, 25), (24.0, 15), (22.5, 15)], tmp_path)
    assert [round(row[2], 2) for row in captured[0]] == [-1.0, -2.5]


def test_reports_and_plots_at_the_end(rig, tmp_path):
    _run([(25.0, 25), (25.0, 15)], tmp_path)
    assert (tmp_path / "results.pdf").exists() and (tmp_path / "results.png").exists()


def test_stops_as_soon_as_userinput_leaves_one(rig, tmp_path, capsys):
    client = _run([(25.0, 25)], tmp_path)
    assert not (tmp_path / "results.csv").exists()
    assert "No samples recorded" in capsys.readouterr().out
    assert client.reads.count((USER_INPUT, 1, 255)) == 1
