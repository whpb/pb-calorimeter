from pathlib import Path


def resolve_results_root(settings):
    """The folder every run's own folder is created inside, made if it is not there yet."""
    if settings["SavePath"] == "auto":
        folder = Path.home() / "Documents" / "PBCal"
    else:
        folder = Path(settings["SavePath"])
    folder.mkdir(parents=True, exist_ok=True)
    return folder
