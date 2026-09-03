from functions.load_settings import load_settings


def test_loads_the_seeded_settings_file(docs_home):
    """Seeded into the operator's docs folder on first run, and read from there."""
    loaded = load_settings()
    assert loaded["addresses"]["controllers"]
    assert loaded["SavePath"] and loaded["FileName"]
    assert isinstance(loaded["HeaterPower"], (int, float))


def test_every_register_names_a_known_controller(docs_home):
    """The contract read_register relies on: entry[0] is always a connected controller."""
    loaded = load_settings()
    controllers = set(loaded["addresses"]["controllers"])
    for registers in loaded["addresses"]["modbus"].values():
        for name, entry in registers.items():
            assert entry[0] in controllers, name
            # None marks a channel whose address is not known yet, such as the master probe
            assert entry[1] is None or str(entry[1]).isdigit(), name


def test_defines_the_registers_the_calorimetry_run_needs(docs_home):
    programmer = load_settings()["addresses"]["modbus"]["programmer"]
    assert {"UserInput", "PlateTemp", "HeaterUtil", "MasterTemp"} <= set(programmer)


def test_the_master_probe_is_configured(docs_home):
    """Confirmed reading correctly on the rig; the shipped default must carry it."""
    controller, address = load_settings()["addresses"]["modbus"]["programmer"]["MasterTemp"][:2]
    assert controller == "pb1" and str(address).isdigit()


def test_the_operator_can_change_a_setting(docs_home):
    """The whole point of the docs folder: an edit there is what the program then reads."""
    from functions.resolve_docs_folder import resolve_docs_folder

    path = resolve_docs_folder() / "settings.json"
    path.write_text(path.read_text().replace('"HeaterPower": 193', '"HeaterPower": 250'))
    assert load_settings()["HeaterPower"] == 250
