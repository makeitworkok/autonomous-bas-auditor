# Development Roadmap

## Phase 1 — Cloud Receiver + Hardening
**Status: complete**
- [x] Health endpoint (`GET /health`)
- [x] Ingest endpoint (`POST /api/v1/ingest/bacnet`)
- [x] Raw payload persistence to disk
- [x] Bearer token auth
- [x] systemd service on Lightsail

## Phase 2 — Edge Collector MVP
**Status: complete**
- [x] Collector scaffold and config system
- [x] Fake BACnet payload generation
- [x] `POST` with retry/exponential backoff
- [x] Local spool queue (enqueue on failure, drain on startup)
- [x] `--once` and `--max-cycles` CLI flags
- [x] 24h reliability test harness (PowerShell scripts under `edge-collector/testing/`)

## Phase 2.5 — OpenClaw Skill Foundation
**Status: complete**
- [x] Agent skill directory structure (`skills/autonomous-bas-auditor/`)
- [x] `SKILL.md` definition with metadata, instructions, and environment config
- [x] Supported workflows: data ingestion, health checks, raw data inspection, audit execution
- [x] Natural-language-ready documentation across all components

## Phase 3 — Real BACnet Acquisition
**Status: not started**
- [ ] Integrate bacpypes3
- [ ] Who-Is / I-Am discovery
- [ ] Object list and present value reads
- [ ] Replace fake payload with live data path

## Phase 4 — Normalization + Tagging
**Status: not started**
- [ ] Normalized point schema
- [ ] Deterministic point tagging
- [ ] Confidence scoring

## Phase 5 — Audit Rules
**Status: not started**
- [ ] First 8 deterministic fault rules
- [ ] Evidence + confidence per finding

## Phase 6 — ROI + Incentives
**Status: not started**
- [ ] Annual energy waste range estimates
- [ ] Top-3 finding ranking
- [ ] Incentive category mapping

## Phase 7 — OpenClaw Skill Expansion
**Status: not started**
- [ ] Expanded skill coverage for normalization, fault detection, and ROI modules
- [ ] Multi-step orchestration with inter-stage traceability
- [ ] Trace logging and automatic retries
- [ ] Report generation skill

## External dependencies (not in code)
- Raspberry Pi hardware and network placement
- Site BAS network access approvals
- Occupancy schedule and utility/provider context
