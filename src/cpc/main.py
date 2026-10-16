"""FastAPI application for CPC."""

from fastapi import FastAPI, Request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from starlette.responses import Response

from cpc.health import get_health, get_readiness

app = FastAPI(
    title="CPC — Visual Private Cloud",
    description="Local-first cloud reliability engineering platform.",
    version="0.1.0",
)

HTTP_REQUESTS = Counter(
    "cpc_http_requests_total",
    "Total HTTP requests received by CPC, excluding the metrics endpoint.",
    ["method"],
)

HTTP_RESPONSES = Counter(
    "cpc_http_responses_total",
    "Total HTTP responses completed by CPC, excluding the metrics endpoint.",
    ["method", "status_code"],
)


@app.middleware("http")
async def record_http_metrics(request: Request, call_next):
    """Count CPC requests and completed responses."""
    if request.url.path == "/metrics":
        return await call_next(request)

    HTTP_REQUESTS.labels(method=request.method).inc()

    response = await call_next(request)

    HTTP_RESPONSES.labels(
        method=request.method,
        status_code=str(response.status_code),
    ).inc()

    return response


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Report the health of the CPC application."""
    return get_health()


@app.get("/ready", tags=["Health"])
def readiness_check() -> dict[str, str]:
    """Report whether CPC is ready to accept requests."""
    return get_readiness()


@app.get("/metrics", tags=["Observability"], include_in_schema=False)
def metrics() -> Response:
    """Expose CPC metrics in Prometheus text format."""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
