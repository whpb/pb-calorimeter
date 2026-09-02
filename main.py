import time

from functions.load_settings import load_settings
from functions.measure_calorimetry import measure_calorimetry
from functions.connect_controllers import connect_controllers
from functions.close_controllers import close_controllers
from functions.keep_alive import keep_alive
from functions.read_register import read_register
from functions.resolve_results_root import resolve_results_root
from functions.resolve_save_path import resolve_save_path
from functions.start_console_log import start_console_log
from functions.stop_console_log import stop_console_log

POLL_INTERVAL_S = 0.2
FUNCTIONS = {1: measure_calorimetry}

print("Loading settings...")
settings = load_settings()

# one log for the whole session, in the results root: a session holds many runs,
# and each of those gets its own folder below
log_file = start_console_log(resolve_results_root(settings))

print("Connecting to controllers...")
clients = connect_controllers(settings)

print("Starting loop...")

while True:
    try:
        value = read_register(clients, settings, "programmer", "UserInput")
        # print(f"Reading UserValue as {value}")
        if value == 2:
            print("Stop signal (UserInput=2) received, terminating.")
            break
        func = FUNCTIONS.get(value)
        if func:
            print(f"User Value 1 = {value}, running function {value}...")
            # resolved per call, so a later run never lands on an earlier one's results
            func(clients, settings, resolve_save_path(settings))
            print("Function finished, resuming polling.")
        else:
            keep_alive(clients, settings)
    except Exception as e:
        # catches MODBUS faults without abandoning the loop
        print(f"Poll cycle error, continuing: {e}")
    time.sleep(POLL_INTERVAL_S)

close_controllers(clients)
stop_console_log(log_file)
