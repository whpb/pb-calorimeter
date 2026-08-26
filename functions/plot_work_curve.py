import matplotlib

matplotlib.use("Agg")  # no GUI on the rig PC; must be set before pyplot is imported

import matplotlib.pyplot as plt


def plot_work_curve(history, save_path):
    """Plot Q_relative against elapsed time and save it beside the results CSV."""
    path = save_path.with_suffix(".png")
    figure, axes = plt.subplots(figsize=(10, 5))
    axes.axhline(0, color="grey", linewidth=0.8)
    axes.plot([row[0] for row in history], [row[1] for row in history], linewidth=1.2)
    axes.set_xlabel("Elapsed (min)")
    axes.set_ylabel("Q_relative (W)")
    axes.set_title("Heat flow relative to baseline")
    axes.grid(alpha=0.3)
    figure.tight_layout()
    figure.savefig(path, dpi=150)
    plt.close(figure)
    return path
