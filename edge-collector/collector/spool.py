from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable
from uuid import uuid4


class SpoolQueue:
    def __init__(self, spool_dir: str) -> None:
        self._dir = Path(spool_dir)
        self._dir.mkdir(parents=True, exist_ok=True)

    def enqueue(self, payload: dict) -> Path:
        filename = f"{uuid4()}.json"
        path = self._dir / filename
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def iter_files(self) -> Iterable[Path]:
        return sorted(self._dir.glob("*.json"), key=lambda p: p.stat().st_mtime)

    @staticmethod
    def read(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def remove(path: Path) -> None:
        path.unlink(missing_ok=True)
