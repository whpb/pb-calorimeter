from pathlib import Path


def stop_requested(sentinel):
    """True once the interface has asked a forced run to stop and produce its report."""
    return Path(sentinel).exists()
