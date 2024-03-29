from mlaide._api_client.dto.experiment_dto import ExperimentDto
from .model import Artifact, ArtifactRef, Git, Run, RunStatus, Experiment
from ._api_client.dto import ArtifactDto, ArtifactRefDto, GitDto, ExperimentRefDto, RunDto, StatusDto

from typing import List, Optional


def dto_to_artifact(artifact_dto: ArtifactDto) -> Artifact:
    return Artifact(
        created_at=artifact_dto.created_at,
        created_by=artifact_dto.created_at,
        files=artifact_dto.files,
        metadata=artifact_dto.metadata,
        model=artifact_dto.model,
        name=artifact_dto.name,
        type=artifact_dto.type,
        updated_at=artifact_dto.updated_at,
        version=artifact_dto.version,
    )

def dto_to_experiment(experiment_dto: ExperimentDto) -> Experiment:
    return Experiment(
        created_at=experiment_dto.created_at,
        key=experiment_dto.key,
        name=experiment_dto.name,
        tags=experiment_dto.tags
    )

def run_to_dto(run: Run, experiment_key: Optional[str], used_artifacts: Optional[List[ArtifactRef]]) -> RunDto:
    return RunDto(
        created_at=None,
        created_by=None,
        end_time=None,
        experiment_refs=None if experiment_key is None else [ExperimentRefDto(experiment_key)],
        git=None if run.git is None else git_to_dto(run.git),
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


def git_to_dto(git: Git) -> GitDto:
    return GitDto(
        commit_time=git.commit_time,
        commit_hash=git.commit_hash,
        is_dirty=git.is_dirty,
        repository_uri=git.repository_uri
    )


def __map_artifact_refs(artifacts: List[ArtifactRef] = None):
    return list(map(lambda a: ArtifactRefDto(name=a.name, version=a.version), artifacts)) if artifacts else None
