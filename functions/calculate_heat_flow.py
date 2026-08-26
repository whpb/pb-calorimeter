from functions.read_register import read_register
from functions.interpolate_cooling_power import interpolate_cooling_power


def calculate_heat_flow(clients, settings, curve):
    """Sample the plate and return (temperature, heater utilisation, net heat flow in watts)."""
    heater_power = settings["HeaterPower"]
    temperature = read_register(clients, settings, "programmer", "PlateTemp", float=True)
    utilisation = read_register(clients, settings, "programmer", "HeaterUtil", float=True)
    cooling = interpolate_cooling_power(temperature, curve, heater_power)
    # the gap between the heater output an unloaded plate would need here and what it actually
    # uses is the heat an external source is supplying; zero when nothing is on the plate
    return temperature, utilisation, cooling - heater_power * utilisation / 100
