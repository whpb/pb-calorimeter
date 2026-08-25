# Code style
- You are playing the role of an experienced developer with a penchant for precise, minimal code. Every line should be deliberate and justified.
- Limit functions one per file, and a maximum of 30 lines.

# File structure
- The program will be run from main.py, which should contain only logic. Functions live in functions/.

# No-gos
- Do not update README.md. If there is a discrepancy between the information provided in README.md and the functionality of the code, correct the code.

# Hardware & MODBUS notes
- Two Eurotherm nanodac controllers (nanodac1, nanodac2), MODBUS TCP on port 502. `functions/connect_controllers.py` opens one persistent `ModbusTcpClient` per controller at startup.
- Every read/write MUST pass `device_id=255` (see `UNIT_ID` in `functions/read_register.py`, reused by `write_register.py`). Without it the nanodacs accept the TCP connection but never reply — this is not a gateway setup, 255 is just the unit ID iTools itself uses. Confirmed via hours of debugging; don't reintroduce the pymodbus default of 1.
- Registers are plain signed 16-bit integers (`DATATYPE.INT16`, `count=1`) — NOT 32-bit floats. Pressure registers are raw millibar with no scaling factor; readings above ~32767mbar wrap negative (two's-complement overflow), which is expected, not a bug.
- Pressure sensors sit **upstream** of each valve. Pressure is expected to rise as the operator manually pressurizes; there is no ramp automation yet (`RampControl` register exists in `settings.json` but nothing writes to it — confirmed out of scope for now).
- `test_cracking_pressure` no longer auto-detects cracking; it just polls each pressure channel's raw reading every cycle, prints it with its unit, and logs the last-seen value per channel when the test ends. `functions/detect_crack.py` has been deleted. Deciding "cracked" is currently a manual/visual call by the operator watching the printed readings.
- Pressure entries in `settings.json` are 3-element lists (`[controller, address, unit]`, e.g. `["nanodac1", "264", "mbar"]`) so the display unit travels with each channel; `programmer` entries stay 2-element (`[controller, address]`). `read_register`/`write_register` slice `[:2]` off the front so both shapes work through the same lookup.
- `SolenoidToggle` is one shared register for the whole rig (not per-valve). The writes in `test_cracking_pressure` (`1` at test start, `0` at test end) are currently commented out — solenoid actuation is disabled in code right now, though it was confirmed working on the practice rig when enabled.
- `TempSensor` is readable but not consumed by any function yet; raw value looked consistent with a ×100-scaled °C reading but that's unconfirmed, not implemented anywhere.
- `pyproject.toml` needs `package-mode = false` (this is a script project, not a packaged library) — plain `poetry install` fails otherwise. Requires Python >=3.13.
- Results are saved to one CSV per program run (`resolve_save_path` is called once at startup, not per test), and `save_csv` appends a row per completed test, writing the header only if the file is new. A row's columns are `Timestamp`, `Elapsed (min)`, `Temperature`, then one column per pressure channel.
- `Elapsed (min)` is minutes since `main.py` started (`session_start = time.monotonic()`, captured once at the top of `main.py` and passed into every function, not re-timed per call), not since the individual test began. This matters because `UserInput` can pulse to `1` for just a few seconds at a time — each pulse is one short call to `test_cracking_pressure` (one "measurement"), and several of these make up one physical experiment on the rig; a per-call timer would report each measurement's few-second duration instead of the running total the operator actually cares about.
- `functions/start_console_log.py` mirrors all stdout/stderr for the session to `<results folder>/logs/<timestamp>.log` by swapping `sys.stdout`/`sys.stderr` for a tee object; `functions/stop_console_log.py` restores the originals and closes the file. Started right after `save_path` is resolved and stopped at the very end of `main.py`, so it misses only the "Loading settings..." print at the top (before the save folder, and therefore the logs folder, is known).

# Current status
- Only Function 1 (`test_cracking_pressure`) is implemented. `main.py`'s `FUNCTIONS` dict is the place to register future functions by number.
- Register reads/writes, solenoid actuation, and CSV output were verified end-to-end against the real rig in a practice test — but that verification predates the removal of automatic crack detection and the switch to raw per-channel polling, and predates the solenoid writes being commented out. Re-verify against the rig before trusting the current behavior.
- When verifying MODBUS logic without hardware access, prefer a fake client built on the real `pymodbus.client.mixin.ModbusClientMixin` (for genuine convert_from/to_registers behavior) over pymodbus's actual TCP server simulator — its API (`ModbusSlaveContext` vs `ModbusDeviceContext`, `pymodbus.payload`, etc.) has churned significantly across 3.14/4.0 and isn't worth fighting for a quick check.