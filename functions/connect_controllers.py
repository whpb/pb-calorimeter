from pymodbus.client import ModbusTcpClient


def connect_controllers(settings):
    clients = {}
    for name, address in settings["addresses"]["controllers"].items():
        host, port = address.split(":")
        client = ModbusTcpClient(host, port=int(port))
        client.connect()
        clients[name] = client
    return clients
