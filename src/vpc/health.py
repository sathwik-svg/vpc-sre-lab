"""Health and readiness checks for the VPC service."""


def get_health() -> dict[str, str]:
    """Report whether the VPC application is alive."""
    return {
        "status": "healthy",
        "service": "vpc",
    }


def get_readiness() -> dict[str, str]:
    """Report whether VPC is ready to accept requests."""
    return {
        "status": "ready",
        "service": "vpc",
    }
