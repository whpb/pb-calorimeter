import matplotlib.pyplot as plt
import pytest

from functions import plot_work_curve as module

HISTORY = [(0.0, 0.0, 0.0), (1.0, 19.3, -0.5), (2.0, 18.0, -1.25)]


@pytest.fixture
def figure(monkeypatch):
    """Intercept the figure before plot_work_curve closes it, so it can be inspected."""
    captured, close = [], module.plt.close
    monkeypatch.setattr(module.plt, "close", captured.append)
    yield captured
    # close through the saved original: the patch is still in place during teardown
    for fig in captured:
        close(fig)


def test_writes_a_png_beside_the_results_csv(tmp_path):
    path = module.plot_work_curve(HISTORY, tmp_path / "results.csv")
    assert path == tmp_path / "results.png" and path.exists()


def test_uses_the_agg_backend():
    """The rig PC is headless, so importing pyplot must never need a display."""
    assert plt.get_backend().lower() == "agg"


def test_draws_both_series(figure, tmp_path):
    module.plot_work_curve(HISTORY, tmp_path / "results.csv")
    power, temperature = (axes.lines[-1] for axes in figure[0].axes)
    assert list(power.get_ydata()) == [row[1] for row in HISTORY]
    assert list(temperature.get_ydata()) == [row[2] for row in HISTORY]


def test_shares_one_x_axis_between_the_series(figure, tmp_path):
    module.plot_work_curve(HISTORY, tmp_path / "results.csv")
    power_axes, temperature_axes = figure[0].axes
    assert temperature_axes in power_axes.get_shared_x_axes().get_siblings(power_axes)
    assert power_axes.get_xlim() == temperature_axes.get_xlim()


def test_gives_each_series_its_own_y_scale(figure, tmp_path):
    """Watts and degrees are not comparable, so a shared y-scale would flatten one trace."""
    module.plot_work_curve(HISTORY, tmp_path / "results.csv")
    power_axes, temperature_axes = figure[0].axes
    assert temperature_axes not in power_axes.get_shared_y_axes().get_siblings(power_axes)
    assert "W" in power_axes.get_ylabel() and "C" in temperature_axes.get_ylabel()


def test_labels_both_series_in_one_legend(figure, tmp_path):
    module.plot_work_curve(HISTORY, tmp_path / "results.csv")
    labels = [text.get_text() for text in figure[0].axes[0].get_legend().get_texts()]
    assert len(labels) == 2 and any("W" in label for label in labels)


def test_handles_a_single_sample(tmp_path):
    assert module.plot_work_curve([(0.0, 0.0, 0.0)], tmp_path / "results.csv").exists()
