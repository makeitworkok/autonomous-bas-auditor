import os
import sys
from datetime import datetime, timezone

import requests

LIGHTSAIL_IP = os.getenv("LIGHTSAIL_IP", "50.19.79.71")
LIGHTSAIL_PORT = os.getenv("LIGHTSAIL_PORT", "8000")
LIGHTSAIL_SCHEME = os.getenv("LIGHTSAIL_SCHEME", "http")
LIGHTSAIL_PATH = os.getenv("LIGHTSAIL_PATH", "/api/v1/ingest/bacnet")
API_KEY = os.getenv("LIGHTSAIL_API_KEY")
BEARER_TOKEN = os.getenv("LIGHTSAIL_BEARER_TOKEN")

payload = {
    "site_id": "demo-site-001",
    "collector_id": "pi-edge-001",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "protocol": "bacnet-ip",
    "devices": [
        {
            "device_instance": 12345,
            "device_name": "AHU-1 Controller",
            "address": "10.46.12.10",
            "vendor_name": "Trane",
            "objects": [
                {
                    "object_type": "analogInput",
                    "object_instance": 1,
                    "object_name": "Supply Air Temp",
                    "present_value": 55.2,
                    "units": "degreesFahrenheit",
                },
                {
                    "object_type": "analogValue",
                    "object_instance": 2,
                    "object_name": "Supply Air Temp Setpoint",
                    "present_value": 55.0,
                    "units": "degreesFahrenheit",
                },
            ],
        }
    ],
}

url = f"{LIGHTSAIL_SCHEME}://{LIGHTSAIL_IP}:{LIGHTSAIL_PORT}{LIGHTSAIL_PATH}"
headers = {}
if BEARER_TOKEN:
    headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
elif API_KEY:
    headers["x-api-key"] = API_KEY

print(f"POST -> {url}")
if BEARER_TOKEN:
    print("Using auth header: Bearer token")
elif API_KEY:
    print("Using auth header: x-api-key")
else:
    print("Using auth header: none")

try:
    response = requests.post(url, json=payload, headers=headers, timeout=15)
    print(f"HTTP {response.status_code}")
    print("Response headers:", dict(response.headers))

    try:
        print("Response JSON:", response.json())
    except ValueError:
        print("Response body:", response.text)

    response.raise_for_status()
    print("Request succeeded.")
except requests.exceptions.ConnectTimeout:
    print("Connection timed out. The host/port may be unreachable.")
    sys.exit(1)
except requests.exceptions.ConnectionError as exc:
    print("Connection failed. Verify Lightsail public IP, open firewall port, and service bind address.")
    print(f"Details: {exc}")
    sys.exit(1)
except requests.exceptions.HTTPError as exc:
    print("Server returned an error status.")
    print(f"Details: {exc}")
    sys.exit(1)