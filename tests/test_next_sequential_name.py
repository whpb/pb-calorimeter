from functions.next_sequential_name import next_sequential_name


def test_starts_at_one_in_an_empty_folder(tmp_path):
    assert next_sequential_name(tmp_path, "Run") == "Run 1"


def test_skips_names_already_taken(tmp_path):
    (tmp_path / "Run 1.csv").touch()
    (tmp_path / "Run 2.csv").touch()
    assert next_sequential_name(tmp_path, "Run") == "Run 3"


def test_only_counts_matching_stems(tmp_path):
    (tmp_path / "Other 1.csv").touch()
    (tmp_path / "Run 1.txt").touch()
    assert next_sequential_name(tmp_path, "Run") == "Run 1"
