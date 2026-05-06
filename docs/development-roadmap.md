# Development Roadmap

## Phase 1 - Cloud Receiver + Hardening
Status: mostly complete
- Health endpoint
- Ingest endpoint
- Raw payload persistence
- Bearer auth
- Systemd service

## Phase 2 - Edge Collector MVP
Status: in progress
- Collector scaffold complete
- Fake payload posting complete
- Retry/backoff and spool complete
- 24h reliability run pending completion

## Phase 3 - Real BACnet Acquisition
Status: not started
- Add bacpypes3
- Discovery (Who-Is/I-Am)
- Object list and present value reads

## Phase 4 - Normalization + Tagging
Status: not started
- Normalized schema
- Deterministic point tags
- Confidence scoring

## Phase 5 - Audit Rules
Status: not started
- Implement first 8 rules
- Evidence + confidence per finding

## Phase 6 - ROI + Incentives
Status: not started
- Annual waste range estimates
- Top-3 ranking
- Incentive category mapping

## Phase 7 - OpenClaw Orchestration
Status: not started
- openclaw agents and tools
- End-to-end orchestration pipeline
- Trace logging and retries

## Physical dependencies (external to code)
- Raspberry Pi hardware and network placement
- Site BAS network access approvals
- Occupancy schedule and utility/provider context
