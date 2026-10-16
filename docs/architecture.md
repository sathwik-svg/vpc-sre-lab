# CPC Architecture — Initial Design

## Host

Ubuntu Server with 2 CPU cores, approximately 8 GiB RAM
and a 44 GiB root filesystem.

## Existing runtime

Podman 5.7.0. The existing n8n workload uses port 5678.
CPC must not modify or replace that workload.

## Proposed application flow

Client
  -> CPC API
  -> Health and readiness endpoints
  -> Application metrics
  -> Monitoring and visualization

## Proposed engineering stages

1. Application and automated tests.
2. Metrics instrumentation.
3. Lightweight monitoring.
4. SLO and alert definitions.
5. Controlled reliability experiments.
6. Optional local Kubernetes deployment.

## Network and security

CPC will initially remain local to the development environment.
Ports will be chosen after inspecting existing listeners.
No public ingress or host firewall changes are planned.

## Limitations

A single physical or virtual host cannot demonstrate
true multi-host high availability. Recovery experiments
will be labelled as local simulations.
