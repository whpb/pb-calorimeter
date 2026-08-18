import time

from functions.read_register import read_register
from functions.write_register import write_register
from functions.detect_crack import detect_crack
from functions.save_csv import save_csv

POLL_INTERVAL_S = 0.5


def test_cracking_pressure(clients, settings):
    """Poll each valve's upstream pressure and latch its peak once it stops rising (cracked), until the operator resets User Value 1."""
    channels = list(settings["addresses"]["modbus"]["pressure"].keys())
    state = {name: {"peak": 0, "stall": 0} for name in channels}
    cracked = {}

    print("Cracking pressure test started. Reset User Value 1 to 0 to stop.")
    #write_register(clients, settings, "programmer", "SolenoidToggle", 1)
    try:
        while read_register(clients, settings, "programmer", "UserInput") != 0:
            for name in channels:
                if name not in cracked:
                    value = read_register(clients, settings, "pressure", name)
                    if detect_crack(value, state[name]):
                        cracked[name] = state[name]["peak"]
                        print(f"{name} cracked at {cracked[name]}mbar")
            time.sleep(POLL_INTERVAL_S)
    finally:
        # always de-energize the solenoid, even if a read/write fails mid-test
        pass #write_register(clients, settings, "programmer", "SolenoidToggle", 0)

    print("Stop signal received, saving results...")
    row = {"Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
    row.update({"Temperature": read_register(clients, settings, "programmer", "TempSensor")})
    row.update({name: cracked.get(name, "") for name in channels})
    save_csv(row, settings)
