import matplotlib

matplotlib.use("Agg")  # no GUI on the rig PC; must be set before pyplot is imported

import matplotlib.pyplot as plt


def plot_work_curve(history, save_path):
    """Plot Q_relative and plate temperature change against a shared elapsed-time axis."""
    path = save_path.with_suffix(".png")
    elapsed = [row[0] for row in history]
    figure, power_axes = plt.subplots(figsize=(10, 5))
    power_axes.axhline(0, color="grey", linewidth=0.8)
    power = power_axes.plot(elapsed, [row[1] for row in history], color="C0",
                            linewidth=1.2, label="Q_relative (W)")
    power_axes.set_xlabel("Elapsed (min)")
    power_axes.set_ylabel("Q_relative (W)", color="C0")
    power_axes.tick_params(axis="y", labelcolor="C0")
    power_axes.grid(alpha=0.3)
    temperature_axes = power_axes.twinx()  # shares the elapsed-time axis, own vertical scale
    temperature = temperature_axes.plot(elapsed, [row[2] for row in history], color="C3",
                                        linewidth=1.2, label="Plate temperature change (C)")
    temperature_axes.set_ylabel("Plate temperature change (C)", color="C3")
    temperature_axes.tick_params(axis="y", labelcolor="C3")
    power_axes.set_title("Heat flow and plate temperature relative to baseline")
    power_axes.legend(power + temperature, [line.get_label() for line in power + temperature],
                      loc="best", fontsize="small")
    figure.tight_layout()
    figure.savefig(path, dpi=150)
    plt.close(figure)
    return path
