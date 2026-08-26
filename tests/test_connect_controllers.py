import pytest

from conftest import FakeClient
from functions import connect_controllers as module


def _patch(monkeypatch, error=False):
    """Swap ModbusTcpClient for a recorder, and return the list of constructor calls."""
    calls = []

    def factory(host, port):
        calls.append((host, port))
        return FakeClient(error=error)

    monkeypatch.setattr(module, "ModbusTcpClient", factory)
    return calls


def test_opens_one_client_per_controller(monkeypatch, settings):
    calls = _patch(monkeypatch)
    clients = module.connect_controllers(settings)
    assert list(clients) == ["pb1"]
    assert calls == [("192.168.111.222", 502)]  # port split off the address and cast to int


def test_supports_several_controllers(monkeypatch, settings):
    settings["addresses"]["controllers"]["pb2"] = "10.0.0.5:503"
    _patch(monkeypatch)
    assert list(module.connect_controllers(settings)) == ["pb1", "pb2"]


def test_raises_when_a_controller_is_unreachable(monkeypatch, settings):
    _patch(monkeypatch, error=True)
    with pytest.raises(ConnectionError, match="pb1"):
        module.connect_controllers(settings)
