import pytest

from functions import load_cooling_curve as module
from functions.resolve_docs_folder import resolve_docs_folder


def _write_curve(body):
    """Overwrite the seeded curve in the docs folder, which is where it is now read from."""
    path = resolve_docs_folder() / module.CURVE_FILE
    path.write_bytes(body)
    return path


def test_reads_the_seeded_calibration_sweep(docs_home):
    temps, outputs = module.load_cooling_curve()
    assert len(temps) == len(outputs) >= 2
    assert all(isinstance(t, float) for t in temps)  # the UTF-8 BOM did not poison column one


def test_returns_points_sorted_by_temperature(docs_home):
    """The sweep is recorded in heating-output order and its cold end is non-monotonic."""
    temps, _ = module.load_cooling_curve()
    assert temps == sorted(temps)


def test_the_operator_can_recalibrate_by_editing_the_docs_copy(docs_home):
    _write_curve(b'"T","O"\r\n20,60\r\n-5,0\r\n10,30\r\n')
    assert module.load_cooling_curve() == ([-5.0, 10.0, 20.0], [0.0, 30.0, 60.0])


def test_skips_trailing_blank_rows(docs_home):
    _write_curve(b'"T","O"\r\n0,0\r\n10,10\r\n,\r\n')
    assert module.load_cooling_curve() == ([0.0, 10.0], [0.0, 10.0])


def test_raises_when_the_file_is_missing(docs_home, monkeypatch):
    monkeypatch.setattr(module, "CURVE_FILE", "absent.csv")
    with pytest.raises(FileNotFoundError):
        module.load_cooling_curve()


def test_raises_when_there_is_nothing_to_interpolate_between(docs_home):
    _write_curve(b'"T","O"\r\n0,0\r\n')
    with pytest.raises(ValueError, match="at least two points"):
        module.load_cooling_curve()
