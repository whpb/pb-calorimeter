from functions.plot_work_curve import plot_work_curve


def generate_report(history, energy, baseline, save_path):
    """Summarise a completed measurement to file and console, and plot its work curve."""
    if not history:
        print("No samples recorded, skipping report.")
        return
    direction = "added to" if energy >= 0 else "removed from"
    peak = max(history, key=lambda row: abs(row[1]))[1]
    plot_path = plot_work_curve(history, save_path)
    lines = [
        f"Samples:         {len(history)}",
        f"Duration:        {history[-1][0] - history[0][0]:.2f} min",
        f"Baseline Q_abs:  {baseline:.2f} W",
        f"Peak Q_relative: {peak:.2f} W",
        f"Total energy:    {energy:.1f} J ({abs(energy) / 1000:.3f} kJ {direction} the plate)",
        f"Work curve:      {plot_path.name}",
    ]
    report_path = save_path.with_suffix(".txt")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"Report written to {report_path}")
