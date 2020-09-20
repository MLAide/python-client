from __future__ import annotations
import os
from typing import Optional, Dict, Any
from dataclasses import dataclass
from modelversioncontrol.active_experiment import ActiveExperiment
from modelversioncontrol.api_client import AuthenticatedClient


@dataclass
class MvcOptions:
    mvc_server_url: Optional[str]
    api_token: Optional[str]

    def __init__(self, mvc_server_url: str = None, api_token: str = None):
        self.mvc_server_url = mvc_server_url
        self.api_token = api_token


    def to_dict(self) -> Dict[str, Any]:
        d = {
            "mvc_server_url": self.mvc_server_url,
            "api_token": self.api_token
        }

        # Remove values from dict that are None
        return {k: v for k, v in d.items() if v is not None}

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> MvcOptions:
        if d is None:
            d = dict()

        options = MvcOptions(
            mvc_server_url=d.get("mvc_server_url", None),
            api_token=d.get("api_token", None)
        )

        return options


class MvcClient:
    __options: MvcOptions
    __api_client: AuthenticatedClient

    def __init__(self, options: MvcOptions = None):
        if options is None:
            self.__options = MvcClient.__get_default_options()
        else:
            self.__options = MvcClient.__merge_options(MvcClient.__get_default_options(), options)

        self.__api_client = AuthenticatedClient(self.__options.mvc_server_url, self.__options.api_token)

    def start_new_experiment(self, project_id: str, experiment_name: str = None) -> ActiveExperiment:
        return ActiveExperiment(self.__api_client, project_id, experiment_name)

    @staticmethod
    def __get_default_options() -> MvcOptions:
        options = MvcOptions()
        options.mvc_server_url = "http://localhost:9000/api/v1"
        options.api_token = os.environ.get('MVC_API_TOKEN')
        return options

    @staticmethod
    def __merge_options(target: MvcOptions, source: MvcOptions) -> MvcOptions:
        merged = dict()
        merged.update(target.to_dict())
        merged.update(source.to_dict())

        return MvcOptions.from_dict(merged)
