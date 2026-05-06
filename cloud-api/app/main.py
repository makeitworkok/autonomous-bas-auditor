from __future__ import annotations

import json
import os
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List, Optional
from uuid import uuid4

from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field


app = FastAPI(title="Autonomous BAS Auditor API")
API_BEARER_TOKEN = os.getenv("BAS_AUDITOR_API_TOKEN", "")

# Repository-root-relative path: <repo>/data/raw_payloads
RAW_PAYLOAD_DIR = Path(__file__).resolve().parents[2] / "data" / "raw_payloads"


class BACnetObject(BaseModel):
    object_type: str
    object_instance: int
    object_name: Optional[str] = None
    present_value: Optional[Any] = None
    units: Optional[str] = None


class BACnetDevice(BaseModel):
    device_instance: int
    device_name: Optional[str] = None
    address: str
    vendor_name: Optional[str] = None
    objects: List[BACnetObject] = Field(default_factory=list)


class BACnetPayload(BaseModel):
    site_id: str
    collector_id: str
    timestamp_utc: Optional[str] = None
    protocol: str = "bacnet-ip"
    devices: List[BACnetDevice]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _save_raw_payload(payload_id: str, received_at: str, payload: BACnetPayload) -> Path:
    RAW_PAYLOAD_DIR.mkdir(parents=True, exist_ok=True)
    payload_document = {
        "payload_id": payload_id,
        "received_at": received_at,
        "payload": payload.model_dump(),
    }
    output_path = RAW_PAYLOAD_DIR / f"{payload_id}.json"
    output_path.write_text(json.dumps(payload_document, indent=2), encoding="utf-8")
    return output_path


def _validate_bearer_token(authorization: Optional[str]) -> None:
    if not API_BEARER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Server auth token is not configured.",
        )

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    provided_token = authorization.split(" ", 1)[1].strip()
    if not secrets.compare_digest(provided_token, API_BEARER_TOKEN):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "autonomous-bas-auditor-api",
    }


@app.post("/api/v1/ingest/bacnet")
def ingest_bacnet(payload: BACnetPayload, authorization: Optional[str] = Header(default=None)) -> dict[str, Any]:
    _validate_bearer_token(authorization)
    received_at = _utc_now_iso()
    payload_id = str(uuid4())
    _save_raw_payload(payload_id=payload_id, received_at=received_at, payload=payload)

    return {
        "status": "accepted",
        "payload_id": payload_id,
        "site_id": payload.site_id,
        "collector_id": payload.collector_id,
        "protocol": payload.protocol,
        "devices_received": len(payload.devices),
        "received_at": received_at,
    }