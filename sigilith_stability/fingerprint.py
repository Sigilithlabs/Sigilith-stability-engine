"""Structural fingerprinting for symbolic strings."""

import math
from collections import Counter


def compute_fingerprint(s: str) -> dict:
    """Return a structural fingerprint for string *s*.

    The fingerprint contains:
    - ``length``        — number of characters
    - ``unique_chars``  — number of distinct characters
    - ``unique_bigrams``— number of distinct consecutive character pairs
    - ``entropy``       — Shannon entropy (bits) based on character frequencies
    """
    length = len(s)
    if length == 0:
        return {"length": 0, "unique_chars": 0, "unique_bigrams": 0, "entropy": 0.0}

    counts = Counter(s)
    unique_chars = len(counts)

    bigrams = [s[i : i + 2] for i in range(length - 1)]
    unique_bigrams = len(set(bigrams))

    entropy = -sum((c / length) * math.log2(c / length) for c in counts.values())

    return {
        "length": length,
        "unique_chars": unique_chars,
        "unique_bigrams": unique_bigrams,
        "entropy": entropy,
    }
