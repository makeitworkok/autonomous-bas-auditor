# Cloud API Setup (Lightsail)

## Purpose
Run and operate the cloud ingest API in AWS Lightsail for edge collector submissions.

## Prerequisites
- Lightsail Ubuntu instance
- SSH access key
- Python 3.x available on host
- TCP 8000 allowed in Lightsail networking

## Deploy source
1. Copy cloud API files to server under /home/ubuntu/autonomous-bas-auditor/cloud-api.
2. Create virtual environment and install requirements.
3. Ensure bearer token env file exists at /etc/autonomous-bas-auditor/api.env.

Expected env file content:
BAS_AUDITOR_API_TOKEN=<strong-token>

## Service management
Use the service unit template:
- cloud-api/deploy/bas-auditor-api.service

Install flow:
1. Copy service file to /etc/systemd/system/bas-auditor-api.service
2. Run systemctl daemon-reload
3. Run systemctl enable bas-auditor-api.service
4. Run systemctl restart bas-auditor-api.service

## Verification checks
- systemctl is-active bas-auditor-api.service
- GET /health should return status ok JSON
- POST /api/v1/ingest/bacnet should require bearer auth

## Troubleshooting
- If service fails to start, check journalctl -u bas-auditor-api.service
- If port bind fails, confirm no legacy uvicorn process owns port 8000
- If ingest is 401, verify BAS_AUDITOR_API_TOKEN and Authorization header
