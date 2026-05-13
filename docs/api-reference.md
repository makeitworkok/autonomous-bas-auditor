# API Reference

> **Note**: The base URL below points to the current Lightsail demo instance. This is a prototype deployment, not a production endpoint.

## Base URL

```
http://50.19.79.71:8000
```

---

## `GET /health`

Public liveness check. No authentication required.

**Response `200`**:

```json
{
  "status": "ok",
  "service": "autonomous-bas-auditor-api"
}
```

---

## `POST /api/v1/ingest/bacnet`

Submit a BAS payload from the edge collector.

### Authentication

| Header | Value |
|--------|-------|
| `Authorization` | `Bearer <token>` |

### Request body

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `site_id` | string | yes | — | Site identifier |
| `collector_id` | string | yes | — | Collector identifier |
| `timestamp_utc` | string | no | — | ISO 8601 timestamp |
| `protocol` | string | no | `"bacnet-ip"` | Protocol tag |
| `devices` | array | yes | — | List of device objects |

### Device object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `device_instance` | int | yes | BACnet device instance |
| `device_name` | string | no | Human-readable name |
| `address` | string | yes | Network address |
| `vendor_name` | string | no | Controller vendor |
| `objects` | array | no | List of BACnet objects |

### BACnet object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `object_type` | string | yes | e.g. `"analogInput"` |
| `object_instance` | int | yes | Object instance number |
| `object_name` | string | no | Human-readable name |
| `present_value` | any | no | Current value |
| `units` | string | no | e.g. `"degreesFahrenheit"` |

### Response `200`

```json
{
  "status": "accepted",
  "payload_id": "uuid",
  "site_id": "demo-site-001",
  "collector_id": "pi-edge-001",
  "protocol": "bacnet-ip",
  "devices_received": 1,
  "received_at": "2026-05-12T22:00:00+00:00"
}
```

### Error responses

| Status | Cause |
|--------|-------|
| `401 Unauthorized` | Missing or invalid `Authorization` header |
| `422 Unprocessable Entity` | Request body fails Pydantic validation (missing required fields, wrong types) |
| `503 Service Unavailable` | Server-side `BAS_AUDITOR_API_TOKEN` env var is not configured |
