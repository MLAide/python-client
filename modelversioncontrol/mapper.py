from .model import Artifact
from ._api_client.dto import ArtifactDto


def to_artifact_dto(artifact: Artifact) -> ArtifactDto:
    pass


def from_artifact_dto(artifact_dto: ArtifactDto) -> Artifact:
    return Artifact(
        name=artifact_dto.name,
        metadata=artifact_dto.metadata,
        type=artifact_dto.type,
        run_key=artifact_dto.run_key,
        version=artifact_dto.version,
        run_name=artifact_dto.run_name,
        created_at=artifact_dto.created_at,
        created_by=artifact_dto.created_at,
        updated_at=artifact_dto.updated_at,
        files=artifact_dto.files,
        model=artifact_dto.model
    )
