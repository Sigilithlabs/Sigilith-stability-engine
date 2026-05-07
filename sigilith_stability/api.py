"""FastAPI micro-API for the Sigilith Stability Engine."""

from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

from .report import generate_report

app = FastAPI(
    title="Sigilith Stability Engine",
    version="0.1.0",
    description="Structural drift detection across symbolic strings.",
)


class AnalyseRequest(BaseModel):
    """Request body for the ``/analyse`` endpoint."""

    lines: List[str]


@app.post("/analyse", summary="Analyse a list of symbolic strings")
def analyse(request: AnalyseRequest) -> dict:
    """Return a full stability report for the supplied *lines*."""
    return generate_report(request.lines)
