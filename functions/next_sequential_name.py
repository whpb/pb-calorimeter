def next_sequential_name(folder, base):
    """Return the next unused "{base} N" filename stem in folder."""
    n = 1
    while (folder / f"{base} {n}.csv").exists():
        n += 1
    return f"{base} {n}"
