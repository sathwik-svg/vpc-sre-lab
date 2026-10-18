# VPC — Visual Private Cloud

A local-first private-cloud simulation and Site Reliability Engineering
(SRE) learning platform built on Ubuntu Server. VPC provides a foundation
for learning API reliability, container health checks, observability,
network troubleshooting, and deployment automation.

## Project goals

- Run locally on Ubuntu Server without requiring AWS.
- Preserve existing home-server workloads.
- Use reproducible container builds and automated tests.
- Measure service reliability with health endpoints and metrics.
- Practice incident response, SLOs, and incremental Agile delivery.

## Architecture

- **API:** FastAPI
- **Container runtime:** Podman
- **Health and readiness:** `/health` and `/ready`
- **Metrics:** Prometheus-compatible `/metrics`
- **Frontend:** HTML, CSS, and JavaScript in `frontend/`
- **CI:** GitHub Actions workflow in `.github/workflows/ci.yml`
- **Public frontend:** Cloudflare Worker static site

The API container is intended to bind to the host loopback interface.
A public frontend does not automatically have access to a private API.
Any remote API connection must be explicitly configured and secured.

See [architecture](docs/architecture.md) and
[deployment runbook](docs/deployment.md) for more details.

## Repository layout

```text
.
├── .github/workflows/ci.yml
├── docs/
│   ├── adr/
│   ├── architecture.md
│   ├── deployment.md
│   └── requirements.md
├── frontend/
├── scripts/healthcheck.py
├── src/vpc/
├── tests/
├── Containerfile
└── requirements.txt
```

## Local development

Use the existing virtual environment if you have one:

```bash
cd ~/projects/cpc-visual-private-cloud
.venv/bin/python -m pip install -r requirements.txt
```

Run the tests:

```bash
PYTHONPATH=src .venv/bin/python -m pytest -q
```

`PYTHONPATH=src` makes the application package available during local
test execution. The GitHub Actions workflow sets this environment
variable automatically.

## API endpoints

| Endpoint | Purpose |
|---|---|
| `/health` | Reports application health |
| `/ready` | Reports application readiness |
| `/metrics` | Exposes Prometheus-format metrics |

Local verification example, using the currently verified test container:

```bash
curl -fsS http://127.0.0.1:18002/health
curl -fsS http://127.0.0.1:18002/ready
curl -fsS http://127.0.0.1:18002/metrics
```

The port above refers to the existing test container, not a production
deployment recommendation. Check the deployment runbook before deploying.

## Container operations

Inspect VPC containers:

```bash
podman ps -a --filter name=vpc
```

Inspect logs for a specific container:

```bash
podman logs --tail 100 vpc-health-test2
```

Do not stop, remove, or recreate unrelated home-server services during
VPC development. In particular, preserve the existing n8n service and
its data.

## Security

- Never commit `.env` files, tunnel tokens, credentials, or private keys.
- Keep the API bound to loopback unless a reviewed deployment design
  explicitly requires another exposure model.
- Do not put Cloudflare tunnel tokens in source code or frontend files.
- Use HTTPS for remote browser-to-API communication.
- Configure authentication and authorization before exposing private
  operations or sensitive metrics.
- A successful health check does not prove the whole host is healthy.
- This single-host lab is not a high-availability production platform.

## Current status

Foundation and container health checks are working. The existing API
health and readiness endpoints have been verified locally, and the
current test suite passes. GitHub Actions CI has been added and must be
confirmed by a successful workflow run after pushing.

## Roadmap

1. Keep the local API and health checks reproducible.
2. Verify CI on GitHub.
3. Connect the frontend to a deliberately selected, secured API endpoint.
4. Add integration tests for API and frontend connectivity.
5. Add monitoring dashboards, SLOs, and incident runbooks.
6. Document recovery procedures and validate them safely.
