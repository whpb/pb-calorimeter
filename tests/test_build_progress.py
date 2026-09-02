from tkinter import ttk

from conftest import canvas_text, descendants, drawn, find

from functions.build_progress import build_progress


def test_hands_back_the_pieces_the_caller_updates(tk_root, backdrop):
    widgets = build_progress(tk_root, backdrop, "Testing mode", lambda: None)
    assert set(widgets) == {"frame", "status", "log"}


def test_shows_the_heading_it_was_given(tk_root, backdrop):
    widgets = build_progress(tk_root, backdrop, "Re-analysis", lambda: None)
    assert "Re-analysis" in canvas_text(widgets["frame"])


def test_the_bar_is_animating(tk_root, backdrop):
    """Indeterminate: there is no total to count towards, only a sign of life."""
    widgets = build_progress(tk_root, backdrop, "Testing mode", lambda: None)
    bar = [w for w in descendants(widgets["frame"]) if isinstance(w, ttk.Progressbar)][0]
    assert str(bar.cget("mode")) == "indeterminate"  # Tk 9 returns a Tcl object, not a str


def test_the_log_accepts_lines(tk_root, backdrop):
    widgets = build_progress(tk_root, backdrop, "Testing mode", lambda: None)
    widgets["log"].insert("end", "Loaded 720 samples\n")
    assert "Loaded 720 samples" in widgets["log"].get("1.0", "end")


def test_the_back_button_says_it_ends_the_run(tk_root, backdrop):
    pressed = []
    widgets = build_progress(tk_root, backdrop, "Testing mode", lambda: pressed.append(1))
    find(widgets["frame"], "ends the run").invoke()
    assert pressed == [1]


def test_only_a_forced_run_offers_a_graceful_stop(tk_root, backdrop):
    """Testing mode ends at the nanodac, so a Stop button there would be a lie."""
    waiting = build_progress(tk_root, backdrop, "Testing mode", lambda: None)
    forced = build_progress(tk_root, backdrop, "Force run", lambda: None, lambda: None)
    assert len(drawn(waiting["frame"])) == 1
    assert [w.cget("text") for w in drawn(forced["frame"])] == [
        "Back to menu  (ends the run)", "Stop and analyse"]


def test_the_stop_button_reports_the_press(tk_root, backdrop):
    pressed = []
    widgets = build_progress(tk_root, backdrop, "Force run", lambda: None,
                             lambda: pressed.append(1))
    find(widgets["frame"], "Stop and analyse").invoke()
    assert pressed == [1]
