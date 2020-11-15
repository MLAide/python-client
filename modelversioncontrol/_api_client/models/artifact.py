from __future__ import annotations

import datetime
from dateutil import parser
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Artifact:
    created_at: Optional[datetime] = None
    created_by: Optional[Dict[Any, Any]] = None
    metadata: Optional[Dict[str, str]] = None
    name: Optional[str] = None
    run_key: Optional[str] = None
    run_name: Optional[str] = None
    type: Optional[str] = None
    updated_at: Optional[datetime] = None
    version: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        created_at = self.created_at.isoformat() if self.created_at else None
        created_by = self.created_by if self.created_by else None
        metadata = self.metadata if self.metadata else None
        name = self.name
        run_key = self.run_key
        run_name = self.run_name
        type = self.type
        updated_at = self.updated_at if self.updated_at else None
        version = self.version

        result = {}
        if created_at is not None:
            result["createdAt"] = created_at
        if created_by is not None:
            result["createdBy"] = created_by
        if metadata is not None:
            result["metadata"] = metadata
        if name is not None:
            result["name"] = name
        if run_key is not None:
            result["runKey"] = run_key
        if run_name is not None:
            result["runName"] = run_name
        if type is not None:
            result["type"] = type
        if updated_at is not None:
            result["updatedAt"] = updated_at
        if version is not None:
            result["version"] = version

        return result

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> Artifact:
        created_at = parser.parse(d["createdAt"])
        created_by = d["createdBy"]
        metadata = d.get("metadata")
        name = d["name"]
        run_key = d["runKey"]
        run_name = d["runName"]
        type = d["type"]
        updated_at = d.get("updatedAt")
        version = d["version"]

        return Artifact(
            created_at=created_at,
            created_by=created_by,
            metadata=metadata,
            name=name,
            run_key=run_key,
            run_name=run_name,
            type=type,
            updated_at=parser.parse(updated_at) if updated_at else None,
            version=version
        )
