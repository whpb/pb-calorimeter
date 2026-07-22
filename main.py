import time

from functions.load_settings import load_settings
from functions.connect_controllers import connect_controllers
from functions.read_register import read_register
from functions.test_cracking_pressure import test_cracking_pressure

POLL_INTERVAL_S = 0.5
FUNCTIONS = {1: test_cracking_pressure}

settings = load_settings()
clients = connect_controllers(settings)

while True:
    value = read_register(clients, settings, "programmer", "UserInput")
    func = FUNCTIONS.get(int(value))
    if func:
        func(clients, settings)
    time.sleep(POLL_INTERVAL_S)
