"""FastAPI micro-API for the Sigilith Stability Engine."""

from __future__ import annotations

from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

from .compare import fingerprint_diff
from .events import detect_events
from .fingerprint import compute_fingerprint
from .report import build_report
from .stability import stability_index

app = FastAPI(
    title="Sigilith Stability Engine",
    description="Structural drift detection across symbolic strings.",
    version="0.1.0",
)


class AnalyseRequest(BaseModel):
    """Request body for the /analyse endpoint."""

    lines: List[str]


@app.post("/analyse")
def analyse(request: AnalyseRequest) -> dict:
    """Analyse a sequence of strings and return a stability report."""
    lines = [line.strip() for line in request.lines if line.strip()]

    if not lines:
        return build_report([], 0.0, [], [])

    fingerprints = [compute_fingerprint(line) for line in lines]
    diffs = [
        fingerprint_diff(fingerprints[i], fingerprints[i + 1])
        for i in range(len(fingerprints) - 1)
    ]
    idx = stability_index(fingerprints)
    drift, mutation = detect_events(fingerprints, diffs)
    return build_report(fingerprints, idx, drift, mutation)
