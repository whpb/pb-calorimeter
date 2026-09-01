from tkinter import ttk

from functions.build_progress import build_progress


def test_hands_back_the_pieces_the_caller_updates(tk_root):
    widgets = build_progress(tk_root, "Testing mode", lambda: None)
    assert set(widgets) == {"frame", "status", "log"}


def test_shows_the_heading_it_was_given(tk_root):
    widgets = build_progress(tk_root, "Re-analysis", lambda: None)
    headings = [w.cget("text") for w in widgets["frame"].winfo_children() if isinstance(w, ttk.Label)]
    assert "Re-analysis" in headings


def test_the_bar_is_animating(tk_root):
    """Indeterminate: there is no total to count towards, only a sign of life."""
    widgets = build_progress(tk_root, "Testing mode", lambda: None)
    bar = [w for w in widgets["frame"].winfo_children() if isinstance(w, ttk.Progressbar)][0]
    assert str(bar.cget("mode")) == "indeterminate"  # Tk 9 returns a Tcl object, not a str


def test_the_log_accepts_lines(tk_root):
    widgets = build_progress(tk_root, "Testing mode", lambda: None)
    widgets["log"].insert("end", "Loaded 720 samples\n")
    assert "Loaded 720 samples" in widgets["log"].get("1.0", "end")


def _buttons(widgets):
    row = [w for w in widgets["frame"].winfo_children() if isinstance(w, ttk.Frame)][-1]
    return [w for w in row.winfo_children() if isinstance(w, ttk.Button)]


def test_the_back_button_says_it_ends_the_run(tk_root):
    pressed = []
    widgets = build_progress(tk_root, "Testing mode", lambda: pressed.append(1))
    button = _buttons(widgets)[0]
    assert "ends the run" in button.cget("text")
    button.invoke()
    assert pressed == [1]


def test_only_a_forced_run_offers_a_graceful_stop(tk_root):
    """Testing mode ends at the nanodac, so a Stop button there would be a lie."""
    waiting = build_progress(tk_root, "Testing mode", lambda: None)
    forced = build_progress(tk_root, "Force run", lambda: None, lambda: None)
    assert [b.cget("text") for b in _buttons(waiting)] == ["Back to menu  (ends the run)"]
    assert "Stop and analyse" in [b.cget("text") for b in _buttons(forced)]


def test_the_stop_button_reports_the_press(tk_root):
    pressed = []
    widgets = build_progress(tk_root, "Force run", lambda: None, lambda: pressed.append(1))
    _buttons(widgets)[0].invoke()
    assert pressed == [1]
