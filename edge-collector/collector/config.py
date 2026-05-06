from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CollectorConfig:
    site_id: str
    collector_id: str
    api_url: str
    bearer_token: str
    protocol: str = "bacnet-ip"
    poll_interval_seconds: int = 60
    max_retries: int = 3
    backoff_seconds: int = 2
    request_timeout_seconds: int = 15
    spool_dir: str = "edge-collector/spool"
    drain_spool_on_start: bool = True
    log_level: str = "INFO"


def _required(raw: dict, key: str) -> str:
    value = raw.get(key)
    if not value:
        raise ValueError(f"Missing required config key: {key}")
    return str(value)


def load_config() -> CollectorConfig:
    config_path = os.getenv("EDGE_COLLECTOR_CONFIG", "edge-collector/config/config.json")
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Config file not found: {path}. Copy edge-collector/config/config.example.json to config.json and set values."
        )

    raw = json.loads(path.read_text(encoding="utf-8"))
    bearer_token = str(raw.get("bearer_token", "")).strip()
    env_token = os.getenv("EDGE_COLLECTOR_BEARER_TOKEN", "").strip()
    if env_token:
        bearer_token = env_token

    if not bearer_token or bearer_token == "REPLACE_WITH_TOKEN":
        raise ValueError("Missing bearer token. Set bearer_token in config.json or EDGE_COLLECTOR_BEARER_TOKEN.")

    return CollectorConfig(
        site_id=_required(raw, "site_id"),
        collector_id=_required(raw, "collector_id"),
        api_url=_required(raw, "api_url"),
        bearer_token=bearer_token,
        protocol=str(raw.get("protocol", "bacnet-ip")),
        poll_interval_seconds=int(raw.get("poll_interval_seconds", 60)),
        max_retries=int(raw.get("max_retries", 3)),
        backoff_seconds=int(raw.get("backoff_seconds", 2)),
        request_timeout_seconds=int(raw.get("request_timeout_seconds", 15)),
        spool_dir=str(raw.get("spool_dir", "edge-collector/spool")),
        drain_spool_on_start=bool(raw.get("drain_spool_on_start", True)),
        log_level=str(raw.get("log_level", "INFO")),
    )
