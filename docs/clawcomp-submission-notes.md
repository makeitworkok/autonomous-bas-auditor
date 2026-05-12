# ClawComp Submission Notes

## Context

This project is a prototype built for the [clawcomp.net](https://clawcomp.net) competition. It demonstrates the skeleton of an automated BAS audit pipeline — not a production-ready product.

**🐾 OpenClaw Native** — Built with first-class OpenClaw integration. The entire pipeline can be orchestrated via natural English commands through the agent skill system.

## One-line pitch

OpenClaw-native edge-to-cloud controls audit prototype that ingests BAS telemetry, stores raw payloads with full traceability, and enables natural-language orchestration of automated fault detection and financial impact analysis.

## What works today

- Cloud API on Lightsail accepting authenticated ingest
- Raw payload persistence with traceable UUIDs
- Edge collector posting fake BACnet payloads with retry/backoff and spool recovery
- `--once` and `--max-cycles` CLI modes for testing and reliability validation
- 24h reliability test harness
- OpenClaw agent skill definition (`skills/autonomous-bas-auditor/SKILL.md`)

## Demonstrable workflow

1. Run `curl /health` to show API is alive
2. Run collector in `--once` mode — show payload accepted
3. Inspect the new `data/raw_payloads/{uuid}.json` file on the server
4. Show a `401` when posting without auth
5. Walk through `skills/autonomous-bas-auditor/SKILL.md` — show how OpenClaw can orchestrate the pipeline via natural English
6. Explain the roadmap from here: real BACnet → fault rules → ROI → expanded OpenClaw skill coverage

## Planned differentiators

- **OpenClaw-native architecture** — agent skill definitions enabling English-to-action workflows
- Real BACnet discovery and live point reads
- Deterministic audit rule engine with evidence scoring
- ROI ranking and incentive pathway mapping
- Expanded OpenClaw skill orchestration from raw data to final audit report

## Key talking points

- **OpenClaw-native** — the entire pipeline is designed for natural-language orchestration. Tell the agent what you want in plain English and it executes the workflow.
- **Cost of manual audits** — expensive, infrequent, inconsistent. This automates the data collection and analysis layer.
- **Edge resilience** — retry, backoff, and spool mean the collector doesn't lose data even when the API is temporarily unreachable.
- **Traceability** — every payload gets a UUID and timestamp, creating an audit trail from edge to cloud.
