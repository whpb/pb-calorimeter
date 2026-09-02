from datetime import datetime

from functions.next_sequential_name import next_sequential_name
from functions.resolve_results_root import resolve_results_root
from functions.safe_name import safe_name

DEFAULT_FILENAME_PATTERN = "%Y-%m-%dT%H-%M-%S"


def resolve_save_path(settings, name=""):
    """Resolve a run's own folder inside the results root, and the CSV file inside it.

    One folder per run, named after the experiment when the operator typed one, so
    everything that run produces stays together and nothing can land on an earlier run.
    """
    root = resolve_results_root(settings)
    stem = safe_name(name)
    if not stem:
        pattern = DEFAULT_FILENAME_PATTERN if settings["FileName"] == "auto" else settings["FileName"]
        stem = datetime.now().strftime(pattern) if "%" in pattern else next_sequential_name(root, pattern, "")
    # a repeated name, or two runs inside one second, takes the next free number
    if (root / stem).exists():
        stem = next_sequential_name(root, stem, "")
    folder = root / stem
    folder.mkdir(parents=True, exist_ok=True)
    return folder / f"{stem}.csv"
