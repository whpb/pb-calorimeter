import matplotlib.pyplot as plt

ZONES = (("baseline", "tab:blue"), ("experiment", "tab:green"))
SURROUND = "#E8E8E8"  # behind the titles and labels; the data area itself stays white


def plot_work_curve(samples, windows, save_path):
    """Plot Q_relative and both temperature traces on a shared time axis, zones shaded."""
    path = save_path.with_suffix(".png")
    elapsed = [row["Elapsed (min)"] for row in samples]
    figure, power_axes = plt.subplots(figsize=(10, 5), facecolor=SURROUND)
    power_axes.set_facecolor("white")
    power_axes.axhline(0, color="grey", linewidth=0.8)
    for name, colour in ZONES:
        power_axes.axvspan(*windows[name], color=colour, alpha=0.12, label=f"{name} zone")
    traces = power_axes.plot(elapsed, [row["Q_relative (W)"] for row in samples], color="C0",
                             linewidth=1.2, label="Q_relative (W)")
    power_axes.set_xlabel("Elapsed (min)")
    power_axes.set_ylabel("Q_relative (W)", color="C0")
    power_axes.tick_params(axis="y", labelcolor="C0")
    power_axes.grid(alpha=0.3)
    temperature_axes = power_axes.twinx()  # shares the elapsed-time axis, own vertical scale
    traces += temperature_axes.plot(elapsed, [row["Plate temperature change (C)"] for row in samples],
                                    color="C3", linewidth=1.2, label="Plate temperature")
    probe = [row["Master temperature change (C)"] for row in samples]
    if any(value is not None for value in probe):
        traces += temperature_axes.plot(elapsed, probe, color="C1", linewidth=1.2, label="Master probe")
    temperature_axes.set_ylabel("Temperature change (C)", color="0.25")  # neutral: two traces
    temperature_axes.tick_params(axis="y", labelcolor="0.25")
    power_axes.set_title("Heat flow and temperatures relative to the selected baseline")
    handles = traces + list(power_axes.patches)
    power_axes.legend(handles, [artist.get_label() for artist in handles], loc="best", fontsize="small")
    figure.tight_layout()
    figure.savefig(path, dpi=150, facecolor=SURROUND)
    plt.close(figure)
    return path
