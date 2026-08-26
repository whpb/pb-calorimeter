import pytest

from conftest import FakeClient, DATATYPE
from functions.calculate_heat_flow import calculate_heat_flow


def _rig(temperature, utilisation):
    return {"pb1": FakeClient({33280: (temperature, DATATYPE.FLOAT32),
                               43874: (utilisation, DATATYPE.INT16)})}


def test_is_zero_when_the_plate_is_unloaded(settings, curve):
    """At equilibrium the heater output matches the sweep, so the net heat balance vanishes."""
    _, _, q_abs = calculate_heat_flow(_rig(25.0, 25), settings, curve)
    assert q_abs == pytest.approx(0.0)


def test_a_heat_source_shows_as_the_heater_backing_off(settings, curve):
    # 10 percentage points of the 193 W heater unused == 19.3 W arriving from the plate
    _, _, q_abs = calculate_heat_flow(_rig(25.0, 15), settings, curve)
    assert q_abs == pytest.approx(19.3)


def test_a_heat_sink_is_negative(settings, curve):
    _, _, q_abs = calculate_heat_flow(_rig(25.0, 35), settings, curve)
    assert q_abs == pytest.approx(-19.3)


def test_returns_the_raw_sample_alongside_the_heat_flow(settings, curve):
    temperature, utilisation, _ = calculate_heat_flow(_rig(12.5, 40), settings, curve)
    assert (temperature, utilisation) == (pytest.approx(12.5), 40)


def test_scales_with_the_configured_heater_power(settings, curve):
    settings["HeaterPower"] = 100
    _, _, q_abs = calculate_heat_flow(_rig(25.0, 15), settings, curve)
    assert q_abs == pytest.approx(10.0)


def test_reads_temperature_as_float32_and_utilisation_as_int16(settings, curve):
    clients = _rig(25.0, 25)
    calculate_heat_flow(clients, settings, curve)
    counts = {address: count for address, count, _ in clients["pb1"].reads}
    assert counts == {33280: 2, 43874: 1}


def test_propagates_a_modbus_fault(settings, curve):
    with pytest.raises(RuntimeError):
        calculate_heat_flow({"pb1": FakeClient(error=True)}, settings, curve)
