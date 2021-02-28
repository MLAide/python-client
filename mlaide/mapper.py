from .model import Artifact, ArtifactRef, Run, RunStatus
from ._api_client.dto import ArtifactDto, ArtifactRefDto, ExperimentRefDto, RunDto, StatusDto

from typing import List, Optional


def dto_to_artifact(artifact_dto: ArtifactDto) -> Artifact:
    return Artifact(
        created_at=artifact_dto.created_at,
        created_by=artifact_dto.created_at,
        files=artifact_dto.files,
        metadata=artifact_dto.metadata,
        model=artifact_dto.model,
        name=artifact_dto.name,
        run_key=artifact_dto.run_key,
        run_name=artifact_dto.run_name,
        type=artifact_dto.type,
        updated_at=artifact_dto.updated_at,
        version=artifact_dto.version,
    )


def run_to_dto(run: Run, experiment_key: Optional[str], used_artifacts: Optional[List[ArtifactRef]]) -> RunDto:
    return RunDto(
        created_at=None,
        created_by=None,
        end_time=None,
        experiment_refs=None if experiment_key is None else [ExperimentRefDto(experiment_key)],
        key=None,
        metrics=None,
        name=run.name,
        parameters=None,
        start_time=None,
        status=StatusDto(run.status.name),
        used_artifacts=__map_artifact_refs(used_artifacts)
    )


def dto_to_run(run_dto: RunDto) -> Run:
    return Run(
        name=run_dto.name,
        status=RunStatus[run_dto.status.name],
        parameters={} if run_dto.parameters is None else run_dto.parameters,
        metrics={} if run_dto.metrics is None else run_dto.metrics,
        start_time=run_dto.start_time,
        end_time=run_dto.end_time,
        key=run_dto.key,
    )


def __map_artifact_refs(artifacts: List[ArtifactRef] = None):
    return list(map(lambda a: ArtifactRefDto(name=a.name, version=a.version), artifacts)) if artifacts else None
