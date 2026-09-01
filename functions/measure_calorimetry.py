from functions.analyse_samples import analyse_samples
from functions.keep_alive import keep_alive
from functions.load_cooling_curve import load_cooling_curve
from functions.record_samples import record_samples


def measure_calorimetry(clients, settings, save_path):
    """Record a run, have the operator pick its baseline and experiment zones, then report."""
    curve = load_cooling_curve()
    samples = record_samples(clients, settings, curve, save_path)
    if not samples:
        print("No samples recorded, nothing to analyse.")
        return
    # the rig drops idle sockets, so the selection window has to keep the connection warm
    analyse_samples(samples, save_path, lambda: keep_alive(clients, settings))
