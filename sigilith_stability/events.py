"""Drift and mutation event detection across fingerprint sequences."""

from .compare import compare_fingerprints

# A *drift event* flags a moderate structural shift between consecutive inputs.
DRIFT_THRESHOLD: float = 0.25

# A *mutation event* flags a large, sudden structural shift.
MUTATION_THRESHOLD: float = 0.45


def detect_drift_events(
    fingerprints: list, threshold: float = DRIFT_THRESHOLD
) -> list:
    """Return a list of drift events for consecutive fingerprint pairs.

    Each event is a dict with ``index`` (the earlier of the two positions) and
    ``drift_score`` (the normalized drift between the pair).  An event is
    emitted when ``drift_score > threshold``.
    """
    events = []
    for i in range(len(fingerprints) - 1):
        score = compare_fingerprints(fingerprints[i], fingerprints[i + 1])
        if score > threshold:
            events.append({"index": i, "drift_score": score})
    return events


def detect_mutation_events(
    fingerprints: list, threshold: float = MUTATION_THRESHOLD
) -> list:
    """Return a list of mutation events for consecutive fingerprint pairs.

    A mutation event represents a sudden, large structural shift.  Each event
    is a dict with ``index`` and ``mutation_score``.
    """
    events = []
    for i in range(len(fingerprints) - 1):
        score = compare_fingerprints(fingerprints[i], fingerprints[i + 1])
        if score > threshold:
            events.append({"index": i, "mutation_score": score})
    return events


def detect_anomaly_flags(fingerprints: list, z_threshold: float = 2.0) -> list:
    """Return indices of fingerprints whose entropy is an outlier (|z| > threshold).

    Anomaly flags highlight inputs whose entropy deviates significantly from
    the mean entropy of the sequence.
    """
    if len(fingerprints) < 2:
        return []

    entropies = [fp["entropy"] for fp in fingerprints]
    mean = sum(entropies) / len(entropies)
    variance = sum((e - mean) ** 2 for e in entropies) / len(entropies)
    if variance == 0:
        return []
    std = variance ** 0.5

    return [
        {"index": i, "entropy": e, "z_score": (e - mean) / std}
        for i, e in enumerate(entropies)
        if abs((e - mean) / std) > z_threshold
    ]
