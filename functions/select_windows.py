import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector

from functions.plot_selection_panes import plot_selection_panes

KEEP_ALIVE_MS = 5000
PANES = (("baseline", "tab:blue"), ("experiment", "tab:green"))


def select_windows(samples, keep_alive_callback):
    """Block on the selection window and return the chosen zones as {name: (start, end)} minutes."""
    figure, *axes = plot_selection_panes(samples)
    elapsed = [row["Elapsed (min)"] for row in samples]
    quarter = elapsed[len(elapsed) // 4]
    chosen = {"baseline": (elapsed[0], quarter), "experiment": (quarter, elapsed[-1])}

    def pump():  # a MODBUS blip must not kill the window, but the rig must not drop us either
        try:
            keep_alive_callback()
        except Exception as e:
            print(f"Keep-alive failed during selection: {e}")

    # held in a list only so the selectors survive garbage collection while the window is open
    selectors = [SpanSelector(pane, lambda a, b, k=name: chosen.__setitem__(k, (a, b)),
                              "horizontal", interactive=True, drag_from_anywhere=True,
                              props=dict(alpha=0.25, facecolor=colour))
                 for pane, (name, colour) in zip(axes, PANES)]
    for selector, (name, _) in zip(selectors, PANES):
        selector.extents = chosen[name]
    timer = figure.canvas.new_timer(interval=KEEP_ALIVE_MS)
    timer.add_callback(pump)
    timer.start()
    plt.show()
    timer.stop()
    return chosen
