from __future__ import annotations

import os
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

from ._api_client import AuthenticatedClient
from .active_run import ActiveRun
from .active_artifact import ActiveArtifact
from .model import ArtifactRef


@dataclass
class MvcOptions:
    mvc_server_url: Optional[str]
    api_key: Optional[str]

    def __init__(self, mvc_server_url: str = None, api_key: str = None):
        self.mvc_server_url = mvc_server_url
        self.api_key = api_key

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "mvc_server_url": self.mvc_server_url,
            "api_key": self.api_key
        }

        # Remove values from dict that are None
        return {k: v for k, v in d.items() if v is not None}

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> MvcOptions:
        if d is None:
            d = dict()

        options = MvcOptions(
            mvc_server_url=d.get("mvc_server_url", None),
            api_key=d.get("api_key", None)
        )

        return options


class MvcClient:
    __options: MvcOptions
    __api_client: AuthenticatedClient
    __project_key: str

    def __init__(self, project_key: str, options: MvcOptions = None):
        if project_key is None:
            raise ValueError("project key must be not None")
        self.__project_key = project_key

        if options is None:
            self.__options = MvcClient.__get_default_options()
        else:
            self.__options = MvcClient.__merge_options(MvcClient.__get_default_options(), options)

        self.__api_client = AuthenticatedClient(base_url=self.__options.mvc_server_url,
                                                api_key=self.__options.api_key)

    def start_new_run(self,
                      experiment_key: str = None,
                      run_name: str = None,
                      used_artifacts: List[ArtifactRef] = None) -> ActiveRun:
        return ActiveRun(self.__api_client, self.__project_key, experiment_key, run_name, used_artifacts)

    def get_artifact(self, artifact_name: str, artifact_version: str) -> ActiveArtifact:
        return ActiveArtifact(self.__api_client, self.__project_key, artifact_name, artifact_version)


    @staticmethod
    def __get_default_options() -> MvcOptions:
        options = MvcOptions()
        options.mvc_server_url = "http://localhost:9000/api/v1"
        options.api_key = os.environ.get('MVC_API_KEY')
        return options

    @staticmethod
    def __merge_options(target: MvcOptions, source: MvcOptions) -> MvcOptions:
        merged = dict()
        merged.update(target.to_dict())
        merged.update(source.to_dict())

        return MvcOptions.from_dict(merged)
