# VPC Requirements

## 1. Purpose

Build a local Visual Private Cloud simulation with practical
SRE capabilities, using the Ubuntu home server as its host.

## 2. Constraints

- No AWS account or cloud infrastructure.
- Preserve the existing n8n workload on port 5678.
- Prefer free and open-source tools.
- Start with a lightweight, testable application.
- Avoid unnecessary changes to the host operating system.

## 3. Functional requirements

- FR-01: Expose an application liveness endpoint.
- FR-02: Expose a readiness endpoint.
- FR-03: Export service metrics.
- FR-04: Display service and infrastructure status.
- FR-05: Record operational events and errors.
- FR-06: Support controlled failure and recovery tests.
- FR-07: Document operational procedures.

## 4. Non-functional requirements

- NFR-01: The application must have automated tests.
- NFR-02: Setup must be reproducible.
- NFR-03: Services must use explicit resource limits where supported.
- NFR-04: Existing unrelated services must remain unaffected.
- NFR-05: Reliability claims must be supported by measurements.
- NFR-06: Secrets must not be committed to Git.

## 5. Initial acceptance criteria

- Repository contains architecture and requirements documentation.
- Application design is reviewed before implementation.
- Automated tests can run locally.
- Existing services remain operational.
- Setup and rollback instructions are documented.

## 6. Out of scope for the first milestone

- Real AWS infrastructure.
- Public exposure of the home server.
- Production-grade high availability from a single host.
- Uncontrolled failure injection.
