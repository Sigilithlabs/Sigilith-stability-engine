"""Command-line interface for the Sigilith Stability Engine."""

import json
import sys

from .events import detect_anomaly_flags, detect_drift_events, detect_mutation_events
from .fingerprint import compute_fingerprint
from .report import generate_report
from .stability import compute_stability_index


def main(argv: list | None = None) -> None:
    """Entry point for ``python -m sigilith_stability <input_file>``."""
    args = argv if argv is not None else sys.argv[1:]

    if not args:
        print(
            "Usage: python -m sigilith_stability <input_file>",
            file=sys.stderr,
        )
        sys.exit(1)

    input_path = args[0]
    try:
        with open(input_path, encoding="utf-8") as fh:
            lines = [line.rstrip("\n") for line in fh if line.strip()]
    except OSError as exc:
        print(f"Error reading {input_path!r}: {exc}", file=sys.stderr)
        sys.exit(1)

    if not lines:
        print("Input file contains no non-empty lines.", file=sys.stderr)
        sys.exit(1)

    fingerprints = [compute_fingerprint(line) for line in lines]
    stability_index = compute_stability_index(fingerprints)
    drift_events = detect_drift_events(fingerprints)
    mutation_events = detect_mutation_events(fingerprints)
    anomaly_flags = detect_anomaly_flags(fingerprints)

    report = generate_report(
        fingerprints, stability_index, drift_events, mutation_events, anomaly_flags
    )
    print(json.dumps(report, indent=2))
