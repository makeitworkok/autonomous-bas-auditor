# Decision Log

Use this log to capture meaningful technical/product choices.

## Template
- Date:
- Decision:
- Context:
- Options considered:
- Selected option:
- Consequences:

## Entries

### 2026-05-06
- Decision: Use bearer token auth for ingest endpoint.
- Context: Need simple, immediate security control for edge-to-cloud posting.
- Options considered: API key header, bearer token, no auth.
- Selected option: Bearer token in Authorization header.
- Consequences: Better default security posture; token rotation process required.

### 2026-05-06
- Decision: Run cloud API via systemd on Lightsail.
- Context: Need persistent service and restart behavior across reboots.
- Options considered: manual nohup process, systemd service.
- Selected option: systemd service.
- Consequences: Improved reliability and operability; adds service management steps.
