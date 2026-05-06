# API Reference

## Base URL
Current deployment target: http://50.19.79.71:8000

## GET /health
Purpose: service liveness check.

Response 200 example:
{
  "status": "ok",
  "service": "autonomous-bas-auditor-api"
}

## POST /api/v1/ingest/bacnet
Purpose: submit site BAS payload from edge collector.

Auth:
- Required header: Authorization: Bearer <token>

Request body fields:
- site_id (string)
- collector_id (string)
- timestamp_utc (string, optional)
- protocol (string, defaults to bacnet-ip)
- devices (array)

Device fields:
- device_instance (int)
- device_name (string, optional)
- address (string)
- vendor_name (string, optional)
- objects (array)

Object fields:
- object_type (string)
- object_instance (int)
- object_name (string, optional)
- present_value (any, optional)
- units (string, optional)

Response 200 example:
{
  "status": "accepted",
  "payload_id": "uuid",
  "site_id": "demo-site-001",
  "collector_id": "pi-edge-001",
  "protocol": "bacnet-ip",
  "devices_received": 1,
  "received_at": "timestamp"
}

Error behavior:
- 401 when Authorization header is missing/invalid
- 503 when server token is not configured
