# Code style
- You are an experienced developer with a penchant for precise, minimal code. Every line should be deliberate and justified.
- Limit functions one per file, and a maximum of 30 lines.

# File structure
- The program will be run from main.py, which should contain only logic. Functions live in functions/.

# No-gos
- Do not update README.md. If there is a discrepancy between the information provided in README.md and the functionality of the code, correct the code.

# Project origin
- This repo was forked from a sister project ("valve-tests-2") by copying its skeleton, then deleting the valve test itself. Anything that still smells of valves, cracking pressure, or solenoids is leftover, not requirement. Still to be corrected: `pyproject.toml` (`name = "valve-tests-2"`). `Run.bat` hardcodes another machine's path and still says "Valve Tests" — deliberately left alone, because the final installation won't be on this PC; do not fix without being asked.
- Inherited and still correct: MODBUS read/write, settings loading, save-path resolution, sequential naming, CSV appending, console logging, connection keep-alive.

# Hardware & MODBUS notes
- The Polar Bear rig is a single Eurotherm nanodac controller, `pb1`, MODBUS TCP on port 502. `functions/connect_controllers.py` opens one persistent `ModbusTcpClient` per controller at startup and still supports several; the valve rig used two (nanodac1, nanodac2).
- Every read/write MUST pass `device_id=255` (see `UNIT_ID` in `functions/read_register.py`, reused by `write_register.py`). Without it the nanodacs accept the TCP connection but never reply — this is not a gateway setup, 255 is just the unit ID iTools itself uses. Confirmed via hours of debugging; don't reintroduce the pymodbus default of 1.
- Registers are plain signed 16-bit integers (`DATATYPE.INT16`, `count=1`) — NOT 32-bit floats. Values arrive raw and unscaled; anything with a decimal place is a fixed-point integer that must be divided by a per-channel scale factor. INT16 wraps negative above 32767, so a channel's scale must leave headroom for its full range.
- Register entries in `settings.json` are lists whose first two elements are always `[controller, address]`; `read_register`/`write_register` slice `[:2]` off the front, so extra trailing metadata (scale, unit) can be carried per channel without touching them.
- **The Polar Bear is not a nanodac.** It is similar equipment but configured very differently, so nothing learned about register blocks or datatypes on the valve rig's nanodacs carries over to `pb1`. Do not infer `pb1`'s datatypes from the `33xxx`/`43874` address ranges.
- `PlateTemp` (`pb1/33280`) is read as **FLOAT32** — `read_register(..., float=True)`, which already reads `count=2` and converts. Flagged by the user as assumed, not confirmed. `HeaterUtil` (`pb1/43874`) is configured to output 0-100 as a straight percentage of `HeaterPower`. Neither channel needs a scale factor.

# Program behaviour
- `main.py` polls `programmer/UserInput` every 200 ms and dispatches on its value via the `FUNCTIONS` dict. `2` terminates the program. Any unmapped value falls through to `keep_alive`, which reads one register per controller so idle TCP connections aren't dropped.
- Latching is achieved by the dispatched function itself looping while `UserInput` still holds its trigger value and returning once it changes — not by a flag in `main.py`. A function that returns while its trigger is still set would be re-entered immediately.
- The whole poll cycle is wrapped in a bare `except` that prints and continues, so a transient MODBUS fault never kills a running session.
- Results go to one CSV per program run (`resolve_save_path` is called once at startup, not per function call); `save_csv` appends a row and writes the header only if the file is new.
- `Elapsed (min)` is minutes since `main.py` started (`session_start = time.monotonic()`, captured once at the top of `main.py` and passed into every function), not since the individual function call began.
- `functions/start_console_log.py` mirrors all stdout/stderr for the session to `<results folder>/logs/<timestamp>.log` by swapping `sys.stdout`/`sys.stderr` for a tee object; `functions/stop_console_log.py` restores the originals and closes the file. Started right after `save_path` is resolved and stopped at the very end of `main.py`, so it misses only the "Loading settings..." print at the top (before the save folder, and therefore the logs folder, is known).
- `pyproject.toml` needs `package-mode = false` (this is a script project, not a packaged library) — plain `poetry install` fails otherwise. Requires Python >=3.13.

