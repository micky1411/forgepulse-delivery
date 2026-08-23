"""Release-aware API used by the Jenkins delivery pipeline."""

from __future__ import annotations

import os
import time

from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

app = FastAPI(title="ForgePulse Delivery", version="1.0.0")
requests_total = Counter("forgepulse_requests_total", "API requests", ["path"])
request_duration = Histogram("forgepulse_request_duration_seconds", "API duration", ["path"])


@app.get("/health/live")
def live() -> dict[str, str]:
    requests_total.labels("live").inc()
    return {"status": "alive"}


@app.get("/health/ready")
def ready() -> dict[str, str]:
    requests_total.labels("ready").inc()
    return {"status": "ready"}


@app.get("/release")
def release() -> dict[str, str]:
    started = time.perf_counter()
    requests_total.labels("release").inc()
    result = {
        "application": "forgepulse", "version": os.getenv("APP_VERSION", "dev"),
        "commit": os.getenv("GIT_SHA", "local"), "environment": os.getenv("ENVIRONMENT", "local"),
    }
    request_duration.labels("release").observe(time.perf_counter() - started)
    return result


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
