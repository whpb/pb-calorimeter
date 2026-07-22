from pymodbus.client.mixin import ModbusClientMixin

# nanodac registers are 32-bit floats over 2 words; flip to "little" here if a
# real device read comes back garbled.
WORD_ORDER = "big"


def read_register(clients, settings, category, name):
    controller, address = settings["addresses"]["modbus"][category][name]
    client = clients[controller]
    result = client.read_holding_registers(int(address), count=2)
    return client.convert_from_registers(
        result.registers, ModbusClientMixin.DATATYPE.FLOAT32, word_order=WORD_ORDER
    )
