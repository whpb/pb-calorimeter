import tempfile
import tkinter as tk
from pathlib import Path

from functions.bundled_path import bundled_path
from functions.load_fonts import load_fonts

load_fonts()  # before Tk exists: Tcl enumerates the font families once, at start-up

from functions import tokens as t
from functions.apply_theme import apply_theme
from functions.build_menu import build_menu
from functions.build_name import build_name
from functions.build_progress import build_progress
from functions.build_results import build_results
from functions.launch_task import launch_task
from functions.window_backdrop import window_backdrop
from functions.window_icon import window_icon

REPORT_PREFIX = "Report written to "
DRAIN_MS = 120
# both processes agree on this path because app.py passes it to the child
SENTINEL = Path(tempfile.gettempdir()) / "pb-calorimeter-stop"

root = tk.Tk()
root.title("PB Calorimeter")
root.geometry(f"{t.WIDTH}x{t.HEIGHT}")
root.resizable(False, False)  # every screen is laid out on the grid at exactly this size
apply_theme(root)
backdrop = window_backdrop(bundled_path("assets") / "background.png",
                           (t.WIDTH, t.HEIGHT))
icon = window_icon(root)
if icon is not None:
    root.iconphoto(True, icon)
state = {"frame": None, "task": None, "screen": None, "widgets": None, "lines": [],
         "report": None, "heading": "", "stop": None}


def stop_task():
    """Terminate the child if one is running. Its CSV and log are already on disk."""
    if state["task"] and state["task"][0].poll() is None:
        state["task"][0].terminate()
    state["task"] = None
    SENTINEL.unlink(missing_ok=True)


def show(frame):
    if state["frame"] is not None:
        state["frame"].destroy()
    state["frame"] = frame
    frame.pack(fill="both", expand=True)


def append(line):
    if state["screen"] != "progress":
        return
    state["widgets"]["status"].configure(text=line[:120])
    state["widgets"]["log"].insert("end", line + "\n")
    state["widgets"]["log"].see("end")


def show_progress(heading):
    state["widgets"] = build_progress(root, backdrop, heading, show_menu, state["stop"])
    state["screen"] = "progress"
    show(state["widgets"]["frame"])
    for line in state["lines"]:  # replayed, so returning from the results panel loses nothing
        append(line)


def show_results():
    state["screen"] = "results"
    running = state["task"] and state["task"][0].poll() is None
    show(build_results(root, backdrop, state["report"], show_menu,
                       resume_testing if running else None))


def resume_testing():
    show_progress(state["heading"])


def request_stop():
    """Ask a forced run to stop; it finishes the file and opens the selection window itself."""
    SENTINEL.touch()
    state["widgets"]["status"].configure(text="Stopping - the selection window will open shortly.")


def drain():
    """Pump the child's output into the holding screen, and spot a finished report going by."""
    if state["task"] is None:
        return
    process, lines = state["task"]
    while not lines.empty():
        line = lines.get().rstrip()
        state["lines"].append(line)
        append(line)
        if line.startswith(REPORT_PREFIX):
            state["report"] = Path(line[len(REPORT_PREFIX):])
            show_results()
    if state["screen"] == "progress" and process.poll() is not None:
        state["widgets"]["status"].configure(text=f"Stopped (exit code {process.returncode})")
    root.after(DRAIN_MS, drain)


def start(mode, heading, arguments=(), on_stop=None):
    state["lines"], state["report"] = [], None
    state["heading"], state["stop"] = heading, on_stop
    state["task"] = launch_task(mode, arguments)
    show_progress(heading)
    root.after(DRAIN_MS, drain)


def show_name():
    """A forced run is named before it starts, so its folder says what it holds."""
    state["screen"] = "name"
    show(build_name(root, backdrop, start_experiment, show_menu))


def start_experiment(name):
    # the name reaches force_run.py as argv[2] and becomes the run folder; blank is allowed
    start("force_run", name.strip() or "Run an Experiment", [str(SENTINEL), name],
          request_stop)


def show_menu():
    stop_task()  # leaving testing mode stops the run; whatever it recorded is kept
    state["screen"], state["lines"], state["report"] = "menu", [], None
    show(build_menu(root, backdrop, (
        lambda: start("main", "Testing mode"),
        show_name,
        lambda: start("reanalyse", "Re-analysis"),
        quit_app)))


def quit_app():
    stop_task()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", quit_app)
show_menu()
root.mainloop()
