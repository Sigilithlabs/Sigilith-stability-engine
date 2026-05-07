"""Structural fingerprint for a single symbolic string."""

import math
from collections import Counter
from dataclasses import dataclass, asdict
from typing import List


@dataclass
class Fingerprint:
    """Structural fingerprint derived from a single input string."""

    length: int
    unique_chars: int
    unique_bigrams: int
    entropy: float

    def to_dict(self) -> dict:
        return asdict(self)


def compute_fingerprint(s: str) -> Fingerprint:
    """Return a :class:`Fingerprint` for *s*.

    Features
    --------
    length
        Total character count.
    unique_chars
        Count of distinct characters.
    unique_bigrams
        Count of distinct two-character substrings.
    entropy
        Shannon entropy (bits) computed over character frequencies.
    """
    length = len(s)
    unique_chars = len(set(s))
    bigrams: List[str] = [s[i : i + 2] for i in range(length - 1)]
    unique_bigrams = len(set(bigrams))

    counts = Counter(s)
    total = length
    if total == 0:
        entropy = 0.0
    else:
        entropy = -sum(
            (c / total) * math.log2(c / total) for c in counts.values()
        )

    return Fingerprint(
        length=length,
        unique_chars=unique_chars,
        unique_bigrams=unique_bigrams,
        entropy=entropy,
    )
