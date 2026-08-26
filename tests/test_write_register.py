import pytest

from conftest import FakeClient
from functions.write_register import write_register
from functions.read_register import UNIT_ID


def test_writes_with_the_itools_unit_id(clients, settings):
    write_register(clients, settings, "programmer", "UserInput", 2)
    assert clients["pb1"].writes == [(14954, 2, UNIT_ID)]


def test_ignores_trailing_metadata_on_the_register_entry(clients, settings):
    settings["addresses"]["modbus"]["programmer"]["UserInput"] = ["pb1", "14954", 1, "-"]
    write_register(clients, settings, "programmer", "UserInput", 1)
    assert clients["pb1"].writes == [(14954, 1, UNIT_ID)]


def test_raises_on_a_modbus_error(settings):
    clients = {"pb1": FakeClient(error=True)}
    with pytest.raises(RuntimeError, match="Write of programmer UserInput"):
        write_register(clients, settings, "programmer", "UserInput", 1)
