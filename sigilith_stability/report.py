"""Final report assembly."""

from __future__ import annotations

# Strings whose entropy deviates from the group mean by more than this many
# standard deviations are flagged as anomalies.
ANOMALY_SIGMA: float = 2.0


def _anomaly_flags(fingerprints: list[dict]) -> list[dict]:
    """Return anomaly flags for fingerprints whose entropy is an outlier."""
    if len(fingerprints) < 3:
        return []

    entropies = [fp["entropy"] for fp in fingerprints]
    mean = sum(entropies) / len(entropies)
    variance = sum((e - mean) ** 2 for e in entropies) / len(entropies)
    std = variance ** 0.5

    if std == 0:
        return []

    flags = []
    for i, fp in enumerate(fingerprints):
        z = (fp["entropy"] - mean) / std
        if abs(z) > ANOMALY_SIGMA:
            flags.append({"index": i, "entropy": fp["entropy"], "z_score": z})
    return flags


def build_report(
    fingerprints: list[dict],
    stability_idx: float,
    drift_events: list[dict],
    mutation_events: list[dict],
    anomaly_flags: list[dict] | None = None,
) -> dict:
    """Assemble the full analysis report dictionary."""
    if anomaly_flags is None:
        anomaly_flags = _anomaly_flags(fingerprints)

    return {
        "stability_index": stability_idx,
        "drift_events": drift_events,
        "mutation_events": mutation_events,
        "entropy_profile": [fp["entropy"] for fp in fingerprints],
        "anomaly_flags": anomaly_flags,
        "fingerprints": fingerprints,
    }
