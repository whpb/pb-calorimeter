from datetime import datetime

from functions.compile_report import compile_report
from functions.plot_work_curve import plot_work_curve


def generate_report(history, energy, baseline, save_path):
    """Summarise a completed measurement to console and render it as a Typst PDF."""
    if not history:
        print("No samples recorded, skipping report.")
        return
    peak = max(history, key=lambda row: abs(row[1]))[1]
    summary = {
        "samples": len(history),
        "duration_min": round(history[-1][0] - history[0][0], 2),
        "baseline_w": round(baseline, 2),
        "peak_w": round(peak, 2),
        "energy_j": round(energy, 1),
        "direction": "added to" if energy >= 0 else "removed from",
        "plot": plot_work_curve(history, save_path).name,
        "finished": datetime.now().isoformat(timespec="seconds"),
    }
    print(f"{summary['samples']} samples over {summary['duration_min']:.2f} min, "
          f"baseline {summary['baseline_w']:.2f} W, peak {summary['peak_w']:.2f} W")
    print(f"Total energy: {energy:.1f} J "
          f"({abs(energy) / 1000:.3f} kJ {summary['direction']} the plate)")
    report = compile_report(summary, save_path)
    if report:
        print(f"Report written to {report}")
