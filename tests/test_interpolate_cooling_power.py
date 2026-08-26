import pytest

from functions.interpolate_cooling_power import interpolate_cooling_power
from functions.load_cooling_curve import load_cooling_curve


def test_is_exact_at_every_knot(curve):
    temps, outputs = curve
    for temperature, output in zip(temps, outputs):
        assert interpolate_cooling_power(temperature, curve, 100) == pytest.approx(output)


def test_round_trips_the_real_curve_at_its_own_points():
    curve = load_cooling_curve()
    for temperature, output in zip(*curve):
        assert interpolate_cooling_power(temperature, curve, 193) == pytest.approx(193 * output / 100)


def test_interpolates_linearly_between_knots(curve):
    assert interpolate_cooling_power(15.0, curve, 100) == pytest.approx(15.0)
    assert interpolate_cooling_power(12.5, curve, 100) == pytest.approx(12.5)


def test_clamps_outside_the_measured_range(curve):
    assert interpolate_cooling_power(-40.0, curve, 100) == pytest.approx(0.0)
    assert interpolate_cooling_power(99.0, curve, 100) == pytest.approx(30.0)


def test_scales_the_output_percentage_by_heater_power(curve):
    # each sweep point is an equilibrium, so output % of HeaterPower is the cooling power
    assert interpolate_cooling_power(10.0, curve, 193) == pytest.approx(19.3)


def test_tolerates_repeated_temperatures(curve):
    duplicated = ([0.0, 10.0, 10.0, 20.0], [0.0, 10.0, 20.0, 30.0])
    assert 0.0 <= interpolate_cooling_power(10.0, duplicated, 100) <= 20.0
