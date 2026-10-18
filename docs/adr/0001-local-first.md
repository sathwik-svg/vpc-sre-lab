# ADR-0001: Local-first development

- Status: Accepted
- Date: 2026-10-16

## Context

An AWS account is unavailable, and the Ubuntu server already
runs an n8n workload under Podman.

## Decision

Develop VPC locally, preserve the existing workload, and
validate application behavior before adding infrastructure.

## Consequences

Positive:
- No AWS costs.
- Direct experience with Linux and container operations.
- Changes can be tested incrementally.

Trade-offs:
- A single host has limited fault isolation.
- Local simulation does not prove multi-region resilience.
- Monitoring and application workloads share host resources.
