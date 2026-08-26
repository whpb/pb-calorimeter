from functions.save_csv import save_csv


def test_writes_a_header_only_for_a_new_file(tmp_path):
    path = tmp_path / "results.csv"
    save_csv({"A": 1, "B": 2}, path, quiet=True)
    save_csv({"A": 3, "B": 4}, path, quiet=True)
    assert path.read_text().splitlines() == ["A,B", "1,2", "3,4"]


def test_appends_without_blank_lines(tmp_path):
    """newline="" matters on Windows; without it every row gains a trailing blank line."""
    path = tmp_path / "results.csv"
    for i in range(3):
        save_csv({"A": i}, path, quiet=True)
    assert path.read_text().count("\n\n") == 0


def test_announces_the_save_unless_quiet(tmp_path, capsys):
    path = tmp_path / "results.csv"
    save_csv({"A": 1}, path, quiet=True)
    assert capsys.readouterr().out == ""
    save_csv({"A": 2}, path)
    assert "Saved results to" in capsys.readouterr().out
