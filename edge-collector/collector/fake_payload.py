from __future__ import annotations

from datetime import datetime, timezone
from random import uniform

from .config import CollectorConfig


def build_fake_payload(config: CollectorConfig) -> dict:
    sat = round(uniform(52.0, 58.0), 2)
    sat_sp = 55.0
    return {
        "site_id": config.site_id,
        "collector_id": config.collector_id,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "protocol": config.protocol,
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
                        "present_value": sat,
                        "units": "degreesFahrenheit",
                    },
                    {
                        "object_type": "analogValue",
                        "object_instance": 2,
                        "object_name": "Supply Air Temp Setpoint",
                        "present_value": sat_sp,
                        "units": "degreesFahrenheit",
                    },
                ],
            }
        ],
    }
