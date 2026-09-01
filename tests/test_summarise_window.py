import pytest

from functions.summarise_window import summarise_window


def _samples(values, key="Q_abs (W)"):
    return [{"Elapsed (min)": i / 60, key: value} for i, value in enumerate(values)]


def test_describes_the_extent_of_the_zone():
    described = summarise_window(_samples([1, 2, 3, 4]), "Q_abs (W)", (0.0, 3 / 60))
    assert (described["start_min"], described["end_min"]) == (0.0, 0.05)
    assert described["duration_min"] == 0.05 and described["samples"] == 4


def test_averages_only_what_lies_inside():
    described = summarise_window(_samples([0, 10, 20, 1000]), "Q_abs (W)", (0.0, 2 / 60))
    assert described["mean"] == pytest.approx(10.0) and described["samples"] == 3


def test_boundaries_are_inclusive():
    assert summarise_window(_samples([5, 5]), "Q_abs (W)", (0.0, 1 / 60))["samples"] == 2


def test_reports_the_swing_it_averaged_over():
    """A wide sd or spread is how the operator learns the zone missed whole noise cycles."""
    described = summarise_window(_samples([-10, 10, -10, 10]), "Q_abs (W)", (0.0, 1.0))
    assert described["mean"] == pytest.approx(0.0)
    assert described["spread"] == pytest.approx(20.0)
    assert described["sd"] > 10


def test_a_steady_zone_has_no_spread():
    described = summarise_window(_samples([4, 4, 4]), "Q_abs (W)", (0.0, 1.0))
    assert (described["sd"], described["spread"]) == (0.0, 0.0)


def test_a_single_sample_has_no_standard_deviation():
    assert summarise_window(_samples([7]), "Q_abs (W)", (0.0, 1.0))["sd"] == 0.0


def test_ignores_unconfigured_probe_readings():
    samples = _samples([None, 5.0, None], key="Master temperature (C)")
    assert summarise_window(samples, "Master temperature (C)", (0.0, 1.0))["samples"] == 1


def test_raises_on_an_empty_selection():
    with pytest.raises(ValueError, match="holds no"):
        summarise_window(_samples([1, 2]), "Q_abs (W)", (5.0, 6.0))
