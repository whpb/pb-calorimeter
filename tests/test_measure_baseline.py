import math

import pytest

from conftest import ScriptedClient
from functions import measure_baseline as module

SETTINGS = {"addresses": {"modbus": {"programmer": {
    "UserInput": ["pb1", "14954"], "PlateTemp": ["pb1", "33280"], "HeaterUtil": ["pb1", "43874"]}}},
    "HeaterPower": 193}

# util swings +/-5 points about 25 with a 12 sample period; 120 samples is exactly ten cycles
OSCILLATION = [(25.0, 25 + round(5 * math.sin(2 * math.pi * i / 12))) for i in range(120)]


@pytest.fixture
def period(monkeypatch):
    """119 s at a 1 s step is 120 samples - ten whole periods of the fixture's swing."""
    monkeypatch.setattr(module, "BASELINE_PERIOD_S", 119.0)


def _run(samples, curve, user_input=None):
    client = ScriptedClient(samples, user_input=user_input)
    return module.measure_baseline({"pb1": client}, SETTINGS, curve, 1.0), client


def test_averages_the_swing_away(period, clock, curve):
    """A single reading lands anywhere in the swing; the mean of whole cycles does not."""
    (_, _, baseline), _ = _run(OSCILLATION, curve)
    assert baseline == pytest.approx(0.0, abs=1e-9)


def test_a_lone_sample_would_have_been_badly_wrong(period, clock, curve):
    peak_first = OSCILLATION[3:] + OSCILLATION[:3]  # start the run at the top of the swing
    (_, _, baseline), _ = _run(peak_first, curve)
    assert abs(baseline) < 0.01  # against roughly 9.65 W had the first reading been taken alone


def test_samples_for_the_whole_period(period, clock, curve):
    _run(OSCILLATION, curve)
    assert clock.now == pytest.approx(119.0)


def test_averages_temperature_and_utilisation_too(period, clock, curve):
    samples = [(20.0, 10), (30.0, 20)] * 60
    (temperature, utilisation, _), _ = _run(samples, curve)
    assert (temperature, utilisation) == (pytest.approx(25.0), pytest.approx(15.0))


def test_stops_early_when_userinput_leaves_one(period, clock, curve):
    (_, _, _), client = _run(OSCILLATION, curve, user_input=lambda: 1 if clock.now < 5 else 0)
    assert clock.now == pytest.approx(5.0) and client.index == 6


def test_says_why_it_stopped_early(period, clock, curve, capsys):
    _run(OSCILLATION, curve, user_input=lambda: 0)
    assert "Baseline cut short" in capsys.readouterr().out


def test_skips_a_faulty_sample_and_averages_the_rest(period, clock, curve, capsys):
    (_, _, baseline), _ = _run([None] + OSCILLATION[:11] * 10, curve)
    assert "Baseline sample skipped" in capsys.readouterr().out
    assert baseline == pytest.approx(sum(193 * (25 - u) / 100 for _, u in OSCILLATION[:11]) / 11)


def test_raises_when_every_sample_failed(period, clock, curve):
    with pytest.raises(RuntimeError, match="nothing to measure against"):
        _run([None], curve, user_input=lambda: 0)


def test_reports_the_spread_it_cancelled(period, clock, curve, capsys):
    _run(OSCILLATION, curve, user_input=lambda: 0)
    # one sample only, so the swing it reports is zero - the wording still has to be there
    assert "Averaged 1 samples, Q_abs spanning 0.00 W" in capsys.readouterr().out


def test_warns_the_operator_before_the_wait(period, clock, curve, capsys):
    _run(OSCILLATION, curve, user_input=lambda: 0)
    assert "leave the plate unloaded" in capsys.readouterr().out