# Calorimetry
- The one function this project exists to provide (README function `1`). It estimates the energy added or removed by a source/sink placed on the Polar Bear's plate, by conservation of energy.
- `pb_cooling_capacity.csv` is **not** a table of watts. Its columns are `Plate Temperature, C` and `Heating Output, %` — a steady-state calibration sweep taken with no load on the plate. At each row the machine is at equilibrium, so the heater output recorded there is exactly the cooling power the machine is producing at that plate temperature. Cooling power in watts is therefore recovered as `Q_cool(T) = HeaterPower * util_curve(T) / 100`, with `HeaterPower` (193 W) from `settings.json`.
- The file has a UTF-8 BOM (read with `encoding="utf-8-sig"`) and CRLF line endings; headers are quoted (`"Plate Temperature C"`, `"Heating Output %"`). Parse with the `csv` module and `newline=""`.
- Rows are ordered by heating output, not temperature, and the cold end is non-monotonic in temperature (-45.89, -46.51, -43.88, ...). Sort by temperature before interpolating.
- The measurement then samples every time step:
  - `Q_cool = HeaterPower * interp(T_plate, curve) / 100` — cooling power at the current plate temperature.
  - `Q_abs = Q_cool - HeaterPower * util_actual / 100`, i.e. `HeaterPower * (util_curve(T_plate) - util_actual) / 100`. The physical meaning: the gap between the heater output the machine *would* need to hold this plate temperature unloaded, and what it is *actually* using, is the heat the external source is supplying. Positive `Q_relative` = energy being added to the plate.
  - `Q_relative = Q_abs - Q_baseline`, where `Q_baseline` is the first `Q_abs` of the run.
- **Why `Q_abs` is ~0 at an unloaded baseline** (this confused the author once; it is not a claim that cooling stops). Both terms of `Q_abs` are large and nonzero at baseline — holding, say, 25 C needs real heater input against real cooling. They are also *equal*, because that is what equilibrium means and exactly what the calibration sweep recorded. Their difference is what goes to zero. `Q_abs` is a net heat balance on the plate, not an absolute cooling power, despite the name: it is the rate at which the plate is gaining heat from everything that is not the machine's own heater and cooler.
- `Q_baseline` is therefore a residual, capturing how far the machine has drifted from its calibration sweep (ambient temperature, condenser fouling, refrigerant charge, interpolation error). Subtracting it cancels that offset at the operating point, so `Q_relative` measures the change caused by the source regardless of how stale the curve is. Print it at run start; beyond roughly +/-10 W (about 5 percentage points of heater output) the curve probably no longer describes the machine and it wants recalibrating — an advisory, not a hard limit.
- Baseline subtraction only cancels the offset at t=0, **not drift during the run**. If ambient temperature moves mid-run, `Q_cool` shifts and the change is misattributed to the source. On long runs this is the dominant error, and it integrates: a 2 W drift over 30 minutes is 3.6 kJ of phantom energy. Keep runs short, or ambient stable, or both.
  - `E_t = E_{t-1} + Q_relative * t_step`.
- All Q values are watts, energy joules, `t_step` seconds. Use the *measured* interval between samples for `t_step`, not the nominal setting — a blocked MODBUS read would otherwise silently corrupt the integral.
- **Conditioning:** above about -29 C the curve is a steady ~2.4-3.2 C per %, so a 1 C temperature error costs only ~0.7 W. Below -39 C it flattens to ~0.6 C per % and goes non-monotonic, so the same error costs ~3 W and the interpolation is ill-defined. Control temperatures should be chosen in the well-conditioned region; warn the operator if the baseline lands in the cold end.
- The curve is a *steady-state* characteristic, so instantaneous `Q_relative` is only valid at thermal equilibrium. During transients the plate's own thermal mass absorbs and releases energy and `Q` will overshoot; the energy integral is the robust number because those transient errors largely cancel once equilibrium returns. Report total energy as the headline figure.
- A run ends when `UserInput` leaves `1`. The function then closes the results file and generates a report: a Q_relative-against-time plot and the total energy change.
- Hardware is now a **single** controller, `pb1`, with `PlateTemp` and `HeaterUtil` alongside `UserInput` under `programmer`. `HeaterUtil` is configured to read 0-100 as a straight percentage. `PlateTemp` cannot be raw INT16 (it must represent values like -45.89), so it carries a fixed-point scale that still needs confirming against the live rig.

# Current status
- `measure_calorimetry` is implemented and wired to `FUNCTIONS = {1: ...}` in `main.py`. Its chain is `load_cooling_curve` -> `calculate_heat_flow` (which calls `interpolate_cooling_power`) -> `check_baseline` -> loop -> `generate_report` -> `plot_work_curve`.
- Verified offline only, against a simulated rig: a 20 W source injected as a heater backing-off of 10.36 % was recovered as 19.99 W of `Q_relative` through a deliberate 7.65 W baseline offset, and interpolation round-trips exactly at every curve knot. **Never yet run against real hardware** — `PlateTemp` as FLOAT32 and `HeaterUtil` as INT16 are both unconfirmed guesses, and a wrong datatype returns obvious garbage rather than a plausible wrong number, so sanity-check the first baseline print.
- `TIME_STEP_S` is a module constant in `measure_calorimetry.py`, deliberately not a `settings.json` entry: the README's settings table lists only `SavePath` and `FileName`, so adding one would create a README discrepancy.
- A sample that raises is skipped with a printed warning and the integral carries straight through it (zero-order hold over the longer gap), so one transient MODBUS fault cannot cost a long run its report.
- `write_register.py` is now unused — nothing in the calorimetry path writes to the rig. Left in place as inherited infrastructure.
