import sys

import pytest

from functions.start_console_log import start_console_log, _Tee
from functions.stop_console_log import stop_console_log


@pytest.fixture
def session(tmp_path):
    """Start the log inside the test body — pytest swaps sys.stdout between setup and call."""
    started = []

    def start():
        started.append(start_console_log(tmp_path / "results.csv"))
        return started[-1], tmp_path / "logs"

    original = sys.stdout, sys.stderr
    try:
        yield start
    finally:
        for log_file in started:
            log_file.close()
        sys.stdout, sys.stderr = original


def test_creates_a_timestamped_log_beside_the_results(session):
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
