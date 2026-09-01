from functions.check_baseline import check_baseline
from functions.generate_report import generate_report
from functions.integrate_energy import integrate_energy
from functions.rewrite_csv import rewrite_csv
from functions.select_windows import select_windows
from functions.summarise_window import summarise_window


def analyse_samples(samples, save_path, keep_alive_callback):
    """Have the operator pick the zones, derive the columns from them, and report."""
    windows = select_windows(samples, keep_alive_callback)
    baseline = summarise_window(samples, "Q_abs (W)", windows["baseline"])
    plate = summarise_window(samples, "Plate temperature (C)", windows["baseline"])
    check_baseline(plate["mean"], baseline["mean"], baseline["spread"])
    master = None
    if any(row["Master temperature (C)"] is not None for row in samples):
        master = summarise_window(samples, "Master temperature (C)", windows["baseline"])["mean"]
    energy = integrate_energy(samples, baseline["mean"], plate["mean"], master, windows)
    rewrite_csv(samples, save_path)
    generate_report(samples, windows, baseline, energy, save_path)
