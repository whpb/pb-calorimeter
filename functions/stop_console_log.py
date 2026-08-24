import sys


def stop_console_log(log_file):
    """Restore normal console output and close the session log file."""
    sys.stdout = sys.stdout.streams[0]
    sys.stderr = sys.stderr.streams[0]
    log_file.close()
