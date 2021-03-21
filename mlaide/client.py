from __future__ import annotations

import os
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

from ._api_client import Client, AuthenticatedClient
from .active_run import ActiveRun
from .active_artifact import ActiveArtifact
from .model import ArtifactRef


@dataclass
class ConnectionOptions:
    """Specify options for a MLAideClient"""

    server_url: Optional[str]
    api_key: Optional[str]

    def __init__(self, server_url: str = None, api_key: str = None):
        self.server_url = server_url
        self.api_key = api_key

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "server_url": self.server_url,
            "api_key": self.api_key
        }

        # Remove values from dict that are None
        return {k: v for k, v in d.items() if v is not None}

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> ConnectionOptions:
        if d is None:
            d = dict()

        options = ConnectionOptions(
            server_url=d.get("server_url", None),
            api_key=d.get("api_key", None)
        )

        return options


class MLAideClient:
    """This is the main entry point to use this library. Creates a connection to the ML Aide server and provides
    read and write access to all resources.
    """

    __options: ConnectionOptions
    __api_client: Client
    __project_key: str

    def __init__(self, project_key: str, options: ConnectionOptions = None):
        """Creates a new instance of this class.

        Arguments:
            project_key: The key of the project, that should be accessed. All operations will be made on this project.
            options: Optional options that will be used to establish a connection.
        """
        if project_key is None:
            raise ValueError("project key must be not None")
        self.__project_key = project_key

        if options is None:
            self.__options = MLAideClient.__get_default_options()
        else:
            self.__options = MLAideClient.__merge_options(MLAideClient.__get_default_options(), options)

        self.__api_client = AuthenticatedClient(base_url=self.__options.server_url,
                                                api_key=self.__options.api_key)

    def start_new_run(self,
                      experiment_key: str = None,
                      run_name: str = None,
                      used_artifacts: List[ArtifactRef] = None) -> ActiveRun:
        """Creates and starts a new run, that will be assigned to the specified experiment. The run object can be used to \
        log all necessary information.

        Arguments:
            experiment_key: The key of the experiment, that the new run should be assigned to. If `None` a new, random \
            experiment will be created.
            run_name: The name of the run. The name helps to identify the run for humans. If `None` a random name will \
            be used.
            used_artifacts: An optional list of `ArtifactRef` that references artifacts, that are used as input for \
            this run. This information will help to create and visualize the experiment lineage.

        Returns:
            This object encapsulates the newly created run and provides functions to log all information \
            that belongs to the run.
        """
        return ActiveRun(self.__api_client, self.__project_key, experiment_key, run_name, used_artifacts)

    def get_artifact(self, artifact_name: str, artifact_version: str) -> ActiveArtifact:
        return ActiveArtifact(self.__api_client, self.__project_key, artifact_name, artifact_version)

    @property
    def options(self) -> ConnectionOptions:
        return self.__options

    @property
    def api_client(self) -> Client:
        return self.__api_client

    @staticmethod
    def __get_default_options() -> ConnectionOptions:
        options = ConnectionOptions()
        options.server_url = 'http://localhost:9000/api/v1'
        options.api_key = os.environ.get('MLAIDE_API_KEY')
        return options

    @staticmethod
    def __merge_options(target: ConnectionOptions, source: ConnectionOptions) -> ConnectionOptions:
        merged = dict()
        merged.update(target.to_dict())
        merged.update(source.to_dict())

        return ConnectionOptions.from_dict(merged)
