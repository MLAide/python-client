from typing import Any, Dict, Union, cast

import httpx

from ..client import Client
from ..errors import ApiResponseError
from ..models.error import Error
from ..models.run import Run


def list_runs(*, client: Client, project_id: str) -> Union[Run, Error]:

    url = "{}/projects/{projectId}/runs".format(client.base_url, projectId=project_id)

    headers: Dict[str, Any] = client.get_headers()

    response = httpx.get(url=url, headers=headers,)

    if response.status_code == 200:
        return Run.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 500:
        return Error.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)


def create_run(*, client: Client, project_id: str, json_body: Run) -> Union[Run, Error]:

    url = "{}/projects/{projectId}/runs".format(client.base_url, projectId=project_id)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body.to_dict()

    response = httpx.post(url=url, headers=headers, json=json_json_body,)

    if response.status_code == 200:
        return Run.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 500:
        return Error.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)


def partial_update_run(*, client: Client, project_id: str, run_id: str, json_body: Run) -> Union[None, Error]:

    url = "{}/projects/{projectId}/runs/{runId}".format(
        client.base_url, projectId=project_id, runId=run_id
    )

    headers: Dict[str, Any] = client.get_headers()
    headers["content-type"] = "application/merge-patch+json"

    json_json_body = json_body.to_dict()

    response = httpx.patch(url=url, headers=headers, json=json_json_body)

    if response.status_code == 204:
        return None
    if response.status_code == 500:
        return Error.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)


def update_run_parameters(*, client: Client, project_id: str, run_id: str, parameters: Dict[str, Any]) -> Union[None, Error]:

    url = "{}/projects/{projectId}/runs/{runId}/parameters".format(
        client.base_url, projectId=project_id, runId=run_id
    )

    headers: Dict[str, Any] = client.get_headers()
    headers["content-type"] = "application/merge-patch+json"

    response = httpx.patch(url=url, headers=headers, json=parameters)

    if response.status_code == 204:
        return None
    if response.status_code == 500:
        return Error.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)


def update_run_metrics(*, client: Client, project_id: str, run_id: str, metrics: Dict[str, Any]) -> Union[None, Error]:

    url = "{}/projects/{projectId}/runs/{runId}/metrics".format(
        client.base_url, projectId=project_id, runId=run_id
    )

    headers: Dict[str, Any] = client.get_headers()
    headers["content-type"] = "application/merge-patch+json"

    response = httpx.patch(url=url, headers=headers, json=metrics)

    if response.status_code == 204:
        return None
    if response.status_code == 500:
        return Error.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)
