from vpc.health import get_health


def test_health_reports_service_as_healthy():
    result = get_health()

    assert result == {
        "status": "healthy",
        "service": "vpc",
    }
