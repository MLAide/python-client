from typing import Any, Dict, Optional, cast

import httpx

from ..client import Client
from ..errors import ApiResponseError
from ..models.error import Error
from ..models.project import Project
from ..models.projects import Projects


def list_projects(*, client: Client,) -> Projects:

    """  """
    url = "{}/projects".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    response = httpx.get(url=url, headers=headers,)

    if response.status_code == 200:
        return Projects.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response, error=Error.from_dict(cast(Dict[str, Any], response.json())))


def create_project(*, client: Client, json_body: Project,) -> Project:

    """  """
    url = "{}/projects".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body.to_dict()

    response = httpx.post(url=url, headers=headers, json=json_json_body,)

    if response.status_code == 200:
        return Project.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response, error=Error.from_dict(cast(Dict[str, Any], response.json())))


def show_project_by_id(*, client: Client, project_key: str, ) -> Optional[Project]:

    """  """
    url = "{}/projects/{projectKey}".format(client.base_url, projectKey=project_key)

    headers: Dict[str, Any] = client.get_headers()

    response = httpx.get(url=url, headers=headers,)

    if response.status_code == 200:
        return Project.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 404:
        return None
    else:
        raise ApiResponseError(response=response, error=Error.from_dict(cast(Dict[str, Any], response.json())))
