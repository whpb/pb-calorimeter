import csv

from functions.rewrite_csv import rewrite_csv
from functions.save_csv import save_csv

ROWS = [{"A": 1, "B": 2, "Derived": 10}, {"A": 3, "B": 4, "Derived": None}]


def test_writes_every_row_under_one_header(tmp_path):
    path = tmp_path / "results.csv"
    rewrite_csv(ROWS, path)
    assert path.read_text().splitlines() == ["A,B,Derived", "1,2,10", "3,4,"]


def test_replaces_the_live_file_it_grew_from(tmp_path):
    """The run appends raw rows as it goes; the rewrite adds the columns selection produced."""
    path = tmp_path / "results.csv"
    for row in ROWS:
        save_csv({"A": row["A"], "B": row["B"]}, path, quiet=True)
    rewrite_csv(ROWS, path)
    with open(path, newline="") as f:
        written = list(csv.DictReader(f))
    assert len(written) == 2 and written[0]["Derived"] == "10"


def test_leaves_no_temporary_file_behind(tmp_path):
    path = tmp_path / "results.csv"
    rewrite_csv(ROWS, path)
    assert [p.name for p in tmp_path.iterdir()] == ["results.csv"]
