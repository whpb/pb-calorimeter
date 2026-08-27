import pytest

from conftest import FakeClient, DATATYPE
from functions.read_register import read_register, UNIT_ID


def test_reads_int16_with_the_itools_unit_id(clients, settings):
    assert read_register(clients, settings, "programmer", "UserInput") == 1
    # device_id=255 is mandatory; without it the nanodac connects but never replies
    assert clients["pb1"].reads == [(14954, 1, UNIT_ID)]
    assert UNIT_ID == 255


def test_reads_float32_over_two_registers(clients, settings):
    assert read_register(clients, settings, "programmer", "PlateTemp", float=True) == pytest.approx(25.0)
    assert clients["pb1"].reads == [(33280, 2, UNIT_ID)]


def test_decodes_negative_int16(settings):
    clients = {"pb1": FakeClient({14954: (-12, DATATYPE.INT16)})}
    assert read_register(clients, settings, "programmer", "UserInput") == -12


def test_ignores_trailing_metadata_on_the_register_entry(clients, settings):
    settings["addresses"]["modbus"]["programmer"]["UserInput"] = ["pb1", "14954", 10, "-"]
    assert read_register(clients, settings, "programmer", "UserInput") == 1


def test_raises_on_a_modbus_error(settings):
    clients = {"pb1": FakeClient(error=True)}
    with pytest.raises(RuntimeError, match="Read of programmer HeaterUtil"):
        read_register(clients, settings, "programmer", "HeaterUtil")
