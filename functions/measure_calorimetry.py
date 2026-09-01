from functions.check_baseline import check_baseline
from functions.generate_report import generate_report
from functions.integrate_energy import integrate_energy
from functions.keep_alive import keep_alive
from functions.load_cooling_curve import load_cooling_curve
from functions.record_samples import record_samples
from functions.rewrite_csv import rewrite_csv
from functions.select_windows import select_windows
from functions.summarise_window import summarise_window


def measure_calorimetry(clients, settings, save_path):
    """Record a run, have the operator pick its baseline and experiment zones, then report."""
    curve = load_cooling_curve()
    samples = record_samples(clients, settings, curve, save_path)
    if not samples:
        print("No samples recorded, nothing to analyse.")
        return
    windows = select_windows(samples, lambda: keep_alive(clients, settings))
    baseline = summarise_window(samples, "Q_abs (W)", windows["baseline"])
    plate = summarise_window(samples, "Plate temperature (C)", windows["baseline"])
    check_baseline(plate["mean"], baseline["mean"], baseline["spread"])
    master = None
    if any(row["Master temperature (C)"] is not None for row in samples):
        master = summarise_window(samples, "Master temperature (C)", windows["baseline"])["mean"]
    energy = integrate_energy(samples, baseline["mean"], plate["mean"], master, windows)
    rewrite_csv(samples, save_path)
    generate_report(samples, windows, baseline, energy, save_path)
