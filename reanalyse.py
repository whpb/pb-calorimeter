import sys

from functions.analyse_samples import analyse_samples
from functions.choose_results_file import choose_results_file
from functions.load_samples import load_samples
from functions.load_settings import load_settings
from functions.next_sequential_name import next_sequential_name
from functions.start_console_log import start_console_log
from functions.stop_console_log import stop_console_log

print("Loading settings...")
settings = load_settings()

source = choose_results_file(sys.argv[1:], settings)
if source is None:
    print("No file chosen, nothing to do.")
    sys.exit()

# a new file every time, inside the run's own folder: the original run's results and
# report are never overwritten, and everything from that experiment stays together
folder = source.parent
target = folder / f"{next_sequential_name(folder, f'{source.stem} reanalysis')}.csv"
log_file = start_console_log(folder)

print(f"Re-analysing {source.name} into {target.name}")
samples = load_samples(source)
print(f"Loaded {len(samples)} samples; pick the zones in the window that opens.")
analyse_samples(samples, target, lambda: None)  # offline, so there is no rig to keep alive

stop_console_log(log_file)
