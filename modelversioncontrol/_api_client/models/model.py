from __future__ import annotations

import datetime
from dateutil import parser
from dataclasses import dataclass
from typing import Any, Dict, Optional

from .stage import Stage


@dataclass
class Model:
    created_at: Optional[datetime.datetime] = None
    name: Optional[str] = None
    run_key: Optional[str] = None
    run_name: Optional[str] = None
    stage: Optional[Stage] = None
    updated_at: Optional[datetime.datetime] = None
    version: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        created_at = self.created_at.isoformat() if self.created_at else None
        name = self.name
        run_key = self.run_key
        run_name = self.run_name
        stage = self.stage
        updated_at = self.updated_at if self.updated_at else None
        version = self.version

        result = {}
        if created_at is not None:
            result["createdAt"] = created_at
        if name is not None:
            result["name"] = name
        if run_key is not None:
            result["runKey"] = run_key
        if run_name is not None:
            result["runName"] = run_name
        if stage is not None:
            result["stage"] = stage
        if updated_at is not None:
            result["updatedAt"] = updated_at
        if version is not None:
            result["version"] = version

        return result

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> Model:
        created_at = parser.parse(d["createdAt"])
        name = d["name"]
        run_key = d["runKey"]
        run_name = d["runName"]
        stage = Stage(d["stage"])
        updated_at = d.get("updatedAt")
        version = d["version"]

        return Model(
            created_at=created_at,
            name=name,
            run_key=run_key,
            run_name=run_name,
            stage=stage,
            updated_at=updated_at,
            version=version
        )
