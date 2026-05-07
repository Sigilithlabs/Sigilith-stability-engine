"""Structural fingerprint computation for symbolic strings."""

from __future__ import annotations

from collections import Counter
from math import log2


def compute_fingerprint(text: str) -> dict:
    """Return a structural fingerprint dictionary for *text*.

    Keys
    ----
    length         : number of characters
    unique_chars   : number of distinct characters
    unique_bigrams : number of distinct consecutive character pairs
    entropy        : Shannon entropy in bits (log base-2)
    """
    n = len(text)
    if n == 0:
        return {"length": 0, "unique_chars": 0, "unique_bigrams": 0, "entropy": 0.0}

    char_counts = Counter(text)
    unique_chars = len(char_counts)

    bigrams = [text[i : i + 2] for i in range(n - 1)]
    unique_bigrams = len(set(bigrams))

    entropy = -sum((c / n) * log2(c / n) for c in char_counts.values())

    return {
        "length": n,
        "unique_chars": unique_chars,
        "unique_bigrams": unique_bigrams,
        "entropy": entropy,
    }
