"""Stability index calculation across a sequence of fingerprints."""

from __future__ import annotations

from math import sqrt


def stability_index(fingerprints: list[dict]) -> float:
    """Return a stability index for the given fingerprint sequence.

    The index is the population standard deviation of the entropy profile.
    A value close to 0 indicates highly stable entropy across all strings;
    larger values indicate greater structural drift.

    Returns 0.0 when fewer than two fingerprints are provided.
    """
    if len(fingerprints) < 2:
        return 0.0

    entropies = [fp["entropy"] for fp in fingerprints]
    mean = sum(entropies) / len(entropies)
    variance = sum((e - mean) ** 2 for e in entropies) / len(entropies)
    return sqrt(variance)
