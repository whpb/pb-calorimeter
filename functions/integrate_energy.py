def integrate_energy(samples, baseline, plate_baseline, master_baseline, windows):
    """Fill the derived columns, tag each sample's zone, and return the experiment energy."""
    baseline_start, baseline_end = windows["baseline"]
    start, end = windows["experiment"]
    energy, previous = 0.0, None
    for row in samples:
        minutes, probe = row["Elapsed (min)"], row["Master temperature (C)"]
        row["Q_relative (W)"] = round(row["Q_abs (W)"] - baseline, 4)
        row["Plate temperature change (C)"] = round(row["Plate temperature (C)"] - plate_baseline, 3)
        # blank while the probe has no address configured, rather than a misleading zero
        row["Master temperature change (C)"] = None if master_baseline is None or probe is None \
            else round(probe - master_baseline, 3)
        inside = start <= minutes <= end
        if inside:
            # measured interval, so a skipped sample integrates as a zero-order hold
            step = 0.0 if previous is None else (minutes - previous) * 60
            energy += row["Q_relative (W)"] * step
            previous = minutes
        row["Energy (J)"] = round(energy, 1) if inside else None
        # the zones may overlap; the experiment wins, since that is what the energy describes
        row["Zone"] = "experiment" if inside else (
            "baseline" if baseline_start <= minutes <= baseline_end else "")
    return energy
