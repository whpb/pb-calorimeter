import time

from functions.calculate_heat_flow import calculate_heat_flow
from functions.read_register import read_register

BASELINE_PERIOD_S = 600.0


def measure_baseline(clients, settings, curve, time_step):
    """Average the unloaded plate over BASELINE_PERIOD_S, cancelling the ~90-120 s power swing."""
    print(f"Measuring baseline for {BASELINE_PERIOD_S / 60:.1f} min; leave the plate unloaded...")
    samples, deadline = [], time.monotonic() + BASELINE_PERIOD_S
    while True:
        try:
            samples.append(calculate_heat_flow(clients, settings, curve))
        except Exception as e:
            print(f"Baseline sample skipped: {e}")
        if time.monotonic() >= deadline:
            break
        if read_register(clients, settings, "programmer", "UserInput") != 1:
            print("Baseline cut short; UserInput left 1 before the period was up.")
            break
        time.sleep(time_step)
    if not samples:
        raise RuntimeError("No baseline samples were taken, so there is nothing to measure against")
    flows = [flow for _, _, flow in samples]
    # the spread is the swing the average is there to cancel; a wide one wants a longer period
    print(f"Averaged {len(samples)} samples, Q_abs spanning {max(flows) - min(flows):.2f} W")
    return tuple(sum(column) / len(samples) for column in zip(*samples))
