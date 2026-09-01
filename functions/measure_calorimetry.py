from functions.load_cooling_curve import load_cooling_curve
from functions.read_register import read_register
from functions.record_samples import record_samples


def measure_calorimetry(clients, settings, save_path):
    """Record a User Value 1 run to CSV and stop there, leaving the zones to be picked later."""
    curve = load_cooling_curve()
    samples = record_samples(clients, settings, curve, save_path,
                             lambda: read_register(clients, settings, "programmer", "UserInput") == 1)
    if not samples:
        print("No samples recorded.")
        return
    # deliberately no zone selection: this mode runs unattended, and a blocking
    # selection window would sit there until someone came back to the machine
    print(f"Recorded {len(samples)} samples to {save_path.name}. "
          "Re-analyse it at the machine to pick zones and produce a report.")
