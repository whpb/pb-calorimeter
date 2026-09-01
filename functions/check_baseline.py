COLD_LIMIT_C = -29.0
BASELINE_WARN_W = 10.0
SPREAD_WARN_W = 5.0


def check_baseline(temperature, baseline, spread):
    """Print the selected baseline zone and warn the operator if it looks unreliable."""
    print(f"Baseline: {temperature:.2f} C plate, Q_abs = {baseline:.2f} W, spread {spread:.2f} W")
    if temperature < COLD_LIMIT_C:
        print(f"  WARNING: below {COLD_LIMIT_C} C the cooling curve is flat and non-monotonic, so a "
              "1 C reading error costs about 3 W. Consider a warmer control temperature.")
    if abs(baseline) > BASELINE_WARN_W:
        print(f"  WARNING: baseline Q_abs exceeds {BASELINE_WARN_W} W. Q_relative stays valid, but the "
              "curve may no longer describe this machine; consider recalibrating it.")
    if spread > SPREAD_WARN_W:
        print(f"  WARNING: Q_abs varies by {spread:.2f} W across the chosen zone. Re-cut it over whole "
              "cycles of the 90-120 s swing, or the mean will not sit at the centre of the noise.")
