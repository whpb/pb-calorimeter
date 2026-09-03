import sys
from pathlib import Path

import matplotlib

# before pyplot is imported: with no interactive backend matplotlib falls back
# to Agg in silence, plt.show() returns at once and the operator never sees the
# selection window - leaving a report built on zones nobody chose
matplotlib.use("TkAgg")

from functions.analyse_samples import analyse_samples
from functions.close_controllers import close_controllers
from functions.connect_controllers import connect_controllers
from functions.keep_alive import keep_alive
from functions.load_cooling_curve import load_cooling_curve
from functions.load_settings import load_settings
from functions.record_samples import record_samples
from functions.resolve_save_path import resolve_save_path
from functions.start_console_log import start_console_log
from functions.stop_console_log import stop_console_log
from functions.stop_requested import stop_requested

if len(sys.argv) < 2:
    sys.exit("force_run.py needs the path of the stop file the interface will create")
sentinel = Path(sys.argv[1])
sentinel.unlink(missing_ok=True)  # a stale stop must not end this run before it starts
name = sys.argv[2] if len(sys.argv) > 2 else ""  # blank falls back to the FileName pattern

print("Loading settings...")
settings = load_settings()
save_path = resolve_save_path(settings, name)
print(f"Recording to {save_path.parent}")
log_file = start_console_log(save_path.parent)

print("Connecting to controllers...")
clients = connect_controllers(settings)
curve = load_cooling_curve()

# User Value 1 is not consulted at all here; the interface owns the start and the stop
print("Recording. Press 'Stop and analyse' in the interface to finish.")
samples = record_samples(clients, settings, curve, save_path, lambda: not stop_requested(sentinel))
if samples:
    analyse_samples(samples, save_path, lambda: keep_alive(clients, settings))
else:
    print("No samples recorded, nothing to analyse.")

close_controllers(clients)
stop_console_log(log_file)
