import pytest

from functions import load_cooling_curve as module


def _write_curve(tmp_path, monkeypatch, body):
    """Point CURVE_FILE at a temporary file (an absolute path wins the / join)."""
    path = tmp_path / "curve.csv"
    path.write_bytes(body)
    monkeypatch.setattr(module, "CURVE_FILE", str(path))
    return path


def test_reads_the_real_calibration_sweep():
    temps, outputs = module.load_cooling_curve()
    assert len(temps) == len(outputs) >= 2
    assert all(isinstance(t, float) for t in temps)  # the UTF-8 BOM did not poison column one


def test_returns_points_sorted_by_temperature():
    """The sweep is recorded in heating-output order and its cold end is non-monotonic."""
    temps, _ = module.load_cooling_curve()
    assert temps == sorted(temps)


def test_sorts_an_unordered_file(tmp_path, monkeypatch):
    _write_curve(tmp_path, monkeypatch, b'"T","O"\r\n20,60\r\n-5,0\r\n10,30\r\n')
    assert module.load_cooling_curve() == ([-5.0, 10.0, 20.0], [0.0, 30.0, 60.0])


def test_skips_trailing_blank_rows(tmp_path, monkeypatch):
    _write_curve(tmp_path, monkeypatch, b'"T","O"\r\n0,0\r\n10,10\r\n,\r\n')
    assert module.load_cooling_curve() == ([0.0, 10.0], [0.0, 10.0])


def test_raises_when_the_file_is_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(module, "CURVE_FILE", str(tmp_path / "absent.csv"))
    with pytest.raises(FileNotFoundError):
        module.load_cooling_curve()


def test_raises_when_there_is_nothing_to_interpolate_between(tmp_path, monkeypatch):
    _write_curve(tmp_path, monkeypatch, b'"T","O"\r\n0,0\r\n')
    with pytest.raises(ValueError, match="at least two points"):
        module.load_cooling_curve()
