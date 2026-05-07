"""Stability index computation across a sequence of fingerprints."""

import math


def compute_stability_index(fingerprints: list) -> float:
    """Return the stability index for a sequence of fingerprints.

    The index is the population standard deviation of the entropy values across
    all fingerprints.  A value near ``0`` indicates that the inputs are
    structurally uniform; higher values indicate increasing entropy variance
    (i.e. instability).
    """
    if len(fingerprints) < 2:
        return 0.0

    entropies = [fp["entropy"] for fp in fingerprints]
    mean = sum(entropies) / len(entropies)
    variance = sum((e - mean) ** 2 for e in entropies) / len(entropies)
    return math.sqrt(variance)
