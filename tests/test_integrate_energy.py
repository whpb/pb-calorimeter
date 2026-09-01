import pytest

from functions.integrate_energy import integrate_energy

WINDOWS = {"baseline": (0.0, 1 / 60), "experiment": (2 / 60, 4 / 60)}


def _samples(flows, temperatures=None, probes=None):
    return [{"Elapsed (min)": i / 60, "Q_abs (W)": flow,
             "Plate temperature (C)": (temperatures or [25.0] * len(flows))[i],
             "Master temperature (C)": (probes or [None] * len(flows))[i]}
            for i, flow in enumerate(flows)]


def test_integrates_only_inside_the_experiment_zone():
    samples = _samples([0.0, 0.0, 10.0, 10.0, 10.0])
    # three samples in the zone, but the first opens it: two 1 s steps at 10 W
    assert integrate_energy(samples, 0.0, 25.0, None, WINDOWS) == pytest.approx(20.0)


def test_subtracts_the_baseline_from_every_sample():
    samples = _samples([5.0] * 5)
    integrate_energy(samples, 2.0, 25.0, None, WINDOWS)
    assert [row["Q_relative (W)"] for row in samples] == [3.0] * 5


def test_records_temperature_change_against_the_baseline_zone():
    samples = _samples([0.0] * 3, temperatures=[25.0, 24.0, 22.5])
    integrate_energy(samples, 0.0, 25.0, None, WINDOWS)
    assert [row["Plate temperature change (C)"] for row in samples] == [0.0, -1.0, -2.5]


def test_tags_each_sample_with_its_zone():
    samples = _samples([0.0] * 5)
    integrate_energy(samples, 0.0, 25.0, None, WINDOWS)
    assert [row["Zone"] for row in samples] == ["baseline", "baseline", "experiment",
                                                "experiment", "experiment"]


def test_energy_is_blank_outside_the_experiment_zone():
    samples = _samples([10.0] * 5)
    integrate_energy(samples, 0.0, 25.0, None, WINDOWS)
    assert [row["Energy (J)"] for row in samples][:2] == [None, None]
    assert samples[-1]["Energy (J)"] is not None


def test_a_gap_integrates_as_a_zero_order_hold():
    """A sample dropped mid-run must not cost the integral the seconds it spanned."""
    samples = _samples([0.0, 0.0, 10.0, 10.0, 10.0])
    del samples[3]
    assert integrate_energy(samples, 0.0, 25.0, None, WINDOWS) == pytest.approx(20.0)


def test_the_experiment_zone_wins_where_the_zones_overlap():
    samples = _samples([0.0] * 3)
    integrate_energy(samples, 0.0, 25.0, None, {"baseline": (0.0, 1.0), "experiment": (0.0, 1.0)})
    assert {row["Zone"] for row in samples} == {"experiment"}


def test_records_probe_change_against_its_own_baseline():
    samples = _samples([0.0] * 3, probes=[5.0, 6.0, 7.5])
    integrate_energy(samples, 0.0, 25.0, 5.0, WINDOWS)
    assert [row["Master temperature change (C)"] for row in samples] == [0.0, 1.0, 2.5]


def test_leaves_the_probe_change_blank_when_it_is_unconfigured():
    """No address means no reading; a zero here would look like a probe holding steady."""
    samples = _samples([0.0] * 3)
    integrate_energy(samples, 0.0, 25.0, None, WINDOWS)
    assert [row["Master temperature change (C)"] for row in samples] == [None] * 3
