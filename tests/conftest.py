import sys
import time

import matplotlib

matplotlib.use("Agg")  # the suite must never open a window

import pytest
from pymodbus.client.mixin import ModbusClientMixin

DATATYPE = ModbusClientMixin.DATATYPE


class FakeResult:
    """Stand-in for a pymodbus response, error or otherwise."""

    def __init__(self, registers=(), error=False):
        self.registers = list(registers)
        self._error = error

    def isError(self):
        return self._error


class FakeClient:
    """Records every call a function makes, and replays canned register values."""

    convert_from_registers = staticmethod(ModbusClientMixin.convert_from_registers)

    def __init__(self, values=None, error=False):
        # {address: (value, datatype)}, encoded on read so decoding is genuinely exercised
        self.values = values or {}
        self.error = error
        self.reads, self.writes, self.closed = [], [], False

    def read_holding_registers(self, address, count=1, device_id=None):
        self.reads.append((address, count, device_id))
        if self.error:
            return FakeResult(error=True)
        value, datatype = self.values.get(address, (0, DATATYPE.INT16))
        return FakeResult(ModbusClientMixin.convert_to_registers(value, datatype))

    def write_register(self, address, value, device_id=None):
        self.writes.append((address, value, device_id))
        return FakeResult(error=self.error)

    def connect(self):
        return not self.error

    def close(self):
        self.closed = True


class ScriptedClient(FakeClient):
    """Replays (plate C, heater %[, master C]) samples; None stages a MODBUS fault."""

    USER_INPUT, PLATE_TEMP, HEATER_UTIL, MASTER_TEMP = 14954, 33280, 43874, 40000

    def __init__(self, samples, user_input=None):
        super().__init__()
        self.samples, self.index, self.current = samples, 0, None
        # by default the run ends once the script is exhausted
        self.user_input = user_input or (lambda: 1 if self.index < len(self.samples) else 0)

    def read_holding_registers(self, address, count=1, device_id=None):
        self.reads.append((address, count, device_id))
        if address == self.USER_INPUT:
            return self._encode(self.user_input(), DATATYPE.INT16)
        if address == self.MASTER_TEMP:
            return self._sample(2, DATATYPE.FLOAT32)
        if address == self.PLATE_TEMP:
            self.current = self.samples[min(self.index, len(self.samples) - 1)]
            self.index += 1
            return self._sample(0, DATATYPE.FLOAT32)
        return self._sample(1, DATATYPE.FLOAT32)

    def _sample(self, field, datatype):
        if self.current is None:
            return FakeResult(error=True)
        return self._encode(self.current[field], datatype)

    @staticmethod
    def _encode(value, datatype):
        return FakeResult(ModbusClientMixin.convert_to_registers(value, datatype))


class Clock:
    """A fake clock that only sleep advances, so a skipped sample still costs its time step."""

    def __init__(self):
        self.now = 0.0

    def sleep(self, seconds):
        self.now += seconds

    def monotonic(self):
        return self.now


@pytest.fixture
def tk_root():
    """A withdrawn Tk root: widgets can be built and inspected, but nothing is ever drawn."""
    tkinter = pytest.importorskip("tkinter")
    root = tkinter.Tk()
    root.withdraw()
    yield root
    root.destroy()


@pytest.fixture
def backdrop():
    """A flat stand-in for the window's photograph: the builders only ever crop from it."""
    Image = pytest.importorskip("PIL.Image")
    from functions import tokens

    return Image.new("RGB", (tokens.WIDTH, tokens.HEIGHT), tokens.CANVAS)


@pytest.fixture
def canvas(tk_root):
    """The canvas every screen is built on: the cards are drawn into it, not placed over it."""
    tkinter = pytest.importorskip("tkinter")
    from functions import tokens

    return tkinter.Canvas(tk_root, width=tokens.WIDTH, height=tokens.HEIGHT)


def descendants(widget):
    """Every widget under this one. The screens nest content inside drawn cards."""
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def drawn(widget):
    """The drawn buttons and rows under a widget, in layout order, by their .invoke handle."""
    return [w for w in descendants(widget) if hasattr(w, "invoke")]


def text_of(widget):
    """Every piece of text under a widget, wherever in the nesting it sits."""
    return [w.cget("text") for w in descendants(widget) if "text" in w.keys()]


def find(widget, needle):
    """The one drawn button or row whose own text, or a label inside it, contains `needle`."""
    matches = [w for w in drawn(widget)
               if any(needle in text for text in [*text_of(w),
                                                  *([w.cget("text")] if "text" in w.keys() else [])])]
    assert len(matches) == 1, f"{needle!r} matched {len(matches)} controls"
    return matches[0]


def packed_height(frame):
    """How tall the children packed into a frame actually come to, padding included.

    The panels are a fixed size, so anything over the frame's own height is clipped away
    rather than scrolled - which is a layout bug, and one only arithmetic will catch.
    """
    total = 0
    for child in frame.winfo_children():
        pady = child.pack_info()["pady"]
        total += child.winfo_reqheight() + (sum(int(v) for v in pady)
                                            if isinstance(pady, tuple) else 2 * int(pady))
    return total


def canvas_text(canvas):
    """The text of every item drawn straight onto a canvas, which is where headings live."""
    return [canvas.itemcget(item, "text") for item in canvas.find_all()
            if canvas.type(item) == "text"]


@pytest.fixture
def clock(monkeypatch):
    """Run time-driven loops instantly, with every interval exactly as long as it claims."""
    fake = Clock()
    monkeypatch.setattr(time, "sleep", fake.sleep)
    monkeypatch.setattr(time, "monotonic", fake.monotonic)
    return fake


@pytest.fixture(autouse=True)
def restore_streams():
    """A failed console-log test must not leave the rest of the suite writing to a Tee."""
    original = sys.stdout, sys.stderr
    yield
    sys.stdout, sys.stderr = original


@pytest.fixture
def settings():
    """Minimal settings mirroring the real rig: one controller, three registers."""
    return {
        "addresses": {
            "controllers": {"pb1": "192.168.111.222:502"},
            "modbus": {
                "programmer": {
                    "UserInput": ["pb1", "14954"],
                    "PlateTemp": ["pb1", "33280"],
                    "HeaterUtil": ["pb1", "43874"],
                    "MasterTemp": ["pb1", None],
                }
            },
        },
        "SavePath": "auto",
        "FileName": "auto",
        "HeaterPower": 193,
    }


@pytest.fixture
def client():
    return FakeClient({
        14954: (1, DATATYPE.INT16),
        33280: (25.0, DATATYPE.FLOAT32),
        43874: (40.0, DATATYPE.FLOAT32),
    })


@pytest.fixture
def clients(client):
    return {"pb1": client}


@pytest.fixture
def curve():
    """A deliberately simple curve: 1 C per %, so expected watts are easy to reason about."""
    return ([0.0, 10.0, 20.0, 30.0], [0.0, 10.0, 20.0, 30.0])
