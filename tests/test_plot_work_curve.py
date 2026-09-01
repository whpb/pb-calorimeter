import matplotlib.pyplot as plt
import pytest

from functions import plot_work_curve as module

SAMPLES = [{"Elapsed (min)": i / 10, "Q_relative (W)": float(i),
            "Plate temperature change (C)": -0.5 * i} for i in range(6)]
WINDOWS = {"baseline": (0.0, 0.2), "experiment": (0.3, 0.5)}


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
    path = module.plot_work_curve(SAMPLES, WINDOWS, tmp_path / "results.csv")
    assert path == tmp_path / "results.png" and path.exists()


def test_draws_both_series(figure, tmp_path):
    module.plot_work_curve(SAMPLES, WINDOWS, tmp_path / "results.csv")
    power, temperature = (axes.lines[-1] for axes in figure[0].axes)
    assert list(power.get_ydata()) == [row["Q_relative (W)"] for row in SAMPLES]
    assert list(temperature.get_ydata()) == [row["Plate temperature change (C)"] for row in SAMPLES]


def test_shares_one_x_axis_between_the_series(figure, tmp_path):
    module.plot_work_curve(SAMPLES, WINDOWS, tmp_path / "results.csv")
    power_axes, temperature_axes = figure[0].axes
    assert temperature_axes in power_axes.get_shared_x_axes().get_siblings(power_axes)
    assert power_axes.get_xlim() == temperature_axes.get_xlim()


def test_gives_each_series_its_own_y_scale(figure, tmp_path):
    """Watts and degrees are not comparable, so a shared y-scale would flatten one trace."""
    module.plot_work_curve(SAMPLES, WINDOWS, tmp_path / "results.csv")
    power_axes, temperature_axes = figure[0].axes
    assert temperature_axes not in power_axes.get_shared_y_axes().get_siblings(power_axes)
    assert "W" in power_axes.get_ylabel() and "C" in temperature_axes.get_ylabel()


def test_shades_both_selected_zones(figure, tmp_path):
    """The report has to show which slices of the run the numbers actually came from."""
    module.plot_work_curve(SAMPLES, WINDOWS, tmp_path / "results.csv")
    spans = [(patch.get_x(), patch.get_x() + patch.get_width())
             for patch in figure[0].axes[0].patches]
    assert spans == [WINDOWS["baseline"], WINDOWS["experiment"]]


def test_names_the_zones_in_the_legend(figure, tmp_path):
    module.plot_work_curve(SAMPLES, WINDOWS, tmp_path / "results.csv")
    labels = [text.get_text() for text in figure[0].axes[0].get_legend().get_texts()]
    assert "baseline zone" in labels and "experiment zone" in labels
    assert len(labels) == 4


def test_handles_a_single_sample(tmp_path):
    assert module.plot_work_curve(SAMPLES[:1], WINDOWS, tmp_path / "results.csv").exists()
