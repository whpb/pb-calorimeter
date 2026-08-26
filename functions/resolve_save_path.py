from pathlib import Path
from datetime import datetime

from functions.next_sequential_name import next_sequential_name

DEFAULT_FILENAME_PATTERN = "%Y-%m-%dT%H-%M-%S"


def resolve_save_path(settings):
    """Resolve the SavePath/FileName settings to a concrete CSV file path."""
    if settings["SavePath"] == "auto":
        folder = Path.home() / "Documents" / "PBCal"
    else:
        folder = Path(settings["SavePath"])
    folder.mkdir(parents=True, exist_ok=True)

    pattern = DEFAULT_FILENAME_PATTERN if settings["FileName"] == "auto" else settings["FileName"]
    if "%" in pattern:
        name = datetime.now().strftime(pattern)
    else:
        name = next_sequential_name(folder, pattern)
    path = folder / f"{name}.csv"
    # two runs inside one second would otherwise share a timestamp, and a file
    return path if not path.exists() else folder / f"{next_sequential_name(folder, name)}.csv"
