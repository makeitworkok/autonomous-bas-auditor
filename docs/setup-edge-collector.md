# Edge Collector Setup (MVP)

## Purpose

Run the edge collector to post BACnet-shaped payloads to the cloud API. Currently uses fake data; real BACnet reads are planned for Phase 3.

## What's implemented

- Fake payload generation (AHU-1 supply air temp + setpoint, randomized values)
- Scheduled loop mode with configurable interval
- One-shot mode (`--once`) for quick testing
- Bounded loop mode (`--max-cycles N`) for reliability testing
- Retry with exponential backoff on failed posts
- Local spool queue for payloads that exhaust retries
- Spool drain on startup before new collection cycles

## Files

| Path | Purpose |
|------|---------|
| `edge-collector/collector/` | Core modules (config, fake_payload, poster, spool) |
| `edge-collector/config/config.example.json` | Config template — copy to `config.json` |
| `edge-collector/run_collector.py` | Entry point |
| `edge-collector/deploy/edge-collector.service` | systemd unit for Raspberry Pi |
| `edge-collector/testing/` | 24h reliability test harness |

## Setup

1. Install Python dependencies:
   ```bash
   pip install -r edge-collector/requirements.txt
   ```

2. Create your config:
   ```bash
   cp edge-collector/config/config.example.json edge-collector/config/config.json
   ```

3. Edit `config.json` — set `api_url` and `bearer_token`.

4. (Preferred) Set the bearer token via env var instead of the config file:
   ```bash
   export EDGE_COLLECTOR_BEARER_TOKEN=<your-token>
   ```

## Run commands

All commands assume you're in the **repo root** (`autonomous-bas-auditor/`):

```bash
# One cycle — post one payload and exit
python edge-collector/run_collector.py --once

# Continuous loop (default 60s interval)
python edge-collector/run_collector.py

# Bounded loop — run N cycles then exit
python edge-collector/run_collector.py --max-cycles 100
```

## Environment variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `EDGE_COLLECTOR_CONFIG` | Override config file path | `edge-collector/config/config.json` |
| `EDGE_COLLECTOR_BEARER_TOKEN` | Override bearer token from config file | (none) |

## Raspberry Pi deployment

The systemd template at `edge-collector/deploy/edge-collector.service` assumes:
- User: `pi`
- Repo at: `/home/pi/autonomous-bas-auditor`
- Virtualenv at: `/home/pi/autonomous-bas-auditor/.venv`

Update `WorkingDirectory`, `ExecStart`, and `Environment` if your paths differ.

## Reliability behavior

- On failed post (after all retries exhausted): payload saved to `edge-collector/spool/`
- On startup: collector drains all spooled files before starting new cycles
- Spool files sorted by modification time (oldest first)

## Reliability testing

A 24h test harness is available under `edge-collector/testing/`. See `reliability_test_plan.md` in that directory for the full plan, success criteria, and run instructions.
