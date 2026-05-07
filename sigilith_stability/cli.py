"""Command-line interface for the Sigilith Stability Engine."""

from __future__ import annotations

import json
import sys

from .compare import fingerprint_diff
from .events import detect_events
from .fingerprint import compute_fingerprint
from .report import build_report
from .stability import stability_index


def main(argv: list[str] | None = None) -> None:
    """Entry point for ``python -m sigilith_stability <input_file>``."""
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        print(
            "Usage: python -m sigilith_stability <input_file>",
            file=sys.stderr,
        )
        sys.exit(1)

    path = argv[0]
    try:
        with open(path, encoding="utf-8") as fh:
            lines = [line.rstrip("\n") for line in fh if line.strip()]
    except OSError as exc:
        print(f"Error reading '{path}': {exc}", file=sys.stderr)
        sys.exit(1)

    if not lines:
        print("Input file contains no non-empty lines.", file=sys.stderr)
        sys.exit(1)

    fingerprints = [compute_fingerprint(line) for line in lines]
    diffs = [
        fingerprint_diff(fingerprints[i], fingerprints[i + 1])
        for i in range(len(fingerprints) - 1)
    ]
    idx = stability_index(fingerprints)
    drift, mutation = detect_events(fingerprints, diffs)
    report = build_report(fingerprints, idx, drift, mutation)

    print(json.dumps(report, indent=2))
