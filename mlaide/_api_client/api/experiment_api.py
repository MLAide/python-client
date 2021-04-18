from typing import Any, cast, Dict, Optional

import httpx

from ..client import Client
from ..errors import ApiResponseError
from ..dto import ExperimentDto, Error


def create_experiment(*, client: Client, project_key: str, experiment: ExperimentDto) -> ExperimentDto:

    url = "{}/projects/{projectKey}/experiments".format(client.base_url, projectKey=project_key)

    headers: Dict[str, Any] = client.get_headers()

    json_body = experiment.to_dict_without_none_values()

    response = httpx.post(url=url, headers=headers, json=json_body)

    if response.status_code == 200:
        return ExperimentDto.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response, error=Error.from_dict(cast(Dict[str, Any], response.json())))


def get_experiment(*, client: Client,
                   project_key: str,
                   experiment_key: str) -> Optional[ExperimentDto]:
    url = "{}/projects/{projectKey}/experiments/{experimentKey}" \
        .format(client.base_url, projectKey=project_key, experimentKey=experiment_key)

    headers: Dict[str, Any] = client.get_headers()

    response = httpx.request(
        method="GET",
        url=url,
        headers=headers,
    )

    if response.status_code == 200:
        return ExperimentDto.from_dict(cast(Dict[str, Any], response.json()))
    elif response.status_code == 404:
        return None
    else:
        raise ApiResponseError(response=response, error=Error.from_response(response))
