# Edge Collector (Phase 2 MVP)

This collector posts fake BACnet-shaped payloads to the cloud ingest API.

## Setup

1. Create config file:
   - Copy `edge-collector/config/config.example.json` to `edge-collector/config/config.json`
   - Fill `api_url` and `bearer_token`
   - Or keep placeholder token and set env var: `EDGE_COLLECTOR_BEARER_TOKEN`
2. Install dependencies:
   - `pip install -r edge-collector/requirements.txt`

## Run once

`python edge-collector/run_collector.py --once`

## Run loop

`python edge-collector/run_collector.py`

## Behavior

- Sends fake payloads on an interval
- Retries failed posts with exponential backoff
- Spools failed payloads to disk
- Drains spool files first on startup
