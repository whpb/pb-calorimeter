from pymodbus.client.mixin import ModbusClientMixin

# matches the unit ID iTools uses to talk to the nanodacs directly (not a gateway setup)
UNIT_ID = 255


def read_register(clients, settings, category, name, float=False, verbose=False):
    """Read a named MODBUS register and return its decoded INT16 value."""
    controller, address = settings["addresses"]["modbus"][category][name][:2]
    client = clients[controller]
    if verbose:
        print(f"Reading {category} {name} from {controller} @ {address}")
    result = client.read_holding_registers(int(address), count=(2 if float else 1), device_id=UNIT_ID)
    if result.isError():
        raise RuntimeError(f"Read of {category} {name} ({controller} @ {address}) failed: {result}")
    return client.convert_from_registers(result.registers, ModbusClientMixin.DATATYPE.FLOAT32 if float else ModbusClientMixin.DATATYPE.INT16)
