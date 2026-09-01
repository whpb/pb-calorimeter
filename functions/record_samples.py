import time
from datetime import datetime

from functions.calculate_heat_flow import calculate_heat_flow
from functions.read_register import read_register
from functions.save_csv import save_csv

TIME_STEP_S = 1.0


def record_samples(clients, settings, curve, save_path):
    """Sample the plate every TIME_STEP_S until UserInput leaves 1, appending each row as it lands."""
    probe = settings["addresses"]["modbus"]["programmer"]["MasterTemp"][1] is not None
    samples, start = [], time.monotonic()
    while read_register(clients, settings, "programmer", "UserInput") == 1:
        time.sleep(TIME_STEP_S)
        try:
            temperature, utilisation, q_abs = calculate_heat_flow(clients, settings, curve)
            # assumed FLOAT32 like the other pb1 channels; None until the address is configured
            master = read_register(clients, settings, "programmer", "MasterTemp", float=True) if probe else None
        except Exception as e:
            print(f"Sample skipped: {e}")
            continue
        row = {
            "Timestamp": datetime.now().isoformat(timespec="seconds"),
            "Elapsed (min)": round((time.monotonic() - start) / 60, 4),
            "Plate temperature (C)": round(temperature, 3),
            "Master temperature (C)": None if master is None else round(master, 3),
            "Heater utilisation (%)": round(utilisation, 3),
            "Q_abs (W)": round(q_abs, 4),
        }
        samples.append(row)
        save_csv(row, save_path, quiet=True)
    return samples
