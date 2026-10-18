"""FastAPI application for VPC."""

from time import perf_counter

from fastapi import FastAPI, Request
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Histogram,
    generate_latest,
)
from starlette.responses import Response

from vpc.health import get_health, get_readiness

app = FastAPI(
    title="VPC — Visual Private Cloud",
    description="Local-first cloud reliability engineering platform.",
    version="0.1.0",
)

HTTP_REQUESTS = Counter(
    "vpc_http_requests_total",
    "Total HTTP requests received by VPC, excluding the metrics endpoint.",
    ["method"],
)

HTTP_RESPONSES = Counter(
    "vpc_http_responses_total",
    "Total HTTP responses completed by VPC, excluding the metrics endpoint.",
    ["method", "status_code"],
)

HTTP_REQUEST_DURATION = Histogram(
    "vpc_http_request_duration_seconds",
    "HTTP request duration in seconds, excluding the metrics endpoint.",
    ["method"],
    buckets=(0.01, 0.05, 0.1, 0.3, 0.5, 1.0, 2.5, 5.0),
)


@app.middleware("http")
async def record_http_metrics(request: Request, call_next):
    """Record request counts, response status and duration."""
    if request.url.path == "/metrics":
        return await call_next(request)

    HTTP_REQUESTS.labels(method=request.method).inc()
    start_time = perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        HTTP_REQUEST_DURATION.labels(method=request.method).observe(
            perf_counter() - start_time
        )
        raise

    HTTP_RESPONSES.labels(
        method=request.method,
        status_code=str(response.status_code),
    ).inc()

    HTTP_REQUEST_DURATION.labels(method=request.method).observe(
        perf_counter() - start_time
    )

    return response


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Report the health of the VPC application."""
    return get_health()


@app.get("/ready", tags=["Health"])
def readiness_check() -> dict[str, str]:
    """Report whether VPC is ready to accept requests."""
    return get_readiness()


@app.get("/metrics", tags=["Observability"], include_in_schema=False)
def metrics() -> Response:
    """Expose VPC metrics in Prometheus text format."""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
