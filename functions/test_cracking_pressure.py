import time

from functions.read_register import read_register
from functions.save_csv import save_csv

POLL_INTERVAL_S = 0.5
CRACK_THRESHOLD = 0.1


def test_cracking_pressure(clients, settings):
    channels = list(settings["addresses"]["modbus"]["pressure"].keys())
    cracked = {}

    while read_register(clients, settings, "programmer", "UserInput") != 0:
        for name in channels:
            if name not in cracked:
                value = read_register(clients, settings, "pressure", name)
                if value > CRACK_THRESHOLD:
                    cracked[name] = value
        time.sleep(POLL_INTERVAL_S)

    row = {"Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
    row.update({name: cracked.get(name, "") for name in channels})
    save_csv(row, settings)
