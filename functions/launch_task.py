import subprocess
import sys
import threading
from queue import Queue

from functions.bundled_path import FROZEN, bundled_path


def launch_task(mode, arguments=()):
    """Run one of the program's other modes as a child process, streaming its output.

    Compiled there is no .py file left to hand an interpreter, so the exe relaunches itself
    with --run and launcher.py dispatches; from source it still runs the script directly.
    """
    # -u is essential from source: piped stdout is block buffered otherwise, and the log
    # arrives in lumps. Compiled it is not accepted, and launcher.py line-buffers instead.
    command = ([bundled_path("PBCal.exe"), "--run", str(mode)] if FROZEN
               else [sys.executable, "-u", str(bundled_path(f"{mode}.py"))])
    process = subprocess.Popen([*command, *arguments],
                               cwd=bundled_path(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               text=True, bufsize=1,
                               creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    lines = Queue()
    # daemon, so a blocking readline can never hold the interface open or outlive it
    threading.Thread(target=lambda: [lines.put(line) for line in process.stdout],
                     daemon=True).start()
    return process, lines
