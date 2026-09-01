import os


def open_path(path):
    """Open a results file or folder in whatever application Windows associates with it."""
    os.startfile(path)
