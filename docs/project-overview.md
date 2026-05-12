# Project Overview

## What this is

Autonomous BAS Auditor is a demo/prototype edge-to-cloud building automation audit system built for the [ClawComp](https://clawcomp.net) competition.

It ingests BAS telemetry (BACnet/IP payloads), stores raw data for traceability, and is designed to eventually detect operational and energy inefficiencies, estimate financial impact, and surface incentive pathways.

> This is internal tooling for demonstration purposes — not built for production scale.

## Problem statement

Most commercial buildings have energy and operational inefficiencies buried in their controls behavior. Manual audits are expensive, infrequent, and don't scale. An automated pipeline that collects BAS data and runs deterministic fault rules could dramatically lower the cost of identifying and prioritizing fixes.

## How it works (today)

1. Edge collector generates a fake BACnet payload (AHU supply air temp + setpoint)
2. Collector posts the JSON payload to the cloud API with bearer auth
3. Cloud API validates the payload schema, assigns a UUID, and writes raw JSON to disk
4. Stored payloads can be inspected for traceability

## What's implemented

- [x] Cloud API ingest path running on Lightsail
- [x] Bearer token auth for ingest
- [x] Raw payload persistence (file-backed, `data/raw_payloads/`)
- [x] Edge collector with fake payload generation
- [x] Retry with exponential backoff
- [x] Local spool queue for failed posts (drain-on-startup)
- [x] `--once` and `--max-cycles` CLI modes
- [x] 24h reliability test harness (`edge-collector/testing/`)

## What's planned

- [ ] Real BACnet/IP discovery and reads (bacpypes3)
- [ ] Point normalization and tagging
- [ ] Deterministic fault detection rules
- [ ] ROI estimation and top-findings ranking
- [ ] Incentive category mapping
- [ ] OpenClaw agent orchestration
- [ ] Reporting layer

## Scope boundaries

This prototype targets:
- Single-site workflow
- BACnet/IP protocol only
- File-backed storage (no database)
- Demo-quality reliability (not HA)
