from bisect import bisect_left


def interpolate_cooling_power(temperature, curve, heater_power):
    """Return the machine's cooling power in watts at the given plate temperature."""
    temps, outputs = curve
    if temperature <= temps[0]:
        output = outputs[0]
    elif temperature >= temps[-1]:
        output = outputs[-1]
    else:
        i = bisect_left(temps, temperature)
        span = temps[i] - temps[i - 1]
        fraction = (temperature - temps[i - 1]) / span if span else 0.0
        output = outputs[i - 1] + fraction * (outputs[i] - outputs[i - 1])
    # each sweep point is an equilibrium, so its heating output is the cooling power there
    return heater_power * output / 100
