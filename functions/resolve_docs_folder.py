import shutil
from pathlib import Path

from functions.bundled_path import bundled_path

# what the operator may edit -> what it is first seeded from. settings.json cannot ship
# under its own name: it is gitignored, so a clean checkout has only the default.
SEEDED = {"settings.json": "settings.default.json",
          "pb_cooling_capacity.csv": "pb_cooling_capacity.csv",
          "report_template.typ": "report_template.typ",
          "README.md": "README.md"}


def resolve_docs_folder():
    """The operator's editable copies of the settings, curve, template and README.

    Fixed under Documents rather than following SavePath, because settings.json lives here
    and nothing can read SavePath until it has been loaded. Seeded only where a file is
    absent, so an upgrade never overwrites a curve or a template the operator has tuned.
    """
    folder = Path.home() / "Documents" / "PBCal" / "docs"
    folder.mkdir(parents=True, exist_ok=True)
    for name, source in SEEDED.items():
        original = bundled_path(source)
        if not (folder / name).exists() and original.exists():
            shutil.copyfile(original, folder / name)
    return folder
