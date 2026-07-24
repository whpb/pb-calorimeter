from pathlib import Path
from datetime import datetime

from functions.next_sequential_name import next_sequential_name

DEFAULT_FILENAME_PATTERN = "%Y-%m-%dT%H-%M-%S"


def resolve_save_path(settings):
    """Resolve the SavePath/FileName settings to a concrete CSV file path."""
    if settings["SavePath"] == "auto":
        folder = Path.home() / "Documents" / "ValveTests2"
    else:
        folder = Path(settings["SavePath"])
    folder.mkdir(parents=True, exist_ok=True)

    pattern = DEFAULT_FILENAME_PATTERN if settings["FileName"] == "auto" else settings["FileName"]
    if "%" in pattern:
        name = datetime.now().strftime(pattern)
    else:
        name = next_sequential_name(folder, pattern)
    return folder / f"{name}.csv"
