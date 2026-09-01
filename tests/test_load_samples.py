import pytest

from functions.load_samples import load_samples
from functions.rewrite_csv import rewrite_csv

RAW = {"Timestamp": "2026-09-01T11:00:00", "Elapsed (min)": 0.0167,
       "Plate temperature (C)": 25.0, "Master temperature (C)": 24.6,
       "Heater utilisation (%)": 25.0, "Q_abs (W)": 7.7}
DERIVED = {"Q_relative (W)": 0.0, "Plate temperature change (C)": 0.0,
           "Master temperature change (C)": 0.0, "Energy (J)": 0.0, "Zone": "baseline"}


def _write(tmp_path, rows):
    path = tmp_path / "results.csv"
    rewrite_csv(rows, path)
    return path


def test_round_trips_a_results_file(tmp_path):
    assert load_samples(_write(tmp_path, [RAW])) == [RAW]


def test_numbers_come_back_as_numbers(tmp_path):
    row = load_samples(_write(tmp_path, [RAW]))[0]
    assert isinstance(row["Q_abs (W)"], float) and isinstance(row["Timestamp"], str)


def test_drops_the_columns_a_previous_analysis_derived(tmp_path):
    """They depend on the old baseline, so re-analysis must recompute them, not inherit them."""
    loaded = load_samples(_write(tmp_path, [RAW | DERIVED]))
    assert set(loaded[0]) == set(RAW)


def test_a_blank_probe_reads_back_as_none(tmp_path):
    blank = RAW | {"Master temperature (C)": None}
    assert load_samples(_write(tmp_path, [blank]))[0]["Master temperature (C)"] is None


def test_reads_every_row(tmp_path):
    rows = [RAW | {"Elapsed (min)": i / 60} for i in range(5)]
    assert len(load_samples(_write(tmp_path, rows))) == 5


def test_rejects_a_file_that_is_not_a_results_csv(tmp_path):
    path = tmp_path / "other.csv"
    path.write_text("a,b\n1,2\n")
    with pytest.raises(ValueError, match="not a results CSV"):
        load_samples(path)


def test_rejects_a_results_file_with_no_rows(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text(",".join(RAW) + "\n")
    with pytest.raises(ValueError, match="holds no samples"):
        load_samples(path)


def test_reads_a_file_recorded_before_the_probe_column_existed(tmp_path):
    """Old results files have no probe column at all; they must still re-analyse."""
    path = tmp_path / "old.csv"
    older = {name: value for name, value in RAW.items() if name != "Master temperature (C)"}
    rewrite_csv([older], path)
    assert load_samples(path) == [RAW | {"Master temperature (C)": None}]


def test_an_old_file_keeps_the_current_column_order(tmp_path):
    """So a re-analysed old file comes out shaped exactly like a fresh run."""
    path = tmp_path / "old.csv"
    rewrite_csv([{n: v for n, v in RAW.items() if n != "Master temperature (C)"}], path)
    assert list(load_samples(path)[0]) == list(RAW)
