# Phase 2 Reliability Test Plan (Fake Data)

## Goal
Validate that the edge collector can continuously post fake payloads to the cloud API with stable behavior over a long run.

## Duration
- Target: 24 hours
- Poll interval: 30 seconds
- Expected cycles: 2880

## Success Criteria
1. Collector process stays running for full test duration.
2. Successful posts >= 99 percent of total cycles.
3. Spool directory remains empty or drains back to zero after transient failures.
4. Cloud raw payload count increases approximately by total successful cycles.
5. No unhandled exceptions terminate the process.

## Pre-checks
1. Cloud API health returns 200.
2. Collector bearer token is valid.
3. EDGE_COLLECTOR_CONFIG points to reliability config.

## Run Command
python edge-collector/run_collector.py --max-cycles 2880

Managed starter command (PowerShell):
powershell -ExecutionPolicy Bypass -File edge-collector/testing/start_reliability_test.ps1

Register hourly checkpoint task:
powershell -ExecutionPolicy Bypass -File edge-collector/testing/register_hourly_checkpoint_task.ps1

Unregister hourly checkpoint task (after test completion):
powershell -ExecutionPolicy Bypass -File edge-collector/testing/unregister_hourly_checkpoint_task.ps1

## Required Environment
- EDGE_COLLECTOR_CONFIG=edge-collector/testing/reliability_config.json
- EDGE_COLLECTOR_BEARER_TOKEN=<server token>

## Evidence Collection
- Collector log output redirected to edge-collector/testing/reliability_run.log
- Start/end payload counts collected from Lightsail raw payloads folder
- Spool file count sampled at start and end

Metrics snapshot command:
powershell -ExecutionPolicy Bypass -File edge-collector/testing/collect_reliability_metrics.ps1

Hourly checkpoint output:
- edge-collector/testing/reliability_hourly.log

## Failure Signals
- Repeated 401 responses (token issue)
- Persistent spool growth (network/API issue)
- Process exits before max-cycles reached

## Recovery Guidance
1. Verify token and API endpoint.
2. Restart collector from same config (spool should drain first).
3. Record outage window and rerun full 24h once stabilized.
