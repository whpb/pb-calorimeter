from datetime import datetime

from functions.compile_report import compile_report
from functions.plot_work_curve import plot_work_curve
from functions.summarise_window import summarise_window


def generate_report(samples, windows, baseline, energy, save_path):
    """Summarise the selected zones to console and render them as a Typst PDF."""
    experiment = summarise_window(samples, "Q_relative (W)", windows["experiment"])
    inside = [row["Q_relative (W)"] for row in samples if row["Zone"] == "experiment"]
    summary = {
        "samples": len(samples),
        "duration_min": round(samples[-1]["Elapsed (min)"] - samples[0]["Elapsed (min)"], 2),
        "baseline_w": baseline["mean"],
        "peak_w": round(max(inside, key=abs), 2),
        "energy_j": round(energy, 1),
        "direction": "added to" if energy >= 0 else "removed from",
        "baseline": baseline,
        "experiment": experiment,
        "plot": plot_work_curve(samples, windows, save_path).name,
        "finished": datetime.now().isoformat(timespec="seconds"),
    }
    print(f"Baseline zone {baseline['start_min']:.2f}-{baseline['end_min']:.2f} min, "
          f"experiment zone {experiment['start_min']:.2f}-{experiment['end_min']:.2f} min")
    print(f"Total energy: {energy:.1f} J "
          f"({abs(energy) / 1000:.3f} kJ {summary['direction']} the plate)")
    report = compile_report(summary, save_path)
    if report:
        print(f"Report written to {report}")
