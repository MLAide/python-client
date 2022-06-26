import io
import cgi
from typing import Any, Collection, Tuple, cast, Dict, Optional

import httpx

from ._api_commons import assert_response_status
from ..client import Client
from ..dto import ArtifactDto, FileHashDto


def create_model(*, client: Client, project_key: str, artifact_name: str, artifact_version: int) -> None:
    url = "{}/projects/{projectKey}/artifacts/{artifactName}/{artifactVersion}/model"\
        .format(client.base_url, projectKey=project_key, artifactName=artifact_name, artifactVersion=artifact_version)

    headers: Dict[str, Any] = client.get_headers()

    response = httpx.request(
        method="PUT",
        url=url,
        headers=headers,
    )

    assert_response_status(response)


def create_artifact(*, client: Client, project_key: str, artifact: ArtifactDto) -> ArtifactDto:
    url = "{}/projects/{projectKey}/artifacts"\
        .format(client.base_url, projectKey=project_key)

    headers: Dict[str, Any] = client.get_headers()

    response = httpx.request(
        method="POST",
        url=url,
        headers=headers,
        json=artifact.to_dict_without_none_values()
    )

    assert_response_status(response)

    return ArtifactDto.from_dict(response.json())


def upload_file(*, client: Client, project_key: str, artifact_name: str, artifact_version: int, filename: str, file_hash: str, file: io.BytesIO):
    url = "{}/projects/{projectKey}/artifacts/{artifactName}/{artifactVersion}/files"\
        .format(client.base_url, projectKey=project_key, artifactName=artifact_name, artifactVersion=artifact_version)

    headers: Dict[str, Any] = client.get_headers()
    query_params = {'file-hash': file_hash}

    files = {'file': (filename, file)}

    response = httpx.request(
        method="POST",
        url=url,
        headers=headers,
        files=files,
        params=query_params
    )

    assert_response_status(response)


def get_artifact(*, client: Client,
                 project_key: str,
                 artifact_name: str,
                 artifact_version: Optional[int],
                 model_stage: str = None) -> ArtifactDto:
    version = artifact_version if artifact_version is not None else "latest"

    url = "{}/projects/{projectKey}/artifacts/{artifactName}/{artifactVersion}" \
        .format(client.base_url, projectKey=project_key, artifactName=artifact_name, artifactVersion=version)

    query_params = None if model_stage is None else {"model-stage": model_stage}

    headers: Dict[str, Any] = client.get_headers()

    response = httpx.request(
        method="GET",
        url=url,
        headers=headers,
        params=query_params
    )

    assert_response_status(response)

    return ArtifactDto.from_dict(cast(Dict[str, Any], response.json()))


def download_artifact(*,
                      client: Client,
                      project_key: str,
                      artifact_name: str,
                      artifact_version: int) -> Tuple[io.BytesIO, str]:

    url = "{}/projects/{projectKey}/artifacts/{artifactName}/{artifactVersion}/files" \
        .format(client.base_url, projectKey=project_key, artifactName=artifact_name, artifactVersion=artifact_version)

    headers: Dict[str, Any] = client.get_headers()
    headers["Accepts"] = "application/zip"

    response = httpx.request(
        method="GET",
        url=url,
        headers=headers
    )

    assert_response_status(response)

    content_disposition = response.headers.get("Content-Disposition")
    value, params = cgi.parse_header(content_disposition)
    filename = params.get("filename")
    return io.BytesIO(response.content), filename

def find_artifact_by_file_hashes(*, client: Client,
                                 project_key: str,
                                 artifact_name: str,
                                 files: Collection[FileHashDto]) -> ArtifactDto:
    url = "{}/projects/{projectKey}/artifacts/{artifactName}/find-by-file-hashes" \
        .format(client.base_url, projectKey=project_key, artifactName=artifact_name)

    headers: Dict[str, Any] = client.get_headers()

    response = httpx.request(
        method="POST",
        url=url,
        headers=headers,
        json=[file.to_dict_without_none_values() for file in files]
    )
    
    assert_response_status(response, is_404_valid=True)

    if response.status_code == 404:
        return None

    return ArtifactDto.from_dict(cast(Dict[str, Any], response.json()))
