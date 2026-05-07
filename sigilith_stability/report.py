"""Report assembly for a stability analysis run."""


def generate_report(
    fingerprints: list,
    stability_index: float,
    drift_events: list,
    mutation_events: list,
    anomaly_flags: list,
) -> dict:
    """Assemble and return the analysis report as a plain dict.

    The returned structure matches the JSON schema shown in ``sample_output.json``:

    .. code-block:: json

        {
          "stability_index": 0.062,
          "drift_events": [],
          "mutation_events": [],
          "entropy_profile": [3.78, 3.88, 3.72, 3.74],
          "anomaly_flags": [],
          "fingerprints": [...]
        }
    """
    return {
        "stability_index": stability_index,
        "drift_events": drift_events,
        "mutation_events": mutation_events,
        "entropy_profile": [fp["entropy"] for fp in fingerprints],
        "anomaly_flags": anomaly_flags,
        "fingerprints": fingerprints,
    }
