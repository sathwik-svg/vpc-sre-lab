# VPC Deployment Runbook

## 1. Current verified state

VPC is a local-first cloud reliability engineering lab running on Ubuntu
Server with Podman.

The existing containers were verified as follows:

| Container | Image | Host binding | Observed status |
|---|---|---|---|
| `vpc-test` | `localhost/vpc:0.1.0` | `127.0.0.1:18000` | Running |
| `vpc-health-test` | `localhost/vpc:0.1.1` | `127.0.0.1:18001` | Running |
| `vpc-health-test2` | `localhost/vpc:0.1.1` | `127.0.0.1:18002` | Healthy |

The health and readiness endpoints on port `18002` returned successful
responses during verification.

These are existing lab containers, not a recommendation to run three
copies indefinitely. Do not remove or recreate them until a separate
deployment and rollback plan has been reviewed.

The existing n8n service and its data must remain untouched.

## 2. Inspect containers

List VPC containers:

```bash
podman ps -a --filter name=vpc
```

Inspect the verified API container:

```bash
podman inspect vpc-health-test2
```

Review recent logs:

```bash
podman logs --tail 100 vpc-health-test2
```

Treat inspect output as potentially sensitive. Do not publish environment
variables, credentials, tunnel tokens, or other secret values.

## 3. Verify API health

Check health:

```bash
curl -fsS http://127.0.0.1:18002/health
```

Expected response:

```json
{"status":"healthy","service":"vpc"}
```

Check readiness:

```bash
curl -fsS http://127.0.0.1:18002/ready
```

Expected response:

```json
{"status":"ready","service":"vpc"}
```

Check metrics:

```bash
curl -fsS http://127.0.0.1:18002/metrics
```

The metrics endpoint should return Prometheus-format text.

## 4. Build an image for a future deployment

The repository contains a `Containerfile`. Build a new, versioned image
without replacing any running container:

```bash
podman build -t localhost/vpc:0.2.0 -f Containerfile .
```

Confirm the image exists:

```bash
podman image inspect localhost/vpc:0.2.0
```

Building an image alone does not deploy it or change existing containers.

Before creating a replacement container, review the configuration, verify
the health-check behavior, and define a rollback procedure. Do not reuse
an existing container name or host port without checking for conflicts.

## 5. Container health checks

List the current containers:

```bash
podman ps --filter name=vpc
```

Inspect health status for the existing health-check container:

```bash
podman inspect --format '{{.State.Health.Status}}' vpc-health-test2
```

Run the configured health check:

```bash
podman healthcheck run vpc-health-test2
```

If health checks fail, inspect the health-check results and application
logs before making changes. A healthy container does not prove the whole
host or platform is healthy.

## 6. Frontend and Cloudflare connectivity

The static frontend hosted on Cloudflare cannot reach a service bound
only to `127.0.0.1` on the Ubuntu server. A browser's localhost refers to
the device running that browser, not the remote server.

Choose and document the backend hosting model before configuring the
frontend:

- **Local-first:** keep the API private and access it through a deliberately
  configured secure connection.
- **Cloud-hosted API:** deploy the API separately with HTTPS, authentication
  and appropriate access controls.

A Cloudflare Tunnel can provide a route to a private service when
configured intentionally. Verify the hostname, origin service, access
policy, and API authentication before relying on it. Do not publish tunnel
tokens or secrets in the repository or frontend JavaScript.

Do not change tunnel configuration, DNS, firewall rules, or existing
services as part of this documentation-only runbook.

## 7. Security and operations

- Keep the API bound to loopback unless a reviewed design requires otherwise.
- Run the application as a non-root container user.
- Keep secrets out of Git, frontend assets, logs, and public issue reports.
- Use HTTPS for remote browser-to-API traffic.
- Add authentication and authorization before exposing private operations.
- Limit metrics access if they reveal operational information.
- Back up important data before any destructive deployment operation.
- Preserve unrelated services, especially n8n and its data.
- This is a single-host learning lab, not a high-availability platform.

## 8. Recovery checklist

1. Confirm which container and endpoint are failing.
2. Check container status and recent logs.
3. Test `/health` and `/ready` locally.
4. Review recent code or configuration changes.
5. Roll back only the affected VPC component if required.
6. Re-test the API and confirm unrelated services remain operational.
7. Record the incident, root cause, and preventive action.
