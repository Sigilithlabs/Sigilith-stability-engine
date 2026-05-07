"""Pairwise fingerprint comparison utilities."""

from __future__ import annotations


def fingerprint_diff(fp1: dict, fp2: dict) -> dict:
    """Return the signed delta between two fingerprints.

    Each field in the returned dict is ``fp2[field] - fp1[field]``, giving the
    direction and magnitude of change from *fp1* to *fp2*.
    """
    return {
        "length_delta": fp2["length"] - fp1["length"],
        "unique_chars_delta": fp2["unique_chars"] - fp1["unique_chars"],
        "unique_bigrams_delta": fp2["unique_bigrams"] - fp1["unique_bigrams"],
        "entropy_delta": fp2["entropy"] - fp1["entropy"],
    }
