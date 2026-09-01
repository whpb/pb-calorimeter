import matplotlib.pyplot as plt
import pytest
from matplotlib.backend_bases import FigureCanvasBase

from functions import select_windows as module

SAMPLES = [{"Elapsed (min)": i / 10, "Q_abs (W)": float(i), "Plate temperature (C)": 25.0,
            "Master temperature (C)": None} for i in range(9)]


@pytest.fixture
def window(monkeypatch):
    """Run the selector without ever showing a window, and capture the timer it installs."""
    timers = []
    monkeypatch.setattr(module.plt, "show", lambda: None)
    original = FigureCanvasBase.new_timer

    def capture(canvas, *args, **kwargs):
        timer = original(canvas, *args, **kwargs)
        timers.append(timer)
        return timer

    monkeypatch.setattr(FigureCanvasBase, "new_timer", capture)
    yield timers
    plt.close("all")


def test_returns_a_zone_for_each_pane(window):
    chosen = module.select_windows(SAMPLES, lambda: None)
    assert set(chosen) == {"baseline", "experiment"}


def test_defaults_span_the_whole_run_so_accepting_blind_still_works(window):
    chosen = module.select_windows(SAMPLES, lambda: None)
    assert chosen["baseline"][0] == 0.0
    assert chosen["experiment"][1] == SAMPLES[-1]["Elapsed (min)"]
    assert chosen["baseline"][1] == chosen["experiment"][0]  # they meet, leaving no gap


def test_a_drag_on_a_pane_replaces_that_zone(window, monkeypatch):
    """The SpanSelector callback is the only route from mouse to result, so drive it directly."""
    captured = {}
    monkeypatch.setattr(module, "SpanSelector",
                        lambda axes, onselect, *a, **k: captured.setdefault(len(captured), onselect))
    chosen = module.select_windows(SAMPLES, lambda: None)
    captured[0](0.1, 0.2)
    captured[1](0.5, 0.7)
    assert chosen == {"baseline": (0.1, 0.2), "experiment": (0.5, 0.7)}


def test_keeps_the_rig_alive_while_the_operator_thinks(window):
    beats = []
    module.select_windows(SAMPLES, lambda: beats.append(1))
    assert window, "no timer was installed"
    window[0]._on_timer()
    assert beats == [1]


def test_a_modbus_fault_does_not_kill_the_window(window, capsys):
    def failing():
        raise RuntimeError("connection reset")

    module.select_windows(SAMPLES, failing)
    window[0]._on_timer()
    assert "Keep-alive failed during selection" in capsys.readouterr().out


def test_the_pump_runs_often_enough_to_hold_the_socket(window):
    module.select_windows(SAMPLES, lambda: None)
    assert 0 < module.KEEP_ALIVE_MS <= 10000
