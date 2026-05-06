# System Architecture

## High-level flow
1. Edge collector gathers BAS data (fake today, BACnet/IP next).
2. Collector posts JSON payloads to cloud API.
3. Cloud API validates auth and stores raw payloads.
4. Audit pipeline (planned) normalizes points, applies rules, estimates ROI, and maps incentives.
5. OpenClaw orchestration (planned) coordinates end-to-end execution and report generation.

## Components

### Edge Collector
- Runs on Raspberry Pi or local machine
- Generates fake payloads now
- Will perform BACnet/IP discovery and reads in Phase 3
- Includes retry/backoff and local spool queue for reliability

### Cloud API
- FastAPI service on AWS Lightsail
- Endpoints: health + ingest
- Ingest requires bearer auth
- Persists each accepted payload with payload_id and received_at

### Audit Engine (planned)
- Normalization and tagging
- Deterministic rule checks
- Evidence and confidence scoring
- ROI ranking (top findings)
- Incentive category mapping

### OpenClaw Layer (planned)
- Invokes each engine stage in order
- Handles traceability, retries, and final report assembly

## Data contracts
- Ingest payload contains site_id, collector_id, protocol, and device/object structures.
- Accepted response contains status, payload_id, and summary metadata.

## Security posture (current)
- Bearer token required for ingest
- Health endpoint public
- Secrets kept out of source files

## Reliability posture (current)
- Cloud API under systemd on Lightsail
- Collector has retry/backoff and disk spool behavior
