from fastapi.testclient import TestClient

from cpc.main import app

client = TestClient(app)


def test_health_endpoint_returns_success():
    response = client.get("/health")

    assert response.status_code == 200


def test_health_endpoint_returns_expected_json():
    response = client.get("/health")

    assert response.json() == {
        "status": "healthy",
        "service": "cpc",
    }


def test_openapi_documentation_is_available():
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/health" in response.json()["paths"]


def test_readiness_endpoint_returns_success():
    response = client.get("/ready")

    assert response.status_code == 200


def test_readiness_endpoint_returns_expected_json():
    response = client.get("/ready")

    assert response.json() == {
        "status": "ready",
        "service": "cpc",
    }


def test_metrics_endpoint_returns_prometheus_format():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "# HELP" in response.text
    assert "# TYPE" in response.text


def test_metrics_endpoint_exposes_request_counters():
    response = client.get("/metrics")

    assert "cpc_http_requests_total" in response.text
    assert "cpc_http_responses_total" in response.text
