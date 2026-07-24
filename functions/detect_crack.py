MIN_PRESSURE = 50  # mbar; peaks below this are idle noise, not a real pressurization event
NOISE_MARGIN = 10  # mbar; ignore small fluctuations while checking for a plateau
PLATEAU_POLLS = 4  # consecutive non-rising polls (2s @ 0.5s/poll) before calling a peak a crack


def detect_crack(value, state):
    """Track a channel's rising peak; report True once it plateaus above MIN_PRESSURE (cracked)."""
    if value > state["peak"] + NOISE_MARGIN:
        state["peak"] = value
        state["stall"] = 0
        return False
    state["stall"] += 1
    return state["stall"] >= PLATEAU_POLLS and state["peak"] > MIN_PRESSURE
