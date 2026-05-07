"""FastAPI micro-service for the Sigilith Stability Engine.

Start with::

    uvicorn sigilith_stability.api:app --reload

Then POST JSON to ``http://localhost:8000/analyse``::

    {"strings": ["hello world", "hello world!!", "eval(\\"os.listdir()\\")"]}
"""

from __future__ import annotations

from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .events import detect_anomaly_flags, detect_drift_events, detect_mutation_events
from .fingerprint import compute_fingerprint
from .report import generate_report
from .stability import compute_stability_index

app = FastAPI(
    title="Sigilith Stability Engine",
    description="Structural drift detection across symbolic strings.",
    version="0.1.0",
)


class AnalyseRequest(BaseModel):
    strings: List[str] = Field(
        ...,
        min_length=1,
        description="Ordered list of symbolic strings to analyse.",
    )


@app.post("/analyse")
def analyse(request: AnalyseRequest) -> dict:
    """Analyse a sequence of strings and return a stability report."""
    fingerprints = [compute_fingerprint(s) for s in request.strings]
    stability_index = compute_stability_index(fingerprints)
    drift_events = detect_drift_events(fingerprints)
    mutation_events = detect_mutation_events(fingerprints)
    anomaly_flags = detect_anomaly_flags(fingerprints)
    return generate_report(
        fingerprints, stability_index, drift_events, mutation_events, anomaly_flags
    )
