import subprocess
import sys
import time
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent

from functions.start_console_log import start_console_log, _Tee
from functions.stop_console_log import stop_console_log


@pytest.fixture
def session(tmp_path):
    """Start the log inside the test body — pytest swaps sys.stdout between setup and call."""
    started = []

    def start():
        started.append(start_console_log(tmp_path))
        return started[-1], tmp_path / "logs"

    original = sys.stdout, sys.stderr
    try:
        yield start
    finally:
        for log_file in started:
            log_file.close()
        sys.stdout, sys.stderr = original


def test_creates_a_timestamped_log_inside_the_folder(session):
    _, logs_dir = session()
    assert [path.suffix for path in logs_dir.iterdir()] == [".log"]


def test_mirrors_stdout_and_stderr_to_the_file(session):
    log_file, logs_dir = session()
    print("hello")
    print("oops", file=sys.stderr)
    log_file.flush()
    written = next(logs_dir.iterdir()).read_text(encoding="utf-8")
    assert "hello" in written and "oops" in written


def test_leaves_the_console_stream_working(session, capsys):
    log_file, _ = session()
    print("still visible")
    stop_console_log(log_file)
    assert "still visible" in capsys.readouterr().out


def test_wraps_both_streams_in_a_tee(session):
    session()
    assert isinstance(sys.stdout, _Tee) and isinstance(sys.stderr, _Tee)


def test_tee_forwards_writes_and_flushes_to_every_stream():
    class Recorder:
        def __init__(self):
            self.data, self.flushed = "", False

        def write(self, text):
            self.data += text

        def flush(self):
            self.flushed = True

    a, b = Recorder(), Recorder()
    tee = _Tee(a, b)
    tee.write("x")
    tee.flush()
    assert (a.data, b.data) == ("x", "x") and a.flushed and b.flushed


def test_the_log_survives_a_hard_kill(tmp_path):
    """The window closing must not take the session's log with it, hence line buffering."""
    driver = tmp_path / "driver.py"
    driver.write_text(f"""
import pathlib, sys, time
sys.path.insert(0, {str(REPO)!r})
from functions.start_console_log import start_console_log

here = pathlib.Path({str(tmp_path)!r})
start_console_log(here)
print("MARKER")
(here / "printed").write_text("y")   # a separately closed file, so it cannot vouch for itself
time.sleep(60)
""", encoding="utf-8")
    process = subprocess.Popen([sys.executable, str(driver)])
    try:
        deadline = time.monotonic() + 30
        while not (tmp_path / "printed").exists() and time.monotonic() < deadline:
            time.sleep(0.05)
        assert (tmp_path / "printed").exists(), "the child never reached its print"
    finally:
        process.kill()  # TerminateProcess on Windows: no atexit, no close, no flush
        process.wait()
    logged = next((tmp_path / "logs").iterdir()).read_text(encoding="utf-8")
    assert "MARKER" in logged
