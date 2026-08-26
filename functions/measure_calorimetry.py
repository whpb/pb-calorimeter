import time
from datetime import datetime

from functions.load_cooling_curve import load_cooling_curve
from functions.calculate_heat_flow import calculate_heat_flow
from functions.check_baseline import check_baseline
from functions.generate_report import generate_report
from functions.measure_baseline import measure_baseline
from functions.read_register import read_register
from functions.save_csv import save_csv

TIME_STEP_S = 1.0


def measure_calorimetry(clients, settings, save_path):
    """Integrate the plate's heat flow against its unloaded baseline until UserInput leaves 1."""
    curve = load_cooling_curve()
    baseline_temperature, baseline_utilisation, baseline = measure_baseline(clients, settings, curve, TIME_STEP_S)
    check_baseline(baseline_temperature, baseline_utilisation, baseline)
    history, energy = [], 0.0
    start = last = time.monotonic()  # t=0 is the end of baselining, not the start of the session
    while read_register(clients, settings, "programmer", "UserInput") == 1:
        time.sleep(TIME_STEP_S)
        try:
            temperature, utilisation, q_abs = calculate_heat_flow(clients, settings, curve)
        except Exception as e:
            print(f"Sample skipped, integrating through it: {e}")
            continue
        now = time.monotonic()
        step, last = now - last, now  # measured, not nominal: a slow read must not skew the integral
        q_relative = q_abs - baseline
        energy += q_relative * step
        elapsed = (now - start) / 60
        history.append((elapsed, q_relative, temperature - baseline_temperature))
        save_csv({
            "Timestamp": datetime.now().isoformat(timespec="seconds"),
            "Elapsed (min)": round(elapsed, 3),
            "Plate temperature (C)": round(temperature, 2),
            "Heater utilisation (%)": round(utilisation, 2),
            "Q_abs (W)": round(q_abs, 3),
            "Q_relative (W)": round(q_relative, 3),
            "Energy (J)": round(energy, 1),
        }, save_path, quiet=True)
    generate_report(history, energy, baseline, save_path)
