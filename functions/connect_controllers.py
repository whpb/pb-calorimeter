from pymodbus.client import ModbusTcpClient


def connect_controllers(settings):
    """Open a MODBUS TCP connection to every controller listed in settings."""
    clients = {}
    for name, address in settings["addresses"]["controllers"].items():
        host, port = address.split(":")
        client = ModbusTcpClient(host, port=int(port))
        if not client.connect():
            raise ConnectionError(f"Could not open a TCP connection to {name} at {address}")
        print(f"Connected to {name} at {address}")
        clients[name] = client
    return clients
