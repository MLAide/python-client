from __future__ import annotations

import datetime
from dateutil import parser
from dataclasses import dataclass
from typing import Any, Dict, Optional, cast, List

from .artifact_ref import ArtifactRef
from .experiment_ref import ExperimentRef
from .status import Status


@dataclass
class Run:
    created_at: Optional[datetime.datetime] = None
    created_by: Optional[Dict[Any, Any]] = None
    end_time: Optional[datetime.datetime] = None
    experiment_refs: Optional[List[ExperimentRef]] = None
    key: Optional[int] = None
    metrics: Optional[Dict[str, Any]] = None
    name: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    start_time: Optional[datetime.datetime] = None
    status: Optional[Status] = None
    used_artifacts: Optional[List[ArtifactRef]] = None

    def to_dict(self) -> Dict[str, Any]:
        created_at = self.created_at.isoformat() if self.created_at else None
        created_by = self.created_by if self.created_by else None
        end_time = self.end_time.isoformat() if self.end_time else None
        experiment_refs = list(map(lambda ref: ref.to_dict(), self.experiment_refs)) if self.experiment_refs else None
        key = self.key if self.key else None
        metrics = self.metrics if self.metrics else None
        name = self.name if self.name else None
        parameters = self.parameters if self.parameters else None
        start_time = self.start_time.isoformat() if self.start_time else None
        status = self.status.value if self.status else None
        used_artifacts = list(map(lambda a: a.to_dict(), self.used_artifacts)) if self.used_artifacts else None

        result = {}
        if created_at is not None:
            result["createdAt"] = created_at
        if created_by is not None:
            result["createdBy"] = created_by
        if end_time is not None:
            result["endTime"] = end_time
        if experiment_refs is not None:
            result["experimentRefs"] = experiment_refs
        if key is not None:
            result["key"] = key
        if metrics is not None:
            result["metrics"] = metrics
        if name is not None:
            result["name"] = name
        if parameters is not None:
            result["parameters"] = parameters
        if start_time is not None:
            result["startTime"] = start_time
        if status is not None:
            result["status"] = status
        if used_artifacts is not None:
            result["usedArtifacts"] = used_artifacts

        return result

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> Run:
        created_at = parser.parse(d["createdAt"])

        end_time = None
        if d.get("endTime") is not None:
            end_time = parser.parse(cast(str, d.get("endTime")))

        experiment_refs = None
        if d.get("experimentRefs") is not None:
            experiment_refs = map(lambda ref: ExperimentRef.from_dict(ref), d.get("experimentRefs"))

        metrics = None
        if d.get("metrics") is not None:
            metrics = cast(Dict[str, Any], d.get("metrics"))

        name = d.get("name")

        parameters = None
        if d.get("parameters") is not None:
            parameters = cast(Dict[str, Any], d.get("parameters"))

        start_time = None
        if d.get("startTime") is not None:
            start_time = parser.parse(cast(str, d.get("startTime")))

        status = Status(d["status"])

        created_by = d["createdBy"]

        key = d["key"]

        used_artifacts = None
        if d.get("usedArtifacts") is not None:
            used_artifacts = map(lambda a: ArtifactRef.from_dict(a), d.get("usedArtifacts"))

        return Run(
            created_at=created_at,
            created_by=created_by,
            end_time=end_time,
            experiment_refs=experiment_refs,
            key=key,
            metrics=metrics,
            name=name,
            parameters=parameters,
            start_time=start_time,
            status=status,
            used_artifacts=used_artifacts
        )
