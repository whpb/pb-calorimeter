import matplotlib.pyplot as plt

ZONES = (("baseline", "tab:blue"), ("experiment", "tab:green"))


def plot_work_curve(samples, windows, save_path):
    """Plot Q_relative and plate temperature change on a shared time axis, zones shaded."""
    path = save_path.with_suffix(".png")
    elapsed = [row["Elapsed (min)"] for row in samples]
    figure, power_axes = plt.subplots(figsize=(10, 5))
    power_axes.axhline(0, color="grey", linewidth=0.8)
    for name, colour in ZONES:
        power_axes.axvspan(*windows[name], color=colour, alpha=0.12, label=f"{name} zone")
    power = power_axes.plot(elapsed, [row["Q_relative (W)"] for row in samples], color="C0",
                            linewidth=1.2, label="Q_relative (W)")
    power_axes.set_xlabel("Elapsed (min)")
    power_axes.set_ylabel("Q_relative (W)", color="C0")
    power_axes.tick_params(axis="y", labelcolor="C0")
    power_axes.grid(alpha=0.3)
    temperature_axes = power_axes.twinx()  # shares the elapsed-time axis, own vertical scale
    temperature = temperature_axes.plot(elapsed, [row["Plate temperature change (C)"] for row in samples],
                                        color="C3", linewidth=1.2, label="Plate temperature change (C)")
    temperature_axes.set_ylabel("Plate temperature change (C)", color="C3")
    temperature_axes.tick_params(axis="y", labelcolor="C3")
    power_axes.set_title("Heat flow and plate temperature relative to the selected baseline")
    handles = power + temperature
    power_axes.legend(handles + [patch for patch in power_axes.patches],
                      [line.get_label() for line in handles] + [f"{name} zone" for name, _ in ZONES],
                      loc="best", fontsize="small")
    figure.tight_layout()
    figure.savefig(path, dpi=150)
    plt.close(figure)
    return path
