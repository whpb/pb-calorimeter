from pathlib import Path


def resolve_results_root(settings):
    """The folder every run's own folder is created inside, made if it is not there yet.

    Only the automatic path gains the results subfolder: an explicit SavePath is used as
    given, since an operator pointing at a share meant that folder, not one below it.
    """
    if settings["SavePath"] == "auto":
        folder = Path.home() / "Documents" / "PBCal" / "results"
    else:
        folder = Path(settings["SavePath"])
    folder.mkdir(parents=True, exist_ok=True)
    return folder
