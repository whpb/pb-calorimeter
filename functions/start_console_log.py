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


def start_console_log(save_path):
    """Mirror all console output to a timestamped log file under logs/ next to save_path."""
    logs_dir = Path(save_path).parent / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / f"{datetime.now():%Y-%m-%dT%H-%M-%S}.log"
    log_file = open(log_path, "a", encoding="utf-8")
    sys.stdout = _Tee(sys.stdout, log_file)
    sys.stderr = _Tee(sys.stderr, log_file)
    print(f"Logging console output to {log_path}")
    return log_file
