import matplotlib.pyplot as plt


def plot_selection_panes(samples):
    """Draw net power above the probe trace on a shared time axis, ready for span selection."""
    elapsed = [row["Elapsed (min)"] for row in samples]
    probe_values = [row["Master temperature (C)"] for row in samples]
    label = "Master probe (C)"
    if all(value is None for value in probe_values):
        # no probe data: either the address is unset, or the file predates the column
        probe_values = [row["Plate temperature (C)"] for row in samples]
        label = "Plate temperature (C) - no master probe data"
    figure, (power, probe) = plt.subplots(2, 1, sharex=True, figsize=(11, 7))
    power.plot(elapsed, [row["Q_abs (W)"] for row in samples], color="C0", linewidth=1.0)
    power.set_ylabel("Q_abs (W)")
    power.set_title("Drag the BASELINE zone here - unloaded plate, whole noise cycles")
    power.grid(alpha=0.3)
    probe.plot(elapsed, probe_values, color="C3", linewidth=1.0)
    probe.set_ylabel(label)
    probe.set_xlabel("Elapsed (min)")
    probe.set_title("Drag the EXPERIMENT zone here, then close the window to accept")
    probe.grid(alpha=0.3)
    figure.tight_layout()
    return figure, power, probe
