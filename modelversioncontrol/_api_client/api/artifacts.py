from typing import Any, Dict, Union, cast, Optional

import httpx
import io
import json

from ..client import Client
from ..errors import ApiResponseError
from ..models.artifact import  Artifact
from ..models.error import Error


def create_model(*, client: Client, project_key: str, artifact_name: str, artifact_version: int) -> Optional[Error]:
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
    if response.status_code == 500:
        return Error.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)


def create_artifact(*, client: Client, project_key: str, artifact: Artifact, binary: io.BytesIO) -> Union[Artifact, Error]:
    url = "{}/projects/{projectKey}/artifacts"\
        .format(client.base_url, projectKey=project_key)

    headers: Dict[str, Any] = client.get_headers()

    artifact_json = json.dumps(artifact.to_dict())
    binary.seek(0)

    multipart = {
        'artifact': ('artifact', artifact_json, 'application/json'),
        'binary': ('binary', binary, 'application/octet-stream')
    }
    response = httpx.request(
        method="POST",
        url=url,
        headers=headers,
        files=multipart
    )

    if response.status_code == 200:
        return Artifact.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 500:
        return Error.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)
