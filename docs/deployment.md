# CPC Deployment Runbook

## 1. Overview

CPC (Visual Private Cloud) is a local-first cloud reliability engineering
project. The API runs in a Podman container and is exposed only on the
host loopback interface.

- Host API address: `http://127.0.0.1:8001`
- Container API port: `8000`
- Health endpoint: `/health`
- Readiness endpoint: `/ready`
- Container image: `localhost/cpc-api:0.2.0`
- Container name: `cpc-api`

The existing n8n service is independent and must remain untouched.

## 2. Build the image

From the repository root:

```bash
podman build -t localhost/cpc-api:0.2.0 .
```

Confirm the image exists:

```bash
podman image inspect localhost/cpc-api:0.2.0
```

## 3. Run CPC

If replacing an existing CPC container, first check its status and
confirm the image and configuration you intend to deploy.

To create the CPC container:

```bash
podman run -d \
  --name cpc-api \
  --publish 127.0.0.1:8001:8000 \
  --restart unless-stopped \
  --health-cmd 'python /app/healthcheck.py' \
  --health-interval 30s \
  --health-timeout 5s \
  --health-start-period 10s \
  --health-retries 3 \
  localhost/cpc-api:0.2.0
```

Do not remove or recreate the n8n container during CPC deployments.

## 4. Verify the API

Check health:

```bash
curl -fsS http://127.0.0.1:8001/health
```

Expected response:

```json
{"status":"healthy","service":"cpc"}
```

Check readiness:

```bash
curl -fsS http://127.0.0.1:8001/ready
```

Expected response:

```json
{"status":"ready","service":"cpc"}
```

## 5. Verify container health

List CPC:

```bash
podman ps --filter name=cpc-api
```

Inspect the health status:

```bash
podman inspect --format '{{.State.Health.Status}}' cpc-api
```

Expected status after the initial health-check period:

```text
healthy
```

Run a health check immediately:

```bash
podman healthcheck run cpc-api
```

Inspect recorded health-check results:

```bash
podman inspect --format '{{json .State.Healthcheck}}' cpc-api
```

## 6. Troubleshooting

Inspect application logs:

```bash
podman logs --tail 100 cpc-api
```

Inspect the container:

```bash
podman inspect cpc-api
```

If the health status is `starting`, allow the initial checks to run.
If it becomes `unhealthy`, inspect the health-check log and application
logs before making changes.

## 7. Security and operational notes

- The host port is bound to `127.0.0.1`, not all host interfaces.
- Do not publish CPC publicly or change firewall rules as part of this runbook.
- The container runs as a non-root user.
- The health check tests the application's `/health` response.
- A healthy container does not prove that the entire host or platform is healthy.
- This deployment is single-host and is not high availability.
- Preserve the existing n8n container and its data during CPC changes.
