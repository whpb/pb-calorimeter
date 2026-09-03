"""The compiled build's single entry point: dispatch on --run, or open the menu.

One exe rather than four, because each carries the whole runtime - matplotlib, Pillow and
a 62 MB Typst compiler - and four copies of that is most of a gigabyte. app.py still runs
its measurements as child processes; it just relaunches this exe instead of an interpreter.
"""
import importlib
import sys

MODES = ("main", "force_run", "reanalyse")

for stream in (sys.stdout, sys.stderr):
    # what -u does from source, which a compiled child cannot be given. None when Windows
    # gave this process no console, which is the menu launched from its own shortcut.
    if stream is not None:
        stream.reconfigure(line_buffering=True)

if sys.argv[1:2] == ["--run"]:
    mode = sys.argv[2] if len(sys.argv) > 2 else ""
    if mode not in MODES:
        sys.exit(f"Unknown mode {mode!r}; expected one of {', '.join(MODES)}")
    sys.argv = [mode, *sys.argv[3:]]  # each entry point reads its own arguments from argv[1:]
    importlib.import_module(mode)  # the module body is the program, exactly as when run
else:
    importlib.import_module("app")
