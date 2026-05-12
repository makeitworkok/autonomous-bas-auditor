# Autonomous BAS Auditor

An edge-to-cloud prototype that ingests building automation system (BAS) telemetry, stores raw payloads, and lays the groundwork for automated fault detection and energy audit reporting.

> **Scope**: This is a demo/prototype built for the [ClawComp](https://clawcomp.net) competition. It is internal tooling — not designed for production scale or multi-tenant deployment.

## What works today

- **Cloud API** — FastAPI service on AWS Lightsail. Accepts BACnet-shaped payloads via `POST /api/v1/ingest/bacnet` with bearer auth. Persists raw JSON to disk.
- **Edge Collector** — Python CLI that generates fake BAS payloads and posts them to the cloud API with retry/backoff and local spool recovery.

## What's planned

- Point normalization and tagging
- Deterministic fault detection rules
- ROI estimation and incentive mapping
- OpenClaw agent orchestration for end-to-end audit workflows

## Project structure

```
autonomous-bas-auditor/
├── cloud-api/              # FastAPI ingest service
│   ├── app/main.py         # API endpoints and models
│   └── deploy/             # systemd service unit
├── edge-collector/         # Edge data collector
│   ├── collector/          # Core modules (config, payload, poster, spool)
│   ├── config/             # Config template
│   ├── deploy/             # systemd service unit
│   └── testing/            # 24h reliability test harness
├── docs/                   # Full documentation package
└── .tests/                 # Integration test scripts
```

## Quickstart

### Cloud API (local)

```bash
cd cloud-api
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
BAS_AUDITOR_API_TOKEN=dev-token uvicorn app.main:app --port 8000
```

### Edge Collector (local)

```bash
cd edge-collector
pip install -r requirements.txt
cp config/config.example.json config/config.json
# Edit config.json: set api_url and bearer_token
python run_collector.py --once
```

## Documentation

- [Full docs package](docs/README.md)
- [API Reference](docs/api-reference.md)
- [ClawComp Submission Notes](docs/clawcomp-submission-notes.md)
