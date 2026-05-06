# ClawComp Submission Notes

## Context
This project is being developed for the clawcomp.net contest.

## One-line pitch
Autonomous BAS Auditor is an edge-to-cloud controls audit platform that ingests BAS telemetry, identifies top operational/energy issues, estimates impact, and suggests incentive pathways.

## Current contest-ready strengths
- Working cloud ingest API on Lightsail
- Authenticated ingestion workflow
- Raw payload persistence with traceable payload IDs
- Functional edge collector MVP that posts fake BAS payloads with resilience features

## Demonstrable workflow today
1. Collector sends fake payload to cloud API.
2. API authenticates, accepts, and stores raw payload.
3. Stored payload can be inspected for traceability.

## Planned differentiators before finalization
- Real BACnet discovery and live point reads
- Deterministic audit rule engine
- ROI ranking and incentive mapping
- OpenClaw orchestration from payload to final report

## Suggested judging demo script
1. Show health endpoint and authenticated ingest behavior.
2. Run one-shot collector and show new payload file appears.
3. Explain roadmap to real BACnet and OpenClaw orchestration.
4. Highlight practical impact: lower audit cost and faster remediation targeting.
