# Operations Runbook

## Operational checks
- API health: GET /health
- API auth: ensure unauthorized ingest is 401
- API process: systemctl status bas-auditor-api.service
- Collector logs: stdout/systemd logs on collector host
- Raw payload growth: monitor data/raw_payloads count

## Standard incidents

### Ingest failing with 401
- Confirm collector uses current bearer token
- Confirm /etc/autonomous-bas-auditor/api.env has BAS_AUDITOR_API_TOKEN
- Restart API service after token changes

### API unreachable
- Check Lightsail firewall for TCP 8000
- Check service status and journal logs
- Check for port conflicts (old uvicorn process)

### Collector cannot post
- Verify api_url and token in collector config/env
- Verify DNS/IP connectivity from collector host
- Inspect spool directory for queued payloads

## Backup and retention guidance
- Raw payloads are currently file-based
- Add retention policy before production scaling
- Rotate/archive old payload files regularly

## Security practices
- Keep tokens in env files, never in git
- Restrict SSH key access and rotate keys periodically
- Avoid exposing non-required ports publicly

## Change management
- Update docs in this folder with each major change
- Record architecture decisions in docs/decision-log.md
