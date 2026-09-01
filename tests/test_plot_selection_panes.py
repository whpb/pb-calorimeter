import matplotlib.pyplot as plt
import pytest

from functions.plot_selection_panes import plot_selection_panes

SAMPLES = [{"Elapsed (min)": i / 60, "Q_abs (W)": float(i), "Plate temperature (C)": 25.0 - i,
            "Master temperature (C)": None} for i in range(4)]


@pytest.fixture
def panes():
    """Hand back (figure, power, probe) and make sure the figure is closed afterwards."""
    made = []
    yield lambda samples: made.append(plot_selection_panes(samples)) or made[-1]
    for figure, *_ in made:
        plt.close(figure)


def test_stacks_power_over_the_probe_on_one_time_axis(panes):
    _, power, probe = panes(SAMPLES)
    assert probe in power.get_shared_x_axes().get_siblings(power)
    assert power.get_ylabel() == "Q_abs (W)"


def test_plots_net_power_for_the_baseline_choice(panes):
    _, power, _ = panes(SAMPLES)
    assert list(power.lines[0].get_ydata()) == [0.0, 1.0, 2.0, 3.0]


def test_falls_back_to_the_plate_when_there_is_no_probe_data(panes):
    _, _, probe = panes(SAMPLES)
    assert list(probe.lines[0].get_ydata()) == [25.0, 24.0, 23.0, 22.0]
    assert "no master probe data" in probe.get_ylabel()


def test_plots_the_probe_once_it_reports(panes):
    samples = [dict(row, **{"Master temperature (C)": 5.0 + i}) for i, row in enumerate(SAMPLES)]
    _, _, probe = panes(samples)
    assert list(probe.lines[0].get_ydata()) == [5.0, 6.0, 7.0, 8.0]
    assert probe.get_ylabel() == "Master probe (C)"


def test_tells_the_operator_which_zone_goes_where(panes):
    _, power, probe = panes(SAMPLES)
    assert "BASELINE" in power.get_title() and "EXPERIMENT" in probe.get_title()
