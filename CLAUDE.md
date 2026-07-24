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
- "Cracking" = the upstream reading stops rising (plateaus), not a fixed threshold crossing. Detection lives in `functions/detect_crack.py`: tracks each channel's rising peak, calls it cracked once the reading stays within `NOISE_MARGIN` of that peak for `PLATEAU_POLLS` consecutive polls, provided the peak clears the `MIN_PRESSURE` noise floor. All three constants are first-guess defaults from one practice run — expect to retune after watching more real tests.
- `SolenoidToggle` is one shared register for the whole rig (not per-valve): `test_cracking_pressure` writes `1` at test start and `0` at test end. Confirmed working on the practice rig.
- `TempSensor` is readable but not consumed by any function yet; raw value looked consistent with a ×100-scaled °C reading but that's unconfirmed, not implemented anywhere.
- `pyproject.toml` needs `package-mode = false` (this is a script project, not a packaged library) — plain `poetry install` fails otherwise. Requires Python >=3.13.

# Current status
- Only Function 1 (`test_cracking_pressure`) is implemented. `main.py`'s `FUNCTIONS` dict is the place to register future functions by number.
- Verified end-to-end against the real rig (register reads/writes, crack detection, solenoid actuation, CSV output all confirmed working in a practice test).
- When verifying MODBUS logic without hardware access, prefer a fake client built on the real `pymodbus.client.mixin.ModbusClientMixin` (for genuine convert_from/to_registers behavior) over pymodbus's actual TCP server simulator — its API (`ModbusSlaveContext` vs `ModbusDeviceContext`, `pymodbus.payload`, etc.) has churned significantly across 3.14/4.0 and isn't worth fighting for a quick check.