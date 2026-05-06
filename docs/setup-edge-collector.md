# Edge Collector Setup (MVP)

## Purpose
Run the fake-data edge collector to continuously post BACnet-shaped payloads to the cloud API.

## Current implementation
- Fake payload generation
- Scheduled loop mode
- Retry with exponential backoff
- Local spool queue for failed posts
- Optional one-shot mode for quick testing

## Files
- edge-collector/config/config.example.json
- edge-collector/config/config.json
- edge-collector/run_collector.py
- edge-collector/deploy/edge-collector.service

## Local setup
1. Install Python dependencies from edge-collector/requirements.txt.
2. Copy config.example.json to config.json.
3. Set api_url and bearer token.
4. Prefer setting token via EDGE_COLLECTOR_BEARER_TOKEN env var.

## Run commands
- One cycle: python edge-collector/run_collector.py --once
- Continuous loop: python edge-collector/run_collector.py

## Raspberry Pi deployment notes
- Default systemd template assumes user pi and repo at /home/pi/autonomous-bas-auditor
- Update WorkingDirectory and ExecStart if your path differs

## Reliability behavior
- On failed post after retries, payload is saved under edge-collector/spool
- On startup, collector attempts to drain spool files before new cycle processing
