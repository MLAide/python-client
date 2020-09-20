from typing import Any, Dict, Union, cast

import httpx

from ..client import Client
from ..errors import ApiResponseError
from ..models.error import Error
from ..models.experiment import Experiment


def list_experiments(*, client: Client, project_id: str,) -> Union[Experiment, Error]:

    url = "{}/projects/{projectId}/experiments".format(client.base_url, projectId=project_id)

    headers: Dict[str, Any] = client.get_headers()

    response = httpx.get(url=url, headers=headers,)

    if response.status_code == 200:
        return Experiment.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 500:
        return Error.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)


def create_experiment(*, client: Client, project_id: str, json_body: Experiment,) -> Union[Experiment, Error]:

    url = "{}/projects/{projectId}/experiments".format(client.base_url, projectId=project_id)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body.to_dict()

    response = httpx.post(url=url, headers=headers, json=json_json_body,)

    if response.status_code == 200:
        return Experiment.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 500:
        return Error.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)


def partial_update_experiment(*, client: Client, project_id: str, experiment_id: str, json_body: Experiment) -> Union[None, Error]:

    url = "{}/projects/{projectId}/experiments/{experimentId}".format(
        client.base_url, projectId=project_id, experimentId=experiment_id
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


def update_experiment_parameters(*, client: Client, project_id: str, experiment_id: str, parameters: Dict[str, Any]) -> Union[None, Error]:

    url = "{}/projects/{projectId}/experiments/{experimentId}/parameters".format(
        client.base_url, projectId=project_id, experimentId=experiment_id
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


def update_experiment_metrics(*, client: Client, project_id: str, experiment_id: str, metrics: Dict[str, Any]) -> Union[None, Error]:

    url = "{}/projects/{projectId}/experiments/{experimentId}/metrics".format(
        client.base_url, projectId=project_id, experimentId=experiment_id
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
