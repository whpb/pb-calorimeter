from functions.read_register import read_register


def keep_alive(clients, settings):
    """Read one register per controller to keep its MODBUS connection alive."""
    pending = set(settings["addresses"]["controllers"])
    for category, registers in settings["addresses"]["modbus"].items():
        for name, entry in registers.items():
            controller = entry[0]
            if controller in pending:
                read_register(clients, settings, category, name)
                pending.discard(controller)
        if not pending:
            break
