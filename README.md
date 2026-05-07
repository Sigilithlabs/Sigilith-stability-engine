# Sigilith Stability Engine v0.1

A minimal Python package and micro‑API for structural drift detection across symbolic strings.

## Features

- Structural fingerprints
- Stability index
- Drift event detection
- Mutation event detection
- CLI execution
- FastAPI micro‑API

## Run CLI

```bash
python -m sigilith_stability demo_input.txt
```

## Run API

```bash
pip install fastapi uvicorn
uvicorn sigilith_stability.api:app --reload
```

POST JSON to:

```text
http://localhost:8000/analyse
```
