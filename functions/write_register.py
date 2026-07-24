from functions.read_register import UNIT_ID


def write_register(clients, settings, category, name, value):
    """Write a single INT16 value to a named MODBUS register."""
    controller, address = settings["addresses"]["modbus"][category][name]
    client = clients[controller]
    result = client.write_register(int(address), value, device_id=UNIT_ID)
    if result.isError():
        raise RuntimeError(f"Write of {category} {name} ({controller} @ {address}) failed: {result}")
