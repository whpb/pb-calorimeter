import time

from functions.read_register import read_register
from functions.write_register import write_register
from functions.save_csv import save_csv

POLL_INTERVAL_S = 0.5


def test_cracking_pressure(clients, settings, save_path):
    """Poll each valve's upstream pressure until the monitored UserInput is reset to 0."""
    channels = list(settings["addresses"]["modbus"]["pressure"].keys())
    state = {name: {"peak": 0, "stall": 0} for name in channels}
    values = {}

    print("Cracking pressure test started. Reset User Value 1 to 0 to stop.")
    # write_register(clients, settings, "programmer", "SolenoidToggle", 1)
    try:
        while read_register(clients, settings, "programmer", "UserInput") == 1:
            for name in channels:
                values[name] = read_register(clients, settings, "pressure", name)
                print(f"{name} cracked at {values[name]}mbar")
            time.sleep(POLL_INTERVAL_S)
    finally:
        # always de-energize the solenoid, even if a read/write fails mid-test
        # write_register(clients, settings, "programmer", "SolenoidToggle", 0)
        temp = read_register(clients, settings, "programmer", "TempSensor")/100
        print(f"Temperature: {temp} °C")

    print("Stop signal received, saving results...")
    row = {"Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
    row.update({"Temperature": temp})
    row.update({name: values[name] for name in channels})
    save_csv(row, save_path)
