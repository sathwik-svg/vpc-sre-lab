"""Health checks for the CPC service."""


def get_health() -> dict[str, str]:
    """Return the current health status of the CPC service."""
    return {
        "status": "healthy",
        "service": "cpc",
    }
