from functions.stop_requested import stop_requested


def test_false_until_the_interface_asks(tmp_path):
    assert stop_requested(tmp_path / "stop") is False


def test_true_once_the_file_appears(tmp_path):
    sentinel = tmp_path / "stop"
    sentinel.touch()
    assert stop_requested(sentinel) is True


def test_accepts_a_plain_string_path(tmp_path):
    """app.py passes the path to the child as a command-line argument, so it arrives as text."""
    sentinel = tmp_path / "stop"
    sentinel.touch()
    assert stop_requested(str(sentinel)) is True


def test_asking_twice_is_harmless(tmp_path):
    """The Stop button can be pressed repeatedly while the last sample finishes."""
    sentinel = tmp_path / "stop"
    sentinel.touch()
    sentinel.touch()
    assert stop_requested(sentinel) is True
