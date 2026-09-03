import sys
from pathlib import Path

# Nuitka marks every compiled module with __compiled__ and sets sys.frozen in standalone
# builds; either alone is enough, both together survive a change of build mode.
FROZEN = getattr(sys, "frozen", False) or "__compiled__" in globals()
# compiled there is no functions/ on disk to climb out of, so the exe's own folder is the
# anchor - which is exactly where Nuitka's --include-data-* options put things
ROOT = Path(sys.executable).parent if FROZEN else Path(__file__).resolve().parent.parent


def bundled_path(name=""):
    """A file shipped with the program, or with no name the folder they all sit in.

    The dist folder compiled, the repo run from source. ROOT is read on each call so
    a test can move the whole bundle with one monkeypatch.
    """
    return ROOT / name
