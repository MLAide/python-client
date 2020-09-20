from __future__ import annotations

import datetime
from dateutil import parser
from dataclasses import dataclass
from typing import Any, Dict, Optional, cast

from .status import Status


@dataclass
class Experiment:
    id: Optional[str] = None
    status: Optional[Status] = None
    created_at: Optional[datetime.datetime] = None
    user: Optional[Dict[Any, Any]] = None
    name: Optional[str] = None
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    parameters: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        id = self.id if self.id else None
        status = self.status.value if self.status else None
        created_at = self.created_at.isoformat() if self.created_at else None
        user = self.user if self.user else None
        name = self.name if self.name else None
        start_time = self.start_time.isoformat() if self.start_time else None
        end_time = self.end_time.isoformat() if self.end_time else None
        parameters = self.parameters if self.parameters else None
        metrics = self.metrics if self.metrics else None

        result = {}
        if id is not None:
            result["id"] = id
        if status is not None:
            result["status"] = status
        if created_at is not None:
            result["createdAt"] = created_at
        if user is not None:
            result["user"] = user
        if name is not None:
            result["name"] = name
        if start_time is not None:
            result["start_time"] = start_time
        if end_time is not None:
            result["end_time"] = end_time
        if parameters is not None:
            result["parameters"] = parameters
        if metrics is not None:
            result["metrics"] = metrics

        return result

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> Experiment:
        id = d["id"]

        status = Status(d["status"])
        created_at = parser.parse(d["createdAt"])
        user = d["user"]
        name = d.get("name")
        start_time = None
        if d.get("startTime") is not None:
            start_time = parser.parse(cast(str, d.get("startTime")))

        end_time = None
        if d.get("endTime") is not None:
            end_time = parser.parse(cast(str, d.get("endTime")))

        parameters = None
        if d.get("parameters") is not None:
            parameters = cast(Dict[str, Any], d.get("parameters"))

        metrics = None
        if d.get("metrics") is not None:
            metrics = cast(Dict[str, Any], d.get("metrics"))

        return Experiment(
            id=id,
            status=status,
            created_at=created_at,
            user=user,
            name=name,
            start_time=start_time,
            end_time=end_time,
            parameters=parameters,
            metrics=metrics,
        )
