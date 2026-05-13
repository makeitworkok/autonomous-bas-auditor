# Autonomous BAS Auditor

**🐾 OpenClaw Native** — This project is built with first-class [OpenClaw](https://clawcomp.net) integration. All components are designed for natural-language orchestration via OpenClaw agent skills, enabling English-to-action workflows across the entire pipeline.

An edge-to-cloud prototype that ingests building automation system (BAS) telemetry, stores raw payloads, and lays the groundwork for automated fault detection and energy audit reporting.

> **Scope**: This is a demo/prototype built for the [ClawComp](https://clawcomp.net) competition. It is internal tooling — not designed for production scale or multi-tenant deployment.

## What works today

- **Cloud API** — FastAPI service on AWS Lightsail. Accepts BACnet-shaped payloads via `POST /api/v1/ingest/bacnet` with bearer auth. Persists raw JSON to disk.
- **Edge Collector** — Python CLI that generates fake BAS payloads and posts them to the cloud API with retry/backoff and local spool recovery.

## OpenClaw integration

This is an **OpenClaw-native** project. The `skills/` directory contains agent skill definitions that allow OpenClaw to orchestrate the full audit pipeline using natural English commands — from triggering data collection to generating financial impact reports.

- **Agent skill**: `skills/autonomous-bas-auditor/SKILL.md`
- **Supported workflows**: data ingestion, system health checks, raw data inspection, full audit execution
- **Natural language**: All components are documented and structured for English-to-action compatibility

## What's planned

- Point normalization and tagging
- Deterministic fault detection rules
- ROI estimation and incentive mapping
- Expanded OpenClaw skill coverage for multi-step audit workflows

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
├── skills/                 # OpenClaw agent skill definitions
│   └── autonomous-bas-auditor/
│       └── SKILL.md        # Primary agent skill
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
- [OpenClaw Agent Skill](skills/autonomous-bas-auditor/SKILL.md)
- [ClawComp Submission Notes](docs/clawcomp-submission-notes.md)
