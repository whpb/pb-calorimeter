from conftest import FakeClient, DATATYPE
from functions.keep_alive import keep_alive
from functions.read_register import UNIT_ID


def test_reads_exactly_one_register_per_controller(clients, settings):
    keep_alive(clients, settings)
    # three registers are defined on pb1, but one read is enough to hold the socket open
    assert clients["pb1"].reads == [(14954, 1, UNIT_ID)]


def test_covers_every_controller(settings):
    settings["addresses"]["controllers"]["pb2"] = "10.0.0.5:503"
    settings["addresses"]["modbus"]["programmer"]["Spare"] = ["pb2", "100"]
    clients = {"pb1": FakeClient({14954: (1, DATATYPE.INT16)}), "pb2": FakeClient()}
    keep_alive(clients, settings)
    assert len(clients["pb1"].reads) == 1
    assert len(clients["pb2"].reads) == 1
