from dataclasses import asdict
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ..client import AuthenticatedClient, Client
from ..errors import ApiResponseError
from ..models.error import Error
from ..models.experiment import Run
from ..models.experiments import Experiments


async def list_experiments(*, client: Client, project_id: str,) -> Union[Run, Error]:

    """  """
    url = "{}/projects/{projectId}/experiments".format(client.base_url, projectId=project_id,)

    headers: Dict[str, Any] = client.get_headers()

    async with httpx.AsyncClient() as _client:
        response = await _client.get(url=url, headers=headers,)

    if response.status_code == 200:
        return Run.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 500:
        return Error.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)


async def create_experiment(*, client: Client, project_id: str, json_body: Run, ) -> Union[Experiments, Error]:

    """  """
    url = "{}/projects/{projectId}/experiments".format(client.base_url, projectId=project_id,)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body.to_dict()

    async with httpx.AsyncClient() as _client:
        response = await _client.post(url=url, headers=headers, json=json_json_body,)

    if response.status_code == 200:
        return Experiments.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 500:
        return Error.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)


async def partial_update_experiment(*, client: Client, project_id: str, experiment_id: str,) -> Union[None, Error]:

    """ Update an existing experiment. This operation executes a partial update. That means, that only properties that should be modified must be contained in the request body. Only the status, parameters and metrics can be updated. If you update parameters or metrics with this operation, all existing parameters/metrics are replaced. If you want to add a parameter/metric to the existing ones, you should use PUT /projects/{projectId}/experiments/{experimentId}/parameters or PUT /projects/{projectId}/experiments/{experimentId}/metrics """
    url = "{}/projects/{projectId}/experiments/{experimentId}".format(
        client.base_url, projectId=project_id, experimentId=experiment_id,
    )

    headers: Dict[str, Any] = client.get_headers()

    async with httpx.AsyncClient() as _client:
        response = await _client.patch(url=url, headers=headers,)

    if response.status_code == 204:
        return None
    if response.status_code == 500:
        return Error.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)


async def update_experiment_parameters(*, client: Client, project_id: str, experiment_id: str,) -> Union[None, Error]:

    """  """
    url = "{}/projects/{projectId}/experiments/{experimentId}/parameters".format(
        client.base_url, projectId=project_id, experimentId=experiment_id,
    )

    headers: Dict[str, Any] = client.get_headers()

    async with httpx.AsyncClient() as _client:
        response = await _client.patch(url=url, headers=headers,)

    if response.status_code == 204:
        return None
    if response.status_code == 500:
        return Error.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)


async def update_experiment_metrics(*, client: Client, project_id: str, experiment_id: str,) -> Union[None, Error]:

    """  """
    url = "{}/projects/{projectId}/experiments/{experimentId}/metrics".format(
        client.base_url, projectId=project_id, experimentId=experiment_id,
    )

    headers: Dict[str, Any] = client.get_headers()

    async with httpx.AsyncClient() as _client:
        response = await _client.patch(url=url, headers=headers,)

    if response.status_code == 204:
        return None
    if response.status_code == 500:
        return Error.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)
