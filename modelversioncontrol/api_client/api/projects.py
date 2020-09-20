from dataclasses import asdict
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ..client import AuthenticatedClient, Client
from ..errors import ApiResponseError
from ..models.error import Error
from ..models.project import Project
from ..models.projects import Projects


def list_projects(*, client: Client,) -> Union[Projects, Error]:

    """  """
    url = "{}/projects".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    response = httpx.get(url=url, headers=headers,)

    if response.status_code == 200:
        return Projects.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 500:
        return Error.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)


def create_project(*, client: Client, json_body: Project,) -> Union[Project, Error]:

    """  """
    url = "{}/projects".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body.to_dict()

    response = httpx.post(url=url, headers=headers, json=json_json_body,)

    if response.status_code == 200:
        return Project.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 500:
        return Error.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)


def show_project_by_id(*, client: Client, project_id: str,) -> Union[Project, None, Error]:

    """  """
    url = "{}/projects/{projectId}".format(client.base_url, projectId=project_id)

    headers: Dict[str, Any] = client.get_headers()

    response = httpx.get(url=url, headers=headers,)

    if response.status_code == 200:
        return Project.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 404:
        return None
    if response.status_code == 500:
        return Error.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)
