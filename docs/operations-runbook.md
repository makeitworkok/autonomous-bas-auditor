# Operations Runbook

> This is a demo/prototype system. These checks are for verifying the demo works, not production monitoring.

## Health checks

| Check | Command / Method |
|-------|-----------------|
| API alive | `curl http://50.19.79.71:8000/health` |
| API auth working | `curl -X POST http://50.19.79.71:8000/api/v1/ingest/bacnet` → expect `401` |
| API process status | `systemctl status bas-auditor-api.service` |
| Collector logs | `journalctl -u edge-collector.service -f` (Pi) or stdout (local) |
| Payload count | `ls data/raw_payloads/ | wc -l` (on Lightsail) |
| Spool backlog | `ls edge-collector/spool/ | wc -l` |

## Standard incidents

### Ingest failing with 401

1. Confirm collector is using the current bearer token
2. Confirm `/etc/autonomous-bas-auditor/api.env` contains `BAS_AUDITOR_API_TOKEN=<token>`
3. Restart API service after token changes: `sudo systemctl restart bas-auditor-api.service`

### API unreachable

1. Check Lightsail firewall allows TCP 8000
2. Check service: `systemctl status bas-auditor-api.service`
3. Check logs: `journalctl -u bas-auditor-api.service --no-pager -n 50`
4. Check for port conflicts: `sudo lsof -i :8000`

### Collector cannot post

1. Verify `api_url` and bearer token in `edge-collector/config/config.json`
2. Test connectivity: `curl <api_url>/health`
3. Inspect spool directory for queued payloads: `ls edge-collector/spool/`

## Backup and retention

- Raw payloads are file-backed under `data/raw_payloads/` on the Lightsail instance
- No automated retention policy — fine for demo, but clean up manually if disk fills
- Spool files are transient and auto-drained on collector restart

## Security practices

- Tokens in env files, never committed to git
- SSH key access to Lightsail should be restricted
- Only TCP 8000 exposed publicly (for API); close other ports

## Change management

- Update docs in `docs/` alongside code changes
- Record architecture/product decisions in `docs/decision-log.md`
