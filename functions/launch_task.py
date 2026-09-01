import subprocess
import sys
import threading
from pathlib import Path
from queue import Queue

REPO = Path(__file__).resolve().parent.parent


def launch_task(script, arguments=()):
    """Run a script as a child process, streaming its output onto a queue a line at a time."""
    # -u is essential: piped stdout is block buffered otherwise, and the log arrives in lumps
    process = subprocess.Popen([sys.executable, "-u", str(REPO / script), *arguments],
                               cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               text=True, bufsize=1,
                               creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    lines = Queue()
    # daemon, so a blocking readline can never hold the interface open or outlive it
    threading.Thread(target=lambda: [lines.put(line) for line in process.stdout],
                     daemon=True).start()
    return process, lines
