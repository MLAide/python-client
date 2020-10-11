from typing import Any, Dict, Union, cast

import httpx
import io

from ..client import Client
from ..errors import ApiResponseError
from ..models.error import Error
from ..models.model import Model


def create_model(*, client: Client, project_id: str, json_body: Model) -> Union[Model, Error]:

    url = "{}/projects/{projectId}/artifacts/models".format(client.base_url, projectId=project_id)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body.to_dict()

    response = httpx.post(url=url, headers=headers, json=json_json_body,)

    if response.status_code == 200:
        return Model.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 500:
        return Error.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)


def upload_artifact_binary(
        *, client: Client, project_id: str, model_name: str, model_version: int, binary: io.BytesIO) \
        -> Union[None, Error]:
    url = "{}/projects/{projectId}/artifacts/models/{modelName}/{modelVersion}/binary" \
        .format(client.base_url, projectId=project_id, modelName=model_name, modelVersion=model_version)

    headers: Dict[str, Any] = client.get_headers()

    binary.seek(0, io.SEEK_END)
    headers["content-length"] = str(binary.tell())
    binary.seek(0)

    response = httpx.post(url=url, headers=headers, data=binary)

    if response.status_code == 204:
        return
    if response.status_code == 500:
        return Error.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)
