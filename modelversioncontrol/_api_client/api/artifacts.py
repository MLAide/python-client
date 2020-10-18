from typing import Any, Dict, Union, cast

import httpx
import io
import json

from ..client import Client
from ..errors import ApiResponseError
from ..models.error import Error
from ..models.model import Model


def create_model(*, client: Client, project_id: str, model: Model, binary: io.BytesIO) -> Union[Model, Error]:
    url = "{}/projects/{projectId}/artifacts/models".format(client.base_url, projectId=project_id)

    headers: Dict[str, Any] = client.get_headers()
    # headers['content-type'] = 'multipart/form-data'

    model_json = json.dumps(model.to_dict())
    binary.seek(0)

    multipart = {
        'model': ('model', model_json, 'application/json'),
        'binary': ('binary', binary, 'application/octet-stream')
    }
    response = httpx.request(
        method="POST",
        url=url,
        headers=headers,
        files=multipart
    )

    if response.status_code == 200:
        return Model.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 500:
        return Error.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)
