"""Pairwise comparison utilities for structural fingerprints."""

import math
from typing import List, Tuple

from .fingerprint import Fingerprint


def _to_vec(fp: Fingerprint) -> List[float]:
    return [float(fp.length), float(fp.unique_chars), float(fp.unique_bigrams), fp.entropy]


def euclidean_distance(fp1: Fingerprint, fp2: Fingerprint) -> float:
    """Return the Euclidean distance between two fingerprint vectors."""
    v1 = _to_vec(fp1)
    v2 = _to_vec(fp2)
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


def cosine_similarity(fp1: Fingerprint, fp2: Fingerprint) -> float:
    """Return the cosine similarity (0–1) between two fingerprint vectors."""
    v1 = _to_vec(fp1)
    v2 = _to_vec(fp2)
    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a ** 2 for a in v1))
    mag2 = math.sqrt(sum(b ** 2 for b in v2))
    if mag1 == 0.0 or mag2 == 0.0:
        return 0.0
    return dot / (mag1 * mag2)


def pairwise_distances(fingerprints: List[Fingerprint]) -> List[Tuple[int, int, float]]:
    """Return Euclidean distances for every consecutive pair.

    Returns
    -------
    list of (i, j, distance) tuples for j == i + 1.
    """
    results: List[Tuple[int, int, float]] = []
    for i in range(len(fingerprints) - 1):
        dist = euclidean_distance(fingerprints[i], fingerprints[i + 1])
        results.append((i, i + 1, dist))
    return results
