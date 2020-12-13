import io
from typing import Any, Dict, cast

import httpx

from ..client import Client
from ..errors import ApiResponseError
from ..models.artifact import Artifact
from ..models.error import Error


def create_model(*, client: Client, project_key: str, artifact_name: str, artifact_version: int) -> None:
    url = "{}/projects/{projectKey}/artifacts/{artifactName}/{artifactVersion}/model"\
        .format(client.base_url, projectKey=project_key, artifactName=artifact_name, artifactVersion=artifact_version)

    headers: Dict[str, Any] = client.get_headers()

    response = httpx.request(
        method="PUT",
        url=url,
        headers=headers,
    )

    if response.status_code == 204:
        return None
    else:
        raise ApiResponseError(response=response, error=Error.from_dict(cast(Dict[str, Any], response.json())))


def create_artifact(*, client: Client, project_key: str, artifact: Artifact) -> Artifact:
    url = "{}/projects/{projectKey}/artifacts"\
        .format(client.base_url, projectKey=project_key)

    headers: Dict[str, Any] = client.get_headers()

    response = httpx.request(
        method="POST",
        url=url,
        headers=headers,
        json=artifact.to_dict()
    )

    if response.status_code == 200:
        return Artifact.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response, error=Error.from_dict(cast(Dict[str, Any], response.json())))


def upload_file(*, client: Client, project_key: str, artifact_name: str, artifact_version: int, file: io.BytesIO):
    url = "{}/projects/{projectKey}/artifacts/{artifactName}/{artifactVersion}/files"\
        .format(client.base_url, projectKey=project_key, artifactName=artifact_name, artifactVersion=artifact_version)

    headers: Dict[str, Any] = client.get_headers()
    files = {'file': file}

    response = httpx.request(
        method="POST",
        url=url,
        headers=headers,
        files=files
    )

    if response.status_code != 204:
        raise ApiResponseError(response=response, error=Error.from_dict(cast(Dict[str, Any], response.json())))
