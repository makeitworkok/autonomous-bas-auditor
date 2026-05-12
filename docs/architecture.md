# System Architecture

> **🐾 OpenClaw Native** — This architecture is designed for natural-language orchestration via OpenClaw agent skills. Every component exposes clear contracts that an OpenClaw agent can invoke through English commands.

## Data flow

```
┌─────────────────┐        HTTPS/JSON         ┌─────────────────────┐
│  Edge Collector  │ ──── POST /api/v1/ ─────▶ │     Cloud API       │
│  (Raspberry Pi   │      ingest/bacnet        │  (FastAPI/Lightsail) │
│   or local)      │                           │                     │
│                  │                           │  ┌───────────────┐  │
│  fake payload ──▶│                           │  │ Auth check    │  │
│  retry/backoff   │                           │  │ Pydantic      │  │
│  spool queue     │◀── 200 accepted ─────────│  │ validation    │  │
└─────────────────┘                           │  │ Persist to    │  │
                                               │  │ disk (JSON)   │  │
                                               │  └───────────────┘  │
                                               └─────────────────────┘
                                                        │
                                                        ▼
                                               data/raw_payloads/
                                               └── {uuid}.json
```

## Components

### Edge Collector (`edge-collector/`)

- Runs on Raspberry Pi or any local machine
- Currently generates **fake** BACnet-shaped payloads (Phase 2)
- Real BACnet/IP discovery planned for Phase 3
- Posts to `POST /api/v1/ingest/bacnet` with bearer auth
- Retry with exponential backoff (`max_retries` × `backoff_seconds × 2^attempt`)
- Local spool queue: failed payloads saved to `edge-collector/spool/`, drained on next startup
- CLI flags: `--once` (single cycle), `--max-cycles N` (bounded loop)
- Config via JSON file (`edge-collector/config/config.json`) or `EDGE_COLLECTOR_CONFIG` env var

### Cloud API (`cloud-api/`)

- FastAPI service deployed on AWS Lightsail (Ubuntu, systemd)
- **`GET /health`** — public liveness check
- **`POST /api/v1/ingest/bacnet`** — authenticated ingest endpoint
- Bearer token auth (token loaded from `BAS_AUDITOR_API_TOKEN` env var)
- Validates payload against Pydantic models (site, device, object structure)
- Persists each accepted payload as `data/raw_payloads/{uuid}.json` with `payload_id` and `received_at` metadata

### Audit Engine (planned)

- Point normalization and tagging
- Deterministic fault rule checks
- Evidence and confidence scoring per finding
- ROI ranking (top findings)
- Incentive category mapping

### OpenClaw Agent Skill (`skills/autonomous-bas-auditor/`)

This project is **OpenClaw-native** — the agent skill definition lives at `skills/autonomous-bas-auditor/SKILL.md` and enables natural English-to-action orchestration across the full pipeline.

**Supported workflows:**
- **Run an audit** — orchestrates ingestion → normalization → fault detection → ROI → report
- **Ingest data** — triggers the edge collector and confirms payload acceptance
- **Check system health** — queries the API health endpoint and spool backlog
- **Inspect raw data** — reads and summarizes stored payloads

**How it works:**
- The `SKILL.md` file provides the agent with context about the system's components, APIs, and environment
- Natural language commands are mapped to shell commands (`curl`, `python run_collector.py`) and API calls
- The agent uses bearer auth from env vars — tokens are never exposed in output
- All actions maintain traceability via payload IDs and timestamps

**Planned extensions:**
- Invokes each audit engine stage in sequence
- Handles multi-step traceability, retries, and final report assembly
- Expanded skill coverage as normalization, fault rules, and ROI modules come online

## Data contracts

**Ingest request** (`POST /api/v1/ingest/bacnet`):
- `site_id` (string, required)
- `collector_id` (string, required)
- `timestamp_utc` (string, optional)
- `protocol` (string, defaults to `"bacnet-ip"`)
- `devices` (array of device objects, required)

**Ingest response** (200):
- `status`, `payload_id`, `site_id`, `collector_id`, `protocol`, `devices_received`, `received_at`

## Security posture

- Bearer token required for ingest (constant-time comparison via `secrets.compare_digest`)
- Health endpoint is public
- Tokens stored in env files, never committed to source
- This is demo-grade auth — sufficient for prototype, not production

## Reliability posture

- Cloud API managed by systemd (`Restart=always`, `RestartSec=5`)
- Collector has retry/backoff and disk spool behavior
- 24h reliability test harness available under `edge-collector/testing/`
