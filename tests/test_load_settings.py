from functions.load_settings import load_settings


def test_loads_the_repo_settings_file():
    loaded = load_settings()
    assert loaded["addresses"]["controllers"]
    assert loaded["SavePath"] and loaded["FileName"]
    assert isinstance(loaded["HeaterPower"], (int, float))


def test_every_register_names_a_known_controller():
    """The contract read_register relies on: entry[0] is always a connected controller."""
    loaded = load_settings()
    controllers = set(loaded["addresses"]["controllers"])
    for registers in loaded["addresses"]["modbus"].values():
        for name, entry in registers.items():
            assert entry[0] in controllers, name
            # None marks a channel whose address is not known yet, such as the master probe
            assert entry[1] is None or str(entry[1]).isdigit(), name


def test_defines_the_registers_the_calorimetry_run_needs():
    programmer = load_settings()["addresses"]["modbus"]["programmer"]
    assert {"UserInput", "PlateTemp", "HeaterUtil", "MasterTemp"} <= set(programmer)


def test_the_master_probe_is_configured():
    """It is read as FLOAT32 like the other pb1 channels - an assumption, not yet observed."""
    controller, address = load_settings()["addresses"]["modbus"]["programmer"]["MasterTemp"][:2]
    assert controller == "pb1" and str(address).isdigit()
