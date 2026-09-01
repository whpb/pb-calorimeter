from pathlib import Path
from tkinter import Tk, filedialog

from functions.resolve_save_path import resolve_save_path


def choose_results_file(arguments, settings):
    """Take the CSV from the command line, or ask for one if the script was double-clicked."""
    if arguments:
        return Path(arguments[0])
    root = Tk()
    root.withdraw()  # the dialog is the whole UI; no empty window behind it
    # only the folder matters, so the filename resolve_save_path invents is discarded
    chosen = filedialog.askopenfilename(title="Choose a results CSV to re-analyse",
                                        initialdir=resolve_save_path(settings).parent,
                                        filetypes=[("Results CSV", "*.csv")])
    root.destroy()
    return Path(chosen) if chosen else None
