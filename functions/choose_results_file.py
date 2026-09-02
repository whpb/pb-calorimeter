from pathlib import Path
from tkinter import Tk, filedialog

from functions.resolve_results_root import resolve_results_root


def choose_results_file(arguments, settings):
    """Take the CSV from the command line, or ask for one if the script was double-clicked."""
    if arguments:
        return Path(arguments[0])
    root = Tk()
    root.withdraw()  # the dialog is the whole UI; no empty window behind it
    # the root, not resolve_save_path: asking for a file must not create a run folder
    chosen = filedialog.askopenfilename(title="Choose a results CSV to re-analyse",
                                        initialdir=resolve_results_root(settings),
                                        filetypes=[("Results CSV", "*.csv")])
    root.destroy()
    return Path(chosen) if chosen else None
