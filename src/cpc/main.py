"""FastAPI application for CPC."""

from fastapi import FastAPI

from cpc.health import get_health

app = FastAPI(
    title="CPC — Visual Private Cloud",
    description="Local-first cloud reliability engineering platform.",
    version="0.1.0",
)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Report the health of the CPC application."""
    return get_health()
