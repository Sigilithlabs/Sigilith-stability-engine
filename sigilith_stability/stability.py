"""Stability index computation across a sequence of fingerprints."""

import math
from typing import List

from .fingerprint import Fingerprint


def _population_cv(values: List[float]) -> float:
    """Return the coefficient of variation (population std / mean) for *values*.

    Returns 0.0 when the mean is zero or fewer than two values are supplied.
    """
    n = len(values)
    if n < 2:
        return 0.0
    mean = sum(values) / n
    if mean == 0.0:
        return 0.0
    variance = sum((v - mean) ** 2 for v in values) / n
    return math.sqrt(variance) / mean


def stability_index(fingerprints: List[Fingerprint]) -> float:
    """Return the stability index for a sequence of fingerprints.

    The index is the mean coefficient of variation (population std / mean)
    computed independently for each fingerprint feature (length,
    unique_chars, unique_bigrams, entropy).  A lower value indicates a more
    structurally consistent set of inputs; a higher value indicates greater
    drift.
    """
    if len(fingerprints) < 2:
        return 0.0

    feature_series: List[List[float]] = [
        [float(fp.length) for fp in fingerprints],
        [float(fp.unique_chars) for fp in fingerprints],
        [float(fp.unique_bigrams) for fp in fingerprints],
        [fp.entropy for fp in fingerprints],
    ]

    cvs = [_population_cv(series) for series in feature_series]
    return sum(cvs) / len(cvs)
