"""Pairwise fingerprint comparison producing a normalized drift score."""

_FIELDS = ("length", "unique_chars", "unique_bigrams", "entropy")


def compare_fingerprints(fp1: dict, fp2: dict) -> float:
    """Return a drift score in ``[0, 1]`` between two fingerprints.

    Each of the four structural features is compared as a normalized absolute
    difference relative to the larger of the two values, then the results are
    averaged.  A score of ``0`` means the two fingerprints are identical; a
    score of ``1`` means the maximum possible divergence across all features.
    """
    diffs = []
    for field in _FIELDS:
        a, b = fp1[field], fp2[field]
        denom = max(a, b)
        diffs.append(0.0 if denom == 0 else abs(a - b) / denom)
    return sum(diffs) / len(diffs)
