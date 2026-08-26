COLD_LIMIT_C = -29.0
BASELINE_WARN_W = 10.0


def check_baseline(temperature, utilisation, baseline):
    """Print the baseline sample and warn the operator if it looks unreliable."""
    print(f"Baseline: {temperature:.2f} C plate, {utilisation:.2f} % heater, Q_abs = {baseline:.2f} W")
    if temperature < COLD_LIMIT_C:
        print(f"  WARNING: below {COLD_LIMIT_C} C the cooling curve is flat and non-monotonic, so a "
              "1 C reading error costs about 3 W. Consider a warmer control temperature.")
    if abs(baseline) > BASELINE_WARN_W:
        print(f"  WARNING: baseline Q_abs exceeds {BASELINE_WARN_W} W. Q_relative stays valid, but the "
              "curve may no longer describe this machine; consider recalibrating it.")
