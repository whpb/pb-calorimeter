import sys
from pathlib import Path
from datetime import datetime


class _Tee:
    """Write to multiple streams at once."""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)

    def flush(self):
        for stream in self.streams:
            stream.flush()


def start_console_log(folder):
    """Mirror all console output to a timestamped log file under logs/ inside folder.

    A folder rather than a file: a run's log belongs in the run's own folder, while a
    testing session spans many runs and keeps one log in the results root.
    """
    logs_dir = Path(folder) / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / f"{datetime.now():%Y-%m-%dT%H-%M-%S}.log"
    # line buffered: an abrupt window close must not take the session's log with it
    log_file = open(log_path, "a", buffering=1, encoding="utf-8")
    sys.stdout = _Tee(sys.stdout, log_file)
    sys.stderr = _Tee(sys.stderr, log_file)
    print(f"Logging console output to {log_path}")
    return log_file
