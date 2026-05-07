"""Drift, mutation, and anomaly event detection."""

import math
from typing import Any, Dict, List

from .fingerprint import Fingerprint

# Default detection thresholds
_DRIFT_ENTROPY_THRESHOLD: float = 0.5
_MUTATION_LENGTH_RATIO: float = 2.0
_ANOMALY_Z_THRESHOLD: float = 2.0


def detect_drift(
    fingerprints: List[Fingerprint],
    threshold: float = _DRIFT_ENTROPY_THRESHOLD,
) -> List[Dict[str, Any]]:
    """Detect entropy drift events between consecutive fingerprints.

    A drift event is recorded whenever the absolute change in Shannon entropy
    between two consecutive strings exceeds *threshold* bits.
    """
    events: List[Dict[str, Any]] = []
    for i in range(1, len(fingerprints)):
        delta = abs(fingerprints[i].entropy - fingerprints[i - 1].entropy)
        if delta > threshold:
            events.append(
                {
                    "index": i,
                    "type": "drift",
                    "entropy_delta": delta,
                }
            )
    return events


def detect_mutation(
    fingerprints: List[Fingerprint],
    threshold: float = _MUTATION_LENGTH_RATIO,
) -> List[Dict[str, Any]]:
    """Detect structural mutation events between consecutive fingerprints.

    A mutation event is recorded whenever the length ratio between two
    consecutive strings exceeds *threshold* (or falls below 1 / *threshold*),
    signalling a sudden structural change.
    """
    events: List[Dict[str, Any]] = []
    for i in range(1, len(fingerprints)):
        prev_len = fingerprints[i - 1].length
        curr_len = fingerprints[i].length
        if prev_len == 0:
            continue
        ratio = curr_len / prev_len
        if ratio > threshold or ratio < (1.0 / threshold):
            events.append(
                {
                    "index": i,
                    "type": "mutation",
                    "length_ratio": ratio,
                }
            )
    return events


def detect_anomalies(
    fingerprints: List[Fingerprint],
    z_threshold: float = _ANOMALY_Z_THRESHOLD,
) -> List[int]:
    """Return indices of fingerprints whose entropy is a statistical anomaly.

    An entry is flagged when its entropy deviates from the population mean by
    more than *z_threshold* standard deviations.
    """
    if len(fingerprints) < 2:
        return []

    entropies = [fp.entropy for fp in fingerprints]
    mean = sum(entropies) / len(entropies)
    variance = sum((e - mean) ** 2 for e in entropies) / len(entropies)
    std = math.sqrt(variance)

    if std == 0.0:
        return []

    return [i for i, e in enumerate(entropies) if abs(e - mean) / std > z_threshold]
