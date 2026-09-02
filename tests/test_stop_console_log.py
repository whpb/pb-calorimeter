import sys

from functions.start_console_log import start_console_log, _Tee
from functions.stop_console_log import stop_console_log


def test_restores_the_original_streams(tmp_path):
    original_out, original_err = sys.stdout, sys.stderr
    log_file = start_console_log(tmp_path)
    assert isinstance(sys.stdout, _Tee)
    stop_console_log(log_file)
    assert sys.stdout is original_out and sys.stderr is original_err


def test_closes_the_log_file(tmp_path):
    log_file = start_console_log(tmp_path)
    stop_console_log(log_file)
    assert log_file.closed


def test_the_log_survives_the_session(tmp_path):
    log_file = start_console_log(tmp_path)
    print("recorded")
    stop_console_log(log_file)
    logged = next((tmp_path / "logs").iterdir()).read_text(encoding="utf-8")
    assert "recorded" in logged
