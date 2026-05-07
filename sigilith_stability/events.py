"""Drift and mutation event detection from fingerprint sequences."""

from __future__ import annotations

# Entropy must change by more than this many bits between consecutive strings
# to be classified as a drift event.
DRIFT_THRESHOLD: float = 0.5

# The number of unique characters or unique bigrams must change by more than
# this value between consecutive strings to be classified as a mutation event.
MUTATION_THRESHOLD: int = 7


def detect_events(
    fingerprints: list[dict],
    diffs: list[dict],
) -> tuple[list[dict], list[dict]]:
    """Detect drift and mutation events in a fingerprint diff sequence.

    Parameters
    ----------
    fingerprints:
        Ordered list of fingerprint dicts (one per input string).
    diffs:
        Ordered list of consecutive fingerprint diffs (len = len(fingerprints) - 1).

    Returns
    -------
    (drift_events, mutation_events)
        Each item is a list of event dicts.  An event dict contains at minimum
        an ``"index"`` key identifying the *target* string (1-based) in the
        sequence where the event was detected.
    """
    drift_events: list[dict] = []
    mutation_events: list[dict] = []

    for i, diff in enumerate(diffs):
        target_index = i + 1  # 1-based index of the second string in the pair

        if abs(diff["entropy_delta"]) > DRIFT_THRESHOLD:
            drift_events.append(
                {
                    "index": target_index,
                    "entropy_delta": diff["entropy_delta"],
                }
            )

        if (
            abs(diff["unique_chars_delta"]) > MUTATION_THRESHOLD
            or abs(diff["unique_bigrams_delta"]) > MUTATION_THRESHOLD
        ):
            mutation_events.append(
                {
                    "index": target_index,
                    "unique_chars_delta": diff["unique_chars_delta"],
                    "unique_bigrams_delta": diff["unique_bigrams_delta"],
                    "length_delta": diff["length_delta"],
                }
            )

    return drift_events, mutation_events
