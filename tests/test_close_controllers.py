from conftest import FakeClient
from functions.close_controllers import close_controllers


def test_closes_every_client(capsys):
    clients = {"pb1": FakeClient(), "pb2": FakeClient()}
    close_controllers(clients)
    assert all(client.closed for client in clients.values())
    assert "Closed connection to pb1" in capsys.readouterr().out


def test_accepts_an_empty_client_map():
    close_controllers({})
