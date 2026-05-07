"""Report generation — combines fingerprinting, stability, and event modules."""

from dataclasses import asdict
from typing import Any, Dict, List

from .events import detect_anomalies, detect_drift, detect_mutation
from .fingerprint import compute_fingerprint
from .stability import stability_index


def generate_report(lines: List[str]) -> Dict[str, Any]:
    """Analyse *lines* and return a structured stability report.

    Parameters
    ----------
    lines:
        A sequence of symbolic strings to analyse.  Blank lines are ignored.

    Returns
    -------
    dict with keys:

    * ``stability_index`` — mean coefficient of variation across fingerprint features.
    * ``drift_events`` — list of entropy-drift events.
    * ``mutation_events`` — list of structural-mutation events.
    * ``entropy_profile`` — per-line Shannon entropy values.
    * ``anomaly_flags`` — indices of statistically anomalous lines.
    * ``fingerprints`` — full fingerprint dicts for every line.
    """
    active_lines = [l for l in lines if l.strip()]
    fingerprints = [compute_fingerprint(l) for l in active_lines]

    return {
        "stability_index": stability_index(fingerprints),
        "drift_events": detect_drift(fingerprints),
        "mutation_events": detect_mutation(fingerprints),
        "entropy_profile": [fp.entropy for fp in fingerprints],
        "anomaly_flags": detect_anomalies(fingerprints),
        "fingerprints": [asdict(fp) for fp in fingerprints],
    }
