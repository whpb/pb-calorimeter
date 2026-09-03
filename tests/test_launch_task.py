import time

from functions import bundled_path as anchor
from functions import launch_task as module

CHATTY = "import time\nfor i in range(3):\n    print(f'line {i}')\n    time.sleep(0.2)\n"


def _mode(tmp_path, monkeypatch, body, name="child"):
    """A stand-in entry point, found the same way the real ones are: by name off the anchor."""
    (tmp_path / f"{name}.py").write_text(body)
    monkeypatch.setattr(anchor, "ROOT", tmp_path)
    return name


def _collect(lines, expected, timeout=15):
    got = []
    deadline = time.monotonic() + timeout
    while len(got) < expected and time.monotonic() < deadline:
        if not lines.empty():
            got.append(lines.get().rstrip())
    return got


def test_streams_the_child_output_onto_the_queue(tmp_path, monkeypatch):
    process, lines = module.launch_task(_mode(tmp_path, monkeypatch, CHATTY))
    assert _collect(lines, 3) == ["line 0", "line 1", "line 2"]
    process.wait()


def test_lines_arrive_while_the_child_is_still_running(tmp_path, monkeypatch):
    """Without -u the child block-buffers and the holding screen stays blank until it exits."""
    process, lines = module.launch_task(_mode(tmp_path, monkeypatch, CHATTY))
    first = _collect(lines, 1)
    assert first == ["line 0"]
    assert process.poll() is None  # still going, so this was not a post-mortem flush
    process.terminate()


def test_stderr_is_folded_in_so_tracebacks_are_visible(tmp_path, monkeypatch):
    body = "import sys\nprint('to stderr', file=sys.stderr)\n"
    process, lines = module.launch_task(_mode(tmp_path, monkeypatch, body))
    assert _collect(lines, 1) == ["to stderr"]
    process.wait()


def test_passes_arguments_through(tmp_path, monkeypatch):
    body = "import sys\nprint('got', sys.argv[1])\n"
    process, lines = module.launch_task(_mode(tmp_path, monkeypatch, body), ["a-file.csv"])
    assert _collect(lines, 1) == ["got a-file.csv"]
    process.wait()


def test_terminating_leaves_what_the_child_already_wrote(tmp_path, monkeypatch):
    """Backing out of testing mode must keep the partial results, not roll them back."""
    body = ("import pathlib, time\n"
            "pathlib.Path(r'%s').write_text('partial')\n"
            "print('written')\ntime.sleep(30)\n" % (tmp_path / "results.csv"))
    process, lines = module.launch_task(_mode(tmp_path, monkeypatch, body))
    assert _collect(lines, 1) == ["written"]
    process.terminate()
    process.wait()
    assert (tmp_path / "results.csv").read_text() == "partial"


def test_from_source_it_runs_the_script_unbuffered(tmp_path, monkeypatch):
    """-u is load-bearing, and only the source path can be given it."""
    captured = {}
    monkeypatch.setattr(module.subprocess, "Popen", lambda command, **kw: captured.update(
        command=command, kw=kw) or _Dummy())
    module.launch_task("force_run", ["sentinel", "Copper block"])
    assert captured["command"][1] == "-u"
    assert captured["command"][2].endswith("force_run.py")
    assert captured["command"][3:] == ["sentinel", "Copper block"]


def test_compiled_it_relaunches_the_exe_with_a_mode(tmp_path, monkeypatch):
    """There is no force_run.py in a dist folder, so the exe dispatches to itself instead."""
    captured = {}
    monkeypatch.setattr(module, "FROZEN", True)
    monkeypatch.setattr(module.subprocess, "Popen", lambda command, **kw: captured.update(
        command=command) or _Dummy())
    module.launch_task("force_run", ["sentinel", "Copper block"])
    assert captured["command"][1:] == ["--run", "force_run", "sentinel", "Copper block"]


class _Dummy:
    """Enough of a Popen for launch_task to start its reader thread against."""
    stdout = ()
