from typing import Any, Dict, cast

import httpx

from ..client import Client
from ..errors import ApiResponseError
from ..models.error import Error
from ..models.run import Run


def list_runs(*, client: Client, project_key: str) -> Run:

    url = "{}/projects/{projectKey}/runs".format(client.base_url, projectKey=project_key)

    headers: Dict[str, Any] = client.get_headers()

    response = httpx.get(url=url, headers=headers,)

    if response.status_code == 200:
        return Run.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response, error=Error.from_dict(cast(Dict[str, Any], response.json())))


def create_run(*, client: Client, project_key: str, json_body: Run) -> Run:

    url = "{}/projects/{projectKey}/runs".format(client.base_url, projectKey=project_key)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body.to_dict()

    response = httpx.post(url=url, headers=headers, json=json_json_body,)

    if response.status_code == 200:
        return Run.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response, error=Error.from_dict(cast(Dict[str, Any], response.json())))


def partial_update_run(*, client: Client, project_key: str, run_key: int, json_body: Run) -> None:

    url = "{}/projects/{projectKey}/runs/{runKey}".format(
        client.base_url, projectKey=project_key, runKey=run_key
    )

    headers: Dict[str, Any] = client.get_headers()
    headers["content-type"] = "application/merge-patch+json"

    json_json_body = json_body.to_dict()

    response = httpx.patch(url=url, headers=headers, json=json_json_body)

    if response.status_code == 204:
        return None
    else:
        raise ApiResponseError(response=response, error=Error.from_dict(cast(Dict[str, Any], response.json())))


def update_run_parameters(*, client: Client, project_key: str, run_key: int, parameters: Dict[str, Any]) -> None:

    url = "{}/projects/{projectKey}/runs/{runKey}/parameters".format(
        client.base_url, projectKey=project_key, runKey=run_key
    )

    headers: Dict[str, Any] = client.get_headers()
    headers["content-type"] = "application/merge-patch+json"

    response = httpx.patch(url=url, headers=headers, json=parameters)

    if response.status_code == 204:
        return None
    else:
        raise ApiResponseError(response=response, error=Error.from_dict(cast(Dict[str, Any], response.json())))


def update_run_metrics(*, client: Client, project_key: str, run_key: int, metrics: Dict[str, Any]) -> None:

    url = "{}/projects/{projectKey}/runs/{runKey}/metrics".format(
        client.base_url, projectKey=project_key, runKey=run_key
    )

    headers: Dict[str, Any] = client.get_headers()
    headers["content-type"] = "application/merge-patch+json"

    response = httpx.patch(url=url, headers=headers, json=metrics)

    if response.status_code == 204:
        return None
    else:
        raise ApiResponseError(response=response, error=Error.from_dict(cast(Dict[str, Any], response.json())))
