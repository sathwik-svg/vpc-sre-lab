"""Health and readiness checks for the CPC service."""


def get_health() -> dict[str, str]:
    """Report whether the CPC application is alive."""
    return {
        "status": "healthy",
        "service": "cpc",
    }


def get_readiness() -> dict[str, str]:
    """Report whether CPC is ready to accept requests."""
    return {
        "status": "ready",
        "service": "cpc",
    }
