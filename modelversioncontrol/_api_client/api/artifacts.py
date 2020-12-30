import io
import cgi
from typing import Any, cast, Dict, Union

import httpx

from ..client import Client
from ..errors import ApiResponseError
from ..dto import ArtifactDto, Error


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


def create_artifact(*, client: Client, project_key: str, artifact: ArtifactDto) -> ArtifactDto:
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
        return ArtifactDto.from_dict(response.json())
    else:
        raise ApiResponseError(response=response, error=Error.from_dict(cast(Dict[str, Any], response.json())))


def upload_file(*, client: Client, project_key: str, artifact_name: str, artifact_version: int, filename: str, file: io.BytesIO):
    url = "{}/projects/{projectKey}/artifacts/{artifactName}/{artifactVersion}/files"\
        .format(client.base_url, projectKey=project_key, artifactName=artifact_name, artifactVersion=artifact_version)

    headers: Dict[str, Any] = client.get_headers()

    files = {'file': (filename, file)}

    response = httpx.request(
        method="POST",
        url=url,
        headers=headers,
        files=files
    )

    if response.status_code != 204:
        raise ApiResponseError(response=response, error=Error.from_dict(cast(Dict[str, Any], response.json())))


def get_artifact(*, client: Client, project_key: str, artifact_name: str, artifact_version: Union[int, str]) -> ArtifactDto:
    url = "{}/projects/{projectKey}/artifacts/{artifactName}/{artifactVersion}" \
        .format(client.base_url, projectKey=project_key, artifactName=artifact_name, artifactVersion=artifact_version)

    headers: Dict[str, Any] = client.get_headers()

    response = httpx.request(
        method="GET",
        url=url,
        headers=headers
    )

    if response.status_code == 200:
        return ArtifactDto.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response, error=Error.from_dict(cast(Dict[str, Any], response.json())))


def download_artifact(*,
                      client: Client,
                      project_key: str,
                      artifact_name: str,
                      artifact_version: Union[int, str]) -> (io.BytesIO, str):

    url = "{}/projects/{projectKey}/artifacts/{artifactName}/{artifactVersion}/files" \
        .format(client.base_url, projectKey=project_key, artifactName=artifact_name, artifactVersion=artifact_version)

    headers: Dict[str, Any] = client.get_headers()
    headers["Accepts"] = "application/zip"

    response = httpx.request(
        method="GET",
        url=url,
        headers=headers
    )

    if response.status_code == 200:
        content_disposition = response.headers.get("Content-Disposition")
        value, params = cgi.parse_header(content_disposition)
        filename = params.get("filename")
        return io.BytesIO(response.content), filename
    else:
        raise ApiResponseError(response=response, error=Error.from_dict(cast(Dict[str, Any], response.json())))
